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
		return label

	def visit(self, *locs):
		self.__locations += locs

	def _generate_location(self, prefix, loc):
		loc_prefix = prefix + '_' + escape(loc.title)
		self.text(loc_prefix, loc.title)

		src = ['']
		src.append(': %s_draw' %(loc_prefix))
		src.append('va := map_title_x')
		src.append('vb := map_title_y')
		src.append('vc := text_%s' %loc_prefix)
		src.append('draw_text')

		for idx, text in enumerate(loc.texts, 1):
			label = '%s_text_%d' %(loc_prefix, idx)
			
			src.append('vc := text_%s' %self.text(label, text))
			src.append('map_draw_text_%d' %idx)

		for idx, action in enumerate(loc.actions, 1):
			label = '%s_action_%d' %(loc_prefix, idx)
			src.append('vd := text_%s' %self.text(label, action.title))
			src.append('map_draw_action_%d' %idx)

		src.append('va := %d' %len(loc.actions))
		src.append('input_action')
		src.append('v0 += v0')
		src.append('jump0 %s_dispatch' %loc_prefix)
		src.append('')

		src.append(': %s_dispatch' %loc_prefix)
		for idx, loc_action in enumerate(loc.actions, 1):
			src.append('jump %s_action_%d' %(loc_prefix, idx))

		for idx, loc_action in enumerate(loc.actions, 1):
			src.append('')
			src.append(': %s_action_%d' %(loc_prefix, idx))
			for action in loc_action.actions:
				if action.name == 'go':
					target = action.args[0]
					if isinstance(target, Location):
						target = escape(target.title)

					labels = map(lambda loc: escape(loc.title), self.__locations)
					idx = labels.index(target)

					src.append('i := %s_location' %prefix)
					src.append('v0 := %d' %idx)
					src.append('save v0')

				elif action.name == 'call':
					for arg in action.args:
						src.append(arg)
				else:
					raise Exception('Unsupported action %s' %action.name)
			src.append('return')

		return src

	def generate(self, prefix, name):
		decl = []
		src = []

		src.append(': %s_location' %name)
		src.append('0')

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
