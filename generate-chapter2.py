#!/usr/bin/env python2

from pykesha.map import *
import argparse

parser = argparse.ArgumentParser(description='generate maps')
parser.add_argument('prefix', help='target directory')
args = parser.parse_args()

glitch = Location('GLITCH', 'FINALLY WE MET\nWhat do you think you\ndo in this CHIP8 realm?')
glitch.add_action(Action('Nothing'))

glitch2 = Location('GLITCH', "No. You keep playing this goddamn game!", id='glitch2')
glitch2.add_action(Action('Stop'))

generator = Generator()
generator.visit(glitch)
generator.generate(args.prefix, 'chapter2')
