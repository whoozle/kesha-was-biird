#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description='generate dialogs')
parser.add_argument('prefix', help='target directory')
args = parser.parse_args()

_dialog, _dialog_idx = 0, 0
_heads = None
_draw_heads = set()
_sleeps = set()
_source = ''
_heads_source = ''
_first_day = True
_texts = {}
_line = 0
_text = 0

for i in xrange(1, 5):
	_heads_source += """\
: dialog_draw_line_{line}
	va := dialog_line_{line}_x
	vb := dialog_line_{line}_y
	jump draw_text
""".format(line = i)

def clear_state():
	global _line, _heads
	_line = 1
	_heads = {1: '', 2: ''}

def dialog(dialog, idx):
	global _first_day, _source, _dialog, _dialog_idx, _text
	_dialog, _dialog_idx, _text = dialog, idx, 1
	if _first_day:
		_first_day = False
	else:
		_source += '\treturn\n\n'

	clear_state()
	_source += ': dialog_%s_%d\n\tpanel_draw\n' %(dialog, idx)

def head(idx, name):
	global _heads_source, _heads, _source
	if name:
		key = (idx, name)
		if key not in _draw_heads:
			_heads_source += """\
: heads_draw_{name}_{idx}
	v0 := dialog_head_{idx}_x
	v1 := dialog_head_{idx}_y
	i := long tile_{name}_data
	sprite v0 v1 0
	return\n\n""".format(name = name, idx = idx)
			_draw_heads.add(key)
	if _heads[idx]:
		_source += '\theads_draw_%s_%d\n' %(_heads[idx], idx) #erase old head
	_heads[idx] = name
	if name:
		_source += '\theads_draw_%s_%d\n' %(name, idx) #erase old head
	pass

def sleep(delay):
	global _source, _sleeps, _heads_source
	if delay > 0:
		if delay not in _sleeps:
			_sleeps.add(delay)
			_heads_source += """\
: sleep_{delay}
		va := {delay}
		jump sleep
""".format(delay = delay)

		_source += """\
	sleep_{delay}
""".format(delay = delay)

def text(text, delay = 60):
	global _source, _texts, _dialog, _dialog_idx, _line, _text
	id = 'dialog_%s_%d_%d' %(_dialog, _dialog_idx, _text)

	_source += """
	vc := text_{id}
	dialog_draw_line_{line}

""".format(line = _line, id = id)
	sleep(delay)

	_line += 1
	_text += 1
	_texts[id] = text

def call(name, *args, **kw):
	global _source
	if len(args) > 4:
		raise Exception("only 4 arguments supported")
	regs = ['va', 'vb', 'vc', 'vd']
	if kw:
		_source += '\n'.join(["\t%s := %s" %(reg, arg) for reg, arg in kw.iteritems()])
	_source += '\n'.join(["\t%s := %s" %(reg, arg) for reg, arg in zip(regs, args)])
	_source += '\n\t%s\n\n' %name

def skip_line():
	global _line
	_line += 1

def clear():
	clear_state()
	call('panel_draw')

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

_source += '\treturn\n\n'
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

""" + _heads_source + _source
	f.write(_source)

with open(os.path.join(prefix, 'dialogs.json'), 'w') as f:
	json.dump(_texts, f)
