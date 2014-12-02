from Stack import *
from Controllers import *


class VSynth(Stack):

	def __init__(self):
		Latchable.Stack = self
		super(VSynth, self).__init__()
		self.current_mode = 'default'
		self.add('camera', CameraController())
		self.add('audio', AudioController())
		self.add('midi', MidiController())


	def set_mode(self, mode):
		self.current_mode = mode
		self.call('set_mode', mode)

	def render(self):
		self.call('update')
		self.call('draw')

		