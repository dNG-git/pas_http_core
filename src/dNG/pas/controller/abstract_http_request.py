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

# pylint: disable=import-error,invalid-name,no-name-in-module

from os import path
from time import time, timezone
import os
import re

try: from urllib.parse import quote, unquote
except ImportError: from urllib import quote, unquote

from dNG.data.rfc.header import Header
from dNG.pas.data.settings import Settings
from dNG.pas.data.http.request_body import RequestBody
from dNG.pas.data.http.request_body_multipart import RequestBodyMultipart
from dNG.pas.data.http.request_body_urlencoded import RequestBodyUrlencoded
from dNG.pas.data.text.input_filter import InputFilter
from dNG.pas.data.text.l10n import L10n
from dNG.pas.database.transaction_context import TransactionContext
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.plugins.hook import Hook
from dNG.pas.runtime.exception_log_trap import ExceptionLogTrap
from .abstract_http_mixin import AbstractHttpMixin
from .abstract_inner_request import AbstractInnerRequest
from .abstract_request import AbstractRequest
from .stdout_stream_response import StdoutStreamResponse

try:
#
	from dNG.pas.data.session.http_adapter import HttpAdapter as HttpSessionAdapter
	from dNG.pas.data.session.implementation import Implementation as Session
#
except ImportError: Session = None

class AbstractHttpRequest(AbstractRequest, AbstractHttpMixin):
#
	"""
"AbstractHttpRequest" implements HTTP request related methods.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
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
	RE_PARAMETER_PLUS_ENCODED_CHAR = re.compile("%2b", re.I)
	"""
RegExp to find URL-encoded plus characters
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
		self.inner_request = None
		"""
A inner request is used to support protocols based on other ones (e.g.
JSON-RPC based on HTTP).
		"""
		self.query_string = ""
		"""
Request query string
		"""
		self.session = None
		"""
Associated session to request
		"""

		self.log_handler = NamedLoader.get_singleton("dNG.pas.data.logging.LogHandler", False)

		self.supported_features['inner_request'] = True
		self.supported_features['query_string'] = True
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

		if (request.is_supported("type")
		    and request.get_type() == "HEAD"
		    and response.is_supported("headers")
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

			if (Settings.get("pas_http_site_events_call_on_execute", False)): Hook.call("dNG.pas.http.Request.onExecute", request = request, response = response)
			self._execute(request, response)
		#
		except Exception as handled_exception:
		#
			if (self.log_handler != None): self.log_handler.error(handled_exception, context = "pas_http_core")
			response.handle_exception(None, handled_exception)
		#

		if (Settings.get("pas_http_site_events_call_on_reponse", False)): Hook.call("dNG.pas.http.Request.onResponse", request = request, response = response)
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

		if (self.log_handler != None): self.log_handler.debug("{0!r} has been called for 'dNG.pas.module.controller.{1}.{2}'", self, requested_module, requested_service, context = "pas_http_core")

		if (NamedLoader.is_defined("dNG.pas.module.controller.{0}.{1}".format(requested_module, requested_service))):
		#
			instance = NamedLoader.get_instance("dNG.pas.module.controller.{0}.{1}".format(requested_module, requested_service))
			instance.init(request, response)
			instance.execute()

			del(instance)
		#
		else:
		#
			if (NamedLoader.is_defined("dNG.pas.module.controller.{0}.Module".format(requested_module))):
			#
				instance = NamedLoader.get_instance("dNG.pas.module.controller.{0}.Module".format(requested_module))
				instance.init(request, response)

				del(instance)
			#

			self.handle_missing_service(response)
		#
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

	def get_query_string(self):
	#
		"""
Returns the raw request query string.

:return: (str) Raw query string
:since:  v0.1.01
		"""

		return self.query_string
	#

	def get_request_body(self, request_body_instance = None, content_type_expected = None):
	#
		"""
Returns a configured RequestBody instance to be read by the Request
implementation.

:param request_body_instance: RequestBody instance to be configured
:param content_type_expected: Expected Content-Type header if any to use the
                              RequestBody instance.

:return: (object) Configured RequestBody instance
:since:  v0.1.00
		"""

		content_type = InputFilter.filter_control_chars(self.get_header("Content-Type"))
		if (content_type != None): content_type = content_type.split(";", 1)[0].lower()

		_return = (self._init_request_body(content_type)
		           if (request_body_instance == None) else
		           request_body_instance
		          )

		if (isinstance(_return, RequestBody)):
		#
			content_length = InputFilter.filter_int(self.get_header("Content-Length"))

			if (self.body_fp != None
			    and (content_type_expected == None or (content_type != None and content_type == content_type_expected))
			    and ((content_length != None and content_length > 0)
			         or "chunked" in Header.get_field_list_dict(self.get_header("Transfer-Encoding"))
			        )
			   ):
			#
				if (content_length != None): _return.set_input_size(content_length)
				else: _return.define_input_chunk_encoded(True)

				content_encoding = self.get_header("Content-Encoding")
				if (content_encoding != None): _return.define_input_compression(content_encoding)

				_return.set_headers(self.get_headers())
				_return.set_input_ptr(self.body_fp)

				self.body_fp = None
			#
		#

		return _return
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

	def _init_request_body(self, content_type):
	#
		"""
Returns the RequestBody instance to be read by the Request implementation
matching the given content type.

:param content_type: Content type to be handled by the RequestBody instance

:return: (object) RequestBody instance; None if not supported
:since:  v0.1.00
		"""

		_return = None

		if (content_type == "application/x-www-form-urlencoded"): _return = RequestBodyUrlencoded()
		elif (content_type[:10] == "multipart/"): _return = RequestBodyMultipart()
		elif (self.get_header("Content-Length") != None
		      or self.get_header("Transfer-Encoding") != None
		     ): _return = RequestBody()

		return _return
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

		with ExceptionLogTrap("pas_http_core"):
		#
			session = self.get_session()
			session_class = (None if (Session == None) else Session.get_class())

			if (session_class != None):
			#
				session_class.set_adapter(HttpSessionAdapter)

				if (session == None):
				#
					session = Session.get_class().load(session_create = False)
					self.set_session(session)
				#
				else: session.set_thread_default()
			#

			if (session != None):
			#
				response.set_content_dynamic(True)

				user_profile = session.get_user_profile()
				if (user_profile != None): self.lang_default = user_profile.get_lang()
			#
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

		if ("a" in self.parameters): self.action = AbstractHttpRequest.filter_parameter_word(self.parameters['a'])
		if ("m" in self.parameters): self.module = AbstractHttpRequest.filter_parameter_word(self.parameters['m'])
		if ("s" in self.parameters): self.service = AbstractHttpRequest.filter_parameter_service(self.parameters['s'])

		if ("dsd" in self.parameters): self.dsd = AbstractHttpRequest.parse_dsd(self.parameters['dsd'])

		if ("ohandler" in self.parameters
		    and len(self.parameters['ohandler']) > 0
		   ): self.output_handler = AbstractHttpRequest.filter_parameter_word(self.parameters['ohandler'])

		"""
Initialize l10n
		"""

		lang = (AbstractHttpRequest.filter_parameter(self.parameters['lang']) if ("lang" in self.parameters) else "")

		if (lang != "" and os.access(path.join(Settings.get("path_lang"), lang, "core.json"), os.R_OK)): self.lang = lang
		else:
		#
			if (self.lang_default == ""): lang_rfc_region = Settings.get("core_lang", "en_US")
			else: lang_rfc_region = self.lang_default.lower()

			lang_rfc_region = re.sub("\\W", "", lang_rfc_region)
			lang_domain = lang_rfc_region[:2]

			if (Settings.is_defined("pas_http_site_lang_{0}".format(lang_rfc_region))): lang_rfc_region = Settings.get("pas_http_site_lang_{0}".format(lang_rfc_region))
			elif (Settings.is_defined("pas_http_site_lang_{0}".format(lang_domain))): lang_domain = Settings.get("pas_http_site_lang_{0}".format(lang_domain))

			if (os.access(path.join(Settings.get("path_lang"), lang_rfc_region, "core.json"), os.R_OK)): self.lang_default = lang_rfc_region
			elif (os.access(path.join(Settings.get("path_lang"), lang_domain, "core.json"), os.R_OK)): self.lang_default = lang_domain
			else: self.lang_default = Settings.get("core_lang", "en")
		#
	#

	def _parse_virtual_config(self, virtual_config, virtual_pathname):
	#
		"""
Parses the given virtual config and returns a matching inner request
instance.

:return: (object) Inner request instance; None if not matched
:since:  v0.1.01
		"""

		if (virtual_config == None): _return = None
		elif ("path_parameters" in virtual_config and virtual_config['path_parameters']):
		#
			_return = NamedLoader.get_instance("dNG.pas.controller.PredefinedHttpRequest")

			encoded_parameters = virtual_pathname[len(virtual_config['_path_prefix']):].split("/")

			parameters = { }
			dsds = { }

			for encoded_parameter in encoded_parameters:
			#
				parameter = encoded_parameter.split(" ", 2)

				if (len(parameter) == 2): parameters[unquote(parameter[0])] = unquote(parameter[1])
				elif (len(parameter) == 3 and parameter[0] == "dsd"): dsds[unquote(parameter[1])] = unquote(parameter[2])
			#

			if ("m" in virtual_config): _return.set_module(virtual_config['m'])
			elif ("m" in parameters): _return.set_module(parameters['m'])

			if ("s" in virtual_config): _return.set_service(virtual_config['s'])
			elif ("s" in parameters): _return.set_service(parameters['s'])

			if ("a" in virtual_config): _return.set_action(virtual_config['a'])
			elif ("a" in parameters): _return.set_action(parameters['a'])

			for key in dsds: _return.set_dsd(key, dsds[key])
		#
		elif ("setup_callback" in virtual_config):
		#
			if ("path" in virtual_config):
			#
				path = (virtual_pathname[len(virtual_config['_path_prefix']):]
				        if ("_path_prefix" in virtual_config and virtual_pathname.lower().startswith(virtual_config['_path_prefix'])) else
				        virtual_pathname
				       )

				self.set_dsd(virtual_config['path'], path)
			#

			_return = virtual_config['setup_callback'](self, virtual_config)
		#
		elif ("m" in virtual_config or "s" in virtual_config or "a" in virtual_config or "path" in virtual_config):
		#
			_return = NamedLoader.get_instance("dNG.pas.controller.PredefinedHttpRequest")

			if ("m" in virtual_config): _return.set_module(virtual_config['m'])
			if ("s" in virtual_config): _return.set_service(virtual_config['s'])
			if ("a" in virtual_config): _return.set_action(virtual_config['a'])

			if ("dsd" in virtual_config and isinstance(virtual_config['dsd'], dict)):
			#
				for key in virtual_config['dsd']: _return.set_dsd(key, virtual_config['dsd'][key])
			#

			if ("path" in virtual_config):
			#
				path = (virtual_pathname[len(virtual_config['_path_prefix']):]
				        if ("_path_prefix" in virtual_config and virtual_pathname.lower().startswith(virtual_config['_path_prefix'])) else
				        virtual_pathname
				       )

				_return.set_dsd(virtual_config['path'], path)
			#
		#

		if (isinstance(_return, AbstractInnerRequest)): _return.init(self)

		return _return
	#

	def _respond(self, response):
	#
		"""
Respond the request with the given response.

:since: v0.1.01
		"""

		# pylint: disable=broad-except,star-args

		with ExceptionLogTrap("pas_http_core"):
		#
			if (self.session != None and self.session.is_active()):
			#
				user_profile = self.session.get_user_profile()

				if (user_profile != None):
				#
					user_profile_data = { "lang": self.lang,
					                      "lastvisit_time": time(),
					                      "lastvisit_ip": self.client_host
					                    }

					if ("theme" in self.parameters): user_profile_data['theme'] = self.parameters['theme']

					with TransactionContext():
					#
						user_profile.set_data_attributes(**user_profile_data)
						user_profile.save()

						self.session.save()
					#
				#
			#
		#

		AbstractRequest._respond(self, response)
	#

	def set_inner_request(self, request):
	#
		"""
Sets the inner request object.

:param request: Request object

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_inner_request()- (#echo(__LINE__)#)", self, context = "pas_http_core")
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

		if ("+" not in dsd and AbstractHttpRequest.RE_PARAMETER_PLUS_ENCODED_CHAR.search(dsd) != None): dsd = unquote(dsd)
		elif (" " in dsd): dsd = quote(dsd)

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