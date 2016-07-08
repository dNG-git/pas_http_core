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

from dNG.controller.abstract_http_request import AbstractHttpRequest
from dNG.controller.predefined_http_request import PredefinedHttpRequest
from dNG.data.http.translatable_error import TranslatableError
from dNG.data.settings import Settings

from .module import Module

class Index(Module):
#
	"""
Service for "m=services" (default values)

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def execute_index(self):
	#
		"""
Action for "index"

:since: v0.2.00
		"""

		default_page_settings = Settings.get_lang_associated("pas_http_site_page_default", self.request.get_lang())

		if (type(default_page_settings) is not dict
		    or ("module" not in default_page_settings
		        and "service" not in default_page_settings
		        and "action" not in default_page_settings
		       )
		   ): raise TranslatableError("pas_http_core_site_unconfigured", 404)

		redirect_request = PredefinedHttpRequest()
		if ("module" in default_page_settings): redirect_request.set_module(default_page_settings['module'])
		if ("service" in default_page_settings): redirect_request.set_module(default_page_settings['service'])
		if ("action" in default_page_settings): redirect_request.set_module(default_page_settings['action'])

		if ("dsd" in default_page_settings):
		#
			dsd = (default_page_settings['dsd']
			       if (type(default_page_settings['dsd']) is dict) else
			       AbstractHttpRequest.parse_dsd(default_page_settings['dsd'])
			      )

			if (type(dsd) is dict):
			#
				for key in dsd: redirect_request.set_dsd(key, dsd[key])
			#
		#

		self.request.redirect(redirect_request)
	#
#

##j## EOF