from abstracts import *
from Noise import *
from CameraController import *

class Vine(Latchable):

	MAX_LENGTH = 600

	def __init__ (s, tangle, origin_x, origin_y, origin_theta = None, speed = 10):
		super(Vine, s).__init__()

		s.x = origin_x
		s.y = origin_y
		s.theta = origin_theta if origin_theta else random(0, 2*PI)
		s.speed = speed	

		s.weight_factor = 1.01

		s.points = [(s.x, s.y)]

		s.functions = tangle.functions
		s.fn = Fn()


	def X(s):
		return s.x

	def Y(s):
		return s.y

	def update(s):
		s.theta += s.fn.frame()

		s.theta += (PI/2 - s.theta) * 0.1

		if s.get('signal') > random(.09, .2):
			s.theta += random(-1,1)

		s.x += sin(s.theta) * s.speed
		s.y += cos(s.theta) * s.speed
		s.points.append ((s.x, s.y))

		if len(s.points) > Vine.MAX_LENGTH:
			del s.points[0]

	def draw(s):
		points_list = zip(s.points[0:-1], s.points[1:])

		stroke_weight = 0.1
		stroke(0,200)
		for points in reversed (points_list):
			stroke_weight += (15 - stroke_weight) * 0.01
			strokeWeight (stroke_weight)
			line (points[0][0], points[0][1], points[1][0], points[1][1])

	def connect(s, stack):
		s.latch('signal', stack[1].mix )


class Tangle(Latchable):

	def __init__(s, length):
		super(Tangle, s).__init__()
		s.vines = [Vine(s, random(width)-width/2, random(height)-height/2) for i in xrange(length)]




	def update(s):
		[vine.update() for vine in s.vines]

		if random(1) < s.get('signal',2):
			s.vines.append(Vine(s, s.vines[0].X(), s.vines[0].Y()))
			

		# sg = sig
		# while( sg > 0.10):
			# sg -= .10
		# if random(1) < 0.01:
			# s.vines.append(Vine(s.vines[0].X(), s.vines[0].Y()))

		if len(s.vines) > 30:
			del s.vines[1]

	def connect(s, stack):
		s.latch('signal', stack[1].mix )


	def draw(s):
		[vine.draw() for vine in s.vines]


