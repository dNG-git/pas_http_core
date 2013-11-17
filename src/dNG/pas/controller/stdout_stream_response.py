# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.controller.StdoutStreamResponse
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

import sys

from .abstract_stream_response import AbstractStreamResponse

class StdoutStreamResponse(AbstractStreamResponse):
#
	"""
This stream response instance will write all data to STDOUT.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def _write(self, data):
	#
		"""
Writes the given data.

:param data: Data to be send

:since: v0.1.00
		"""

		sys.stdout.write(data)
	#
#

##j## EOF