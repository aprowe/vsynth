
from CameraController import *
from Tangle import *

# camera = 0
# audio  = 1
# vines  =


def setup():
	global stack
	stack = Stack()

	size(1440, 900)

	stack.add('camera', CameraController())
	stack.add('audio', AudioController())
	stack.add('vines', VineArray(1))

	stack.call('connect', stack)


def draw():
	update()
	background (247, 227, 200)
	stack.call('draw')


def update():
	stack.call('update')



class Stack(dict):

	def __init__(s):
		super(Stack, s).__init__()
		s.order = list()

	def add(s, label, runnable):
		s[label] = runnable
		s.order.append(label)

	def call(s, fn, *args):
		[getattr(s[item], fn)(*args) for item in s.order]


