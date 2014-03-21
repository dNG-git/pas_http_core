# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.http.RequestBodyUrlencoded
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

# pylint: disable=import-error,no-name-in-module

import re

try: from urllib.parse import parse_qsl
except ImportError: from urlparse import parse_qsl

from dNG.pas.data.binary import Binary
from dNG.pas.runtime.value_exception import ValueException
from .request_body import RequestBody

class RequestBodyUrlencoded(RequestBody):
#
	"""
"RequestBodyUrlencoded" parses an incoming request body as
"application/x-www-form-urlencoded".

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	# pylint: disable=arguments-differ

	RE_ARRAY = re.compile("^(.+)\\[(\\S*)\\]$")

	def __init__(self, parse_in_thread = False):
	#
		"""
Constructor __init__(RequestBodyUrlencoded)

:since: v0.1.00
		"""

		RequestBody.__init__(self, parse_in_thread)

		self.parsed_data = None
		"""
Parsed data
		"""
	#

	def __getattr__(self, name):
	#
		"""
python.org: Called when an attribute lookup has not found the attribute in
the usual places (i.e. it is not an instance attribute nor is it found in the
class tree for self).

:param name: Attribute name

:return: (mixed) Instance attribute
:since:  v0.1.00
		"""

		return self.get(name)
	#

	def get(self, name, timeout = None):
	#
		"""
python.org: Called when an attribute lookup has not found the attribute in
the usual places (i.e. it is not an instance attribute nor is it found in the
class tree for self).

:param name: Attribute name

:return: (mixed) Form content
:since:  v0.1.00
		"""

		self.parse(timeout)

		if (name not in self.parsed_data): raise ValueException("Given key not found in data received")
		return self.parsed_data[name]
	#

	def get_dict(self, timeout = None):
	#
		"""
python.org: Called when an attribute lookup has not found the attribute in
the usual places (i.e. it is not an instance attribute nor is it found in the
class tree for self).

:param timeout: Timeout for reading input

:return: (dict) Data read
:since:  v0.1.00
		"""

		self.parse(timeout)
		return self.parsed_data
	#

	def parse(self, timeout = None):
	#
		"""
Sets a given pointer for the streamed post instance.

:since: v0.1.00
		"""

		post_data = RequestBody.get(self, timeout)

		field_arrays = { }
		parsed_data = parse_qsl(Binary.str(post_data.read()), True, True)
		self.parsed_data = { }

		for parsed_field in parsed_data:
		#
			re_result = RequestBodyUrlencoded.RE_ARRAY.search(parsed_field[0])

			if (re_result == None):
			#
				if (parsed_field[0] not in self.parsed_data): self.parsed_data[parsed_field[0]] = parsed_field[1]
				elif (type(self.parsed_data[parsed_field[0]]) == list): self.parsed_data[parsed_field[0]].append(parsed_field[1])
				else: self.parsed_data[parsed_field[0]] = [ self.parsed_data[parsed_field[0]], parsed_field[1] ]
			#
			elif (re_result.group(1) in field_arrays): field_arrays[re_result.group(1)].append({ "key": re_result.group(2), "value": parsed_field[1] })
			else: field_arrays[re_result.group(1)] = [ { "key": re_result.group(2), "value": parsed_field[1] } ]
		#

		for field in field_arrays:
		#
			element_position = 0
			if (field in self.parsed_data): field_arrays[field].append(self.parsed_data[field])
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