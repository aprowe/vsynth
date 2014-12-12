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

	vs.set_mode('intro')

def draw():
	background(0)
	vs.render()


class Line(Positional):

	MAX_LENGTH = 600

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

		if i >= len(s.points)-1:
			i = len(s.points)-2

		I = int(i)
		R = i-I

		inter = interpolate(s.points[I], s.points[I+1], R)
		return inter
		# return s.points[I]

	def get_angle(s, i):
		i = i - (s.length - Line.MAX_LENGTH)

		if i < 0:
			i = 0

		if i >= len(s.angles)-1:
			i = len(s.angles)-2

		I = int(i)
		R = i-I

		inter = interpolate(s.angles[I], s.angles[I+1], R)
		return inter
		# return s.angles[I]


	def mid_point(s):
		return len(s.points)/2.0

	def update(s):
		while s.index + Line.MAX_LENGTH > s.length:
			s.extend()

	def extend(s):
		s.theta = normalize(s.theta, PI/6)
		s.phi= normalize(s.phi, PI)

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


	def update_default(s):	
		i = s.length

		speed = 1/60.0
		amplitude = 0.05
		s.phi 	+= (noise(i*speed, 0)-0.5) * amplitude*5
		s.theta += (noise(i*speed, 100)-0.5) * amplitude

		s.theta += 0.01
		s.phi = s.approach(s.phi, 0, 0.01)
		# s.phi = s.approach(s.phi, s.lfo(amplitude=2*PI, period=0.1)	

	def update_straight(s):
		amplitude = 0
		s.theta = s.approach(s.theta, 0)
		# s.theta += s.lfo(amplitude=0.01, period = 10.0)
		s.phi += s.lfo(amplitude=vs['audio'].signal()*5.0)

	def update_slow(s):
		# s.phi = PI/2.0
		s.phi += 0.01
		s.theta = 0.2
		# s.phi = s.noise(speed=100.0)

	def update_intro(s):
		s.theta = 0.4
		s.phi += 0.02





class Cam(Latchable):

	def init(s):
		s.line = vs['line']
		s.lookahead = 100
		s.index = -10
		s.pos = (0,0,0)
		s.speed = 0

	def draw(s):
		cam = s.pos + s.target + (0, 1, 0)
		camera(*cam)

		pointLight(255,255,255,*s.line.get_point(s.index+30))

	def update(s):
		s.index += s.speed
		s.line.index = s.index
		s.pos = s.line.get_point(s.index)
		s.target = s.line.get_point(s.index + s.lookahead)

	# def update_default(s): 
		# s.speed = s.approach(s.speed, s.signal()*10, 0.05)

	def update_default(s): 
		if vs['audio'].beat.isKick():
			s.speed -= 0.5

		if vs['audio'].beat.isSnare():
			s.speed = 3

		if s.speed < 0.75:
			s.speed = 0.75



		s.speed = s.approach(s.speed, s.signal(10.), 0.01)

	def update_straight(s):
		s.speed = 2 + s.lfo(period=5.0)

	def update_slow(s):
		s.speed = 0.5

	def update_intro(s):
		s.speed = 1.0



class Tunnel(Latchable):

	WIDTH = 300
	TAPER = 0.5
	SIDES = 30

	def init(s):
		s.line = vs['line']
		s.block_size = 10
		s.min = 0
		s.max = 100
		# s.texture = loadImage('texture.jpg')
		# s.texture = loadImage('texture2.jpg')
		# s.texture = loadImage('babe.jpg')
		s.texture = loadImage('pattern-2.jpg')
		s.off = 0
		s.width = 1.0
		s.width_factor = 1.0
		s.brightness = 1.0
		s.length=1

	def interval(s):
		floor = lambda i,j: i - i % j
		return range( floor(vs['line'].length-s.length, s.block_size), vs['line'].length, s.block_size)

	def update_default(s):
		if vs['audio'].beat.isKick():
			s.brightness = 1.0

		s.brightness = s.approach(s.brightness, 0.5, 0.01)

	def update_straight(s):
		s.update_default()
		s.width_factor = 0.85

	def update_slow(s):
		s.width = 1 + 0.1*s.lfo(period = 4.0)

	def update_intro(s):
		s.update_default()
		s.length = s.approach(s.length, Line.MAX_LENGTH, 0.01)
		if frameCount == 179:
			s.length = Line.MAX_LENGTH

	def draw(s):
		fill(0,255,255)
		noStroke()
		s.off += 0.1
		if s.off >= s.block_size:
			s.off = 0

		width = 1.0

		for i in s.interval():
			i += s.off
			p1 = s.line.get_point(i)
			a1 = s.line.get_angle(i)
			p2 = s.line.get_point(i + s.block_size)
			a2 = s.line.get_angle(i + s.block_size)

			width *= s.width_factor
			if width < 0.1:
				width = 0.1

			width *= s.width

			pushMatrix()
			translate(*s.line.get_point(i))
			rotateZ(a1[1])
			rotateY(a1[0])
			n = [noise(i*0.01, j)*255*s.brightness for j in range(3)]
			tint(n[0],n[1], n[2])
			cylinder(Tunnel.WIDTH*0.7, Tunnel.TAPER*Tunnel.WIDTH*width, 
				a1[2]*s.block_size*3, Tunnel.SIDES, s.texture)
			popMatrix()
