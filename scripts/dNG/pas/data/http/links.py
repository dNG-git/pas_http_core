# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.http.Links
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

try: from urllib.parse import quote, urlsplit
except ImportError:
#
	from urllib import quote
	from urlparse import urlsplit
#

from dNG.pas.controller.abstract_request import AbstractRequest
from dNG.pas.data.binary import Binary
from dNG.pas.data.settings import Settings
from dNG.pas.data.logging.log_line import LogLine

try: from dNG.pas.data.session import Session
except ImportError: Session = None

class Links(object):
#
	"""
"Links" provides common method for (X)HTML links.

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
Constructor __init__(Links)

:since: v0.1.01
		"""

		self.host = None
		"""
Override for the URL host
		"""
		self.path = None
		"""
Override for the URL path
		"""
		self.port = None
		"""
Override for the URL port
		"""
		self.scheme = None
		"""
Override for the URL scheme
		"""
	#

	def build_url(self, var_type, parameters, py_escape = None):
	#
		"""
Adds a link. You may use internal links "index.py?...", external links like
"http://localhost/index.py?...", input (hidden) forms or an URL, replacing
parts of it if it's larger than x characters. This function uses "shadow"
URLs to be search engine friendly if applicable and the request URI as a
source for parameters.

:param var_type: Link type (see constants)

:since: v0.1.00
		"""

		if (type(var_type) != int): var_type = self.get_type(var_type)
		var_return = self.get_url(var_type, parameters)

		parameters = self.parameters_filter(parameters)
		parameters = self.parameters_append_defaults(parameters)

		if (len(parameters) > 0):
		#
			if ("?" not in var_return): var_return += "?"
			elif (var_return[-1:] != ";"): var_return += ";"

			var_return += self.build_url_formatted("{0}={1}", ";", parameters, py_escape = None)
		#

		if (var_type & Links.TYPE_OPTICAL == Links.TYPE_OPTICAL):
		#
			"""
A filter is required for really long URLs. First we will have a look at the
"optical maximal length" setting, then if the URL is larger than the setting
			"""

			length_available = int(Settings.get("pas_html_url_optical_max_length", 100))

			if (len(var_return) > length_available):
			#
				url_elements = urlsplit(var_return)

				var_return = "{0}://".format(url_elements.scheme)
				if (url_elements.username != None or url_elements.password != None): var_return += "{0}:{1}@".format(("" if (url_elements.username == None) else url_elements.username), ("" if (url_elements.password == None) else url_elements.password))
				var_return += ("" if (url_elements.hostname == None) else url_elements.hostname)

				if (url_elements.port != None): var_return += ":{0:d}".format(url_elements.port)
				path_length = len(url_elements.path)
				if (path_length > 0): basepath_position = (url_elements[:-1] if (url_elements[-1:] == "/") else url_elements).path.rfind("/")

				if (path_length > 0 and basepath_position > 0):
				#
					basepath_position += 1

					file_name = url_elements.path[basepath_position:]
					var_return += url_elements.path[:basepath_position]
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

					if (len(var_return) < 3 + three_eigths + one_eighth):
					#
						"""
The URL (excluding the file name) is small enough. We will add the whole
string to our result
						"""

						length_available -= len(var_return)
					#
					else:
					#
						"""
The source URL is too large - we will strip everything, that's larger than
our projected size
						"""

						var_return = "{0} ... {1}".format(var_return[:three_eigths], var_return[-1 * one_eighth:])
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

						var_return += file_name
						length_available -= len(file_name)
					#
					else:
					#
						"""
Unfortunately, the filename is too long - we will remove the first part
						"""

						var_return += " ... {0}".format(file_name[-1 * one_fourth])
						length_available -= 3 + one_fourth
					#

					"""
Our last step is to add the whole or the last part of the query string, once
more depending on the string length
					"""

					query_fragment = ""
					if (url_elements.query != ""): query_fragment += "?{0}".format(url_elements.query)
					if (url_elements.fragment != ""): query_fragment += "#{0}".format(url_elements.fragment)

					if (len(query_fragment) < 3 + length_available): var_return += query_fragment
					else: var_return += " ... {0}".format(query_fragment[-1 * length_available:])
				#
			#
		#

		return var_return
	#

	def build_url_formatted(self, link_template, link_separator, parameters, py_escape = None):
	#
		"""
This method removes all parameters marked as "__remove__".

:param parameters: Parameters dict

:access: protected
:return: (dict) Filtered parameters dict
:since:  v0.1.00
		"""

		var_return = ""

		if (py_escape == None): py_escape = Links.escape

		for key in parameters:
		#
			escaped_key = py_escape(key)
			value_type = type(parameters[key])

			if (key == "dsd"):
			#
				dsd_value = self.build_url_dsd_formatted(parameters[key], py_escape)

				if (len(dsd_value) > 0):
				#
					if (var_return != ""): var_return += link_separator
					var_return += link_template.format("dsd", dsd_value)
				#
			#
			elif (value_type == dict):
			#
				for value_key in parameters[key]:
				#
					escaped_key = "{0}[{1}]".format(py_escape(key), py_escape(value_key))
					escaped_value = py_escape(parameters[key][value_key])

					if (var_return != ""): var_return += link_separator
					var_return += link_template.format(escaped_key, escaped_value)
				#
			#
			elif (value_type == list):
			#
				for value in parameters[key]:
				#
					escaped_value = py_escape(value)

					if (var_return != ""): var_return += link_separator
					var_return += link_template.format("{0}[]".format(escaped_key), escaped_value)
				#
			#
			else:
			#
				escaped_value = py_escape(parameters[key])

				if (var_return != ""): var_return += link_separator
				var_return += link_template.format(escaped_key, escaped_value)
			#
		#

		return var_return
	#

	def build_url_dsd_formatted(self, parameters, py_escape):
	#
		"""
This method removes all parameters marked as "__remove__".

:param parameters: Parameters dict

:access: protected
:return: (dict) Filtered parameters dict
:since:  v0.1.00
		"""

		var_return = ""

		if (type(parameters) == dict):
		#
			for key in parameters:
			#
				if (len(parameters[key]) > 0):
				#
					escaped_key = py_escape(key)
					escaped_value = py_escape(parameters[key])

					if (var_return != ""): var_return += "++"
					var_return += "{0}+{1}".format(escaped_key, escaped_value)
				#
			#
		#

		return var_return
	#

	def get_type(self, var_type):
	#
		"""
Parses the given type parameter given as a string value.

:param var_type: String type

:access: protected
:return: (int) Internal type
:since:  v0.1.01
		"""

		if (var_type == "elink"): var_return = Links.TYPE_FULL
		elif (var_type == "ilink"): var_return = Links.TYPE_RELATIVE
		elif (var_type == "optical"): var_return = Links.TYPE_OPTICAL
		else: var_return = 0

		return var_return
	#

	def parameters_append_defaults(self, parameters):
	#
		"""
This method filters all parameters of the type "__<KEYWORD>__".

:param parameters: Parameters dict

:access: protected
:return: (dict) Filtered parameters dict
:since:  v0.1.00
		"""

		var_return = parameters
		request = None

		if ("lang" not in var_return):
		#
			request = AbstractRequest.get_instance()
			if (request != None): var_return['lang'] = request.get_lang()
		#

		if ("uuid" not in var_return and Session != None):
		#
			if (request == None): request = AbstractRequest.get_instance()
			session = request.get_session()
			if (session != None and session.is_active() and (not session.is_persistent())): var_return['uuid'] = Session.get_uuid()
		#

		return var_return
	#

	def parameters_filter(self, parameters):
	#
		"""
This method filters all parameters of the type "__<KEYWORD>__".

:param parameters: Parameters dict

:access: protected
:return: (dict) Filtered parameters dict
:since:  v0.1.00
		"""

		var_return = parameters.copy()

		if ("__query__" in var_return and len(var_return['__query__']) > 0):
		#
			if (len(var_return) == 1): var_return = AbstractRequest.get_instance().iline_parse(var_return['__query__'])
			else: del(var_return['__query__'])
		#
		elif ("__request__" in var_return and var_return['__request__']):
		#
			request = AbstractRequest.get_instance()
			inner_request = request.get_inner_request()
			if (inner_request != None): request = inner_request

			if (request != None):
			#
				if ("ohandler" not in var_return): var_return['ohandler'] = request.get_output_format()
				if ("m" not in var_return): var_return['m'] = request.get_module()
				if ("s" not in var_return): var_return['s'] = request.get_service().replace(".", " ")
				if ("a" not in var_return): var_return['a'] = request.get_action()

				dsd_dict = request.get_dsd_dict()
				if (len(dsd_dict) and "dsd" not in var_return): var_return['dsd'] = { }

				for key in dsd_dict:
				#
					if (key not in var_return['dsd']): var_return['dsd'][key] = dsd_dict[key]
				#
			#

			del(var_return['__request__'])
		#

		return self.parameters_remove_filtered(var_return)
	#

	def parameters_remove_filtered(self, parameters):
	#
		"""
This method removes all parameters marked as "__remove__" or special ones.

:param parameters: Parameters dict

:access: protected
:return: (dict) Filtered parameters dict
:since:  v0.1.00
		"""

		var_return = parameters.copy()

		for key in parameters:
		#
			if (type(parameters[key]) == dict and len(parameters[key]) > 0): var_return[key] = self.parameters_remove_filtered(parameters[key])
			elif (parameters[key] == "__remove__"): del(var_return[key])
		#

		if ("__host__" in parameters): del(var_return['__host__'])
		if ("__path__" in parameters): del(var_return['__path__'])
		if ("__port__" in parameters): del(var_return['__port__'])
		if ("__scheme__" in parameters): del(var_return['__scheme__'])

		return var_return
	#

	def get_url(self, var_type, parameters):
	#
		"""
Adds a link.

:param var_type: Link type (see constants)
:param parameters: Link parameters

:since: v0.1.00
		"""

		var_return = ""

		if (self.scheme != None and self.path != None):
		#
			var_return = "{0}://".format(Binary.str(self.scheme))
			if (self.host != None): var_return += Binary.str(self.host)
			if (self.port != None): var_return += ":{0}".format(Binary.str(self.port))
			var_return += Binary.str(self.path)
		#
		else:
		#
			request = AbstractRequest.get_instance()

			if (var_type == Links.TYPE_RELATIVE):
			#
				if (self.path == None):
				#
					script_name = request.get_script_name()
					if (script_name != None): var_return = Binary.str(script_name)
				#
				else: var_return = Binary.str(self.path)
			#
			else:
			#
				scheme = request.get_server_scheme()
				host = request.get_server_host()
				port = request.get_server_port()
				script_pathname = request.get_script_pathname()

				if (scheme == None or (self.path == None and script_pathname == None)): raise RuntimeError("Can't construct a full URL from the received request if it is not provided", 5)

				var_return = "{0}://".format(Binary.str(scheme))
				if (host != None): var_return += Binary.str(host)
				if (port != None): var_return += ":{0:d}".format(port)
				var_return += ("/" + Binary.str(script_pathname) if (self.path == None) else Binary.str(self.path))
			#
		#

		return var_return
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
#

##j## EOF