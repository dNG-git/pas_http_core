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

from .translatable_error import TranslatableError

class TranslatableException(TranslatableError):
#
	"""
This exception takes a translatable messages for critical errors.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, l10n_id, http_code = 500, value = None, _exception = None):
	#
		"""
Constructor __init__(TranslatableException)

:param l10n_id: L10n translatable key (prefixed with "errors_")
:param http_code: HTTP code
:param value: Exception message value
:param _exception: Inner exception

:since: v0.1.01
		"""

		TranslatableError.__init__(self, l10n_id, http_code, value, _exception)
	#
#

##j## EOF