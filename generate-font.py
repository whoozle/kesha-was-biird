#!/usr/bin/env python

def generate(name, file, addr, font_height = 5, space_width = 3):
	source = ":org 0x%04x\n" %addr
	source += ": font_%s_data\n" %name
	with open(file) as fontsource:
		font = {}
		while True:
			decl = fontsource.readline()
			if decl == '':
				break
			elif decl == '\n':
				continue
			decl = decl.split()
			if not decl:
				break
			if len(decl) == 3:
				char, height, width = (t(s) for t,s in zip((str, int, int), decl))
				descent = 0
			else:
				char, height, width, descent = (t(s) for t,s in zip((str, int, int, int), decl))

			width += 1 #shadow + interval
			if width > 8:
				raise "width is more than 8"

			rows, shadows = [], []
			for y in xrange(0, height):
				rowstr = fontsource.readline().rstrip()
				row = [1 if ch != ' ' else 0 for ch in rowstr]
				for x in xrange(len(row), width):
					row.append(0)

				#shadow
				shadow = [0 for i in xrange(0, width)]
				for i in xrange(1, width):
					x = width - 1 - i
					if row[x] and not row[x + 1]:
						shadow[x + 1] = 1
				#print y, row, shadow
				rows.append(row)
				shadows.append(shadow)

			font[char] = (height, width, descent, rows, shadows)

		#print font
		chars = [ord(x) - 31 for x in font.keys()]
		cmin, cmax = min(chars), max(chars)

		glyph = 0
		font_data = []
		index_source = ""
		for ch in xrange(cmin, cmax + 1):
			key = chr(ch + 31)
			if key in font:
				height, width, descent, rows, shadow = font[key]
				offset = len(font_data)
				assert height == len(rows)
				assert height == len(shadow)
				for data in [rows, shadow]:
					for row in data:
						value = 0
						for i in xrange(0, width):
							if row[i]:
								value |= (0x80 >> i)
						font_data.append(value)

				index_source += "%d 0x%02x 0x%02x %d %d " %(height, offset & 0xff, offset >> 8, width, (256 - descent) & 0xff)
				#print key, font[key]
				glyph += 1
			else:
				index_source += "0 0xff 0xff %d 0 " %space_width
	source += " ".join(["0x%02x" %x for x in font_data])
	source += "\n\n"
	source += ": data_%s_index\n%s\n\n" %(name, index_source)
	source += "#glyphs: %d, size: %d\n\n" %(glyph, len(font_data))
	header = """
: draw_{name}_char_error
	v0 := {space_width}
	return

: draw_font_char
	vf := 31
	vc -= vf

: _draw_{name}_char
	if vc < {min} then jump draw_{name}_char_error
	if vc > {max} then jump draw_{name}_char_error

	vc += -{min}
	v0 := vc
	v0 += vc
	i := long data_font_index
	i += v0
	i += v0
	i += vc
	load v4 #v0 height v1 v2 offset v3 width v4 ascend
	if v1 == -1 then jump draw_{name}_char_error

	i := draw_{name}_char_sprite_index
	ve := 0xb0
	v0 |= ve
	save v0

	v5 := v1
	v6 := v2

	v0 := {addrh}
	v1 := {addrl}
	v1 += v5
	v0 += vf
	v0 += v6
	i := draw_{name}_load_glyph_addr
	save v1

	0xf0 0x00
: draw_{name}_load_glyph_addr
	0x00 0x00

	vb += v4

:next draw_{name}_char_sprite_index
	sprite va vb 0
	vb -= v4
	v0 := v3
	return

""".format(min = cmin, max = cmax, name = name, space_width = space_width, addrh = addr >> 8, addrl = addr & 0xff)
	return header, source

import argparse
import os.path

parser = argparse.ArgumentParser(description='Compile font.')
parser.add_argument('source', help='input file')
parser.add_argument('name', help='input file')
parser.add_argument('segment', help='font data address in high mem (e.g. f000)')
parser.add_argument('target', help='target directory')
args = parser.parse_args()
addr = int(args.segment, 16)

decl, defn = generate(args.name, args.source, addr)
with open(os.path.join(args.target, args.name + ".8o"), "w") as f:
	f.write(decl)

with open(os.path.join(args.target, args.name + "_data.8o"), "w") as f:
	f.write(defn)

