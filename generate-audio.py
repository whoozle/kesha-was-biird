#!/usr/bin/env python2

from __future__ import print_function

import argparse
import wave
import struct
import sys

parser = argparse.ArgumentParser(description='Convert audio.')
parser.add_argument('source', help='input file')
parser.add_argument('address', help='address to load from')
parser.add_argument('name', help='name')
parser.add_argument('-e', '--encoding', help = 'encoder : [pdm|pwd]', default='pwm')
parser.add_argument('-c', '--cutoff', help = 'cutoff value', default=0.1, type=float)
parser.add_argument('-o', '--output', help = 'dump audio as wav file')
parser.add_argument('-l', '--level', type = int, default = 0, help = 'compression level')
args = parser.parse_args()

addr = int(args.address, 16)

wav = wave.open(args.source)
n = wav.getnframes()
if wav.getsampwidth() != 2:
	raise Exception("invalid sample width")
if wav.getnchannels() != 1:
	raise Exception("only mono supported")
if wav.getframerate() != 4000:
	raise Exception("invalid sample rate, sox -S %s -r 4000 -b 16 <output>" %args.source)

frames = wav.readframes(n)

wavdata = bytes()
data = []
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
level = args.level

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
		wavdata += struct.pack('<h', 16384)
	else:
		y = -1
		wavdata += struct.pack('<h', -16384)

	if enc == 'pdm':
		qe = y - x + qe
		assert qe >= -1 and qe <= 1

	bit += 1
	if bit == 8:
		data.append(byte)
		bit = 0
		byte = 0
		size += 1

if size % 16:
	rem = 16 - (size % 16)
	for i in xrange(0, rem):
		size += 1

def compress(data):
	print("uncompressed data: %u bytes" %len(data), file=sys.stderr)
	pack, bitpack, index = [], [], []

	def bitcount(value):
		return bin(value).count('1')

	def read(next):
		value = 0L
		for idx, byte in enumerate(next):
			value |= byte << (8 * idx)
		return value

	def difference(v1, v2):
		r = bitcount(v1 ^ v2)
		if r == 0:
			return r
		for s in xrange(1, min(8, 1 + level)):
			r = min(r, s + bitcount(v1 ^ (v2 << s)))
			if r == 0:
				return r
			r = min(r, s + bitcount((v1 << s) ^ v2))
			if r == 0:
				return r
		return r

	def indexOf(next):
		mindiff, minindex = 128, -1
		for i, seq in enumerate(bitpack):
			diff = difference(seq, next)
			if diff < mindiff:
				mindiff, minindex = diff, i
		#print('indexOf(%d) -> %d with diff %d' %(next, minindex, mindiff), file=sys.stderr)
		return minindex if mindiff <= level else -1

	last_progress = 0
	total = 0
	for offset in xrange(0, len(data), 16):
		#print('offset %d, bitpack %d' %(offset, len(bitpack)), file=sys.stderr)
		next = data[offset:offset + 16]
		bits = read(next)
		src = indexOf(bits)
		if src < 0:
			src = len(pack)
			pack += next
			bitpack.append(bits)
		index.append(src)
		progress = 100 * offset / len(data)
		if last_progress != progress:
			last_progress = progress
			total = len(pack) + len(index) * 2
			print("encoding progress: %02d%% %d/%d" %(progress, total, len(data)), file=sys.stderr)

	print("compressed data: %u + %u = %u bytes, level: %u, ratio: %.1f%%" %(len(pack), len(index) * 2, total, args.level, 100.0 * total / len(data)), file=sys.stderr)
	return pack, index

data, offsets = compress(data)

source, index = '', ''
source += ": audio_%s\n" %args.name

for idx, byte in enumerate(data):
	mask = idx & 0x0f
	if mask == 0:
		source += '\t'
	source += '0x%02x' %byte
	if mask == 15:
		source += '\n'
	else:
		source += ' '

for offset in offsets:
	offset += addr + (len(offsets) * 2) + 2
	h, l = (offset >> 8), offset & 0xff
	if h >= 0x100:
		raise Exception('offset is out of 64k')
	index += '\t0x%02x 0x%02x\n' %(h, l)
index += '\t0xff 0xff\n'

size /= 16 #loop count
print (":org 0x%04x\n" %addr)
print (":const audio_%s_hi 0x%02x" %(args.name, addr >> 8))
print (":const audio_%s_lo 0x%02x\n" %(args.name, addr & 0xff))

print (": audio_%s_index\n%s\n%s"  %(args.name, index, source))

if args.output:
	out = wave.open(args.output, 'w')
	out.setnchannels(1)
	out.setsampwidth(2)
	out.setframerate(wav.getframerate())
	out.setnframes(len(wavdata) / 2)
	out.writeframes(wavdata)
	out.close() #no __exit__
