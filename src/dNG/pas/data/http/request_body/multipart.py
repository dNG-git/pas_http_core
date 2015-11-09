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

from collections import Mapping
import re

from dNG.data.rfc.header import Header
from dNG.pas.data.binary import Binary
from dNG.pas.data.byte_buffer import ByteBuffer
from dNG.pas.data.settings import Settings
from dNG.pas.data.streamer.base64_decoder import Base64Decoder
from dNG.pas.data.streamer.quoted_printable_decoder import QuotedPrintableDecoder
from dNG.pas.runtime.io_exception import IOException
from dNG.pas.runtime.value_exception import ValueException
from .data import Data

class Multipart(Mapping, Data):
#
	"""
"Multipart" parses an incoming request body in MIME format.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.03
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	BINARY_BOUNDARY_PREFIX = Binary.bytes("\r\n--")
	"""
Boundary prefix
	"""
	RE_MIME_BOUNDARY = re.compile(Binary.bytes("(^|\r\n)\\-\\-(\S{1,994})(\r\n.+?\r\n|\\-\\-)(?=\r\n|$)"), re.S)
	"""
RegEx to identify opening and closing MIME boundaries
	"""
	TYPE_ID = "multipart"
	"""
Body type ID
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Multipart)

:since: v0.1.03
		"""

		Data.__init__(self)

		self.parts = None
		"""
Parts found in the "multipart/form_data" submission.
		"""
		self.pending_buffer = None
		"""
		"""
		self.pending_buffer_header_size_max = int(Settings.get("pas_http_site_request_body_multipart_pending_buffer_header_size_max", 65536))
		"""
Threshold to write the internal buffer to an external file.
		"""
		self.pending_mime_parts = [ ]
		"""
		"""
		self.pending_received_data = None
		"""
		"""

		self.supported_features['body_parser'] = True
	#

	def __getitem__(self, key):
	#
		"""
python.org: Called to implement evaluation of self[key].

:param key: Value key

:return: (mixed) Value
:since:  v0.1.03
		"""

		if (self.parts is None): self.parse()
		return (self.parts[key]['list'] if ("list" in self.parts[key]) else self.parts[key])
	#

	def __iter__(self):
	#
		"""
python.org: Return an iterator object.

:return: (object) Iterator object
:since:  v0.1.03
		"""

		if (self.parts is None): self.parse()
		return iter(self.parts)
	#

	def __len__(self):
	#
		"""
python.org: Called to implement the built-in function len().

:return: (int) Length of the object
:since:  v0.1.03
		"""

		if (self.parts is None): self.parse()
		return len(self.parts)
	#

	def _check_mime_part_id(self, mime_part_id):
	#
		"""
Checks if a given MIME part ID is a false positive.

:return: (bool) True if valid MIME part ID
:since:  v0.1.03
		"""

		return (mime_part_id in self.pending_mime_parts)
	#

	def _handle_data(self, data):
	#
		"""
Handles data received.

:param data: Data read from input

:since: v0.1.01
		"""

		data = self._decompress(data)

		if (data is not None):
		#
			buffered_data = self.pending_buffer + data
			buffered_data_size = len(buffered_data)
			data_size = len(data)
			last_boundary_end_position = 0

			if (self.pending_received_data is None):
			#
				re_result = Multipart.RE_MIME_BOUNDARY.search(buffered_data)

				if (re_result is not None):
				#
					mime_part_id = Binary.str(re_result.group(2))
					mime_part_trailing_data = Binary.str(re_result.group(3))

					if (mime_part_trailing_data == "--"
					    or (len(self.pending_mime_parts) > 0
					        and mime_part_id not in self.pending_mime_parts
					       )
					   ): raise IOException("Invalid MIME part received")

					if (len(self.pending_mime_parts) < 1): self.pending_mime_parts.append(mime_part_id)

					self._handle_mime_part_headers(mime_part_id, mime_part_trailing_data.strip())

					last_boundary_end_position = re_result.end()

					self.pending_received_data = ByteBuffer()
				#
				elif (buffered_data_size >= self.pending_buffer_header_size_max): raise IOException("MIME part buffer exceeded")
			#

			self.received_data_size += data_size
			if (self.received_size_max > 0 and self.received_data_size > self.received_size_max): raise ValueException("Input size exceeds allowed limit")

			if (Multipart.BINARY_BOUNDARY_PREFIX not in buffered_data):
			#
				self.pending_buffer = Binary.BYTES_TYPE()
				self.pending_received_data.write(buffered_data)
			#
			else:
			#
				for re_result in Multipart.RE_MIME_BOUNDARY.finditer(buffered_data, last_boundary_end_position):
				#
					current_boundary_start_position = re_result.start()
					current_boundary_end_position = re_result.end()

					mime_part_id = Binary.raw_str(re_result.group(2))

					if (last_boundary_end_position != current_boundary_start_position):
					#
						self.pending_received_data.write(buffered_data[last_boundary_end_position:current_boundary_start_position])
					#

					if (self._check_mime_part_id(mime_part_id)):
					#
						mime_part_trailing_data = Binary.str(re_result.group(3))

						if (self.pending_received_data is not None):
						#
							self._handle_mime_part_received(mime_part_id)
							self.pending_received_data = ByteBuffer()
						#

						if (mime_part_trailing_data == "--"): self.pending_mime_parts.remove(mime_part_id)
						else:
						#
							self._handle_mime_part_headers(mime_part_id, mime_part_trailing_data.strip())
							current_boundary_end_position += 2 # Ignore CR LF of look-ahead match end
						#
					#
					else: self.pending_received_data.write(buffered_data[current_boundary_start_position:current_boundary_end_position])

					last_boundary_end_position = current_boundary_end_position
				#

				pending_buffer_start_position = (buffered_data_size - last_boundary_end_position)

				if (pending_buffer_start_position > self.pending_buffer_header_size_max):
				#
					self.pending_buffer = buffered_data[-1 * self.pending_buffer_header_size_max:]
					self.pending_received_data.write(buffered_data[:-1 * self.pending_buffer_header_size_max])
				#
				else:
				#
					self.pending_buffer = (Binary.BYTES_TYPE()
					                       if (pending_buffer_start_position < 1) else
					                       buffered_data[-1 * pending_buffer_start_position:]
					                      )
				#
			#
		#
	#

	def _handle_mime_part_received(self, mime_part_id):
	#
		"""
Handles MIME part header.

:param mime_part_id: MIME part ID
:param data: Data read from input

:since: v0.1.03
		"""

		if (mime_part_id not in self.pending_mime_parts): raise IOException("Invalid MIME part received")

		part = (self.parts[mime_part_id]['list'][-1]
		        if ("list" in self.parts[mime_part_id]) else
		        self.parts[mime_part_id]
		       )

		content_transfer_encoding = ""

		if ("CONTENT-TRANSFER-ENCODING" in part['headers']):
		#
			content_transfer_encoding = part['headers']['CONTENT-TRANSFER-ENCODING'].strip()
		#

		if (content_transfer_encoding == "base64"): part['data'] = Base64Decoder(self.pending_received_data)
		elif (content_transfer_encoding == "quoted-printable"): part['data'] = QuotedPrintableDecoder(self.pending_received_data)
		else: part['data'] = self.pending_received_data
	#

	def _handle_mime_part_headers(self, mime_part_id, data):
	#
		"""
Handles MIME part header.

:param mime_part_id: MIME part ID
:param data: Data read from input

:since: v0.1.03
		"""

		mime_headers = Header.get_headers(Binary.str(data))

		if (mime_part_id not in self.parts):
		#
			part_position = len(self.parts)
			self.parts[mime_part_id] = { "headers": mime_headers, "position": part_position }
		#
		elif ("list" in self.parts[mime_part_id]): self.parts[mime_part_id]['list'].append({ "headers": mime_headers })
		else:
		#
			single_mime_part = { "headers": self.parts[mime_part_id]['headers'] }
			if ("data" in self.parts[mime_part_id]): single_mime_part['data'] = self.parts[mime_part_id]['data']

			self.parts[mime_part_id] = { "position": self.parts[mime_part_id]['position'],
			                             "list": [ single_mime_part,
			                                       { "headers": mime_headers }
			                                     ]
			                           }
		#
	#

	def _init_read(self):
	#
		"""
Initializes internal variables for reading from input.

:since: v0.1.03
		"""

		Data._init_read(self)

		self.parts = { }
		self.pending_buffer = Binary.BYTES_TYPE()
	#

	def parse(self):
	#
		"""
Parses the content of the request body.

:since: v0.1.03
		"""

		if (self.headers is None): raise ValueException("Request body can't be read without HTTP headers")

		if ("CONTENT-TYPE" not in self.headers): raise IOException("Content-Type not specified")

		for content_type_option in Header.get_field_list_dict(self.headers['CONTENT-TYPE'], ";", "="):
		#
			if (type(content_type_option) is dict
			    and content_type_option['key'].lower() == "boundary"
			   ): self.pending_mime_parts.append(content_type_option['value'])
		#

		self.read()

		if (len(self.pending_mime_parts) > 0): raise IOException("Not all MIME parts have been received")
	#
#

##j## EOF