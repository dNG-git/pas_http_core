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

from math import floor
from time import time

from dNG.pas.controller.http_wsgi1_request import HttpWsgi1Request
from dNG.pas.data.settings import Settings
from dNG.pas.data.text.l10n import L10n
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.plugins.hook import Hook
from .server_implementation import ServerImplementation

class ServerWsgi(ServerImplementation):
#
	"""
"ServerWsgi" takes requests from WSGI aware servers.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	# pylint: disable=unused-argument

	def __init__(self, wsgi_env, wsgi_header_response):
	#
		"""
Constructor __init__(ServerWsgi)

:since: v0.1.00
		"""

		self.cache_instance = NamedLoader.get_singleton("dNG.pas.data.Cache", False)
		"""
Cache instance
		"""
		self.time_started = time()
		"""
Timestamp of service initialisation
		"""

		self.cache_instance.disable()

		# Call super after we disabled the cache
		ServerImplementation.__init__(self)

		self._configure()

		Hook.load("http")
		Hook.register("dNG.pas.Status.getTimeStarted", self.get_time_started)
		Hook.register("dNG.pas.Status.getUptime", self.get_uptime)

		if (self.log_handler != None):
		#
			Hook.set_log_handler(self.log_handler)
			NamedLoader.set_log_handler(self.log_handler)
			self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.__init__()- (#echo(__LINE__)#)", self, context = "pas_http_core")
		#

		Hook.call("dNG.pas.Status.onStartup")
		Hook.call("dNG.pas.http.Wsgi.onStartup")

		self.http_wsgi1_request = HttpWsgi1Request(wsgi_env, wsgi_header_response)
	#

	def __del__(self):
	#
		"""
Destructor __del__(ServerWsgi)

Ensure that references are freed for GC. Some implementations like Apache's
mod_wsgi may already have removed globals at this stage.

:since: v0.1.00
		"""

		if (Hook != None): Hook.free()
	#

	def __iter__(self):
	#
		"""
python.org: Return an iterator object.

:return: (object) Iterator object
:since:  v0.1.00
		"""

		http_wsgi1_request = self.http_wsgi1_request
		self.http_wsgi1_request = None

		Hook.call("dNG.pas.http.Wsgi.onShutdown")
		Hook.call("dNG.pas.Status.onShutdown")
		Hook.free()

		return iter(http_wsgi1_request)
	#

	def _configure(self):
	#
		"""
Configures the server

:since: v0.1.01
		"""

		Settings.read_file("{0}/settings/pas_core.json".format(Settings.get("path_data")), True)
		Settings.read_file("{0}/settings/pas_http.json".format(Settings.get("path_data")))

		ServerImplementation._configure(self)
	#

	def get_time_started(self, params = None, last_return = None):
	#
		"""
Returns the time (timestamp) this service had been initialized.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (int) Unix timestamp
:since:  v1.0.0
		"""

		return self.time_started
	#

	def get_uptime(self, params = None, last_return = None):
	#
		"""
Returns the time in seconds since this service had been initialized.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (int) Uptime in seconds
:since:  v0.1.00
		"""

		return int(floor(time() - self.time_started))
	#
#

##j## EOF