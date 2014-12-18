from VSynth import *
from auxilary import *

vs = VSynth()

def setup():
	size(1440,900)
	textureMode(NORMAL)

	vs.append(Orb())

	vs.append_mode('smooth')
	vs.append_mode(Crazy())

	vs.set_mode('crazy')

def draw():
	background(0)
	vs.render()

class Orb(Positional):

	def init(s):
		s.attach_behavior(Bound(-10,10), 'x')
		s.attach_behavior(Bound(-10,10), 'y')

	def draw(s):
		fill(255)
		ellipse(s.x, s.y, 20, 20)

	def update_default(s):
		s.x += random(-1,1)
		s.y += random(-1,1)

	def update_smooth(s):
		s.x = s.lfo(amplitude=200, period=2)
		s.y = s.lfo(amplitude=200, period=2)

class Crazy(Mode):

	def update_orb(mode, s):
		s.x = s.noise(amplitude=200)
		s.y = s.noise(amplitude=200)
		mode 



# class WrapTheta(Behavior):

# 	def update(s, theta):
# 		if theta > TWO_PI:
# 			theta = 0

# 		if theta < 0:
# 			theta = TWO_PI

# 		return theta
