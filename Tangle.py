from abstracts import *
from Noise import *
from CameraController import *

class Vine(Latchable):

	MAX_LENGTH = 600
	SPEED = 10

	def __init__ (s, origin_x=0, origin_y=0, theta=None, speed=10):
		super(Vine, s).__init__()

		s.x = origin_x
		s.y = origin_y
		s.theta = random(0, 2*PI) if theta is None else theta
		s.speed = speed

		s.weight_factor = 1.01

		s.points = [(s.x, s.y)]

		# Random Seeder
		s.fn = Fn()

		s.connect(Vine.stack)


	def X(s):
		return s.x

	def Y(s):
		return s.y


	def update(s):

		s.theta += s.get('theta')
		s.x += sin(s.theta) * s.get('speed')
		s.y += cos(s.theta) * s.get('speed')
		s.points.append ((s.x, s.y))

		if len(s.points) > Vine.MAX_LENGTH:
			del s.points[0]


	def draw(s):
		points_list = zip(s.points[0:-1], s.points[1:])

		stroke_weight = 0.1
		for points in reversed (points_list):
			stroke_weight += (15 - stroke_weight) * 0.01
			strokeWeight (stroke_weight)
			line (points[0][0], points[0][1], points[1][0], points[1][1])

	def connect(s, stack):
		modes = {
			'normal': {
				'signal': lambda: stack['audio'].mix(),
				'speed': lambda: s.speed * (1 + s.get('signal')) ,
				'wander': lambda: 0.1 + 0.05 * Fn.sin(1000.),
				'follow_angle': lambda: (PI/2 - s.theta)*0.1,
				'theta': lambda: s.get('follow_angle') + s.fn.noise()
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

	def __init__(s, length=1):
		super(VineArray, s).__init__()
		s.vines = [Vine() for i in xrange(length)]

	def update(s):
		[vine.update() for vine in s.vines]

		if s.get('spawn_rate'):
			s.spawn(s.get('spawn_amount'))

		if len(s.vines) > 30:
			del s.vines[1]

	def spawn(s, amount=0):
		[s.vines.append( Vine(*s.get('spawnling', None, i)) ) for i in range(amount)]

	def randomVine(s):
		return s.vines[ int(random(0, len(s.vines))) ] 


	def connect(s, stack):
		s.latch('signal', stack['audio'].mix)
		s.latch('spawn_rate', lambda: random(1) < s.get('signal'))
		s.latch('spawnling', lambda i: (s.vines[0].x, s.vines[0].y) )
		s.latch('spawn_amount', lambda: 1 )


		def spawnTwo(i):
			x = s.vines[0].x
			y = s.vines[0].y
			theta = s.vines[0].theta-PI/4 if i == 0 else s.vines[0].theta+PI/4
			return (x,y,theta)

		modes = {
			'fixed_rate': {
				'spawn_rate': lambda: Fn.every(2),
				'spawn_amount': lambda: 2,
				'spawnling': spawnTwo
			}
		}

		s.addModes(modes)

		s.mode('fixed_rate')

	def draw(s):
		[vine.draw() for vine in s.vines]


