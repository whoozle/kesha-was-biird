#!/usr/bin/env python

import argparse
parser = argparse.ArgumentParser(description='Convert string to the sequence of strings')
parser.add_argument('text', help='text')
parser.add_argument('--right-align', help='text', default=0)
args = parser.parse_args()

ralign = int(args.right_align)
data = bytes(args.text)
n = len(data)
if ralign:
	print ":org 0x%04x" %(ralign - n + 512)
for ch in data:
	print hex(ord(ch)),
print


