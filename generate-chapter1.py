#!/usr/bin/env python2

from pykesha.map import *
import argparse

parser = argparse.ArgumentParser(description='generate maps')
parser.add_argument('prefix', help='target directory')
args = parser.parse_args()

lab = Location('LAB INTERIOR', 'Lab refused to die easily,\nsome unrecognizeable panels\nare still flashing with leds')
lab.add_action(Action('Return to lab\'s entrance', go('dead_lab_entrance')))
lab.add_action(Action('Look into broken compartment', go('isotope'), predicate = test('chapter1_got_isotope', 0)))

f_ray = Location('F-RAY ISOTOPE', """F-ray isotope was glowing with
green light, which is physically
impossible, because green
isn't in black body's spectre
Professor thought
""", id='isotope')

f_ray.add_action(Action('Continue searching', go(lab)))
f_ray.add_action(Action('Pick isotope with tongs', set_flag('chapter1_got_isotope', 1), go(lab), predicate = test('chapter1_got_tongs', 1)))

chav = Location('CHAV FROM THE FUTURE', 'Hey you, have you seen\nthe sign there?', id='chav')
chav.add_action(Action("Yes, I have", banner('tile_chav_data', 'text_chav_thanks'), set_flag('chapter1_got_tongs', 1), go('dead_lab_entrance')))
chav.add_action(Action("Do nothing", banner('tile_chav_data', 'text_chav_thanks'), set_flag('chapter1_got_tongs', 1), go('dead_lab_entrance')))
chav.add_action(Action("Run", go('dead lab entrance')))

lab_ruins = Location('DEAD LAB ENTRANCE', "Black mouth of dead lab\nlays before you. Sign says\nRummaging punished by death.")
lab_ruins.add_action(Action('Enter dark corridor', go(lab)))
lab_ruins.add_action(Action('Return to vault', go('vault')))
lab_ruins.add_action(Action('Rummage through rubbish', banner('tile_chav_data', 'text_chav_greeting'), go(chav), predicate=test('chapter1_got_tongs', 0)))

vault_bed = Location('BED', "Professor lays in bed sleepless\nHe keeps thinking on his\nnew invention")
vault_bed.add_action(Action('Get out of bed', go('vault')))
vault_bed.add_action(Action('Try to sleep', banner('tile_dream_data', 'text_professors_dream')))
vault_bed.add_action(Action('Invent time machine', \
	set_flag('time_machine_invented'), banner('tile_time_machine_data', 'text_time_machine_invented'), \
	predicate=test('time_machine_invented', 0)))

vault = Location('VAULT', "Vault was warm and cozy,\nalmost nothing reminiscents\nrecent fishapocalipse.")
vault.add_action(Action('Go outside', go(lab_ruins)))
vault.add_action(Action('Stay inside', go(vault_bed)))
vault.add_action(Action('Go chapter 2', chapter(2)))


generator = Generator()
generator.visit(vault, lab, lab_ruins, vault_bed, chav, f_ray)

generator.generate(args.prefix, 'chapter1')
