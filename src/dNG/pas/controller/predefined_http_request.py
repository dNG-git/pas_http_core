# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.controller.PredefinedHttpRequest
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

from .abstract_http_request import AbstractHttpRequest
from .abstract_inner_http_request import AbstractInnerHttpRequest

class PredefinedHttpRequest(AbstractInnerHttpRequest):
#
	"""
"PredefinedHttpRequest" implements predefined HTTP requests.

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

:since: v0.1.00
		"""

		self.action = action
	#

	def set_iline(self, iline):
	#
		"""
Sets all parameters defined in the given URI request string.

:since: v0.1.00
		"""

		parameters = AbstractHttpRequest.parse_iline(iline)

		if ("a" in parameters): self.set_action(AbstractHttpRequest.filter_parameter_word(parameters['a']))
		if ("m" in parameters): self.set_module(AbstractHttpRequest.filter_parameter_word(parameters['m']))
		if ("s" in parameters): self.set_service(AbstractHttpRequest.filter_parameter_service(parameters['s']))

		if ("dsd" in parameters):
		#
			dsd = AbstractHttpRequest.parse_dsd(parameters['dsd'])
			for key in dsd: self.set_dsd(key, dsd[key])
		#

		if ("ohandler" in parameters and len(parameters['ohandler']) > 0): self.set_output_format(AbstractHttpRequest.filter_parameter_word(self.parameters['ohandler']))
	#

	def set_module(self, module):
	#
		"""
Sets the requested module.

:param module: Requested module

:since: v0.1.00
		"""

		self.module = module
	#

	def set_output_format(self, output_format):
	#
		"""
Sets the output format.

:param output_format: (str) Output format

:since: v0.1.00
		"""

		self.output_format = output_format
	#

	def set_service(self, service):
	#
		"""
Sets the requested service.

:param service: Requested service

:since: v0.1.00
		"""

		self.service = service
	#
#

##j## EOF