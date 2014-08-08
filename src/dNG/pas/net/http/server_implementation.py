# -*- coding: utf-8 -*-
##j## BOF

"""
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
"""

from socket import error as socket_error
from socket import getaddrinfo, gethostname, getfqdn

from dNG.pas.data.settings import Settings
from dNG.pas.data.http.virtual_config import VirtualConfig
from dNG.pas.data.logging.log_line import LogLine
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.plugins.hook import Hook
from dNG.pas.runtime.not_implemented_exception import NotImplementedException
from dNG.pas.runtime.thread import Thread

class ServerImplementation(Thread):
#
	"""
"ServerImplementation" is responsible to configure an HTTP aware instance.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	# pylint: disable=arguments-differ,unused-argument

	def __init__(self):
	#
		"""
Constructor __init__(ServerImplementation)

:since: v0.1.00
		"""

		Thread.__init__(self)

		self.host = None
		"""
Configured server host
		"""
		self.log_handler = NamedLoader.get_singleton("dNG.pas.data.logging.LogHandler", False)
		"""
The LogHandler is called whenever debug messages should be logged or errors
happened.
		"""
		self.port = None
		"""
Configured server port
		"""
		self.socket_hostname = None
		"""
Socket server hostname
		"""

		socket_hostname = getfqdn()

		try:
		#
			getaddrinfo(socket_hostname, None)
			self.socket_hostname = socket_hostname
		#
		except socket_error: self.socket_hostname = gethostname()

		self.socket_hostname = self.socket_hostname.lower()

		Hook.register("dNG.pas.http.Server.getHost", self.get_host)
		Hook.register("dNG.pas.http.Server.getPort", self.get_port)
	#

	def _configure(self):
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

		VirtualConfig.set_virtual_path("/data/mmedia/{0}/".format(site_version), { "s": "cache", "path": "dfile" })
		VirtualConfig.set_virtual_path("/data/mmedia/", { "s": "cache", "path": "dfile" })

		Hook.call("dNG.pas.http.Server.onConfigured", server = self)
	#

	def get_host(self, params = None, last_return = None):
	#
		"""
Returns the configured server host.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
		"""

		return (self.host if (last_return == None) else last_return)
	#

	def get_port(self, params = None, last_return = None):
	#
		"""
Returns the configured server port.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
		"""

		return (self.port if (last_return == None) else last_return)
	#

	def start(self, params = None, last_return = None):
	#
		"""
Start the server

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
		"""

		self._configure()
		Thread.start(self)

		Hook.call("dNG.pas.http.Server.onStartup", server = self)
		return self
	#

	def run(self):
	#
		"""
Runs the server

:since: v0.1.00
		"""

		raise NotImplementedException()
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

		Hook.call("dNG.pas.http.Server.onShutdown", server = self)
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

		# pylint: disable=broad-except

		_return = None

		Settings.read_file("{0}/settings/pas_http.json".format(Settings.get("path_data")))
		server_implementation = Settings.get("pas_http_server_implementation", "Standalone")

		try: _return = NamedLoader.get_instance("dNG.pas.net.http.Server{0}".format(server_implementation))
		except Exception as handled_exception:
		#
			LogLine.error(handled_exception, context = "pas_http_site")
			LogLine.warning("pas.http.core use fallback after an exception occurred while instantiating the HTTP implementation", context = "pas_http_site")

			server_implementation = "Standalone"
		#

		if (server_implementation == "Standalone"): _return = NamedLoader.get_instance("dNG.pas.net.http.ServerStandalone")
		return _return
	#
#

##j## EOF