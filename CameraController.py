from abstracts import *
from Noise import *
from ddf.minim import Minim

class CameraController(Latchable):

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

	def draw(s):
		pass

	def mix(s):
		return s.sig