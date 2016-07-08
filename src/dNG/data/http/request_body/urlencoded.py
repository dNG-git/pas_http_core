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

# pylint: disable=import-error,no-name-in-module

from collections import Mapping
import re

try: from urllib.parse import parse_qsl
except ImportError: from urlparse import parse_qsl

from dNG.data.binary import Binary

from .data import Data

class Urlencoded(Mapping, Data):
#
	"""
"Urlencoded" parses an incoming request body as
"application/x-www-form-urlencoded". Multi-dimensional arrays are not
supported.

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
	TYPE_ID = "urlencoded_form"
	"""
Body type ID
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Urlencoded)

:since: v0.2.00
		"""

		Data.__init__(self)

		self.parsed_data = None
		"""
Parsed data
		"""

		self.supported_features['body_parser'] = True
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

		Data._init_read(self)

		self.parsed_data = { }
	#

	def parse(self):
	#
		"""
Parses the content of the request body.

:since: v0.2.00
		"""

		byte_buffer = Data.get(self)

		field_arrays = { }

		parsed_fields = ([ ]
		                 if (byte_buffer is None or byte_buffer.get_size() < 1) else
		                 parse_qsl(Binary.str(byte_buffer.read()), True, True)
		                )

		for parsed_field in parsed_fields:
		#
			re_result = Urlencoded.RE_ARRAY.match(parsed_field[0])

			if (re_result is None): self.parsed_data[parsed_field[0]] = parsed_field[1]
			elif (re_result.group(1) in field_arrays): field_arrays[re_result.group(1)].append({ "key": re_result.group(2), "value": parsed_field[1] })
			else: field_arrays[re_result.group(1)] = [ { "key": re_result.group(2), "value": parsed_field[1] } ]
		#

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
#

##j## EOF