

def setup():
	global stack
	stack = []

	size(1440, 900)

	stack.append( CameraController() )
	stack.append( Tangle(1) )

def draw():
	update()
	background (247, 227, 200)
	[s.draw() for s in stack]

def update():
	[s.update() for s in stack]


class Stacker:
	def draw():
		pass

	def update():
		pass

class Positional:
	def X():
		pass

	def Y():
		pass


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
		s.positional = positional



class Noise:

	@staticmethod
	def Frame (seed = 0, seed2 = 0, speed = 60.0):
		return noise (float( frameCount / speed), seed, seed2) - 0.5

	def frame (s):
		return Noise.Frame(s.seed1, s.seed2)

	def __init__ (s, seed1 = None, seed2 = None):
		s.seed1 = seed1 if seed1 else random(-1000, 1000)
		s.seed2 = seed2 if seed2 else random(-1000, 1000)

class Vine(Stacker):

	MAX_LENGTH = 1000

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




class Tangle(CameraController):

	def __init__(s, length):
		s.vines = [Vine(random(width)-width/2, random(height)-height/2) for i in xrange(length)]

		stack[0].latch(s.vines[0])

	def update(s):
		[vine.update() for vine in s.vines]

		if random(1) < 0.05:
			s.vines.append(Vine(s.vines[0].X(), s.vines[0].Y()))

		if len(s.vines) > 20:
			del s.vines[1]

	def draw(s):
		[vine.draw() for vine in s.vines]

