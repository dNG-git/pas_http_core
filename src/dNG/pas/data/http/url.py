# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.http.Url
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

try: from urllib.parse import quote, unquote
except ImportError: from urllib import quote, unquote

from dNG.pas.controller.abstract_response import AbstractResponse
from dNG.pas.data.text.input_filter import InputFilter
from dNG.pas.data.text.url import Url as AbstractUrl
from dNG.pas.data.xhtml.formatting import Formatting as XhtmlFormatting

class Url(AbstractUrl):
#
	"""
"Url" provides basic URL decoding / encoding methods.

TODO: Code incomplete

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	TYPE_FORM_FIELDS = 8
	"""
Hidden input fields
	"""
	TYPE_FORM_URL = 16
	"""
Form action URL
	"""

	def build_url(self, _type, parameters, escape = True):
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

		if (type(_type) != int): _type = self._get_type(_type)

		#if (_type == "asis"): _return = self.build_url(data)
		#elif ($f__type == "asisuuid"):
		#
		#	uuid = (((isset ($direct_globals['input']))&&($f_withuuid)) ? $direct_globals['input']->uuidGet () : "");
		#	_return = str_replace ("[uuid]",((($f_uuid)&&(!$direct_globals['kernel']->vUuidIsCookied ())&&($direct_globals['kernel']->vUuidCheckUsage ())) ? $f_uuid : ""),$f_data);
		#

		if (_type & Url.TYPE_FORM_FIELDS == Url.TYPE_FORM_FIELDS):
		#
			"""
Get all form data in a string like "<input type='hidden' name='lang'
value='de' />". Automatically add language, theme and uuid fields.
			"""

			parameters = self._parameters_filter(parameters)
			parameters = self._parameters_append_defaults(parameters)

			#if (/*#ifndef(PHP4) */stripos/* #*//*#ifdef(PHP4):stristr:#*/($f_data,"lang=") === false) { $f_return .= "<input type='hidden' name='lang' value='$direct_settings[lang]' />"; }
			#if (/*#ifndef(PHP4) */stripos/* #*//*#ifdef(PHP4):stristr:#*/($f_data,"theme=") === false) { $f_return .= "<input type='hidden' name='theme' value='$direct_settings[theme]' />"; }

			#if ((isset ($direct_globals['input']))&&($f_withuuid))
			#{
			#	$f_uuid = $direct_globals['input']->uuidGet ();
			#	if (($f_uuid)&&(!$direct_globals['kernel']->vUuidIsCookied ())&&($direct_globals['kernel']->vUuidCheckUsage ())) { $f_return .= "<input type='hidden' name='uuid' value='$f_uuid' />"; }
			#}

			_return = self._build_url_formatted("<input type='hidden' name=\"{0}\" value=\"{1}\" />", "", parameters)
		#
		elif (_type & Url.TYPE_FORM_URL == Url.TYPE_FORM_URL):
		#
			if (_type == Url.TYPE_FORM_URL): _type = Url.TYPE_RELATIVE
			_return = AbstractUrl.build_url(self, _type, { }, (Url.escape if (escape) else AbstractUrl.escape))
		#
		else: _return = AbstractUrl.build_url(self, _type, parameters, (Url.escape if (escape) else AbstractUrl.escape))

		return _return
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

		return AbstractUrl.escape(XhtmlFormatting.escape(data))
	#

	@staticmethod
	def query_param_decode(data):
	#
		"""
Decode special characters from a RFC 2396 compliant URI.

:param data: Input string

:return: (str) Decoded string
:since:  v0.1.00
		"""

		data = unquote(data)
		return InputFilter.filter_control_chars(data).strip()
	#

	@staticmethod
	def query_param_encode(data):
	#
		"""
Encode special characters for a RFC 2396 compliant URI.

:param data: Input string

:return: (str) Encoded string
:since:  v0.1.00
		"""

		data = InputFilter.filter_control_chars(data).strip()
		return quote(data, "")
	#

	@staticmethod
	def store_get(set_name):
	#
		"""
Return all links defined for the given set name.

:param set_name: Link set name

:since: v0.1.01
		"""

		store = AbstractResponse.get_instance_store()

		if (store != None and "dNG.pas.data.text.url.links" in store and set_name in store['dNG.pas.data.text.url.links']): return store['dNG.pas.data.text.url.links'][set_name]
		else: return [ ]
	#

	@staticmethod
	def store_set(set_name, _type, title, parameters = { }, **kwargs):
	#
		"""
Adds a link to the given set name.

:param set_name: Link set name
:param _type: Link type (see constants)
:param title: Link title
:param parameters: Parameters dict

:since: v0.1.01
		"""

		store = AbstractResponse.get_instance_store()

		if (store != None):
		#
			if ("dNG.pas.data.text.url.links" not in store): store['dNG.pas.data.text.url.links'] = { }
			store = store['dNG.pas.data.text.url.links']

			priority = (kwargs['priority'] if ("priority" in kwargs) else 5)

			link = { "title": title, "type": _type, "parameters": parameters, "priority": priority }
			link.update(kwargs)

			if (set_name in store): store[set_name].append(link)
			store[set_name] = [ link ]
		#
	#
#

##j## EOF