# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.controller.abstract_http_request
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

from dNG.data.rfc.http import direct_http
from dNG.pas.controller.abstract_inner_request import direct_abstract_inner_request
from dNG.pas.controller.predefined_http_request import direct_predefined_http_request
from dNG.pas.data.http.request_body import direct_request_body
from dNG.pas.data.http.request_headers_mixin import direct_request_headers_mixin
from dNG.pas.data.text.input_filter import direct_input_filter
from .abstract_request import direct_abstract_request

class direct_abstract_http_request(direct_abstract_request, direct_request_headers_mixin):
#
	"""
"direct_abstract_http_request" implements header related methods.

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
Constructor __init__(direct_abstract_http_request)

:since: v0.1.00
		"""

		direct_abstract_request.__init__(self)
		direct_request_headers_mixin.__init__(self)

		self.type = None
		"""
Request type
		"""

		self.server_scheme = "http"
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

	def get_type(self):
	#
		"""
Returns the request type.

:return: (str) Request type
:since:  v0.1.00
		"""

		return self.type
	#

	def init_response(self):
	#
		"""
Initializes the matching response instance.

:return: (object) Response object
:since:  v0.1.01
		"""

		response = direct_abstract_request.init_response(self)
		if (response.supports_headers() and self.type == "HEAD"): response.set_send_headers_only(True)
		return response
	#

	def parse_parameters(self):
	#
		"""
Parses request parameters.

:since: v0.1.00
		"""

		if (self.lang == ""):
		#
			lang = direct_input_filter.filter_control_chars(self.get_header("Accept-Language"))
			if (lang != None): self.lang = lang.lower().split(",", 1)[0]
		#

		direct_abstract_request.parse_parameters(self)
	#

	def parse_virtual_config(self, virtual_config, virtual_pathname):
	#
		"""
Parses the given virtual config and returns a matching inner request
instance.

:access: protected
:return: (object) Inner request instance; None if not matched
:since:  v0.1.01
		"""

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

		if (isinstance(inner_request, direct_abstract_inner_request)): inner_request.init(self)

		return inner_request
	#

	def set_header(self, name, value):
	#
		"""
Returns the request header if defined.

:param name: Header name

:return: (str) Header value if set; None otherwise
:since:  v0.1.00
		"""

		name = name.upper()

		if (name in self.headers): self.headers[name] = "{0},{1}".format(self.headers[name], value)
		else: self.headers[name] = value
	#

	def supports_accepted_formats(self):
	#
		"""
Returns false if accepted formats can not be identified.

:return: (bool) True if accepted formats are identified.
:since:  v0.1.00
		"""

		return True
	#

	def supports_compression(self):
	#
		"""
Returns false if supported compression formats can not be identified.

:return: (bool) True if compression formats are identified.
:since:  v0.1.01
		"""

		return True
	#

	def supports_headers(self):
	#
		"""
Returns false if the script name is not needed for execution.

:return: (bool) True if the request contains headers.
:since:  v0.1.00
		"""

		return True
	#

	def supports_listener_data(self):
	#
		"""
Returns false if the server address is unknown.

:return: (bool) True if listener are known.
:since:  v0.1.00
		"""

		return True
	#
#

##j## EOF