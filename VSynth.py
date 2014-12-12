from Stack import *
from Controllers import *
import random as rand

class VSynth(Stack):

	modes = ['straight','slow','default']

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
		self.call('render')
		self.mode_walk()
		# self.call('update')
		# self.call('draw')

	def mode_walk(s, period=5.0):
		# if frameCount > 0:
			# return


		if random(1) < 1.0/(50.0*period):
			mode = rand.choice(VSynth.modes)
			s.set_mode(mode)

			