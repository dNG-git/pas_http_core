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

# pylint: disable=import-error,no-name-in-module

import re

try: from http.client import responses
except ImportError: from httplib import responses

from dNG.controller.abstract_inner_request import AbstractInnerRequest
from dNG.data.http.translatable_exception import TranslatableException
from dNG.data.text.input_filter import InputFilter
from dNG.data.text.l10n import L10n
from dNG.data.xhtml.link import Link
from dNG.module.http import Http as HttpModule

class Http(HttpModule):
    """
Service for "/output/http"

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
Constructor __init__(Http)

:since: v1.0.0
        """

        HttpModule.__init__(self)

        self.error_messages = responses
        """
Extendable list of standard HTTP error codes
        """
    #

    def execute_done(self):
        """
Action for "done"

:since: v1.0.0
        """

        if (not isinstance(self.request, AbstractInnerRequest)): raise TranslatableException("pas_http_core_400", 400)

        parameters_chained = self.request.parameters_chained
        is_parameters_chained_valid = ("title" in parameters_chained and "message" in parameters_chained)

        if (not is_parameters_chained_valid): raise TranslatableException("pas_http_core_500")

        l10n = (L10n.get_instance(parameters_chained['lang'])
                if ("lang" in parameters_chained) else
                L10n.get_instance()
               )

        L10n.init("core", l10n.lang)

        content = { "title": parameters_chained['title'],
                    "title_task_done": l10n.get("core_title_task_done"),
                    "message": parameters_chained['message']
                  }

        if ("target_iline" in parameters_chained):
            content['link_title'] = l10n.get("core_continue")

            target_iline = re.sub("\\_\\_\\w+\\_\\_", "", parameters_chained['target_iline'])
            content['link_url'] = Link().build_url(Link.TYPE_RELATIVE_URL, { "__query__": target_iline })
        #

        self.response.init()
        self.response.page_title = parameters_chained['title']

        self.response.add_oset_content("core.done", content)
    #

    def execute_error(self):
        """
Action for "error"

:since: v1.0.0
        """

        code = InputFilter.filter_int(self.request.get_parameter("code", "500"))

        if (L10n.is_defined("errors_pas_http_core_{0:d}".format(code))):
            if (self.response.is_supported("headers")):
                self.response.set_header("HTTP",
                                         ("HTTP/2.0 {0:d} {1}".format(code, self.error_messages[code])
                                          if (code in self.error_messages) else
                                          "HTTP/2.0 500 Internal Server Error"
                                         ),
                                         True
                                        )
            #

            self.response.handle_error("pas_http_core_{0:d}".format(code))
        else:
            if (self.response.is_supported("headers")): self.response.set_header("HTTP", "HTTP/2.0 500 Internal Server Error", True)
            self.response.handle_critical_error("core_unknown_error")
        #
    #
#
