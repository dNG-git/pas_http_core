# -*- coding: utf-8 -*-
##j## BOF

"""
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
"""

from dNG.pas.data.binary import Binary
from .abstract_encapsulated import AbstractEncapsulated

class HttpWsgi1(AbstractEncapsulated):
#
	"""
WSGI 1.0 compliant streamer.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def read(self, _bytes = None):
	#
		"""
Reads from the current streamer session.

:param _bytes: How many bytes to read from the current position (0 means
               until EOF)

:return: (bytes) Data; Empty byte string if EOF
:since:  v0.1.00
		"""

		_return = AbstractEncapsulated.read(self, _bytes)
		if (_return == None): _return = Binary.BYTES_TYPE()
		return _return
	#
#

##j## EOF