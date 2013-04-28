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

import re

from dNG.pas.data.settings import direct_settings
from dNG.pas.data.tag_parser.abstract_impl import direct_abstract_impl
from dNG.pas.data.text.l10n import direct_l10n
from dNG.pas.data.text.tag_parser.block_mixin import direct_block_mixin
from dNG.pas.data.text.tag_parser.each_mixin import direct_each_mixin
from dNG.pas.data.text.tag_parser.if_condition_mixin import direct_if_condition_mixin
from dNG.pas.data.text.tag_parser.mapped_element_mixin import direct_mapped_element_mixin
from dNG.pas.data.text.tag_parser.rewrite_mixin import direct_rewrite_mixin
from dNG.pas.module.named_loader import direct_named_loader

class direct_parser(direct_abstract_impl, direct_block_mixin, direct_each_mixin, direct_if_condition_mixin, direct_mapped_element_mixin, direct_rewrite_mixin):
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
Constructor __init__(direct_parser)

:since: v0.1.00
		"""

		direct_abstract_impl.__init__(self)
		direct_mapped_element_mixin.__init__(self)

		self.content = None
		"""
Content cache for OSet template replacements
		"""
		self.log_handler = direct_named_loader.get_singleton("dNG.pas.data.logging.log_handler", False)
		"""
The log_handler is called whenever debug messages should be logged or errors
happened.
		"""
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
			re_result = re.match("^\[block(:(\w+):(\w+):(\w+)){0,1}\]", data[tag_position:data_position])

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
			re_result = re.match("^\[each:(\w+):(\w+):(\w+)\]", data[tag_position:data_position])

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
			re_result = re.match("^\[if:(\w+):(\w+)(\s*)(\!=|==)(.*)\]", data[tag_position:data_position])

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
					re_result = re_result = re.match("^\[block(:\w+:\w+:\w+){0,1}\]", data)
					if (re_result != None): var_return = { "tag": "block", "tag_end": "[/block]", "type": "top_down" }
				#
				elif (data_match == "each"):
				#
					re_result = re.match("^\[each:(\w+):(\w+):(\w+)\]", data)
					if (re_result != None): var_return = { "tag": "each", "tag_end": "[/each]", "type": "top_down" }
				#
				elif (data_match == "if"):
				#
					re_result = re.match("^\[if:(\w+):(\w+)(\s*)(\!=|==)(.*)\]", data)
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

	def render(self, template_data, content):
	#
		"""
Renders content ready for output from the given OSet template.

:param template_data: OSet template data
:param content: Content object

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -osetParser.render(template_data, content)- (#echo(__LINE__)#)")

		self.content = content
		return self.parser(template_data)
	#
#

##j## EOF