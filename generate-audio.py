#!/usr/bin/env python

import argparse
import wave
import struct

parser = argparse.ArgumentParser(description='Convert audio.')
parser.add_argument('source', help='input file')
parser.add_argument('name', help='name')
parser.add_argument('-e', '--encoding', help = 'encoder : [pdm|pwd]', default='pwm')
parser.add_argument('-c', '--cutoff', help = 'cutoff value', default=0.1, type=float)
parser.add_argument('-o', '--output', help = 'dump audio as wav file')
args = parser.parse_args()

wav = wave.open(args.source)
n = wav.getnframes()
if wav.getsampwidth() != 2:
	raise Exception("invalid sample width")
if wav.getnchannels() != 1:
	raise Exception("only mono supported")
if wav.getframerate() != 4000:
	raise Exception("invalid sample rate, sox -S %s -r 4000 -b 16 <output>" %args.source)

frames = wav.readframes(n)

source = ""
source += ": audio_%s\n" %args.name

data = bytes()
enc = args.encoding

qe = 0
peak = 0

offset = 0
for i in xrange(0, n):
	value, = struct.unpack('<h', frames[offset: offset + 2]) if offset < len(frames) else (0,)
	offset += 2
	if value > peak:
		peak = value
	elif value < -peak:
		peak = -value

offset = 0
size = 0
bit, byte = 0, 0
cutoff = args.cutoff

for i in xrange(0, n):
	buf = []

	value, = struct.unpack('<h', frames[offset: offset + 2]) if offset < len(frames) else (0,)
	offset += 2

	x = 1.0 * value / peak
	assert x >= -1 and x <= 1

	if enc == 'pdm':
		out = x >= qe
	elif enc == 'pwm':
		out = x >= cutoff
	else:
		raise Exception("unknown encoding " + enc)

	if out:
		byte |= (0x80 >> bit)
		y = 1
		data += struct.pack('<h', 16384)
	else:
		y = -1
		data += struct.pack('<h', -16384)

	if enc == 'pdm':
		qe = y - x + qe
		assert qe >= -1 and qe <= 1

	bit += 1
	if bit == 8:
		source += "0x%02x " %byte
		bit = 0
		byte = 0
		size += 1
		if (size % 32) == 0:
			source += "\n"

if size % 16:
	rem = 16 - (size % 16)
	for i in xrange(0, rem):
		source += "0x00 "
		size += 1

print
size /= 16 #loop count
#print ":const audio_%s_size %d"  %(args.name, size)
print ": audio_%s_size\n\t0x%02x 0x%02x\n%s"  %(args.name, size & 0xff, size >> 8, source)

if args.output:
	out = wave.open(args.output, 'w')
	out.setnchannels(1)
	out.setsampwidth(2)
	out.setframerate(wav.getframerate())
	out.setnframes(len(data) / 2)
	out.writeframes(data)
	out.close() #no __exit__
