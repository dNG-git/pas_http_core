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
from zlib import decompressobj, MAX_WBITS

from dNG.net.http.chunked_reader_mixin import ChunkedReaderMixin
from dNG.pas.data.byte_buffer import ByteBuffer
from dNG.pas.data.settings import Settings
from dNG.pas.data.supports_mixin import SupportsMixin
from dNG.pas.runtime.io_exception import IOException
from dNG.pas.runtime.value_exception import ValueException

class RequestBody(ChunkedReaderMixin, SupportsMixin):
#
	"""
The class "RequestBody" implements method to read the request body.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	# pylint: disable=arguments-differ

	def __init__(self):
	#
		"""
Constructor __init__(RequestBody)

:since: v0.1.00
		"""

		ChunkedReaderMixin.__init__(self)
		SupportsMixin.__init__(self)

		self.decompressors = None
		"""
List of decompressors
		"""
		self.headers = None
		"""
Dictionary with request headers
		"""
		self.input_chunk_encoded = False
		"""
True if the input is "chunked" encoded (and the size is unknown).
		"""
		self.input_ptr = None
		"""
Input pointer
		"""
		self.input_size = -1
		"""
Input size in bytes if known.
		"""
		self.received_data = None
		"""
Received file-like data object
		"""
		self.received_data_size = 0
		"""
Size of the file-like data object
		"""
		self.received_size_max = int(Settings.get("pas_http_site_request_body_size_max", 10485760))
		"""
Timeout for each network read.
		"""
		self.socket_data_timeout = int(Settings.get("pas_http_core_request_body_socket_data_timeout", 0))
		"""
Timeout for each network read.
		"""
		self.timeout = int(Settings.get("pas_http_request_body_timeout", 7200))
		"""
Absolute timeout to receive the request body.
		"""

		if (self.socket_data_timeout < 1): self.socket_data_timeout = int(Settings.get("pas_global_client_socket_data_timeout", 0))
		if (self.socket_data_timeout < 1): self.socket_data_timeout = int(Settings.get("pas_global_socket_data_timeout", 30))
	#

	def _append_received_data(self, data):
	#
		"""
Handles data received.

:param data: Data read from input

:since: v0.1.01
		"""

		if (data == None): data = self.decompress(None)

		if (data != None):
		#
			self.received_data_size += len(data)
			if (self.received_size_max > 0 and self.received_data_size > self.received_size_max): raise ValueException("Input size exceeds allowed limit")
			self.received_data.write(data)
		#
	#

	def decompress(self, data):
	#
		"""
Reads "chunked" encoded content if set to true.

:param chunk_encoded: True to active the "chunked" encoded mode

:since: v0.1.00
		"""

		_return = (data if (self.decompressors == None) else None)
		raw_data = data

		if (self.decompressors != None):
		#
			for decompressor in self.decompressors: raw_data = (decompressor.flush() if (data == None) else decompressor.decompress(raw_data))
			_return = raw_data
		#

		return _return
	#

	def define_input_chunk_encoded(self, chunk_encoded):
	#
		"""
Reads "chunked" encoded content if set to true.

:param chunk_encoded: True to active the "chunked" encoded mode

:since: v0.1.00
		"""

		self.input_chunk_encoded = chunk_encoded
	#

	def define_input_compression(self, method):
	#
		"""
Reads "chunked" encoded content if set to true.

:param chunk_encoded: True to active the "chunked" encoded mode

:since: v0.1.00
		"""

		methods = (method if (type(method) == list) else [ method ])
		self.decompressors = [ ]

		for method in methods:
		#
			if (method == "deflate"): self.decompressors.append(decompressobj(MAX_WBITS))
			elif (method == "gzip"): self.decompressors.append(decompressobj(16 + MAX_WBITS))
			else: raise ValueException("Unsupported compression definition '{0}' given".format(method))
		#
	#

	def get(self, timeout = None):
	#
		"""
Returns the request body.

:param timeout: Attribute name

:return: (str) Request body data
:since:  v0.1.00
		"""

		# pylint: disable=arguments-differ,raising-bad-type

		if (timeout == None): timeout = self.socket_data_timeout

		if (self.input_ptr != None):
		#
			if (hasattr(self.input_ptr, "settimeout")): self.input_ptr.settimeout(self.socket_data_timeout)

			try: self.run(timeout)
			finally: self.input_ptr = None
		#

		return self.received_data
	#

	def run(self, timeout = None):
	#
		"""
Sets a given pointer for the streamed post instance.

:since: v0.1.00
		"""

		# pylint: disable=broad-except

		if (timeout == None): timeout = self.timeout

		self.received_data = ByteBuffer()
		self.received_data_size = 0

		if (self.input_size < 0 and (not self.input_chunk_encoded)): raise IOException("Input size and expected first chunk size are unknown")

		if (self.input_chunk_encoded): self._read_chunked_data(self.input_ptr.read, self._append_received_data,timeout = timeout)
		else:
		#
			timeout_time = time() + timeout
			size_unread = self.input_size

			while (size_unread > 0 and time() < timeout_time):
			#
				part_size = (4096 if (size_unread > 4096) else size_unread)
				part_data = self.input_ptr.read(part_size)
				part_size = len(part_data)

				if (part_size < 1): raise IOException("Input pointer could not be read before socket timeout occurred")

				if (part_size > 0):
				#
					size_unread -= part_size
					self._append_received_data(part_data)
				#
			#
		#

		self._append_received_data(None)
		self.received_data.seek(0)
	#

	def set_headers(self, headers):
	#
		"""
Sets a given pointer for the RequestBody instance.

:param instance: File-like instance

:since: v0.1.00
		"""

		self.headers = headers
	#

	def set_input_ptr(self, input_ptr):
	#
		"""
Sets a given pointer for the RequestBody instance.

:param instance: File-like instance

:since: v0.1.00
		"""

		self.input_ptr = input_ptr
	#

	def set_input_size(self, _bytes):
	#
		"""
Sets the expected input size.

:param _bytes: Size in bytes

:since: v0.1.00
		"""

		self.input_size = _bytes
	#

	def set_timeout(self, timeout):
	#
		"""
Sets the absolute timeout to receive the request body.

:param timeout: Timeout in seconds

:since: v0.1.00
		"""

		self.timeout = timeout
	#
#

##j## EOF