#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description='Decompile bin to hex')
parser.add_argument('source', help='input file')
parser.add_argument('destination', help='destination')

args = parser.parse_args()
with open(args.source) as fi, open(args.destination, 'w') as fo:
	data = fi.read()
	i = 0
	fo.write(": main\n")
	for x in data:
		fo.write("0x%02x%c" %(ord(x), '\n' if i == 31 else ' '))
		i += 1
		if i == 32:
			i = 0



