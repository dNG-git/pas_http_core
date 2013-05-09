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
from threading import local
from time import timezone
from weakref import proxy
import os, re

from dNG.pas.data.settings import direct_settings
from dNG.pas.data.text.input_filter import direct_input_filter
from dNG.pas.data.text.l10n import direct_l10n
from dNG.pas.module.named_loader import direct_named_loader
from .stdout_stream_response import direct_stdout_stream_response

try: from urllib import parse as urlparse
except ImportError: import urllib as urlparse

class direct_abstract_request(object):
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

	local = local()
	"""
Thread-local static object
	"""

	def __init__(self):
	#
		"""
Constructor __init__(direct_abstract_request)

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
The log_handler is called whenever debug messages should be logged or errors
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
		self.timezone = None
		"""
Source timezone
		"""
		self.output_format = "xhtml"
		"""
Requested response format name
		"""

		direct_abstract_request.local.instance = proxy(self)
	#

	def __del__(self):
	#
		"""
Destructor __del__(direct_abstract_request)

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.return_instance()
	#

	def execute(self):
	#
		"""
Executes the given request.

:since: v0.1.00
		"""

		self.log_handler = direct_named_loader.get_singleton("dNG.pas.data.logging.log_handler", False)

		direct_settings.set_log_handler(self.log_handler)

		direct_l10n.set_default_lang(self.lang)
		direct_l10n.set_log_handler(self.log_handler)

		direct_l10n.init("core")
		direct_l10n.init("pas_http_core")

		if (self.inner_request != None):
		#
			request = self.inner_request
			if (request.get_output_format() != None): self.output_format = request.get_output_format()
		#
		else: request = self

		response = direct_named_loader.get_instance("dNG.pas.controller.{0}_response".format(self.output_format))
		if (self.log_handler != None): response.set_log_handler(self.log_handler)
		response.set_charset(direct_l10n.get("lang_charset", "UTF-8"))
		response.set_stream_response(self.get_stream_response())

		try:
		#
			if (self.supports_accepted_formats()):
			#
				accepted_formats = self.get_accepted_formats()
				if (len(accepted_formats) > 0): response.set_accepted_formats(accepted_formats)
			#

			requested_module = request.get_module()
			if (response.supports_script_name()): response.set_script_name(request.get_script_name())

			requested_service = request.get_service()

			if (direct_named_loader.is_defined("dNG.pas.module.blocks.{0}.{1}".format(requested_module, requested_service))):
			#
				instance = direct_named_loader.get_instance("dNG.pas.module.blocks.{0}.{1}".format(requested_module, requested_service))
				if (self.log_handler != None): instance.set_log_handler(self.log_handler)
				instance.init(request, response)
				instance.execute()
			#
			else:
			#
				if (direct_named_loader.is_defined("dNG.pas.module.blocks.{0}.module".format(requested_module))):
				#
					instance = direct_named_loader.get_instance("dNG.pas.module.blocks.{0}.module".format(requested_module));
					if (self.log_handler != None): instance.set_log_handler(self.log_handler)
					instance.init(request, response)
				#

				if (response.supports_headers()): response.set_header("HTTP/1.1", "HTTP/1.1 404 Not Found", True)
				response.handle_critical_error("core_unsupported_command")
			#
		#
		except Exception as handled_exception:
		#
			if (self.log_handler != None): self.log_handler.error(handled_exception)
			response.handle_exception_error(None, handled_exception)
		#

		response.send()
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

		return (self.dsd[key] if (key in self.dsd) else default)
	#

	def get_dsd_dict(self):
	#
		"""
Return all DSD parameters received.

:return: (mixed) Request DSD values
:since:  v0.1.00
		"""

		return self.dsd.copy()
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

		return self.parameters.copy()
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

	def get_stream_response(self):
	#
		"""
Returns the stream object output should go to.

:access: protected
:return: (object) Stream response object
:since:  v0.1.00
		"""

		return direct_stdout_stream_response()
	#

	def iline_parse(self, iline = None):
	#
		"""
Parse the input variables given as an URI query string.

:param iline: Input query string with ";" delimiter.

:return: (dict) Parsed query string
:since:  v0.1.00
		"""

		var_return = { }

		if (iline != None):
		#
			iline_list = iline.split(";")

			for iline in iline_list:
			#
				value_element = iline.split("=", 1)

				if (len(value_element) > 1): var_return[value_element[0]] = value_element[1]
				elif ("ohandler" not in var_return): var_return['ohandler'] = re.sub("\W+", "", iline)
			#
		#

		return var_return
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

		self.parse_parameters()
		self.timezone = float(direct_settings.get("core_timezone", (timezone / 3600)))
	#

	def parse_dsd (self, dsd):
	#
		"""
DSD stands for dynamic service data and should be used for transfering IDs for
news, topics, ... Take care for injection attacks!

:param dsd: DSD string for parsing

:return: (dict) Parsed DSD
:since:  v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -request.parse_dsd(+dsd)- (#echo(__LINE__)#)")

		if (" " in dsd): dsd = urlparse.quote(dsd)
		dsd = re.sub("[\+]{3,}", "++", dsd, flags = re.I)

		dsd_list = dsd.split("++")
		var_return = { }

		for dsd in dsd_list:
		#
			dsd_element = dsd.strip().split("+", 1)

			if (len(dsd_element) > 1): var_return[dsd_element[0]] = direct_input_filter.filter_control_chars(urlparse.unquote(dsd_element[1]))
			elif (len(dsd_element[0]) > 0): var_return[dsd_element[0]] = ""
		#

		return var_return
	#

	def parse_parameters(self):
	#
		"""
Parses request parameters.

:since: v0.1.00
		"""

		self.parameters = self.iline_parse()

		self.action = (re.sub("[;\/\\\?:@\=\&\. \+]", "", urlparse.unquote(self.parameters['a'])) if ("a" in self.parameters) else "")
		self.module = (re.sub("[;\/\\\?:@\=\&\. \+]", "", self.parameters['m']) if ("m" in self.parameters) else "")

		if ("s" in self.parameters):
		#
			if (" " in self.parameters): self.parameters['s'] = urlparse.quote(self.parameters['s'])
			self.service = re.sub("[\+]", " ", self.parameters['s'])
			self.service = re.sub("^\W+", "", self.service)
			self.service = re.sub("[\/\\\?:@\=\&\.]", "", self.service)
			self.service = re.sub("\W+$", "", self.service)
			self.service = re.sub("\\x20", ".", self.service)
		#
		else: self.service = ""

		if ("dsd" in self.parameters): self.dsd = self.parse_dsd(self.parameters['dsd'])
		if ("ohandler" in self.parameters and len(self.parameters['ohandler']) > 0): self.output_handler = self.parameters['ohandler']

		"""
Initialize l10n
		"""

		if ("lang" in self.parameters and os.access(path.normpath("{0}/{1}/core.json".format(direct_settings.get("path_lang"), self.lang)), os.R_OK)): self.lang = self.parameters['lang']
		else:
		#
			if (self.lang == ""): lang_iso = direct_settings.get("core_lang", "en_US")
			else: lang_iso = self.lang.lower()

			lang_iso = re.sub("\\W", "", lang_iso)
			lang_domain = lang_iso[:2]

			if (direct_settings.is_defined("core_lang_{0}".format(lang_iso))): lang_iso = direct_settings.get("core_lang_{0}".format(lang_iso))
			elif (direct_settings.is_defined("core_lang_{0}".format(lang_domain))): lang_domain = direct_settings.get("core_lang_{0}".format(lang_domain))

			if (os.access(path.normpath("{0}/{1}/core.json".format(direct_settings.get("path_lang"), lang_iso)), os.R_OK)): self.lang = lang_iso
			elif (os.access(path.normpath("{0}/{1}/core.json".format(direct_settings.get("path_lang"), lang_domain)), os.R_OK)): self.lang = lang_domain
			else: self.lang = direct_settings.get("core_lang", "en")
		#

		"""
Set some standard values
		"""

		if (self.action == ""): self.action = "index"
		if (self.module == ""): self.module = "services"
		if (self.service == ""): self.service = "index"
	#

	def return_instance(self):
	#
		"""
This "return_instance()" implementation is a dummy as a thread-local weakref
is used for "get_instance()".

:since: v0.1.00
		"""

		pass
	#

	def set_dsd(self, key, value):
	#
		"""
Sets the DSD value for the specified parameter.

:param key: DSD key
:param default: DSD value

:since:  v0.1.00
		"""

		if (self.dsd == None): self.dsd = { key: value }
		else: self.dsd[key] = value
	#

	def set_inner_request(self, request):
	#
		"""
Sets the inner request object.

:param request: Request object

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -request.set_inner_request(+request)- (#echo(__LINE__)#)")
		self.inner_request = request
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

	@staticmethod
	def get_instance(count = False):
	#
		"""
Get the abstract_request singleton.

:param count: Count "get()" request

:return: (direct_abstract_request) Object on success
:since:  v0.1.00
		"""

		return (direct_abstract_request.local.instance if (hasattr(direct_abstract_request.local, "instance")) else None)
	#
#

##j## EOF