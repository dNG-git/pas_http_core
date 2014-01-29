# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.controller.AbstractRequest
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
from threading import local
from time import timezone
from weakref import ref
import os
import re

from dNG.pas.data.settings import Settings
from dNG.pas.data.translatable_exception import TranslatableException
from dNG.pas.data.text.input_filter import InputFilter
from dNG.pas.data.text.l10n import L10n
from dNG.pas.module.named_loader import NamedLoader
from .abstract_inner_request import AbstractInnerRequest
from .abstract_response import AbstractResponse
from .stdout_stream_response import StdoutStreamResponse

try: from urllib.parse import quote, unquote
except ImportError: from urllib import quote, unquote

class AbstractRequest(object):
#
	"""
This abstract class contains common methods for request implementations.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

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

	local = local()
	"""
Thread-local static object
	"""

	def __init__(self):
	#
		"""
Constructor __init__(AbstractRequest)

:since: v0.1.00
		"""

		self.action = None
		"""
Requested action
		"""
		self.client_host = None
		"""
Client host
		"""
		self.client_port = None
		"""
Client port
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
		self.lang = ""
		"""
Source language
		"""
		self.log_handler = None
		"""
The LogHandler is called whenever debug messages should be logged or errors
happened.
		"""
		self.module = None
		"""
Requested module block
		"""
		self.parameters = { }
		"""
Request parameters
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
Server host
		"""
		self.server_port = None
		"""
Server port
		"""
		self.server_scheme = "http"
		"""
Server scheme / protocol
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
		self.output_format = "http_xhtml"
		"""
Requested response format name
		"""

		AbstractRequest.local.weakref_instance = ref(self)
	#

	def execute(self):
	#
		"""
Executes the incoming request.

:since: v0.1.00
		"""

		self.log_handler = NamedLoader.get_singleton("dNG.pas.data.logging.LogHandler", False)
		Settings.set_log_handler(self.log_handler)

		L10n.set_thread_lang(self.lang)

		L10n.init("core")
		L10n.init("pas_core")
		L10n.init("pas_http_core")

		if (self.inner_request != None):
		#
			request = self.inner_request
			if (request.get_output_format() != None): self.output_format = request.get_output_format()
		#
		else: request = self

		response = self._init_response()

		try:
		#
			if (self.supports_accepted_formats()):
			#
				accepted_formats = self.get_accepted_formats()
				if (len(accepted_formats) > 0): response.set_accepted_formats(accepted_formats)
			#

			if (self.supports_compression()):
			#
				compression_formats = self.get_compression_formats()
				if (len(compression_formats) > 0): response.set_compression_formats(compression_formats)
			#

			if (response.supports_script_name()): response.set_script_name(request.get_script_name())
			self._execute(request, response)
		#
		except Exception as handled_exception:
		#
			if (self.log_handler != None): self.log_handler.error(handled_exception)
			response.handle_exception_error(None, handled_exception)
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
				instance = NamedLoader.get_instance("dNG.pas.module.blocks.{0}.module".format(requested_module));
				if (self.log_handler != None): instance.set_log_handler(self.log_handler)

				instance.init(request, response)
				del(instance)
			#

			self.handle_missing_service(response)
		#
	#

	def handle_missing_service(self, response):
	#
		"""
"handle_missing_service()" is called if the requested service has not been
found.

:param response: Waiting response object

:since: v0.1.00
		"""

		response.handle_critical_error("core_unsupported_command")
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

	def get_client_host(self):
	#
		"""
Returns the client host if any.

:return: (str) Client host; None if unknown or not applicable
:since:  v0.1.00
		"""

		return self.client_host
	#

	def get_client_port(self):
	#
		"""
Returns the client port if any.

:return: (int) Client port; None if unknown or not applicable
:since:  v0.1.00
		"""

		return self.client_port
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

	def get_lang(self):
	#
		"""
Returns the requested or supported language.

:return: (str) Requested l10n key
:since:  v0.1.00
		"""

		return self.lang
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

	def get_parameter(self, name, default = None):
	#
		"""
Returns the value for the specified parameter.

:param key: Parameter name
:param default: Default value if not set

:return: (mixed) Requested value or default one if undefined
:since:  v0.1.00
		"""

		return (self.parameters[name] if (name in self.parameters) else default)
	#

	def get_parameters(self):
	#
		"""
Return all parameters received.

:return: (mixed) Request parameters
:since:  v0.1.00
		"""

		return self.parameters
	#

	def get_output_format(self):
	#
		"""
Returns the requested output format.

:return: (str) Requested output format
:since:  v0.1.00
		"""

		return self.output_format
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

	def get_server_host(self):
	#
		"""
Returns the server host if any.

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

	def get_session(self):
	#
		"""
Returns the associated session.

:return: (object) Session instance
:since:  v0.1.00
		"""

		return self.session
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

		response = NamedLoader.get_instance("dNG.pas.controller.{0}Response".format("".join([word.capitalize() for word in self.output_format.split("_")])))
		if (self.log_handler != None): response.set_log_handler(self.log_handler)
		response.set_charset(L10n.get("lang_charset", "UTF-8"))
		response.set_stream_response(self._init_stream_response())

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

		self.parameters = self._get_request_parameters()

		self.action = (AbstractRequest.filter_parameter_word(self.parameters['a']) if ("a" in self.parameters) else "")
		self.module = (AbstractRequest.filter_parameter_word(self.parameters['m']) if ("m" in self.parameters) else "")
		self.service = (AbstractRequest.filter_parameter_service(self.parameters['s']) if ("s" in self.parameters) else "")

		if ("dsd" in self.parameters): self.dsd = AbstractRequest.parse_dsd(self.parameters['dsd'])
		if ("ohandler" in self.parameters and len(self.parameters['ohandler']) > 0): self.output_handler = AbstractRequest.filter_parameter_word(self.parameters['ohandler'])

		"""
Initialize l10n
		"""

		lang = (AbstractRequest.filter_parameter(self.parameters['lang']) if ("lang" in self.parameters) else "")

		if (lang != "" and os.access(path.normpath("{0}/{1}/core.json".format(Settings.get("path_lang"), lang)), os.R_OK)): self.lang = lang
		else:
		#
			if (self.lang == ""): lang_rfc_region = Settings.get("core_lang", "en_US")
			else: lang_rfc_region = self.lang.lower()

			lang_rfc_region = re.sub("\\W", "", lang_rfc_region)
			lang_domain = lang_rfc_region[:2]

			if (Settings.is_defined("core_lang_{0}".format(lang_rfc_region))): lang_rfc_region = Settings.get("core_lang_{0}".format(lang_rfc_region))
			elif (Settings.is_defined("core_lang_{0}".format(lang_domain))): lang_domain = Settings.get("core_lang_{0}".format(lang_domain))

			if (os.access(path.normpath("{0}/{1}/core.json".format(Settings.get("path_lang"), lang_rfc_region)), os.R_OK)): self.lang = lang_rfc_region
			elif (os.access(path.normpath("{0}/{1}/core.json".format(Settings.get("path_lang"), lang_domain)), os.R_OK)): self.lang = lang_domain
			else: self.lang = Settings.get("core_lang", "en")
		#

		"""
Set some standard values
		"""

		if (self.action == ""): self.action = "index"
		if (self.module == ""): self.module = "services"
		if (self.service == ""): self.service = "index"
	#

	def redirect(self, request, response = None):
	#
		"""
A request redirect executes the given new request as if it has been
requested by the client. It will reset the response and its cached values.

:param response: Waiting response object

:since: v0.1.00
		"""

		if (isinstance(request, AbstractInnerRequest)):
		#
			request.init(self)
			if (not isinstance(response, AbstractResponse)): response = AbstractResponse.get_instance()
			self._execute(request, response)
		#
		else: raise TranslatableException("core_unsupported_command")
	#

	def _respond(self, response):
	#
		"""
Reply the request with the given response.

:since: v0.1.01
		"""

		response.send()
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

	def set_log_handler(self, log_handler):
	#
		"""
Sets the LogHandler.

:param log_handler: LogHandler to use

:since: v0.1.00
		"""

		self.log_handler = log_handler
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

	def supports_accepted_formats(self):
	#
		"""
Returns false if accepted formats can not be identified.

:return: (bool) True if accepted formats are identified.
:since:  v0.1.00
		"""

		return False
	#

	def supports_compression(self):
	#
		"""
Returns false if supported compression formats can not be identified.

:return: (bool) True if compression formats are identified.
:since:  v0.1.01
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

	@staticmethod
	def filter_parameter(value):
	#
		"""
Filters the given parameter value.

:param value: Request parameter

:return: (str) Filtered parameter
:since:  v0.1.01
		"""

		if (" " in value): _return = quote(value)
		value = AbstractRequest.RE_PARAMETER_NON_WORD_START.sub("", value)
		value = AbstractRequest.RE_PARAMETER_FILTERED_CHARS.sub("", value)
		return AbstractRequest.RE_PARAMETER_NON_WORD_END.sub("", value)
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

		value = AbstractRequest.filter_parameter(value)
		value = AbstractRequest.RE_PARAMETER_PLUS_CHAR.sub(" ", value)
		return AbstractRequest.RE_PARAMETER_SPACE_CHAR.sub(".", value)
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

		value = AbstractRequest.filter_parameter(value)
		return AbstractRequest.RE_PARAMETER_FILTERED_WORD_CHARS.sub("", unquote(value))
	#

	@staticmethod
	def get_instance():
	#
		"""
Get the AbstractRequest singleton.

:return: (object) Object on success
:since:  v0.1.00
		"""

		return (AbstractRequest.local.weakref_instance() if (hasattr(AbstractRequest.local, "weakref_instance")) else None)
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
		dsd = AbstractRequest.RE_PARAMETER_DSD_PLUS_SPAM_CHAR.sub("++", dsd)

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