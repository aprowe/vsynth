from VSynth import *

vs = VSynth()

def setup():
	size(1440,900, P3D)
	textureMode(NORMAL)

	vs.append(VineArray(), 'vines')
	vs.append_mode(Default())
	vs.append_mode(Follow())

	vs.set_mode('follow')


def draw():
	background(255)
	vs.render()

class Vine(Positional):

	def init(s):
		s.theta = random(0,TWO_PI)
		s.phi = random(0, PI)
		s.speed = 5.0
		s.attach_behavior('wrap', 'theta')
		s.points = [(0,0,0)]

	def pos(s):
		return (s.x,s.y,s.z)

	def angle(s):
		return (s.theta, s.phi, s.speed)

	def update(s):
		s.points.append((s.x,s.y,s.z))
		(dx, dy, dz) = toCart(*s.angle())
		# s.x += s.speed * sin(s.theta)
		# s.y += s.speed * cos(s.theta)
		s.x += dx
		s.y += dy
		s.z += dz

		if len(s.points) > 500:
			del s.points[0]


	def draw(s):
		stroke(0)
		weight = 10
		min_weight = 0.8
		for p1, p2 in zip(s.points[0:-1], s.points[1:]):
			weight -= (weight-min_weight)*0.05
			strokeWeight(weight)
			line(*(p2+p1))


class VineArray(Substack):

	def init(s):
		s.append_array(Vine, 10)
		s.x = 0
		s.y = 0
		s.z = 0

	def pos(s):
		return (s.x,s.y,s.z)

	def update(s):
		s.x = s.get(0).x
		s.y = s.get(0).y

class Default(Mode):

	def update_vine(mode, s):
		s.theta += s.noise(amplitude = 1.0)
		s.phi += s.noise(amplitude = 1.0)

	def update_camera3D(mode, s):
		# s.follow(s.stack('vines'))
		s.theta += 0.01
		s.phi += 0.00

		(s.x, s.y, s.z) = toCart(*(s.theta, s.phi, 1000))
		# s.follow()

class Follow(Default):

	def update_camera3D(mode, s):
		# s.follow(s.stack('vines'))
		s.target = s.stack('vines').pos()
		s.theta += 0.01
		s.phi += 0.00

		(s.x, s.y, s.z) = toCart(*(s.theta, s.phi, 1000))
		# s.follow()