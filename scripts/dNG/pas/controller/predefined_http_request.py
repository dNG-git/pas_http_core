# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.controller.abstract_request
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

from .abstract_inner_http_request import direct_abstract_inner_http_request

class direct_predefined_http_request(direct_abstract_inner_http_request):
#
	"""
"direct_predefined_http_request" implements predefined requests.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def set_action(self, action):
	#
		"""
Sets the requested action.

:since:  v0.1.00
		"""

		self.action = action
	#

	def set_module(self, module):
	#
		"""
Sets the requested module.

:param module: Requested module

:since:  v0.1.00
		"""

		self.module = module
	#

	def set_output_format(self, output_format):
	#
		"""
Sets the output format.

:param output_format: (str) Output format

:since:  v0.1.00
		"""

		self.output_format = output_format
	#

	def set_service(self, service):
	#
		"""
Sets the requested service.

:param service: Requested service

:since:  v0.1.00
		"""

		self.service = service
	#
#

##j## EOF