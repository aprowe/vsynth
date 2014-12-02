from Stack import *
from Controllers import *


class VSynth(Stack):

	def __init__(self):
		Latchable.stack = self
		super(VSynth, self).__init__()
		self.add('camera', CameraController())
		self.add('audio', AudioController())
		self.add('midi', MidiController())
		self.current_mode = 'default'


	def set_mode(self, mode):
		self.current_mode = mode
		self.call('set_mode', mode)

	def render(self):
		self.call('update')
		self.call('draw')