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