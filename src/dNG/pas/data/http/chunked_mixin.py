# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.http.ChunkedMixin
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

from dNG.pas.data.binary import Binary

class ChunkedMixin(object):
#
	"""
This response mixin provides the "chunkify()" method.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	BINARY_NEWLINE = Binary.bytes("\r\n")

	def chunkify(self, data):
	#
		"""
Returns the formats the client accepts.

:return: (list) Accepted formats
:since:  v0.1.00
		"""

		data = Binary.bytes(data)

		if (data == None): _return = Binary.bytes("0\r\n\r\n")
		elif (type(data) == type(ChunkedMixin.BINARY_NEWLINE) and len(data) > 0): _return = Binary.bytes("{0:x}\r\n".format(len(data))) + data + ChunkedMixin.BINARY_NEWLINE
		else: _return = Binary.BYTES_TYPE()

		return _return
	#
#

##j## EOF