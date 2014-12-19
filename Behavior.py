class Behavior(object):

	def create_function(s, instance, parameters):

		def _update():
			attr = [getattr(instance, p) for p in parameters]
			attr = s.behave(*attr)
			if not hasattr(attr, '__iter__'):
				attr = [attr]
			[setattr(instance, p, a) for p, a in zip(parameters, attr)]

		return _update

	def update(s, *param):
		pass



class Bound(Behavior):
	def __init__(s, max, min):
		s.max = max
		s.min = min

	def behave(s, param):
		if param > s.max:
			return s.max

		if param < s.min:
			return s.min

		return param


class Wrap(Behavior):

	def __init__(s, max=TWO_PI, min=0):
		s.max = max
		s.min = min
		s.width = max - min

	def behave(s, param):
		while param >= s.max:
			param -= s.width

		while param < s.min:
			param += s.width

		return param
