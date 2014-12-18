import Latchable

class Positional(Latchable):

	def __init__(s, x=0, y=0, z=0):
		s.x = x
		s.y = y
		s.z = z
		super(Positional, s).__init__()

	def follow(s, target, source, speed = 0.2):
		x = s.approach(target.x, source.x, speed)
		y = s.approach(target.y, source.y, speed)
		z = s.approach(target.z, source.z, speed)
		target.x = x
		target.y = y
		target.z = z
		return target

	def wander(s, target=None, source=None, amplitude=10, speed=1):
		if target is None:
			target = s

		x = s.noise(amplitude, speed, 1)
		y = s.noise(amplitude, speed, 2)
		z = s.noise(amplitude, speed, 3)
		target.x += x
		target.y += y
		target.z += z
		return target


	def point(s, x, y, z):
		return Positional(x, y, z)

	def distance(s, point):
		return sqrt((point.y - s.y)**2+(point.x - s.x)**2)

	def bound(s, target=None, source=None, margin=100):
		if target is None:
			target = s

		if target.x < source.x - width/2 - margin:
			target.x = source.x + width/2 + margin 

		elif target.x > source.x + width/2 + margin:
			target.x = source.x - width/2 - margin 

		if target.y < source.y - height/2 - margin:
			target.y = source.y + height/2 + margin 

		elif target.y > source.y + height/2 + margin:
			target.y = source.y - height/2 - margin

		return target