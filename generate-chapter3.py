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

loc4 = Location('0x04', 'Gotcha! Hahaha')

generator = Generator()
generator.visit(loc1, loc2, loc3, loc4)
generator.generate(args.prefix, 'chapter3')
