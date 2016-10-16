#!/usr/bin/env python2

from pykesha.map import *
import argparse

parser = argparse.ArgumentParser(description='generate maps')
parser.add_argument('prefix', help='target directory')
args = parser.parse_args()

lab_ruins = Location('DEAD LAB')
lab_ruins_def = State("Black mouth of dead lab\nlays before you")
lab_ruins.add_state('default', lab_ruins_def)

#vault.text("Proffesor woke up.")
#vault.text("It's been three years")
#vault.text("after that tragic night.")
#vault.text("But memories, they still haunt him")

vault = Location('VAULT')

vault_def = State("Vault was warm and cozy,\nalmost nothing reminiscents\nrecent fishapocalipse.")
vault_def.add_action(Action('Go outside', go(lab_ruins)))
vault_def.add_action(Action('Stay inside', rest()))

vault.add_state('default', vault_def)

generator = Generator()
generator.visit(vault)
generator.visit(lab_ruins)

generator.generate(args.prefix)