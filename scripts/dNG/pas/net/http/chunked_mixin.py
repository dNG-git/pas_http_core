# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.net.http.chunked_mixin
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

from dNG.pas.data.binary import direct_binary

class direct_chunked_mixin(object):
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

	BINARY_NEWLINE = direct_binary.bytes("\r\n")

	def chunkify(self, data):
	#
		"""
Returns the formats the client accepts.

:return: (list) Accepted formats
:since:  v0.1.00
		"""

		data = direct_binary.bytes(data)

		if (data == None): var_return = direct_binary.bytes("0\r\n\r\n")
		elif (type(data) == type(direct_chunked_mixin.BINARY_NEWLINE) and len(data) > 0): var_return = direct_binary.bytes("{0:d}\r\n".format(len(data))) + data + direct_chunked_mixin.BINARY_NEWLINE
		else: var_return = direct_binary.BYTES_TYPE()

		return var_return
	#
#

##j## EOF