# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.module.blocks.services.Index
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

from dNG.pas.controller.abstract_http_request import AbstractHttpRequest
from dNG.pas.controller.predefined_http_request import PredefinedHttpRequest
from dNG.pas.data.settings import Settings
from dNG.pas.data.http.translatable_exception import TranslatableException
from .module import Module

class Index(Module):
#
	"""
Service for "m=services;s=index" (default values)

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def execute_index(self):
	#
		"""
Action for "index"

:since: v0.1.00
		"""

		default_page_settings = Settings.get("pas_http_site_page_default_{0}".format(self.request.get_lang()))
		if (default_page_settings == None): default_page_settings = Settings.get("pas_http_site_page_default")

		if (type(default_page_settings) == dict and ("module" in default_page_settings or "service" in default_page_settings or "action" in default_page_settings)):
		#
			redirect_request = PredefinedHttpRequest()
			if ("module" in default_page_settings): redirect_request.set_module(default_page_settings['module'])
			if ("service" in default_page_settings): redirect_request.set_module(default_page_settings['service'])
			if ("action" in default_page_settings): redirect_request.set_module(default_page_settings['action'])

			if ("dsd" in default_page_settings):
			#
				dsd = (default_page_settings['dsd'] if (type(default_page_settings['dsd']) == dict) else AbstractHttpRequest.parse_dsd(default_page_settings['dsd']))

				if (type(dsd) == dict):
				#
					for key in dsd: redirect_request.set_dsd(key, dsd[key])
				#
			#

			self.request.redirect(redirect_request)
		#
		else: raise TranslatableException("pas_http_core_site_unconfigured", 404)
	#
#

##j## EOF