#!/usr/bin/env python

import argparse
from pykesha.dialogs import *

parser = argparse.ArgumentParser(description='generate dialogs')
parser.add_argument('prefix', help='target directory')
args = parser.parse_args()

dialog('kesha', 1)
head(1, 'fish')
text(' o o O O   . . o O o')
text('  .   O . O')
text('   O o O')

clear()
head(2, 'professor')
text('Yes, I understand, sir')
text('I can handle it')

clear()
head(1, 'fish')
text('    o o o O . . o .')
text('')
head(2, 'professor')
text('Yes, of course')
text('Good-bye, sir', 90)


import os.path
import json

prefix = args.prefix
with open(os.path.join(prefix, 'dialogs.8o'), 'w') as f:
	_source = """\
:const dialog_line_1_x 27
:const dialog_line_2_x 27
:const dialog_line_3_x 10
:const dialog_line_4_x 10

:const dialog_line_1_y 10
:const dialog_line_2_y 20
:const dialog_line_3_y 30
:const dialog_line_4_y 40

:const dialog_head_1_x 9
:const dialog_head_1_y 10

:const dialog_head_2_x 100
:const dialog_head_2_y 20

""" + get_heads_source() + get_source()
	_source += '\treturn\n\n'
	f.write(_source)

with open(os.path.join(prefix, 'dialogs.json'), 'w') as f:
	json.dump(get_texts(), f)
