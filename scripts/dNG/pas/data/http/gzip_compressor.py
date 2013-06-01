# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.http.gzip_compressor
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

from struct import pack
from zlib import compress, crc32, Z_FINISH

from dNG.pas.data.binary import direct_binary

class direct_gzip_compressor(object):
#
	"""
"direct_gzip_compressor" creates a new Gzip member for each "compress()"
call.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, level = 6):
	#
		"""
Constructor __init__(direct_gzip_compressor)

:since: v0.1.01
		"""

		self.level = level
		"""
Deflate compression level
		"""
	#

	def compress(self, string):
	#
		"""
python.org: Compress string, returning a string containing compressed data
for at least part of the data in string.

:param string: Original string

:since: v0.1.01
		"""

		data = direct_binary.bytes(string)

		if (self.level == 9): deflate_flag = 2
		elif (self.level == 1): deflate_flag = 4
		else: deflate_flag = 0

		var_return = pack("<8s2B", direct_binary.bytes("\x1f\x8b" + ("\x00" if (self.level == 0) else "\x08") + "\x00\x00\x00\x00\x00"), deflate_flag, 255)
		var_return += compress(data, self.level)[2:-4]
		var_return += pack("<2L", crc32(data), int(len(data) % 4294967296))

		return var_return
	#

	def flush(self, mode = Z_FINISH):
	#
		"""
python.org: All pending input is processed, and a string containing the
remaining compressed output is returned.

:param mode: Flush mode

:since: v0.1.01
		"""

		return direct_binary.BYTES_TYPE()
	#
#

##j## EOF