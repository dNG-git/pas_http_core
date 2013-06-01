# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.net.http.server_standalone
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

from dNG.pas.data.settings import direct_settings
from dNG.pas.controller.http_wsgi1_request import direct_http_wsgi1_request
from . import direct_server

class direct_server_standalone(direct_server):
#
	"""
"direct_server_standalone" is responsible to start an HTTP aware server.

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
Constructor __init__(direct_server_standalone)

:since: v0.1.00
		"""

		direct_server.__init__(self)

		self.server = None
		"""
WSGI server
		"""
	#

	def configure(self):
	#
		"""
Configures the server

:since: v0.1.00
		"""

		listener_host = direct_settings.get("pas_http_standalone_server_host", self.socket_hostname)
		self.port = int(direct_settings.get("pas_http_standalone_server_port", 8080))

		if (listener_host == ""): self.host = direct_settings.get("pas_http_standalone_server_preferred_hostname", self.socket_hostname)

		self.server = make_server(listener_host, self.port, direct_http_wsgi1_request)
		self.server.socket.settimeout(5)
		if (self.log_handler != None): self.log_handler.info("pas.http.core wsgiref server starts at '{0}:{1:d}'".format(self.host, self.port))

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
		return direct_server.stop(self, params, last_return)
	#
#

##j## EOF