class Behavior(object):

	def update_latch(s, instance, *parameters):

		def _update():
			attr = [getattr(instance, p) for p in parameters]
			attr = s.update(*attr)
			[setattr(instance, p, a) for p, a in zip(parameters, attr)]

		return _update;

	def update(s, *param):
		pass

