from abstracts import *
from Noise import *

class CameraController(Latchable):

	def __init__(s):
		super(CameraController, s).__init__()
		s.x = s.y = 0
		s.scale = 1
		s.rotate = 0
		s.following = None

	def connect(s, stack):

		modes = {
			'normal': {
				'signal': lambda: stack['audio'].mix(),
				'following': lambda: stack['vines'].vines[0],
				'x_follow': lambda: s.get('following').x,
				'y_follow': lambda: s.get('following').y,
				'step_x': lambda: 
					Fn.approach( s.get('x_follow'), s.x, 0.03),
				'step_y': lambda: 
					Fn.approach( s.get('y_follow'), s.y, 0.03),
				'rotate': lambda: PI/2 * Fn.sin( 15.0 )
			},
			'shift_targets': {
				'following': lambda: s.following
			}
		}

		s.addModes(modes)

	def update(s):
		s.x += s.get('step_x')
		s.y += s.get('step_y')
		s.rotate = s.get('rotate')

		if Fn.every(2):
			s.following = s.stack['vines'].randomVine()
			s.mode('shift_targets')


	def draw(s):
		translate (width/2, height/2)
		scale(s.scale)
		rotate (s.rotate)
		translate (-s.x, -s.y)

from ddf.minim import Minim

class AudioController(Latchable):
	
	def __init__(s):
		s.minim = Minim(this)
		s.mic = s.minim.getLineIn(1)
		s.sig = 0
	

	def average(s):
		sum=0
		for i in xrange(s.mic.bufferSize()):
			sum += sq(s.mic.mix.get(i))
		sum/= s.mic.bufferSize()
		return sqrt(sum);

	def update(s):
		s.sig = s.average()

	def draw(s):
		pass

	def mix(s):
		return s.sig