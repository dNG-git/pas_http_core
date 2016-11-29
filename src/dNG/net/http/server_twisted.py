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

from dNG.controller.http_wsgi1_request import HttpWsgi1Request
from dNG.data.settings import Settings
from dNG.module.named_loader import NamedLoader
from dNG.runtime.exception_log_trap import ExceptionLogTrap

from twisted.internet import reactor
from twisted.internet.endpoints import serverFromString
from twisted.python import log
from twisted.python.threadpool import ThreadPool
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

from .abstract_server import AbstractServer

class ServerTwisted(AbstractServer):
    """
"ServerTwisted" is responsible to start the HTTP Twisted server.

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
Constructor __init__(ServerTwisted)

:since: v0.2.00
        """

        AbstractServer.__init__(self)

        self.log_observer = None
        """
@TODO
        """
        self.reactor = None
        """
Twisted reactor instance
        """
        self.thread_pool = None
        """
@TODO
        """

        log_handler = NamedLoader.get_singleton("dNG.data.logging.LogHandler", False)

        if (log_handler is not None):
            log_handler.add_logger("twisted")

            self.log_observer = log.PythonLoggingObserver("twisted")
            self.log_observer.start()

            log.startLoggingWithObserver(self.log_observer.emit, setStdout = False)
        #
    #

    def _configure(self):
        """
Configures the server

:since: v0.2.00
        """

        listener_host = Settings.get("pas_http_twisted_server_host", self.socket_hostname)
        self.port = int(Settings.get("pas_http_twisted_server_port", 8080))

        self.reactor = reactor
        self.reactor.addSystemEventTrigger('before', 'shutdown', self.stop)

        server_description = "tcp:{0:d}".format(self.port)

        if (listener_host == ""): self.host = Settings.get("pas_http_server_preferred_hostname", self.socket_hostname)
        else:
            self.host = listener_host
            server_description += ":interface={0}".format(self.host)
        #

        self.thread_pool = ThreadPool()
        self.thread_pool.start()

        if (self.log_handler is not None): self.log_handler.info("pas.http.core Twisted server starts at '{0}:{1:d}'", listener_host, self.port, context = "pas_http_core")

        server = serverFromString(self.reactor, server_description)
        server.listen(Site(WSGIResource(reactor, self.thread_pool, HttpWsgi1Request)))

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

        self.reactor.startRunning(installSignalHandlers = False)
        with ExceptionLogTrap("pas_http_core"): self.reactor.mainLoop()
    #

    def stop(self, params = None, last_return = None):
        """
Stop the server

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.2.00
        """

        if (self.thread_pool is not None):
            self.thread_pool.stop()
            self.thread_pool = None
        #

        if (self.reactor is not None):
            self.reactor.stop()
            self.reactor = None
        #

        if (self.log_observer is not None):
            self.log_observer.stop()
            self.log_observer = None
        #

        return AbstractServer.stop(self, params, last_return)
    #
#
