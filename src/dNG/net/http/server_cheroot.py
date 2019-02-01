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

from logging import getLogger
import socket

from cheroot.wsgi import Server

from dNG.controller.http_wsgi1_request import HttpWsgi1Request
from dNG.data.settings import Settings
from dNG.plugins.hook import Hook
from dNG.runtime.exception_log_trap import ExceptionLogTrap

from .abstract_server import AbstractServer

class _WsgiServer(Server):
    """
cheroot.cherrypy.org: This class holds Cheroot WSGI server implementation.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def error_log(self, msg='', level=20, traceback=False):
        """
cheroot.cherrypy.org: Write error message to log.

:param msg: Error message
:param last_return: Logging level
:param: traceback: Add traceback to output or not

:since: v1.0.0
        """

        getLogger("cheroot").log(msg, level)
    #
#

class ServerCheroot(AbstractServer):
    """
"ServerCheroot" is responsible to start the HTTP Cheroot server.

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
Constructor __init__(ServerCheroot)

:since: v1.0.0
        """

        AbstractServer.__init__(self)

        self.server = None
        """
WSGI server
        """

        if (self._log_handler is not None): self._log_handler.add_logger("cheroot")
    #

    def _configure(self):
        """
Configures the server

:since: v1.0.0
        """

        listener_host = Settings.get("pas_http_cheroot_server_host", self.socket_hostname)
        self.port = int(Settings.get("pas_http_cheroot_server_port", 8080))

        if (listener_host == ""):
            listener_host = ("::" if (getattr(socket, "has_ipv6", False)) else "0.0.0.0")
            self.host = Settings.get("pas_http_server_preferred_hostname", self.socket_hostname)
        else: self.host = listener_host

        self.server = _WsgiServer((listener_host, self.port),
                                  HttpWsgi1Request,
                                  Settings.get("pas_http_cheroot_server_threads", 10),
                                  self.host,
                                  Settings.get("pas_http_cheroot_server_listener_queue_size", 5),
                                  Settings.get("pas_http_cheroot_response_timeout", 600)
                                 )

        if (self._log_handler is not None): self._log_handler.info("pas.http.core cheroot server starts at '{0}:{1:d}'", listener_host, self.port, context = "pas_http_core")

        """
Configure common paths and settings
        """

        AbstractServer._configure(self)
    #

    def run(self):
        """
Runs the server

:since: v1.0.0
        """

        with ExceptionLogTrap("pas_http_core"):
            self.server.start()
        #
    #

    def stop(self, params = None, last_return = None):
        """
Stop the server

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v1.0.0
        """

        if (self.server is not None):
            self.server.stop()
            self.server = None
        #

        return AbstractServer.stop(self, params, last_return)
    #
#
