
from ddf.minim import Minim
from themidibus import MidiBus, SimpleMidiListener
from ddf.minim.analysis import BeatDetect

from auxilary import *
from Latchable import *
from Positional import *

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

class Camera3D(Positional):

	def init(s):
		s.target = (0,0,0)
		s.theta = 0
		s.phi = 0

	def draw(s):
		camera(*(s.pos()+s.target+(0,1,0)))


class AudioController(Latchable):
	
	def __init__(s):
		s.minim = Minim(this)
		s.mic = s.minim.getLineIn(1)
		s.sig = 0
		s.beat = BeatDetect()
		s.beat.setSensitivity(300)
		s.beat.detectMode(BeatDetect.FREQ_ENERGY)
		s.on_beat = False
		super(AudioController, s).__init__()

	def update(s):
		s.sig = s.average()
		s.beat.detect(s.mic.mix)
		s.on_beat = s.beat.isOnset()
		super(AudioController, s).update()
	
	def average(s):
		sum=0
		for i in xrange(s.mic.bufferSize()):
			sum += sq(s.mic.mix.get(i))
		sum/= s.mic.bufferSize()
		return sqrt(sum);

	def mix(s):
		return s.sig

class MidiController(Latchable, SimpleMidiListener):

	def init(s):
		s.bus = MidiBus(s, 1, 2)
		s.bus.list()
		midi_map = load_json('data/midi_map')

		s.mapping = midi_map['nanoKontrol']
		s.values = midi_map['default']
		for key in s.values:
			s.values[key] = float(s.values[key])

		print(s.mapping)
		print(s.values)


	def controllerChange(s, channel, number, value):
		key = s.mapping[str(number)]
		s.values[key] = value/127.0
		print(value)


	def get(s, key):
		if "macro_"+str(key) in s.values:
			return s.values["macro_"+str(key)]

		if key in s.values:
			return s.values[key]

		return 0








