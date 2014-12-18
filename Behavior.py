class Behavior(object):

	def update_latch(s, instance, parameters):
		print parameters
		print parameters

		def _update():
			attr = [getattr(instance, p) for p in parameters]
			attr = s.update(*attr)
			if not hasattr(attr, '__iter__'):
				attr = [attr]
			[setattr(instance, p, a) for p, a in zip(parameters, attr)]

		return _update;

	def update(s, *param):
		print('hi')
		pass



class Bound(Behavior):
	def __init__(s, max, min):
		s.max = max
		s.min = min

	def update(s, param):
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

	def update(s, param):
		while theta >= s.max:
			theta -= s.width

		while theta < s.min
			theta += s.witch

		return theta