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
from collections import Mapping
from os import path

from dNG.data.http.virtual_config import VirtualConfig
from dNG.data.settings import Settings
from .abstract_http_request import AbstractHttpRequest
from .abstract_inner_request import AbstractInnerRequest

class AbstractHttpCgiRequest(AbstractHttpRequest):
    """
"HttpScgi1Request" takes a WSGI environment and the start response callback.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    RE_SERVER_PROTOCOL_VERSION = re.compile("HTTP/(\d\\.\d)")
    """
RegEx to extract the HTTP protocol version in use
    """

    def __init__(self):
        """
Constructor __init__(HttpScgi1Request)

:since: v0.2.00
        """

        AbstractHttpRequest.__init__(self)

        self.virtual_path_name = ""
        """
Request path after the script
        """
    #

    def execute(self):
        """
Executes the incoming request.

:since: v0.2.00
        """

        self._init_request()

        virtual_config = VirtualConfig.get_config(self.virtual_path_name)

        if (virtual_config is None and self.virtual_path_name != ""):
            virtual_config = VirtualConfig.get_config(self.script_path_name)
            virtual_path_name = self.script_path_name
        else: virtual_path_name = self.virtual_path_name

        inner_request = self._parse_virtual_config(virtual_config, virtual_path_name)
        if (isinstance(inner_request, AbstractInnerRequest)): self.set_inner_request(inner_request)

        AbstractHttpRequest.execute(self)
    #

    def _get_request_parameters(self):
        """
Returns the unparsed request parameters.

:return: (dict) Request parameters
:since:  v0.2.00
        """

        # pylint: disable=broad-except,no-member

        _return = AbstractHttpRequest.parse_iline(self.query_string)

        request_body = self.prepare_body_instance(content_type_expected = "application/x-www-form-urlencoded")
        if (request_body is None): request_body = self.prepare_body_instance(content_type_expected = "multipart/form-data")

        if (isinstance(request_body, Mapping)):
            for key in request_body: _return[key] = request_body[key]
        #

        return _return
    #

    def _handle_cgi_headers(self, cgi_env):
        """
Handles CGI environment compliant headers.

:param cgi_env: CGI environment dictionary

:since: v0.2.00
        """

        for key in cgi_env:
            if (cgi_env[key] != ""):
                if (key[:5] == "HTTP_"):
                    header_name = key[5:].replace("_", "-").upper()

                    if (header_name not in ( "CONTENT-LENGTH",
                                             "CONTENT-TYPE"
                                             )
                        ): self.set_header(header_name, cgi_env[key])
                elif (key == "CONTENT_LENGTH" or key == "CONTENT_TYPE"): self.set_header(key.replace("_", "-"), cgi_env[key])
                elif (key == "PATH_INFO"): self.virtual_path_name = cgi_env.get("SCRIPT_NAME", "") + cgi_env[key]
                elif (key == "QUERY_STRING"): self.query_string = cgi_env[key]
                elif (key == "REMOTE_ADDR" and self.client_host is None): self.client_host = cgi_env[key]
                elif (key == "REMOTE_HOST"): self.client_host = cgi_env[key]
                elif (key == "REMOTE_PORT"): self.client_port = cgi_env[key]
                elif (key == "REQUEST_METHOD"): self.type = cgi_env[key].upper()
                elif (key == "REQUEST_URI"):
                    request_data = cgi_env[key].split("?", 1)

                    if (self.virtual_path_name == ""): self.virtual_path_name = request_data[0]

                    if (self.query_string is None
                        and len(request_data) > 1
                       ): self.query_string = request_data[1]
                elif (key == "SCRIPT_NAME"): self.script_path_name = cgi_env[key]
                elif (self.server_host is None and key == "SERVER_NAME"): self.server_host = cgi_env[key]
                elif (self.server_port is None and key == "SERVER_PORT"): self.server_port = int(cgi_env[key])
            #
        #
    #

    def _handle_host_definition_headers(self, headers, default_host_definition_headers):
        """
Handles headers containing the server host name and port.

:param headers: Headers to search
:param default_host_definition_headers: Default list of HOST header names

:since: v0.2.00
        """

        host_definition_headers = Settings.get("pas_http_server_host_definition_headers",
                                               default_host_definition_headers
                                              )

        for host_definition_header in host_definition_headers:
            if (host_definition_header in headers):
                host_parts = headers[host_definition_header].rsplit(":", 2)

                if (len(host_parts) < 2 or host_parts[1][-1:] == "]"): self.server_host = headers[host_definition_header]
                else:
                    self.server_host = host_parts[0]
                    if (self.server_port is None): self.server_port = int(host_parts[1])
                #

                del(headers[host_definition_header])
                break
            #
        #
    #

    def _handle_remote_address_headers(self, headers):
        """
Handles headers containing the remote host name and port.

:since: v0.2.00
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

    def _init_request(self):
        """
Do preparations for request handling.

:since: v0.2.00
        """

        self.script_name = path.basename(self.script_path_name)

        AbstractHttpRequest._init_request(self)
    #

    def _rewrite_client_ipv4_in_ipv6_address(self):
        """
Extracts a client host IPv4 address represented as an IPv6 address.

:since: v0.2.00
        """

        re_result = (None if (self.client_host is None) else re.match("^::ffff:(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)$", self.client_host))
        if (re_result is not None): self.client_host = "{0}.{1}.{2}.{3}".format(re_result.group(1), re_result.group(2), re_result.group(3), re_result.group(4))
    #
#
