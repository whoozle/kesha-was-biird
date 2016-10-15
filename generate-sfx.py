#!/usr/bin/env python2

class BitStream(object):
	def __init__(self):
		self.data = []
		self.bitidx = 0
		self.value = 0

	def add_bit(self, bit):
		if bit:
			self.value |= (0x80 >> self.bitidx)
		self.bitidx += 1

		if self.bitidx == 8:
			self.data.append(self.value)
			self.bitidx = 0
			self.value = 0

def generate_sweep():
	bs = BitStream()
	for interval in xrange(1, 32):
		for period in xrange(2):
			bs.add_bit(True)
			for i in xrange(interval):
				bs.add_bit(False)
	print " ".join(map(lambda x: "0x%02x" %x, bs.data[:32]))

generate_sweep()