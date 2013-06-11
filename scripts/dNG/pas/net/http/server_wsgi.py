# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.net.http.server_wsgi
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

from math import floor
from time import time

from dNG.pas.controller.http_wsgi1_request import direct_http_wsgi1_request
from dNG.pas.data.settings import direct_settings
from dNG.pas.module.named_loader import direct_named_loader
from dNG.pas.plugins.hooks import direct_hooks
from . import direct_server

class direct_server_wsgi(direct_server):
#
	"""
"direct_server_wsgi" takes requests from WSGI aware servers.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, wsgi_env, wsgi_header_response):
	#
		"""
Constructor __init__(direct_server_wsgi)

:since: v0.1.00
		"""

		direct_settings.read_file("{0}/settings/pas_core.json".format(direct_settings.get("path_data")), True)
		direct_settings.read_file("{0}/settings/pas_http_server.json".format(direct_settings.get("path_data")), True)

		self.cache_instance = direct_named_loader.get_singleton("dNG.pas.data.cache", False)
		"""
Cache instance
		"""
		self.host = None
		"""
Configured server host
		"""
		self.log_handler = direct_named_loader.get_singleton("dNG.pas.data.logging.log_handler", False)
		"""
The log_handler is called whenever debug messages should be logged or errors
happened.
		"""
		self.port = None
		"""
Server port
		"""
		self.time_started = time()
		"""
Timestamp of service initialisation
		"""

		direct_hooks.load("http")
		direct_hooks.register("dNG.pas.status.getUptime", self.get_uptime)

		if (self.log_handler != None):
		#
			direct_hooks.set_log_handler(self.log_handler)
			direct_named_loader.set_log_handler(self.log_handler)
			self.log_handler.debug("#echo(__FILEPATH__)# -server.__init__()- (#echo(__LINE__)#)")
		#

		direct_hooks.call("dNG.pas.http.wsgi.startup")

		self.configure()
		self.http_wsgi1_request = direct_http_wsgi1_request(wsgi_env, wsgi_header_response)
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
		direct_hooks.call("dNG.pas.http.shutdown")
		direct_hooks.call("dNG.pas.status.shutdown")
		if (self.cache_instance != None): self.cache_instance.return_instance()

		return iter(http_wsgi1_request)
	#

	def get_uptime (self, params = None, last_return = None):
	#
		"""
Returns the time (timestamp) this service had been initialized.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (int) Unix timestamp; None if unknown
:since:  v0.1.00
		"""

		return floor(self.time_started)
	#
#

##j## EOF