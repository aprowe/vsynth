from abstracts import *
from Noise import *
from CameraController import *

class Vine(Latchable):

	MAX_LENGTH = 100
	SPEED = 10

	def __init__ (s, origin_x=0, origin_y=0, theta=None, speed=15):
		super(Vine, s).__init__()

		s.x = origin_x
		s.y = origin_y
		s.theta = random(0, 2*PI) if theta is None else theta
		s.speed = speed
		s.weight_factor = 1.01
		s.points = [(s.x, s.y)]

		noise = {
			'source': 'noise',
			'noise': {
				'amplitude': 1
			},
			'operator': 'add',
			'target':'theta'
		}

		# noise2 = {
		# 	'source': 'noise',
		# 	'noise': {
		# 		'amplitude': 100
		# 	},
		# 	'operator': 'add',
		# 	'target':'theta'
		# }

		s.latch(noise)
		# s.latch(noise2)


	def update(s):
		super(Vine, s).update()
		s.x += sin(s.theta) * s.speed
		s.y += cos(s.theta) * s.speed
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



class VineArray(Latchable):

	def __init__(s, length=1):
		super(VineArray, s).__init__()
		s.vines = [Vine() for i in xrange(length)]
		s.lastx = 0
		s.lasty = 0
		s.spawn = 0

		lastx = {
			'source': lambda: s.vines[0].x,
			'operator': 'equals',
			'target': 'lastx'
		}

		lasty = {
			'source': lambda: s.vines[0].y,
			'operator': 'equals',
			'target': 'lasty'
		}

		spawn = {
			'source': 'every',
			'operator': 'equals',
			'target': 'spawn'
		}

		s.latch(lastx)
		s.latch(lasty)
		s.latch(spawn)



	def update(s):
		super(VineArray, s).update()
		[vine.update() for vine in s.vines]
		print s.lasty

		if s.spawn:
			s.vines.append(Vine(s.lastx, s.lasty))


		if len(s.vines) > 20:
			del s.vines[1]



	def draw(s):
		[vine.draw() for vine in s.vines]


