from abstracts import *
from Noise import *
from CameraController import *

class Vine(Latchable):

	MAX_LENGTH = 600

	def __init__ (s, origin_x=0, origin_y=0, origin_theta = None, speed = 10):
		super(Vine, s).__init__()

		s.x = origin_x
		s.y = origin_y
		s.theta = origin_theta if origin_theta else random(0, 2*PI)
		s.speed = speed	

		s.weight_factor = 1.01

		s.points = [(s.x, s.y)]

		s.fn = Fn()


	def X(s):
		return s.x

	def Y(s):
		return s.y


	def update(s):
		s.theta += s.get('theta_wander')

		s.theta += (PI/2 - s.theta)* 0.05 #* ( Fn.sin(10, 0.05, 0.1) )

		s.x += sin(s.theta) * s.get('speed')
		s.y += cos(s.theta) * s.get('speed')
		s.points.append ((s.x, s.y))

		if len(s.points) > Vine.MAX_LENGTH:
			del s.points[0]

		if frameCount > 120:
			s.mode('sharp_wander')

	def draw(s):
		points_list = zip(s.points[0:-1], s.points[1:])

		stroke_weight = 0.1
		stroke(0,200)
		for points in reversed (points_list):
			stroke_weight += (15 - stroke_weight) * 0.01
			strokeWeight (stroke_weight)
			line (points[0][0], points[0][1], points[1][0], points[1][1])

	def connect(s, stack):
		modes = {
			'normal': {
				'signal': stack['audio'].mix,
				'speed': lambda: s.speed * (1 + s.get('signal', 1.0)) ,
				'wander': lambda: 0.1 + 0.05 * Fn.sin(1000.),
				'theta_wander': lambda: s.fn.noise() * 0.5 
			}, 
			'sharp': {
				'theta_wander': lambda: s.fn.noise() * 5.0
			},
			'sharp_wander': {
				'theta_wander': lambda: s.fn.noise() * s.get('wander')*10
			}
		}



		s.addModes(modes)


class Bead(Latchable):

	MAX_SIZE = 10
	GROWTH = .04

	def __init__(s, x, y):
		super(Bead, s).__init__()
		s.x = x + random(-100, 100)
		s.y = y + random(-100,100)

		s.size = 0
		s.active = True

	def update(s):
		s.size += (Bead.MAX_SIZE - s.size)* Bead.GROWTH

		if s.size > Bead.MAX_SIZE * .999:
			s.active = False

	def draw(s):
		noStroke()
		fill(0)
		ellipse(s.x, s.y, s.size, s.size)


class VineArray(Latchable):

	def __init__(s, length):
		super(VineArray, s).__init__()
		s.vines = [Vine() for i in xrange(length)]

	def update(s):
		[vine.update() for vine in s.vines]

		# if random(1) < s.get('signal',1):
			# s.vines.append(Vine(s, s.vines[0].X(), s.vines[0].Y()))
			

		if len(s.vines) > 30:
			del s.vines[1]


	def connect(s, stack):
		s.latch('signal', stack['audio'].mix)
		[v.connect(stack) for v in s.vines]


	def draw(s):
		[vine.draw() for vine in s.vines]


