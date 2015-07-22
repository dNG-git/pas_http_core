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

from dNG.pas.data.text.abstract_form_tags import AbstractFormTags
from dNG.pas.data.xhtml.content_link_renderer import ContentLinkRenderer
from dNG.pas.data.xhtml.formatting import Formatting

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

	TAGS = AbstractFormTags.TAGS + [ "nobr" ]
	"""
Known tags used for en- and decoding.
	"""

	def __init__(self):
	#
		"""
Constructor __init__(FormTagsRenderer)

:since: v0.1.01
		"""

		AbstractFormTags.__init__(self)

		self.datalinker_main_id = None
		"""
DataLinker main ID for tags
		"""
		self.is_block_encoding_supported = True
		"""
True if block level elements are allowed.
		"""
		self.is_xhtml_allowed = False
		"""
True if (X)HTML content is allowed.
		"""
		self.xhtml_title_top_level = 1
		"""
First level available for [title].
		"""
	#

	def _change_match_b(self, data, tag_position, data_position, tag_end_position):
	#
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

		enclosed_data = data[data_position:tag_end_position]
		return ("<b>{0}</b>".format(enclosed_data) if (len(enclosed_data) > 0) else "")
	#

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

		if (self.is_block_encoding_supported and len(_return) > 0):
		#
			tag_params = FormTagsRenderer.parse_tag_parameters("box", data, tag_position, data_position)

			css_styles = [ ]
			if ("align" in tag_params): css_styles.append("float: {0}".format(tag_params['align']))
			if ("clear" in tag_params): css_styles.append("clear: {0}".format(tag_params['clear']))
			if ("width" in tag_params): css_styles.append("width: {0}".format(tag_params['width']))

			css_style = (' style="{0}"'.format("; ".join(css_styles)) if (len(css_styles) > 0) else "")

			_return = '<div class="pagecontent_box"{0}>{1}</div>[nobr]'.format(css_style, _return)
		#

		return _return
	#

	def _change_match_center(self, data, tag_position, data_position, tag_end_position):
	#
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

		_return = data[data_position:tag_end_position]

		if (self.is_block_encoding_supported and len(_return) > 0):
		#
			tag_params = FormTagsRenderer.parse_tag_parameters("center", data, tag_position, data_position)

			if ("box" in tag_params): _return = "<div style='text-align: center'><div class='pagecontent_box' style='display: inline-block; width: {0}'>{1}</div></div>[nobr]".format(tag_params['box'], _return)
			else: _return = "<div class='pagecontent_box' style='text-align: center'>{0}</div>[nobr]".format(_return)
		#

		return _return
	#

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

		if (len(_return) > 0):
		#
			_return = _return.replace("[", "&#91;")
			_return = _return.replace("]", "&#93;")
			_return = "<code class='pagecontent_box'>{0}</code>".format(_return)
		#

		return _return
	#

	def _change_match_color(self, data, tag_position, data_position, tag_end_position):
	#
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

		_return = data[data_position:tag_end_position]

		if (len(_return) > 0):
		#
			color = Formatting.escape(data[(7 + tag_position):(data_position - 1)])
			_return = '<span style="color: {0}">{1}</span>'.format(color, _return)

		return _return
	#

	def _change_match_del(self, data, tag_position, data_position, tag_end_position):
	#
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

		enclosed_data = data[data_position:tag_end_position]
		return ("<del>{0}</del>".format(enclosed_data) if (len(enclosed_data) > 0) else "")
	#

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

		if (self.is_block_encoding_supported and len(_return) > 0):
		#
			tag_params = FormTagsRenderer.parse_tag_parameters("highlight", data, tag_position, data_position)
			css_style = (' style="width: {0}"'.format(tag_params['box']) if ("box" in tag_params) else "")

			_return = "<div class='pagecontent_box pagecontent_highlight_box'{0}>{1}</div>[nobr]".format(css_style, _return)
		#

		return _return
	#

	def _change_match_i(self, data, tag_position, data_position, tag_end_position):
	#
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

		enclosed_data = data[data_position:tag_end_position]
		return ("<i>{0}</i>".format(enclosed_data) if (len(enclosed_data) > 0) else "")
	#

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

		url = data[data_position:tag_end_position]

		if (len(url) > 0):
		#
			url = Formatting.escape(url)

			tag_params = FormTagsRenderer.parse_tag_parameters("img", data, tag_position, data_position)

			element_code = ""
			title = (Formatting.escape(tag_params['title']) if ("title" in tag_params) else url)

			if ("align" in tag_params):
			#
				if (tag_params['align'] == "left"): element_code = " class='pagecontent_box pagecontent_box_left' style='clear: left; float: left'"
				elif (tag_params['align'] == "right"): element_code = " class='pagecontent_box pagecontent_box_right' style='clear: right; float: right'"
			#

			_return = '<img src="{0}" title="{1}"{2} />'.format(Formatting.escape(url), title, element_code)
		#

		return _return
	#

	def _change_match_justify(self, data, tag_position, data_position, tag_end_position):
	#
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

		_return = data[data_position:tag_end_position]

		if (self.is_block_encoding_supported and len(_return) > 0):
		#
			tag_params = FormTagsRenderer.parse_tag_parameters("justify", data, tag_position, data_position)
			css_style = ("float: left; width: {0}; ".format(tag_params['box']) if ("box" in tag_params) else "")

			_return = '<div class="pagecontent_box" style="{0}text-align: justify">{1}</div>[nobr]'.format(css_style, _return)
		#

		return _return
	#

	def _change_match_left(self, data, tag_position, data_position, tag_end_position):
	#
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

		_return = data[data_position:tag_end_position]

		if (self.is_block_encoding_supported and len(_return) > 0):
		#
			tag_params = FormTagsRenderer.parse_tag_parameters("left", data, tag_position, data_position)

			element_code = ""

			if ("box" in tag_params): element_code = "class='pagecontent_box pagecontent_box_left' style='clear: left; float: left; width: {0}'".format(tag_params['box'])
			else: element_code = "style='text-align: left'"

			_return = '<div {0}>{1}</div>[nobr]'.format(element_code, _return)
		#

		return _return
	#

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

	def _change_match_list(self, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the "list" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
		"""

		_return = ""

		list_content = data[data_position:tag_end_position]

		if (self.is_block_encoding_supported and len(list_content) > 0):
		#
			list_items = list_content.split("[*]")

			_return = "<ul>"

			for item in list_items:
			#
				item = item.strip()
				if (len(item) > 0): _return += "<li>{0}</li>".format(item)
			#

			_return += "</ul>[nobr]"
		#

		return _return
	#

	def _change_match_margin(self, data, tag_position, data_position, tag_end_position):
	#
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

		_return = data[data_position:tag_end_position]

		if (self.is_block_encoding_supported and len(_return) > 0):
		#
			re_result = re.match("^\\[margin=(.+?)\\]", data[tag_position:data_position])
			if (re_result is not None): _return = '<div style="padding: {0}">{1}</div>[nobr]'.format(re_result.group(1), _return)
		#

		return _return
	#

	def _change_match_nobr(self, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the "nobr" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
		"""

		return (data[7 + tag_position:] if (data[6 + tag_position:7 + tag_position] == "\n") else data[6 + tag_position:])
	#

	def _change_match_quote(self, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the "quote" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
		"""

		_return = data[data_position:tag_end_position]

		if (self.is_block_encoding_supported and len(_return) > 0): _return = "<blockquote class='pagecontent_box pagecontent_quote_box'>{0}</blockquote>[nobr]".format(_return)

		return _return
	#

	def _change_match_right(self, data, tag_position, data_position, tag_end_position):
	#
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

		_return = data[data_position:tag_end_position]

		if (self.is_block_encoding_supported and len(_return) > 0):
		#
			tag_params = FormTagsRenderer.parse_tag_parameters("right", data, tag_position, data_position)

			element_code = ""

			if ("box" in tag_params): element_code = "class='pagecontent_box pagecontent_box_right' style='clear: right; float: right; width: {0}'".format(tag_params['box'])
			else: element_code = "style='text-align: right'"

			_return = '<div {0}>{1}</div>[nobr]'.format(element_code, _return)
		#

		return _return
	#

	def _change_match_s(self, data, tag_position, data_position, tag_end_position):
	#
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

		enclosed_data = data[data_position:tag_end_position]
		return ("<span style='text-decoration: line-through'>{0}</span>".format(enclosed_data) if (len(enclosed_data) > 0) else "")
	#

	def _change_match_size(self, data, tag_position, data_position, tag_end_position):
	#
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

		_return = data[data_position:tag_end_position]

		if (len(_return) > 0):
		#
			re_result = re.match("^\\[size=(.+?)\\]", data[tag_position:data_position])
			if (re_result is not None): _return = '<span style="font-size: {0}">{1}</span>'.format(re_result.group(1), _return)
		#

		return _return
	#

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

		_return = data[data_position:tag_end_position]

		if (len(_return) > 0):
		#
			tag_params = FormTagsRenderer.parse_tag_parameters("title", data, tag_position, data_position)

			element_code = ""
			subtitle_level = self.xhtml_title_top_level

			if ("title" in tag_params):
			#
				try:
				#
					sublevel = int(tag_params['title'])
					if (sublevel > 0): subtitle_level += (sublevel - 1)
				#
				except ValueError: pass
			#

			if (subtitle_level > 6): subtitle_level = 6

			if ("clear" in tag_params):
			#
				if (tag_params['clear'] == "both"): element_code = " style='clear: both'"
				elif (tag_params['clear'] == "left"): element_code = " style='clear: left'"
				elif (tag_params['clear'] == "right"): element_code = " style='clear: right'"
			#

			_return = "<h{0:d}{1}>{2}</h{0:d}>[nobr]".format(subtitle_level, element_code, _return)
		#

		return _return
	#

	def _change_match_u(self, data, tag_position, data_position, tag_end_position):
	#
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

		enclosed_data = data[data_position:tag_end_position]
		return ("<u>{0}</u>".format(enclosed_data) if (len(enclosed_data) > 0) else "")
	#

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

		re_result = re.match("^\\[url=(\\w+:.*|)\\]", data[tag_position:data_position])
		enclosed_data = ""
		url = None

		if (re_result is not None and len(re_result.group(1)) > 0):
		#
			enclosed_data = data[data_position:tag_end_position]
			url = re_result.group(1)
		#
		else: url = data[data_position:tag_end_position]

		_return = enclosed_data

		if (url is not None):
		#
			if (len(_return) < 1): _return = Formatting.escape(url)
			_return = '<a href="{0}" rel="nofollow">{1}</a>'.format(Formatting.escape(url), _return)
		#

		return _return
	#

	def _check_match_nobr(self, data):
	#
		"""
Check if a possible tag match is a valid "nobr" tag.

:param data: Data starting with the possible tag

:return: (bool) True if valid
:since:  v0.1.01
		"""

		return self._check_match_simple_tag("nobr", data)
	#

	def _get_match_definition_nobr(self):
	#
		"""
Returns the "nobr" tag definition for the parser.

:return: (dict) Tag definition
:since:  v0.1.01
		"""

		return { "tag": "nobr", "type": "simple" }
	#

	def render(self, content):
	#
		"""
Renders the given FormTags content.

:param content: FormTags content

:return: (str) Rendered content
:since:  v0.1.01
		"""

		if (not self.is_xhtml_allowed): content = Formatting.escape(content)
		content = self._parse(content).strip()
		content = content.replace("[", "&#91;")
		content = content.replace("]", "&#93;")
		content = content.replace("\n", "<br />\n")

		return content
	#

	def set_blocks_supported(self, supported):
	#
		"""
Sets if block level elements are allowed.

:param supported: True if block level elements are allowed

:since: v0.1.01
		"""

		self.is_block_encoding_supported = supported
	#

	def set_datalinker_main_id(self, id_main):
	#
		"""
Sets the DataLinker main ID for tags.

:param id_main: DataLinker main ID

:since: v0.1.01
		"""

		self.datalinker_main_id = id_main
	#

	def set_xhtml_allowed(self, allowed):
	#
		"""
Sets if (X)HTML encoding is allowed.

:param allowed: True if (X)HTML encoding is allowed

:since: v0.1.01
		"""

		self.is_xhtml_allowed = allowed
	#

	def set_xhtml_title_top_level(self, level):
	#
		"""
Sets the first level available for [title].

:param level: First level available

:since: v0.1.01
		"""

		self.xhtml_title_top_level = level
	#
#

##j## EOF