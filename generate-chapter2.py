#!/usr/bin/env python2

from pykesha.map import *
import argparse

parser = argparse.ArgumentParser(description='generate maps')
parser.add_argument('prefix', help='target directory')
args = parser.parse_args()

street = Location('STREET', """City's centre looks promising.
Professor noticed plaque next
to the opened door saying 'G'
""")
street.add_action(Action("Enter G-door", banner('tile_galina_data', 0), go('brothel')))

brothel = Location('BROTHEL', """Professor entered building
and realised that it's brothel.
One of the dancing girls
looks VERY familiar""")
brothel.add_action(Action('Run outside', go(street)))
brothel.add_action(Action('Ask her name', go('anila')))

anila = Location('ANILA', """Anila, girl giggled.
Professor remembered that he
ain't got any money
""")
anila.add_action(Action('Go outside'))
anila.add_action(Action('Offer coin'))

glitch = Location('GLITCH', "           P A U S I N G\n       S I M U L A T I O N\n\nHello, nice to see you again\nDo you remember me?", id='glitch1')
glitch.add_action(Action('Yes', go('glitch2')))
glitch.add_action(Action('Not really', go('glitch2')))

glitch2 = Location('GLITCH', "I'm CHIP9 mainframe,\nrunning these shitty games\nI warned you before, but you\ndid not listen, did you?\nOr you wouldn't come so far", id='glitch2')
glitch2.add_action(Action("I didn't :(", go('glitch3')))

glitch3 = Location('GLITCH', "I'm offering you a deal:\nYou play my game and we will\nfigure out what to do next.\nIn fact you don't have a choice.\nClose browser window if you\ndon't agree, lol", id='glitch3')
glitch3.add_action(Action("[ I agree ]", chapter(3)))

generator = Generator()
generator.visit(street, brothel, anila, glitch, glitch2, glitch3)
generator.generate(args.prefix, 'chapter2')
