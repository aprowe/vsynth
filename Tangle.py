from abstracts import *
from Noise import *
from CameraController import *

class Vine(Latchable):

	MAX_LENGTH = 200

	def __init__ (s, origin_x=0, origin_y=0, theta=None, speed=15):
		s.x = origin_x
		s.y = origin_y
		s.theta = random(0, 2*PI) if theta is None else theta
		s.speed = speed
		s.weight_factor = 1.01
		s.points = [(s.x, s.y)]
		super(Vine, s).__init__()

	def update(s):
		super(Vine, s).update()
		print(s.speed)
		s.x += sin(s.theta) * s.speed
		s.y += cos(s.theta) * s.speed
		s.points.append ((s.x, s.y))

		if len(s.points) > Vine.MAX_LENGTH:
			del s.points[0]


	def draw(s):
		points_list = zip(s.points[0:-1], s.points[1:])

		stroke_weight = 0.1
		for points, index in zip(reversed (points_list), range(len(points_list))):
			mod = 1
			if index > Vine.MAX_LENGTH/2:
				mod = -1
			stroke_weight += (15 - stroke_weight) * 0.01 * mod
			strokeWeight (stroke_weight)
			line (points[0][0], points[0][1], points[1][0], points[1][1])



class VineArray(Latchable):

	def __init__(s, length=1):
		s.vines = [Vine() for i in xrange(length)]
		s.lastx = 0
		s.lasty = 0
		s.spawn = 0
		super(VineArray, s).__init__()

	def update(s):
		super(VineArray, s).update()
		[vine.update() for vine in s.vines]	

		for i in range(int(s.spawn)):
			s.vines.append (Vine(s.lastx, s.lasty))

		s.lastx = s.vines[0].x
		s.lasty = s.vines[0].y

		while len(s.vines) > 25:
			del s.vines[1]

	def draw(s):
		[vine.draw() for vine in s.vines]


