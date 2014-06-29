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

from dNG.pas.data.translatable_exception import TranslatableException

class TranslatableError(TranslatableException):
#
	"""
This exception is used for non-critical, translatable error messages.
Non-critical errors are usually expected like wrong entity IDs.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, l10n_id, http_code = 200, value = None, _exception = None):
	#
		"""
Constructor __init__(TranslatableError)

:param l10n_id: L10n translatable key (prefixed with "errors_")
:param http_code: HTTP code
:param value: Exception message value
:param _exception: Inner exception

:since: v0.1.01
		"""

		TranslatableException.__init__(self, l10n_id, value, _exception)

		self.http_code = http_code
		"""
HTTP error code
		"""
	#

	def get_http_code(self):
	#
		"""
Return the HTTP error code.

:return: (int) HTTP error code
:since:  v0.1.01
		"""

		return self.http_code
	#
#

##j## EOF