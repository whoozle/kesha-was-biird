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

call('day_intertitle')
call('room_draw')
sleep(60)

clear()
head(1, 'kesha')
text("What a strange dream...")
text("What happened? I can", 0)
text("hardly remember anything...")
text("......")

dialog('galina', 1)
text("We really need to talk")
text("1113. Galina")

dialog('galina', 2)
head(1, 'kesha')
text("Hello! Who is this?")
head(2, 'cow')
text("It's Galina.")
head(1, 'kesha_o')
text("We need to talk")
head(2, '')
head(1, 'kesha_e')
text("I'll have a drink first")
call('drinking_draw')

dialog('galina', 3)
head(1, 'kesha_o')
text("Hi, it's Kesha")
head(2, 'cow')
text("Can we talk now?")
text("You need to find -", 0)

clear()

head(1, 'professor')
text('Excuse me, you two', 0)
text('love birds...')
text('Galina, I need you', 0)
text('RIGHT NOW!!!')
call('professor_show_banner')

dialog('galina', 4)
head(1, 'kesha_o')
text("Hi, it's me again")

head(2, 'cow')
text("Can we -", 0)

clear()

head(1, 'ninja')
text('Pardon me')
text('I\'d like to help you')
text('Call me, 1337', 120) #leet :D
call('ninja_show_banner')

dialog('galina', 5)
head(2, 'cow')
text("I don't know if you", 0)
text("remember, but you", 0)
text("have to save me.", 90)
text("I got the code.")

dialog('ninja', 1)
head(1, 'kesha_o')
text("Why are you", 0)
text("interrupting my calls?")

head(2, 'ninja')
text("Sorry, I have no choice")
text("I want to help you")

clear()
head(1, 'ninja')
text("I need to infiltrate", 0)
text("PROFESSOR'S lab")
text("And you are the key", 120)

clear()
head(1, 'ninja')
text('You\'re a secret agent', 0)
text('of the secret CHIP8', 0)
text('organization', 120)

clear()
head(1, 'ninja')
text('We erased your memory', 0)
text('to trick professor into', 0)
text('hiring you as a janitor')
call('ninja_show_eraser')
sleep(240)
clear()

head(1, 'ninja')
text('Galina is our agent too')
text('So we need to find her,')
text('EXTRACT THE KEY')
text('And stop the F-DAY', 120)
clear()

head(1, 'ninja')
text('Later, man')

dialog('ninja', 2)
head(1, 'ninja')
text("Hi, I followed professor.")
text("He's with his mum today")
text("It's time to act.", 0)
text("We need Galina's key", 120)
clear()
head(1, 'ninja')
text("She's a dog, you know")
text("She will not", 0)
text(" give her collar to us")
call('set_flag', i = 'pets_plan')

dialog('spam', 1)
text('Any problems with SPAM?')
text('Call 0-SPAM and we will', 30)
text('not send you anything')
text('    PROMISE')

dialog('spam', 2)
text('SPAMSPAMSPAMSPAM')
text('Any problems with PESTS?')
text('or PETS?')
text('call 0-PETS    or PEST')

dialog('pets', 1)
head(1, 'pets')
text('PETS (or PESTS) hotline.')
text('How can I help you?')
head(2, 'kesha')
text('STOP SPAMMING ME')

dialog('pets', 2)
#head(1, 'pets')
head(1, 'kesha')
text('Hello, I\'d like to', 0)
text('report stray dog in', 0)
text('the Lab district area')
clear()
head(1, 'pets')
text('Ok, we are on it')
skip_line()
head(2, 'kesha')
text('Thank you, bye...')

dialog('galina', 6)
head(1, 'kesha')
text('Hi, can we meet today?')
text('Yes I\'ll pick you up', 0)
text('at the lab')

dialog('ninja', 3)
head(1, 'ninja')
text('Well, Galina is safe now')
text('Call PETS and ask them if', 0)
text('she had any code on her collar')

dialog('pets', 3)
head(1, 'kesha')
text('Hello, could you tell me', 0)
text('if that dog had a', 0)
text('number on her collar')
clear()
head(1, 'pets')
text('Let me see....')
text('Well, yes, it says: ')
text('eight plus five star three', 150)

dialog('ninja', 4)
sleep(30)
call('audio_play_sync', i = 'long audio_click')
sleep(30)
head(1, 'kesha')
text('I heard a click', 120)
call('ninja_show_fday_device')
clear()
head(1, 'ninja')
text('STOP RIGHT THERE!!')
text("With the F-DAY device")
text("I can rule all the fishes", 0)
text("in the world!", 180)

dialog('ninja', 5)
head(1, 'ninja')
text('(ninja moves towards you)')
text('1 - FIGHT')
text('2 - ACTIVATE DEVICE')

dialog('ninja', 66)
head(1, 'ninja')
text("What do you think", 0)
text("you're doing?")
text("You cannot fight me")
text("You're weak, Kesha")

dialog('glitch', 1)
head(1, 'glitch')
text(': dialog_kesha_1', 0)
text('panel_draw', 0)
text('heads_draw_kesha_1')

clear()
head(1, 'glitch')
text('va := dialog_line_1_x', 0)
text('vb := dialog_line_1_y', 0)
text('vc := text_dialog_kesha_1_1', 0)
text('draw_text', 0)
call('glitch_fill')
call('glitch_voice')
sleep(60)

clear()
head(1, 'kesha')
text('What was that???')

dialog('glitch', 2)
head(1, 'glitch')

text('if lab_opened then kesha_dies')
call('glitch_voice')
text('if lab_opened then kesha_dies')
call('glitch_voice_next')
text('if lab_opened then kesha_dies')
call('glitch_voice_next')
text('if lab_opened then kesha_dies')
call('glitch_voice_next')

dialog('no_answer', 1)
call('audio_invalid_number')
head(1, 'kesha')
text("Hmm.. No answer", 60)

dialog('no_answer', 2)
head(1, 'disabled')
text("WHOSHOLLING", 30)
text("I'M DISABLED")
text("STOPITSTOPIT")
text("YOU CRANK")

dialog('no_answer', 3)
head(1, 'disabled')
text("YOU AGAIN")
text("I'M VETERAN")
text("NOW ILL KICK YOUR ASS")
text("TARD")

dialog('no_answer', 4)
head(1, 'disabled')
text("STOPCALLINGME")
text("IMDISABLEDVETERAN")
text("CHEWYOUBREAKFASTCHEW")
text("IMBECILE")

dialog('no_answer', 5)
head(2, 'fish')
text("  o o  O  o O")
text("   o  ")
text("    o O O ")
text("  O o  .  .")


#FINAL PUZZLE
dialog('lab_security', 1)
head(1, 'lab')
text("WELCOME TO HIGH", 0)
text("SECURE LAB", 30)
text("ENTER PIN", 0)

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
