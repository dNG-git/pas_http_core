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

from collections import Mapping
from os import path
import re

from dNG.pas.data.settings import Settings
from dNG.pas.data.http.virtual_config import VirtualConfig
from dNG.pas.runtime.io_exception import IOException
from .abstract_http_request import AbstractHttpRequest
from .abstract_inner_request import AbstractInnerRequest
from .http_wsgi1_stream_response import HttpWsgi1StreamResponse

class HttpWsgi1Request(AbstractHttpRequest):
#
	"""
"HttpWsgi1Request" takes a WSGI environment and the start response callback.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, wsgi_env, wsgi_header_response):
	#
		"""
Constructor __init__(HttpWsgi1Request)

:param wsgi_env: WSGI environment
:param wsgi_header_response: WSGI header response callback

:since: v0.1.00
		"""

		# pylint: disable=broad-except

		if ("wsgi.version" not in wsgi_env or (wsgi_env['wsgi.version'] not in ( ( 1, 0 ), ( 1, 1 ) ))): raise IOException("WSGI protocol unsupported")

		AbstractHttpRequest.__init__(self)

		self.http_wsgi_stream_response = None
		"""
The WSGI stream response instance
		"""
		self.virtual_pathname = ""
		"""
Request path after the script
		"""

		self.server_host = Settings.get("pas_http_server_forced_hostname")
		self.server_port = Settings.get("pas_http_server_forced_port")

		host_definition_headers = Settings.get("pas_http_server_host_definition_headers", [ "HTTP_HOST" ])

		for host_definition_header in host_definition_headers:
		#
			if (host_definition_header in wsgi_env):
			#
				host_parts = wsgi_env[host_definition_header].rsplit(":", 2)

				if (len(host_parts) < 2 or host_parts[1][-1:] == "]"): self.server_host = wsgi_env[host_definition_header]
				else:
				#
					self.server_host = host_parts[0]
					if (self.server_port is None): self.server_port = int(host_parts[1])
				#

				del(wsgi_env[host_definition_header])
				break
			#
		#

		if (self.server_host is None):
		#
			self.server_host = Settings.get("pas_http_server_preferred_hostname")
			if (self.server_port is None): self.server_port = Settings.get("pas_http_server_preferred_port")
		#

		for key in wsgi_env:
		#
			if (wsgi_env[key] != ""):
			#
				if (key[:5] == "HTTP_"): self.set_header(key[5:].replace("_", "-"), wsgi_env[key])
				elif (key == "CONTENT_LENGTH" or key == "CONTENT_TYPE"): self.set_header(key.replace("_", "-"), wsgi_env[key])
				elif (key == "REMOTE_ADDR" and self.client_host is None): self.client_host = wsgi_env[key]
				elif (key == "REMOTE_HOST"): self.client_host = wsgi_env[key]
				elif (key == "REMOTE_PORT"): self.client_port = wsgi_env[key]
				elif (key == "REQUEST_METHOD"): self.type = wsgi_env[key].upper()
				elif (key == "SCRIPT_NAME"): self.script_path_name = wsgi_env[key]
				elif (key == "QUERY_STRING"): self.query_string = wsgi_env[key]
				elif (key == "PATH_INFO"): self.virtual_pathname = wsgi_env[key]
				elif (self.server_host is None and key == "SERVER_NAME"): self.server_host = wsgi_env[key]
				elif (self.server_port is None and key == "SERVER_PORT"): self.server_port = int(wsgi_env[key])
			#
		#

		remote_address_headers = Settings.get("pas_http_server_remote_address_headers", [ ])

		for remote_address_header in remote_address_headers:
		#
			remote_address_header = remote_address_header.upper()

			remote_address_value = (wsgi_env[remote_address_header].strip()
			                        if (remote_address_header in wsgi_env
			                            and wsgi_env[remote_address_header] is not None
			                           ) else
			                        ""
			                       )

			if (remote_address_value != ""):
			#
				self.client_host = remote_address_value.split(",")[0]
				self.client_port = None
			#
		#

		re_result = (None if (self.client_host is None) else re.match("^::ffff:(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)$", self.client_host))
		if (re_result is not None): self.client_host = "{0}.{1}.{2}.{3}".format(re_result.group(1), re_result.group(2), re_result.group(3), re_result.group(4))

		try:
		#
			wsgi_file_wrapper = wsgi_env.get("wsgi.file_wrapper")

			self.http_wsgi_stream_response = HttpWsgi1StreamResponse(wsgi_header_response, wsgi_file_wrapper)
			if (wsgi_env.get("SERVER_PROTOCOL") == "HTTP/1.0"): self.http_wsgi_stream_response.set_http_version(1)

			self.body_fp = wsgi_env['wsgi.input']

			scheme_header = Settings.get("pas_http_server_scheme_header", "")
			self.server_scheme = (wsgi_env['wsgi.url_scheme'] if (scheme_header == "") else wsgi_env.get(scheme_header.upper().replace("-", "_")))

			if (self.script_path_name is None): self.script_path_name = ""

			self.init()

			virtual_config = VirtualConfig.get_config(self.virtual_pathname)

			if (virtual_config is None and self.virtual_pathname != ""):
			#
				virtual_config = VirtualConfig.get_config(self.script_path_name)
				virtual_pathname = self.script_path_name
			#
			else: virtual_pathname = self.virtual_pathname

			inner_request = self._parse_virtual_config(virtual_config, virtual_pathname)
			if (isinstance(inner_request, AbstractInnerRequest)): self.set_inner_request(inner_request)

			self.execute()
		#
		except Exception as handled_exception:
		#
			if (self.log_handler is not None): self.log_handler.error(handled_exception, "pas_http_core")

			# Died before output
			if (not self.http_wsgi_stream_response.are_headers_sent()):
			#
				self.http_wsgi_stream_response.set_header("HTTP/1.1", "HTTP/1.1 500 Internal Server Error", True)
				self.http_wsgi_stream_response.send_data("Internal Server Error")
			#
		#
	#

	def __iter__(self):
	#
		"""
python.org: Return an iterator object.

:return: (object) Iterator object
:since:  v0.1.00
		"""

		return iter(self.http_wsgi_stream_response)
	#

	def _get_request_parameters(self):
	#
		"""
Returns the unparsed request parameters.

:return: (dict) Request parameters
:since:  v0.1.01
		"""

		# pylint: disable=broad-except,no-member

		_return = AbstractHttpRequest.parse_iline(self.query_string)

		request_body = self.get_request_body(content_type_expected = "application/x-www-form-urlencoded")

		if (isinstance(request_body, Mapping)):
		#
			for key in request_body: _return[key] = request_body[key]
		#

		return _return
	#

	def init(self):
	#
		"""
Do preparations for request handling.

:since: v0.1.00
		"""

		self.script_name = path.basename(self.script_path_name)

		AbstractHttpRequest.init(self)
	#

	def _init_stream_response(self):
	#
		"""
Initializes the matching stream response instance.

:return: (object) Stream response object
:since:  v0.1.00
		"""

		return self.http_wsgi_stream_response
	#
#

##j## EOF