#!/usr/bin/env python2

from pykesha.map import *
import argparse

parser = argparse.ArgumentParser(description='generate maps')
parser.add_argument('prefix', help='target directory')
args = parser.parse_args()

street = Location('MARKET STREET', """City's centre looks promising.
Professor noticed plaque next to
the opened door saying 'G'.
There's some camp in the distance
""", id='street')
street.add_action(Action("Enter G-door", banner('tile_galina_data', 0), go('brothel')))
street.add_action(Action("Go camp", go('ninja')))

ninja = Location('NINJA CAMP', """Slender ranks of deactivated
ninjas were melting into
the horizon. They are staring at
the projection screen""", id='ninja')
ninja.add_action(Action('Activate projector', go('projector')))
ninja.add_action(Action('Take katana from nearest ninja', set_flag('chapter2_got_katana'), predicate = test('chapter2_got_katana', 0)))

projector = Location('NINJA EDUCATION FILM', """Surprising, but projector worked
You see education film about
intercepting calls, greeting lovers
and killing people with katana""", id='projector')
projector.add_action(Action('Return to city centre', go('street')))

brothel = Location('BROTHEL', """Professor entered building
and realised that it's brothel.
One of the dancing girls
looks VERY familiar""")
brothel.add_action(Action('Run outside', go(street)))
brothel.add_action(Action('Ask for her name', go('anila')))

anila = Location('ANILA', """Anila, girl giggled.
. . .
The conversation flagged.
""")
anila.add_action(Action('Go outside', go(street)))
anila.add_action(Action('Kill her', go('katana'), predicate = test('chapter2_got_katana', 1)))

katana = Location('ANILA', """Anila started running, fell
and huddled in a corner
asking for mercy""", id='katana')
katana.add_action(Action('Cut her head off', go('glitch1')))
katana.add_action(Action('Plunge katana into her gut', go('glitch1')))

glitch = Location('GLITCH', "           P A U S I N G\n       S I M U L A T I O N\n\nHello, nice to see you again\nDo you remember me?", id='glitch1')
glitch.add_action(Action('Yes', go('glitch2')))
glitch.add_action(Action('Not really', go('glitch2')))

glitch2 = Location('GLITCH', "I'm CHIP9 mainframe,\nrunning these shitty games\nI warned you before, but you\ndid not listen, did you?\nOr you wouldn't come so far", id='glitch2')
glitch2.add_action(Action("I didn't :(", go('glitch3')))

glitch3 = Location('GLITCH', "I'm offering you a deal:\nYou play my game and we will\nfigure out what to do next.\nIn fact you don't have a choice.\nClose browser window if you\ndon't agree, lol", id='glitch3')
glitch3.add_action(Action("[ I agree ]", chapter(3)))

generator = Generator()
generator.visit(street, brothel, anila, glitch, glitch2, glitch3, ninja, projector, katana)
generator.generate(args.prefix, 'chapter2')
