#!/usr/bin/env python2

from pykesha.map import *
import argparse

parser = argparse.ArgumentParser(description='generate maps')
parser.add_argument('prefix', help='target directory')
args = parser.parse_args()

glitch = Location('GLITCH', "")
glitch.add_action(Action('Nothing'))

generator = Generator()
generator.visit(glitch)
generator.generate(args.prefix, 'chapter2')
