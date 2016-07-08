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

from dNG.data.http.translatable_exception import TranslatableException
from dNG.data.text.input_filter import InputFilter
from dNG.module.controller.abstract_http import AbstractHttp as AbstractHttpController
from dNG.runtime.io_exception import IOException

try: from dNG.data.session.implementation import Implementation as _Session
except ImportError: _Session = None

class Session(AbstractHttpController):
#
	"""
Service for "s=session"
The "Form" class implements the form view.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def execute_api_ping(self):
	#
		"""
Action for "api_ping"

:since: v0.2.00
		"""

		if (not self.response.is_supported("dict_result_renderer")): raise IOException("Unsupported response object for action")
		uuid = InputFilter.filter_control_chars(self.request.get_dsd("uuid"))

		session = (self.request.get_session() if (self.request.is_supported("session")) else None)

		if (session is None):
		#
			if (uuid is None or _Session is None): raise TranslatableException("core_unsupported_command", 400)
			session = _Session.load(uuid, False)
		#

		if (session is None): raise TranslatableException("core_access_denied", 403)

		session.save()
		self.response.set_result({ "expires_in": int(session.get_timeout()) })
	#
#

##j## EOF