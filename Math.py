

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
