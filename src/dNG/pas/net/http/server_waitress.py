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

from waitress.server import create_server
from socket import error as socket_error

from dNG.pas.data.settings import Settings
from dNG.pas.controller.http_wsgi1_request import HttpWsgi1Request
from dNG.pas.runtime.exception_log_trap import ExceptionLogTrap
from .server_implementation import ServerImplementation

class ServerWaitress(ServerImplementation):
#
	"""
"ServerWaitress" is responsible to start an HTTP aware server.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(ServerWaitress)

:since: v0.1.00
		"""

		ServerImplementation.__init__(self)

		self.server = None
		"""
WSGI server
		"""
		self.sockets = { }
		"""
waitress opened sockets
		"""
	#

	def _configure(self):
	#
		"""
Configures the server

:since: v0.1.00
		"""

		listener_host = Settings.get("pas_http_waitress_server_host", self.socket_hostname)
		self.port = int(Settings.get("pas_http_waitress_server_port", 8080))

		if (listener_host == ""): self.host = Settings.get("pas_http_server_preferred_hostname", self.socket_hostname)
		else: self.host = listener_host

		if (self.log_handler != None): self.log_handler.info("pas.http.core waitress server starts at '{0}:{1:d}'", self.host, self.port, context = "pas_http_core")
		self.server = create_server(HttpWsgi1Request, self.sockets, host = listener_host, port = self.port, asyncore_loop_timeout = 5)

		"""
Configure common paths and settings
		"""

		ServerImplementation._configure(self)
	#

	def run(self):
	#
		"""
Runs the server

:since: v0.1.00
		"""

		with ExceptionLogTrap("pas_http_core"): self.server.run()
	#

	def stop(self, params = None, last_return = None):
	#
		"""
Stop the server

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
		"""

		if (self.server != None):
		#
			self.server = None

			while (len(self.sockets) > 0):
			#
				sockets = self.sockets.copy()

				for _socket in sockets:
				#
					try:
					#
						self.sockets.remove(_socket)
						sockets[_socket].close()
					#
					except socket_error: pass
				#
			#

			self.sockets = { }
		#

		return ServerImplementation.stop(self, params, last_return)
	#
#

##j## EOF