from abstracts import *
from Noise import *
from ddf.minim import Minim

class CameraController(Latchable):

	def __init__(s):
		super(CameraController, s).__init__()
		s.x = s.y = 0
		s.scale = 1
		s.rotate = 0
		s.following = None

		followx = {
			'source': 'stack',
			'stack': {
				'key': 'vines',
				'attr': 'lastx',
			},
			'operator': 'approach',
			'approach': {
				'speed': 0.015
			},
			'target': 'x'
		}

		followy = {
			'source': 'stack',
			'stack': {
				'key': 'vines',
				'attr': 'lasty',
			},
			'operator': 'approach',
			'target': 'y'
		}


		s.latch(followx)
		s.latch(followy)


	def draw(s):
		translate (width/2, height/2)
		scale(s.scale)
		rotate (s.rotate)
		translate (-s.x, -s.y)


class AudioController(Latchable):
	
	def __init__(s):
		super(AudioController, s).__init__()
		s.minim = Minim(this)
		s.mic = s.minim.getLineIn(1)
		s.sig = 0
	
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