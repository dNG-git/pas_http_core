# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.module.blocks.output.http
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;user_profile

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

from dNG.pas.data.text.input_filter import direct_input_filter
from dNG.pas.data.text.l10n import direct_l10n
from .module import direct_module

try: from http.client import responses
except ImportError: from httplib import responses

class direct_http(direct_module):
#
	"""
Service for "m=output;s=http"

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
Constructor __init__(direct_http)

@since v0.1.00
		"""

		direct_module.__init__(self)

		self.error_messages = responses
		"""
Extendable list of standard HTTP error codes
		"""
	#

	def execute_error(self):
	#
		"""
Action for "login"

:since: v0.1.00
		"""

		code = direct_input_filter.filter_int(self.request.get_dsd("code", "500"))

		if (direct_l10n.is_defined("pas_http_error_{0:d}".format(code))):
		#
			if (self.response.supports_headers()): self.response.set_header("HTTP/1.1", ("HTTP/1.1 {0:d} {1}".format(code, self.error_messages[code]) if (code in self.error_messages) else "HTTP/1.1 500 Internal Server Error"), True)
			self.response.handle_critical_error("pas_http_error_{0:d}".format(code))
		#
		else:
		#
			if (self.response.supports_headers()): self.response.set_header("HTTP/1.1", "HTTP/1.1 500 Internal Server Error", True)
			self.response.handle_critical_error("core_unknown_error")
		#
	#
#

##j## EOF