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

try: from collections.abc import Mapping, Sequence
except ImportError: from collections import Mapping, Sequence

from dNG.data.binary import Binary
from dNG.data.json_resource import JsonResource
from dNG.data.text.l10n import L10n
from dNG.runtime.value_exception import ValueException

from .abstract_http_response import AbstractHttpResponse

class HttpJsonResponse(AbstractHttpResponse):
    """
The following class implements the response object for JSON data.

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
Constructor __init__(HttpJsonResponse)

:since: v1.0.0
        """

        AbstractHttpResponse.__init__(self)

        self.supported_features['dict_result_data'] = True
    #

    @property
    def data(self):
        """
Returns buffered data to be transmitted.

:return: (bytes) Data to be send
:since:  v1.0.0
        """

        return Binary.bytes(JsonResource().data_to_json(self.result))
    #

    @property
    def result(self):
        """
Sets the response result to be send JSON encoded.

:param result: Result data

:since: v1.0.0
        """

        return ({ } if (self.raw_data is None) else self.raw_data)
    #

    @result.setter
    def result(self, result):
        """
Sets the response result to be send JSON encoded.

:param result: Result data

:since: v1.0.0
        """

        if ((not isinstance(result, Mapping)) and (not isinstance(result, Sequence))): raise ValueException("Result data type given is invalid")
        self.raw_data = result
    #

    def _prepare_error_response(self):
        """
Prepares an error response.

:since: v1.0.0
        """

        errors = self.errors
        self.reset()

        if (not self.are_headers_sent):
            self.init(False, True)

            header = self.get_header("HTTP", True)
            if (header is None): self.set_header("HTTP", "HTTP/2.0 500 Internal Server Error", True)
        #

        self.result = ({ "error": { "title": L10n.get("core_title_error"),
                                    "message": (L10n.get("errors_core_unknown_error")
                                                if (header is None) else
                                                header
                                               )
                                  }
                       }
                       if (errors is None) else
                       { "error": ({ "messages": errors }
                                   if (len(errors) > 1) else
                                   errors[0]
                                  )
                       }
                      )
    #

    def send(self):
        """
Sends the prepared response.

:since: v1.0.0
        """

        if (self.errors is not None): self._prepare_error_response()

        if (self.raw_data is not None or self.stream_response.is_streamer_set):
            if (not self.initialized): self.init()

            if (self.content_type is None):
                self.content_type = "application/json; charset={0}".format(self.charset)
            #

            self.send_headers()
            AbstractHttpResponse.send(self)
        else:
            self._prepare_error_response()
            self.send()
        #
    #
#
