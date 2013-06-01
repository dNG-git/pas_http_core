# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.net.http.server_tornado
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

from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer

from dNG.pas.data.settings import direct_settings
from dNG.pas.controller.http_wsgi1_request import direct_http_wsgi1_request
from dNG.pas.module.named_loader import direct_named_loader
from . import direct_server

class direct_server_tornado(direct_server):
#
	"""
"direct_server_tornado" is responsible to start the HTTP tornado server.

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
Constructor __init__(direct_server_tornado)

:since: v0.1.00
		"""

		direct_server.__init__(self)

		self.server = None
		"""
Tornado server
		"""

		log_handler = direct_named_loader.get_singleton("dNG.pas.data.logging.log_handler", False)

		if (log_handler != None):
		#
			log_handler.add_logger("tornado.application")
			log_handler.add_logger("tornado.general")
			log_handler.return_instance()
		#
	#

	def configure(self):
	#
		"""
Configures the server

:since: v0.1.00
		"""

		listener_host = direct_settings.get("pas_http_tornado_server_host", self.socket_hostname)
		self.port = int(direct_settings.get("pas_http_tornado_server_port", 8080))

		self.server = HTTPServer(WSGIContainer(direct_http_wsgi1_request))

		if (listener_host == ""):
		#
			self.host = direct_settings.get("pas_http_tornado_server_preferred_hostname", self.socket_hostname)
			self.server.listen(self.port)
		#
		else:
		#
			self.host = listener_host
			self.server.listen(self.port, listener_host)
		#

		if (self.log_handler != None): self.log_handler.info("pas.http.core tornado server starts at '{0}:{1:d}'".format(listener_host, self.port))

		"""
Configure common paths and settings
		"""

		direct_server.configure(self)
	#

	def run(self):
	#
		"""
Runs the server

:since: v0.1.00
		"""

		try: IOLoop.instance().start()
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

		if (self.server != None): IOLoop.instance().stop()
		return direct_server.stop(self, params, last_return)
	#
#

##j## EOF