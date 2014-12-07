from VSynth import *

vs = VSynth()
Latchable.Stack = vs

def setup():
	size(1440,900, P3D)
	textureMode(NORMAL);
	vs.add('line',Line())

def draw():
	background(0)
	vs.render()


class Line(Positional):

	def init(s):
		s.z = 0
		s.phi = 0
		s.theta = PI/2.0
		s.speed = 5
		s.points = [(0,0,0) for i in range(20)]
		s.angles = [(0,0, s.speed) for i in range(20)]
		s.computePath()
		s.texture = loadImage('texture.jpg')

	def pos(s):
		return (s.x,s.y,s.z)

	def computePath(s, length=500, rate=10.0):
		for i in range(length):
			s.phi 	+= (noise(1.0*i/length/rate, 100)-0.5)*0.3
			s.theta += (noise(1.0*i/length/rate, 200)-0.5)*0.3
	
			s.phi = s.approach(s.phi, 0)
			s.theta = s.approach(s.theta, 0)

			s.x += cos(s.phi) * sin(s.theta) * s.speed
			s.y += sin(s.phi) * sin(s.theta) * s.speed
			s.z += cos(s.theta) * s.speed


			s.points.append( (s.x, s.y, s.z) )
			s.angles.append( (s.theta, s.phi, s.speed) )

	def update(s):

		s.x += cos(s.phi) * sin(s.theta) * s.speed
		s.y += sin(s.phi) * sin(s.theta) * s.speed
		s.z += cos(s.theta) * s.speed

		# s.x += s.noise(seed1=0)*10
		# s.y += s.noise(seed1=100)*10
		# s.z += s.noise(seed1=200)*10


		s.phi 	+= s.noise(seed1=0)*0.3
		s.theta += s.noise(seed1=100)*0.3

		s.phi = s.approach(s.phi, 0)
		s.theta = s.approach(s.theta, 0)

		s.points.append( (s.x, s.y, s.z) )
		s.angles.append( (s.theta, s.phi, s.speed) )

		if len(s.points) > 500:
			del s.points[0]
		if len(s.angles) > 500:
			del s.angles[0]

	def draw(s):
		fill(255)
		stroke(255)
		i = 0
		j =0
		for p1, p2 in zip(s.points, s.angles):
			tint(s.noise(seed1=100.0, seed2=j)*100+155, s.noise(seed1=0.0,seed2=j)*100+155, s.noise(seed1=200,seed2=j)*100+255)
			i += 1
			j += 0.1
			pushMatrix()
			# line(*(p1 + p2))
			translate(*p1)
			rotateZ(p2[1])
			rotateY(p2[0])
			if i == 10:
				i = 0
				cylinder(250 + s.noise(seed1=j)*100, abs(s.noise(seed1=j)*250) + 250 , p2[2]*10, 30, s.texture)
			# line(0,0,0,0,0,p2[2])
			# line(5,0,0,5,0,p2[2])
			# line(0,5,0,0,5,p2[2])
			# line(-5,0,0,-5,0,p2[2])
			# line(0,-5,0,0,-5,p2[2])
			popMatrix()







# def cylinder(w, h, sides):
# 	x = []
# 	z = []

# 	for i in range(sides):
# 		angle = TWO_PI / (sides) * i;
# 		x.append (sin(angle) * w)
# 		z.append (cos(angle) * w)
 
# 	beginShape(TRIANGLE_FAN)
# 	vertex(0,   0,    0)
 
# 	for i, j in zip(x,z):
# 		vertex(i, j, h)
 
# 	endShape()
 
# 	beginShape(QUAD_STRIP)
 
# 	for i, j in zip(x,z):
# 		vertex(i, j, 0)
# 		vertex(i, j, h)

# 	endShape()


# void taper(float w, float w2, float h, int sides){
#   float angle;
#   float[] x = new float[sides+1]; // x for bottom 
#   float[] x2 = new float[sides+1];  // x for top
#   float[] z = new float[sides+1];
#   float[] z2 = new float[sides+1];
 
#   //get the x and z position on a circle for all the sides
#   for(int i=0; i < x.length; i++){
#     angle = TWO_PI / (sides) * i;
#     x[i] = sin(angle) * w;
#     z[i] = cos(angle) * w;
#     x2[i] = sin(angle) * w2;
#     z2[i] = cos(angle) * w2;
#   }
 
#   //draw the top of the cylinder
#   beginShape(TRIANGLE_FAN);
#   vertex(0,   0,    0);
 
#   for(int i=0; i < x.length; i++){
#     vertex(x[i], 0, z[i]);
#   }
 
#   endShape();
 
#   //draw the center of the cylinder
#   beginShape(QUAD_STRIP); 
 
#   for(int i=0; i < x.length; i++){
#     vertex(x[i], 0, z[i]);
#     vertex(x2[i], h, z2[i]);
#   }
 
#   endShape();
 
#   //draw the bottom of the cylinder
#   beginShape(TRIANGLE_FAN); 
 
#   vertex(0,   h,    0);
 
#   for(int i=0; i < x.length; i++){
#     vertex(x2[i], h, z2[i]);
#   }
 
#   endShape();

# }

def cylinder(w, w2=None, h=1, sides=6, pimage=None):
	sides += 1
	w2 = w if w2 is None else w2

	x = []
	x2 = []
	z = []
	z2 = []
 
	for i in range(sides):
		angle = TWO_PI / (sides - 1) * i;

		x.append(sin(angle) * w)
		z.append(cos(angle) * w)

		x2.append(sin(angle) * w2)
		z2.append(cos(angle) * w2)
 
	# //draw the center of the cylinder
	noStroke()
	beginShape(QUAD_STRIP)

	if pimage:
		texture(pimage)

	for i in range(sides):
		vertex (x[i], z[i], 0, i / float(sides) * 1.0, 0)
		vertex (x2[i], z2[i], h+1, i / float(sides) * 1.0, 1)

	endShape()
