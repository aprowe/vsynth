from VSynth import *
from auxiliary import *

vs = VSynth()
Latchable.Stack = vs

def setup():
	size(1440,900, P3D)
	textureMode(NORMAL);

def draw():
	background(0)
	vs.render()
