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
	vs.add('pyra',PyramidArray())

	vs.set_mode('default')

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
		s.theta = bound(s.theta, PI/6)
		s.phi = wrap(s.phi)

		while s.index + Line.MAX_LENGTH-10 > s.length:
			s.extend()

	def extend(s):

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
		s.phi += 0.01


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

		pointLight(255,255,255,*s.line.get_point(s.index+30.0))

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
			s.speed = 3.0

		if s.speed < 0.75:
			s.speed = 0.75



		s.speed = s.approach(s.speed, s.signal(10.), 0.01)

	def update_straight(s):
		s.speed = 2.0 + s.lfo(period=5.0)

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
		s.length = Line.MAX_LENGTH
		s.segment_length = 10
		s.radius = 1.0
		s.taper_factor = 0.99
		
		s.offset = 0
		s.speed = 0.1
		
		s.texture = loadImage('texture.jpg')
		# s.texture = loadImage('pattern-2.jpg')
		s.brightness = 1.0

	def interval(s):
		floor = lambda i,j: i - i % j
		return range( 
			floor(vs['line'].length-s.length, s.segment_length), 
			vs['line'].length, 
			s.segment_length)

	def update(s):
		s.offset += s.speed
		s.offset = wrap(s.offset, s.segment_length)

	def update_default(s):
		if vs['audio'].beat.isKick():
			s.brightness = 1.0

		s.brightness = s.approach(s.brightness, 0.5, 0.01)

	def update_straight(s):
		s.update_default()
		s.taper_factor = 0.85

	def update_slow(s):
		# s.raius = 1.5
		s.radius = 1 + 0.1*s.lfo(period = 4.0)

	def update_intro(s):
		s.radius = s.approach(s.radius, 100.0)
		# s.update_default()
		# s.length = s.approach(s.length*1.0, Line.MAX_LENGTH*1.0, 0.01)

		# if frameCount >= 179:
			# s.length = Line.MAX_LENGTH


	def draw(s):
		fill(0,255,255)
		noStroke()
		
		radius = 1.0

		for i in s.interval():
			i += s.offset
			p1 = s.line.get_point(i)
			a1 = s.line.get_angle(i)
			p2 = s.line.get_point(i + s.segment_length)
			a2 = s.line.get_angle(i + s.segment_length)

			## Taper the tunnel to the minimum radius
			radius *= s.taper_factor
			if radius < 0.1:
				radius = 0.1
			radius *= s.radius

			pushMatrix()

			# Translate / Rotate
			translate(*s.line.get_point(i))
			rotateZ(a1[1])
			rotateY(a1[0])

			# Random Color
			n = [noise(i*0.01, j)*255*s.brightness for j in range(3)]
			tint(n[0],n[1], n[2])

			# Draw the Cylinder
			cylinder(
				Tunnel.WIDTH*0.7, 
				Tunnel.TAPER*Tunnel.WIDTH*radius, 
				a1[2]*s.segment_length*3, 
				Tunnel.SIDES, 
				s.texture )
			popMatrix()



class Pyramid(Positional):

	texture = None

	def init(s):
		s.z = 0
		s.x = random(-500,500)
		s.y = random(-500,500)
		s.z = random(-500,500)
		s.size = random(3,50)
		s.theta = random(TWO_PI)
		s.phi= random(TWO_PI)
		s.texture = Pyramid.texture

	def update(s):
		s.theta += 0.1
		s.phi += 0.1
		# s.x = s.approach(s.x, vs['cam'].target[0], 0.01)
		# s.y = s.approach(s.y, vs['cam'].target[1], 0.01)
		# s.z = s.approach(s.z, vs['cam'].target[2], 0.01)

	def draw(s):
		noStroke()
		fill(255)

		pushMatrix();

		translate(s.x,s.y,s.z)
		rotateX(s.phi)
		rotateZ(s.theta)
		# ellipse(0,0,s.size, s.size)
		# tetrahedron(s.size, s.texture)
		popMatrix();


class PyramidArray(Positional):

	def init(s):
		Pyramid.texture = loadImage('texture.jpg')
		s.pyramids = [Pyramid() for p in range(100)]
		

	def update(s):
		[p.update() for p in s.pyramids]

	def draw(s):
		[p.draw() for p in s.pyramids]
