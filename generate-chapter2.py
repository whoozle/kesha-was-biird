#!/usr/bin/env python2

from pykesha.map import *
import argparse

parser = argparse.ArgumentParser(description='generate maps')
parser.add_argument('prefix', help='target directory')
args = parser.parse_args()

glitch = Location('GLITCH', "           P A U S I N G\n       S I M U L A T I O N\n\nHello, nice to see you again\nDo you remember me?", id='glitch1')
glitch.add_action(Action('Yes', go('glitch2')))
glitch.add_action(Action('Not really', go('glitch2')))

glitch2 = Location('GLITCH', "I'm CHIP9 mainframe,\nrunning these shitty games\nI warned you before, but you\ndid not listen, did you?\nOr you wouldn't come so far", id='glitch2')
glitch2.add_action(Action("I didn't :(", go('glitch3')))

glitch3 = Location('GLITCH', "I'm offering you a deal:\nYou play my game and we will\nfigure out what to do next.\nIn fact you don't have a choice.\nClose browser window if you\ndon't agree, lol", id='glitch3')
glitch3.add_action(Action("[ I agree ]", chapter(3)))

generator = Generator()
generator.visit(glitch, glitch2, glitch3)
generator.generate(args.prefix, 'chapter2')
