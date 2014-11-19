
class Positional(object):
	def X():
		pass

	def Y():
		pass

class Latchable(object):

	def __init__(self):
		self.current_mode = 'normal'		
		self.modes = {'normal': {}}

	def draw(self):
		pass

	def update(self):
		pass

	def latch(self, name, function):
		self.modes[self.current_mode][name] = function

	def get(self, name, factor = 1):
		return self.modes[self.current_mode][name]() * factor

	def connect(self, stack):
		pass

	def addModes(self, modes):
		if 'normal' in modes:
			self.addMode('normal', modes['normal'])
			del modes['normal']


		for item in modes.items():
			self.addMode(item[0], item[1])

	def mode(self, label):
		if label not in self.modes:
			self.addMode(label)

		self.current_mode = label

	def addMode(self, name, mode={}):
		new_mode = dict(self.modes['normal'].items() + mode.items())
		self.modes[name] = new_mode
