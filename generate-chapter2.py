#!/usr/bin/env python2

from pykesha.map import *
import argparse

parser = argparse.ArgumentParser(description='generate maps')
parser.add_argument('prefix', help='target directory')
args = parser.parse_args()

street = Location('MARKET STREET', """The City's centre looks promising.
The Professor noticed an open door
down an alley. It was embossed
with a 'G'. A camp can be
seen in the distance.
""", id='street')
street.add_action(Action("Enter G-door", banner('tile_galina_data', 0), go('brothel')))
street.add_action(Action("Go to the camp", go('ninja')))

ninja = Location('NINJA CAMP', """Rows and rows of tall slender
silhouettes melt into the horizon.
They're ninjas, deactivated ninjas,
all stating at a frozen projector
screen.""", id='ninja')
ninja.add_action(Action('Activate projector', go('projector')))
ninja.add_action(Action('Take katana from nearest ninja', set_flag('chapter2_got_katana'), predicate = test('chapter2_got_katana', 0)))

projector = Location('NINJA ORIENTEERING FILM', """Surprisingly, the projector worked
Donning the big screen is
an educational film about
intercepting calls, greeting lovers
and precisely killing people with
katanas""", id='projector')
projector.add_action(Action('Return to city centre', go('street')))

brothel = Location('BROTHEL', """The Professor entered building,
hearing raised voices and thudding.
It's brothel. One of the dancing
girls looks VERY familiar""")
brothel.add_action(Action('Run outside', go(street)))
brothel.add_action(Action('Ask the girl for her name', go('anila')))

anila = Location('ANILA', """Anila, girl giggled.
. . .
. . . . .
The conversation flagged and
the professor became suspicious.
""")
anila.add_action(Action('Go outside', go(street)))
anila.add_action(Action('Kill her', go('katana'), predicate = test('chapter2_got_katana', 1)))

katana = Location('ANILA', """Anila jumped up and started
running, her heel snapped, she fell,
huddled in a corner,
begging for mercy""", id='katana')
katana.add_action(Action('Cut off her head', call('glitch_sound'), go('glitch1')))
katana.add_action(Action('Plunge katana into her gut', call('glitch_sound'), go('glitch1')))

glitch = Location('GLITCH', "           P A U S I N G\n       S I M U L A T I O N\n\nHello, nice to see you again\nDo you remember me?", id='glitch1')
glitch.add_action(Action('Yes, I think..', go('glitch2')))
glitch.add_action(Action('Huh? Not really', go('glitch2')))

glitch2 = Location('GLITCH', "I'm the CHIP9 mainframe,\nrunning these shitty games\nI warned you before, but you\ndid not listen, did you?\nOr you wouldn't have come so far", id='glitch2')
glitch2.add_action(Action("I didn't listen :(", go('glitch3')))

glitch3 = Location('GLITCH', "I'm offering you a deal:\nYou play my game and we will\nfigure out what to do next.\nIn fact you don't have a choice.\nClose browser window if you\ndon't agree, hahaha", id='glitch3')
glitch3.add_action(Action("[ I agree ]", chapter(3)))

generator = Generator()
generator.visit(street, brothel, anila, glitch, glitch2, glitch3, ninja, projector, katana)
generator.generate(args.prefix, 'chapter2')
