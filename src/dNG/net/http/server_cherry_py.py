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

import socket

import cherrypy

from dNG.controller.http_wsgi1_request import HttpWsgi1Request
from dNG.data.settings import Settings
from dNG.plugins.hook import Hook
from dNG.runtime.exception_log_trap import ExceptionLogTrap

from .abstract_server import AbstractServer

class ServerCherryPy(AbstractServer):
    """
"ServerCherryPy" is responsible to start the HTTP CherryPy server.

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
Constructor __init__(ServerCherryPy)

:since: v1.0.0
        """

        AbstractServer.__init__(self)

        if (self._log_handler is not None): self._log_handler.add_logger("{0}.error.{1}".format(cherrypy.log.logger_root, cherrypy.log.appid))
    #

    def _configure(self):
        """
Configures the server

:since: v1.0.0
        """

        listener_host = Settings.get("pas_http_cherrypy_server_host", self.socket_hostname)
        self.port = int(Settings.get("pas_http_cherrypy_server_port", 8080))

        if (listener_host == ""):
            listener_host = ("::" if (getattr(socket, "has_ipv6", False)) else "0.0.0.0")
            self.host = Settings.get("pas_http_server_preferred_hostname", self.socket_hostname)
        else: self.host = listener_host

        cherrypy.config.update({ "server.socket_host": listener_host,
                                 "server.socket_port": self.port,
                                 "server.thread_pool": Settings.get("pas_http_cherrypy_server_threads", 10),
                                 "response.stream": True,
                                 "response.timeout": Settings.get("pas_http_cherrypy_response_timeout", 600),
                                 "log.screen": False
                               })

        if (self._log_handler is not None): self._log_handler.info("pas.http.core cherrypy server starts at '{0}:{1:d}'", listener_host, self.port, context = "pas_http_core")

        cherrypy.engine.subscribe("exit", self.on_exit_event)
        cherrypy.tree.graft(HttpWsgi1Request)

        """
Configure common paths and settings
        """

        AbstractServer._configure(self)
    #

    def on_exit_event(self):
        """
Stop the application on CherryPy's request.

:since:  v1.0.0
        """

        Hook.call("dNG.pas.Status.stop")
    #

    def run(self):
        """
Runs the server

:since: v1.0.0
        """

        with ExceptionLogTrap("pas_http_core"):
            cherrypy.engine.start()
            cherrypy.engine.block()
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

        cherrypy.engine.unsubscribe("exit", self.on_exit_event)
        if (cherrypy.engine.state != cherrypy.engine.states.EXITING): cherrypy.engine.exit()

        return AbstractServer.stop(self, params, last_return)
    #
#
