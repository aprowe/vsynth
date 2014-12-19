from Behavior import *
import inspect


class Trigger(Behavior):
	'''Triggers a function on a latchable when the Behavior function returns true'''

	def create_function(s, instance, parameters):
		function = parameters[0]
		parameters = parameters[1:]

		args = inspect.getargspec(getattr(instance, function)).args
		if not len(args) == len(parameters) + 1:
			raise Exception('Input parameters dont match behave functions inputs')

		def _update():
			attr = [getattr(instance, p) for p in parameters]
			if s.behave(instance, *attr):
				getattr(instance, function)()

		return _update;

	def behave(s):
		return False


class Every(Trigger):

	def __init__(s, seconds=60):
		s.seconds = seconds

	def behave(s):
		return frameCount % int(60*s.seconds) == 0:


class Threshold(Trigger):

	def __init__(s, thresh=1.0):
		s.thresh = thresh

	def behave(s, thresh):
		return thresh > s.thresh 
