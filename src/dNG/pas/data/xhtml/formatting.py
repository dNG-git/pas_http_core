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

# pylint: disable=import-error

from cgi import escape
import re

try: from html.parser import HTMLParser
except ImportError: from HTMLParser import HTMLParser

from dNG.pas.data.binary import Binary

class Formatting(object):
#
	"""
"Formatting" is a helper library for (X)HTML related stuff.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	@staticmethod
	def escape(data):
	#
		"""
Escapes given data for (X)HTML output.

:param data: Input string

:return: (str) Output string
:since:  v0.1.00
		"""

		return escape(Binary.str(data), True)
	#

	@staticmethod
	def rewrite_legacy_html(data):
	#
		"""
Use this function to return legacy HTML output for the given XHTML data. If
the browser does not support XHTML we need to switch to a legacy HTML
(quirks) mode for output.

:param data: Output content

:return: (str) Converted output content
:since:  v0.1.00
		"""

		data = re.sub("\\s*<\\?(.*?)\\?>\\s*", "", data, flags = re.S)
		data = re.sub("\\s*/\\s*>", ">", data)
		data = re.sub("<meta\\s+http\\-equiv=(.)Content\\-Type(.)\\s+content=(.)application/xhtml\\+xml(.)", "<meta http-equiv=\\1Content-Type\\2 content=\\3text/html\\4", data, flags = (re.I | re.S))
		data = re.sub("<\\!\\[CDATA\\[(.*?)\\]\\]>", "<!--\\1-->", data, flags = (re.I | re.S))

		return data
	#

	@staticmethod
	def unescape(data):
	#
		"""
Unescapes given (X)HTML data.

:param data: Input string

:return: (str) Output string
:since:  v0.1.00
		"""

		return HTMLParser().unescape(Binary.str(data))
	#
#

##j## EOF