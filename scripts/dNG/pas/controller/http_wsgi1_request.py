# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.controller.HttpWsgi1Request
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
import re

from dNG.pas.controller.abstract_inner_request import AbstractInnerRequest
from dNG.pas.data.http.request_body_urlencoded import RequestBodyUrlencoded
from dNG.pas.data.http.virtual_config import VirtualConfig
from .abstract_http_request import AbstractHttpRequest
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
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
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

		if ("wsgi.version" not in wsgi_env or (wsgi_env['wsgi.version'] != ( 1, 0 ) and wsgi_env['wsgi.version'] != ( 1, 1 ))): raise RuntimeError("WSGI protocol unsupported")

		AbstractHttpRequest.__init__(self)

		self.http_wsgi_stream_response = None
		"""
The WSGI stream response instance
		"""
		self.query_string = ""
		"""
Request query string
		"""
		self.virtual_pathname = ""
		"""
Request path after the script
		"""

		for key in wsgi_env:
		#
			if (wsgi_env[key] != ""):
			#
				if (key.startswith("HTTP_")): self.set_header(key[5:].replace("_", "-"), wsgi_env[key])
				elif (key == "CONTENT_LENGTH" or key == "CONTENT_TYPE"): self.set_header(key.replace("_", "-"), wsgi_env[key])
				elif (key == "REMOTE_ADDR" and self.client_host == None): self.client_host = wsgi_env[key]
				elif (key == "REMOTE_HOST"): self.client_host = wsgi_env[key]
				elif (key == "REMOTE_PORT"): self.client_port = wsgi_env[key]
				elif (key == "REQUEST_METHOD"): self.type = wsgi_env[key]
				elif (key == "SCRIPT_NAME"): self.script_pathname = wsgi_env[key]
				elif (key == "QUERY_STRING"): self.query_string = wsgi_env[key]
				elif (key == "PATH_INFO"): self.virtual_pathname = wsgi_env[key]
				elif (key == "SERVER_NAME"): self.server_host = wsgi_env[key]
				elif (key == "SERVER_PORT"): self.server_port = int(wsgi_env[key])
			#
		#

		if ("HTTP_HOST" in wsgi_env):
		#
			host_parts = wsgi_env['HTTP_HOST'].rsplit(":", 2)

			if (len(host_parts) < 2 or host_parts[1][-1:] == "]"): self.server_host = wsgi_env['HTTP_HOST']
			else:
			#
				self.server_host = host_parts[0]
				self.server_port = int(host_parts[1])
			#
		#

		re_result = (None if (self.client_host == None) else re.match("^::ffff:(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)$", self.client_host))
		if (re_result != None): self.client_host = "{0}.{1}.{2}.{3}".format(re_result.group(1), re_result.group(2), re_result.group(3), re_result.group(4))

		wsgi_file_wrapper = (wsgi_env['wsgi.file_wrapper'] if ("wsgi.file_wrapper" in wsgi_env) else None)

		self.http_wsgi_stream_response = HttpWsgi1StreamResponse(wsgi_header_response, wsgi_file_wrapper)
		if ("SERVER_PROTOCOL" in wsgi_env and wsgi_env['SERVER_PROTOCOL'] == "HTTP/1.0"): self.http_wsgi_stream_response.set_http_version(1)

		self.body_fp = wsgi_env['wsgi.input']
		self.server_scheme = wsgi_env['wsgi.url_scheme']
		if (self.script_pathname == None): self.script_pathname = ""

		self.init()
		virtual_config = VirtualConfig.get_config(self.virtual_pathname)

		if (virtual_config == None and (self.virtual_pathname != "" or self.virtual_pathname == "/")):
		#
			virtual_config = VirtualConfig.get_config(self.script_pathname)
			virtual_pathname = self.script_pathname
		#
		else: virtual_pathname = self.virtual_pathname

		inner_request = self.parse_virtual_config(virtual_config, virtual_pathname)
		if (isinstance(inner_request, AbstractInnerRequest)): self.set_inner_request(inner_request)

		self.execute()
	#

	def __iter__(self):
	#
		"""
python.org: Return an iterator object.

:return: (object) Iterator object
:since:  v0.1.00
		"""

		http_wsgi_stream_response = self.http_wsgi_stream_response
		self.http_wsgi_stream_response = None

		return iter(http_wsgi_stream_response)
	#

	def get_stream_response(self):
	#
		"""
Returns the stream object output should go to.

:access: protected
:return: (object) Stream response object
:since:  v0.1.00
		"""

		return self.http_wsgi_stream_response
	#

	def iline_parse(self, iline = None):
	#
		"""
Parse the input variables given as an URI query string.

:param iline: Input query string with ";" delimiter.

:return: (dict) Parsed query string
:since:  v0.1.00
		"""

		if (iline == None): iline = self.query_string
		var_return = AbstractHttpRequest.iline_parse(self, iline)

		request_body = RequestBodyUrlencoded()
		request_body = self.configure_request_body(request_body, "application/x-www-form-urlencoded")

		if (request_body != None):
		#
			try: post_data = request_body.get_dict()
			except: post_data = { }

			for key in post_data: var_return[key] = post_data[key]
		#

		return var_return
	#

	def init(self):
	#
		"""
Do preparations for request handling.

:since: v0.1.00
		"""

		if ("ACCEPT-LANGUAGE" in self.headers): self.lang = self.headers['ACCEPT-LANGUAGE']
		self.script_name = path.basename(self.script_pathname)

		AbstractHttpRequest.init(self)
	#
#

##j## EOF