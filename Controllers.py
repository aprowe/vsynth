from Stack import *
from ddf.minim import Minim
from themidibus import MidiBus

class CameraController(Positional):

	def __init__(s):
		s.x = s.y = 0
		s.scale = 1
		s.rotate = 0
		s.following = None
		super(CameraController, s).__init__()

	def draw(s):
		translate (width/2, height/2)
		scale(s.scale)
		rotate (s.rotate)
		translate (-s.x, -s.y)



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






