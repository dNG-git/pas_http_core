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

# pylint: disable=import-error,no-name-in-module

try: from urllib.parse import quote, unquote
except ImportError: from urllib import quote, unquote

from dNG.pas.data.text.input_filter import InputFilter

class Uri(object):
#
	"""
"Uri" provides basic URI decoding / encoding methods.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	@staticmethod
	def decode_query_value(data):
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
	def encode_query_value(data):
	#
		"""
Encode special characters for a RFC 2396 compliant URI.

:param data: Input string

:return: (str) Encoded string
:since:  v0.1.00
		"""

		if (type(data) != str): data = str(data)
		data = InputFilter.filter_control_chars(data).strip()
		return quote(data, "")
	#
#

##j## EOF