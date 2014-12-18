

#########################
# Math Functions
#########################
def toCart(theta, phi, rho):
	x = cos(phi) * sin(theta) * rho
	y = sin(phi) * sin(theta) * rho
	z = cos(theta) * rho

	return (x,y,z)

def interpolate(p1, p2, frac):
	i = lambda y,x,f: y+(x-y)*f

	return  tuple((i(p1[j], p2[j], frac) for j in range(len(p1))))

def wrap(theta, bound=TWO_PI):
	while theta >= bound:
		theta -= bound

	while theta < 0:
		theta += bound

	return theta

def bound (x, upper, lower=None):
	if lower is None:
		lower = -upper

	if x > upper:
		x = upper

	if x < -upper:
		x = -upper

	return x


#############################
# Shapes					#
#############################
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

def tetrahedron(edgeLength=100, pimage=None):
	beginShape(TRIANGLE_STRIP);
	if pimage:
		texture(pimage)
	vertex(edgeLength, edgeLength, edgeLength  , 1.0, 1.0);
	vertex(-edgeLength, -edgeLength, edgeLength, 0, 1.0);
	vertex(-edgeLength, edgeLength, -edgeLength, 0.25, 0.0);
	vertex(edgeLength, -edgeLength, -edgeLength, 0.75, 0.0);
	vertex(edgeLength, edgeLength, edgeLength  , 1.0, 1.0);
	vertex(-edgeLength, -edgeLength, edgeLength, 0, 1.0);
	endShape(CLOSE);


##########################
# Color Stuff
##########################

def randomColor(max=255):
	return tuple((random(max) for i in range (3)))


##########################
#	Data stuff
##########################
import json

def load_json(path):
	try:
		json_data=open(path + '.json')
	except:
		return {}

	data = json.load(json_data)
	print("loaded",path)
	json_data.close()
	return data

def lcfirst(string):
	return string[:1].lower() + string[1:] if string else ''

def ucfirst(string):
	return string[:1].upper() + string[1:] if string else ''
