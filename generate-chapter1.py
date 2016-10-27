#!/usr/bin/env python2

from pykesha.map import *
import argparse

parser = argparse.ArgumentParser(description='generate maps')
parser.add_argument('prefix', help='target directory')
args = parser.parse_args()

lab = Location('LAB INTERIOR', 'Lab refused to die easily,\nsome unrecognizeable panels\nare still flashing with leds')
lab.add_action(Action('Look into broken compartment'))

lab_ruins = Location('DEAD LAB ENTRANCE', "Black mouth of dead lab\nlays before you")
lab_ruins.add_action(Action('Enter dark corridor', go(lab)))
lab_ruins.add_action(Action('Go outside', go(lab_ruins)))

vault_bed = Location('BED', "Professor lays in bed sleepless\nHe keeps thinking on his\nnew invention")
vault_bed.add_action(Action('Get out of bed', go('vault')))
vault_bed.add_action(Action('Try to sleep', banner('tile_dream_data', 'text_professors_dream')))
vault_bed.add_action(Action('Invent time machine', \
	set_flag('time_machine_invented'), banner('tile_time_machine_data', 'text_time_machine_invented'), \
	predicate=test('time_machine_invented', 0)))

vault = Location('VAULT', "Vault was warm and cozy,\nalmost nothing reminiscents\nrecent fishapocalipse.")
vault.add_action(Action('Go outside', go(lab_ruins)))
vault.add_action(Action('Stay inside', go(vault_bed)))


generator = Generator()
generator.visit(vault, lab, lab_ruins, vault_bed)

generator.generate(args.prefix, 'chapter1')
