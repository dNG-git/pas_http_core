# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.controller.AbstractHttpRequest
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

from time import time

from dNG.data.rfc.http import Http
from dNG.pas.controller.abstract_inner_request import AbstractInnerRequest
from dNG.pas.controller.predefined_http_request import PredefinedHttpRequest
from dNG.pas.data.http.request_body import RequestBody
from dNG.pas.data.http.request_headers_mixin import RequestHeadersMixin
from dNG.pas.data.text.input_filter import InputFilter
from .abstract_request import AbstractRequest

try:
#
	from dNG.pas.data.session import Session
	from dNG.pas.data.session.http_adapter import HttpAdapter as HttpSessionAdapter
#
except ImportError: Session = None

class AbstractHttpRequest(AbstractRequest, RequestHeadersMixin):
#
	"""
"AbstractHttpRequest" implements HTTP request related methods.

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
Constructor __init__(AbstractHttpRequest)

:since: v0.1.00
		"""

		AbstractRequest.__init__(self)
		RequestHeadersMixin.__init__(self)

		self.body_fp = None
		"""
Request body pointer
		"""
		self.type = None
		"""
Request type
		"""

		self.server_scheme = "http"
	#

	def configure_request_body(self, request_body, content_type_expected = None):
	#
		"""
Configures the given RequestBody to be read by the Request implementation.

:param request_body: RequestBody instance
:param content_type_expected: Expected Content-Type header if any to use the
                              RequestBody instance.

:return: (object) Configured RequestBody instance
:since:  v0.1.00
		"""

		_return = None

		if (isinstance(request_body, RequestBody)):
		#
			if (content_type_expected != None):
			#
				content_type = InputFilter.filter_control_chars(self.get_header("Content-Type"))
				if (content_type != None): content_type = content_type.lower().split(";", 1)[0]
			#

			content_length = InputFilter.filter_int(self.get_header("Content-Length"))

			if (self.body_fp != None and (content_type_expected == None or (content_type != None and content_type == content_type_expected)) and ((content_length != None and content_length > 0) or "chunked" in Http.header_field_list(self.get_header("Transfer-Encoding")))):
			#
				if (content_length != None): request_body.set_input_size(content_length)
				else: request_body.define_input_chunk_encoded(True)

				content_encoding = self.get_header("Content-Encoding")
				if (content_encoding != None): request_body.define_input_compression(content_encoding)

				request_body.set_input_ptr(self.body_fp)
				self.body_fp = None
				_return = request_body
			#
		#

		return _return
	#

	def get_cookie(self, name):
	#
		"""
Returns the request cookie if defined.

:param name: Cookie name

:return: (str) Cookie value if set; None otherwise
:since:  v0.1.00
		"""

		cookies = self.get_cookies()
		return (cookies[name] if (name in cookies) else None)
	#

	def get_cookies(self):
	#
		"""
Returns request cookies.

:return: (dict) Request cookie name as key and value
:since:  v0.1.00
		"""

		_return = { }

		cookies = Http.header_field_list(InputFilter.filter_control_chars(self.get_header("Cookie")), ";", "=")
		for cookie in cookies: _return[cookie['key']] = cookie['value']

		return _return
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

	def init(self):
	#
		"""
Do preparations for request handling.

:since: v0.1.00
		"""

		if (Session != None): Session.set_adapter(HttpSessionAdapter)
		AbstractRequest.init(self)

		try:
		#
			if (Session != None):
			#
				session = Session.load(session_create = False)
				if (session != None): self.set_session(session)
			#
		#
		except Exception as handled_exception:
		#
			if (self.log_handler != None): self.log_handler.error(handled_exception)
		#
	#

	def _init_response(self):
	#
		"""
Initializes the matching response instance.

:return: (object) Response object
:since:  v0.1.01
		"""

		response = AbstractRequest._init_response(self)
		if (response.supports_headers() and self.type == "HEAD"): response.set_send_headers_only(True)
		return response
	#

	def _parse_parameters(self):
	#
		"""
Parses request parameters.

:since: v0.1.00
		"""

		if (self.lang == ""):
		#
			lang = InputFilter.filter_control_chars(self.get_header("Accept-Language"))
			if (lang != None): self.lang = lang.lower().split(",", 1)[0]
		#

		AbstractRequest._parse_parameters(self)
	#

	def _parse_virtual_config(self, virtual_config, virtual_pathname):
	#
		"""
Parses the given virtual config and returns a matching inner request
instance.

:return: (object) Inner request instance; None if not matched
:since:  v0.1.01
		"""

		if (virtual_config == None): inner_request = None
		elif ("setup_callback" in virtual_config):
		#
			if ("uri" in virtual_config):
			#
				uri = (virtual_pathname[len(virtual_config['uri_prefix']):] if ("uri_prefix" in virtual_config and virtual_pathname.lower().startswith(virtual_config['uri_prefix'])) else virtual_pathname)
				self.set_dsd(virtual_config['uri'], uri)
			#

			inner_request = virtual_config['setup_callback'](self, virtual_config)
		#
		elif ("m" in virtual_config or "s" in virtual_config or "a" in virtual_config or "uri" in virtual_config):
		#
			inner_request = PredefinedHttpRequest()

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

		if (isinstance(inner_request, AbstractInnerRequest)): inner_request.init(self)

		return inner_request
	#

	def respond(self, response):
	#
		"""
Respond the request with the given response.

:since: v0.1.01
		"""

		try:
		#
			if (self.session != None and self.session.is_active()):
			#
				user_profile = self.session.get_user_profile()

				if (user_profile != None):
				#
					user_profile_data = {
						"lang": self.lang,
						"lastvisit_time": int(time()),
						"lastvisit_ip": self.client_host
					}

					if ("theme" in self.parameters): user_profile_data['theme'] = self.parameters['theme']

					user_profile.data_set(**user_profile_data)
					user_profile.save()
				#

				self.session.save()
			#
		#
		except Exception as handled_exception:
		#
			if (self.log_handler != None): self.log_handler.error(handled_exception)
		#

		AbstractRequest.respond(self, response)
	#

	def set_header(self, name, value):
	#
		"""
Set the header with the given name and value.

:param name: Header name
:param value: Header value

:since: v0.1.00
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