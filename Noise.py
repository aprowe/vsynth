class Fn(object):

	@staticmethod
	def Frame (seed = 0, seed2 = 0, speed = 60.0):
		return noise (float( frameCount / speed), seed, seed2) - 0.5

	def frame (s):
		return Fn.Frame(s.seed1, s.seed2)

	@staticmethod
	def approach(var1, var2, speed=0.05):
		return (var1-var2)*speed

	@staticmethod
	def sin(speed=0.2222):
		return sin(frameCount/speed)

	def __init__ (s, seed1 = None, seed2 = None):
		s.seed1 = seed1 if seed1 else random(-1000, 1000)
		s.seed2 = seed2 if seed2 else random(-1000, 1000)
	



