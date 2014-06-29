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
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def execute_render(self):
	#
		"""
Action for "render"

:since: v0.1.00
		"""

		if ("file" in self.context): self.set_action_result(self.render_service_list_file(self.context['file']))
		else: raise TranslatableException("core_unknown_error", value = "Missing service list to render")
	#
#

##j## EOF