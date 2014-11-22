class Fn(object):

	@staticmethod
	def Noise (seed = 0, seed2 = 0, speed = 0.0):
		return noise (float( frameCount / speed), seed, seed2) - 0.5

	def noise (s, speed=60.0):
		return Fn.Noise(s.seed1, s.seed2, speed)

	@staticmethod
	def approach(var1, var2, speed=0.05):
		return (var1-var2)*speed

	@staticmethod
	def sin(speed=1.0, amplitude = 1.0, yoff=0.0, xoff = 0.0):
		return amplitude * sin(
			float(frameCount)/60.0 / speed * 2 * PI + xoff) + yoff

	@staticmethod
	def every(seconds=1):
		if frameCount % int(60*seconds) == 0:
			return True
		else:
			return False

	@staticmethod
	def call_every(seconds, function):
		if Fn.every(seconds):
			function()

	def __init__ (s, seed1 = None, seed2 = None):
		s.seed1 = seed1 if seed1 else random(-1000, 1000)
		s.seed2 = seed2 if seed2 else random(-1000, 1000)
	



