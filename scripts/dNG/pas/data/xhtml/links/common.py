# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.xhtml.links.common
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;user_profile

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasHttpUserProfileVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from threading import local

from dNG.pas.data.http.links import direct_links
from dNG.pas.data.xhtml.formatting import direct_formatting

class direct_common(direct_links):
#
	"""
"direct_common" provides common method for (X)HTML links.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
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

	store = local()
	"""
Thread-local store for links set
	"""

	@staticmethod
	def build_url(type, parameters, escape = True):
	#
		"""
Adds a link. You may use internal links "index.py?...", external links like
"http://localhost/index.py?...", input (hidden) forms or an URL, replacing
parts of it if it's larger than x characters. This function uses "shadow"
URLs to be search engine friendly if applicable and the request URI as a
source for parameters.

:param type: Link type (see constants)

:since: v0.1.00
		"""

		parameters = direct_common.filter_parameters(parameters)

		#if (type == "asis"): var_return = direct_common.build_url(data)
		#elif ($f_type == "asisuuid"):
		#
		#	uuid = (((isset ($direct_globals['input']))&&($f_withuuid)) ? $direct_globals['input']->uuidGet () : "");
		#	var_return = str_replace ("[uuid]",((($f_uuid)&&(!$direct_globals['kernel']->vUuidIsCookied ())&&($direct_globals['kernel']->vUuidCheckUsage ())) ? $f_uuid : ""),$f_data);
		#
		if (type & direct_common.TYPE_FORM_FIELDS == direct_common.TYPE_FORM_FIELDS):
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

			var_return = direct_common.build_url_formatted("<input type='hidden' name=\"{0}\" value=\"{1}\" />", "", parameters, False)
		#
		elif (type & direct_common.TYPE_FORM_URL == direct_common.TYPE_FORM_URL):
		#
			if (type == direct_common.TYPE_FORM_URL): type = direct_common.TYPE_RELATIVE
			var_return = direct_links.build_url(type, { }, (direct_common.escape if (escape) else direct_links.escape))
		#
		else: var_return = direct_links.build_url(type, parameters, (direct_common.escape if (escape) else direct_links.escape))

		return var_return
	#

	@staticmethod
	def build_url_formatted(link_template, link_separator, parameters, escape):
	#
		"""
This method removes all parameters marked as "__remove__".

:param parameters: Parameters dict

:access: protected
:return: (dict) Filtered parameters dict
:since:  v0.1.00
		"""

		return direct_links.build_url_formatted(link_template, link_separator, parameters, (direct_common.escape if (escape) else direct_links.escape))
	#

	@staticmethod
	def escape(data):
	#
		"""
Escape the given data for embedding into (X)HTML.

:param parameters: Parameters dict

:access: protected
:return: (dict) Filtered parameters dict
:since:  v0.1.00
		"""

		return direct_links.escape(direct_formatting.escape(data))
	#

	@staticmethod
	def set(type, title, parameters):
	#
		"""
Adds a link. You may use internal links "index.py?...", external links like
"http://localhost/index.py?...", input (hidden) forms or an URL, replacing
parts of it if it's larger than x characters. This function uses "shadow"
URLs to be search engine friendly if applicable and the request URI as a
source for parameters.

:param type: Link type (

:since: v0.1.00
		"""

		url = direct_common.build_url(type, parameters)
		direct_common.thread_local_check()
		direct_common.store.links.append({ "title": title, "url": url })
	#

	@staticmethod
	def thread_local_check():
	#
		"""
For thread safety some variables are defined per thread. This method makes
sure that these variables are defined.

:since: v0.1.00
		"""

		if (not hasattr(direct_common.store, "links")): direct_common.store.links = { }
	#
#

##j## EOF