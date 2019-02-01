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

import re

from dNG.controller.abstract_http_mixin import AbstractHttpMixin as AbstractHttpInstance
from dNG.data.http.translatable_exception import TranslatableException

from .abstract import Abstract

class Http(Abstract):
    """
"Http" provides methods for HTTP module and service based implementations.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def _get_executable_method_name(self):
        """
Returns the executable method name used for the given request and response
instances.

:return: (str) Method name to be executed
:since:  v1.0.0
        """

        if (not isinstance(self.request, AbstractHttpInstance)):
            error_value = "Request type '{0!r}' is not supported".format(self.request)
            raise TranslatableException("core_unsupported_command", value = error_value)
        #

        re_object = re.compile("\\W+")

        action_name = re_object.sub("_", self.request.action)
        request_type = (re_object.sub("_", self.request.type.lower()) if self.request.is_supported("type") else "execute")

        _return = "{0}_{1}".format(request_type, action_name)
        if (request_type == "head" and (not hasattr(self, _return))): _return = "get_{0}".format(action_name)
        if (not hasattr(self, _return)): _return = "execute_{0}".format(action_name)

        if (not hasattr(self, _return)): self._raise_executable_not_found(action_name)

        return _return
    #

    def _raise_executable_not_found(self, method_name):
        """
Raises the executable method not found error.

:param method_name: Executable method name expected

:since: v1.0.0
        """

        if (self.response.is_supported("headers")): self.response.set_header("HTTP", "HTTP/2.0 404 Not Found", True)

        error_value = "Identified action method '{0}' is not supported".format(method_name)
        raise TranslatableException("core_unsupported_command", value = error_value)
    #
#
