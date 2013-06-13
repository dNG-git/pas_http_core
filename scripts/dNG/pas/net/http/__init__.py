# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.net.http
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

from threading import Thread
from socket import getfqdn

from dNG.pas.data.settings import Settings
from dNG.pas.data.http.virtual_config import VirtualConfig
from dNG.pas.data.logging.log_line import LogLine
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.plugins.hooks import Hooks

class Server(Thread):
#
	"""
"Server" is responsible to configure an HTTP aware instance.

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
Constructor __init__(Server)

:since: v0.1.00
		"""

		Thread.__init__(self)

		self.host = None
		"""
Configured server host
		"""
		self.log_handler = NamedLoader.get_singleton("dNG.pas.data.logging.LogHandler", False)
		"""
The log_handler is called whenever debug messages should be logged or errors
happened.
		"""
		self.socket_hostname = getfqdn().lower()
		"""
Socket server hostname
		"""
		self.port = None
		"""
Configured server port
		"""

		Hooks.register("dNG.pas.http.server.get_host", self.get_host)
		Hooks.register("dNG.pas.http.server.get_port", self.get_port)
	#

	def __del__(self):
	#
		"""
Destructor __del__(Server)

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.return_instance()
		Hooks.unregister("dNG.pas.http.server.get_host", self.get_host)
		Hooks.unregister("dNG.pas.http.server.get_port", self.get_port)
	#

	def configure(self):
	#
		"""
Configures the server

:since: v0.1.00
		"""

		site_version = Settings.get("pas_http_site_version", "")

		if (site_version == ""):
		#
			site_version = "#echo(pasHttpCoreIVersion)#"
			Settings.set("pas_http_site_version", site_version)
		#

		Settings.set("http_path_mmedia_versioned", "/data/mmedia/{0}".format(site_version))

		VirtualConfig.set_virtual_path("/data/mmedia/{0}/".format(site_version), { "s": "cache", "uri": "dfile", "uri_prefix": "{0}/".format(Settings.get("http_path_mmedia_versioned")) })
		VirtualConfig.set_virtual_path("/data/mmedia/", { "s": "cache", "uri": "dfile", "uri_prefix": "/data/mmedia/" })

		Hooks.call("dNG.pas.http.server.configured", server = self)
	#

	def get_host(self, params = None, last_return = None):
	#
		"""
Returns the configured server host.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:since: v0.1.00
		"""

		return (self.host if (last_return == None) else last_return)
	#

	def get_port(self, params = None, last_return = None):
	#
		"""
Returns the configured server port.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:since: v0.1.00
		"""

		return (self.port if (last_return == None) else last_return)
	#

	def start(self, params = None, last_return = None):
	#
		"""
Start the server

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:since: v0.1.00
		"""

		self.configure()
		Thread.start(self)

		Hooks.call("dNG.pas.http.startup", server = self)
		return self
	#

	def log_request(self, handler):
	#
		"""
tornadoweb.org: Writes a completed HTTP request to the logs.

:since: v0.1.00
		"""

		if (self.log_handler != None):
		#
			if handler.get_status() < 400: py_function = self.log_handler.info
			elif handler.get_status() < 500: py_function = self.log_handler.warning
			else: py_function = self.log_handler.error

			py_function("{0} {1:d} {2} {3} ({4} {5:.2f})".format(handler.request.version, handler.get_status(), handler.request.method, handler.request.uri , handler.request.remote_ip, handler.request.request_time()))
		#

	def run(self):
	#
		"""
Runs the server

:since: v0.1.00
		"""

		raise RuntimeError("Not implemented", 38)
	#

	def stop(self, params = None, last_return = None):
	#
		"""
Stop the server

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:since: v0.1.00
		"""

		Hooks.call("dNG.pas.http.shutdown", server = self)
		return last_return
	#

	@staticmethod
	def get_instance():
	#
		"""
Returns an HTTP server instance based on the configuration set.

:return: (object) HTTP server implementation
:since:  v0.1.00
		"""

		var_return = None
		http_server_mode = Settings.get("pas_http_server_mode", "standalone")

		try:
		#
			if (http_server_mode == "cherrypy"): var_return = NamedLoader.get_instance("dNG.pas.net.http.ServerCherryPy")
			elif (http_server_mode == "waitress"): var_return = NamedLoader.get_instance("dNG.pas.net.http.ServerWaitress")
		#
		except Exception as handled_exception:
		#
			LogLine.error(handled_exception)
			LogLine.warning("pas.http.core use fallback after an exception occurred while instantiating the HTTP implementation")

			http_server_mode= "standalone"
		#

		if (http_server_mode == "standalone"): var_return = NamedLoader.get_instance("dNG.pas.net.http.ServerStandalone")
		return var_return
	#
#

##j## EOF