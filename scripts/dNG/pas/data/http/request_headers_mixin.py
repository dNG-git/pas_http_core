# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.http.RequestHeadersMixin
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

from dNG.data.rfc.http import Http

class RequestHeadersMixin(object):
#
	"""
This request mixin provides header specific methods.

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
Constructor __init__(RequestHeadersMixin)

:since: v0.1.00
		"""

		self.headers = { }
		"""
HTTP request headers
		"""
	#

	def get_accepted_formats(self):
	#
		"""
Returns the formats the client accepts.

:return: (list) Accepted formats
:since:  v0.1.00
		"""

		_return = self.get_header("Accept")
		if (_return != None): _return = Http.header_field_list(_return)
		if (_return == None): _return = [ ]

		for position in range(0, len(_return)): _return[position] = _return[position].split(";")[0]
		return _return
	#

	def get_compression_formats(self):
	#
		"""
Returns the compression formats the client accepts.

:return: (list) Accepted compression formats
:since:  v0.1.01
		"""

		_return = self.get_header("Accept-Encoding")
		if (_return != None): _return = Http.header_field_list(_return)
		if (_return == None): _return = [ ]

		for position in range(0, len(_return)): _return[position] = _return[position].split(";")[0]
		return _return
	#

	def get_header(self, name):
	#
		"""
Returns the request header if defined.

:param name: Header name

:return: (str) Header value if set; None otherwise
:since:  v0.1.00
		"""

		name = name.upper()

		if (name in self.headers): return self.headers[name]
		else: return None
	#

	def get_headers(self):
	#
		"""
Returns the request headers as dict.

:return: (dict) Headers
:since:  v0.1.00
		"""

		return self.headers.copy()
	#
#

##j## EOF