# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.xhtml.Formatting
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

from cgi import escape as html_escape

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
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	@staticmethod
	def escape(data):
	#
		"""
Escapes given data for (X)HTML output.

:param data: Input string

:return: Output string
:since:  v0.1.00
		"""

		return html_escape(Binary.str(data), True)
	#

	@staticmethod
	def unescape(data):
	#
		"""
Unescapes given (X)HTML data.

:param data: Input string

:return: Output string
:since:  v0.1.00
		"""

		return HTMLParser().unescape(Binary.str(data))
	#
#

##j## EOF