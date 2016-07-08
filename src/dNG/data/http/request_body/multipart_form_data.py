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

from dNG.data.binary import Binary
from dNG.data.rfc.header import Header
from dNG.runtime.io_exception import IOException

from .multipart import Multipart
from .uploaded_file import UploadedFile

class MultipartFormData(Multipart):
#
	"""
"Multipart" parses an incoming request body as "multipart/form-data".
Multi-dimensional arrays are not supported.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	RE_ARRAY = re.compile("^(.+)\\[(\\S*)\\]$")
	"""
RegEx for keys with array indices
	"""
	TYPE_ID = "multipart_form_data"
	"""
Body type ID
	"""

	def __init__(self):
	#
		"""
Constructor __init__(MultipartFormData)

:since: v0.2.00
		"""

		Multipart.__init__(self)

		self.parsed_data = None
		"""
Parsed data
		"""
		self.parsed_parts = None
		"""
Parsed data
		"""
	#

	def __getitem__(self, key):
	#
		"""
python.org: Called to implement evaluation of self[key].

:param key: Value key

:return: (mixed) Value
:since:  v0.2.00
		"""

		if (self.parsed_data is None): self.parse()
		return self.parsed_data[key]
	#

	def __iter__(self):
	#
		"""
python.org: Return an iterator object.

:return: (object) Iterator object
:since:  v0.2.00
		"""

		if (self.parsed_data is None): self.parse()
		return iter(self.parsed_data)
	#

	def __len__(self):
	#
		"""
python.org: Called to implement the built-in function len().

:return: (int) Length of the object
:since:  v0.2.00
		"""

		if (self.parsed_data is None): self.parse()
		return len(self.parsed_data)
	#

	def _init_read(self):
	#
		"""
Initializes internal variables for reading from input.

:since: v0.2.00
		"""

		Multipart._init_read(self)

		self.parsed_data = { }
	#

	def parse(self):
	#
		"""
Parses the content of the request body.

:since: v0.2.00
		"""

		Multipart.parse(self)

		self.parsed_parts = { }

		for key in self.parts:
		#
			part = self.parts[key]

			if ("list" in part):
			#
				for part_list_entry in part['list']: self._parse_part_entry(part_list_entry)
			#
			else: self._parse_part_entry(part)
		#

		self.parts = None

		field_arrays = { }

		for key in self.parsed_parts:
		#
			re_result = MultipartFormData.RE_ARRAY.match(key)
			parsed_part_value = self.parsed_parts[key]

			if (re_result is None): self.parsed_data[key] = parsed_part_value
			elif (re_result.group(1) in field_arrays): field_arrays[re_result.group(1)].append({ "key": re_result.group(2), "value": parsed_part_value })
			else: field_arrays[re_result.group(1)] = [ { "key": re_result.group(2), "value": parsed_part_value } ]
		#

		self.parsed_parts = None

		for field in field_arrays:
		#
			element_position = 0
			if (field in self.parsed_data): field_arrays[field].insert(0, self.parsed_data[field])
			self.parsed_data[field] = { }

			for element in field_arrays[field]:
			#
				if (len(element['key']) > 0): self.parsed_data[field][element['key']] = element['value']
				else:
				#
					self.parsed_data[field][element_position] = element['value']
					element_position += 1
				#
			#
		#
	#

	def _parse_part_entry(self, part):
	#
		"""
Parses a part entry.

:since: v0.2.00
		"""

		form_entry_name = None
		file_name = None

		if ("CONTENT-DISPOSITION" in part['headers']):
		#
			for content_disposition_option in Header.get_field_list_dict(part['headers']['CONTENT-DISPOSITION'], ";", "="):
			#
				if (type(content_disposition_option) is dict):
				#
					content_disposition_option_key = content_disposition_option['key'].lower()

					if (content_disposition_option_key == "filename"): file_name = content_disposition_option['value']
					if (content_disposition_option_key == "name"): form_entry_name = content_disposition_option['value']
				#
			#
		#

		if (form_entry_name is None): raise IOException("Invalid MIME part detected for 'multipart/form-data'")
		is_content_type_defined = ("CONTENT-TYPE" in part['headers'])
		part_data = None

		if (is_content_type_defined or file_name is not None):
		#
			if (file_name is None): file_name = ""

			if (file_name != "" or part['data'].get_size() > 0):
			#
				part_data = UploadedFile()

				if (is_content_type_defined): part_data.set_client_content_type(part['headers']['CONTENT-TYPE'])
				part_data.set_client_file_name(file_name)
				part_data.set_file(part['data'])
			#
		#
		else: part_data = Binary.str(part['data'].read())

		if (form_entry_name in self.parsed_parts):
		#
			if (type(self.parsed_parts[form_entry_name]) is list): self.parsed_parts[form_entry_name].append(part_data)
			else: self.parsed_parts[form_entry_name] = [ self.parsed_parts[form_entry_name], part_data ]
		#
		else: self.parsed_parts[form_entry_name] = part_data
	#
#

##j## EOF