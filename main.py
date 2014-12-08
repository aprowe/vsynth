from VSynth import *
from Math import *
from shapes import *

vs = VSynth()
Latchable.Stack = vs

def setup():
	size(1440,900, P3D)
	textureMode(NORMAL);
	vs.add('line',Line())
	vs.add('cam',Cam())
	vs.add('tunnel',Tunnel())

def draw():
	background(0)
	vs.render()


class Line(Positional):

	MAX_LENGTH = 100

	def init(s):
		s.x = s.y = s.z = 0
		
		s.phi = 0
		s.theta = PI/2.0
		s.speed = 5

		s.length = 1
		s.trim = 0

		s.points = [(0,0,0) for i in range(1)]
		s.angles = [(0,0, s.speed) for i in range(1)]

		s.index = 5

	def pos(s):
		return (s.x, s.y, s.z)

	def polar(s):
		return (s.theta, s.phi, s.speed)

	def get_point(s, i):
		i = i - (s.length - Line.MAX_LENGTH)

		if i < 0:
			i = 0

		if i >= len(s.points):
			i = len(s.points)-1
		return s.points[int(i)]

	def get_angle(s, i):
		i = i - (s.length - Line.MAX_LENGTH)

		if i < 0:
			i = 0

		if i >= len(s.angles):
			i = len(s.angles)-1
		return s.angles[int(i)]

	def mid_point(s):
		return len(s.points)/2.0

	def update(s):
		while s.index + Line.MAX_LENGTH/2.0 > s.length:
			s.extend()


	def extend(s, i=None, speed=1/60.0, amplitude=0.3):
		dx, dy, dz = toCart(*s.polar())

		s.x += dx
		s.y += dy
		s.z += dz

		s.points.append (s.pos())
		s.angles.append (s.polar())
		s.length += 1

		while len(s.points) > Line.MAX_LENGTH:
			del s.points[0]
		while len(s.angles) > Line.MAX_LENGTH:
			del s.angles[0]

		if i is None:
			i = s.length

		s.phi 	+= (noise(i*speed, 0)-0.5) * amplitude
		s.theta += (noise(i*speed, 100)-0.5) * amplitude

		s.theta = s.approach(s.theta, 0)
		s.phi = s.approach(s.phi, 0)


	# def draw(s):
	# 	fill(255)
	# 	stroke(255)
	# 	i = 0
	# 	j =0
	# 	for p1, p2 in zip(s.points, s.angles):
	# 		tint(s.noise(seed1=100.0, seed2=j)*100+155, s.noise(seed1=0.0,seed2=j)*100+155, s.noise(seed1=200,seed2=j)*100+255)
	# 		i += 1
	# 		j += 0.1
	# 		pushMatrix()
	# 		# line(*(p1 + p2))
	# 		translate(*p1)
	# 		rotateZ(p2[1])
	# 		rotateY(p2[0])
	# 		if i == 10:
	# 			i = 0
	# 			cylinder(250 + s.noise(seed1=j)*100, abs(s.noise(seed1=j)*250) + 250 , p2[2]*10, 30, s.texture)
	# 		# line(0,0,0,0,0,p2[2])
	# 		# line(5,0,0,5,0,p2[2])
	# 		# line(0,5,0,0,5,p2[2])
	# 		# line(-5,0,0,-5,0,p2[2])
	# 		# line(0,-5,0,0,-5,p2[2])
	# 		popMatrix()

class Cam(Latchable):

	def init(s):
		s.line = vs['line']
		s.lookahead = 20
		s.index = -10
		s.pos = (0,0,0)

	def draw(s):
		cam = s.pos + s.target + (0, 1, 0)
		# pushMatrix()
		# translate(*s.pos)
		# fill(0,0,255)
		# sphere(5)
		# popMatrix()
		camera(*cam)

	def update(s):
		s.index += random(2.0)
		s.line.index = s.index
		s.pos = s.line.get_point(s.index)
		s.target = s.line.get_point(s.index + s.lookahead)

class Tunnel(Latchable):

	def init(s):
		s.line = vs['line']
		s.block_size = 10
		s.min = 0
		s.max = 100
		s.texture = loadImage('texture.jpg')

	def interval(s):
		floor = lambda i,j: i - i % j
		return range( floor(vs['line'].length-Line.MAX_LENGTH, s.block_size), vs['line'].length, s.block_size)

	def draw(s):
		fill(0,255,255)
		noStroke()
		for i in s.interval():
			p1 = s.line.get_point(i)
			a1 = s.line.get_angle(i)
			p2 = s.line.get_point(i + s.block_size)
			a2 = s.line.get_angle(i + s.block_size)


			pushMatrix()
			translate(*s.line.get_point(i))
			rotateY(a1[1])
			rotateZ(a1[0])
			cylinder(250, 50, a1[2], 6, s.texture)
			popMatrix()
