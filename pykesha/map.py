import os.path
import json
import re

class Location(object):
	def __init__(self, title):
		self.title = title
		self.states = {}

	def add_state(self, name, state):
		self.states[name] = state

class State(object):
	def __init__(self, text):
		self.texts = []
		self.actions = []
		self.text(text)

	def text(self, text):
		self.texts += text.split('\n')

	def add_action(self, action):
		self.actions.append(action)


class Action(object):
	def __init__(self, title, action):
		self.title = title
		self.action = action

class ActionImpl(object):
	def __init__(self, action):
		self.action = action

	def __call__(self, *args, **kw):
		self.args = args
		self.kw = kw

go = ActionImpl('go')

class Generator(object):
	def __init__(self):
		self.__texts = {}
		self.__locations = []
		self.__counters = {}
		self.__source = []
		self.__states = []

	def next(self, name):
		value = self.__counters.get(name, 1)
		self.__counters[name] = value + 1
		return value

	def escape(self, text):
		return re.sub(r'[^\w]', '_', text).lower()

	def text(self, prefix, text):
		label = 'map_%s_draw_title' %prefix
		self.__texts[label] = text
		return label

	def visit(self, loc):
		self.__locations.append(loc)

	def generate_location(self, loc):
		src = self.__source
		prefix = self.escape(loc.title)
		src.append(':map_%s_draw_title' %prefix)
		src.append('va := 10')
		src.append('vb := 0')
		src.append('vc := %s' %self.text(prefix, loc.title))
		src.append('jump draw_text')
		src.append('')
		for name, state in loc.states.iteritems():
			print name, state

	def generate(self, prefix):
		src = self.__source
		src.append(':map_dispatch')
		src.append('i := map_state')
		src.append('load v0')
		src.append('i := map_dispatch_table')
		src.append('jump0 v0')
		src.append('')

		for loc in self.__locations:
			self.generate_location(loc)

		src.append(':map_dispatch_table')
		src += self.__states
		src.append('')
		with open(os.path.join(prefix, 'map.json'), 'wt') as text:
			json.dump(self.__texts, text)

		with open(os.path.join(prefix, 'map.8o'), 'wt') as text:
			text.write('\n'.join(self.__source))
