#!/usr/bin/env python2

from pykesha.audio import *

#Eb F Gb Ab Bb Cb Db
#http://www.phy.mtu.edu/~suits/scales.html
freqs = [313.96, 348.83, 367.92, 418.60, 470.93, 490.55, 545.08]

print ": music_keys"

for freq in [6, 0, 2]:
	generate(pulse(freqs[freq]))
	generate(pulse(freqs[freq] * 2))
