from abstracts import *
from Noise import *

class CameraController(Latchable):

	def __init__(s):
		super(CameraController, s).__init__()
		s.x = s.y = 0
		s.scale = 1
		s.rotate = 0

	def connect(s, stack):
		s.latch('x_follow', stack['vines'].vines[0].X )
		s.latch('y_follow', stack['vines'].vines[0].Y )

		s.latch('signal', lambda: 1 - stack['audio'].mix() )

	def update(s):
		s.x += Fn.approach( s.get('x_follow'), s.x, 0.03) 
		s.y += Fn.approach( s.get('y_follow'), s.y, 0.03)
		# s.scale += Fn.approach ( s.get('signal'), s.scale, 0.1)
		s.rotate = PI/2 * Fn.sin( 15.0 )
		# if s.positional:
			# s.x += (s.get('x_follow') - s.x) * 0.03
			# s.y += (s.get('y_follow') - s.y) * 0.03

		# s.x += Noise.Noise(0)
		# s.y += Noise.Noise(1)
		# s.scale += Noise.Noise(2)/50

	def draw(s):
		translate (width/2, height/2)
		# scale (s.scale)
		scale( s.scale + .2)
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