# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.module.blocks.abstract_block
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

import re

from dNG.pas.controller.abstract_request import direct_abstract_request
from dNG.pas.controller.abstract_response import direct_abstract_response
from dNG.pas.data.translatable_exception import direct_translatable_exception

class direct_abstract_block(object):
#
	"""
"direct_abstract_block" provides methods for module and service
implementations.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(direct_abstract_block)

:since: v0.1.00
		"""

		self.action = None
		"""
Requested action
		"""
		self.action_result = None
		"""
Action result
		"""
		self.context = None
		"""
Secondary action context
		"""
		self.log_handler = None
		"""
The log_handler is called whenever debug messages should be logged or errors
happened.
		"""
		self.primary_action = True
		"""
True if action is the primary requested one
		"""
		self.request = None
		"""
Request instance
		"""
		self.response = None
		"""
Response instance
		"""
	#

	def __del__(self):
	#
		"""
Destructor __del__(direct_abstract_block)

:since: v0.1.00
		"""

		pass
	#

	def init(self, request, response):
	#
		"""
Initialize block from the given request and response.

:param request: Request object
:param response: Response object

:since: v0.1.00
		"""

		self.action = request.get_action()
		self.request = request
		self.response = response
	#

	def execute(self):
	#
		"""
Execute the requested action.

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("pas.http.core.block identified action '{0}'".format(self.action))
		py_method = "execute_{0}".format(re.sub("\W", "_", self.action))

		if (hasattr(self, py_method)):
		#
			py_method = getattr(self, py_method)
			py_method()
		#
		else:
		#
			if (self.primary_action and self.response.supports_headers()): self.response.set_header("HTTP/1.1", "HTTP/1.1 404 Not Found", True)
			raise direct_translatable_exception("core_unsupported_command", "Identified action '{0}' is not supported".format(self.action))
		#

		return self.action_result
	#

	def set_action(self, action, context = None):
	#
		"""
Sets an block action for execution.

:param action: Action requested
:param context: Action context

:since: v0.1.00
		"""

		self.action = action
		self.context = context
		self.primary_action = False
		self.request = direct_abstract_request.get_instance()
		self.response = direct_abstract_response.get_instance()
	#

	def set_action_result(self, result):
	#
		"""
Sets an action result.

:param result: Result to be returned for the action

:since: v0.1.00
		"""

		self.action_result = result
	#

	def set_log_handler(self, log_handler):
	#
		"""
Sets the log_handler.

:param log_handler: log_handler to use

:since: v0.1.00
		"""

		self.log_handler = log_handler
	#
#

##j## EOF