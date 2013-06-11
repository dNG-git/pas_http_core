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

from dNG.pas.data.settings import direct_settings
from dNG.pas.data.http.virtual_config import direct_virtual_config
from dNG.pas.data.logging.log_line import direct_log_line
from dNG.pas.module.named_loader import direct_named_loader
from dNG.pas.plugins.hooks import direct_hooks

class direct_server(Thread):
#
	"""
"direct_server" is responsible to configure an HTTP aware instance.

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
Constructor __init__(direct_server)

:since: v0.1.00
		"""

		Thread.__init__(self)

		self.host = None
		"""
Configured server host
		"""
		self.log_handler = direct_named_loader.get_singleton("dNG.pas.data.logging.log_handler", False)
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

		direct_hooks.register("dNG.pas.http.server.get_host", self.get_host)
		direct_hooks.register("dNG.pas.http.server.get_port", self.get_port)
	#

	def __del__(self):
	#
		"""
Destructor __del__(direct_server)

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.return_instance()
		direct_hooks.unregister("dNG.pas.http.server.get_host", self.get_host)
		direct_hooks.unregister("dNG.pas.http.server.get_port", self.get_port)
	#

	def configure(self):
	#
		"""
Configures the server

:since: v0.1.00
		"""

		site_version = direct_settings.get("pas_http_site_version", "")

		if (site_version == ""):
		#
			site_version = "#echo(pasHttpCoreIVersion)#"
			direct_settings.set("pas_http_site_version", site_version)
		#

		direct_settings.set("http_path_mmedia_versioned", "/data/mmedia/{0}".format(site_version))

		direct_virtual_config.set_virtual_path("/data/mmedia/{0}/".format(site_version), { "s": "cache", "uri": "dfile", "uri_prefix": "{0}/".format(direct_settings.get("http_path_mmedia_versioned")) })
		direct_virtual_config.set_virtual_path("/data/mmedia/", { "s": "cache", "uri": "dfile", "uri_prefix": "/data/mmedia/" })

		direct_hooks.call("dNG.pas.http.server.configured", server = self)
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

		direct_hooks.call("dNG.pas.http.startup", server = self)
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

		direct_hooks.call("dNG.pas.http.shutdown", server = self)
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
		http_server_mode = direct_settings.get("pas_http_server_mode", "standalone")

		try:
		#
			if (http_server_mode == "cherrypy"): var_return = direct_named_loader.get_instance("dNG.pas.net.http.server_cherrypy")
			elif (http_server_mode == "waitress"): var_return = direct_named_loader.get_instance("dNG.pas.net.http.server_waitress")
		#
		except Exception as handled_exception:
		#
			direct_log_line.error(handled_exception)
			direct_log_line.warning("pas.http.core use fallback after an exception occurred while instantiating the HTTP implementation")

			http_server_mode= "standalone"
		#

		if (http_server_mode == "standalone"): var_return = direct_named_loader.get_instance("dNG.pas.net.http.server_standalone")
		return var_return
	#
#

##j## EOF