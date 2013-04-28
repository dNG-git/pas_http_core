# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.controller.http_wsgi1_stream_response
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

from collections import Iterator

from dNG.pas.pythonback import direct_bytes
from .abstract_http_stream_response import direct_abstract_http_stream_response

class direct_http_wsgi1_stream_response(direct_abstract_http_stream_response, Iterator):
#
	"""
This stream response instance will write all data to the underlying WSGI
implementation.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, wsgi_header_response):
	#
		"""
Constructor __init__(direct_http_wsgi1_stream_response)

:param wsgi_header_response: WSGI header response callback

:since: v0.1.00
		"""

		direct_abstract_http_stream_response.__init__(self)

		self.stream_mode_supported = direct_abstract_http_stream_response.STREAM_DIRECT
		"""
Support chunked streaming
		"""
		self.wsgi_header_response = wsgi_header_response
		"""
The WSGI header response callback
		"""
		self.wsgi_write = None
		"""
The WSGI response writer callback
		"""
	#

	def __iter__(self):
	#
		"""
python.org: Return an iterator object.

:return: (object) Iterator object
:since:  v0.1.00
		"""

		return self
	#

	def __next__(self):
	#
		"""
python.org: Return the next item from the container.

:return: (str) Response data
:since:  v0.1.00
		"""

		if (self.active and self.data != None):
		#
			var_return = self.data
			self.data = None

			self.finish()
			return var_return
		#
		else: raise StopIteration()
	#
	next = __next__

	def close(self):
	#
		"""
Finish transmission and cleanup resources.

:since: v0.1.00
		"""

		self.active = False
	#

	def finish(self):
	#
		"""
Finish transmission and cleanup resources.

:since: v0.1.00
		"""

		if (self.active):
		#
			direct_abstract_http_stream_response.finish(self)
			self.wsgi_write = None
		#
	#

	def send_headers(self):
	#
		"""
Sends the prepared response headers.

:since: v0.1.00
		"""

		http_status_line = "200 Ok"

		headers = [ ]
		headers_indexed = dict([( value, key ) for ( key, value ) in self.headers_indexed.items()])

		for header_name in self.headers:
		#
			header_value = str(self.headers[header_name])

			if (type(header_name) == int):
			#
				header_name = headers_indexed[header_name]

				if (header_name == "HTTP/1.1"): http_status_line = header_value[9:]
				else: headers.append(( header_name, header_value ))
			#
			elif (type(header_value) == list):
			#
				for header_list_value in header_value: headers.append(( header_name, header_list_value ))
			#
			else: headers.append(( header_name, header_value ))
		#

		self.headers_sent = True
		self.wsgi_write = self.wsgi_header_response(http_status_line, headers)
		self.wsgi_header_response = None
	#

	def write(self, data):
	#
		"""
Writes the given data.

:param data: Data to be send

:access: protected
:since:  v0.1.00
		"""

		try:
		#
			if (self.active and self.wsgi_write != None):
			#
				data = direct_bytes(data)
				self.wsgi_write(data)
			#
		#
		except: self.active = False
	#
#

##j## EOF