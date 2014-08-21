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

from dNG.pas.data.http.translatable_exception import TranslatableException
from dNG.pas.module.controller.abstract_http import AbstractHttp as AbstractHttpController
from .service_list_mixin import ServiceListMixin

class ServiceList(AbstractHttpController, ServiceListMixin):
#
	"""
"ServiceList" is a navigation element providing links to other services.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def execute_render(self):
	#
		"""
Action for "render"

:since: v0.1.00
		"""

		if ("css_sprite" in self.context): self._add_options_block_css_sprite(self.context['css_sprite'])

		if ("file" in self.context): self.set_action_result(self.render_service_list_file(self.context['file']))
		elif (isinstance(self.context.get("entries"), list)): self.set_action_result(self.render_service_list_entries(self.context['entries']))
		else: raise TranslatableException("core_unknown_error", value = "Missing service list to render")
	#
#

##j## EOF