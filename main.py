from VSynth import *

vs = VSynth()

img = loadImage('back.jpg')

def setup():
	global edges
	size(1400,900, P3D)
	textureMode(NORMAL)
	# edges = loadShader("blur.glsl")

	vs.append(VineArray(), 'vines')
	vs.append_mode(Default())
	vs.append_mode(Follow())

	# vs.set_mode('follow')

z= 0
def draw():
	global z
	background(255)

	pushMatrix()
	# translate(width/2, height/2)
	# z += 1
	# print z
	# w = 240
	z+=1
	print(z)
	spotLight(255, 255, 255, 0, 0, 1400, 0, 0, -1, PI, 45)
	fill(255,0,0)
	# sphere(120)
	# fill(255,255,0)
	w = 1400
	translate(-w/2,-w/2,0)
	noStroke()
	max =20.0
	for i in range(max):
		for j in range(max):
			beginShape()
			texture(img)
			vertex(i*w/max,j*w/max, i*j, i/max, j/max)
			vertex((i+1)*w/max,j*w/max, (i+1)*(j), (i+1)/max, j/max)
			vertex((i+1)*w/max,(j+1)*w/max,(i+1)*(j+1), (i+1)/max, (j+1)/max)
			vertex(i*w/max,(j+1)*w/max,(i)*(j+1), i/max, (j+1)/max)
			endShape()
	# shader(edges);
	
	# # camera(0, 0, 500, 0, 0, 0, 0, 1, 0)
	popMatrix()
	translate(0,0,40)
	# translate(width/2,height/2,0)
	vs.render()

class Vine(Positional):

	def init(s):
		s.theta = random(0,TWO_PI)
		s.phi = random(0, PI)
		s.speed = 5.0
		s.attach_behavior('wrap', 'theta')
		s.attach_behavior('threshold', ('_print','x'))
		s.points = [(0,0,0)]

	def pos(s):
		return (s.x,s.y,s.z)

	def angle(s):
		return (s.theta, s.phi, s.speed)

	def update(s):
		s.points.append((s.x,s.y,s.z))
		(dx, dy, dz) = toCart(*s.angle())
		# s.x += s.speed * sin(s.theta)
		# s.y += s.speed * cos(s.theta)
		s.x += dx
		s.y += dy
		s.z += dz

		if len(s.points) > 500:
			del s.points[0]


	def draw(s):
		stroke(0)
		weight = 10
		min_weight = 0.8
		for p1, p2 in zip(s.points[0:-1], s.points[1:]):
			weight -= (weight-min_weight)*0.05
			strokeWeight(weight)
			line(*(p2+p1))

	def _print(s):
		pass

class VineArray(Substack):

	def init(s):
		s.append_array(Vine, 10)
		s.x = 0
		s.y = 0
		s.z = 0

	def pos(s):
		return (s.x,s.y,s.z)

	def update(s):
		s.x = s.get(0).x
		s.y = s.get(0).y

class Default(Mode):

	def update_vine(mode, s):
		s.theta += s.noise(amplitude = 1.0)
		s.phi += s.noise(amplitude = 1.0)

	def update_camera3D(mode, s):
		# s.follow(s.stack('vines'))
		s.theta += 0.01
		s.phi += 0.00
		s.x += s.noise()*10
		s.y+= s.noise()*10
		# s.follow()

class Follow(Default):

	def update_camera3D(mode, s):
		pass

		# s.follow(s.stack('vines'))
		s.target = s.stack('vines').pos()
		# s.theta += 0.01
		# s.phi += 0.00

		# (s.x, s.y, s.z) = toCart(*(s.theta, s.phi, 1000))
		# s.follow()