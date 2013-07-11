# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.net.http.ServerStandalone
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;http;core

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasHttpCoreVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from wsgiref.simple_server import make_server

from dNG.pas.data.settings import Settings
from dNG.pas.controller.http_wsgi1_request import HttpWsgi1Request
from . import Server

class ServerStandalone(Server):
#
	"""
"ServerStandalone" is responsible to start an HTTP aware server.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(ServerStandalone)

:since: v0.1.00
		"""

		Server.__init__(self)

		self.server = None
		"""
WSGI server
		"""
	#

	def _configure(self):
	#
		"""
Configures the server

:since: v0.1.00
		"""

		listener_host = Settings.get("pas_http_standalone_server_host", self.socket_hostname)
		self.port = int(Settings.get("pas_http_standalone_server_port", 8080))

		if (listener_host == ""): self.host = Settings.get("pas_http_standalone_server_preferred_hostname", self.socket_hostname)
		else: self.host = listener_host

		self.server = make_server(listener_host, self.port, HttpWsgi1Request)
		self.server.socket.settimeout(5)
		if (self.log_handler != None): self.log_handler.info("pas.http.core wsgiref server starts at '{0}:{1:d}'".format(self.host, self.port))

		"""
Configure common paths and settings
		"""

		Server._configure(self)
	#

	def run(self):
	#
		"""
Runs the server

:since: v0.1.00
		"""

		try: self.server.serve_forever(5)
		except Exception as handled_exception:
		#
			if (self.log_handler != None): self.log_handler.error(handled_exception)
		#
	#

	def stop(self, params = None, last_return = None):
	#
		"""
Stop the server

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:since: v0.1.00
		"""

		if (self.server != None): self.server.shutdown()
		return Server.stop(self, params, last_return)
	#
#

##j## EOF