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

from os import path

class direct_abstract_inner_request(object):
#
	"""
This abstract class contains common methods for inner requests.

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
Constructor __init__(direct_abstract_inner_request)

:since: v0.1.00
		"""

		self.action = "index"
		"""
Requested action
		"""
		self.dsd = None
		"""
Data transmitted with the request
		"""
		self.module = "services"
		"""
Requested module block
		"""
		self.script_name = None
		"""
Called script
		"""
		self.script_pathname = None
		"""
Request path to the script
		"""
		self.server_host = None
		"""
Server hostname
		"""
		self.server_port = None
		"""
Server port
		"""
		self.server_scheme = "http"
		"""
Server scheme / protocol
		"""
		self.service = "index"
		"""
Requested service
		"""
		self.output_format = None
		"""
Requested response format name
		"""
	#

	def get_action(self):
	#
		"""
Returns the requested action.

:return: (str) Requested action
:since:  v0.1.00
		"""

		return self.action
	#

	def get_dsd(self, key, default = None):
	#
		"""
Returns the DSD value for the specified parameter.

:param key: DSD key
:param default: Default value if not set

:return: (mixed) Requested DSD value or default one if undefined
:since:  v0.1.00
		"""

		return (self.dsd[key] if (self.dsd != None and key in self.dsd) else default)
	#

	def get_module(self):
	#
		"""
Returns the requested module.

:return: (str) Requested module
:since:  v0.1.00
		"""

		return self.module
	#

	def get_output_format(self):
	#
		"""
Returns the requested output format.

:return: (str) Requested output format; None if not defined
:since:  v0.1.00
		"""

		return self.output_format
	#

	def get_script_name(self):
	#
		"""
Returns the script name.

:return: (str) Script name
:since:  v0.1.00
		"""

		return self.script_name
	#

	def get_script_pathname(self):
	#
		"""
Returns the script path and name of the request.

:return: (str) Script path and name
:since:  v0.1.00
		"""

		return self.script_pathname
	#

	def get_server_host(self):
	#
		"""
Returns the server hostname if any.

:return: (str) Server host; None if unknown or not applicable
:since:  v0.1.00
		"""

		return self.server_host
	#

	def get_server_port(self):
	#
		"""
Returns the server port if any.

:return: (int) Server port; None if unknown or not applicable
:since:  v0.1.00
		"""

		return self.server_port
	#

	def get_server_scheme(self):
	#
		"""
Returns the server scheme.

:return: (str) Server scheme / protocol; None if unknown
:since:  v0.1.00
		"""

		return self.server_scheme
	#

	def get_service(self):
	#
		"""
Returns the requested service.

:return: (str) Requested service
:since:  v0.1.00
		"""

		return self.service
	#

	def set_dsd(self, key, value):
	#
		"""
Sets the DSD value for the specified parameter.

:param key: DSD key
:param default: DSD value

:since: v0.1.00
		"""

		if (self.dsd == None): self.dsd = { key: value }
		else: self.dsd[key] = value
	#

	def set_script_pathname(self, script_pathname):
	#
		"""
Sets the script path and name of the request.

:param script_pathname: Script path and name

:since: v0.1.00
		"""

		self.script_name = path.basename(script_pathname)
		self.script_pathname = script_pathname
	#

	def set_server_host(self, host):
	#
		"""
Sets the server hostname for the inner request.

:param host: Server hostname

:since: v0.1.00
		"""

		self.server_host = host
	#

	def set_server_port(self, port):
	#
		"""
Sets the server port.

:param port: Server port

:since: v0.1.00
		"""

		self.server_port = port
	#

	def set_server_scheme(self, scheme):
	#
		"""
Sets the underlying server scheme.

:param scheme: Server scheme / protocol

:since: v0.1.00
		"""

		self.server_scheme = scheme
	#

	def supports_accepted_formats(self):
	#
		"""
Returns false if accepted formats can not be identified.

:return: (bool) True accepted formats are supported.
:since:  v0.1.00
		"""

		return False
	#

	def supports_headers(self):
	#
		"""
Returns false if the script name is not needed for execution.

:return: (bool) True if the request contains headers.
:since:  v0.1.00
		"""

		return False
	#

	def supports_listener_data(self):
	#
		"""
Returns false if the server address is unknown.

:return: (bool) True if listener are known.
:since:  v0.1.00
		"""

		return False
	#
#

##j## EOF