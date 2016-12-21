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

# pylint: disable=import-error

from aiohttp.wsgi import WSGIServerHttpProtocol
import asyncio
import socket

from dNG.controller.http_wsgi1_request import HttpWsgi1Request
from dNG.data.settings import Settings
from dNG.runtime.exception_log_trap import ExceptionLogTrap

from .abstract_server import AbstractServer

class ServerAiohttp(AbstractServer):
    """
"ServerAiohttp" is responsible to start an HTTP aware server.

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
Constructor __init__(ServerAiohttp)

:since: v0.2.00
        """

        AbstractServer.__init__(self)

        self.asyncio_loop = None
        """
asyncio loop instance
        """
        self.server = None
        """
asyncio loop instance
        """
    #

    def _configure(self):
        """
Configures the server

:since: v0.2.00
        """

        listener_host = Settings.get("pas_http_aiohttp_server_host", self.socket_hostname)
        self.port = int(Settings.get("pas_http_aiohttp_server_port", 8080))

        if (listener_host == ""):
            listener_host = ("::" if (hasattr(socket, "has_ipv6") and socket.has_ipv6) else "0.0.0.0")
            self.host = Settings.get("pas_http_server_preferred_hostname", self.socket_hostname)
        else: self.host = listener_host

        if (self.log_handler is not None): self.log_handler.info("pas.http.core aiohttp server starts at '{0}:{1:d}'", self.host, self.port, context = "pas_http_core")

        self.asyncio_loop = asyncio.get_event_loop()
        self.server = self.asyncio_loop.create_server(lambda: WSGIServerHttpProtocol(HttpWsgi1Request), listener_host, self.port)

        """
Configure common paths and settings
        """

        AbstractServer._configure(self)
    #

    def run(self):
        """
Runs the server

:since: v0.2.00
        """

        with ExceptionLogTrap("pas_http_core"): self.asyncio_loop.run_forever()
    #

    def stop(self, params = None, last_return = None):
        """
Stop the server

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.2.00
        """

        if (self.server is not None):
            self.server.close()
            self.server = None

            self.asyncio_loop.stop()
            self.asyncio_loop = None
        #

        return AbstractServer.stop(self, params, last_return)
    #
#
