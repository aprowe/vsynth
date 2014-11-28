from CDict import *

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

	def latch(self, args):
		target = args['target']
		args['target'] = [target]
		args = Latchable.formatLatch(args)

		operator = args.reduce(self)['operator']
		update = lambda: setattr(self, target, operator())

		self.functions.append(update)

	@staticmethod
	def formatLatch(dic):
		source = dic['source']
		target = dic['target']
		op_params = {}
		op_fn = dic['operator'][0]

		if len(dic['operator']) > 1:
			op_params = dic['operator'][1]

		params = list(op_params.items()) + list({'source': source, 'target': target}.items())
		params = dict(params)
		output = {'operator': [op_fn, params]}
		return CDict(output)


	##################################
	#	Operator Methods
	##################################

	def add(self, target, source):
		return target + source

	def equals(self, target, source):
		return source;

	def multiply(self, target, source):
		return target * source;

	def approach(self, target, source, speed=0.03):
		return target + (source-target)*speed

	def vadd(self, target, source):
		c = []
		for a, b in zip(target, source):
			c.append(a + b)
		return tuple(c)



	##################################
	#	Source Methods
	##################################
	def lfo(self, amplitude=1, period=1, phase=0, offset=0):
		return amplitude * sin(float(frameCount)/60.0 / period * 2 * PI + phase) + offset

	def envelope(self, attack, decay, sustain, release):
		pass

	def stack(self, key, attr):
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

	def signal(self, amplitude = 1.0):
		return Latchable.Stack['audio'].mix() * amplitude




