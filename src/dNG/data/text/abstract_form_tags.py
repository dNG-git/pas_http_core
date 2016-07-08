# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;http;core

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasHttpCoreVersion)#
#echo(__FILEPATH__)#
"""

import re

from dNG.module.named_loader import NamedLoader

from .tag_parser.abstract import Abstract as AbstractTagParser

class AbstractFormTags(AbstractTagParser):
#
	"""
Abstract parser to handle FormTags.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	# pylint: disable=unused-argument

	RE_NUMBER = re.compile("^\\d+$")
	"""

	"""
	TAGS = [ "b", "i", "s", "u", "color", "del", "face", "size",
	         "box", "center", "justify", "left", "right",
	         "link", "title", "url",
	         "code", "highlight", "margin", "quote",
	         "hr", "img", "list"
	       ]
	"""
Known tags used for en- and decoding.
	"""

	def __init__(self):
	#
		"""
Constructor __init__(AbstractFormTags)

:since: v0.2.00
		"""

		AbstractTagParser.__init__(self)

		self.log_handler = NamedLoader.get_singleton("dNG.data.logging.LogHandler", False)
		"""
The LogHandler is called whenever debug messages should be logged or errors
happened.
		"""
	#

	def _change_match(self, tag_definition, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the matched tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.2.00
		"""

		_return = data[:tag_position]

		method = (getattr(self, "_change_match_{0}".format(tag_definition['tag'])) if (hasattr(self, "_change_match_{0}".format(tag_definition['tag']))) else None)

		if (method is not None): _return += method(data, tag_position, data_position, tag_end_position)
		if ("type" not in tag_definition or tag_definition['type'] != "simple"): _return += data[self._find_tag_end_position(data, tag_end_position):]

		return _return
	#

	def _check_match(self, data):
	#
		"""
Check if a possible tag match is a false positive.

:param data: Data starting with the possible tag

:return: (dict) Matched tag definition; None if false positive
:since:  v0.2.00
		"""

		_return = None

		i = 0
		tags_length = len(self.__class__.TAGS)

		while (_return is None and i < tags_length):
		#
			tag = self.__class__.TAGS[i]
			data_match = data[1:1 + len(tag)]

			if (data_match == tag):
			#
				method = (getattr(self, "_check_match_{0}".format(tag)) if (hasattr(self, "_check_match_{0}".format(tag))) else None)
				if (method is not None and method(data)): _return = getattr(self, "_get_match_definition_{0}".format(tag))()
			#

			i += 1
		#

		return _return
	#

	def _check_match_b(self, data):
	#
		"""
Check if a possible tag match is a valid "b" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		return self._check_match_simple_tag("b", data)
	#

	def _check_match_box(self, data):
	#
		"""
Check if a possible tag match is a valid "box" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		_return = False

		tag_element_end_position = self._find_tag_end_position(data, 4)

		if (tag_element_end_position > 5):
		#
			tag_params = AbstractFormTags.parse_tag_parameters("box", data, 0, tag_element_end_position)

			_return = (data[:5] == "[box:")
			if (_return and "align" in tag_params): _return = (tag_params['align'].lower() in ( "left", "center", "right" ))
			if (_return and "clear" in tag_params): _return = (tag_params['clear'].lower() in ( "both", "left", "right" ))
			if (_return and "width" in tag_params): _return = (AbstractFormTags.check_size_percent(tag_params['width']) or AbstractFormTags.check_size_px(tag_params['width'], 50))
		#
		else: _return = (data[:5] == "[box]")

		return _return
	#

	def _check_match_center(self, data):
	#
		"""
Check if a possible tag match is a valid "center" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		_return = False

		tag_element_end_position = self._find_tag_end_position(data, 7)

		if (tag_element_end_position > 8):
		#
			tag_params = AbstractFormTags.parse_tag_parameters("center", data, 0, tag_element_end_position)
			if (data[:8] == "[center:" and "box" in tag_params): _return = (AbstractFormTags.check_size_percent(tag_params['box']) or AbstractFormTags.check_size_px(tag_params['box'], 50))
		#
		else: _return = (data[:8] == "[center]")

		return _return
	#

	def _check_match_code(self, data):
	#
		"""
Check if a possible tag match is a valid "code" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		return self._check_match_simple_tag("code", data)
	#

	def _check_match_color(self, data):
	#
		"""
Check if a possible tag match is a valid "color" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		return (re.match("^\\[color=#[0-9a-f]{6}\\]", data) is not None)
	#

	def _check_match_del(self, data):
	#
		"""
Check if a possible tag match is a valid "del" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		return self._check_match_simple_tag("del", data)
	#

	def _check_match_face(self, data):
	#
		"""
Check if a possible tag match is a valid "face" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		return False # TODO: Implement me
	#

	def _check_match_highlight(self, data):
	#
		"""
Check if a possible tag match is a valid "highlight" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		_return = False

		tag_element_end_position = self._find_tag_end_position(data, 10)

		if (tag_element_end_position > 11):
		#
			tag_params = AbstractFormTags.parse_tag_parameters("highlight", data, 0, tag_element_end_position)
			if (data[:11] == "[highlight:" and "width" in tag_params): _return = (AbstractFormTags.check_size_percent(tag_params['width']) or AbstractFormTags.check_size_px(tag_params['width'], 50))
		#
		else: _return = (data[:11] == "[highlight]")

		return _return
	#

	def _check_match_hr(self, data):
	#
		"""
Check if a possible tag match is a valid "hr" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		return self._check_match_simple_tag("hr", data)
	#

	def _check_match_i(self, data):
	#
		"""
Check if a possible tag match is a valid "i" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		return self._check_match_simple_tag("i", data)
	#

	def _check_match_img(self, data):
	#
		"""
Check if a possible tag match is a valid "img" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		_return = False

		tag_element_end_position = self._find_tag_end_position(data, 4)

		if (tag_element_end_position > 5):
		#
			tag_params = AbstractFormTags.parse_tag_parameters("img", data, 0, tag_element_end_position)

			_return = (data[:5] == "[img:")
			if (_return and "width" in tag_params): _return = (AbstractFormTags.check_size_percent(tag_params['width']) or AbstractFormTags.check_size_px(tag_params['width']))
			if (_return and "height" in tag_params): _return = (AbstractFormTags.check_size_percent(tag_params['height']) or AbstractFormTags.check_size_px(tag_params['height']))
		#
		else: _return = (data[:5] == "[img]")

		return _return
	#

	def _check_match_justify(self, data):
	#
		"""
Check if a possible tag match is a valid "justify" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		return self._check_match_simple_tag("justify", data)
	#

	def _check_match_left(self, data):
	#
		"""
Check if a possible tag match is a valid "left" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		return self._check_match_simple_tag("left", data)
	#

	def _check_match_link(self, data):
	#
		"""
Check if a possible tag match is a valid "link" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		_return = False

		tag_element_end_position = self._find_tag_end_position(data, 5)

		if (tag_element_end_position > 6):
		#
			tag_params = AbstractFormTags.parse_tag_parameters("link", data, 0, tag_element_end_position)

			if (data[:6] == "[link:"):
			#
				if ("id" in tag_params): _return = (len(tag_params['id'].strip()) > 0)
				elif (tag_params.get("link") == "params"): _return = (len(tag_params) > 1)
				elif ("tag" in tag_params): _return = (len(tag_params['tag'].strip()) > 0)
			#
		#

		return _return
	#

	def _check_match_list(self, data):
	#
		"""
Check if a possible tag match is a valid "list" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		_return = False

		tag_element_end_position = self._find_tag_end_position(data, 5)

		if (tag_element_end_position > 6):
		#
			tag_params = AbstractFormTags.parse_tag_parameters("list", data, 0, tag_element_end_position)
			_return = (data[:6] == "[list:" and "type" in tag_params)
		#
		else: _return = (data[:6] == "[list]")

		return _return
	#

	def _check_match_margin(self, data):
	#
		"""
Check if a possible tag match is a valid "margin" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		_return = False

		re_result = re.match("^\\[margin=(.+?)\\]", data)

		if (re_result is not None):
		#
			value = re_result.group(1)
			_return = (AbstractFormTags.check_size_percent(value, _max = 49) or AbstractFormTags.check_size_px(value, 1))
		#

		return _return
	#

	def _check_match_quote(self, data):
	#
		"""
Check if a possible tag match is a valid "quote" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		return self._check_match_simple_tag("quote", data)
	#

	def _check_match_right(self, data):
	#
		"""
Check if a possible tag match is a valid "right" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		return self._check_match_simple_tag("right", data)
	#

	def _check_match_s(self, data):
	#
		"""
Check if a possible tag match is a valid "s" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		return self._check_match_simple_tag("s", data)
	#

	def _check_match_simple_tag(self, tag, data):
	#
		"""
Check if a possible tag matches the given expected, simple tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		return (data[:len(tag) + 2] == "[{0}]".format(tag))
	#

	def _check_match_size(self, data):
	#
		"""
Check if a possible tag match is a valid "size" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		_return = False

		re_result = re.match("^\\[size=(.+?)\\]", data)

		if (re_result is not None):
		#
			value = re_result.group(1)
			_return = (AbstractFormTags.check_size_percent(value, 60, 500) or AbstractFormTags.check_size_px(value, _max = 80))
		#

		return _return
	#

	def _check_match_title(self, data):
	#
		"""
Check if a possible tag match is a valid "title" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		_return = False

		tag_element_end_position = self._find_tag_end_position(data, 6)

		if (tag_element_end_position > 7):
		#
			tag_params = AbstractFormTags.parse_tag_parameters("title", data, 0, tag_element_end_position)

			_return = (data[:7] in ( "[title:", "[title=" ))
			if (_return and "clear" in tag_params): _return = (tag_params['clear'] in ( "both", "left", "right" ))
		#
		else: _return = (data[:7] == "[title]")

		return _return
	#

	def _check_match_u(self, data):
	#
		"""
Check if a possible tag match is a valid "i" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		return self._check_match_simple_tag("u", data)
	#

	def _check_match_url(self, data):
	#
		"""
Check if a possible tag match is a valid "url" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		return (re.match("^(\\[url=\\w+:.*\\]|\\[url\\]\\w+:.*)", data) is not None)
	#

	def _get_match_definition_b(self):
	#
		"""
Returns the "b" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "b", "tag_end": "[/b]" }
	#

	def _get_match_definition_box(self):
	#
		"""
Returns the "box" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "box", "tag_end": "[/box]" }
	#

	def _get_match_definition_center(self):
	#
		"""
Returns the "center" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "center", "tag_end": "[/center]" }
	#

	def _get_match_definition_code(self):
	#
		"""
Returns the "code" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "code", "tag_end": "[/code]", "type": "top_down" }
	#

	def _get_match_definition_color(self):
	#
		"""
Returns the "color" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "color", "tag_end": "[/color]" }
	#

	def _get_match_definition_del(self):
	#
		"""
Returns the "del" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "del", "tag_end": "[/del]" }
	#

	def _get_match_definition_face(self):
	#
		"""
Returns the "face" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "face", "tag_end": "[/face]" }
	#

	def _get_match_definition_highlight(self):
	#
		"""
Returns the "highlight" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "highlight", "tag_end": "[/highlight]" }
	#

	def _get_match_definition_hr(self):
	#
		"""
Returns the "hr" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "hr", "type": "simple" }
	#

	def _get_match_definition_i(self):
	#
		"""
Returns the "i" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "i", "tag_end": "[/i]" }
	#

	def _get_match_definition_img(self):
	#
		"""
Returns the "img" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "img", "tag_end": "[/img]" }
	#

	def _get_match_definition_justify(self):
	#
		"""
Returns the "justify" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "justify", "tag_end": "[/justify]" }
	#

	def _get_match_definition_left(self):
	#
		"""
Returns the "left" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "left", "tag_end": "[/left]" }
	#

	def _get_match_definition_link(self):
	#
		"""
Returns the "link" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "link", "tag_end": "[/link]" }
	#

	def _get_match_definition_list(self):
	#
		"""
Returns the "list" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "list", "tag_end": "[/list]" }
	#

	def _get_match_definition_quote(self):
	#
		"""
Returns the "quote" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "quote", "tag_end": "[/quote]" }
	#

	def _get_match_definition_margin(self):
	#
		"""
Returns the "quote" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "margin", "tag_end": "[/margin]" }
	#

	def _get_match_definition_right(self):
	#
		"""
Returns the "right" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "right", "tag_end": "[/right]" }
	#

	def _get_match_definition_s(self):
	#
		"""
Returns the "s" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "s", "tag_end": "[/s]" }
	#

	def _get_match_definition_size(self):
	#
		"""
Returns the "size" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "size", "tag_end": "[/size]" }
	#

	def _get_match_definition_title(self):
	#
		"""
Returns the "title" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "title", "tag_end": "[/title]" }
	#

	def _get_match_definition_u(self):
	#
		"""
Returns the "u" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
		"""

		return { "tag": "u", "tag_end": "[/u]" }
	#

	def _get_match_definition_url(self):
	#
		"""
Returns the "url" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.2.00
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
:since:  v0.2.00
		"""

		_type = type(value)

		_return = (_type in ( int, float ))
		if (_return and _min is not None and value < _min): _return = False
		if (_return and _max is not None and value > _max): _return = False

		return _return
	#

	@staticmethod
	def check_size_percent(value, _min = 1, _max = 100):
	#
		"""
Check if a possible tag match is a valid "center" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.2.00
		"""

		_return = False

		if (value[-1:] == "%"):
		#
			if (AbstractFormTags.RE_NUMBER.match(value[:-1]) is not None): _return = AbstractFormTags._check_number(int(value[:-1]), _min, _max)
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
:since:  v0.2.00
		"""

		_return = False

		if (value[-2:] == "px"):
		#
			if (AbstractFormTags.RE_NUMBER.match(value[:-2]) is not None): _return = AbstractFormTags._check_number(int(value[:-2]), _min, _max)
		#

		return _return
	#
#

##j## EOF