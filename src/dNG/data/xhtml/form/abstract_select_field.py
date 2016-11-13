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

from dNG.data.binary import Binary
from dNG.data.xhtml.formatting import Formatting

from .abstract_field import AbstractField

class AbstractSelectField(AbstractField):
    """
"AbstractSelectField" provides common methods for a selectbox.

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
Constructor __init__(AbstractSelectField)

:param name: Form field name

:since: v0.2.00
        """

        AbstractField.__init__(self, name)

        self.size = AbstractSelectField.SIZE_SMALL
    #

    def _check(self):
        """
Executes checks if the field value is valid.

:return: (bool) True if all checks are passed
:since:  v0.2.00
        """

        _return = AbstractField._check(self)

        if (_return):
            _return = False

            for choice in self.choices:
                if ("value" in choice and choice['value'] == self.value):
                    _return = True
                    break
                #
            #

            if (not _return): self.error_data = "format_invalid"
        #

        return _return
    #

    def _check_selected_value(self, value):
        """
Check if the given value has been selected.

:param value: Value

:return: (bool) True if selected
:since:  v0.2.00
        """

        return (self.value is not None and self.value == value)
    #

    def _get_render_context(self):
        """
Returns the context used for rendering the given field.

:return: (dict) Renderer context
:since:  v0.2.00
        """

        if (self.size == AbstractSelectField.SIZE_MEDIUM): rows = 4
        elif (self.size == AbstractSelectField.SIZE_LARGE): rows = 8
        else: rows = 1

        return { "id": "pas_{0}".format(Formatting.escape(self.get_id())),
                 "name": Formatting.escape(self.name),
                 "title": Formatting.escape(self.get_title()),
                 "choices": self._get_content(),
                 "rows": rows,
                 "required": self.required,
                 "error_message": ("" if (self.error_data is None) else Formatting.escape(self.get_error_message()))
               }
    #

    def get_type(self):
        """
Returns the field type.

:return: (str) Field type
:since:  v0.2.00
        """

        return "select"
    #

    def get_value(self, _raw_input = False):
        """
Returns the field value given or transmitted.

:param raw_input: True to return the raw (transmitted) value.

:return: (mixed) Field value; None on error
:since:  v0.2.00
        """

        if (_raw_input): _return = self.value
        else: _return = (self.values_selected[0] if (len(self.values_selected) > 0) else None)

        return _return
    #

    def render(self):
        """
Renders the given field.

:return: (str) Valid XHTML form field definition
:since:  v0.2.00
        """

        return self._render_oset_file("core/form/select", self._get_render_context())
    #

    def set_value(self, value):
        """
Sets the field value.

:param value: Field value

:since: v0.2.00
        """

        value = Binary.str(value)

        if (not isinstance(value, str)):
            value = Binary.str(value)
            if (type(value) is not str): value = str(value)
        #

        self.value = value

        self.valid = None
    #
#
