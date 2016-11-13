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

from cherrypy import config, log
from cherrypy.wsgiserver import CherryPyWSGIServer
import socket

from dNG.controller.http_wsgi1_request import HttpWsgi1Request
from dNG.data.settings import Settings
from dNG.module.named_loader import NamedLoader
from dNG.runtime.exception_log_trap import ExceptionLogTrap

from .abstract_server import AbstractServer

class ServerCherryPy(AbstractServer):
    """
"ServerCherryPy" is responsible to start the HTTP CherryPy server.

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
Constructor __init__(ServerCherryPy)

:since: v0.2.00
        """

        AbstractServer.__init__(self)

        self.server = None
        """
cherrypy server
        """

        log_handler = NamedLoader.get_singleton("dNG.data.logging.LogHandler", False)
        if (log_handler is not None): log_handler.add_logger("{0}.error.{1}".format(log.logger_root, log.appid))
    #

    def _configure(self):
        """
Configures the server

:since: v0.2.00
        """

        listener_host = Settings.get("pas_http_cherrypy_server_host", self.socket_hostname)
        self.port = int(Settings.get("pas_http_cherrypy_server_port", 8080))

        if (listener_host == ""):
            listener_host = ("::" if (hasattr(socket, "has_ipv6") and socket.has_ipv6) else "0.0.0.0")
            self.host = Settings.get("pas_http_server_preferred_hostname", self.socket_hostname)
        else: self.host = listener_host

        config.update({ "response.stream": True })

        if (self.log_handler is not None): self.log_handler.info("pas.http.core cherrypy server starts at '{0}:{1:d}'", listener_host, self.port, context = "pas_http_core")

        listener_data = ( listener_host, self.port )
        threads = Settings.get("pas_http_cherrypy_server_threads", 10)

        self.server = CherryPyWSGIServer(listener_data,
                                         HttpWsgi1Request,
                                         numthreads = threads,
                                         server_name = self.host
                                        )

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

        with ExceptionLogTrap("pas_http_core"): self.server.start()
    #

    def stop(self, params = None, last_return = None):
        """
Stop the server

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.2.00
        """

        if (self.server is not None): self.server.stop()
        return AbstractServer.stop(self, params, last_return)
    #
#
