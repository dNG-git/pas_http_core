# -*- coding: utf-8 -*-
##j## BOF

"""
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
"""

from .abstract_http_mixin import AbstractHttpMixin
from .abstract_inner_request import AbstractInnerRequest

class AbstractInnerHttpRequest(AbstractInnerRequest, AbstractHttpMixin):
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
		AbstractHttpMixin.__init__(self)

		self.accepted_formats = None
		"""
Formats the client accepts
		"""
		self.compression_formats = None
		"""
Compression formats the client accepts
		"""
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

		if (request.is_supported("accepted_formats")): self.accepted_formats = request.get_accepted_formats()
		if (request.is_supported("compression")): self.compression_formats = request.get_compression_formats()
		if (request.is_supported("headers")): self.headers = request.get_headers()
		self.lang = request.get_lang()
		self.lang_default = request.get_lang_default()
		if (self.session == None): self.session = request.get_session()
		if (request.is_supported("type")): self.type = request.get_type()

		self.set_script_pathname(request.get_script_pathname())
	#

	def _supports_accepted_formats(self):
	#
		"""
Returns false if accepted formats can not be identified.

:return: (bool) True if accepted formats are identified.
:since:  v0.1.01
		"""

		return (self.accepted_formats != None)
	#

	def _supports_compression(self):
	#
		"""
Returns false if supported compression formats can not be identified.

:return: (bool) True if compression formats are identified.
:since:  v0.1.01
		"""

		return (self.compression_formats != None)
	#
#

##j## EOF