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

from .abstract_http_request import AbstractHttpRequest
from .abstract_inner_http_request import AbstractInnerHttpRequest

class PredefinedHttpRequest(AbstractInnerHttpRequest):
    """
"PredefinedHttpRequest" implements predefined HTTP requests.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self):
        """
Constructor __init__(PredefinedHttpRequest)

:since: v1.0.0
        """

        AbstractInnerHttpRequest.__init__(self)

        self.supported_features['query_string'] = True
    #

    @AbstractInnerHttpRequest.output_handler.setter
    def output_handler(self, output_handler):
        """
Sets the output format.

:param output_handler: (str) Output format

:since: v1.0.0
        """

        self._output_handler = output_handler
    #

    def set_query_string(self, query_string):
        """
Sets all parameters defined in the given URI request string.

:param query_string: URL query string

:since: v1.0.0
        """

        parameters = AbstractHttpRequest.parse_friendly_query_string(query_string)

        if ("a" in parameters): self.action = AbstractHttpRequest.filter_parameter_word(parameters['a'])
        if ("m" in parameters): self.module_package = AbstractHttpRequest.filter_parameter_word(parameters['m'])
        if ("s" in parameters): self.service_package_and_module = AbstractHttpRequest.filter_parameter_service(parameters['s'])

        self.parameters = parameters

        if ("ohandler" in parameters
            and len(parameters['ohandler']) > 0
        ): self.output_handler = AbstractHttpRequest.filter_parameter_word(parameters['ohandler'])
    #
#
