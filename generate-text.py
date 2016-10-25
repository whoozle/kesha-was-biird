#!/usr/bin/env python2

import argparse
import os.path
import json

parser = argparse.ArgumentParser(description='Compile font.')
parser.add_argument('target', help='target directory')
parser.add_argument('address', help='target address')
parser.add_argument('sources', help='input file', nargs='+')
args = parser.parse_args()

offsets = []
data = []

addr = int(args.address, 16)
header = """\
:const data_text_hi 0x%02x
:const data_text_lo 0x%02x
""" %(addr >> 8, addr & 0xff)

def add(key, value):
	global header, offsets, data
	header += ":const text_%s %d\n" %(key, len(offsets))
	offsets.append(len(data))
	for ch in value:
		v = ord(ch) - 31
		if v < 0:
			raise Exception('invalid character %s' %repr(ch))
		data.append(v)
	data.append(0)

for source in args.sources:
	messages = json.load(open(source))
	for key, value in messages.iteritems():
		if isinstance(value, list):
			for idx, text in enumerate(value, 1):
				add('%s_%d' %(key, idx), text)
		else:
			add(key, value)

source = ":org 0x%04x\n" %(addr)
source += ": data_text\n\t "
source += " ".join(["0x%02x" %i for i in data])
source += "\n\n"
source += ": data_text_index\n\t"
source += " ".join(["0x%02x 0x%02x" %(x & 0xff, x >> 8) for x in offsets])
source += "\n\n"

with open(os.path.join(args.target, 'texts.8o'), 'w') as f:
	f.write(header)

with open(os.path.join(args.target, 'texts_data.8o'), 'w') as f:
	f.write(source)
