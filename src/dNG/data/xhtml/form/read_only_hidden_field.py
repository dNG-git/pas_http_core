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

from .hidden_field import HiddenField
from .read_only_field_mixin import ReadOnlyFieldMixin

class ReadOnlyHiddenField(HiddenField, ReadOnlyFieldMixin):
    """
"ReadOnlyHiddenField" provides a non-replaceable hidden input field.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self, name = None):
        """
Constructor __init__(ReadOnlyHiddenField)

:param name: Form field name

:since: v0.2.00
        """

        HiddenField.__init__(self, name)
        ReadOnlyFieldMixin.__init__(self)
    #
#
