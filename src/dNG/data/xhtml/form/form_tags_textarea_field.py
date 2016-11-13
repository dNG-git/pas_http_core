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

from .textarea_field import TextareaField

class FormTagsTextareaField(TextareaField):
    """
"FormTagsTextareaField" provides a textarea field with FormTags.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def _get_content(self):
        """
Returns the field content.

:return: (str) Field content
:since:  v0.2.00
        """

        _return = TextareaField._get_content(self)

        _return = _return.replace("[", "&#91;")
        _return = _return.replace("]", "&#93;")

        return _return
    #
#
