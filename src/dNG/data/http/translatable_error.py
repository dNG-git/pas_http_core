# -*- coding: utf-8 -*-

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

from dNG.data.translatable_exception import TranslatableException

class TranslatableError(TranslatableException):
    """
This exception is used for non-critical, translatable error messages.
Non-critical errors are usually expected like wrong entity IDs.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self, l10n_id, http_code = 200, value = None, _exception = None):
        """
Constructor __init__(TranslatableError)

:param l10n_id: L10n translatable key (prefixed with "errors_")
:param http_code: HTTP code
:param value: Exception message value
:param _exception: Inner exception

:since: v1.0.0
        """

        TranslatableException.__init__(self, l10n_id, value, _exception)

        self._http_code = http_code
        """
HTTP error code
        """
        self._http_message = None
        """
HTTP error message
        """
    #

    @property
    def http_code(self):
        """
Return the HTTP error code.

:return: (int) HTTP error code
:since:  v1.0.0
        """

        return self._http_code
    #

    @property
    def http_message(self):
        """
Returns the HTTP error message.

:return: (str) HTTP error message
:since:  v1.0.0
        """

        return self._http_message
    #
#
