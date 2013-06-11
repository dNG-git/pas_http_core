# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.streamer.http_compressed
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
from dNG.pas.data.logging.log_line import direct_log_line
from .abstract_encapsulated import direct_abstract_encapsulated

class direct_http_compressed(direct_abstract_encapsulated):
#
	"""
Throttles streamer based on the given bandwidth limitation.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, streamer, compressor):
	#
		"""
Constructor __init__(direct_http_compressed)

:param streamer: Encapsulated streamer instance
:param compressor: Compression function

:since: v0.1.00
		"""

		direct_abstract_encapsulated.__init__(self, streamer)

		self.compressor = compressor
		"""
Compression function
		"""
	#

	def read(self, var_bytes = 1048576):
	#
		"""
Reads from the current streamer session.

:param var_bytes: How many bytes to read from the current position (0 means
                  until EOF)

:return: (mixed) Data; False on error
:since:  v0.1.00
		"""

		data = direct_abstract_encapsulated.read(self, var_bytes)

		if (self.compressor != None):
		#
			if (data == None or data == False):
			#
				data = self.compressor.flush()
				self.compressor = None
			#
			elif (len(data) > 0): data = self.compressor.compress(direct_binary.bytes(data))
		#

		return data
	#
#

##j## EOF