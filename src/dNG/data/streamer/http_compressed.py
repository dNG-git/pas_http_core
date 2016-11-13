# -*- coding: utf-8 -*-

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
from dNG.data.settings import Settings

from .abstract_encapsulated import AbstractEncapsulated

class HttpCompressed(AbstractEncapsulated):
    """
Compressing streamer based on the given compressor.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self, streamer, compressor):
        """
Constructor __init__(HttpCompressed)

:param streamer: Encapsulated streamer instance
:param compressor: Compression object

:since: v0.2.00
        """

        AbstractEncapsulated.__init__(self, streamer)

        self.compressor = compressor
        """
Compression function
        """

        self.set_io_chunk_size(int(Settings.get("pas_global_io_chunk_size_local_network", 1048576)))
    #

    def read(self, n = None):
        """
Reads from the current streamer session.

:param n: How many bytes to read from the current position (0 means until
          EOF)

:return: (bytes) Data; None if EOF
:since:  v0.2.00
        """

        _return = AbstractEncapsulated.read(self, n)

        is_data_uncompressed = (self.compressor is not None)

        while (is_data_uncompressed):
            if (_return is None):
                _return = self.compressor.flush()
                self.compressor = None

                break
            else:
                _return = self.compressor.compress(Binary.bytes(_return))

                # Feed compressor object with data until it returns at least one byte
                if (len(_return) < 1): _return = AbstractEncapsulated.read(self, n)
                else: is_data_uncompressed = False
            #
        #

        return _return
    #
#
