# -*- coding: utf-8 -*-
##j## BOF

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

from dNG.pas.data.settings import Settings
from dNG.pas.controller.http_wsgi1_request import HttpWsgi1Request
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.runtime.exception_log_trap import ExceptionLogTrap
from .server_implementation import ServerImplementation

class ServerCherryPy(ServerImplementation):
#
	"""
"ServerCherryPy" is responsible to start the HTTP CherryPy server.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(ServerCherryPy)

:since: v0.1.01
		"""

		ServerImplementation.__init__(self)

		self.server = None
		"""
cherrypy server
		"""

		log_handler = NamedLoader.get_singleton("dNG.pas.data.logging.LogHandler", False)
		if (log_handler is not None): log_handler.add_logger("{0}.error.{1}".format(log.logger_root, log.appid))
	#

	def _configure(self):
	#
		"""
Configures the server

:since: v0.1.01
		"""

		listener_host = Settings.get("pas_http_cherrypy_server_host", self.socket_hostname)
		self.port = int(Settings.get("pas_http_cherrypy_server_port", 8080))

		if (listener_host == ""):
		#
			listener_host = ("::" if (hasattr(socket, "has_ipv6") and socket.has_ipv6) else "0.0.0.0")
			self.host = Settings.get("pas_http_server_preferred_hostname", self.socket_hostname)
		#
		else: self.host = listener_host

		config.update({ "response.stream": True })
		numthreads = Settings.get("pas_http_cherrypy_server_numthreads", 10)

		if (self.log_handler is not None): self.log_handler.info("pas.http.core cherrypy server starts at '{0}:{1:d}'", listener_host, self.port, context = "pas_http_core")

		listener_data = ( listener_host, self.port )
		self.server = CherryPyWSGIServer(listener_data, HttpWsgi1Request, numthreads = numthreads, server_name = self.host)

		"""
Configure common paths and settings
		"""

		ServerImplementation._configure(self)
	#

	def run(self):
	#
		"""
Runs the server

:since: v0.1.01
		"""

		with ExceptionLogTrap("pas_http_core"): self.server.start()
	#

	def stop(self, params = None, last_return = None):
	#
		"""
Stop the server

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.01
		"""

		if (self.server is not None): self.server.stop()
		return ServerImplementation.stop(self, params, last_return)
	#
#

##j## EOF