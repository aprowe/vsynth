from Stack import *
from Controllers import *
import random as rand

class VSynth(Stack):

	def __init__(self):
		super(VSynth, self).__init__()
		Latchable.Stack = self
		
		self.modes = [Mode('default')]
		self.current_mode = self.modes[0]

		self.append(CameraController(), 'camera')
		self.append(AudioController(), 'audio')
		self.append(MidiController(), 'midi')

	def append_mode(self, mode):
		if type(mode) is str:
			mode = Mode(mode)

		[mode.attach_latch(latch) for latch in self.dict.values()]
		self.modes.append(mode)

	def append(s, latch, label=None):
		[mode.attach_latch(latch) for mode in s.modes]
		super(VSynth, s).append(latch, label)

	def set_mode(self, mode):
		if type(mode) is str:
			mode = [m for m in self.modes if m.label == mode][0]

		self.current_mode = mode
		self.call('set_mode', mode.label)

	def render(self):
		self.call('render')
		self.mode_walk()

	def mode_walk(s, period=5.0):
		# if frameCount > 0:
			# return

		if random(1) < 1.0/(50.0*period):
			mode = rand.choice(s.modes)
			s.set_mode(mode)


from types import MethodType
			
class Mode(object):

	def __init__(s, label=None):
		s.label = label if label else s.name()

	@staticmethod
	def lcfirst(string):
		return string[:1].lower() + string[1:] if string else ''

	@staticmethod
	def to_function_str(fn, latch):
		return fn+'_'+Mode.lcfirst(latch.__class__.__name__)

	def name(s):
		return	Mode.lcfirst(s.__class__.__name__)

	def attach_latch(s,latch):
		update_name = 'update_'+Mode.lcfirst(latch.__class__.__name__)

		if hasattr(s, update_name):
			mode_function = getattr(s, update_name)
			mode_function = MethodType(mode_function, latch, latch.__class__)
			setattr(latch, 'update_'+s.label, mode_function)
			print getattr(latch, 'update_'+s.label)()

	def __str__(s):
		return s.label
