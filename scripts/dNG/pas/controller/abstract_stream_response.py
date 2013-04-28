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

from dNG.pas.pythonback import direct_bytes

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
			if (self.data != None): self.write(self.data)
			self.active = False
		#
	#

	def is_active(self):
	#
		"""
Constructor __init__(direct_server_fascti)

@since v0.1.00
		"""

		return self.active
	#

	def send_data(self, data):
	#
		"""
Constructor __init__(direct_server_fascti)

@since v0.1.00
		"""

		data = direct_bytes(data)

		if (self.active):
		#
			if (self.stream_mode == direct_abstract_stream_response.STREAM_NONE):
			#
				if (self.data == None): self.data = direct_bytes("")
				self.data += data
			#
			else: self.write(data)
		#
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