# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.xhtml.Link
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

from dNG.pas.controller.abstract_response import AbstractResponse
from dNG.pas.controller.http_xhtml_response import HttpXhtmlResponse
from dNG.pas.data.text.link import Link as _Link
from dNG.pas.data.xhtml.formatting import Formatting as XhtmlFormatting

class Link(_Link):
#
	"""
"Link" provides (X)HTML centric methods to build them from parameters.

TODO: Code incomplete

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	# pylint: disable=arguments-differ

	TYPE_FORM_FIELDS = 16
	"""
Hidden input fields
	"""
	TYPE_FORM_URL = 32
	"""
Form action URL
	"""
	TYPE_JS_REQUIRED = 64
	"""
JavaScript is required
	"""
	TYPE_QUERY_STRING = 128
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
:since:  v0.1.00
		"""

		if (type(_type) != int): _type = self.__class__.get_type(_type)

		if (parameters == None): parameters = { }
		xhtml_escape = escape

		#if (_type == "asis"): _return = self.build_url(data)
		#elif ($f__type == "asisuuid"):
		#
		#	uuid = (((isset ($direct_globals['input']))&&($f_withuuid)) ? $direct_globals['input']->uuidGet () : "");
		#	_return = str_replace ("[uuid]",((($f_uuid)&&(!$direct_globals['kernel']->vUuidIsCookied ())&&($direct_globals['kernel']->vUuidCheckUsage ())) ? $f_uuid : ""),$f_data);
		#

		if (_type & Link.TYPE_FORM_FIELDS == Link.TYPE_FORM_FIELDS):
		#
			"""
Get all form data in a string like "<input type='hidden' name='lang'
value='de' />". Automatically add language, theme and uuid fields.
			"""

			parameters = self._filter_parameters(parameters)
			parameters = self._add_default_parameters(parameters)

			#if (/*#ifndef(PHP4) */stripos/* #*//*#ifdef(PHP4):stristr:#*/($f_data,"lang=") === false) { $f_return .= "<input type='hidden' name='lang' value='$direct_settings[lang]' />"; }
			#if (/*#ifndef(PHP4) */stripos/* #*//*#ifdef(PHP4):stristr:#*/($f_data,"theme=") === false) { $f_return .= "<input type='hidden' name='theme' value='$direct_settings[theme]' />"; }

			#if ((isset ($direct_globals['input']))&&($f_withuuid))
			#{
			#	$f_uuid = $direct_globals['input']->uuidGet ();
			#	if (($f_uuid)&&(!$direct_globals['kernel']->vUuidIsCookied ())&&($direct_globals['kernel']->vUuidCheckUsage ())) { $f_return .= "<input type='hidden' name='uuid' value='$f_uuid' />"; }
			#}

			_return = self._build_url_formatted("<input type='hidden' name=\"{0}\" value=\"{1}\" />", "", parameters, Link.escape)
			xhtml_escape = False
		#
		elif (_type & Link.TYPE_FORM_URL == Link.TYPE_FORM_URL):
		#
			if (_type == Link.TYPE_FORM_URL): _type |= Link.TYPE_RELATIVE
			_return = _Link.build_url(self, _type)
		#
		elif (_type & Link.TYPE_QUERY_STRING == Link.TYPE_QUERY_STRING):
		#
			if (_type == Link.TYPE_FORM_URL): _type = Link.TYPE_RELATIVE
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
:since:  v0.1.00
		"""

		_return = _Link._add_default_parameters(self, parameters)

		if ("theme" not in _return):
		#
			response = HttpXhtmlResponse.get_instance()

			if (isinstance(response, HttpXhtmlResponse)):
			#
				theme = response.get_theme()
				if (theme != None): _return['theme'] = theme
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
:since:  v0.1.00
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

:since: v0.1.01
		"""

		store = AbstractResponse.get_instance_store()
		if (store != None and set_name in store.get("dNG.pas.data.text.url.links", { })): del(store['dNG.pas.data.text.url.links'][set_name])
	#

	@staticmethod
	def escape(data):
	#
		"""
Escape the given data for embedding into (X)HTML.

:param parameters: Parameters dict

:return: (dict) Filtered parameters dict
:since:  v0.1.01
		"""

		return XhtmlFormatting.escape(data)
	#

	@staticmethod
	def get_store(set_name):
	#
		"""
Returns all links defined for the given set name.

:param set_name: Link set name

:since: v0.1.01
		"""

		store = AbstractResponse.get_instance_store()

		if (store != None and set_name in store.get("dNG.pas.data.text.url.links", { })): return store['dNG.pas.data.text.url.links'][set_name]
		else: return [ ]
	#

	@staticmethod
	def get_type(_type):
	#
		"""
Parses the given type parameter given as a string value.

:param _type: String type

:return: (int) Internal type
:since:  v0.1.01
		"""

		if (_type == "js_elink"): _return = Link.TYPE_ABSOLUTE & Link.TYPE_JS_REQUIRED
		elif (_type == "js_ilink"): _return = Link.TYPE_RELATIVE & Link.TYPE_JS_REQUIRED
		elif (_type == "query_string"): _return = Link.TYPE_QUERY_STRING
		else: _return = _Link.get_type(_type)

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

:since: v0.1.01
		"""

		if (parameters == None): parameters = { }
		store = AbstractResponse.get_instance_store()

		if (store != None):
		#
			if ("dNG.pas.data.text.url.links" not in store): store['dNG.pas.data.text.url.links'] = { }
			store = store['dNG.pas.data.text.url.links']

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

:param parameters: Parameters dict

:return: (dict) Filtered parameters dict
:since:  v0.1.01
		"""

		return XhtmlFormatting.unescape(data)
	#
#

##j## EOF