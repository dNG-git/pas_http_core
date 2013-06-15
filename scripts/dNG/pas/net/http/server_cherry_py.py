# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.net.http.ServerCherryPy
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

from cherrypy import log
from cherrypy.wsgiserver import CherryPyWSGIServer
import socket

from dNG.pas.data.settings import Settings
from dNG.pas.controller.http_wsgi1_request import HttpWsgi1Request
from dNG.pas.module.named_loader import NamedLoader
from . import Server

class ServerCherryPy(Server):
#
	"""
"ServerCherryPy" is responsible to start the HTTP CherryPy server.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(ServerCherryPy)

:since: v0.1.01
		"""

		Server.__init__(self)

		self.server = None
		"""
cherrypy server
		"""

		log_handler = NamedLoader.get_singleton("dNG.pas.data.logging.LogHandler", False)

		if (log_handler != None):
		#
			log_handler.add_logger("{0}.error.{1}".format(log.logger_root, log.appid))
			log_handler.return_instance()
		#
	#

	def configure(self):
	#
		"""
Configures the server

:since: v0.1.01
		"""

		listener_host = Settings.get("pas_http_cherrypy_server_host", self.socket_hostname)
		self.port = int(Settings.get("pas_http_cherrypy_server_port", 8080))

		if (listener_host == ""):
		#
			listener_host = ("::" if (socket.has_ipv6) else "0.0.0.0")
			self.host = Settings.get("pas_http_cherrypy_server_preferred_hostname", self.socket_hostname)
		#
		else: self.host = listener_host

		listener_data = ( listener_host, self.port )
		self.server = CherryPyWSGIServer(listener_data, HttpWsgi1Request, server_name = "directPAS/#echo(pasHttpCoreIVersion)# [direct Netware Group]")

		if (self.log_handler != None): self.log_handler.info("pas.http.core cherrypy server starts at '{0}:{1:d}'".format(listener_host, self.port))

		"""
Configure common paths and settings
		"""

		Server.configure(self)
	#

	def run(self):
	#
		"""
Runs the server

:since: v0.1.01
		"""

		try: self.server.start()
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

:since: v0.1.01
		"""

		if (self.server != None): self.server.stop()
		return Server.stop(self, params, last_return)
	#
#

##j## EOF