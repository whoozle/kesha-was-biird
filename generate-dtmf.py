#!/usr/bin/env python

FREQ = 4000
from math import sin, pi, floor

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

def mix(a, b):
	c = []
	for i in xrange(0, 128):
		c.append(a[i] + b[i])
	return c

cols = (pulse(1209), pulse(1336), pulse(1477), pulse(1633))
rows = (pulse(697), pulse(770), pulse(852), pulse(941))
rosit = (pulse(913), pulse(1428), pulse(1776))
dial_tone = mix(pulse(350), pulse(440))

mapping = (
	1, 2, 3, 12,
	4, 5, 6, 13,
	7, 8, 9, 14,
	10, 0, 11, 15
)

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

print ": audio_phone_tones"
for row in xrange(0, 4):
	for col in xrange(0, 4):
		idx = row * 4 + col
		#print row, col, mapping[idx]
		tone = mix(rows[row], cols[col])
		#print tone
		generate(tone)

for tone in rosit: #16, 17, 18
	generate(tone)

generate(dial_tone) #19
