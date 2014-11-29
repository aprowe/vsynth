from CDict import *
import json


def callable(arg):
	return hasattr(arg, '__call__')

def numeric(arg):
	return type(arg) in [type(1),type(1.0)]

def string(arg):
	return type(arg) is type('str')

class Latchable(object):

	def __init__(self):
		self.seed1 = random(-1000, 1000)
		self.seed2 = random(-1000, 1000)
		self.current_mode_name = 'default'
		self.modes = {'default': []}
		self.attach_latches()


	def draw(self):
		pass

	def update(self):
		[fn() for fn in self.current_mode()]

	##################################
	#	Mode Methods
	##################################
	def setMode(self, name):
		self.current_mode_name = name

	def current_mode(self):
		return self.modes[self.current_mode_name]

	def load_mode(self, filename):
		try:
			json_data=open('modes/'+filename + '.json')
		except:
			return {}

		data = json.load(json_data)
		json_data.close()
		print(data)
		return data

	##################################
	#	'Stack' Methods
	##################################
	def attach_latches(self):
		latches = self.getLatches()
		if type(latches) is list:
			[self.latch(l) for l in latches]
		elif type(latches) is dict:
			for mode, value in latches.items():
				self.modes[mode] = []
				[self.latch(l, mode) for l in value]

	def getLatches(self):
		return self.load_mode(self.__class__.__name__)
		# return {}

	def addStack(self, stack):
		Latchable.Stack = stack

	def latch(self, args, mode='default'):
		target = args['target']
		args['target'] = [target]
		args = Latchable.formatLatch(args)

		operator = args.reduce(self)['operator']
		update = lambda: setattr(self, target, operator())

		self.modes[mode].append(update)

	@staticmethod
	def formatLatch(dic):
		if 'source' not in dic:
			dic['source'] = dic['target']

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
	#	Behaviors
	##################################
	def tanh(self, target, source, min=0, max=1, dmin=0, dmax=1, sharpness=1.0):
		amp = (max-min)/2.0
		off = (max+min)/2.0
		damp = (dmax-dmin)/2.0
		doff = (dmax+dmin)/2.0
		x = sharpness/damp*(source-doff)
		y = x/sqrt(1+x**2) 

		return amp * y + off



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



