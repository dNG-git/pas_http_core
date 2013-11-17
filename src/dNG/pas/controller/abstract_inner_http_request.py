# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.controller.AbstractInnerHttpRequest
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

from dNG.pas.data.http.request_headers_mixin import RequestHeadersMixin
from .abstract_inner_request import AbstractInnerRequest

class AbstractInnerHttpRequest(AbstractInnerRequest, RequestHeadersMixin):
#
	"""
This abstract class contains HTTP methods for inner requests.

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
Constructor __init__(AbstractInnerHttpRequest)

:since: v0.1.00
		"""

		AbstractInnerRequest.__init__(self)
		RequestHeadersMixin.__init__(self)

		self.compression_formats = None
		"""
Compression formats the client accepts
		"""
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

	def init(self, request):
	#
		"""
Initializes default values from the original request.

:param request: (object) Request instance

:since: v0.1.00
		"""

		AbstractInnerRequest.init(self, request)

		if (request.supports_compression()): self.compression_formats = request.get_compression_formats()
		if (request.supports_headers()): self.headers = request.get_headers()
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

	def supports_accepted_formats(self):
	#
		"""
Sets false if accepted formats can not be identified.

:return: (bool) True accepted formats are supported.
:since:  v0.1.00
		"""

		return (False if (self.headers == None) else True)
	#

	def supports_compression(self):
	#
		"""
Returns false if supported compression formats can not be identified.

:return: (bool) True if compression formats are identified.
:since:  v0.1.01
		"""

		return (False if (self.compression_formats == None) else True)
	#

	def supports_headers(self):
	#
		"""
Sets false if the script name is not needed for execution.

:return: (bool) True if the request contains headers.
:since:  v0.1.00
		"""

		return (False if (self.headers == None) else True)
	#

	def supports_listener_data(self):
	#
		"""
Returns false if the server address is unknown.

:return: (bool) True if listener are known.
:since:  v0.1.00
		"""

		return True
	#
#

##j## EOF