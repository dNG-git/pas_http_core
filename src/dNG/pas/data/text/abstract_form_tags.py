# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.AbstractFormTags
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

from dNG.pas.data.text.tag_parser.abstract import Abstract as AbstractTagParser
from dNG.pas.module.named_loader import NamedLoader

class AbstractFormTags(AbstractTagParser):
#
	"""
The OSet parser takes a template string to render the output.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	RE_NUMBER = re.compile("^\d+$")
	"""

	"""
	TAGS = [
		"b", "i", "s", "u", "color", "del", "face", "size",
		"center", "justify", "left", "right",
		"code", "link", "margin", "quote", "title", "url",
		"hr", "img"
	]
	"""
Known tags used for en- and decoding.
	"""

	def __init__(self):
	#
		"""
Constructor __init__(AbstractFormTags)

:since: v0.1.01
		"""

		AbstractTagParser.__init__(self)

		self.log_handler = NamedLoader.get_singleton("dNG.pas.data.logging.LogHandler", False)
		"""
The LogHandler is called whenever debug messages should be logged or errors
happened.
		"""
	#

	def _match_change(self, tag_definition, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the matched tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
		"""

		_return = data[:tag_position]

		method = (getattr(self, "_match_change_{0}".format(tag_definition['tag'])) if (hasattr(self, "_match_change_{0}".format(tag_definition['tag']))) else None)

		if (method != None): _return += method(data, tag_position, data_position, tag_end_position)
		if ("type" not in tag_definition or tag_definition['type'] != "simple"): _return += data[self._find_tag_end_position(data, tag_end_position):]

		return _return
	#

	def _match_check(self, data):
	#
		"""
Check if a possible tag match is a false positive.

:param data: Data starting with the possible tag

:return: (dict) Matched tag definition; None if false positive
:since:  v0.1.01
		"""

		_return = None

		i = 0
		tags_length = len(self.__class__.TAGS)

		while (_return == None and i < tags_length):
		#
			tag = self.__class__.TAGS[i]
			data_match = data[1:1 + len(tag)]

			if (data_match == tag):
			#
				method = (getattr(self, "_match_check_{0}".format(tag)) if (hasattr(self, "_match_check_{0}".format(tag))) else None)
				if (method != None and method(data)): _return = getattr(self, "_match_get_definition_{0}".format(tag))()
			#

			i += 1
		#

		return _return
	#

	def _match_check_b(self, data):
	#
		"""
Check if a possible tag match is a valid "b" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		return self._match_check_simple_tag("b", data)
	#

	def _match_check_center(self, data):
	#
		"""
Check if a possible tag match is a valid "center" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		_return = False

		tag_element_end_position = self._find_tag_end_position(data, 7)

		if (tag_element_end_position > 8):
		#
			tag_params = AbstractFormTags.parse_tag_parameters("center", data, 0, tag_element_end_position)
			if (data.find("[center:") == 0 and "box" in tag_params): _return = (AbstractFormTags.check_size_percent(tag_params['box']) or AbstractFormTags.check_size_px(tag_params['box'], 50))
		#
		else: _return = (data.find("[center]") == 0)

		return _return
	#

	def _match_check_code(self, data):
	#
		"""
Check if a possible tag match is a valid "code" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		return self._match_check_simple_tag("code", data)
	#

	def _match_check_color(self, data):
	#
		"""
Check if a possible tag match is a valid "color" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		return (re.match("^\\[color=#[0-9a-f]{6}\\]", data) != None)
	#

	def _match_check_del(self, data):
	#
		"""
Check if a possible tag match is a valid "del" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		return self._match_check_simple_tag("del", data)
	#

	def _match_check_face(self, data):
	#
		"""
Check if a possible tag match is a valid "b" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		return False # TODO: Implement me
	#

	def _match_check_hr(self, data):
	#
		"""
Check if a possible tag match is a valid "hr" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		return self._match_check_simple_tag("hr", data)
	#

	def _match_check_i(self, data):
	#
		"""
Check if a possible tag match is a valid "i" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		return self._match_check_simple_tag("i", data)
	#

	def _match_check_img(self, data):
	#
		"""
Check if a possible tag match is a valid "img" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		return False # TODO: Implement me
	#

	def _match_check_justify(self, data):
	#
		"""
Check if a possible tag match is a valid "justify" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		_return = False

		tag_element_end_position = self._find_tag_end_position(data, 8)

		if (tag_element_end_position > 9):
		#
			tag_params = AbstractFormTags.parse_tag_parameters("justify", data, 0, tag_element_end_position)
			if (data.find("[justify:") == 0 and "box" in tag_params): _return = (AbstractFormTags.check_size_percent(tag_params['box']) or AbstractFormTags.check_size_px(tag_params['box'], 50))
		#
		else: _return = (data.find("[justify]") == 0)

		return _return
	#

	def _match_check_left(self, data):
	#
		"""
Check if a possible tag match is a valid "left" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		_return = False

		tag_element_end_position = self._find_tag_end_position(data, 5)

		if (tag_element_end_position > 6):
		#
			tag_params = AbstractFormTags.parse_tag_parameters("left", data, 0, tag_element_end_position)
			if (data.find("[left:") == 0 and "box" in tag_params): _return = (AbstractFormTags.check_size_percent(tag_params['box']) or AbstractFormTags.check_size_px(tag_params['box'], 50))
		#
		else: _return = (data.find("[left]") == 0)

		return _return
	#

	def _match_check_link(self, data):
	#
		"""
Check if a possible tag match is a valid "link" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		_return = False

		tag_element_end_position = self._find_tag_end_position(data, 5)

		if (tag_element_end_position > 6):
		#
			tag_params = AbstractFormTags.parse_tag_parameters("link", data, 0, tag_element_end_position)

			if (data.find("[link:") == 0):
			#
				if ("type" not in tag_params or tag_params['type'] == "id"): _return = ("id" in tag_params and len(tag_params['id'].strip()) > 0)
				elif (tag_params['type'] == "tag"): _return = ("tag" in tag_params and len(tag_params['tag'].strip()) > 0)
			#
		#

		return _return
	#

	def _match_check_margin(self, data):
	#
		"""
Check if a possible tag match is a valid "margin" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		_return = False

		re_result = re.match("^\\[margin=(.+?)\\]", data)

		if (re_result != None):
		#
			value = re_result.group(1)
			_return = (AbstractFormTags.check_size_percent(value, _max = 49) or AbstractFormTags.check_size_px(value, 1))
		#

		return _return
	#

	def _match_check_quote(self, data):
	#
		"""
Check if a possible tag match is a valid "quote" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		return self._match_check_simple_tag("quote", data)
	#

	def _match_check_right(self, data):
	#
		"""
Check if a possible tag match is a valid "right" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		_return = False

		tag_element_end_position = self._find_tag_end_position(data, 6)

		if (tag_element_end_position > 7):
		#
			tag_params = AbstractFormTags.parse_tag_parameters("right", data, 0, tag_element_end_position)
			if (data.find("[right:") == 0 and "box" in tag_params): _return = (AbstractFormTags.check_size_percent(tag_params['box']) or AbstractFormTags.check_size_px(tag_params['box'], 50))
		#
		else: _return = (data.find("[right]") == 0)

		return _return
	#

	def _match_check_s(self, data):
	#
		"""
Check if a possible tag match is a valid "s" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		return self._match_check_simple_tag("s", data)
	#

	def _match_check_simple_tag(self, tag, data):
	#
		"""
Check if a possible tag matches the given expected, simple tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		return (data.find("[{0}]".format(tag)) == 0)
	#

	def _match_check_size(self, data):
	#
		"""
Check if a possible tag match is a valid "size" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		_return = False

		re_result = re.match("^\\[size=(.+?)\\]", data)

		if (re_result != None):
		#
			value = re_result.group(1)
			_return = (AbstractFormTags.check_size_percent(value, 60, 500) or AbstractFormTags.check_size_px(value, _max = 80))
		#

		return _return
	#

	def _match_check_title(self, data):
	#
		"""
Check if a possible tag match is a valid "title" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		return (re.match("^\\[title(=\\d|)\\]", data) != None)
	#

	def _match_check_u(self, data):
	#
		"""
Check if a possible tag match is a valid "i" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		return self._match_check_simple_tag("u", data)
	#

	def _match_check_url(self, data):
	#
		"""
Check if a possible tag match is a valid "url" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		return (re.match("^(\\[url=\\w+://.*\\]|\\[url\\]\\w+://.*)", data) != None)
	#

	def _match_get_definition_b(self):
	#
		"""
Returns the "b" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "b", "tag_end": "[/b]" }
	#

	def _match_get_definition_center(self):
	#
		"""
Returns the "center" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "center", "tag_end": "[/center]" }
	#

	def _match_get_definition_code(self):
	#
		"""
Returns the "code" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "code", "tag_end": "[/code]", "type": "top_down" }
	#

	def _match_get_definition_color(self):
	#
		"""
Returns the "color" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "color", "tag_end": "[/color]" }
	#

	def _match_get_definition_del(self):
	#
		"""
Returns the "del" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "del", "tag_end": "[/del]" }
	#

	def _match_get_definition_face(self):
	#
		"""
Returns the "face" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "face", "tag_end": "[/face]" }
	#

	def _match_get_definition_hr(self):
	#
		"""
Returns the "hr" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "hr", "type": "simple" }
	#

	def _match_get_definition_i(self):
	#
		"""
Returns the "i" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "i", "tag_end": "[/i]" }
	#

	def _match_get_definition_img(self):
	#
		"""
Returns the "img" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "img", "tag_end": "[/img]" }
	#

	def _match_get_definition_justify(self):
	#
		"""
Returns the "justify" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "justify", "tag_end": "[/justify]" }
	#

	def _match_get_definition_left(self):
	#
		"""
Returns the "left" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "left", "tag_end": "[/left]" }
	#

	def _match_get_definition_link(self):
	#
		"""
Returns the "link" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "link", "tag_end": "[/link]" }
	#

	def _match_get_definition_quote(self):
	#
		"""
Returns the "quote" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "quote", "tag_end": "[/quote]" }
	#

	def _match_get_definition_margin(self):
	#
		"""
Returns the "quote" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "margin", "tag_end": "[/margin]" }
	#

	def _match_get_definition_right(self):
	#
		"""
Returns the "right" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "right", "tag_end": "[/right]" }
	#

	def _match_get_definition_s(self):
	#
		"""
Returns the "s" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "s", "tag_end": "[/s]" }
	#

	def _match_get_definition_size(self):
	#
		"""
Returns the "size" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "size", "tag_end": "[/size]" }
	#

	def _match_get_definition_title(self):
	#
		"""
Returns the "title" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "title", "tag_end": "[/title]" }
	#

	def _match_get_definition_u(self):
	#
		"""
Returns the "u" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "u", "tag_end": "[/u]" }
	#

	def _match_get_definition_url(self):
	#
		"""
Returns the "url" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "url", "tag_end": "[/url]" }
	#

	@staticmethod
	def _check_number(value, _min = None, _max = None):
	#
		"""
Check if a possible tag match is a valid "center" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		_type = type(value)

		_return = (_type == int or _type == float)
		if (_return and _min != None and value < _min): _return = False
		if (_return and _max != None and value > _max): _return = False

		return _return
	#

	@staticmethod
	def check_size_percent(value, _min = 1, _max = 100):
	#
		"""
Check if a possible tag match is a valid "center" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		_return = False

		if (value[-1:] == "%"):
		#
			if (AbstractFormTags.RE_NUMBER.match(value[:-1]) != None): _return = AbstractFormTags._check_number(int(value[:-1]), _min, _max)
		#

		return _return
	#

	@staticmethod
	def check_size_px(value, _min = 8, _max = None):
	#
		"""
Check if a possible tag match is a valid "center" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		_return = False

		if (value[-2:] == "px"):
		#
			if (AbstractFormTags.RE_NUMBER.match(value[:-2]) != None): _return = AbstractFormTags._check_number(int(value[:-2]), _min, _max)
		#

		return _return
	#

	@staticmethod
	def parse_tag_parameters(tag_key, data, tag_position, data_position):
	#
		"""
Check if a possible tag matches the given expected, simple tag.

:param tag_key: Tag key
:param data: Data starting with the possible tag
:param tag_position: Tag starting position
:param data_position: Data starting position

:return: (bool) True if valid
:since:  v0.1.01
		"""

		_return = { }

		data_splitted = data[1 + len(tag_key) + tag_position:data_position - 1].split(":", 1)

		data = (data_splitted[0] if (len(data_splitted[0]) > 0 or len(data_splitted) > 1) else None)
		re_escaped = re.compile("(\\\\+)$")
		value = ""

		while (data != None):
		#
			if (len(data) > 0):
			#
				re_result = re_escaped.search(data)
				value += data

				if (re_result == None or (len(re_result.group(1)) % 2) != 1):
				#
					value_splitted = value.split("=", 1)

					if (len(value_splitted) > 1):
					#
						key = value_splitted[0]
						value = value_splitted[1]
					#
					else: key = tag_key

					if (key not in _return): _return[key] = value
					value = ""
				#
			#

			if (len(data_splitted) > 1):
			#
				data_splitted = data_splitted[1].split(":", 1)
				data = data_splitted[0]
			#
			else: data = None
		#

		return _return
	#
#

##j## EOF