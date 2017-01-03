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

from dNG.data.streamer.http_compressed import HttpCompressed as HttpCompressedStreamer
from dNG.runtime.iterator import Iterator

from .abstract_http_stream_response import AbstractHttpStreamResponse

class AbstractHttpCgiStreamResponse(Iterator, AbstractHttpStreamResponse):
    """
This stream response instance will write all data to the underlying WSGI 1.0
implementation.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self):
        """
Constructor __init__(HttpWsgi1StreamResponse)

:since: v0.2.00
        """

        AbstractHttpStreamResponse.__init__(self)

        self.stream_mode_supported |= AbstractHttpCgiStreamResponse.STREAM_DIRECT
    #

    def __iter__(self):
        """
python.org: Return an iterator object.

:return: (object) Iterator object
:since:  v0.2.00
        """

        if (not self.headers_sent): self.send_headers()
        _return = self

        if (self.streamer is not None):
            if (self.compressor is not None):
                _return = HttpCompressedStreamer(self.streamer, self.compressor)
                self.compressor = None
            else: _return = self.streamer
        #

        return _return
    #

    def __next__(self):
        """
python.org: Return the next item from the container.

:return: (bytes) Response data
:since:  v0.2.00
        """

        _return = None

        if (self.active and (not self.headers_only)):
            """
This iterator is only called for uncompressed data.
            """

            if (self.streamer is not None):
                _return = (None if (self.streamer.is_eof()) else self.streamer.read())
                if (_return is not None): _return = self._prepare_output_data(_return)
            elif (self.data is not None):
                _return = self.data
                self.data = None
            #
        #

        if (_return is None):
            self.finish()
            raise StopIteration()
        #

        return _return
    #
#
