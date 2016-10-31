#!/usr/bin/env python2

import sys

while True:
	width = int(sys.stdin.readline(), 16)
	print (128 - width) / 2
