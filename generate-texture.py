#!/usr/bin/env python

import argparse
import png

parser = argparse.ArgumentParser(description='Compile font.')
parser.add_argument('source', help='input file')
parser.add_argument('name', help='name')
parser.add_argument('planes', type=int, help='planes (1/2)')
parser.add_argument('tile-size', type=int, help='tile size (8/16)')
args = parser.parse_args()

tex = png.Reader(args.source)
w, h, pixels, metadata = tex.read_flat()
tile_size = getattr(args, 'tile-size')
if tile_size != 8 and tile_size != 16:
	raise Exception("invalid tile size %d" %tile_size)
tw, th = tile_size, tile_size

def label(name):
	return ": tile_%s_%s" %(args.name, name)

nx = (w + tw - 1) / tw
ny = (h + th - 1) / th

def get_pixel(x, y, plane):
	if x < 0 or x >= w:
		return 0
	if y < 0 or y >= h:
		return 0

	bit = 1 << plane
	return 1 if pixels[y * w + x] & bit else 0

print label("data"),
for ty in xrange(0, ny):
	basey = ty * th
	if nx > 1 or ny > 1:
		print "\n" + label("row_%d" %ty)
	for tx in xrange(0, nx):
		basex = tx * tw
		if nx > 1 or ny > 1:
			print "\n" + label("%d_%d" %(ty, tx))
		for plane in xrange(0, args.planes):
			for y in xrange(0, th):
				for x in xrange(0, tw / 8):
					byte = 0
					for bit in xrange(0, 8):
						byte |= get_pixel(basex + x * 8 + bit, basey + y, plane) << (7 - bit)
					print "0x%02x" %byte ,
