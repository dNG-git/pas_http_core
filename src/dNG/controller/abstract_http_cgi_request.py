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
from os import path

try: from collections.abc import Mapping
except ImportError: from collections import Mapping

from dNG.data.binary import Binary
from dNG.data.http.virtual_route import VirtualRoute
from dNG.data.text.input_filter import InputFilter
from dNG.data.settings import Settings

from .abstract_http_request import AbstractHttpRequest
from .abstract_inner_request import AbstractInnerRequest

class AbstractHttpCgiRequest(AbstractHttpRequest):
    """
"AbstractHttpCgiRequest" takes a WSGI environment and the start response
callback.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    RE_SERVER_PROTOCOL_VERSION = re.compile("HTTP/(\d\\.\d)")
    """
RegEx to extract the HTTP protocol version in use
    """

    def __init__(self):
        """
Constructor __init__(AbstractHttpCgiRequest)

:since: v1.0.0
        """

        AbstractHttpRequest.__init__(self)

        self._virtual_path_name = ""
        """
Request path after the script
        """
    #

    @AbstractHttpRequest.script_path_name.setter
    def script_path_name(self, script_path_name):
        """
Sets the script path and name of the request.

:param script_path_name: Script path and name

:since: v1.0.0
        """

        AbstractHttpRequest.script_path_name.fset(self, script_path_name)
        self._script_name = path.basename(script_path_name)
    #

    def execute(self):
        """
Executes the incoming request.

:since: v1.0.0
        """

        self._init_request()

        script_path_name = self.script_path_name
        virtual_route_config = VirtualRoute.get_config(self._virtual_path_name)

        if (virtual_route_config is None and self._virtual_path_name == "" and script_path_name != ""):
            virtual_route_config = VirtualRoute.get_config(script_path_name)
            virtual_path_name = script_path_name
        else: virtual_path_name = self._virtual_path_name

        inner_request = self._parse_virtual_route_config(virtual_route_config, virtual_path_name)

        if (isinstance(inner_request, AbstractInnerRequest)):
            self.inner_request = inner_request
            self._path = virtual_path_name
        else: self.path = virtual_path_name

        AbstractHttpRequest.execute(self)
    #

    def _handle_cgi_headers(self, cgi_env):
        """
Handles CGI environment compliant headers.

:param cgi_env: CGI environment dictionary

:since: v1.0.0
        """

        for key in cgi_env:
            if (cgi_env[key] != ""):
                cgi_env_value = Binary.str(cgi_env[key])

                if (key[:5] == "HTTP_"):
                    header_name = key[5:].replace("_", "-").lower()

                    if (header_name not in ( "content-length",
                                             "content-type"
                                           )
                       ): self.set_header(header_name, cgi_env_value)
                elif (key == "CONTENT_LENGTH" or key == "CONTENT_TYPE"): self.set_header(key.replace("_", "-"), cgi_env_value)
                elif (key == "PATH_INFO"): self._virtual_path_name = cgi_env.get("SCRIPT_NAME", "") + cgi_env_value
                elif (key == "QUERY_STRING"): self._query_string = cgi_env_value
                elif (key == "REMOTE_ADDR" and self.client_host is None): self._client_host = cgi_env_value
                elif (key == "REMOTE_HOST"): self._client_host = cgi_env_value
                elif (key == "REMOTE_PORT"): self._client_port = cgi_env_value
                elif (key == "REQUEST_METHOD"): self._type = cgi_env_value.upper()
                elif (key == "REQUEST_URI"):
                    request_data = cgi_env_value.split("?", 1)

                    if (self._virtual_path_name == ""): self._virtual_path_name = request_data[0]

                    if (self._query_string is None
                        and len(request_data) > 1
                       ): self._query_string = request_data[1]
                elif (key == "SCRIPT_NAME"): self.script_path_name = cgi_env_value
                elif (self.server_host is None and key == "SERVER_NAME"): self._server_host = cgi_env_value
                elif (self.server_port is None and key == "SERVER_PORT"): self._server_port = int(cgi_env_value)
            #
        #
    #

    def _handle_host_definition_headers(self, headers, default_host_definition_headers):
        """
Handles headers containing the server host name and port.

:param headers: Headers to search
:param default_host_definition_headers: Default list of HOST header names

:since: v1.0.0
        """

        host_definition_headers = Settings.get("pas_http_server_host_definition_headers",
                                               default_host_definition_headers
                                              )

        for host_definition_header in host_definition_headers:
            if (host_definition_header in headers):
                host_definition_header = host_definition_header.upper()

                host_parts = headers[host_definition_header].rsplit(":", 2)

                if (len(host_parts) < 2 or host_parts[1][-1:] == "]"): self._server_host = headers[host_definition_header]
                else:
                    self._server_host = host_parts[0]
                    if (self.server_port is None): self._server_port = int(host_parts[1])
                #

                del(headers[host_definition_header])
                break
            #
        #
    #

    def _handle_remote_address_headers(self, headers):
        """
Handles headers containing the remote host name and port.

:since: v1.0.0
        """

        remote_address_headers = Settings.get("pas_http_server_remote_address_headers", [ ])

        for remote_address_header in remote_address_headers:
            remote_address_header = remote_address_header.upper()

            remote_address_value = (headers[remote_address_header].strip()
                                    if (remote_address_header in headers
                                        and headers[remote_address_header] is not None
                                       ) else
                                    ""
                                   )

            if (remote_address_value != ""):
                self.client_host = remote_address_value.split(",")[0]
                self.client_port = None

                break
            #
        #
    #

    def _read_parameters(self):
        """
Reads and returns the request parameters from the incoming request.

:return: (dict) Request parameters
:since:  v1.0.0
        """

        _return = AbstractHttpRequest._read_parameters(self)

        request_body = self.prepare_body_instance(content_type_expected = "application/x-www-form-urlencoded")
        if (request_body is None): request_body = self.prepare_body_instance(content_type_expected = "multipart/form-data")

        if (isinstance(request_body, Mapping)):
            for key in request_body: _return[InputFilter.filter_control_chars(key)] = request_body[key]
        #

        return _return
    #

    def _rewrite_client_ipv4_in_ipv6_address(self):
        """
Extracts a client host IPv4 address represented as an IPv6 address.

:since: v1.0.0
        """

        re_result = (None if (self.client_host is None) else re.match("^::ffff:(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)$", self.client_host))
        if (re_result is not None): self._client_host = "{0}.{1}.{2}.{3}".format(re_result.group(1), re_result.group(2), re_result.group(3), re_result.group(4))
    #
#
