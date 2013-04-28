# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.input_filter
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

from dNG.pas.data.text.input_filter import direct_input_filter

try: from urllib import parse as urlparse
except ImportError: import urllib as urlparse

class direct_url(object):
#
	"""
"direct_input_filter" provides basic input filter functions.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	@staticmethod
	def query_param_decode(data):
	#
		"""
Decode special characters from a RFC 2396 compliant URI.

:param data: Input string

:return: (str) Decoded string
:since:  v0.1.00
		"""

		data = urlparse.unquote(data)
		return direct_input_filter.filter_control_chars(data).strip()
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

		data = direct_input_filter.filter_control_chars(data).strip()
		return urlparse.quote(data, "")
	#
#

##j## EOF