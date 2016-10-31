#!/usr/bin/env python2

from pykesha.map import *
import argparse

parser = argparse.ArgumentParser(description='generate maps')
parser.add_argument('prefix', help='target directory')
args = parser.parse_args()

lab = Location('LAB INTERIOR', """Lab clung on to operation.
Among the rubble mangled panels
refused to die, blinking franticly
among the dust and rubble.""")

lab.add_action(Action('Return to lab\'s entrance', go('dead_lab_entrance')))
lab.add_action(Action('Look into broken compartment', go('isotope'), predicate = test('chapter1_got_isotope', 0)))

f_ray = Location('F-RAY ISOTOPE', """ The professor was confused.
The F-ray isotope emitted
a green glow, which is physically
impossible because green
isn't in the black body's spectre!
""", id='isotope')

f_ray.add_action(Action('Continue searching', go(lab)))
f_ray.add_action(Action('Pick up isotope with tongs', set_flag('chapter1_got_isotope', 1), go(lab), predicate = test('chapter1_got_tongs', 1)))

chav = Location('ANTI-LOOTING BRUTE', """OII MUSH, Are you grievin' me?
Read the sign or I'll shank off
ya theivin' mits !""", id='chav')
chav.add_action(Action("I dropped it can I have it back?", banner('tile_chav_data', 'text_chav_thanks'), set_flag('chapter1_got_tongs', 1), go('dead_lab_entrance')))
chav.add_action(Action("Do nothing", banner('tile_chav_data', 'text_chav_thanks'), set_flag('chapter1_got_tongs', 1), go('dead_lab_entrance')))
chav.add_action(Action("Run", go('dead lab entrance')))

lab_ruins = Location('DECAYING LAB ENTRANCE',
"""The dark mouth like entrance of
the dying lab lays before you.
Sign says
"Looting is punishable by death".""", id='dead_lab_entrance')

lab_ruins.add_action(Action('Enter the dark corridor', go(lab)))
lab_ruins.add_action(Action('Return to the vault', go('vault')))
lab_ruins.add_action(Action('Rummage through the rubble', banner('tile_chav_data', 'text_chav_greeting'), go(chav), predicate=test('chapter1_got_tongs', 0)))

crater = Location('CRATER', """The crater is perfectly round,
You see ninja's remains covered
by disintegrating black robes.
""")
crater.add_action(Action("Go back", go('vault')))
crater.add_action(Action("Reflect on ninja's death"))
crater.add_action(Action("Kick Ninja's corpse", go('ninja'), predicate = test('chapter1_got_fish', 0)))

ninja = Location("NINJA'S CORPSE", """Ninja's robes turned to dust as
professor's passed through his corpse.
It smells like old books! There's
something underneath the corpse.""", id='ninja')
ninja.add_action(Action("Examine ninja's remains", go('ninja2')))

ninja2 = Location("NINJA'S CORPSE", """You see a see a mummified fish head,
which looks very familiar!""", id='ninja2')
ninja2.add_action(Action('Pick up dried fish head', set_flag('chapter1_got_fish'), go("crater")))

vault_bed = Location('BED', """The Professor lays in bed,
eyes wide open, sleepless,
fixated on his new invention""")

vault_bed.add_action(Action('Get out of the bed', go('vault')))
vault_bed.add_action(Action('Try to sleep', banner('tile_dream_data', 'text_professors_dream')))
vault_bed.add_action(Action('Begin inventing', \
	set_flag('chapter1_time_machine_invented'), banner('tile_time_machine_data', 'text_time_machine_invented'), \
	predicate=test('chapter1_time_machine_invented', 0)))

vault = Location('VAULT', """The Vault was warm and cozy,
the recent fishapocalipse fimly
at the back of the professors mind.""")

vault.add_action(Action('Stay in the warmth & safety', go(vault_bed)))
vault.add_action(Action("Go lab's ruins", go('dead_lab_entrance')))
vault.add_action(Action("Take a walk around the crater", go(crater)))
vault.add_action(Action("Work on the time machine", go("time_machine"), predicate = test('chapter1_time_machine_invented', 1)))

tm = Location('Time Machine', """The Time machine was almost ready
Frustratingly only a few pieces are
needed to complete his masterpiece""")

tm.add_action(Action("Return to vault", go(vault)))
tm.add_action(Action("Place the fish head in the tank", add_flag('chapter1_tm_stage'), set_flag('chapter1_got_fish', 2), call('time_machine_fish'), predicate = test('chapter1_got_fish', 1)))
tm.add_action(Action("Screw in the f-ray container", add_flag('chapter1_tm_stage'), set_flag('chapter1_got_isotope', 2), call('time_machine_isotope'), predicate = test('chapter1_got_isotope', 1)))
tm.add_action(Action("Flip the big red toggle switch!", go('kesha'), call('time_machine_activated'), predicate = test('chapter1_tm_stage', '>= 2')))

kesha = Location('KESHA MACHINE', """Suddenly the professor began to
recognise the mummified fish
head's face. It was Kesha's!
He left it carefully floating
in tank, ready for action""", id = 'kesha')

kesha.add_action(Action('Call professor-from-the-past', call('dialog_kesha_1'), go('kesha2')))

kesha2 = Location('KESHA MACHINE', """I tried to warn the professor from
the past, but nothing happened...
It looks that we'll have to try
something else. We need to warn him!
""", id = 'kesha2')
kesha2.add_action(Action('Go to city centre', chapter(2)))

generator = Generator()
generator.visit(vault, lab, lab_ruins, vault_bed, chav, f_ray, kesha, kesha2, crater, ninja, ninja2, tm)

generator.generate(args.prefix, 'chapter1')
