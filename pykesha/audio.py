FREQ = 4000
from math import sin, pi, floor, sqrt

def osc(t, freq):
	return sin(t * 2 * pi * freq)

def pulse(freq):
	buf = []
	byte = 0
	bit = 0
	for i in xrange(0, 128):
		v = osc(i * 1.0 / FREQ, freq)
		buf.append(v)
	return buf

def generate(tone):
	byte = 0
	bit = 0
	qe = 0
	for i in xrange(0, 128):
		x = tone[i]
		if x >= qe:
			byte |= (0x80 >> bit)
			y = 1
		else:
			y = -1
		qe = y - x + qe

		bit += 1
		if bit == 8:
			print "0x%02x" %byte,
			bit = 0
			byte = 0
	print

def mix(a, b):
	c = []
	n = sqrt(2)
	for i in xrange(0, 128):
		c.append((a[i] + b[i]) / n)
	return c
