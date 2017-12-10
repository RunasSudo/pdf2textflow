#!/usr/bin/env python3
#   pdf2textflow - Extract text from PDF, automatically reflowing text
#   Copyright © 2017  RunasSudo (Yingtong Li)
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

from lxml import etree

import argparse
import sys

args = argparse.Namespace()
_, args.infile, args.crop_x, args.crop_y, args.crop_w, args.crop_h, args.r_margin = sys.argv
args.crop_x, args.crop_y, args.crop_w, args.crop_h, args.r_margin = int(args.crop_x), int(args.crop_y), int(args.crop_w), int(args.crop_h), int(args.r_margin)

parser = etree.XMLParser(recover=True)
with open(args.infile, 'r') as f:
	tree = etree.parse(f, parser)
root = tree.getroot()

last_x = None
last_w = None
for page in root.iterfind('page'):
	last_y = None
	last_h = None
	
	crop_y = int(page.get('height')) - args.crop_y - args.crop_h # PDF counts from top, Inkscape counts from bottom
	
	for elem in page.iterfind('text'):
		text = etree.tostring(elem, method='text', encoding='unicode').strip()
		
		if len(text) == 0:
			continue
		
		x, y, w, h = int(elem.get('left')), int(elem.get('top')), int(elem.get('width')), int(elem.get('height'))
		
		if x + w < args.crop_x or x > args.crop_x + args.crop_w or y + h < crop_y or y > crop_y + args.crop_h:
			# Outside crop box
			continue
		
		# OK! Print the text
		
		if last_x is None:
			is_continuation = False
		elif last_y is None:
			# Assume no page breaks in paragraphs
			is_continuation = False
		#elif last_y is None or last_y + last_h - y < 10:
		elif y - (last_y + last_h) < 0:
			# Vertical overlap
			is_continuation = True
		elif y - (last_y + last_h) < 10:
			if last_x + last_w > args.r_margin:
				is_continuation = True
			else:
				is_continuation = False
		else:
			is_continuation = False
		
		if is_continuation:
			print(' ', end='')
		else:
			# Don't print a newline on the first page
			if last_x is not None:
				print()
		
		print(text, end='')
		
		last_x = x
		last_y = y
		last_w = w
		last_h = h
