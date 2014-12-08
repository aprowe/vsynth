

def toCart(theta, phi, rho):
	x = cos(phi) * sin(theta) * rho
	y = sin(phi) * sin(theta) * rho
	z = cos(theta) * rho

	return (x,y,z)

def interpolate(p1, p2):
	return ((p1[0]+p2[0])/2,(p1[1]+p2[1])/2,(p1[2]+p2[2])/2)
