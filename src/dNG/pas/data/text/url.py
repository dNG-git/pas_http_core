# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.Url
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

from math import floor

try: from urllib.parse import quote, unquote, urlsplit
except ImportError:
#
	from urllib import quote, unquote
	from urlparse import urlsplit
#

from dNG.pas.controller.abstract_request import AbstractRequest
from dNG.pas.data.binary import Binary
from dNG.pas.data.settings import Settings
from dNG.pas.data.traced_exception import TracedException
from dNG.pas.data.text.input_filter import InputFilter

try: from dNG.pas.data.session import Session
except ImportError: Session = None

class Url(object):
#
	"""
"Url" provides common methods to build them from parameters.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	TYPE_FULL = 1
	"""
Full URLs like "http://localhost/index.py?..."
	"""
	TYPE_OPTICAL = 2
	"""
Optical URLs are used to show the target address.
	"""
	TYPE_RELATIVE = 4
	"""
Relative URLs like "index.py?..."
	"""

	def __init__(self, scheme = None, host = None, port = None, path = None):
	#
		"""
Constructor __init__(Url)

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
	#

	def build_url(self, _type, parameters, _escape = None):
	#
		"""
Builds an URL string. You may use internal links "index.py?...", external
links like "http://localhost/index.py?...", input (hidden) forms or an URL,
replacing parts of it if it's larger than x characters. This function uses
"shadow" URLs to be search engine friendly if applicable and the request URI
as a source for parameters.

:param _type: Link type (see constants)
:param parameters: Parameters dict
:param _escape: Data escape method

:return: (str) Formatted URL string
:since:  v0.1.00
		"""

		if (type(_type) != int): _type = self._get_type(_type)
		_return = self.get_url_base(_type, parameters)

		parameters = self._parameters_filter(parameters)
		parameters = self._parameters_append_defaults(parameters)

		if (len(parameters) > 0):
		#
			if ("?" not in _return): _return += "?"
			elif (_return[-1:] != ";"): _return += ";"

			_return += self._build_url_formatted("{0}={1}", ";", parameters, _escape = None)
		#

		if (_type & Url.TYPE_OPTICAL == Url.TYPE_OPTICAL):
		#
			"""
A filter is required for really long URLs. First we will have a look at the
"optical maximal length" setting, then if the URL is larger than the setting
			"""

			length_available = int(Settings.get("pas_html_url_optical_max_length", 100))

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

		_return = ""

		if (_escape == None): _escape = Url.escape

		for key in parameters:
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

		if (type(parameters) == dict):
		#
			for key in parameters:
			#
				if (len(parameters[key]) > 0):
				#
					escaped_key = _escape(key)
					escaped_value = _escape(parameters[key])

					if (_return != ""): _return += "++"
					_return += "{0}+{1}".format(escaped_key, escaped_value)
				#
			#
		#

		return _return
	#

	def _get_type(self, _type):
	#
		"""
Parses the given type parameter given as a string value.

:param _type: String type

:return: (int) Internal type
:since:  v0.1.01
		"""

		if (_type == "elink"): _return = Url.TYPE_FULL
		elif (_type == "ilink"): _return = Url.TYPE_RELATIVE
		elif (_type == "optical"): _return = Url.TYPE_OPTICAL
		else: _return = 0

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
			if (self.port != None): _return += ":{0}".format(Binary.str(self.port))
			_return += Binary.str(self.path)
		#
		else:
		#
			request = AbstractRequest.get_instance()

			if (_type == Url.TYPE_RELATIVE):
			#
				if (self.path == None):
				#
					script_name = request.get_script_name()
					if (script_name != None): _return = Binary.str(script_name)
				#
				else: _return = Binary.str(self.path)
			#
			else:
			#
				scheme = request.get_server_scheme()
				host = request.get_server_host()
				port = request.get_server_port()
				script_pathname = request.get_script_pathname()

				if (scheme == None or (self.path == None and script_pathname == None)): raise TracedException("Can't construct a full URL from the received request if it is not provided")

				_return = "{0}://".format(Binary.str(scheme))
				if (host != None): _return += Binary.str(host)
				if (port != None): _return += ":{0:d}".format(port)
				_return += ("/" + Binary.str(script_pathname) if (self.path == None) else Binary.str(self.path))
			#
		#

		return _return
	#

	def _parameters_append_defaults(self, parameters):
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
			request = AbstractRequest.get_instance()
			if (request != None): _return['lang'] = request.get_lang()
		#

		if ("uuid" not in _return and Session != None):
		#
			if (request == None): request = AbstractRequest.get_instance()
			session = request.get_session()
			if (session != None and session.is_active() and (not session.is_persistent())): _return['uuid'] = Session.get_uuid()
		#

		return _return
	#

	def _parameters_filter(self, parameters):
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
			if (len(_return) == 1 and len(_return['__query__']) > 0): _return = AbstractRequest.get_instance().iline_parse(InputFilter.filter_control_chars(_return['__query__']))
			else: del(_return['__query__'])
		#

		if ("__request__" in _return and _return['__request__']):
		#
			request = AbstractRequest.get_instance()
			inner_request = request.get_inner_request()
			if (inner_request != None): request = inner_request

			if (request != None):
			#
				if ("ohandler" not in _return): _return['ohandler'] = request.get_output_format()
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

		return self._parameters_remove_filtered(_return)
	#

	def _parameters_remove_filtered(self, parameters):
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
			if (type(parameters[key]) == dict and len(parameters[key]) > 0): _return[key] = self._parameters_remove_filtered(parameters[key])
			elif (parameters[key] == "__remove__"): del(_return[key])
		#

		if ("__host__" in parameters): del(_return['__host__'])
		if ("__path__" in parameters): del(_return['__path__'])
		if ("__port__" in parameters): del(_return['__port__'])
		if ("__scheme__" in parameters): del(_return['__scheme__'])

		return _return
	#

	@staticmethod
	def escape(data):
	#
		"""
Escape the given data for embedding into (X)HTML.

:param parameters: Parameters dict

:return: (dict) Filtered parameters dict
:since:  v0.1.00
		"""

		return quote(data, "")
	#

	@staticmethod
	def unescape(data):
	#
		"""
Unescape the given data.

:param parameters: Parameters dict

:return: (dict) Filtered parameters dict
:since:  v0.1.01
		"""

		return unquote(data)
	#
#

##j## EOF