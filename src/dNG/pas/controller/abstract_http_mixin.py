# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.controller.AbstractHttpMixin
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

from dNG.pas.data.translatable_exception import TranslatableException
from dNG.pas.data.http.request_headers_mixin import RequestHeadersMixin
from .abstract_inner_request import AbstractInnerRequest
from .abstract_response import AbstractResponse

class AbstractHttpMixin(RequestHeadersMixin):
#
	"""
"AbstractHttpMixin" is used to support common methods for HTTP request
instances.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(AbstractInnerHttpRequest)

:since: v0.1.01
		"""

		RequestHeadersMixin.__init__(self)

		self.compression_formats = None
		"""
Compression formats the client accepts
		"""
		self.lang = ""
		"""
User requested language
		"""
		self.lang_default = ""
		"""
Request based default language
		"""
		self.parent_request = None
		"""
Executable parent request
		"""
		self.type = None
		"""
Request type
		"""

		self.supported_features['compression'] = self._supports_compression
		self.supported_features['headers'] = self._supports_headers
		self.supported_features['type'] = self._supports_type
	#

	def get_lang(self):
	#
		"""
Returns the requested or supported language.

:return: (str) Language identifier
:since:  v0.1.00
		"""

		return self.lang
	#

	def get_lang_default(self):
	#
		"""
Returns the default language.

:return: (str) Language identifier
:since:  v0.1.00
		"""

		return self.lang_default
	#

	def get_type(self):
	#
		"""
Returns the request type.

:return: (str) Request type
:since:  v0.1.00
		"""

		return self.type
	#

	def redirect(self, request, response = None):
	#
		"""
A request redirect executes the given new request as if it has been
requested by the client. It will reset the response and its cached values.

:param response: Waiting response object

:since: v0.1.01
		"""

		if (isinstance(request, AbstractInnerRequest)):
		#
			parent_request = (self if (self.parent_request == None) else self.parent_request)

			request.init(self)
			if (isinstance(request, AbstractHttpMixin)): request._set_parent_request(parent_request)

			if (not isinstance(response, AbstractResponse)): response = AbstractResponse.get_instance()

			parent_request._execute(request, response)
		#
		else: raise TranslatableException("core_unsupported_command")
	#

	def _set_parent_request(self, parent_request):
	#
		"""
Sets the parent request used for execution of chained requests.

:param parent_request: Executable parent request

:since: v0.1.01
		"""

		self.parent_request = parent_request
	#

	def _supports_compression(self):
	#
		"""
Returns false if supported compression formats can not be identified.

:return: (bool) True if compression formats are identified.
:since:  v0.1.01
		"""

		return (False if (self.compression_formats == None) else True)
	#

	def _supports_headers(self):
	#
		"""
Sets false if the script name is not needed for execution.

:return: (bool) True if the request contains headers.
:since:  v0.1.00
		"""

		return (False if (self.headers == None) else True)
	#

	def _supports_type(self):
	#
		"""
Returns true if the request type is known.

:return: (bool) True if request type is known
:since:  v0.1.00
		"""

		return (self.get_type() != None)
	#
#

##j## EOF