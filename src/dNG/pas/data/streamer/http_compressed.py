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

class HttpCompressed(AbstractEncapsulated):
#
	"""
Compressing streamer based on the given compressor.

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
Constructor __init__(HttpCompressed)

:param streamer: Encapsulated streamer instance
:param compressor: Compression object

:since: v0.1.00
		"""

		AbstractEncapsulated.__init__(self, streamer)

		self.compressor = compressor
		"""
Compression function
		"""

		self.set_io_chunk_size(1048576)
	#

	def read(self, _bytes = None):
	#
		"""
Reads from the current streamer session.

:param _bytes: How many bytes to read from the current position (0 means
               until EOF)

:return: (mixed) Data; None if EOF
:since:  v0.1.00
		"""

		_return = AbstractEncapsulated.read(self, _bytes)
		is_data_uncompressed = True

		while (self.compressor != None and is_data_uncompressed):
		#
			if (_return == None):
			#
				_return = self.compressor.flush()

				is_data_uncompressed = False
				self.compressor = None
			#
			else:
			#
				_return = self.compressor.compress(Binary.bytes(_return))

				# Feed compressor object with data until it returns at least one byte
				is_data_uncompressed = (len(_return) < 1)
				if (is_data_uncompressed): _return = AbstractEncapsulated.read(self, _bytes)
			#
		#

		return _return
	#
#

##j## EOF