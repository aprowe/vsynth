from VSynth import *

vs = VSynth()
Latchable.Stack = vs

def setup():
	size(1440,900, OPENGL)

def draw():
	vs.render()
