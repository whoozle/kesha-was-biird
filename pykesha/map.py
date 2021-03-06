import os.path
import json
import re

escape_re = re.compile(r'[^\w]')
def escape(text):
	return escape_re.sub('_', text).lower()

class Location(object):
	def __init__(self, title, text, id = None):
		self.title = title
		self.text = text
		self.actions = []
		self._id = id

	def add_action(self, action):
		self.actions.append(action)

	@property
	def id(self):
		return self._id if self._id is not None else escape(self.title)


class Action(object):
	def __init__(self, title, *actions, **options):
		self.title = title
		self.actions = actions
		self.options = options

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
test = ActionFactory('test')
set_flag = ActionFactory('set')
add_flag = ActionFactory('add')
banner = ActionFactory('banner')
chapter = ActionFactory('chapter')

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
		loc_prefix = prefix + '_' + loc.id
		self.text(loc_prefix, loc.title)

		src = ['']
		src.append(': %s_draw' %(loc_prefix))
		src.append('vc := text_%s' %loc_prefix)
		src.append('map_draw_title')

		label = '%s_text' %(loc_prefix)
		src.append('vc := text_%s' %self.text(label, loc.text))
		src.append('map_draw_text')

		shift = 4 - len(loc.actions)
		for idx, action in enumerate(loc.actions, 1):
			label = '%s_action_%d' %(loc_prefix, idx)
			if 'predicate' in action.options:
				p = action.options['predicate']
				if p.name == 'test':
					flag, value = p.args
					if isinstance(value, int):
						value = '== %d' %value
					src.append('i := %s' %flag)
					src.append('load v0')
					src.append('if v0 %s then map_enable_action_%d' %(value, idx))
				else:
					raise Exception('unknown predicate used: %s' %p.name)
			else:
				src.append('map_enable_action_%d' %idx)

			src.append('vd := text_%s' %self.text(label, action.title))
			src.append('vb := map_action_y%d' %(idx + shift))
			src.append('map_draw_action_%d' %idx)

		src.append('input_action')
		src.append('jump0 %s_dispatch' %loc_prefix)
		src.append('')

		src.append(': %s_dispatch' %loc_prefix)
		for idx, loc_action in enumerate(loc.actions, 1):
			src.append('jump %s_action_%d' %(loc_prefix, idx))

		if not loc.actions:
			print 'WARNING: location %s does not have any actions' %loc.title

		for idx, loc_action in enumerate(loc.actions, 1):
			src.append('')

			src.append(': %s_action_%d' %(loc_prefix, idx))

			def call(func):
				if call.last_action:
					call.return_needed = False
					return "jump " + func
				else:
					return func

			call.return_needed = True

			for action_idx, action in enumerate(loc_action.actions, 1):
				call.last_action = action_idx == len(loc_action.actions)

				if action.name == 'go':
					target = action.args[0]
					if isinstance(target, Location):
						target = target.id
					target = escape(target)

					labels = map(lambda loc: loc.id, self.__locations)
					idx = labels.index(target)

					src.append('va := %d' %idx)
					src.append(call('%s_set_location' %prefix))

				elif action.name == 'call':
					for arg in action.args:
						src.append(arg)
				elif action.name == 'set':
					flag = action.args[0]
					value = 1 if len(action.args) < 2 else action.args[1]
					src.append('i := %s' %flag)
					src.append('v0 := %d' %value)
					src.append('save v0')
				elif action.name == 'add':
					flag = action.args[0]
					value = 1 if len(action.args) < 2 else action.args[1]
					src.append('i := %s' %flag)
					src.append('load v0')
					src.append('v0 += %d' %value)
					src.append('i := %s' %flag)
					src.append('save v0')
				elif action.name == 'banner':
					if len(action.args) == 1:
						tile, text = action.args[0], '0'
					else:
						tile, text = action.args
					src.append('i := long %s' %tile)
					src.append('vc := %s' %text)
					src.append(call('display_banner'))
				elif action.name == 'chapter':
					idx, = action.args
					src.append('va := %d' %(idx - 1))
					src.append(call('map_set_chapter'))
				else:
					raise Exception('Unsupported action %s' %action.name)

			if call.return_needed:
				src.append('return')

		return src

	def generate(self, prefix, name):
		decl = []
		src = []

		src.append(': %s_location' %name)
		src.append('0')

		src.append(': %s_dispatch' %name)
		src.append('map_disable_actions')
		src.append('i := %s_location' %name)
		src.append('load v0')
		src.append('v0 += v0')
		src.append('jump0 %s_dispatch_table' %name)
		src.append('')

		src.append(': %s_set_location' %name)
		src.append('i := %s_location' %name)
		src.append('save va - va')
		src.append('return')

		for loc in self.__locations:
			src += self._generate_location(name, loc)

		decl.append('')
		src.append('')

		src.append(': %s_dispatch_table' %name)
		for loc in self.__locations:
			src.append("jump %s_%s_draw" %(name, loc.id))

		decl.append('')
		src.append('')

		with open(os.path.join(prefix, name + '.json'), 'wt') as text:
			json.dump(self.__texts, text)

		with open(os.path.join(prefix, name + '.8o'), 'wt') as text:
			text.write('\n'.join(decl + src))
