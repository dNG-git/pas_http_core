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

from dNG.data.settings import Settings
from dNG.runtime.io_exception import IOException

from .abstract_http_cgi_request import AbstractHttpCgiRequest
from .http_wsgi1_stream_response import HttpWsgi1StreamResponse

class HttpWsgi1Request(AbstractHttpCgiRequest):
    """
"HttpWsgi1Request" takes a WSGI environment and the start response callback.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self, wsgi_env, wsgi_header_response):
        """
Constructor __init__(HttpWsgi1Request)

:param wsgi_env: WSGI environment
:param wsgi_header_response: WSGI header response callback

:since: v0.2.00
        """

        # pylint: disable=broad-except

        if ("wsgi.version" not in wsgi_env or (wsgi_env['wsgi.version'] not in ( ( 1, 0 ), ( 1, 1 ) ))): raise IOException("WSGI protocol unsupported")

        AbstractHttpCgiRequest.__init__(self)

        self._stream_response = None
        """
The WSGI stream response instance
        """

        self._handle_wsgi_request(wsgi_env, wsgi_header_response)
    #

    def __iter__(self):
        """
python.org: Return an iterator object.

:return: (object) Iterator object
:since:  v0.2.00
        """

        return iter(self._stream_response)
    #

    def _handle_wsgi_request(self, wsgi_env, wsgi_header_response):
        """
Handles a WSGI compliant resource request.

:param wsgi_env: WSGI environment
:param wsgi_header_response: WSGI header response callback

:since: v0.2.00
        """

        self.server_host = Settings.get("pas_http_server_forced_hostname")
        self.server_port = Settings.get("pas_http_server_forced_port")

        self._handle_host_definition_headers(wsgi_env, [ "HTTP_HOST" ])

        if (self.server_host is None):
            self.server_host = Settings.get("pas_http_server_preferred_hostname")
            if (self.server_port is None): self.server_port = Settings.get("pas_http_server_preferred_port")
        #

        self._handle_cgi_headers(wsgi_env)
        self._handle_remote_address_headers(wsgi_env)
        self._rewrite_client_ipv4_in_ipv6_address()

        wsgi_file_wrapper = wsgi_env.get("wsgi.file_wrapper")
        self._stream_response = HttpWsgi1StreamResponse(wsgi_header_response, wsgi_file_wrapper)

        try:
            re_object = HttpWsgi1Request.RE_SERVER_PROTOCOL_VERSION.match(wsgi_env.get("SERVER_PROTOCOL", ""))
            if (re_object is not None): self._stream_response.set_http_version(re_object.group(1))

            self.body_fp = wsgi_env['wsgi.input']

            scheme_header = Settings.get("pas_http_server_scheme_header", "")
            self.server_scheme = (wsgi_env['wsgi.url_scheme'] if (scheme_header == "") else wsgi_env.get(scheme_header.upper().replace("-", "_")))

            if (self.script_path_name is None): self.script_path_name = ""

            if (not (self.get_header("Upgrade") is not None
                     and self._handle_upgrade(self.virtual_path_name, self._stream_response)
                    )
               ): self.execute()
        except Exception as handled_exception:
            if (self.log_handler is not None): self.log_handler.error(handled_exception, "pas_http_core")

            # Died before output
            if (not self._stream_response.are_headers_sent()):
                self._stream_response.set_header("HTTP", "HTTP/2.0 500 Internal Server Error", True)
                self._stream_response.send_data("Internal Server Error")
            #
        #
    #

    def _init_stream_response(self):
        """
Initializes the matching stream response instance.

:return: (object) Stream response object
:since:  v0.2.00
        """

        return self._stream_response
    #
#
