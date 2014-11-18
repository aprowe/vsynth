
from CameraController import *
from Tangle import *

# camera = 0
# audio  = 1
# vines  =


def setup():
	global stack
	stack = []

	size(1440, 900)

	stack.append (CameraController()) 
	stack.append (AudioController())
	stack.append (Tangle(1))
	# stack['audio'] = AudioController()
	# stack['audio'] = AudioController()
	# stack['vines'] = Tangle(1)

	[s.connect(stack) for s in stack]
	# stack[1].latch(stack[0])
	# stack['camera'].latch('x_follow', stack[1].vines[0].X )
	# stack[0].latch('y_follow', stack[1].vines[0].Y )

def draw():
	update()
	background (247, 227, 200)
	[s.draw() for s in stack]


def update():
	[s.update() for s in stack]



