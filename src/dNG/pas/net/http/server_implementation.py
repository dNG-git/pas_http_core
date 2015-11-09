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

from dNG.pas.data.settings import Settings
from dNG.pas.data.logging.log_line import LogLine
from dNG.pas.module.named_loader import NamedLoader

class ServerImplementation(object):
#
	"""
"ServerImplementation" is a factory for the configured, implementing HTTP
aware instance.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

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