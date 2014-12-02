from VSynth import *

vs = VSynth()
Latchable.Stack = vs

def setup():
	size(1440,900)
	vs.add('colors', Colors())
	vs.add('circles', CircleArray())

def draw():
	# background(0)
	fill(0,230)
	rect(-10000, -10000, 20000, 20000)
	vs.render()
	if (frameCount/120 % 5 == 0):
		vs.set_mode('colorChanging')
	elif (frameCount/120 % 5 == 3):
		vs.set_mode('focus')
	else:
		vs.set_mode('default')

class Colors(Latchable):

	COLORS = [
		[289,85,128],
		[240,195,100],
		[189,172,136],
		[86,151,140],
		[136,189,165]
	]

	def __init__(s):
		super(Colors, s).__init__()
		s.colors = Colors.COLORS
		s.speed = 1
		s.threshhold = 0.2


	def update(s):

		for x,a in enumerate(s.colors):
			for y,b in enumerate(s.colors[x]):
				s.colors[x][y] = s.move_color(s.colors[x][y], x, y, s.speed)
	
		s.shift_color()

		super(Colors, s).update()

	def move_color(s, i, seed1, seed2, speed):
		i += s.noise(speed, 100, seed1, seed2)
		if i > 255:
			i -= 255
		elif i < 0:
			i += 255

		return i

	def shift_color(s):
		if s.speed == 200:
			s.speed = 1

		if vs['audio'].mix() > s.threshhold:
			s.speed = 200


class CircleArray(Positional):

	def __init__(self, x=0, y=0):
		self.circles = list()
		Circle.parent = self
		self.rotation = 0
		WIDTH = 14.0
		HEIGHT = 9.0
		RADIUS = 10.0
		SPACING = 5.0
		for i in range(WIDTH*2):
			for j in range(HEIGHT*2):
				x = (i/WIDTH * width) - width
				y = (j/HEIGHT * height) - height
				self.circles.append(Circle(x, y, i, j))


				

		super(CircleArray, self).__init__(x, y)
		
	def update(self):
		[c.update() for c in self.circles]
		super(CircleArray, self).update()

	def draw(self):
		[c.draw() for c in self.circles]
		super(CircleArray, self).draw()

	def set_mode(self, mode):
		[c.set_mode(mode) for c in self.circles]

class Circle(Positional):
	COLORS = [
		[289,85,128],
		[240,195,100],
		[189,172,136],
		[86,151,140],
		[136,189,165]
	]

	def randomColor(s): 
		return Circle.COLORS[
			int(
				random(0, len(Circle.COLORS))
				)
			] 

	def __init__(s, x=0, y=0, i=0, j=0):
		s.color = int(random(0, len(Circle.COLORS)))
		s.radius = 25
		s.extra_radius = 0
		s.rotation = 0
		s.randomness = 0
		s.i = i
		s.j = j
		s.fill = Circle.COLORS[s.color]
		s.delay = (s.color + 1) * 0.02

		super(Circle, s).__init__(x,y)

	def update(s):
		s.bound()
		super(Circle, s).update()


	def bound(s):

		switch = False

		if s.x < vs['camera'].x - width:
			s.x += 2*width
			switch = True

		elif s.x > vs['camera'].x + width:
			s.x -= 2*width
			switch = True

		elif s.y < vs['camera'].y - height:
			s.y += 2*height
			switch = True

		elif s.y > vs['camera'].y + height:
			s.y -= 2*height
			switch = True

		if switch:
			s.fill= s.randomColor()



	def draw(s):
		# noStroke()
		strokeWeight(2)
		stroke(*s.fill)
		s.fill = vs['colors'].colors[s.color]
		# fill(*s.fill)
		radius = 1 - s.distance(Circle.parent)/float(width/4)
		radius += s.extra_radius
		radius *= s.radius

		x = s.x + s.noise(s.randomness, 500, s.i, s.j)
		y = s.y + s.noise(s.randomness, 500, s.i + 1000, s.j + 1000)

		if s.i is 14:
			s.y += 5 * (1 + 10.0*vs['audio'].mix())

		elif s.j is 1 or s.j is 2:
			s.x += 3


		# if radius > 100:
		# 	fill(*s.fill, alpha=150)

		rotate(s.rotation)
		ellipse(x, y, radius, radius)
		# fill(0)
		# ellipse(x, y, radius*0.9, radius*0.9)


