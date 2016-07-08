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

from dNG.controller.abstract_response import AbstractResponse
from dNG.controller.http_xhtml_response import HttpXhtmlResponse
from dNG.data.text.link import Link as _Link
from dNG.data.xhtml.formatting import Formatting
from dNG.module.named_loader import NamedLoader

class Link(_Link):
#
	"""
"Link" provides (X)HTML centric methods to build them from parameters.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	# pylint: disable=arguments-differ

	TYPE_FORM_FIELDS = 256
	"""
Hidden input fields
	"""
	TYPE_FORM_URL = 128
	"""
Form action URL
	"""
	TYPE_JS_REQUIRED = 1024
	"""
JavaScript is required
	"""
	TYPE_QUERY_STRING = 512
	"""
Generate the query string
	"""

	def build_url(self, _type, parameters = None, escape = True):
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
:since:  v0.2.00
		"""

		if (type(_type) is not int): _type = self.__class__.get_type_int(_type)

		if (parameters is None): parameters = { }
		xhtml_escape = escape

		if (_type & Link.TYPE_FORM_FIELDS == Link.TYPE_FORM_FIELDS):
		#
			"""
Get all form data in a string like "<input type='hidden' name='lang'
value='de' />". Automatically add language, theme and uuid fields.
			"""

			parameters = self._filter_parameters(parameters)
			parameters = self._add_default_parameters(parameters)

			_return = self._build_url_formatted("<input type='hidden' name=\"{0}\" value=\"{1}\" />",
			                                    "",
			                                    parameters,
			                                    Link.escape
			                                   )

			xhtml_escape = False
		#
		elif (_type & Link.TYPE_FORM_URL == Link.TYPE_FORM_URL):
		#
			_type |= Link.TYPE_RELATIVE_URL
			_type |= Link.TYPE_PARAMETER_LESS

			_return = _Link.build_url(self, _type)
		#
		elif (_type & Link.TYPE_QUERY_STRING == Link.TYPE_QUERY_STRING):
		#
			parameters = self._filter_parameters(parameters)
			parameters = self._add_default_parameters(parameters)

			_return = (self._build_url_formatted("{0}={1}", ";", parameters)
			           if (len(parameters) > 0) else
			           ""
			          )
		#
		else: _return = _Link.build_url(self, _type, parameters)

		if (xhtml_escape): _return = Link.escape(_return)

		return _return
	#

	def _add_default_parameters(self, parameters):
	#
		"""
This method appends default parameters if not already set.

:param parameters: Parameters dict

:return: (dict) Appended parameters dict
:since:  v0.2.00
		"""

		_return = _Link._add_default_parameters(self, parameters)

		if ("theme" not in _return):
		#
			response = HttpXhtmlResponse.get_instance()

			if (isinstance(response, HttpXhtmlResponse)):
			#
				default_theme = NamedLoader.get_class("dNG.data.xhtml.theme.Renderer").get_default_theme()
				theme = response.get_theme()

				if (theme is not None and theme != default_theme): _return['theme'] = theme
			#
		#

		return _return
	#

	@staticmethod
	def _build_url_sorted_parameters(parameter_keys):
	#
		"""
Builds a sorted list for the parameter key list given.

:param parameter_keys: Parameter key list

:return: (list) Sorted parameter key list
:since:  v0.2.00
		"""

		_return = _Link._build_url_sorted_parameters(parameter_keys)

		if ("theme" in _return):
		#
			_return.remove("theme")
			_return.append("theme")
		#

		return _return
	#

	@staticmethod
	def clear_store(set_name):
	#
		"""
Removes all links defined for the given set name.

:param set_name: Link set name

:since: v0.2.00
		"""

		store = AbstractResponse.get_instance_store()
		if (store is not None and set_name in store.get("dNG.data.text.url.links", { })): del(store['dNG.data.text.url.links'][set_name])
	#

	@staticmethod
	def escape(data):
	#
		"""
Escape the given data for embedding into (X)HTML.

:param data: Input string

:return: (str) Output string
:since:  v0.2.00
		"""

		return Formatting.escape(data)
	#

	@staticmethod
	def get_store(set_name):
	#
		"""
Returns all links defined for the given set name.

:param set_name: Link set name

:since: v0.2.00
		"""

		store = AbstractResponse.get_instance_store()

		if (store is not None and set_name in store.get("dNG.data.text.url.links", { })): return store['dNG.data.text.url.links'][set_name]
		else: return [ ]
	#

	@staticmethod
	def get_type_int(_type):
	#
		"""
Parses the given type parameter given as a string value.

:param _type: String type

:return: (int) Internal type
:since:  v0.2.00
		"""

		_return = _Link.get_type_int(_type)

		type_set = _type.split("+")

		for _type in type_set:
		#
			if (_type == "js"): _return |= Link.TYPE_JS_REQUIRED
			elif (_type == "query_string"): _return |= Link.TYPE_QUERY_STRING
		#

		return _return
	#

	@staticmethod
	def set_store(set_name, _type, title, parameters = None, **kwargs):
	#
		"""
Adds a link to the given set name.

:param set_name: Link set name
:param _type: Link type (see constants)
:param title: Link title
:param parameters: Parameters dict

:since: v0.2.00
		"""

		if (parameters is None): parameters = { }
		store = AbstractResponse.get_instance_store()

		if (store is not None):
		#
			if ("dNG.data.text.url.links" not in store): store['dNG.data.text.url.links'] = { }
			store = store['dNG.data.text.url.links']

			priority = kwargs.get("priority", 5)

			link = { "title": title, "type": _type, "parameters": parameters, "priority": priority }
			link.update(kwargs)

			if (set_name in store):
			#
				store = store[set_name]
				index = -1
				index_replaced = -1

				for position in range(0, len(store)):
				#
					if (link['title'] == store[position]['title']):
					#
						index_replaced = position
						break
					#
					elif (index < 0 and link['priority'] > store[position]['priority']): index = position
				#

				if (index_replaced < 0):
				#
					if (index < 0): index = len(store)
					store.insert(index, link)
				#
				else: store[index_replaced] = link
			#
			else: store[set_name] = [ link ]
		#
	#

	@staticmethod
	def unescape(data):
	#
		"""
Unescape the given data.

:param data: Input string

:return: (str) Output string
:since:  v0.2.00
		"""

		return Formatting.unescape(data)
	#
#

##j## EOF