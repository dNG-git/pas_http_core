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

	TYPE_FORM = 8
	"""
Hidden input fields
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
		if (type == direct_common.TYPE_FORM):
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

			var_return = direct_common.build_url_formatted("<input type='hidden' name=\"{0}\" value=\"{1}\" />", "", parameters, True)
		#
		else: var_return = direct_common.build_url_formatted("{0}={1}", ";", parameters, escape)
		"""
	elseif ($f_type == "optical")
	{
/* -------------------------------------------------------------------------
A filter is required for really long URLs. First we will have a look at the
"optical maximal length" setting, then if the URL is larger than the setting
------------------------------------------------------------------------- */

		if (strlen ($f_data) > $direct_settings['swg_url_opticalmaxlength'])
		{
			$f_url_array = parse_url ($f_data);

			$f_url_array['url'] = $f_url_array['scheme']."://";
			if ((isset ($f_url_array['user']))||(isset ($f_url_array['pass']))) { $f_url_array['url'] .= $f_url_array['user'].":{$f_url_array['pass']}@"; }
			$f_url_array['url'] .= $f_url_array['host'];

			if (isset ($f_url_array['port'])) { $f_url_array['url'] .= ":".$f_url_array['port']; }

			if (isset ($f_url_array['path']))
			{
				$f_pathinfo = pathinfo ($f_url_array['path']);
				if (substr ($f_url_array['path'],-1) == "/") { $f_pathinfo['basename'] .= "/"; }
				$f_url_array['url'] .= preg_replace ("#{$f_pathinfo['basename']}$#","",$f_url_array['path']);
			}
			else { $f_pathinfo = array ("basename" => ""); }

			if ((isset ($f_url_array['query']))||(isset ($f_url_array['fragment'])))
			{
				$f_length_available = $direct_settings['swg_url_opticalmaxlength'];
				$f_one_eighth = floor (($f_length_available - 3) / 8);
				$f_one_fourth = ($f_one_eighth * 2);
				$f_three_eigths = ($f_length_available - ($f_one_fourth * 2) - $f_one_eighth);

/* -------------------------------------------------------------------------
Now we will find out, how to remove unimportant parts of the given URL
------------------------------------------------------------------------- */

				if (strlen ($f_url_array['url']) < (3 + $f_three_eigths + $f_one_eighth))
				{
/* -------------------------------------------------------------------------
The URL (excluding the file name) is small enough. We will add the whole
string to our result
------------------------------------------------------------------------- */

					$f_return = $f_url_array['url'];
					$f_length_available -= strlen ($f_url_array['url']);
				}
				else
				{
/* -------------------------------------------------------------------------
The source URL is too large - we will strip everything, that's larger than
our projected size
------------------------------------------------------------------------- */

					$f_return = (substr ($f_url_array['url'],0,$f_three_eigths))." ... ".(substr ($f_url_array['url'],(-1 * $f_one_eighth)));
					$f_length_available -= (3 + $f_three_eigths + $f_one_eighth);
				}

/* -------------------------------------------------------------------------
The next few lines will check the size of the filename and remove parts of
it if required
------------------------------------------------------------------------- */

				if (strlen ($f_pathinfo['basename']) < (3 + $f_one_fourth))
				{
/* -------------------------------------------------------------------------
Again, the filename is small enough - no action is required (add it 1 to 1)
------------------------------------------------------------------------- */

					$f_return .= $f_pathinfo['basename'];
					$f_length_available -= strlen ($f_pathinfo['basename']);
				}
				else
				{
/* -------------------------------------------------------------------------
Unfortunately, the filename is too long - we will remove the first part
------------------------------------------------------------------------- */

					$f_return .= " ... ".(substr ($f_pathinfo['basename'],(-1 * $f_one_fourth)));
					$f_length_available -= (3 + $f_one_fourth);
				}

/* -------------------------------------------------------------------------
Our last step is to add the whole or the last part of the query string, once
more depending on the string length
------------------------------------------------------------------------- */

				$f_query = "";
				if (isset ($f_url_array['query'])) { $f_query .= "?".$f_url_array['query']; }
				if (isset ($f_url_array['fragment'])) { $f_query .= "#".$f_url_array['fragment']; }

				if (strlen ($f_query) < (3 + $f_length_available)) { $f_return .= $f_query; }
				else { $f_return .= " ... ".(substr ($f_query,(-1 * $f_length_available))); }
			}
			else
			{
				$f_length_available = $direct_settings['swg_url_opticalmaxlength'];
				$f_one_sixth = floor ($f_length_available / 6);
				$f_one_third = ($f_one_sixth * 2);

/* -------------------------------------------------------------------------
Now we will find out, how to remove unimportant parts of the given URL
------------------------------------------------------------------------- */

				if (strlen ($f_url_array['url']) < (3 + $f_one_third + $f_one_sixth))
				{
/* -------------------------------------------------------------------------
The URL (excluding the file name) is small enough. We will add the whole
string to our result
------------------------------------------------------------------------- */

					$f_return = $f_url_array['url'];
					$f_length_available -= strlen ($f_url_array['url']);
				}
				else
				{
/* -------------------------------------------------------------------------
The source URL is too large - we will strip everything, that's larger than
our projected size
------------------------------------------------------------------------- */

					$f_return = (substr ($f_url_array['url'],0,$f_one_third))." ... ".(substr ($f_url_array['url'],(-1 * $f_one_sixth)));
					$f_length_available -= (3 + $f_one_third + $f_one_sixth);
				}

/* -------------------------------------------------------------------------
The next two lines will check the size of the filename and remove parts of
it if required
------------------------------------------------------------------------- */

				$f_return .= ((strlen ($f_pathinfo['basename']) < (3 + $f_length_available)) ? $f_pathinfo['basename'] : " ... ".(substr ($f_pathinfo['basename'],(-1 * $f_length_available))));
			}
		}
		else { $f_return = $f_data; }

		$f_return = direct_html_encode_special ($f_return);
	}
		"""

		return var_return
	#

	@staticmethod
	def build_url_escape(data):
	#
		"""
Escape the given data for embedding into (X)HTML.

:param parameters: Parameters dict

:access: protected
:return: (dict) Filtered parameters dict
:since:  v0.1.00
		"""

		return direct_links.build_url_escape(direct_formatting.escape(data))
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

		return direct_links.build_url_formatted(link_template, link_separator, parameters, (direct_common.build_url_escape if (escape) else direct_links.build_url_escape))
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