#!/usr/bin/env python2

from pykesha.audio import *

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
