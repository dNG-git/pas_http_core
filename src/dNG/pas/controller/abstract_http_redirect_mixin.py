# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.controller.AbstractHttpRequest
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
from .abstract_inner_request import AbstractInnerRequest
from .abstract_response import AbstractResponse

class AbstractHttpRedirectMixin(object):
#
	"""
"AbstractHttpRedirectMixin" is used to chain execution of requests.

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

		self.parent_request = None
		"""
Executable parent request
		"""
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
			if (isinstance(request, AbstractHttpRedirectMixin)): request._set_parent_request(parent_request)

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
#

##j## EOF