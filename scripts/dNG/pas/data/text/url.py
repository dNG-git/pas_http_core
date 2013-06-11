# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.url
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

try: from urllib.parse import quote, unquote
except ImportError: from urllib import quote, unquote

class direct_url(object):
#
	"""
"direct_url" provides basic URL decoding / encoding methods.

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

		data = unquote(data)
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
		return quote(data, "")
	#
#

##j## EOF