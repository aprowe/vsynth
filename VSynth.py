from auxilary import *
from Stack import *
from Behavior import *
from Mode import *
from Latchable import *
from Substack import *
from Positional import *
from Controllers import *

import random as rand

class VSynth(Stack):

	def __init__(self):
		super(VSynth, self).__init__()
		
		self.modes = [Mode('default')]
		self.current_mode = self.modes[0]

		# self.append(CameraController(), 'camera')
		self.append(Camera3D(), 'camera3d')
		self.append(AudioController(), 'audio')
		self.append(MidiController(), 'midi')

	def append_mode(self, mode):
		if type(mode) is str:
			mode = Mode(mode)

		# [mode.attach_latch(latch) for latch in self.dict.values()]
		# [latch.append_mode(mode) for latch in self.dict.values()]
		self.call('append_mode', mode)

		self.modes.append(mode)

	def set_mode(self, mode):
		if type(mode) is str:
			mode = [m for m in self.modes if m.label == mode][0]

		self.current_mode = mode
		self.current_mode.init(self)
		self.call('set_mode', mode.label)

	def append(s, latch, label=None):
		[mode.attach_latch(latch) for mode in s.modes]
		super(VSynth, s).append(latch, label)

	def render(self):
		self.call('render')
		self.mode_walk()

	def mode_walk(s, period=5.0):
		# if frameCount > 0:
			# return

		if random(1) < 1.0/(50.0*period):
			mode = rand.choice(s.modes)
			s.set_mode(mode)


