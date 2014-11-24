import CDict

def callable(arg):
	return hasattr(arg, '__call__')

def numeric(arg):
	return type(arg) in [type(1),type(1.0)]

def string(arg):
	return type(arg) is type('str')

class Latchable(object):

	def __init__(self):
		self.functions = []
		self.seed1 = random(-1000, 1000)
		self.seed2 = random(-1000, 1000)

	def draw(self):
		pass

	def update(self):
		[fn() for fn in self.functions]

	##################################
	#	'Stack' Methods
	##################################
	def addStack(self, stack):
		Latchable.Stack = stack


	def call(self, args, key):
		value = args[key]
		
		if string(value):
			attr = getattr(self, value)
			if callable(attr):
				params = {}
				if value in args:				
					params = args[value]

				return lambda: attr(**params)

			else:
				return lambda: attr


		elif callable(value):
			return value

		return lambda: value


	def latch(self, args):
		target = args['target']

		targetFn = lambda: getattr(self, target)
		sourceFn = self.call(args, 'source')

		operator = args['operator']
		operatorFn = getattr(self, operator)

		opArgs = {}
		if operator in args:
			opArgs = args[operator]

		value = lambda: operatorFn(targetFn(), sourceFn(), **opArgs)

		fn = lambda: setattr(self, target, value())

		self.functions.append(fn)

	##################################
	#	Operator Methods
	##################################

	def add(self, target, source):
		return target + source

	def equals(self, target, source):
		return source;

	def multiply(self, target, source):
		return target * source;

	def approach(self, target, source, speed=0.01):
		return target + (source-target)*speed

	def vadd(self, target, source):
		c = []
		for a, b in zip(target, source):
			c.append(a + b)
		return tuple(c)



	##################################
	#	Source Methods
	##################################
	def lfo(self, amplitude=1, rate=1, phase=0, offset=0):
		return amplitude * sin(float(frameCount)/60.0 / rate * 2 * PI + phase) + offset

	def envelope(self, attack, decay, sustain, release):
		pass

	def stack(self, key, attr):
		print key, attr
		return getattr(Latchable.Stack[key], attr);

	def noise (self, amplitude=1, speed=100.0, seed1=None, seed2=None):
		if seed1 is None:
			seed1 = self.seed1

		if seed2 is None:
			seed2 = self.seed2

		return amplitude * noise(float( frameCount / speed), seed1, seed2) - 0.5


	def every(self, seconds=1):
		if frameCount % int(60*seconds) == 0:
			return 1
		else:
			return 0




