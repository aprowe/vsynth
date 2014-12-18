from types import MethodType
from auxilary import lcfirst
			
class Mode(object):

	def __init__(s, label=None):
		s.label = label if label else s.name()

	def init(s):
		pass

	@staticmethod
	def to_function_str(fn, latch):
		return fn+'_'+lcfirst(latch.__class__.__name__)

	def name(s):
		return	lcfirst(s.__class__.__name__)

	def attach_latch(s,latch):
		update_name = 'update_'+lcfirst(latch.__class__.__name__)

		if hasattr(s, update_name):
			mode_function = getattr(s, update_name)
			mode_function = MethodType(mode_function, latch, latch.__class__)
			setattr(latch, 'update_'+s.label, mode_function)

	def __str__(s):
		return s.label
