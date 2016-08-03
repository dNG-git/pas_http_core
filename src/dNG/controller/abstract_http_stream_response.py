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

from time import time
from zlib import compressobj

from dNG.data.binary import Binary
from dNG.data.gzip import Gzip
from dNG.data.http.chunked_mixin import ChunkedMixin
from dNG.data.rfc.basics import Basics as RfcBasics
from dNG.runtime.io_exception import IOException
from dNG.runtime.not_implemented_exception import NotImplementedException

from .abstract_http_request import AbstractHttpRequest
from .abstract_stream_response import AbstractStreamResponse

class AbstractHttpStreamResponse(ChunkedMixin, AbstractStreamResponse):
#
	"""
A HTTP aware stream response.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	STREAM_DIRECT = 2
	"""
Do not set Transfer-Encoding but output content directly as soon as it is
available.
	"""
	STREAM_CHUNKED = 4
	"""
Set Transfer-Encoding to chunked and encode output.
	"""

	def __init__(self):
	#
		"""
Constructor __init__(AbstractHttpStreamResponse)

:since: v0.2.00
		"""

		AbstractStreamResponse.__init__(self)

		self.accepted_formats = [ ]
		"""
Formats the client accepts
		"""
		self.compressor = None
		"""
Compression object or file
		"""
		self.compression_formats = None
		"""
Compression formats the client accepts
		"""
		self.cookies = { }
		"""
True if headers are sent
		"""
		self.headers = { }
		"""
Headers are used by the final node
		"""
		self.headers_only = False
		"""
Send headers only (usually HEAD requests)s
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

		self.set_header("Server", "directPAS/#echo(pasHttpCoreIVersion)# [direct Netware Group]")

		self.supported_features['compression'] = True
		self.supported_features['headers'] = True
		self.supported_features['streaming'] = True
	#

	def are_headers_sent(self):
	#
		"""
Returns true if headers are already sent.

:return: (bool) True if sent
:since:  v0.2.00
		"""

		return self.headers_sent
	#

	def _filter_headers(self):
	#
		"""
Filter response headers to remove conflicting ones.

:return: (dict) Filtered headers
:since:  v0.2.00
		"""

		_return = self.headers.copy()

		if ((self.compressor is not None
		     or self.stream_mode & AbstractHttpStreamResponse.STREAM_CHUNKED == AbstractHttpStreamResponse.STREAM_CHUNKED
		    )
		    and "CONTENT-LENGTH" in _return
		   ): del(_return['CONTENT-LENGTH'])

		if (len(self.cookies) > 0):
		#
			if ("SET-COOKIE" not in _return): _return['SET-COOKIE'] = [ ]
			elif (type(_return['SET-COOKIE']) is not list): _return['SET-COOKIE'] = [ _return['SET-COOKIE'] ]

			for cookie_name in self.cookies: _return['SET-COOKIE'].append(self.cookies[cookie_name])
		#

		return _return
	#

	def finish(self):
	#
		"""
Finish transmission and cleanup resources.

:since: v0.2.00
		"""

		if (self.active):
		#
			is_chunked_response = False

			if (self.stream_mode & AbstractHttpStreamResponse.STREAM_CHUNKED == AbstractHttpStreamResponse.STREAM_CHUNKED):
			#
				is_chunked_response = True
				self.send()
			#

			if (is_chunked_response or self.compressor is not None): self.send_data(None)

			AbstractStreamResponse.finish(self)
			self.compressor = None
		#
	#

	def get_accepted_formats(self):
	#
		"""
Returns the formats the client accepts.

:return: (list) Accepted formats
:since:  v0.2.00
		"""

		return self.accepted_formats
	#

	def get_compression_formats(self):
	#
		"""
Returns the compression formats the client accepts.

:return: (list) Compression formats supported
:since:  v0.2.00
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
:since:  v0.2.00
		"""

		name = name.upper()

		if (name in self.headers): _return = self.headers[name]
		elif (name_as_key and name in self.headers_indexed): _return = self.headers[self.headers_indexed[name]]
		else: _return = None

		return _return
	#

	def get_http_code(self):
	#
		"""
Returns the HTTP response code.

:return: (int) HTTP code
:since:  v0.2.00
		"""

		return (200 if (self.http_code is None) else self.http_code)
	#

	def is_compressing(self):
	#
		"""
Returns true if the response will be compressed.

:return: (bool) True if compression is used for the response
:since:  v0.2.00
		"""

		return (self.compressor is not None)
	#

	def _prepare_output_data(self, data):
	#
		"""
Prepare data for output. Compress and transform it if required.

:param data: Data for output

:return: (bytes) Transformed data
:since:  v0.2.00
		"""

		is_chunked_response = (self.stream_mode & AbstractHttpStreamResponse.STREAM_CHUNKED == AbstractHttpStreamResponse.STREAM_CHUNKED)

		if (self.compressor is not None):
		#
			if (data is None): data = self.compressor.flush()
			elif (len(data) > 0): data = self.compressor.compress(Binary.bytes(data))
		#

		if (is_chunked_response): data = self.chunkify(data)

		return data
	#

	def send_data(self, data):
	#
		"""
Sends response data.

:param data: Additional data to be send

:since: v0.2.00
		"""

		if (self.active):
		#
			if (not self.headers_sent):
			#
				if (self.http_code is None): self.set_http_code(200)
				self.send_headers()
			#

			if (not self.headers_only): AbstractStreamResponse.send_data(self, self._prepare_output_data(data))
		#
	#

	def send_headers(self):
	#
		"""
Sends the prepared response headers.

:since: v0.2.00
		"""

		raise NotImplementedException()
	#

	def set_accepted_formats(self, accepted_formats):
	#
		"""
Sets the formats the client accepts.

:param accepted_formats: List of accepted formats

:since: v0.2.00
		"""

		if (isinstance(accepted_formats, list)): self.accepted_formats = accepted_formats
	#

	def set_compression(self, compress):
	#
		"""
Sets the compression formats the client accepts.

:param compress: True to compress the response

:since: v0.2.00
		"""

		if (compress == False):
		#
			self.compressor = None
			self.set_header("Content-Encoding", None)
		#
		elif (self.compression_formats is not None):
		#
			if ("gzip" in self.compression_formats):
			#
				self.compressor = Gzip()
				self.set_header("Content-Encoding", "gzip")
			#
			elif ("deflate" in self.compression_formats):
			#
				self.compressor = compressobj()
				self.set_header("Content-Encoding", "deflate")
			#
		#
	#

	def set_compression_formats(self, compression_formats):
	#
		"""
Sets the compression formats the client accepts.

:param compression_formats: List of accepted compression formats

:since: v0.2.00
		"""

		if (isinstance(compression_formats, list)): self.compression_formats = compression_formats
	#

	def set_cookie(self, name, value, timeout = 1209600, secure_only = False, http_only = False, domain = None, path = None):
	#
		"""
Sets a cookie.

:param name: Cookie name
:param value: Cookue value as string
:param timeout: Cookie timeout in seconds (max-age)
:param secure_only: True if send "secure" flag
:param http_only: True if send "httpOnly" flag
:param domain: Cookie domain restriction (defaults to requested host)
:param path: Cookie path restriction (defaults to "/")

:since: v0.2.00
		"""

		if (";" in value or '"' in value):
		#
			value = value.replace('"', '\"')
			value = '"{0}"'.format(value)
		#

		timeout = (time() + timeout if (timeout > 0) else time() - 3600)

		cookie = "{0}={1};Expires={2}".format(name, value, RfcBasics.get_rfc5322_datetime(timeout))
		if (secure_only): cookie += ";Secure="
		if (http_only): cookie += ";HttpOnly="

		if (domain is None):
		#
			request = AbstractHttpRequest.get_instance()
			if (request is not None): cookie += ";Domain={0}".format(request.get_server_host())
		#
		else: cookie += ";Domain={0}".format(domain)

		if (path is None): path = "/"
		cookie += ";Path={0}".format(path)

		self.cookies[name] = cookie
	#

	def set_header(self, name, value, name_as_key = False, value_append = False):
	#
		"""
Sets a header.

:param name: Header name
:param value: Header value as string or array
:param name_as_key: True if the name is used as a key
:param value_append: True if headers should be appended

:since: v0.2.00
		"""

		# pylint: disable=maybe-no-member
		# pylint doesn't work well with value being of type mixed

		if (self.headers_sent): raise IOException("Headers are already sent")
		name = name.upper()

		if (name_as_key and name == "HTTP/1.1"):
		#
			http_values = value.split(" ", 2)
			if (len(http_values) == 3): self.set_http_code(int(http_values[1]))

			if (self.http_version == 1):
			#
				if (value == "HTTP/1.1 203 Non-Authoritative Information"): value = "HTTP/1.1 200 OK"
				elif (value == "HTTP/1.1 303 See Other"): value = "HTTP/1.1 302 Found"
				elif (value == "HTTP/1.1 307 Temporary Redirect"): value = "HTTP/1.1 302 Found"
			#
		#

		if (name_as_key):
		#
			if (name in self.headers_indexed):
			#
				if (value is None): del(self.headers[self.headers_indexed[name]])
				elif (value_append):
				#
					if (type(self.headers[self.headers_indexed[name]]) is list): self.headers[self.headers_indexed[name]].append(value)
					else: self.headers[self.headers_indexed[name]] = [ self.headers[self.headers_indexed[name]], value ]
				#
				else: self.headers[self.headers_indexed[name]] = value
			#
			elif (value is not None):
			#
				self.headers[self.headers_index] = value
				self.headers_indexed[name] = self.headers_index
				self.headers_index += 1
			#
		#
		elif (value is None):
		#
			if (name in self.headers): del(self.headers[name])
		#
		elif (type(value) is list): self.headers[name] = (value if (len(value) > 1) else value.pop())
		elif (value_append and name in self.headers):
		#
			if (type(self.headers[name]) is list): self.headers[name].append(value)
			else: self.headers[name] = [ self.headers[name], value ]
		#
		else: self.headers[name] = value
	#

	def set_http_code(self, http_code):
	#
		"""
Sets the HTTP response code.

:param http_version: HTTP code

:since: v0.2.00
		"""

		self.http_code = http_code
	#

	def set_http_version(self, http_version):
	#
		"""
Sets the HTTP protocol version.

:param http_version: HTTP version

:since: v0.2.00
		"""

		self.http_version = http_version
	#

	def set_send_headers_only(self, headers_only):
	#
		"""
Set to true to send headers only.

:param headers_only: Usually true for HEAD requests

:since: v0.2.00
		"""

		self.headers_only = headers_only
	#

	def set_stream_mode(self):
	#
		"""
Sets the stream mode to send output as soon as available instead of caching
it.

:since: v0.2.00
		"""

		self.update_stream_mode()
	#

	def update_stream_mode(self):
	#
		"""
Sets the stream mode or updates the stream mode algorithm selected to send
output as soon as available instead of caching it.

:since: v0.2.00
		"""

		is_chunked_mode_required = (self.get_header("Content-Length") is None)

		is_chunked_mode_supported = (self.stream_mode_supported & AbstractHttpStreamResponse.STREAM_CHUNKED == AbstractHttpStreamResponse.STREAM_CHUNKED
		                             and self.http_version > 1
		                            )

		if (is_chunked_mode_supported
		    and (not is_chunked_mode_required)
		    and self.stream_mode & AbstractHttpStreamResponse.STREAM_CHUNKED == AbstractHttpStreamResponse.STREAM_CHUNKED
		   ):
		#
			if (self.get_header("Transfer-Encoding") == "chunked"): self.set_header("Transfer-Encoding", None)
			self.stream_mode ^= AbstractHttpStreamResponse.STREAM_CHUNKED
		#

		is_direct_mode_supported = (self.stream_mode_supported & AbstractHttpStreamResponse.STREAM_DIRECT == AbstractHttpStreamResponse.STREAM_DIRECT)

		if (not is_direct_mode_supported
		    and self.stream_mode & AbstractHttpStreamResponse.STREAM_DIRECT == AbstractHttpStreamResponse.STREAM_DIRECT
		   ): self.stream_mode ^= AbstractHttpStreamResponse.STREAM_DIRECT


		if (is_chunked_mode_supported and is_chunked_mode_required):
		#
			self.set_header("Transfer-Encoding", "chunked")
			self.stream_mode |= AbstractHttpStreamResponse.STREAM_CHUNKED
		#
		elif (is_direct_mode_supported): self.stream_mode |= AbstractHttpStreamResponse.STREAM_DIRECT
	#
#

##j## EOF