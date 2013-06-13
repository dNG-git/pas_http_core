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

try: from urllib.parse import quote, unquote
except ImportError: from urllib import quote, unquote

from dNG.pas.controller.abstract_response import AbstractResponse
from dNG.pas.data.http.links import Links
from dNG.pas.data.xhtml.formatting import Formatting as XhtmlFormatting
from .input_filter import InputFilter

class Url(Links):
#
	"""
"Url" provides basic URL decoding / encoding methods.

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

	@staticmethod
	def build_url(var_type, parameters, escape = True):
	#
		"""
Adds a link. You may use internal links "index.py?...", external links like
"http://localhost/index.py?...", input (hidden) forms or an URL, replacing
parts of it if it's larger than x characters. This function uses "shadow"
URLs to be search engine friendly if applicable and the request URI as a
source for parameters.

:param var_type: Link type (see constants)

:since: v0.1.01
		"""

		parameters = Url.filter_parameters(parameters)

		#if (var_type == "asis"): var_return = Url.build_url(data)
		#elif ($f_var_type == "asisuuid"):
		#
		#	uuid = (((isset ($direct_globals['input']))&&($f_withuuid)) ? $direct_globals['input']->uuidGet () : "");
		#	var_return = str_replace ("[uuid]",((($f_uuid)&&(!$direct_globals['kernel']->vUuidIsCookied ())&&($direct_globals['kernel']->vUuidCheckUsage ())) ? $f_uuid : ""),$f_data);
		#
		if (var_type & Url.TYPE_FORM_FIELDS == Url.TYPE_FORM_FIELDS):
		#
			"""
Get all form data in a string like "<input type='hidden' name='lang'
value='de' />". Automatically add language, theme and uuid fields.
			"""

			#if (/*#ifndef(PHP4) */stripos/* #*//*#ifdef(PHP4):stristr:#*/($f_data,"lang=") === false) { $f_return .= "<input type='hidden' name='lang' value='$direct_settings[lang]' />"; }
			#if (/*#ifndef(PHP4) */stripos/* #*//*#ifdef(PHP4):stristr:#*/($f_data,"theme=") === false) { $f_return .= "<input type='hidden' name='theme' value='$direct_settings[theme]' />"; }

			#if ((isset ($direct_globals['input']))&&($f_withuuid))
			#{
			#	$f_uuid = $direct_globals['input']->uuidGet ();
			#	if (($f_uuid)&&(!$direct_globals['kernel']->vUuidIsCookied ())&&($direct_globals['kernel']->vUuidCheckUsage ())) { $f_return .= "<input type='hidden' name='uuid' value='$f_uuid' />"; }
			#}

			var_return = Url.build_url_formatted("<input type='hidden' name=\"{0}\" value=\"{1}\" />", "", parameters, False)
		#
		elif (var_type & Url.TYPE_FORM_URL == Url.TYPE_FORM_URL):
		#
			if (var_type == Url.TYPE_FORM_URL): var_type = Url.TYPE_RELATIVE
			var_return = Links.build_url(var_type, { }, (Url.escape if (escape) else Links.escape))
		#
		else: var_return = Links.build_url(var_type, parameters, (Url.escape if (escape) else Links.escape))

		return var_return
	#

	@staticmethod
	def build_url_formatted(link_template, link_separator, parameters, xhtml_escape):
	#
		"""
This method removes all parameters marked as "__remove__".

:param parameters: Parameters dict

:access: protected
:return: (dict) Filtered parameters dict
:since:  v0.1.01
		"""

		return Links.build_url_formatted(link_template, link_separator, parameters, (Url.xhtml_escape if (xhtml_escape) else Links.escape))
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
	def store_set(set_name, var_type, title, parameters = { }, **kwargs):
	#
		"""
Adds a link. You may use internal links "index.py?...", external links like
"http://localhost/index.py?...", input (hidden) forms or an URL, replacing
parts of it if it's larger than x characters. This function uses "shadow"
URLs to be search engine friendly if applicable and the request URI as a
source for parameters.

:param var_type: Link type (

:since: v0.1.01
		"""

		url = Url.build_url(var_type, parameters)
		store = AbstractResponse.get_instance_store()

		if (store != None):
		#
			if ("dNG.pas.data.text.url.links" not in store): store['dNG.pas.data.text.url.links'] = { }
			store = store['dNG.pas.data.text.url.links']

			priority = (kwargs['priority'] if ("priority" in kwargs) else 5)

			link = { "title": title, "url": url, "priority": priority }
			link.update(kwargs)

			if (set_name in store): store[set_name].append(link)
			store[set_name] = [ link ]
		#
	#

	@staticmethod
	def xhtml_escape(data):
	#
		"""
Escape the given data for embedding into (X)HTML.

:param parameters: Parameters dict

:access: protected
:return: (dict) Filtered parameters dict
:since:  v0.1.01
		"""

		return Links.escape(XhtmlFormatting.escape(data))
	#
#

##j## EOF