# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.xhtml.FormTagsEncoder
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

from .abstract_form_tags import AbstractFormTags

class FormTagsEncoder(AbstractFormTags):
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

	def _match_change_center(self, data, tag_position, data_position, tag_end_position):
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

		_return = ""

		re_object = re.match("^\\[center\\:box=(\\d+)\\]", data[tag_position:data_position])

		if (re_object != None):
		#
			enclosed_data = data[data_position:tag_end_position]
			value = int(re_object.group(1))

			_return = ("[center:box={0:d}%]{1}[/center]".format(value, enclosed_data) if (value > 0 and value <= 100) else enclosed_data)
		#

		return _return
	#

	def _match_change_hr(self, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the "hr" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
		"""

		_return = ""

		re_object = re.match("^\\[hr=(\\d+)\\]", data[tag_position:data_position])

		if (re_object != None):
		#
			value = int(re_object.group(1))
			if (value > 0 and value <= 100): _return = "[hr={0:d}%]".format(value)
		#

		return _return
	#

	def _match_change_justify(self, data, tag_position, data_position, tag_end_position):
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

		_return = ""

		re_object = re.match("^\\[justify\\:box=(\\d+)\\]", data[tag_position:data_position])

		if (re_object != None):
		#
			enclosed_data = data[data_position:tag_end_position]
			value = int(re_object.group(1))

			_return = ("[justify:box={0:d}%]{1}[/justify]".format(value, enclosed_data) if (value > 0 and value <= 100) else enclosed_data)
		#

		return _return
	#

	def _match_change_left(self, data, tag_position, data_position, tag_end_position):
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

		_return = ""

		re_object = re.match("^\\[left\\:box=(\\d+)\\]", data[tag_position:data_position])

		if (re_object != None):
		#
			enclosed_data = data[data_position:tag_end_position]
			value = int(re_object.group(1))

			_return = ("[left:box={0:d}%]{1}[/left]".format(value, enclosed_data) if (value > 0 and value <= 100) else enclosed_data)
		#

		return _return
	#

	def _match_change_margin(self, data, tag_position, data_position, tag_end_position):
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

		_return = ""

		re_object = re.match("^\\[margin=(\\d+)\\]", data[tag_position:data_position])

		if (re_object != None):
		#
			enclosed_data = data[data_position:tag_end_position]
			value = int(re_object.group(1))

			_return = ("[margin={0:d}%]{1}[/margin]".format(value, enclosed_data) if (value > 0 and value <= 100) else enclosed_data)
		#

		return _return
	#

	def _match_change_right(self, data, tag_position, data_position, tag_end_position):
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

		_return = ""

		re_object = re.match("^\\[right\\:box=(\\d+)\\]", data[tag_position:data_position])

		if (re_object != None):
		#
			enclosed_data = data[data_position:tag_end_position]
			value = int(re_object.group(1))

			_return = ("[right:box={0:d}%]{1}[/right]".format(value, enclosed_data) if (value > 0 and value <= 100) else enclosed_data)
		#

		return _return
	#

	def _match_change_size(self, data, tag_position, data_position, tag_end_position):
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

		_return = ""

		re_object = re.match("^\\[size=(\\d+)\\]", data[tag_position:data_position])

		if (re_object != None):
		#
			enclosed_data = data[data_position:tag_end_position]
			value = int(re_object.group(1))

			_return = ("[size={0:d}%]{1}[/size]".format(value, enclosed_data) if (value > 0 and value <= 100) else enclosed_data)
		#

		return _return
	#

	def _match_check_b(self, data):
	#
		"""
Check if a possible tag match is a valid "b" tag that needs to be changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		return False
	#

	def _match_check_center(self, data):
	#
		"""
Check if a possible tag match is a valid "center" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		return (re.match("^\\[center\\:box=(\\d+)\\]", data) != None)
	#

	def _match_check_color(self, data):
	#
		"""
Check if a possible tag match is a valid "color" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		return False
	#

	def _match_check_code(self, data):
	#
		"""
Check if a possible tag match is a valid "code" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		return False
	#

	def _match_check_del(self, data):
	#
		"""
Check if a possible tag match is a valid "del" tag that needs to be changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		return False
	#

	def _match_check_face(self, data):
	#
		"""
Check if a possible tag match is a valid "face" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		return False
	#

	def _match_check_hr(self, data):
	#
		"""
Check if a possible tag match is a valid "hr" tag that needs to be changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		return (re.match("^\\[hr=(\\d+)\\]", data) != None)
	#

	def _match_check_i(self, data):
	#
		"""
Check if a possible tag match is a valid "i" tag that needs to be changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		return False
	#

	def _match_check_img(self, data):
	#
		"""
Check if a possible tag match is a valid "img" tag that needs to be changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		return False
	#

	def _match_check_justify(self, data):
	#
		"""
Check if a possible tag match is a valid "justify" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		return (re.match("^\\[justify\\:box=(\\d+)\\]", data) != None)
	#

	def _match_check_left(self, data):
	#
		"""
Check if a possible tag match is a valid "left" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		return (re.match("^\\[left\\:box=(\\d+)\\]", data) != None)
	#

	def _match_check_link(self, data):
	#
		"""
Check if a possible tag match is a valid "link" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		return False
	#

	def _match_check_margin(self, data):
	#
		"""
Check if a possible tag match is a valid "margin" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		return (re.match("^\\[margin=(\\d+)\\]", data) != None)
	#

	def _match_check_quote(self, data):
	#
		"""
Check if a possible tag match is a valid "quote" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		return False
	#

	def _match_check_right(self, data):
	#
		"""
Check if a possible tag match is a valid "right" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		return (re.match("^\\[right\\:box=(\\d+)\\]", data) != None)
	#

	def _match_check_s(self, data):
	#
		"""
Check if a possible tag match is a valid "s" tag that needs to be changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		return False
	#

	def _match_check_size(self, data):
	#
		"""
Check if a possible tag match is a valid "size" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		return (re.match("^\\[size=(\\d+)\\]", data) != None)
	#

	def _match_check_title(self, data):
	#
		"""
Check if a possible tag match is a valid "title" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		return False
	#

	def _match_check_u(self, data):
	#
		"""
Check if a possible tag match is a valid "u" tag that needs to be changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		return False
	#

	def _match_check_url(self, data):
	#
		"""
Check if a possible tag match is a valid "url" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		return False
	#

	def process(self, content):
	#
		"""
Constructor __init__(FormTagsEncoder)

:since: v0.1.01
		"""

		return self._parse(content)
	#
#

##j## EOF