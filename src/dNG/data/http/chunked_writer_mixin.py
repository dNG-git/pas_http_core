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

from .chunked_reader_mixin import ChunkedReaderMixin

class ChunkedWriterMixin(object):
    """
This response mixin provides the "chunkify()" method.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def chunkify(self, data):
        """
Returns the formats the client accepts.

:return: (list) Accepted formats
:since:  v1.0.0
        """

        data = Binary.bytes(data)

        if (data is None): _return = Binary.bytes("0\r\n\r\n")
        elif (type(data) is type(ChunkedReaderMixin.BINARY_NEWLINE)
              and len(data) > 0
             ): _return = Binary.bytes("{0:x}\r\n".format(len(data))) + data + ChunkedReaderMixin.BINARY_NEWLINE
        else: _return = Binary.BYTES_TYPE()

        return _return
    #
#
