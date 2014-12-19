from types import MethodType
			
class Mode(object):

	def __init__(s, label=None):
		s.label = label if label else s.name()

	def init(s, stack):
		pass

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

	def __str__(s):
		return s.label
