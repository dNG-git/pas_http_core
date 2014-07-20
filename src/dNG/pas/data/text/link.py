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

# pylint: disable=import-error,invalid-name,no-name-in-module

from collections import Iterable
from math import floor
import re

try: from urllib.parse import urlsplit
except ImportError: from urlparse import urlsplit

from dNG.pas.controller.abstract_http_request import AbstractHttpRequest
from dNG.pas.data.binary import Binary
from dNG.pas.data.settings import Settings
from dNG.pas.data.text.input_filter import InputFilter
from dNG.pas.runtime.value_exception import ValueException
from .uri import Uri

try: from dNG.pas.data.session.implementation import Implementation as SessionImplementation
except ImportError: SessionImplementation = None

class Link(Uri):
#
	"""
"Link" provides common methods to build them from parameters.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	# pylint: disable=unused-argument

	TYPE_ABSOLUTE = 1
	"""
Absolute URLs like "http://localhost/index.py?..."
	"""
	TYPE_BASE_PATH = 2
	"""
Generates URLs to the base path of this application.
	"""
	TYPE_OPTICAL = 4
	"""
Optical URLs are used to show the target address.
	"""
	TYPE_RELATIVE = 8
	"""
Relative URLs like "index.py?..."
	"""
	TYPE_VIRTUAL_PATH = 16
	"""
Generates absolute URLs based on the "__virtual__" path parameter.
	"""

	def __init__(self, scheme = None, host = None, port = None, path = None):
	#
		"""
Constructor __init__(Link)

:since: v0.1.01
		"""

		self.host = host
		"""
Override for the URL host
		"""
		self.path = path
		"""
Override for the URL path
		"""
		self.port = port
		"""
Override for the URL port
		"""
		self.scheme = scheme
		"""
Override for the URL scheme
		"""

		if (not Settings.is_defined("pas_http_site_preferred_url_base")): Settings.read_file("{0}/settings/pas_http.json".format(Settings.get("path_data")))
	#

	def _add_default_parameters(self, parameters):
	#
		"""
This method appends default parameters if not already set.

:param parameters: Parameters dict

:return: (dict) Appended parameters dict
:since:  v0.1.00
		"""

		_return = parameters
		request = None

		if ("lang" not in _return):
		#
			request = AbstractHttpRequest.get_instance()
			if (request != None and request.get_lang() != request.get_lang_default()): _return['lang'] = request.get_lang()
		#

		if ("uuid" not in _return and SessionImplementation != None):
		#
			if (request == None): request = AbstractHttpRequest.get_instance()
			session = (None if (request == None) else request.get_session())
			if (session != None and session.is_active() and (not session.is_persistent())): _return['uuid'] = SessionImplementation.get_class().get_uuid()
		#

		return _return
	#

	def build_url(self, _type, parameters = None):
	#
		"""
Builds an URL string. You may use internal links "index.py?...", external
links like "http://localhost/index.py?...", input (hidden) forms or an URL,
replacing parts of it if it's larger than x characters. This function uses
"shadow" URLs to be search engine friendly if applicable and the request URI
as a source for parameters.

:param _type: Link type (see constants)
:param parameters: Parameters dict
:param escape: True to URL escape input

:return: (str) Formatted URL string
:since:  v0.1.00
		"""

		if (type(_type) != int): _type = self.__class__.get_type_int(_type)

		_return = self.get_url_base(_type, parameters)

		if (parameters == None
		    or _type & Link.TYPE_BASE_PATH == Link.TYPE_BASE_PATH
		   ): parameters = { }
		else: parameters = self._filter_parameters(parameters)

		if (_type & Link.TYPE_VIRTUAL_PATH == Link.TYPE_VIRTUAL_PATH):
		#
			if (parameters == None or "__virtual__" not in parameters): raise ValueException("Virtual path URL requested but base path not defined")

			virtual_parameters = parameters.copy()

			virtual_base_path = (virtual_parameters['__virtual__'][1:]
			                     if (virtual_parameters['__virtual__'][:1] == "/") else
			                     virtual_parameters['__virtual__']
			                    )

			del(virtual_parameters['__virtual__'])

			dsds = virtual_parameters.get("dsd")
			if (dsds != None): del(virtual_parameters['dsd'])

			_return += virtual_base_path
			if (len(virtual_parameters) > 0): _return += "/" + self._build_url_formatted("{0}%20{1}", "/", virtual_parameters)
			if (dsds != None): _return += "/" + self._build_url_formatted("dsd%20{0}%20{1}", "/", dsds)
		#
		else:
		#
			parameters = self._add_default_parameters(parameters)

			if (len(parameters) > 0):
			#
				if ("?" not in _return): _return += "?"
				elif (_return[-1:] != ";"): _return += ";"

				_return += self._build_url_formatted("{0}={1}", ";", parameters)
			#
		#

		if (_type & Link.TYPE_OPTICAL == Link.TYPE_OPTICAL):
		#
			"""
A filter is required for really long URLs. First we will have a look at the
"optical maximal length" setting, then if the URL is larger than the setting
			"""

			length_available = int(Settings.get("pas_http_url_optical_max_length", 100))

			if (len(_return) > length_available):
			#
				url_elements = urlsplit(_return)

				_return = "{0}://".format(url_elements.scheme)
				if (url_elements.username != None or url_elements.password != None): _return += "{0}:{1}@".format(("" if (url_elements.username == None) else url_elements.username), ("" if (url_elements.password == None) else url_elements.password))
				_return += ("" if (url_elements.hostname == None) else url_elements.hostname)

				if (url_elements.port != None): _return += ":{0:d}".format(url_elements.port)
				path_length = len(url_elements.path)
				if (path_length > 0): basepath_position = (url_elements[:-1] if (url_elements[-1:] == "/") else url_elements).path.rfind("/")

				if (path_length > 0 and basepath_position > 0):
				#
					basepath_position += 1

					file_name = url_elements.path[basepath_position:]
					_return += url_elements.path[:basepath_position]
				#
				else: file_name = url_elements.path

				if (len(url_elements.query + url_elements.fragment) > 0):
				#
					one_eighth = int(floor((length_available - 3) / 8))
					one_fourth = one_eighth * 2
					three_eigths = length_available - (one_fourth * 2) - one_eighth

					"""
Now we will find out, how to remove unimportant parts of the given URL
					"""

					if (len(_return) < 3 + three_eigths + one_eighth):
					#
						"""
The URL (excluding the file name) is small enough. We will add the whole
string to our result
						"""

						length_available -= len(_return)
					#
					else:
					#
						"""
The source URL is too large - we will strip everything, that's larger than
our projected size
						"""

						_return = "{0} ... {1}".format(_return[:three_eigths], _return[-1 * one_eighth:])
						length_available -= 3 + three_eigths + one_eighth
					#

					"""
The next few lines will check the size of the filename and remove parts of
it if required
					"""

					if (len(file_name) < 3 + one_fourth):
					#
						"""
Again, the filename is small enough - no action is required
						"""

						_return += file_name
						length_available -= len(file_name)
					#
					else:
					#
						"""
Unfortunately, the filename is too long - we will remove the first part
						"""

						_return += " ... {0}".format(file_name[-1 * one_fourth])
						length_available -= 3 + one_fourth
					#

					"""
Our last step is to add the whole or the last part of the query string, once
more depending on the string length
					"""

					query_fragment = ""
					if (url_elements.query != ""): query_fragment += "?{0}".format(url_elements.query)
					if (url_elements.fragment != ""): query_fragment += "#{0}".format(url_elements.fragment)

					if (len(query_fragment) < 3 + length_available): _return += query_fragment
					else: _return += " ... {0}".format(query_fragment[-1 * length_available:])
				#
			#
		#

		return _return
	#

	def _build_url_formatted(self, link_template, link_separator, parameters, _escape = None):
	#
		"""
Builds a template-defined string containing the given URL parameters.

:param link_template: Link template
:param link_separator: Link separator
:param parameters: Parameters dict
:param _escape: Data escape method

:return: (str) Formatted URL string
:since:  v0.1.00
		"""

		# pylint: disable=protected-access

		_return = ""

		if (_escape == None): _escape = Link.encode_query_value

		for key in self.__class__._build_url_sorted_parameters(parameters.keys()):
		#
			escaped_key = _escape(key)
			value_type = type(parameters[key])

			if (key == "dsd"):
			#
				dsd_value = self._build_url_dsd_formatted(parameters[key], _escape)

				if (len(dsd_value) > 0):
				#
					if (_return != ""): _return += link_separator
					_return += link_template.format("dsd", dsd_value)
				#
			#
			elif (value_type == dict):
			#
				for value_key in parameters[key]:
				#
					escaped_key = "{0}[{1}]".format(_escape(key), _escape(value_key))
					escaped_value = _escape(parameters[key][value_key])

					if (_return != ""): _return += link_separator
					_return += link_template.format(escaped_key, escaped_value)
				#
			#
			elif (value_type == list):
			#
				for value in parameters[key]:
				#
					escaped_value = _escape(value)

					if (_return != ""): _return += link_separator
					_return += link_template.format("{0}[]".format(escaped_key), escaped_value)
				#
			#
			else:
			#
				escaped_value = _escape(parameters[key])

				if (_return != ""): _return += link_separator
				_return += link_template.format(escaped_key, escaped_value)
			#
		#

		return _return
	#

	def _build_url_dsd_formatted(self, parameters, _escape):
	#
		"""
Builds a URL DSD string.

:param parameters: Parameters dict
:param _escape: Data escape method

:return: (str) URL DSD string
:since:  v0.1.00
		"""

		_return = ""
		_type = type(parameters)

		if (_type == dict):
		#
			for key in sorted(parameters.keys()):
			#
				escaped_key = _escape(key)
				escaped_value = _escape(parameters[key])

				if (_return != ""): _return += "++"
				_return += "{0}+{1}".format(escaped_key, escaped_value)
			#
		#
		elif (_type == str): _return = parameters

		return _return
	#

	def _filter_parameters(self, parameters):
	#
		"""
This method filters all parameters of the type "__<KEYWORD>__".

:param parameters: Parameters dict

:return: (dict) Filtered parameters dict
:since:  v0.1.00
		"""

		_return = parameters.copy()

		if ("__query__" in _return):
		#
			if (len(_return) == 1 and len(_return['__query__']) > 0):
			#
				_return = AbstractHttpRequest.parse_iline(InputFilter.filter_control_chars(_return['__query__']))
				if ("dsd" in _return): _return['dsd'] = AbstractHttpRequest.parse_dsd(_return['dsd'])
			#
			else: del(_return['__query__'])
		#

		if (_return.get("__request__", False)):
		#
			request = AbstractHttpRequest.get_instance()
			inner_request = request.get_inner_request()
			if (inner_request != None): request = inner_request

			if (request != None):
			#
				if ("ohandler" not in _return): _return['ohandler'] = request.get_output_handler()
				if ("m" not in _return): _return['m'] = request.get_module()
				if ("s" not in _return): _return['s'] = request.get_service().replace(".", " ")
				if ("a" not in _return): _return['a'] = request.get_action()

				dsd_dict = request.get_dsd_dict()
				if (len(dsd_dict) and "dsd" not in _return): _return['dsd'] = { }

				for key in dsd_dict:
				#
					if (key not in _return['dsd']): _return['dsd'][key] = dsd_dict[key]
				#
			#

			del(_return['__request__'])
		#

		return self._filter_remove_parameters(_return)
	#

	def _filter_remove_parameters(self, parameters):
	#
		"""
This method removes all parameters marked as "__remove__" or special ones.

:param parameters: Parameters dict

:return: (dict) Filtered parameters dict
:since:  v0.1.00
		"""

		_return = parameters.copy()

		for key in parameters:
		#
			if (type(parameters[key]) == dict and len(parameters[key]) > 0): _return[key] = self._filter_remove_parameters(parameters[key])
			elif (parameters[key] == "__remove__"): del(_return[key])
		#

		if ("__host__" in parameters): del(_return['__host__'])
		if ("__path__" in parameters): del(_return['__path__'])
		if ("__port__" in parameters): del(_return['__port__'])
		if ("__scheme__" in parameters): del(_return['__scheme__'])

		return _return
	#

	def get_url_base(self, _type, parameters):
	#
		"""
Returns the base URL for the given type and parameters.

:param _type: Link type (see constants)
:param parameters: Link parameters

:return: (str) Base URL
:since:  v0.1.00
		"""

		_return = ""

		if (self.scheme != None and self.path != None):
		#
			_return = "{0}://".format(Binary.str(self.scheme))
			if (self.host != None): _return += Binary.str(self.host)

			if (self.port != None):
			#
				port = Link._filter_well_known_port(self.scheme, self.port)
				if (port > 0): _return += ":{0:d}".format(port)
			#

			path = ("/" if (self.path == None) else Binary.str(self.path))
			_return += ("/" if (path == "") else path)
		#
		else:
		#
			request = AbstractHttpRequest.get_instance()

			if (_type & Link.TYPE_ABSOLUTE == Link.TYPE_ABSOLUTE):
			#
				scheme = request.get_server_scheme()
				if (scheme == None): raise ValueException("Can't construct a full URL from the received request if it is not provided")

				_return = "{0}://".format(Binary.str(scheme))

				host = request.get_server_host()
				if (host != None): _return += Binary.str(host)

				port = Link._filter_well_known_port(scheme, request.get_server_port())
				if (port > 0): _return += ":{0:d}".format(port)

				if (_type & Link.TYPE_BASE_PATH == Link.TYPE_BASE_PATH
				    or _type & Link.TYPE_VIRTUAL_PATH == Link.TYPE_VIRTUAL_PATH
				   ): _return += self._get_url_path(request, False)
				else: _return += self._get_url_path(request)
			#
			else: _return = self._get_url_path(request)
		#

		return _return
	#

	def _get_url_path(self, request = None, include_script_name = True):
	#
		"""
Returns the base URL path for the given URL or the current handled one.

:return: (str) Base URL path
:since:  v0.1.01
		"""

		if (self.path == None):
		#
			if (request == None): request = AbstractHttpRequest.get_instance()
			script_name = request.get_script_name()

			if ((not include_script_name) or script_name == None): path = "/"
			else:
			#
				script_name = Binary.str(script_name)
				path = (script_name if (script_name[:1] == "/") else "/{0}".format(script_name))
			#
		#
		else: path = Binary.str(self.path)

		return ("/" if (path == "") else path)
	#

	@staticmethod
	def _build_url_sorted_parameters(parameter_keys):
	#
		"""
Builds a sorted list for the parameter key list given.

:param parameter_keys: Parameter key list

:return: (list) Sorted parameter key list
:since:  v0.1.00
		"""

		_return = [ ]

		if (isinstance(parameter_keys, Iterable)):
		#
			_return = sorted(parameter_keys)

			if ("a" in _return):
			#
				_return.remove("a")
				_return.insert(0, "a")
			#

			if ("s" in _return):
			#
				_return.remove("s")
				_return.insert(0, "s")
			#

			if ("m" in _return):
			#
				_return.remove("m")
				_return.insert(0, "m")
			#

			if ("lang" in _return):
			#
				_return.remove("lang")
				_return.append("lang")
			#

			if ("uuid" in _return):
			#
				_return.remove("uuid")
				_return.append("uuid")
			#
		#

		return _return
	#

	@staticmethod
	def _filter_well_known_port(scheme, port):
	#
		"""
Filter well known ports defined for the given scheme.

:param scheme: Scheme
:param port: Port number

:return: (int) Port not equal to zero if not specified for the given scheme
:since:  v0.1.01
		"""

		_return = 0

		if (port != None):
		#
			port = int(port)

			if ((scheme == "http" and port == 80)
			    or (scheme == "https" and port == 443)
			   ): _return = 0
			else: _return = port
		#

		return _return
	#

	@staticmethod
	def get_preferred(context = None):
	#
		"""
Returns a "Link" instance based on the defined preferred URL.

:param context: Context for the preferred link

:return: (object) Link instance
:since:  v0.1.01
		"""

		if (not Settings.is_defined("pas_http_site_preferred_url_base")): Settings.read_file("{0}/settings/pas_http.json".format(Settings.get("path_data")))

		url = None

		if (context != None): url = Settings.get("pas_http_site_preferred_url_base_{0}".format(re.sub("\\W+", "_", context)))
		if (url == None): url = Settings.get("pas_http_site_preferred_url_base")

		if (url == None): raise ValueException("Preferred URL base setting is not defined")
		url_elements = urlsplit(url)

		return Link(url_elements.scheme, url_elements.hostname, url_elements.port, url_elements.path)
	#

	@staticmethod
	def get_type_int(_type):
	#
		"""
Parses the given type parameter given as a string value.

:param _type: String type

:return: (int) Internal type
:since:  v0.1.01
		"""

		_return = 0

		type_set = _type.split("+")

		for _type in type_set:
		#
			if (_type == "elink"): _return |= Link.TYPE_ABSOLUTE
			elif (_type == "ilink"): _return |= Link.TYPE_RELATIVE
			elif (_type == "optical"): _return |= Link.TYPE_OPTICAL
			elif (_type == "vlink"): _return |= Link.TYPE_VIRTUAL_PATH
		#

		return _return
	#
#

##j## EOF