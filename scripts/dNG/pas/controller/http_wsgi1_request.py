# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.controller.http_wsgi1_request
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

from dNG.data.rfc.http import direct_http
from dNG.pas.controller.abstract_inner_request import direct_abstract_inner_request
from dNG.pas.controller.predefined_http_request import direct_predefined_http_request
from dNG.pas.data.http.request_body import direct_request_body
from dNG.pas.data.http.request_body_urlencoded import direct_request_body_urlencoded
from dNG.pas.data.text.input_filter import direct_input_filter
from dNG.pas.net.http.virtual_config import direct_virtual_config
from .abstract_http_request import direct_abstract_http_request
from .http_wsgi1_stream_response import direct_http_wsgi1_stream_response

class direct_http_wsgi1_request(direct_abstract_http_request, direct_virtual_config):
#
	"""
"direct_http_server" is responsible to start an HTTP aware server.

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
Constructor __init__(direct_wsgi1_request)

:param wsgi_env: WSGI environment
:param wsgi_header_response: WSGI header response callback

:since: v0.1.00
		"""

		if ("wsgi.version" not in wsgi_env or (wsgi_env['wsgi.version'] != ( 1, 0 ) and wsgi_env['wsgi.version'] != ( 1, 1 ))): raise RuntimeError("WSGI protocol unsupported")

		direct_abstract_http_request.__init__(self)

		self.body_fp = None
		"""
Request query string
		"""
		self.http_wsgi_stream_response = None
		"""
The WSGI header response callback
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

		self.body_fp = wsgi_env['wsgi.input']
		self.server_scheme = wsgi_env['wsgi.url_scheme']

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

		if (self.script_pathname == None): self.script_pathname = ""

		self.http_wsgi_stream_response = direct_http_wsgi1_stream_response(wsgi_header_response)
		if ("SERVER_PROTOCOL" in wsgi_env and wsgi_env['SERVER_PROTOCOL'] == "HTTP/1.0"): self.http_wsgi_stream_response.set_http_version(1)

		self.init()
		virtual_config = direct_virtual_config.get_config(self.virtual_pathname)

		if (virtual_config == None and (self.virtual_pathname != "" or self.virtual_pathname == "/")):
		#
			virtual_config = direct_virtual_config.get_config(self.script_pathname)
			virtual_pathname = self.script_pathname
		#
		else: virtual_pathname = self.virtual_pathname

		if (virtual_config == None): inner_request = None
		elif ("setup_function" in virtual_config):
		#
			if ("uri" in virtual_config):
			#
				uri = (virtual_pathname[len(virtual_config['uri_prefix']):] if ("uri_prefix" in virtual_config and virtual_pathname.lower().startswith(virtual_config['uri_prefix'])) else virtual_pathname)
				self.set_dsd(virtual_config['uri'], uri)
			#

			inner_request = virtual_config['setup_function'](self, virtual_config)
		#
		elif ("m" in virtual_config or "s" in virtual_config or "a" in virtual_config or "uri" in virtual_config):
		#
			inner_request = direct_predefined_http_request()

			if ("m" in virtual_config): inner_request.set_module(virtual_config['m'])
			if ("s" in virtual_config): inner_request.set_service(virtual_config['s'])
			if ("a" in virtual_config): inner_request.set_action(virtual_config['a'])

			if ("dsd" in virtual_config):
			#
				for key in virtual_config['dsd']: inner_request.set_dsd(key, virtual_config['dsd'][key])
			#

			if ("uri" in virtual_config):
			#
				uri = (virtual_pathname[len(virtual_config['uri_prefix']):] if ("uri_prefix" in virtual_config and virtual_pathname.lower().startswith(virtual_config['uri_prefix'])) else virtual_pathname)
				inner_request.set_dsd(virtual_config['uri'], uri)
			#
		#

		if (isinstance(inner_request, direct_abstract_inner_request)):
		#
			inner_request.init(self)
			self.set_inner_request(inner_request)
		#

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

		return http_wsgi_stream_response
	#

	def configure_request_body(self, request_body, content_type_expected = None):
	#
		"""
Parse the input variables given as an URI query string.

:param iline: Input query string with ";" delimiter.

:return: (dict) Parsed query string
:since:  v0.1.00
		"""

		var_return = None

		if (isinstance(request_body, direct_request_body)):
		#
			if (content_type_expected != None):
			#
				content_type = direct_input_filter.filter_control_chars(self.get_header("Content-Type"))
				if (content_type != None): content_type = content_type.lower().split(";", 1)[0]
			#

			content_length = direct_input_filter.filter_int(self.get_header("Content-Length"))

			if (self.body_fp != None and (content_type_expected == None or (content_type != None and content_type == content_type_expected)) and ((content_length != None and content_length > 0) or "chunked" in direct_http.header_field_list(self.get_header("Transfer-Encoding")))):
			#
				if (content_length != None): request_body.set_input_size(content_length)
				else: request_body.define_input_chunk_encoded(True)

				content_encoding = self.get_header("Content-Encoding")
				if (content_encoding != None): request_body.define_input_compression(content_encoding)

				request_body.set_input_ptr(self.body_fp)
				var_return = request_body
			#
		#

		return var_return
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
		var_return = direct_abstract_http_request.iline_parse(self, iline)

		request_body = direct_request_body_urlencoded()
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

		direct_abstract_http_request.init(self)
	#
#

##j## EOF