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

from dNG.data.text.input_filter import InputFilter

from .text_field import TextField

class EMailField(TextField):
    """
"EMailField" provides an e-mail input field.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def _check(self):
        """
Executes checks if the field value is valid.

:return: (bool) True if all checks are passed
:since:  v0.2.00
        """

        _return = TextField._check(self)
        if (_return): _return = self._check_format()

        return _return
    #

    def _check_format(self):
        """
Checks if the field value has the expected format.

:return: (bool) True if all checks are passed
:since:  v0.2.00
        """

        error_data = None

        if (len(self.value) > 0 and InputFilter.filter_email_address(self.value) == ""):
            error_data = "format_invalid"
        #

        if (error_data is not None): self.error_data = error_data
        return (error_data is None)
    #

    def get_type(self):
        """
Returns the field type.

:return: (str) Field type
:since:  v0.2.00
        """

        return "email"
    #
#
