#!/usr/bin/env python2

from pykesha.map import *
import argparse

parser = argparse.ArgumentParser(description='generate maps')
parser.add_argument('prefix', help='target directory')
args = parser.parse_args()

glitch = Location('GLITCH', "           P A U S I N G\n       S I M U L A T I O N\n\nHello, nice to see you again\nDo you remember me?")
glitch.add_action(Action('Yes'))
glitch.add_action(Action('Not really'))

generator = Generator()
generator.visit(glitch)
generator.generate(args.prefix, 'chapter2')
