
class Positional(object):
	def X():
		pass

	def Y():
		pass

class Latchable(object):

	def __init__(self):
		self.functions = {}

	def draw(self):
		pass

	def update(self):
		pass

	def latch(self, name, function):
		self.functions[name] = function

	def get(self, name, factor = 1):
		return self.functions[name]() * factor

	def connect(self, stack):
		pass