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

from dNG.data.binary import Binary

from .abstract_encapsulated import AbstractEncapsulated

class HttpWsgi1(AbstractEncapsulated):
#
	"""
WSGI 1.0 compliant streamer.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def read(self, n = None):
	#
		"""
Reads from the current streamer session.

:param n: How many bytes to read from the current position (0 means until
          EOF)

:return: (bytes) Data; Empty byte string if EOF
:since:  v0.2.00
		"""

		_return = AbstractEncapsulated.read(self, n)
		if (_return is None): _return = Binary.BYTES_TYPE()
		return _return
	#
#

##j## EOF