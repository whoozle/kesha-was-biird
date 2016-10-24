#!/usr/bin/env python2

from pykesha.map import *
import argparse

parser = argparse.ArgumentParser(description='generate maps')
parser.add_argument('prefix', help='target directory')
args = parser.parse_args()

loc1 = Location('0x01', 'You\'re White Knight, you see\nblack tower in the distance\nWhat would you do?')
loc1.add_action(Action('Nothing', call('chapter3_restart')))
loc1.add_action(Action('Rush towards the tower', go('0x02')))
loc1.add_action(Action('Go home', call('chapter3_restart')))

loc2 = Location('0x02', 'See! You CAN\'T resist me!\nYou hear familiar G G GGGLN\nVVVvoice. Your next move?')
loc2.add_action(Action('Nothing', call('chapter3_restart')))
loc2.add_action(Action('Shout answer', call('chapter3_restart')))
loc2.add_action(Action('Bash tower door', go('0x03')))

loc3 = Location('0x03', 'All right, you won.\nNo more nasty reboots\nIt\'s dark')
loc3.add_action(Action('Cast light spell', call('zx_reboot'), go('0x04')))
loc3.add_action(Action('Light match', call('zx_reboot'), go('0x04')))
loc3.add_action(Action('Wait until you can see', call('zx_reboot'), go('0x04')))

loc4 = Location('0x04', 'Gotcha! Hahaha\nLike I said, NO MORE RESTARTS\n2 + 2 = ?')
loc4.add_action(Action('3', call('zx_reboot'), go('0x11')))
loc4.add_action(Action('5', call('zx_reboot'), go('0x11')))
loc4.add_action(Action('42', call('zx_reboot'), go('0x11')))

loc5 = Location('0x11', 'You\'re White Knight, you see\nblack tower in the distance\nHAHAHAHAHA HAHA HA :(')
loc5.add_action(Action('jump 0x01', go(loc1)))
loc5.add_action(Action('jump 0x11', go(loc5)))
loc5.add_action(Action('jump 0x12', go('0x12')))

loc6 = Location('0x12', 'You see telephone\nWhat number would you call?')
loc6.add_action(Action('FISH', go('0xFF')))

loc7 = Location('0xFF', 'Kesha:\nHello? Who\'s this?')
loc7.add_action(Action('o o O . o O', go('-1')))
loc7.add_action(Action('. . o . o O', go('-1')))
loc7.add_action(Action('. . o O O o', go('-1')))

loc8 = Location('-1', "It's pitchblack dark")
loc8.add_action(Action('DIE', go('-1')))

generator = Generator()
generator.visit(loc1, loc2, loc3, loc4, loc5, loc6, loc7, loc8)
generator.generate(args.prefix, 'chapter3')
