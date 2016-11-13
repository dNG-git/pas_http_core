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

from dNG.data.xhtml.formatting import Formatting
from dNG.data.xml_parser import XmlParser

from .abstract_field import AbstractField

class HiddenField(AbstractField):
    """
"HiddenField" provides a hidden input field.

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

        _return = AbstractField._check(self)
        if (_return): _return = (self.value is not None)

        return _return
    #

    def _get_content(self):
        """
Returns the field content.

:return: (str) Field content
:since:  v0.2.00
        """

        return Formatting.escape(AbstractField._get_content(self))
    #

    def get_type(self):
        """
Returns the field type.

:return: (str) Field type
:since:  v0.2.00
        """

        return "hidden"
    #

    def render(self):
        """
Renders the given field.

:return: (str) Valid XHTML form field definition
:since:  v0.2.00
        """

        hidden_attributes = { "type": "hidden",
                              "name": Formatting.escape(self.name),
                              "value": self._get_content()
                            }

        return XmlParser().dict_to_xml_item_encoder({ "tag": "input",
                                                      "attributes": hidden_attributes
                                                    },
                                                    strict_standard_mode = False
                                                   )
    #
#
