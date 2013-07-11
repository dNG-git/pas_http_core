# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.oset.Parser
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

from dNG.pas.data.settings import Settings
from dNG.pas.data.tag_parser.abstract import Abstract as AbstractTagParser
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.text.tag_parser.block_mixin import BlockMixin
from dNG.pas.data.text.tag_parser.each_mixin import EachMixin
from dNG.pas.data.text.tag_parser.if_condition_mixin import IfConditionMixin
from dNG.pas.data.text.tag_parser.mapped_element_mixin import MappedElementMixin
from dNG.pas.data.text.tag_parser.rewrite_mixin import RewriteMixin
from dNG.pas.module.named_loader import NamedLoader

class Parser(AbstractTagParser, BlockMixin, EachMixin, IfConditionMixin, MappedElementMixin, RewriteMixin):
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
Constructor __init__(Parser)

:since: v0.1.00
		"""

		AbstractTagParser.__init__(self)
		MappedElementMixin.__init__(self)

		self.content = None
		"""
Content cache for OSet template replacements
		"""
		self.log_handler = NamedLoader.get_singleton("dNG.pas.data.logging.LogHandler", False)
		"""
The log_handler is called whenever debug messages should be logged or errors
happened.
		"""
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
			re_result = re.match("^\\[if:(\\w+):([\\w\\.]+)(\\s*)(\\!=|==)(.*)\\]", data[tag_position:data_position])

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

			if (data_match == tag):
			#
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
					re_result = re.match("^\\[if:\\w+:[\\w\\.]+\\s*(\\!=|==).*\\]", data)
					if (re_result != None): _return = { "tag": "if", "tag_end": "[/if]", "type": "top_down" }
				#
				elif (data_match == "rewrite"):
				#
					re_result = re.match("^\\[rewrite:(\\w+)\\]", data)
					if (re_result != None and re_result.group(1) in [ "content", "l10n", "settings" ]): _return = { "tag": "rewrite", "tag_end": "[/rewrite]" }
				#
			#

			i += 1
		#

		return _return
	#

	def render(self, template_data, content):
	#
		"""
Renders content ready for output from the given OSet template.

:param template_data: OSet template data
:param content: Content object

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Parser.render(template_data, content)- (#echo(__LINE__)#)")

		self.content = content
		return self._parser(template_data)
	#
#

##j## EOF