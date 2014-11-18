from abstracts import *
from Noise import *

class CameraController(Stacker, Positional):

	def __init__(s, positional = None):
		s.x = s.y = 0
		s.scale = 1
		s.positional = positional if positional else None

	def update(s):
		if s.positional:
			s.x += (s.positional.x - s.x) * 0.03
			s.y += (s.positional.y - s.y) * 0.03

		# s.x += Noise.Frame(0)
		# s.y += Noise.Frame(1)
		# s.scale += Noise.Frame(2)/50

	def X():
		return X()

	def Y():
		return Y()

	def draw(s):
		translate (width/2, height/2)
		scale (s.scale)
		translate (-s.x, -s.y)

	def latch(s, positional):
		s.positional = positionalclass Noise:

	@staticmethod
	def Frame (seed = 0, seed2 = 0, speed = 60.0):
		return noise (float( frameCount / speed), seed, seed2) - 0.5

	def frame (s):
		return Noise.Frame(s.seed1, s.seed2)

	def __init__ (s, seed1 = None, seed2 = None):
		s.seed1 = seed1 if seed1 else random(-1000, 1000)
		s.seed2 = seed2 if seed2 else random(-1000, 1000)


from abstracts import *
from Noise import *
from CameraController import *

class Vine(Stacker):

	MAX_LENGTH = 600

	def __init__ (s, origin_x, origin_y, origin_theta = None, speed = 10):
		s.x = origin_x
		s.y = origin_y
		s.theta = origin_theta if origin_theta else random(0, 2*PI)
		s.speed = speed	

		s.weight_factor = 1.01

		s.points = [(s.x, s.y)]

		s.noise = Noise()

	def X(s):
		return s.x

	def Y(s):
		return s.y

	def update(s):
		s.theta += s.noise.frame()

		s.theta += (PI/2 - s.theta) * 0.1

		s.x += sin(s.theta) * s.speed
		s.y += cos(s.theta) * s.speed
		s.points.append ((s.x, s.y))

		if len(s.points) > Vine.MAX_LENGTH:
			del s.points[0]

	def draw(s):
		points_list = zip(s.points[0:-1], s.points[1:])

		stroke_weight = 0.1
		for points in reversed (points_list):
			stroke_weight += (15 - stroke_weight)*0.01
			strokeWeight (stroke_weight)
			line (points[0][0], points[0][1], points[1][0], points[1][1])


class Tangle():

	def __init__(s, length):
		s.vines = [Vine(random(width)-width/2, random(height)-height/2) for i in xrange(length)]

	def update(s):
		[vine.update() for vine in s.vines]

		# sg = sig
		# while( sg > 0.10):
			# sg -= .10
		if random(1) < 0.01:
			s.vines.append(Vine(s.vines[0].X(), s.vines[0].Y()))

		if len(s.vines) > 30:
			del s.vines[1]

	def draw(s):
		[vine.draw() for vine in s.vines]

	def latch(s, camera_controller):
		camera_controller.latch(s.vines[0])


class Stacker:
	def draw():
		pass

	def update():
		pass

class Positional:
	def X():
		pass

	def Y():
		passabstracts
from CameraController import *
from Tangle import *
from Noise import * 
from ddf.minim import Minim

minim = Minim(this)
mic = minim.getLineIn(1)
sig = 0

def average():
	sum=0
	for i in xrange(mic.bufferSize()):
		sum += sq(mic.mix.get(i))
	sum/= mic.bufferSize()
	return sqrt(sum);

def setup():
	global stack
	stack = []


	size(1440, 900)

	stack.append( CameraController() )
	stack.append( Tangle(1) )

	stack[1].latch(stack[0])

def draw():
	update()
	background (247, 227, 200)
	[s.draw() for s in stack]


def update():
	global sig
	sig = average()
	[s.update() for s in stack]



