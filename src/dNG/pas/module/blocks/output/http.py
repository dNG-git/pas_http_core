# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.module.blocks.output.Http
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

# pylint: disable=import-error,no-name-in-module

try: from http.client import responses
except ImportError: from httplib import responses

from dNG.pas.data.text.input_filter import InputFilter
from dNG.pas.data.text.l10n import L10n
from .module import Module

class Http(Module):
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
Constructor __init__(Http)

:since: v0.1.00
		"""

		Module.__init__(self)

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

		code = InputFilter.filter_int(self.request.get_dsd("code", "500"))

		if (L10n.is_defined("errors_pas_http_core_{0:d}".format(code))):
		#
			if (self.response.is_supported("headers")): self.response.set_header("HTTP/1.1", ("HTTP/1.1 {0:d} {1}".format(code, self.error_messages[code]) if (code in self.error_messages) else "HTTP/1.1 500 Internal Server Error"), True)
			self.response.handle_critical_error("pas_http_core_{0:d}".format(code))
		#
		else:
		#
			if (self.response.is_supported("headers")): self.response.set_header("HTTP/1.1", "HTTP/1.1 500 Internal Server Error", True)
			self.response.handle_critical_error("core_unknown_error")
		#
	#
#

##j## EOF