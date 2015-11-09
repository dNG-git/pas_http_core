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

from .abstract_form_tags import AbstractFormTags
from .content_link_renderer import ContentLinkRenderer

class FormTagsRenderer(AbstractFormTags):
#
	"""
The OSet parser takes a template string to render the output.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	# pylint: disable=unused-argument

	def __init__(self):
	#
		"""
Constructor __init__(AbstractFormTags)

:since: v0.1.01
		"""

		AbstractFormTags.__init__(self)

		self.null_byte_markup = False
		"""
NULL-bytes are used to mark special markup. They should be removed after
processing is completed.
		"""
	#

	def _change_plain_content(self, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to only contain the plain content.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
		"""

		return data[data_position:tag_end_position]
	#

	_change_match_b = _change_plain_content
	"""
Change data according to the "b" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
	"""

	def _change_match_box(self, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the "box" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
		"""

		_return = data[data_position:tag_end_position]
		if (len(_return) > 0): _return = "---\n{0}\n---".format(_return)

		return _return
	#

	_change_match_center = _change_plain_content
	"""
Change data according to the "center" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
	"""

	def _change_match_code(self, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the "code" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
		"""

		_return = data[data_position:tag_end_position]

		if (len(_return) > 0 and "[" in _return):
		#
			self.null_byte_markup = True

			_return = _return.replace("[", "\x00#91;")
			_return = _return.replace("]", "\x00#93;")
			_return = _return = "---\n{0}\n---".format(_return)
		#

		return _return
	#

	_change_match_color = _change_plain_content
	"""
Change data according to the "color" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
	"""

	_change_match_del = _change_plain_content
	"""
Change data according to the "del" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
	"""

	def _change_match_highlight(self, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the "highlight" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
		"""

		_return = data[data_position:tag_end_position]

		if (len(_return) > 0):
		#
			tag_params = FormTagsRenderer.parse_tag_parameters("highlight", data, tag_position, data_position)
			if ("width" in tag_params): _return = "---\n{0}\n---".format(_return)
		#

		return _return
	#

	_change_match_i = _change_plain_content
	"""
Change data according to the "i" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
	"""

	def _change_match_img(self, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the "img" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
		"""

		_return = ""

		tag_params = FormTagsRenderer.parse_tag_parameters("img", data, tag_position, data_position)
		url = data[data_position:tag_end_position]

		if (len(url) > 0 and "title" in tag_params):
		#
			img_text = ("- {0} ({1}) -" if ("align" in tag_params) else "{0} ({1})")
			_return = img_text.format(tag_params['title'], url)
		#

		return _return
	#

	justify = _change_plain_content
	"""
Change data according to the "justify" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
	"""

	_change_match_left = _change_plain_content
	"""
Change data according to the "left" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
	"""

	def _change_match_link(self, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the "link" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
		"""

		_return = data[data_position:tag_end_position]

		if (len(_return) > 0):
		#
			renderer = ContentLinkRenderer()
			if (self.datalinker_main_id is not None): renderer.set_datalinker_main_id(self.datalinker_main_id)
			tag_params = FormTagsRenderer.parse_tag_parameters("link", data, tag_position, data_position)

			_return = renderer.render(_return, tag_params)
		#

		return _return
	#

	_change_match_margin = _change_plain_content
	"""
Change data according to the "margin" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
	"""

	_change_match_right = _change_plain_content
	"""
Change data according to the "right" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
	"""

	_change_match_s = _change_plain_content
	"""
Change data according to the "s" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
	"""

	_change_match_size = _change_plain_content
	"""
Change data according to the "size" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
	"""

	def _change_match_title(self, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the "title" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
		"""

		return "\n===\n{0}\n===\n".format(data[data_position:tag_end_position])
	#

	_change_match_u = _change_plain_content
	"""
Change data according to the "u" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
	"""

	def _change_match_url(self, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the "url" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
		"""

		_return = ""

		re_result = re.match("^\\[url=(\\w+:.*)?\\]", data[tag_position:data_position])
		enclosed_data = ""
		url = None

		if (re_result is not None and len(re_result.group(1)) > 0):
		#
			enclosed_data = data[data_position:tag_end_position]
			url = re_result.group(1)
		#
		else: url = data[data_position:tag_end_position]

		if (url is not None): _return = ("{0} ({1})".format(enclosed_data, url) if (len(enclosed_data) > 0) else url)

		return _return
	#

	def render(self, content):
	#
		"""
Renders the given FormTags content.

:param content: FormTags content

:return: (str) Rendered content
:since:  v0.1.01
		"""

		_return = self._parse(content)

		if (self.null_byte_markup):
		#
			_return = _return.replace("\x00#91;", "[")
			_return = _return.replace("\x00#93;", "]")
		#

		return _return
	#
#

##j## EOF