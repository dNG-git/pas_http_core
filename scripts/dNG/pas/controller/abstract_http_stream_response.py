# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.controller.abstract_http_stream_response
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

from zlib import compressobj, Z_SYNC_FLUSH

from dNG.pas.net.http.chunked_mixin import direct_chunked_mixin
from dNG.pas.data.binary import direct_binary
from dNG.pas.data.http.gzip_compressor import direct_gzip_compressor
from .abstract_stream_response import direct_abstract_stream_response

class direct_abstract_http_stream_response(direct_abstract_stream_response, direct_chunked_mixin):
#
	"""
A HTTP headers aware stream response.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	STREAM_DIRECT = 1
	"""
Do not set Transfer-Encoding but output content directly as soon as it is
available.
	"""
	STREAM_CHUNKED = 2
	"""
Set Transfer-Encoding to chunked and encode output.
	"""

	def __init__(self):
	#
		"""
Constructor __init__(direct_abstract_http_stream_response)

:since: v0.1.00
		"""

		direct_abstract_stream_response.__init__(self)

		self.compressor = None
		"""
Compression object or file
		"""
		self.compressor_buffer = None
		"""
Buffer to read compressed object
		"""
		self.compression_formats = None
		"""
Compression formats the client accepts
		"""
		self.headers = { }
		"""
Headers are used by the final node
		"""
		self.headers_index = 0
		"""
Current named headers index
		"""
		self.headers_indexed = { }
		"""
Headers using a header index
		"""
		self.headers_sent = False
		"""
True if headers are sent
		"""
		self.http_code = None
		"""
HTTP result code
		"""
		self.http_version = 1.1
		"""
HTTP request version
		"""
		self.stream_mode_supported = 2
		"""
Support chunked streaming
		"""
	#

	def are_headers_sent(self):
	#
		"""
Sends the prepared response headers.

:since: v0.1.00
		"""

		return self.headers_sent
	#

	def finish(self):
	#
		"""
Finish transmission and cleanup resources.

:since: v0.1.00
		"""

		if (self.active):
		#
			if (self.stream_mode == direct_abstract_http_stream_response.STREAM_CHUNKED): self.send_data(self.chunkify(None))
			direct_abstract_stream_response.finish(self)
		#
	#

	def get_compression_formats(self):
	#
		"""
Returns the compression formats the client accepts.

:return: (list) Compression formats supported
:since:  v0.1.01
		"""

		return self.compression_formats
	#

	def get_header(self, name, name_as_key = True):
	#
		"""
Returns an already defined header.

:param name: Header name
:param name_as_key: True if the name is used as a key

:return: (str) Header value if set; None otherwise
:since:  v0.1.00
		"""

		name = name.upper()

		if (name in self.headers): var_return = self.headers[name]
		elif (name_as_key and name in self.headers_indexed): var_return = self.headers[self.headers_indexed[name]]
		else: var_return = None

		return var_return
	#

	def get_http_code(self):
	#
		"""
Returns the HTTP response code.

:return: (int) HTTP code
:since:  v0.1.00
		"""

		return self.http_code
	#

	def send_data(self, data):
	#
		"""
Sends response data.

:param data: Additional data to be send

:since: v0.1.00
		"""

		if (self.active):
		#
			if (not self.headers_sent):
			#
				if (self.http_code == None): self.set_http_code(200)
				self.send_headers()
			#

			if (self.compressor != None): data = self.compressor.compress(direct_binary.bytes(data)) + self.compressor.flush(Z_SYNC_FLUSH)
			if (self.stream_mode == direct_abstract_http_stream_response.STREAM_CHUNKED): data = self.chunkify(data)
			direct_abstract_stream_response.send_data(self, data)
		#
	#

	def send_headers(self):
	#
		"""
Sends the prepared response headers.

:since: v0.1.00
		"""

		raise RuntimeError("Not implemented", 38)
	#

	def set_compression(self, compress):
	#
		"""
Sets the compression formats the client accepts.

:param compression_formats: List of accepted compression formats

:since: v0.1.01
		"""

		if (compress == True and self.compression_formats != None):
		#
			if ("deflate" in self.compression_formats):
			#
				self.compressor = compressobj()
				self.set_header("Content-Encoding", "deflate")
			#
			elif ("gzip" in self.compression_formats):
			#
				self.compressor = direct_gzip_compressor()
				self.set_header("Content-Encoding", "gzip")
			#
		#
	#

	def set_compression_formats(self, compression_formats):
	#
		"""
Sets the compression formats the client accepts.

:param compression_formats: List of accepted compression formats

:since: v0.1.01
		"""

		if (isinstance(compression_formats, list)): self.compression_formats = compression_formats
	#

	def set_header(self, name, value, name_as_key = False, value_append = False):
	#
		"""
Sets a header.

:param name: Header name
:param value: Header value as string or array
:param name_as_key: True if the name is used as a key
:param value_append: True if headers should be appended

:since: v0.1.00
		"""

		name = name.upper()

		if (name_as_key and name == "HTTP/1.1"):
		#
			http_values = value.split(" ", 2)
			if (len(http_values) == 3): self.set_http_code(int(http_values[1]))

			if (self.http_version == 1):
			#
				if (value == "HTTP/1.1 203 Non-Authoritative Information"): value = "HTTP/1.1 200 OK"
				elif (value == "HTTP/1.1 303 See Other"): value = "HTTP/1.0 302 Found"
				elif (value == "HTTP/1.1 307 Temporary Redirect"): value = "HTTP/1.0 302 Found"
			#
		#

		if (name_as_key):
		#
			if (name in self.headers_indexed):
			#
				if (value == None): del(self.headers[self.headers_indexed[name]])
				elif (value_append):
				#
					if (type(self.headers[self.headers_indexed[name]]) == list): self.headers[self.headers_indexed[name]].append(value)
					else: self.headers[self.headers_indexed[name]] = [ self.headers[self.headers_indexed[name]], value ]
				#
				else: self.headers[self.headers_indexed[name]] = value
			#
			elif (value != None):
			#
				self.headers[self.headers_index] = value
				self.headers_indexed[name] = self.headers_index
				self.headers_index += 1
			#
		#
		elif (value == None):
		#
			if (name in self.headers): del(self.headers[name])
		#
		elif (type(value) == list): self.headers[name] = (value if (len(value) > 1) else value.pop())
		elif (value_append and name in self.headers):
		#
			if (type(self.headers[name]) == list): self.headers[name].append(value)
			else: self.headers[name] = [ self.headers[name], value ]
		#
		else: self.headers[name] = value
	#

	def set_http_code(self, http_code):
	#
		"""
Sets the HTTP response code.

:param http_version: HTTP code

:since: v0.1.00
		"""

		if (self.http_code == None and "Server" not in self.headers): self.set_header("Server", "directPAS/#echo(pasHttpCoreIVersion)# [direct Netware Group]")
		self.http_code = http_code
	#

	def set_http_version(self, http_version):
	#
		"""
Sets the HTTP protocol version.

:param http_version: HTTP version

:since: v0.1.00
		"""

		self.http_version = http_version
	#

	def set_stream_mode(self, active):
	#
		"""
Sets the stream response object used to send data to.

:param active: True if streaming response
:since: v0.1.00
		"""

		if (self.headers_sent): raise RuntimeError("Can't change streaming mode after headers are sent", 38)

		if (active and self.stream_mode == direct_abstract_http_stream_response.STREAM_NONE):
		#
			self.stream_mode = self.stream_mode_supported
			if (self.stream_mode_supported == direct_abstract_http_stream_response.STREAM_CHUNKED): self.set_header("Transfer-Encoding", "chunked")
		#
		elif (self.stream_mode != direct_abstract_http_stream_response.STREAM_NONE):
		#
			self.stream_mode = direct_abstract_http_stream_response.STREAM_NONE
			if (self.stream_mode_supported == direct_abstract_http_stream_response.STREAM_CHUNKED): self.set_header("Transfer-Encoding", None)
		#
	#

	def supports_compression(self):
	#
		"""
Returns false if data can not be compressed before being send.

:return: (bool) True if the response can be compressed.
:since:  v0.1.00
		"""

		return True
	#

	def supports_headers(self):
	#
		"""
Returns false if headers are not supported.

:return: (bool) True if the response contain headers.
:since:  v0.1.00
		"""

		return True
	#

	def supports_streaming(self):
	#
		"""
Returns false if responses can not be streamed.

:return: (bool) True if streaming is supported.
:since:  v0.1.00
		"""

		return True
	#
#

##j## EOF