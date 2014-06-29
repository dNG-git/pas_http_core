# -*- coding: utf-8 -*-
##j## BOF

"""
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
"""

from os import path

from dNG.data.rfc.header import Header
from dNG.pas.data.translatable_exception import TranslatableException
from dNG.pas.data.text.input_filter import InputFilter
from .abstract_inner_request import AbstractInnerRequest
from .abstract_response import AbstractResponse

class AbstractHttpMixin(object):
#
	"""
"AbstractHttpMixin" is used to support common methods for HTTP request
instances.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(AbstractInnerHttpRequest)

:since: v0.1.01
		"""

		self.action = None
		"""
Requested action
		"""
		self.dsd = { }
		"""
Data transmitted with the request
		"""
		self.headers = { }
		"""
HTTP request headers
		"""
		self.lang = ""
		"""
User requested language
		"""
		self.lang_default = ""
		"""
Request based default language
		"""
		self.parent_request = None
		"""
Executable parent request
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
		self.type = None
		"""
Request type
		"""
		self.output_handler = "http_xhtml"
		"""
Requested response format handler
		"""

		self.server_scheme = "http"

		self.supported_features['accepted_formats'] = self._supports_accepted_formats
		self.supported_features['compression'] = self._supports_compression
		self.supported_features['headers'] = self._supports_headers
		self.supported_features['session'] = True
		self.supported_features['type'] = self._supports_type
	#

	def get_accepted_formats(self):
	#
		"""
Returns the formats the client accepts.

:return: (list) Accepted formats
:since:  v0.1.00
		"""

		_return = [ ]

		formats = self.get_header("Accept")
		if (formats != None): formats = Header.get_field_list_dict(formats, field_separator = None)
		if (formats == None): formats = [ ]

		for _format in formats: _return.append(_format.split(";")[0])

		return _return
	#

	def get_action(self):
	#
		"""
Returns the requested action.

:return: (str) Requested action
:since:  v0.1.00
		"""

		return ("index" if (self.action == None) else self.action)
	#

	def get_compression_formats(self):
	#
		"""
Returns the compression formats the client accepts.

:return: (list) Accepted compression formats
:since:  v0.1.01
		"""

		_return = [ ]

		formats = self.get_header("Accept-Encoding")
		if (formats != None): formats = Header.get_field_list_dict(formats, field_separator = None)
		if (formats == None): formats = [ ]

		for _format in formats: _return.append(_format.split(";")[0])

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

		cookies = Header.get_field_list_dict(InputFilter.filter_control_chars(self.get_header("Cookie")), ";", "=")
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

		return (self.dsd[key] if (self.is_dsd_set(key) and len(self.dsd[key]) > 0) else default)
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

	def get_header(self, name):
	#
		"""
Returns the request header if defined.

:param name: Header name

:return: (str) Header value if set; None otherwise
:since:  v0.1.00
		"""

		name = name.upper()
		return self.headers.get(name)
	#

	def get_headers(self):
	#
		"""
Returns the request headers as dict.

:return: (dict) Headers
:since:  v0.1.00
		"""

		return self.headers
	#

	def get_lang(self):
	#
		"""
Returns the requested or supported language.

:return: (str) Language identifier
:since:  v0.1.00
		"""

		return self.lang
	#

	def get_lang_default(self):
	#
		"""
Returns the default language.

:return: (str) Language identifier
:since:  v0.1.00
		"""

		return self.lang_default
	#

	def get_module(self):
	#
		"""
Returns the requested module.

:return: (str) Requested module
:since:  v0.1.00
		"""

		return ("services" if (self.module == None) else self.module)
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

		return ("index" if (self.service == None) else self.service)
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

	def get_type(self):
	#
		"""
Returns the request type.

:return: (str) Request type
:since:  v0.1.00
		"""

		return self.type
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

	def redirect(self, request, response = None):
	#
		"""
A request redirect executes the given new request as if it has been
requested by the client. It will reset the response and its cached values.

:param response: Waiting response object

:since: v0.1.01
		"""

		# pylint: disable=protected-access

		if (isinstance(request, AbstractInnerRequest)):
		#
			parent_request = (self if (self.parent_request == None) else self.parent_request)

			request.init(self)
			if (isinstance(request, AbstractHttpMixin)): request._set_parent_request(parent_request)

			if (not isinstance(response, AbstractResponse)): response = AbstractResponse.get_instance()

			parent_request._execute(request, response)
		#
		else: raise TranslatableException("core_unsupported_command")
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

	def set_dsd_dict(self, dsd_dict):
	#
		"""
Sets the DSD parameters dictionary.

:param dsd_dict: Request DSD values

:since: v0.1.01
		"""

		self.dsd = dsd_dict
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

		self.headers[name] = ("{0},{1}".format(self.headers[name], value)
		                      if (name in self.headers) else
		                      value
		                     )
	#

	def _set_parent_request(self, parent_request):
	#
		"""
Sets the parent request used for execution of chained requests.

:param parent_request: Executable parent request

:since: v0.1.01
		"""

		self.parent_request = parent_request
	#

	def set_script_pathname(self, script_pathname):
	#
		"""
Sets the script path and name of the request.

:param script_pathname: Script path and name

:since: v0.1.01
		"""

		if (script_pathname != None):
		#
			self.script_name = path.basename(script_pathname)
			self.script_pathname = script_pathname
		#
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

	def _supports_accepted_formats(self):
	#
		"""
Returns false if accepted formats can not be identified.

:return: (bool) True if accepted formats are identified.
:since:  v0.1.01
		"""

		return (self._supports_headers() and self.get_header("Accept") != None)
	#

	def _supports_compression(self):
	#
		"""
Returns false if supported compression formats can not be identified.

:return: (bool) True if compression formats are identified.
:since:  v0.1.01
		"""

		return (self._supports_headers() and self.get_header("Accept-Encoding") != None)
	#

	def _supports_headers(self):
	#
		"""
Returns false if headers are not received.

:return: (bool) True if the request contains headers.
:since:  v0.1.00
		"""

		return (self.headers != None)
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
#

##j## EOF