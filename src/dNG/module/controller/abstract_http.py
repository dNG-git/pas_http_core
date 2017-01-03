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

from dNG.controller.abstract_request import AbstractRequest
from dNG.controller.abstract_response import AbstractResponse
from dNG.data.http.translatable_exception import TranslatableException

from .abstract import Abstract as AbstractController

class AbstractHttp(AbstractController):
    """
"AbstractHttp" provides methods for HTTP module and service implementations.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self):
        """
Constructor __init__(AbstractHttp)

:since: v0.2.00
        """

        AbstractController.__init__(self)

        self.action = None
        """
Requested action
        """
        self.action_result = None
        """
Action result
        """
        self.context = None
        """
Secondary action context
        """
        self.primary_action = True
        """
True if action is the primary requested one
        """
    #

    def execute(self):
        """
Execute the requested action.

:since: v0.2.00
        """

        method_name = "execute_{0}".format(re.sub("\\W", "_", self.action))
        return self._execute(method_name)
    #

    def _execute(self, method_name):
        """
Execute the given action method.

:param method_name: Method to be executed

:since: v0.2.00
        """

        if (self.log_handler is not None): self.log_handler.debug("{0!r} identified action '{1}'", self, self.action, context = "pas_http_core")

        if (hasattr(self, method_name)):
            method = getattr(self, method_name)
            method()
        else: self._raise_executable_not_found()

        return ("" if (self.action_result is None) else self.action_result)
    #

    def init(self, request, response):
        """
Initializes the controller from the given request and response.

:param request: Request object
:param response: Response object

:since: v0.2.00
        """

        AbstractController.init(self, request, response)
        self.action = request.get_action()
    #

    def _is_primary_action(self):
        """
Returns true if the action is the primary requested one.

:return: (bool) True if primary action
:since:  v0.2.00
        """

        return self.primary_action
    #

    def _raise_executable_not_found(self):
        """
Raises the executable method not found error.

:since: v0.2.00
        """

        if (self.primary_action and self.response.is_supported("headers")): self.response.set_header("HTTP", "HTTP/2.0 404 Not Found", True)
        raise TranslatableException("core_unsupported_command", value = "Identified action '{0}' is not supported".format(self.action))
    #

    def set_action(self, action, context = None):
        """
Sets an block action for execution.

:param action: Action requested
:param context: Action context

:since: v0.2.00
        """

        self.action = action
        self.context = context
        self.primary_action = False

        if (self.request is None): self.request = AbstractRequest.get_instance()
        if (self.response is None): self.response = AbstractResponse.get_instance()
    #

    def set_action_result(self, result):
        """
Sets an action result.

:param result: Result to be returned for the action

:since: v0.2.00
        """

        self.action_result = result
    #
#
