#!/usr/bin/env python2

from pykesha.map import *
import argparse

parser = argparse.ArgumentParser(description='generate maps')
parser.add_argument('prefix', help='target directory')
args = parser.parse_args()

lab = Location('LAB INTERIOR', 'Lab refused to die easily,\nsome unrecognizeable panels\nare still flashing with leds')

lab_ruins = Location('DEAD LAB ENTRANCE', "Black mouth of dead lab\nlays before you")
lab_ruins.add_action(Action('Go outside', go(lab_ruins)))

vault = Location('VAULT', "Vault was warm and cozy,\nalmost nothing reminiscents\nrecent fishapocalipse.")
vault.add_action(Action('Go outside', go(lab_ruins)))
vault.add_action(Action('Stay inside', rest()))

generator = Generator()
generator.visit(lab, vault, lab_ruins)

generator.generate(args.prefix, 'chapter1')
