# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.http.RequestBody
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

from threading import Event, Thread
from time import time
from zlib import decompressobj, MAX_WBITS

from dNG.pas.data.binary import Binary
from dNG.pas.data.byte_buffer import ByteBuffer
from dNG.pas.data.settings import Settings

class RequestBody(dict, Thread):
#
	"""
The class "RequestBody" implements method to read the request body.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, receive_in_thread = False):
	#
		"""
Constructor __init__(RequestBody)

:since: v0.1.00
		"""

		dict.__init__(self)
		if (receive_in_thread): Thread.__init__(self)

		self.decompressors = None
		"""
List of decompressors
		"""
		self.input_chunk_encoded = False
		"""
True if the input is "chunked" encoded (and the size is unknown).
		"""
		self.input_data = None
		"""
Received file-like data object
		"""
		self.input_ptr = None
		"""
Input pointer
		"""
		self.input_size = -1
		"""
Input size in bytes if known.
		"""
		self.receive_in_thread = receive_in_thread
		"""
True if reading should happen in a separate thread.
		"""
		self.received_event = Event()
		"""
Event called after all data has been received.
		"""
		self.socket_data_timeout = int(Settings.get("pas_server_socket_data_timeout", 0))
		"""
Timeout for each network read.
		"""
		self.timeout = int(Settings.get("pas_http_request_body_timeout", 7200))
		"""
Absolute timeout to receive the request body.
		"""

		if (self.socket_data_timeout < 1): self.socket_data_timeout = int(Settings.get("pas_global_socket_data_timeout", 30))
		self.received_event.set()
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
			else: raise ValueError("Unsupported compression definition '{0}' given".format(method))
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

		_return = None

		if (timeout == None): timeout = self.socket_data_timeout
		if (self.input_ptr != None and (not self.receive_in_thread)): self.run(timeout)

		if (self.received_event.wait(timeout)):
		#
			if (isinstance(self.input_data, Exception)): raise self.input_data
			else: _return = self.input_data
		#
		else: raise RuntimeError("Input pointer could not be read before timeout occurred", 62)

		return _return
	#

	def run(self, timeout = None):
	#
		"""
Sets a given pointer for the streamed post instance.

:since: v0.1.00
		"""

		try:
		#
			binary_newline = Binary.bytes("\r\n")
			chunk_buffer = None
			chunk_size = 0
			input_data = ByteBuffer()
			is_last_chunk = False
			if (self.input_size < 0): self.input_size = 5
			size_unread = self.input_size
			timeout_time = time() + (self.timeout if (timeout == None) else timeout)

			while (size_unread > 0 and time() < timeout_time):
			#
				part_size = (4096 if (size_unread > 4096) else size_unread)
				part_data = self.input_ptr.read(part_size)
				part_size = len(part_data)

				if (part_size < 1): raise RuntimeError("Input pointer could not be read before socket timeout occurred", 62)
				elif (self.input_chunk_encoded):
				#
					"""
Read remaining data from last chunk
					"""

					if (chunk_size > 0):
					#
						chunk_size = (0 if (part_size >= chunk_size) else chunk_size - part_size)
						input_data.write(self.decompress(part_data[:part_size]))

						part_data = part_data[part_size:]
					#

					"""
Get size for next chunk
					"""

					if (chunk_size < 1):
					#
						if (chunk_buffer == None): newline_position = part_data.find(binary_newline)
						else: newline_position = (chunk_buffer + part_data).find(binary_newline)

						chunk_octets = None

						if (newline_position < 0):
						#
							if (chunk_buffer == None): chunk_buffer = part_data
							else: chunk_buffer += part_data

							part_size = 0
							self.input_size += 3
						#
						elif (chunk_buffer != None):
						#
							chunk_octets = (chunk_buffer + part_data)[:newline_position]
							part_data = (chunk_buffer + part_data)[2 + newline_position:]
							part_size = len(part_data)

							chunk_buffer = None
						#
						elif (not is_last_chunk):
						#
							chunk_octets = part_data[:newline_position]
							part_data = part_data[2 + newline_position:]

							part_size = len(part_data)
						#
						else: part_size = 0

						if (chunk_octets != None):
						#
							chunk_size = int(chunk_octets, 16)

							if (chunk_size == 0): is_last_chunk = True
							else:
							#
								self.input_size += chunk_size
								size_unread += chunk_size
							#
						#
					#
				#

				if (part_size > 0):
				#
					size_unread -= part_size
					input_data.write(self.decompress(part_data))
				#
			#
		#
		except Exception as handled_exception: self.input_data = handled_exception

		part_data = self.decompress(None)
		if (part_data != None): input_data.write(part_data)
		input_data.seek(0)

		self.input_data = input_data
		self.input_ptr = None

		self.received_event.set()
	#

	def set_input_ptr(self, input_ptr):
	#
		"""
Sets a given pointer for the streamed post instance. If a separate thread is
used to read the body it is started here as well.

:since: v0.1.00
		"""

		if (self.input_size < 0 and (not self.input_chunk_encoded)): self.input_data = RuntimeError("Input size and expected first chunk size are unknown", 5)
		else:
		#
			if (hasattr(input_ptr, "settimeout")): input_ptr.settimeout(self.socket_data_timeout)
			self.input_ptr = input_ptr
			self.received_event.clear()

			if (self.receive_in_thread): self.start()
		#
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
#

##j## EOF