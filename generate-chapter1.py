#!/usr/bin/env python2

from pykesha.map import *
import argparse

parser = argparse.ArgumentParser(description='generate maps')
parser.add_argument('prefix', help='target directory')
args = parser.parse_args()

lab = Location('LAB INTERIOR', """Lab refused to die easily,
some unrecognizeable panels
are still flashing with leds""")

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

chav = Location('RUMMAGE PUNISHER', """Hey you, have you seen
the sign there?""", id='chav')
chav.add_action(Action("Yes, I have", banner('tile_chav_data', 'text_chav_thanks'), set_flag('chapter1_got_tongs', 1), go('dead_lab_entrance')))
chav.add_action(Action("Do nothing", banner('tile_chav_data', 'text_chav_thanks'), set_flag('chapter1_got_tongs', 1), go('dead_lab_entrance')))
chav.add_action(Action("Run", go('dead lab entrance')))

lab_ruins = Location('DEAD LAB ENTRANCE',
"""Black mouth of dead lab
lays before you. Sign says
"Rummaging is punished by death".""")

lab_ruins.add_action(Action('Enter dark corridor', go(lab)))
lab_ruins.add_action(Action('Return to vault', go('vault')))
lab_ruins.add_action(Action('Rummage through rubbish', banner('tile_chav_data', 'text_chav_greeting'), go(chav), predicate=test('chapter1_got_tongs', 0)))

crater = Location('CRATER', """Crater was perfectly round
You see ninja's remains covered
by rotten black robes.
""")
crater.add_action(Action("Go back", go('vault')))
crater.add_action(Action("Stay sadly for a while"))
crater.add_action(Action("Kick ninja's corpse", go('ninja'), predicate = test('chapter1_got_fish', 0)))

ninja = Location("NINJA'S CORPSE", """Ninja's robes turned to dust as
professor's shoe touched them.
There's something underneath it.""", id='ninja')
ninja.add_action(Action("Examine ninja's remains", go('ninja2')))

ninja2 = Location("NINJA'S CORPSE", """You see dried fish head,
which looks very familiar""", id='ninja2')
ninja2.add_action(Action('Pick up dried fish head', set_flag('chapter1_got_fish'), go("crater")))

vault_bed = Location('BED', """Professor lays in bed sleepless
He keeps thinking on his
new invention""")

vault_bed.add_action(Action('Get out of bed', go('vault')))
vault_bed.add_action(Action('Try to sleep', banner('tile_dream_data', 'text_professors_dream')))
vault_bed.add_action(Action('Invent time machine', \
	set_flag('time_machine_invented'), banner('tile_time_machine_data', 'text_time_machine_invented'), \
	predicate=test('time_machine_invented', 0)))

vault = Location('VAULT', """Vault was warm and cozy,
almost nothing reminiscents
recent fishapocalipse.""")

vault.add_action(Action('Stay inside', go(vault_bed)))
vault.add_action(Action("Go lab's ruins", go(lab_ruins)))
vault.add_action(Action("Take a walk around crater", go(crater)))

kesha = Location('KESHA MACHINE', """Kesha's head is floating in tank,
ready for action""", id = 'kesha')

kesha.add_action(Action('Call professor', call('dialog_kesha_1'), go('kesha2')))

kesha2 = Location('KESHA MACHINE', """I warned professor from the past,
but nothing happened, why?
I looks that we have to try
different way to warn him
""", id = 'kesha2')
kesha2.add_action(Action('Go city centre', chapter(2)))

generator = Generator()
generator.visit(vault, lab, lab_ruins, vault_bed, chav, f_ray, kesha, kesha2, crater, ninja, ninja2)

generator.generate(args.prefix, 'chapter1')
