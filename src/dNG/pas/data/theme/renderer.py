# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.theme.Renderer
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;http;core

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasHttpCoreVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from copy import copy
from os import path
import os
import re

from dNG.data.file import File
from dNG.pas.data.settings import Settings
from dNG.pas.data.traced_exception import TracedException
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.text.tag_parser.abstract import Abstract as AbstractTagParser
from dNG.pas.data.text.tag_parser.block_mixin import BlockMixin
from dNG.pas.data.text.tag_parser.each_mixin import EachMixin
from dNG.pas.data.text.tag_parser.if_condition_mixin import IfConditionMixin
from dNG.pas.data.text.tag_parser.mapped_element_mixin import MappedElementMixin
from dNG.pas.data.text.tag_parser.rewrite_mixin import RewriteMixin
from dNG.pas.module.named_loader import NamedLoader

class Renderer(AbstractTagParser, BlockMixin, EachMixin, IfConditionMixin, MappedElementMixin, RewriteMixin):
#
	"""
The theme renderer parses and renders a template file.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Renderer)

:since: v0.1.00
		"""

		AbstractTagParser.__init__(self)
		MappedElementMixin.__init__(self)

		self.cache_instance = NamedLoader.get_singleton("dNG.pas.data.Cache", False)
		"""
Cache instance
		"""
		self.content = None
		"""
Content cache for OSet template replacements
		"""
		self.css_files = [ ]
		"""
CSS files to be added.
		"""
		self.js_files = [ ]
		"""
JavaScript files to be added.
		"""
		self.log_handler = NamedLoader.get_singleton("dNG.pas.data.logging.LogHandler", False)
		"""
The LogHandler is called whenever debug messages should be logged or errors
happened.
		"""
		self.path = Settings.get("path_themes", "{0}/themes".format(Settings.get("path_data")))
		"""
Path to the themes directory
		"""
		self.theme = None
		"""
Selected output theme
		"""
		self.theme_subtype = "site"
		"""
Output theme subtype
		"""
		self.title = None
		"""
Page title
		"""
	#

	def add_js_file(self, js_file):
	#
		"""
Add the defined javascript file to the output.

:param js_file: JS file name

:since: v0.1.00
		"""

		if (js_file not in self.js_files): self.js_files.append({ "name": js_file })
	#

	def _get_unique_filelist(self, raw_list):
	#
		"""
Sets the theme to use.

:param theme: Output theme

:return: (list) List with unique file entries
:since: v0.1.00
		"""

		_return = [ ]
		names_list = [ ]

		if (len(raw_list) > 0):
		#
			for entry in raw_list:
			#
				if (entry['name'] not in names_list):
				#
					names_list.append(entry['name'])
					_return.append(entry)
				#
			#
		#

		return _return
	#

	def is_supported(self, theme, subtype = None):
	#
		"""
Sets the theme to use.

:param theme: Output theme
:param subtype: Output theme subtype

:since: v0.1.00
		"""

		_return = False

		if (theme != None):
		#
			file_pathname = path.normpath("{0}/{1}/{2}.tsc".format(self.path, theme.replace(".", "/"), ("site" if (subtype == None) else subtype)))
			_return = os.access(file_pathname, os.R_OK)
		#

		return _return
	#

	def _parser_change(self, tag_definition, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the matched tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.00
		"""

		_return = data[:tag_position]

		data_closed = data[self._parser_tag_find_end_position(data, tag_end_position):]

		if (tag_definition['tag'] == "block"):
		#
			re_result = re.match("^\\[block(:(\\w+):([\\w\\.]+)){0,1}\\]", data[tag_position:data_position])

			if (re_result != None):
			#
				if (re_result.group(1) != None):
				#
					source = re_result.group(2)
					key = re_result.group(3)
				#
				else: source = None

				if (source == None): _return += self.render_block(data[data_position:tag_end_position])
				elif (source == "content"): _return += self.render_block(data[data_position:tag_end_position], "content", self._mapped_element_update("content", self.content), key)
				elif (source == "settings"): _return += self.render_block(data[data_position:tag_end_position], "settings", self._mapped_element_update("settings", Settings.get_instance()), key)
			#

			_return += data_closed
		#
		elif (tag_definition['tag'] == "each"):
		#
			re_result = re.match("^\\[each:(\\w+):([\\w\\.]+):([\\w\\.]+)\\]", data[tag_position:data_position])

			source = (None if (re_result == None) else re_result.group(1))

			if (source != None):
			#
				key = re_result.group(2)
				mapping_key = re_result.group(3)

				if (source == "content"): _return += self.render_each(data[data_position:tag_end_position], "content", self._mapped_element_update("content", self.content), key, mapping_key)
				elif (source == "settings"): _return += self.render_each(data[data_position:tag_end_position], "settings", self._mapped_element_update("settings", Settings.get_instance()), key, mapping_key)
			#

			_return += data_closed
		#
		elif (tag_definition['tag'] == "if"):
		#
			re_result = re.match("^\\[if:(\\w+):([\\w\\.]+)(\\s*)(\\!=|==)(.*?)\\]", data[tag_position:data_position])

			source = (None if (re_result == None) else re_result.group(1))

			if (source != None):
			#
				key = re_result.group(2)
				operator = re_result.group(4)
				value = re_result.group(5).strip()

				if (source == "content"): _return += self.render_if_condition(self._mapped_element_update("content", self.content), key, operator, value, data[data_position:tag_end_position])
				elif (source == "settings"): _return += self.render_if_condition(self._mapped_element_update("settings", Settings.get_instance()), key, operator, value, data[data_position:tag_end_position])
			#

			_return += data_closed
		#
		elif (tag_definition['tag'] == "rewrite"):
		#
			source = re.match("^\\[rewrite:(\\w+)\\]", data[tag_position:data_position]).group(1)
			key = data[data_position:tag_end_position]

			if (source == "content"): _return += self.render_rewrite(self._mapped_element_update("content", self.content), key)
			elif (source == "l10n"): _return += self.render_rewrite(self._mapped_element_update("l10n", L10n.get_instance()), key)
			elif (source == "settings"): _return += self.render_rewrite(self._mapped_element_update("settings", Settings.get_instance()), key)

			_return += data_closed
		#
		else: _return += data_closed

		return _return
	#

	def _parser_check(self, data):
	#
		"""
Check if a possible tag match is a false positive.

:param data: Data starting with the possible tag

:return: (dict) Matched tag definition; None if false positive
:since:  v0.1.00
		"""

		_return = None

		i = 0
		tags = [ "block", "each", "if", "rewrite" ]
		tags_length = len(tags)

		while (_return == None and i < tags_length):
		#
			tag = tags[i]
			data_match = data[1:1 + len(tag)]

			if (data_match == "block"):
			#
				re_result = re_result = re.match("^\\[block(:\\w+:[\\w\\.]+){0,1}\\]", data)
				if (re_result != None): _return = { "tag": "block", "tag_end": "[/block]", "type": "top_down" }
			#
			elif (data_match == "each"):
			#
				re_result = re.match("^\\[each:\\w+:[\\w\\.]+:[\\w\\.]+\\]", data)
				if (re_result != None): _return = { "tag": "each", "tag_end": "[/each]", "type": "top_down" }
			#
			elif (data_match == "if"):
			#
				re_result = re.match("^\\[if:\\w+:[\\w\\.]+\\s*(\\!=|==).*?\\]", data)
				if (re_result != None): _return = { "tag": "if", "tag_end": "[/if]", "type": "top_down" }
			#
			elif (data_match == "rewrite"):
			#
				re_result = re.match("^\\[rewrite:(\\w+)\\]", data)
				if (re_result != None and re_result.group(1) in [ "content", "l10n", "settings" ]): _return = { "tag": "rewrite", "tag_end": "[/rewrite]" }
			#

			i += 1
		#

		return _return
	#

	def render(self, content):
	#
		"""
Renders content ready for output from the given OSet template.

:param content: Content data

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Renderer.render(template_data, content)- (#echo(__LINE__)#)")

		theme = self.theme
		theme_subtype = self.theme_subtype

		file_pathname = path.normpath("{0}/{1}/{2}.tsc".format(self.path, theme, theme_subtype))

		if (theme_subtype != "site" and (not os.access(file_pathname, os.R_OK))):
		#
			file_pathname = path.normpath("{0}/{1}/site.tsc".format(self.path, theme))
			theme_subtype = "site"
		#

		theme_data = (None if (self.cache_instance == None) else self.cache_instance.get_file(file_pathname))

		if (theme_data == None):
		#
			file_obj = File()
			if (not file_obj.open(file_pathname, True, "r")): raise TracedException("Failed to open theme file for '{0}'".format(self.theme))

			theme_data = file_obj.read()
			file_obj.close()

			if (theme_data == False): raise TracedException("Failed to read theme file for '{0}'".format(self.theme))
			if (self.cache_instance != None): self.cache_instance.set_file(file_pathname, theme_data)
		#

		"""
Read corresponding theme configuration
		"""

		file_pathname = file_pathname[:-3] + "json"
		Settings.read_file(file_pathname)

		if (self.title == None): self.title = Settings.get("pas_html_title", "Unconfigured site")

		self.content = {
			"page_title": self.title,
			"page_content": content
		}

		theme_settings = Settings.get("pas_http_theme_{0}".format(theme))

		css_files = (self.css_files.copy() if (hasattr(self.css_files, "copy")) else copy(self.css_files))
		js_files = (self.js_files.copy() if (hasattr(self.js_files, "copy")) else copy(self.js_files))

		if (theme_settings != None and theme_subtype in theme_settings):
		#
			if ("css_files" in theme_settings[theme_subtype]): css_files += theme_settings[theme_subtype]['css_files']
			if ("js_files" in theme_settings[theme_subtype]): js_files += theme_settings[theme_subtype]['js_files']
		#

		css_files = self._get_unique_filelist(css_files)
		if (len(css_files) > 0): self.content['css_files'] = css_files

		js_files = self._get_unique_filelist(js_files)
		if (len(js_files) > 0): self.content['js_files'] = js_files

		return self._parser(theme_data)
	#

	def set(self, theme):
	#
		"""
Sets the theme to use.

:param theme: Output theme
:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Renderer.set({0})- (#echo(__LINE__)#)".format(theme))

		theme = theme.replace(".", "/")
		file_pathname = path.normpath("{0}/{1}/site.tsc".format(self.path, theme))

		"""
Retry with default theme
		"""

		if (os.access(file_pathname, os.R_OK)): self.theme = theme
		else:
		#
			self.theme = Settings.get("pas_http_theme_default", "simple").replace(".", "/")
			file_pathname = path.normpath("{0}/{1}/site.tsc".format(self.path, self.theme))
		#

		"""
Read corresponding theme configuration
		"""

		file_pathname = file_pathname[:-3] + "json"
		Settings.read_file(file_pathname)
	#

	def set_log_handler(self, log_handler):
	#
		"""
Sets the LogHandler.

:param log_handler: LogHandler to use

:since: v0.1.00
		"""

		self.log_handler = log_handler
	#

	def set_subtype(self, subtype):
	#
		"""
Sets the theme to use.

:param theme: Output theme
:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Renderer.set_subtype({0})- (#echo(__LINE__)#)".format(subtype))
		self.subtype = subtype
	#

	def set_title(self, title):
	#
		"""
Sets the theme to use.

:param theme: Output theme
:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Renderer.set_title({0})- (#echo(__LINE__)#)".format(title))
		self.title = title
	#
#

##j## EOF