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

from cgi import FieldStorage
from collections import Mapping

from dNG.pas.runtime.value_exception import ValueException
from .request_body import RequestBody

class RequestBodyMultipart(Mapping, RequestBody):
#
	"""
"RequestBodyMultipart" parses an incoming request body as
"multipart/form-data".

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(RequestBodyMultipart)

:since: v0.1.00
		"""

		RequestBody.__init__(self)

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
:since:  v0.1.00
		"""

		if (self.parsed_data == None): self.parse()
		return self.parsed_data[key].value
	#

	def __iter__(self):
	#
		"""
python.org: Return an iterator object.

:return: (object) Iterator object
:since:  v0.1.00
		"""

		if (self.parsed_data == None): self.parse()
		return iter(self.parsed_data)
	#

	def __len__(self):
	#
		"""
python.org: Called to implement the built-in function len().

:return: (int) Length of the object
:since:  v0.1.00
		"""

		if (self.parsed_data == None): self.parse()
		return len(self.parsed_data)
	#

	def parse(self):
	#
		"""
Sets a given pointer for the streamed post instance.

:since: v0.1.00
		"""

		if (self.headers == None): raise ValueException("Request body can't be read without HTTP headers")

		byte_buffer = RequestBody.get(self)
		if (byte_buffer != None): self.parsed_data = FieldStorage(byte_buffer, self.headers, environ = { }, keep_blank_values = True)
	#
#

##j## EOF