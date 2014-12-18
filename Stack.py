
class Stack(object):

	@staticmethod
	def subcall(instance, fn, *args):
		if hasattr(instance, 'call'):
			instance.call(fn, *args)

		if hasattr(instance, fn):
			getattr(instance, fn)(*args)


	def __init__(s):
		s.dict = dict()	
		s.order = list()

	def append(s, latchable, label=None):
		latchable.__stack__ = s

		if label is None:
			label = "latch_"+str(len(s.order))

		s.dict[label] = latchable
		s.order.append(label)

	def get(s, index):
		return s.dict[s.order[index]]


	def call(s, fn, *args):
		[Stack.subcall(s.dict[item],fn,*args) for item in s.order]
