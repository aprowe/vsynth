from CDict import *
import json
import os

def callable(arg):
	return hasattr(arg, '__call__')

def numeric(arg):
	return type(arg) in [type(1),type(1.0)]

def string(arg):
	return type(arg) is type('str')


class Stack(dict):

	def __init__(s):
		super(Stack, s).__init__()
		s.order = list()

	def add(s, label, runnable):
		s[label] = runnable
		s.order.append(label)

	def call(s, fn, *args):
		[getattr(s[item], fn)(*args) for item in s.order]


class Latchable(object):

	ROOT_DIR = "modes/"
	Stack = None

	def __init__(self, mode='default'):
		self.self = self
		self.seed1 = random(-1000, 1000)
		self.seed2 = random(-1000, 1000)
		self.current_mode_name = mode
		self.modes = {mode: []}
		self.load_all_modes()

	def draw(self):
		pass

	def update(self):
		[fn() for fn in self.current_mode()]

	##################################
	#	Mode Methods                 #
	##################################
	def set_mode(self, name):
		if name in self.modes:
			self.current_mode_name = name

	def current_mode(self):
		return self.modes[self.current_mode_name]

	def load_json(self, path):
		try:
			json_data=open(Latchable.ROOT_DIR + path + '.json')
		except:
			return {}

		data = json.load(json_data)
		json_data.close()
		return data

	def load_mode_file(self, mode):
		data = self.load_json(mode)
		class_name = self.__class__.__name__

		if class_name not in data:
			return

		args = data[class_name]
		self.attach_latches(args, mode)
		print "Loaded "+mode 

	def load_all_modes(self):
		files = (os.path.splitext(file)[0]
				for file in os.listdir(Latchable.ROOT_DIR) 
				if file.endswith('.json'))

		for file in files:
			self.load_mode_file(file)


	##################################
	#	'Stack' Methods
	##################################
	def attach_latches(self, latches, mode='default'):
		if mode not in self.modes:
			self.modes[mode] = []

		if type(latches) is list:
			[self.latch(l, mode) for l in latches]
		elif type(latches) is dict:
			for mode, value in latches.items():
				self.modes[mode] = []
				[self.latch(l, mode) for l in value]


	def latch(self, dic, mode='default'):
		args = Latchable.formatLatch(dic)
		target = args['operator'][1]['target'][0]

		operator = args.reduce(self)['operator']

		attr = getattr(self, target)
		update = lambda: setattr(self, target, operator())			

		self.modes[mode].append(update)

	@staticmethod
	def formatLatch(dic):
		if 'target' not in dic:
			dic['target'] = 'self'

		dic['target'] = [ dic['target'] ]

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
	def tanh(self, target, source, range_max=1.0, range_min=0.0, domain_max=1.0, domain_min=0.0, sharpness=4.0):
		amp = (range_max-range_min)/2.0
		off = (range_max+range_min)/2.0
		damp = (domain_max-domain_min)/2.0
		doff = (domain_max+domain_min)/2.0
		x = sharpness/damp*(source-doff)
		y = x/sqrt(1+x**2) 

		return amp * y + off

	def arctan(self, x1, y1, x2, y2):
		tan = -atan2(y2-y1, x2-x1)
		
		if tan < -PI+0.1:
			tan = tan * -1

		return tan


	##################################
	#	Source Methods
	##################################
	def lfo(self, amplitude=1, period=1, phase=0, offset=0):
		return amplitude * sin(float(frameCount)/60.0 / period * 2 * PI + phase) + offset

	def envelope(self, attack, decay, sustain, release):
		pass

	def stack(self, key, attr="self"):
		return getattr(Latchable.Stack[key], attr);

	def noise (self, amplitude=1, speed=100.0, seed1=None, seed2=None):
		if seed1 is None:
			seed1 = self.seed1

		if seed2 is None:
			seed2 = self.seed2

		return amplitude * (noise(float( frameCount / speed), seed1, seed2) - 0.5)


	def every(self, seconds=1):
		if frameCount % int(60*seconds) == 0:
			return 1
		else:
			return 0

	def signal(self, amplitude = 1.0):
		return Latchable.Stack['audio'].mix() * amplitude

	def midi(self, num, amplitude = 1.0):
		return Latchable.Stack['midi'].get_value(num) * amplitude

	def atan(s, p1, p2):
			
		tan = -atan2(p1.y-p2.y, p1.x-p2.x)

		if tan < -PI+0.1: 
			tan = tan * -1

		return tan

class Positional(Latchable):

	def __init__(s, x=0, y=0):
		s.x = x
		s.y = y
		super(Positional, s).__init__()

	def follow(s, target, source, speed = 0.2):
		x = s.approach(target.x, source.x, speed)
		y = s.approach(target.y, source.y, speed)
		target.x = x
		target.y = y
		return target

	def wander(s, target, source, amplitude=1, speed=1):
		x = s.noise(amplitude, speed, 1)
		y = s.noise(amplitude, speed, 2)
		target.x += x
		target.y += y
		return target


	def point(s, x, y):
		return Positional(x, y)

	def distance(s, point):
		return sqrt((point.y - s.y)**2+(point.x - s.x)**2)


