import os.path
import json
import re

class Location(object):
	def __init__(self, title, text):
		self.title = title
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

class ActionFactory(object):
	class Impl(object):
		def __init__(self, name, args, kw):
			self.name, self.args, self.kw = name, args, kw

	def __init__(self, action):
		self.name = action

	def __call__(self, *args, **kw):
		return ActionFactory.Impl(self.name, args, kw)

go = ActionFactory('go')
rest = ActionFactory('rest')

class Generator(object):
	def __init__(self):
		self.__texts = {}
		self.__locations = []
		self.__counters = {}

	def next(self, name):
		value = self.__counters.get(name, 1)
		self.__counters[name] = value + 1
		return value

	def escape(self, text):
		return re.sub(r'[^\w]', '_', text).lower()

	def text(self, label, text):
		self.__texts[label] = text

	def visit(self, *locs):
		return

	def generate(self, prefix, name):
		decl = []
		src = []

		src.append(': %s_dispatch' %name)
		src.append('i := %s_state' %name)
		src.append('load v0')
		src.append('v0 += v0')
		src.append('jump0 %s_dispatch_table' %name)
		src.append('')

		with open(os.path.join(prefix, name + '.json'), 'wt') as text:
			json.dump(self.__texts, text)

		with open(os.path.join(prefix, name + '.8o'), 'wt') as text:
			text.write('\n'.join(decl + src))
