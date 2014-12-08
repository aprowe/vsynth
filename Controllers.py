from Stack import *
from ddf.minim import Minim
from themidibus import MidiBus

class CameraController(Positional):

	def init(s):
		s.scale = 1
		s.rotate = 0
		s.speed = 0

	def draw(s):
		translate (width/2, height/2)
		scale(s.scale)
		rotate (s.rotate)
		translate (-s.x, -s.y)

		# for i in range(-3,3):
		# 	for j in range(-3,3):
		# 		for k in range(-3,3):
		# 			pushMatrix()
		# 			translate(i*250, j*250, k*250)
		# 			noStroke()
		# 			fill(0,0,255)
		# 			sphere(5)
		# 			popMatrix()
				


	def update(s):
		return 
		s.n += s.signal()*20
		if s.n > 400:
			s.n = 0
		s.x,s.y,s.z = s.pos
		s.target = Latchable.Stack['line'].points[int(s.n+10)]
		s.pos = Latchable.Stack['line'].points[int(s.n)]

class AudioController(Latchable):
	
	def __init__(s):
		s.minim = Minim(this)
		s.mic = s.minim.getLineIn(1)
		s.sig = 0
		super(AudioController, s).__init__()

	def update(s):
		s.sig = s.average()
		super(AudioController, s).update()
	
	def average(s):
		sum=0
		for i in xrange(s.mic.bufferSize()):
			sum += sq(s.mic.mix.get(i))
		sum/= s.mic.bufferSize()
		return sqrt(sum);

	def mix(s):
		return s.sig

class MidiController(Latchable):
	def __init__(s):
		  s.bus = MidiBus(s, 1, 1)
		  s.bus.list()
		  s.controls = {}
		  super(MidiController, s).__init__()


	def control_change(s, num, val):
		s.controls[num] = val

	def get_value(s, num):
		if num in s.controls:
			return s.controls[num]

		return 0






