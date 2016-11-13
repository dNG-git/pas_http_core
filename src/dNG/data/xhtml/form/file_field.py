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

from dNG.data.http.request_body.uploaded_file import UploadedFile
from dNG.data.xhtml.formatting import Formatting

from .abstract_field import AbstractField
from .placeholder_mixin import PlaceholderMixin

class FileField(PlaceholderMixin, AbstractField):
    """
"FileField" provides a file input field.

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
Constructor __init__(FileField)

:param name: Form field name

:since: v0.2.00
        """

        AbstractField.__init__(self, name)
        PlaceholderMixin.__init__(self)
    #

    def _check(self):
        """
Executes checks if the field value is valid.

:return: (bool) True if all checks are passed
:since:  v0.2.00
        """

        _return = AbstractField._check(self)
        if (_return): _return = self._check_file_size()

        return _return
    #

    def _check_file_size(self):
        """
Checks the file size of value.

:return: (bool) True if all checks are passed
:since:  v0.2.00
        """

        data_size = (self.value.get_size() if (isinstance(self.value, UploadedFile)) else -1)
        error_data = None

        if (self.required and data_size < 0): error_data = "required_element"

        if (error_data is None and data_size > -1):
            if (self.limit_min is not None and self.limit_min > data_size): error_data = ( "file_size_min", str(self.limit_min) )
            if (self.limit_max is not None and self.limit_max < data_size): error_data = ( "file_size_max", str(self.limit_max) )
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

        return "file"
    #

    def render(self):
        """
Renders the given field.

:return: (str) Valid XHTML form field definition
:since:  v0.2.00
        """

        context = { "type": Formatting.escape(self.get_type()),
                    "id": "pas_{0}".format(Formatting.escape(self.get_id())),
                    "name": Formatting.escape(self.name),
                    "title": Formatting.escape(self.get_title()),
                    "placeholder": Formatting.escape(self.get_placeholder()),
                    "required": self.required,
                    "error_message": ("" if (self.error_data is None) else Formatting.escape(self.get_error_message()))
                  }

        if (self.size == FileField.SIZE_SMALL):
            context['size'] = 10
            context['size_percentage'] = "30%"
        elif (self.size == FileField.SIZE_LARGE):
            context['size'] = 26
            context['size_percentage'] = "80%"
        else:
            context['size'] = 18
            context['size_percentage'] = "55%"
        #

        if (self.limit_max is not None): context['max_file_size'] = self.limit_max
        if (self.limit_min is not None): context['min_file_size'] = self.limit_min

        return self._render_oset_file("core/form/file", context)
    #
#
