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

# pylint: disable=import-error,invalid-name,no-name-in-module

from os import path
from time import time, timezone
import os
import re

try: from urllib.parse import quote, unquote
except ImportError: from urllib import quote, unquote

from dNG.data.rfc.http import Http
from dNG.pas.data.settings import Settings
from dNG.pas.data.http.request_body import RequestBody
from dNG.pas.data.text.input_filter import InputFilter
from dNG.pas.data.text.l10n import L10n
from dNG.pas.module.named_loader import NamedLoader
from .abstract_http_mixin import AbstractHttpMixin
from .abstract_inner_request import AbstractInnerRequest
from .abstract_request import AbstractRequest
from .stdout_stream_response import StdoutStreamResponse

try:
#
	from dNG.pas.data.session.http_adapter import HttpAdapter as HttpSessionAdapter
	from dNG.pas.data.session.implementation import Implementation as SessionImplementation
#
except ImportError: SessionImplementation = None

class AbstractHttpRequest(AbstractRequest, AbstractHttpMixin):
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

	# pylint: disable=unused-argument

	RE_PARAMETER_DSD_PLUS_SPAM_CHAR = re.compile("(\\+){3,}")
	"""
RegExp to find more than 3 plus characters in a row
	"""
	RE_PARAMETER_FILTERED_CHARS = re.compile("[/\\\\\\?:@\\=\\&\\.]")
	"""
RegExp to find characters to be filtered out
	"""
	RE_PARAMETER_FILTERED_WORD_CHARS = re.compile("[;\\x20\\+]")
	"""
RegExp to find characters to be filtered out
	"""
	RE_PARAMETER_NON_WORD_END = re.compile("\\W+$")
	"""
RegExp to find non-word characters at the end of the string
	"""
	RE_PARAMETER_NON_WORD_START = re.compile("^\\W+")
	"""
RegExp to find non-word characters at the beginning of the string
	"""
	RE_PARAMETER_PLUS_CHAR = re.compile("\\+")
	"""
RegExp to find plus characters
	"""
	RE_PARAMETER_SPACE_CHAR = re.compile("\\x20")
	"""
RegExp to find space characters
	"""

	def __init__(self):
	#
		"""
Constructor __init__(AbstractHttpRequest)

:since: v0.1.00
		"""

		AbstractRequest.__init__(self)
		AbstractHttpMixin.__init__(self)

		self.body_fp = None
		"""
Request body pointer
		"""

		self.action = None
		"""
Requested action
		"""
		self.dsd = { }
		"""
Data transmitted with the request
		"""
		self.inner_request = None
		"""
A inner request is used to support protocols based on other ones (e.g.
JSON-RPC based on HTTP).
		"""
		self.module = None
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
		self.service = None
		"""
Requested service
		"""
		self.session = None
		"""
Associated session to request
		"""
		self.timezone = None
		"""
Source timezone
		"""
		self.output_handler = "http_xhtml"
		"""
Requested response format handler
		"""

		self.log_handler = NamedLoader.get_singleton("dNG.pas.data.logging.LogHandler", False)
		self.server_scheme = "http"

		self.supported_features['accepted_formats'] = True
		self.supported_features['compression'] = True
		self.supported_features['headers'] = True
		self.supported_features['type'] = self._supports_type
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

	def execute(self):
	#
		"""
Executes the incoming request.

:since: v0.1.00
		"""

		# pylint: disable=broad-except

		if (self.inner_request != None):
		#
			request = self.inner_request
			if (request.get_output_handler() != None): self.output_handler = request.get_output_handler()
		#
		else: request = self

		response = self._init_response()

		if (
			request.is_supported("type") and
			request.get_type() == "HEAD" and
			response.is_supported("headers")
		): response.set_send_headers_only(True)

		try:
		#
			if (self.is_supported("accepted_formats")):
			#
				accepted_formats = self.get_accepted_formats()
				if (len(accepted_formats) > 0): response.set_accepted_formats(accepted_formats)
			#

			if (self.is_supported("compression")):
			#
				compression_formats = self.get_compression_formats()
				if (len(compression_formats) > 0): response.set_compression_formats(compression_formats)
			#

			if (response.is_supported("script_name")): response.set_script_name(request.get_script_name())
			self._execute(request, response)
		#
		except Exception as handled_exception:
		#
			if (self.log_handler != None): self.log_handler.error(handled_exception)
			response.handle_exception(None, handled_exception)
		#

		self._respond(response)
	#

	def _execute(self, request, response):
	#
		"""
Executes the given request and generate content for the given response.

:since: v0.1.00
		"""

		requested_module = request.get_module()
		requested_service = "".join([word.capitalize() for word in request.get_service().split("_")])

		if (NamedLoader.is_defined("dNG.pas.module.blocks.{0}.{1}".format(requested_module, requested_service))):
		#
			instance = NamedLoader.get_instance("dNG.pas.module.blocks.{0}.{1}".format(requested_module, requested_service))
			if (self.log_handler != None): instance.set_log_handler(self.log_handler)

			instance.init(request, response)
			instance.execute()
			del(instance)
		#
		else:
		#
			if (NamedLoader.is_defined("dNG.pas.module.blocks.{0}.module".format(requested_module))):
			#
				instance = NamedLoader.get_instance("dNG.pas.module.blocks.{0}.module".format(requested_module))
				if (self.log_handler != None): instance.set_log_handler(self.log_handler)

				instance.init(request, response)
				del(instance)
			#

			self.handle_missing_service(response)
		#
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

	def get_dsd(self, key, default = None):
	#
		"""
Returns the DSD value for the specified parameter.

:param key: DSD key
:param default: Default value if not set

:return: (mixed) Requested DSD value or default one if undefined
:since:  v0.1.00
		"""

		return (self.dsd[key] if (self.is_dsd_set(key)) else default)
	#

	def get_dsd_dict(self):
	#
		"""
Return all DSD parameters received.

:return: (mixed) Request DSD values
:since:  v0.1.00
		"""

		return self.dsd
	#

	def get_inner_request(self):
	#
		"""
Returns the inner request instance.

:return: (object) Request instance; None if not available
:since:  v0.1.00
		"""

		return self.inner_request
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

	def get_output_handler(self):
	#
		"""
Returns the requested output format.

:return: (str) Requested output format
:since:  v0.1.00
		"""

		return self.output_handler
	#

	def _get_request_parameters(self):
	#
		"""
Returns the unparsed request parameters.

:return: (dict) Request parameters
:since:  v0.1.01
		"""

		return { }
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

	def get_service(self):
	#
		"""
Returns the requested service.

:return: (str) Requested service
:since:  v0.1.00
		"""

		return self.service
	#

	def get_session(self):
	#
		"""
Returns the associated session.

:return: (object) Session instance
:since:  v0.1.00
		"""

		return self.session
	#

	def handle_missing_service(self, response):
	#
		"""
"handle_missing_service()" is called if the requested service has not been
found.

:param response: Waiting response object

:since: v0.1.00
		"""

		if (response.is_supported("headers")): response.set_header("HTTP/1.1", "HTTP/1.1 404 Not Found", True)
		response.handle_critical_error("core_unsupported_command")
	#

	def init(self):
	#
		"""
Do preparations for request handling.

:since: v0.1.00
		"""

		"""
Set source variables. The server timezone will be changed if a user is
logged in and/or its timezone is identified.
		"""

		self._parse_parameters()
		self.timezone = float(Settings.get("core_timezone", (timezone / 3600)))
	#

	def _init_response(self):
	#
		"""
Initializes the matching response instance.

:return: (object) Response object
:since:  v0.1.01
		"""

		# pylint: disable=broad-except

		response = NamedLoader.get_instance("dNG.pas.controller.{0}Response".format("".join([word.capitalize() for word in self.output_handler.split("_")])))

		try:
		#
			if (SessionImplementation != None):
			#
				session_class = SessionImplementation.get_class()
				session_class.set_adapter(HttpSessionAdapter)

				session = session_class.load(session_create = False)

				if (session != None):
				#
					response.set_content_dynamic(True)
					self.set_session(session)

					user_profile = session.get_user_profile()
					if (user_profile != None): self.lang_default = user_profile.get_lang()
				#
			#
		#
		except Exception as handled_exception:
		#
			if (self.log_handler != None): self.log_handler.error(handled_exception)
		#

		if (self.lang == ""): self.lang = self.lang_default
		L10n.set_thread_lang(self.lang)

		L10n.init("core")
		L10n.init("pas_core")
		L10n.init("pas_http_core")

		if (self.log_handler != None): response.set_log_handler(self.log_handler)
		response.set_charset(L10n.get("lang_charset", "UTF-8"))
		response.set_stream_response(self._init_stream_response())

		if (response.is_supported("headers") and self.type == "HEAD"): response.set_send_headers_only(True)

		return response
	#

	def _init_stream_response(self):
	#
		"""
Initializes the matching stream response instance.

:return: (object) Stream response object
:since:  v0.1.00
		"""

		return StdoutStreamResponse()
	#

	def is_dsd_set(self, key):
	#
		"""
Returns true if the DSD for the specified parameter exists.

:param key: DSD key

:return: (bool) True if set
:since:  v0.1.01
		"""

		return (key in self.dsd)
	#

	def _parse_parameters(self):
	#
		"""
Parses request parameters.

:since: v0.1.00
		"""

		if (self.lang_default == ""):
		#
			lang = InputFilter.filter_control_chars(self.get_header("Accept-Language"))
			if (lang != None): self.lang_default = lang.lower().split(",", 1)[0]
		#

		self.parameters = self._get_request_parameters()

		self.action = (AbstractHttpRequest.filter_parameter_word(self.parameters['a']) if ("a" in self.parameters) else "")
		self.module = (AbstractHttpRequest.filter_parameter_word(self.parameters['m']) if ("m" in self.parameters) else "")
		self.service = (AbstractHttpRequest.filter_parameter_service(self.parameters['s']) if ("s" in self.parameters) else "")

		if ("dsd" in self.parameters): self.dsd = AbstractHttpRequest.parse_dsd(self.parameters['dsd'])
		if ("ohandler" in self.parameters and len(self.parameters['ohandler']) > 0): self.output_handler = AbstractHttpRequest.filter_parameter_word(self.parameters['ohandler'])

		"""
Initialize l10n
		"""

		lang = (AbstractHttpRequest.filter_parameter(self.parameters['lang']) if ("lang" in self.parameters) else "")

		if (lang != "" and os.access(path.normpath("{0}/{1}/core.json".format(Settings.get("path_lang"), lang)), os.R_OK)): self.lang = lang
		else:
		#
			if (self.lang_default == ""): lang_rfc_region = Settings.get("core_lang", "en_US")
			else: lang_rfc_region = self.lang_default.lower()

			lang_rfc_region = re.sub("\\W", "", lang_rfc_region)
			lang_domain = lang_rfc_region[:2]

			if (Settings.is_defined("pas_http_site_lang_{0}".format(lang_rfc_region))): lang_rfc_region = Settings.get("pas_http_site_lang_{0}".format(lang_rfc_region))
			elif (Settings.is_defined("pas_http_site_lang_{0}".format(lang_domain))): lang_domain = Settings.get("pas_http_site_lang_{0}".format(lang_domain))

			if (os.access(path.normpath("{0}/{1}/core.json".format(Settings.get("path_lang"), lang_rfc_region)), os.R_OK)): self.lang_default = lang_rfc_region
			elif (os.access(path.normpath("{0}/{1}/core.json".format(Settings.get("path_lang"), lang_domain)), os.R_OK)): self.lang_default = lang_domain
			else: self.lang_default = Settings.get("core_lang", "en")
		#

		"""
Set some standard values
		"""

		if (self.action == ""): self.action = "index"
		if (self.module == ""): self.module = "services"
		if (self.service == ""): self.service = "index"
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
			inner_request = NamedLoader.get_instance("dNG.pas.controller.PredefinedHttpRequest")

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

	def _respond(self, response):
	#
		"""
Respond the request with the given response.

:since: v0.1.01
		"""

		# pylint: disable=broad-except,star-args

		try:
		#
			if (self.session != None and self.session.is_active()):
			#
				user_profile = self.session.get_user_profile()

				if (user_profile != None):
				#
					user_profile_data = {
						"lang": self.lang,
						"lastvisit_time": time(),
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

		AbstractRequest._respond(self, response)
	#

	def set_dsd(self, key, value):
	#
		"""
Sets the DSD value for the specified parameter.

:param key: DSD key
:param default: DSD value

:since: v0.1.00
		"""

		self.dsd[key] = value
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

	def set_inner_request(self, request):
	#
		"""
Sets the inner request object.

:param request: Request object

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Request.set_inner_request(+request)- (#echo(__LINE__)#)")
		self.inner_request = request
	#

	def set_session(self, session):
	#
		"""
Sets the associated session.

:param session: (object) Session instance

:since: v0.1.00
		"""

		self.session = session
	#

	def _supports_type(self):
	#
		"""
Returns true if the request type is known.

:return: (bool) True if request type is known
:since:  v0.1.00
		"""

		return (self.get_type() != None)
	#

	@staticmethod
	def filter_parameter(value):
	#
		"""
Filters the given parameter value.

:param value: Request parameter

:return: (str) Filtered parameter
:since:  v0.1.01
		"""

		if (" " in value): value = quote(value)
		value = AbstractHttpRequest.RE_PARAMETER_NON_WORD_START.sub("", value)
		value = AbstractHttpRequest.RE_PARAMETER_FILTERED_CHARS.sub("", value)
		return AbstractHttpRequest.RE_PARAMETER_NON_WORD_END.sub("", value)
	#

	@staticmethod
	def filter_parameter_service(value):
	#
		"""
Filter service like parameters.

:param value: Request parameter

:return: (str) Filtered parameter
:since:  v0.1.01
		"""

		value = AbstractHttpRequest.filter_parameter(value)
		value = AbstractHttpRequest.RE_PARAMETER_PLUS_CHAR.sub(" ", value)
		return AbstractHttpRequest.RE_PARAMETER_SPACE_CHAR.sub(".", value)
	#

	@staticmethod
	def filter_parameter_word(value):
	#
		"""
Filter word parameters used for module and action statements.

:param value: Request parameter

:return: (str) Filtered parameter
:since:  v0.1.01
		"""

		value = AbstractHttpRequest.filter_parameter(value)
		return AbstractHttpRequest.RE_PARAMETER_FILTERED_WORD_CHARS.sub("", unquote(value))
	#

	@staticmethod
	def parse_dsd(dsd):
	#
		"""
DSD stands for dynamic service data and should be used for transfering IDs for
news, topics, ... Take care for injection attacks!

:param dsd: DSD string for parsing

:return: (dict) Parsed DSD
:since:  v0.1.00
		"""

		if (" " in dsd): dsd = quote(dsd)
		dsd = AbstractHttpRequest.RE_PARAMETER_DSD_PLUS_SPAM_CHAR.sub("++", dsd)

		dsd_list = dsd.split("++")
		_return = { }

		for dsd in dsd_list:
		#
			dsd_element = dsd.strip().split("+", 1)

			if (len(dsd_element) > 1): _return[dsd_element[0]] = InputFilter.filter_control_chars(unquote(dsd_element[1]))
			elif (len(dsd_element[0]) > 0): _return[dsd_element[0]] = ""
		#

		return _return
	#

	@staticmethod
	def parse_iline(iline):
	#
		"""
Parse the input variables given as an URI query string.

:param iline: Input query string with ";" delimiter.

:return: (dict) Parsed query string
:since:  v0.1.00
		"""

		_return = { }

		if (iline != None):
		#
			iline_list = iline.split(";")

			for iline in iline_list:
			#
				value_element = iline.split("=", 1)

				if (len(value_element) > 1): _return[value_element[0]] = value_element[1]
				elif ("ohandler" not in _return): _return['ohandler'] = re.sub("\\W+", "", iline)
			#
		#

		return _return
	#
#

##j## EOF