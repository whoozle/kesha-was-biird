import os.path
import json
import re

escape_re = re.compile(r'[^\w]')
def escape(text):
	return escape_re.sub('_', text).lower()

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
	def __init__(self, title, *actions):
		self.title = title
		self.actions = actions

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
restart = ActionFactory('restart')
call = ActionFactory('call')

class Generator(object):
	def __init__(self):
		self.__texts = {}
		self.__locations = []
		self.__counters = {}

	def next(self, name):
		value = self.__counters.get(name, 1)
		self.__counters[name] = value + 1
		return value


	def text(self, label, text):
		self.__texts[label] = text

	def visit(self, *locs):
		self.__locations += locs

	def _generate_location(self, prefix, loc):
		loc_prefix = escape(loc.title)

		src = ['']
		src.append(': %s_%s_draw' %(prefix, loc_prefix))
		src.append('return')
		return src

	def generate(self, prefix, name):
		decl = []
		src = []

		src.append(': %s_dispatch' %name)
		src.append('i := %s_location' %name)
		src.append('load v0')
		src.append('v0 += v0')
		src.append('jump0 %s_dispatch_table' %name)
		src.append('')

		for loc in self.__locations:
			src += self._generate_location(name, loc)

		decl.append('')
		src.append('')

		src.append(': %s_dispatch_table' %name)
		for loc in self.__locations:
			src.append("jump %s_%s_draw" %(name, escape(loc.title)))

		decl.append('')
		src.append('')

		with open(os.path.join(prefix, name + '.json'), 'wt') as text:
			json.dump(self.__texts, text)

		with open(os.path.join(prefix, name + '.8o'), 'wt') as text:
			text.write('\n'.join(decl + src))
