# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.controller.abstract_stream_response
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

from dNG.pas.data.binary import direct_binary

class direct_abstract_stream_response(object):
#
	"""
A stream response writes given data threadsafe to a underlying stream.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	STREAM_CALLBACK = 1
	"""
Do not set Transfer-Encoding but output content directly as soon as it is
available.
	"""
	STREAM_NONE = 0
	"""
Do not stream content
	"""

	def __init__(self):
	#
		"""
Constructor __init__(direct_abstract_http_stream_response)

:since: v0.1.00
		"""

		self.accepted_formats = [ ]
		"""
Formats the client accepts
		"""
		self.active = True
		"""
True if ready for output.
		"""
		self.data = None
		"""
Data buffer
		"""
		self.stream_mode = 0
		"""
Stream response instead of holding it in a buffer
		"""
		self.stream_mode_supported = 0
		"""
Supported streaming mode
		"""
		self.streamer = None
		"""
Streamer implementation
		"""
	#

	def __del__(self):
	#
		"""
Destructor __del__(direct_abstract_response)

@since v0.1.00
		"""

		self.finish()
	#

	def finish(self):
	#
		"""
Finish transmission and cleanup resources.

:since: v0.1.00
		"""

		if (self.active):
		#
			self.send()
			self.active = False
		#
	#

	def get_accepted_formats(self):
	#
		"""
Returns the formats the client accepts.

:return: (list) Accepted formats
:since:  v0.1.01
		"""

		return self.accepted_formats
	#

	def is_active(self):
	#
		"""
Constructor __init__(direct_server_fascti)

@since v0.1.00
		"""

		return self.active
	#

	def is_streamer_set(self):
	#
		"""
Returns true if a streamer has been set.

:return: (bool) True if set
:since:  v0.1.01
		"""

		return (self.streamer != None)
	#

	def send(self):
	#
		"""
Send data in cache.

:since: v0.1.01
		"""

		if (self.active):
		#
			if (self.streamer != None and self.stream_mode_supported & direct_abstract_stream_response.STREAM_CALLBACK != direct_abstract_stream_response.STREAM_CALLBACK):
			#
				is_valid = True

				while (is_valid and (not self.streamer.eof_check())):
				#
					data = self.streamer.read()

					if (data == False or data == None): is_valid = False
					else: self.send_data(data)
				#

				self.streamer.close()
				self.streamer = None
			#
			elif (self.data != None):
			#
				self.write(self.data)
				self.data = None
			#
		#
	#

	def send_data(self, data):
	#
		"""
Constructor __init__(direct_server_fascti)

@since v0.1.00
		"""

		if (self.active):
		#
			data = direct_binary.bytes(data)

			if (self.stream_mode == direct_abstract_stream_response.STREAM_NONE):
			#
				if (self.data == None): self.data = direct_binary.BYTES_TYPE()
				self.data += data
			#
			else: self.write(data)
		#
	#

	def set_accepted_formats(self, accepted_formats):
	#
		"""
Sets the formats the client accepts.

:param accepted_formats: List of accepted formats

:since: v0.1.01
		"""

		if (isinstance(accepted_formats, list)): self.accepted_formats = accepted_formats
	#

	def set_active(self, is_active = True):
	#
		"""
Constructor __init__(direct_server_fascti)

@since v0.1.00
		"""

		self.active = is_active
		if (not is_active): self.data = None
	#

	def set_streamer(self, streamer):
	#
		"""
Sets the streamer to create response data when requested.

:since: v0.1.01
		"""

		if (hasattr(streamer, "read")):
		#
			self.streamer = streamer

			if (self.stream_mode_supported & direct_abstract_stream_response.STREAM_CALLBACK == direct_abstract_stream_response.STREAM_CALLBACK): self.stream_mode |= direct_abstract_stream_response.STREAM_CALLBACK
			elif (self.supports_streaming()): self.set_stream_mode()
		#
		else: raise RuntimeError("Given streaming object is not supported.", 95)
	#

	def supports_compression(self):
	#
		"""
Returns false if data can not be compressed before being send.

:return: (bool) True if the response can be compressed.
:since:  v0.1.00
		"""

		return False
	#

	def supports_headers(self):
	#
		"""
Returns false if headers are not supported.

:return: (bool) True if the response contain headers.
:since:  v0.1.00
		"""

		return False
	#

	def supports_streaming(self):
	#
		"""
Returns false if responses can not be streamed.

:return: (bool) True if streaming is supported.
:since:  v0.1.00
		"""

		return False
	#

	def write(self):
	#
		"""
Writes the given data.

:access: protected
:since:  v0.1.00
		"""

		raise RuntimeError("Not implemented", 38)
	#
#

##j## EOF