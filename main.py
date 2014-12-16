from VSynth import *
from auxilary import *

vs = VSynth()

def setup():
	size(1440,900)
	textureMode(NORMAL)

def draw():
	background(0)
	vs.render()
