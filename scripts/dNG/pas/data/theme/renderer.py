# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.oset.parser
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
import os, re

from dNG.data.file import direct_file
from dNG.pas.data.settings import direct_settings
from dNG.pas.data.tag_parser.abstract_impl import direct_abstract_impl
from dNG.pas.data.text.l10n import direct_l10n
from dNG.pas.data.text.tag_parser.block_mixin import direct_block_mixin
from dNG.pas.data.text.tag_parser.each_mixin import direct_each_mixin
from dNG.pas.data.text.tag_parser.if_condition_mixin import direct_if_condition_mixin
from dNG.pas.data.text.tag_parser.mapped_element_mixin import direct_mapped_element_mixin
from dNG.pas.data.text.tag_parser.rewrite_mixin import direct_rewrite_mixin
from dNG.pas.module.named_loader import direct_named_loader

class direct_renderer(direct_abstract_impl, direct_block_mixin, direct_each_mixin, direct_if_condition_mixin, direct_mapped_element_mixin, direct_rewrite_mixin):
#
	"""
The OSet parser takes a template string to render the output.

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
Constructor __init__(direct_renderer)

:since: v0.1.00
		"""

		direct_abstract_impl.__init__(self)
		direct_mapped_element_mixin.__init__(self)

		self.cache_instance = direct_named_loader.get_singleton("dNG.pas.data.cache", False)
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
		self.log_handler = direct_named_loader.get_singleton("dNG.pas.data.logging.log_handler", False)
		"""
The log_handler is called whenever debug messages should be logged or errors
happened.
		"""
		self.path = direct_settings.get("path_themes", "{0}/themes".format(direct_settings.get("path_data")))
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

	def __del__(self):
	#
		"""
Destructor __del__(direct_renderer)

:since: v0.1.00
		"""

		if (self.cache_instance != None): self.cache_instance.return_instance()
		if (direct_abstract_impl != None): direct_abstract_impl.__del__(self)
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

	def get_unique_filelist(self, raw_list):
	#
		"""
Sets the theme to use.

:param theme: Output theme

:access: protected
:return: (list) List with unique file entries
:since: v0.1.00
		"""

		var_return = [ ]
		names_list = [ ]

		if (len(raw_list) > 0):
		#
			for entry in raw_list:
			#
				if (entry['name'] not in names_list):
				#
					names_list.append(entry['name'])
					var_return.append(entry)
				#
			#
		#

		return var_return
	#

	def is_supported(self, theme, subtype = None):
	#
		"""
Sets the theme to use.

:param theme: Output theme
:param subtype: Output theme subtype

:since: v0.1.00
		"""

		var_return = False

		if (theme != None):
		#
			file_pathname = path.normpath("{0}/{1}/{2}.tsc".format(self.path, theme.replace(".", "/"), ("site" if (subtype == None) else subtype)))
			var_return = os.access(file_pathname, os.R_OK)
		#

		return var_return
	#

	def parser_change(self, tag_definition, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the matched tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:access: protected
:return: (str) Converted data
:since:  v0.1.00
		"""

		var_return = data[:tag_position]

		data_closed = data[self.parser_tag_find_end_position(data, tag_end_position):]

		if (tag_definition['tag'] == "block"):
		#
			re_result = re.match("^\[block(:(\w+):([\w\.]+):([\w\.]+)){0,1}\]", data[tag_position:data_position])

			if (re_result != None):
			#
				if (re_result.group(1) != None):
				#
					source = re_result.group(2)
					key = re_result.group(3)
					mapping_key = re_result.group(4)
				#
				else: source = None

				if (source == None): var_return += self.render_block(data[data_position:tag_end_position])
				elif (source == "content"): var_return += self.render_block(data[data_position:tag_end_position], "content", self.mapped_element_update("content", self.content), key, mapping_key)
				elif (source == "settings"): var_return += self.render_block(data[data_position:tag_end_position], "settings", self.mapped_element_update("settings", direct_settings.get_instance()), key, mapping_key)
			#

			var_return += data_closed
		#
		elif (tag_definition['tag'] == "each"):
		#
			re_result = re.match("^\[each:(\w+):([\w\.]+):([\w\.]+)\]", data[tag_position:data_position])

			source = (None if (re_result == None) else re_result.group(1))

			if (source != None):
			#
				key = re_result.group(2)
				mapping_key = re_result.group(3)

				if (source == "content"): var_return += self.render_each(data[data_position:tag_end_position], "content", self.mapped_element_update("content", self.content), key, mapping_key)
				elif (source == "settings"): var_return += self.render_each(data[data_position:tag_end_position], "settings", self.mapped_element_update("settings", direct_settings.get_instance()), key, mapping_key)
			#

			var_return += data_closed
		#
		elif (tag_definition['tag'] == "if"):
		#
			re_result = re.match("^\[if:(\w+):([\w\.]+)(\s*)(\!=|==)(.*)\]", data[tag_position:data_position])

			source = (None if (re_result == None) else re_result.group(1))

			if (source != None):
			#
				key = re_result.group(2)
				operator = re_result.group(4)
				value = re_result.group(5).strip()

				if (source == "content"): var_return += self.render_if_condition(self.mapped_element_update("content", self.content), key, operator, value, data[data_position:tag_end_position])
				elif (source == "settings"): var_return += self.render_if_condition(self.mapped_element_update("settings", direct_settings.get_instance()), key, operator, value, data[data_position:tag_end_position])
			#

			var_return += data_closed
		#
		elif (tag_definition['tag'] == "rewrite"):
		#
			source = re.match("^\[rewrite:(\w+)\]", data[tag_position:data_position]).group(1)
			key = data[data_position:tag_end_position]

			if (source == "content"): var_return += self.render_rewrite(self.mapped_element_update("content", self.content), key)
			elif (source == "l10n"): var_return += self.render_rewrite(self.mapped_element_update("l10n", direct_l10n.get_instance()), key)
			elif (source == "settings"): var_return += self.render_rewrite(self.mapped_element_update("settings", direct_settings.get_instance()), key)

			var_return += data_closed
		#
		else: var_return += data_closed

		return var_return
	#

	def parser_check(self, data):
	#
		"""
Check if a possible tag match is a false positive.

:param data: Data starting with the possible tag

:access: protected
:return: (dict) Matched tag definition; None if false positive
:since:  v0.1.00
		"""

		var_return = None

		i = 0
		tags = [ "block", "each", "if", "rewrite" ]
		tags_length = len(tags)

		while (var_return == None and i < tags_length):
		#
			tag = tags[i]
			data_match = data[1:1 + len(tag)]

			if (data_match == tag):
			#
				if (data_match == "block"):
				#
					re_result = re_result = re.match("^\[block(:\w+:[\w\.]+:[\w\.]+){0,1}\]", data)
					if (re_result != None): var_return = { "tag": "block", "tag_end": "[/block]", "type": "top_down" }
				#
				elif (data_match == "each"):
				#
					re_result = re.match("^\[each:\w+:[\w\.]+:[\w\.]+\]", data)
					if (re_result != None): var_return = { "tag": "each", "tag_end": "[/each]", "type": "top_down" }
				#
				elif (data_match == "if"):
				#
					re_result = re.match("^\[if:\w+:[\w\.]+\s*(\!=|==).*\]", data)
					if (re_result != None): var_return = { "tag": "if", "tag_end": "[/if]", "type": "top_down" }
				#
				elif (data_match == "rewrite"):
				#
					re_result = re.match("^\[rewrite:(\w+)\]", data)
					if (re_result != None and re_result.group(1) in [ "content", "l10n", "settings" ]): var_return = { "tag": "rewrite", "tag_end": "[/rewrite]" }
				#
			#

			i += 1
		#

		return var_return
	#

	def render(self, content):
	#
		"""
Renders content ready for output from the given OSet template.

:param content: Content data

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -themeRenderer.render(template_data, content)- (#echo(__LINE__)#)")

		theme = self.theme.replace(".", "/")
		theme_subtype = self.theme_subtype

		file_pathname = path.normpath("{0}/{1}/{2}.tsc".format(self.path, theme, theme_subtype))

		if (theme_subtype != "site" and (not os.access(file_pathname, os.R_OK))):
		#
			file_pathname = path.normpath("{0}/{1}/site.tsc".format(self.path, theme))
			theme_subtype = "site"
		#

		"""
Retry with default theme
		"""

		if (not os.access(file_pathname, os.R_OK)):
		#
			theme = direct_settings.get("pas_http_theme_default").replace(".", "/")
			theme_subtype = self.theme_subtype

			file_pathname = path.normpath("{0}/{1}/{2}.tsc".format(self.path, theme, theme_subtype))

			if (theme_subtype != "site" and (not os.access(file_pathname, os.R_OK))):
			#
				file_pathname = path.normpath("{0}/{1}/site.tsc".format(self.path, theme))
				theme_subtype = "site"
			#
		#

		theme_data = (None if (self.cache_instance == None) else self.cache_instance.get_file(file_pathname))

		if (theme_data == None):
		#
			file_obj = direct_file()

			if (file_obj.open(file_pathname, True, "r")): theme_data = file_obj.read()
			else: raise RuntimeError("Failed to open theme file for '{0}'".format(self.theme), 77)

			file_obj.close()

			if (theme_data == False): raise RuntimeError("Failed to read theme file for '{0}'".format(self.theme), 5)
			elif (self.cache_instance != None): self.cache_instance.set_file(file_pathname, theme_data)
		#

		"""
Read corresponding theme configuration
		"""

		file_pathname = file_pathname[:-3] + "json"
		direct_settings.read_file(file_pathname)

		if (self.title == None): self.title = direct_settings.get("pas_html_title", "Unconfigured site")

		self.content = {
			"page_title": self.title,
			"page_content": content
		}

		theme_settings = direct_settings.get("pas_http_theme_{0}".format(theme))

		css_files = (self.css_files.copy() if (hasattr(self.css_files, "copy")) else copy(self.css_files))
		js_files = (self.js_files.copy() if (hasattr(self.js_files, "copy")) else copy(self.js_files))

		if (theme_settings != None and theme_subtype in theme_settings):
		#
			if ("css_files" in theme_settings[theme_subtype]): css_files += theme_settings[theme_subtype]['css_files']
			if ("js_files" in theme_settings[theme_subtype]): js_files += theme_settings[theme_subtype]['js_files']
		#

		css_files = self.get_unique_filelist(css_files)
		if (len(css_files) > 0): self.content['css_files'] = css_files

		js_files = self.get_unique_filelist(js_files)
		if (len(js_files) > 0): self.content['js_files'] = js_files

		return self.parser(theme_data)
	#

	def set(self, theme):
	#
		"""
Sets the theme to use.

:param theme: Output theme
:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -themeRenderer.set({0})- (#echo(__LINE__)#)".format(theme))
		self.theme = theme
	#

	def set_log_handler(self, log_handler):
	#
		"""
Sets the log_handler.

:param log_handler: log_handler to use

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

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -themeRenderer.set_subtype({0})- (#echo(__LINE__)#)".format(subtype))
		self.subtype = subtype
	#

	def set_title(self, title):
	#
		"""
Sets the theme to use.

:param theme: Output theme
:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -themeRenderer.set_title({0})- (#echo(__LINE__)#)".format(title))
		self.title = title
	#
#

##j## EOF