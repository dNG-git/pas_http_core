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

from time import time
from zlib import decompressobj, MAX_WBITS

from dNG.data.byte_buffer import ByteBuffer
from dNG.data.settings import Settings
from dNG.data.supports_mixin import SupportsMixin
from dNG.net.http.chunked_reader_mixin import ChunkedReaderMixin
from dNG.runtime.io_exception import IOException
from dNG.runtime.value_exception import ValueException

class Data(ChunkedReaderMixin, SupportsMixin):
    """
The class "Data" implements method to read the request body.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=arguments-differ

    TYPE_ID = None
    """
Body type ID
    """

    def __init__(self):
        """
Constructor __init__(Data)

:since: v0.2.00
        """

        ChunkedReaderMixin.__init__(self)
        SupportsMixin.__init__(self)

        self.decompressors = None
        """
List of decompressors
        """
        self.headers = None
        """
Dictionary with request headers
        """
        self.input_chunk_encoded = False
        """
True if the input is "chunked" encoded (and the size is unknown).
        """
        self.input_ptr = None
        """
Input pointer
        """
        self.input_size = -1
        """
Input size in bytes if known
        """
        self.received_data = None
        """
Received file-like data object
        """
        self.received_data_size = 0
        """
Size of the file-like data object
        """
        self.received_size_max = 0
        """
Allowed size in bytes of the request body
        """
        self.socket_data_timeout = int(Settings.get("pas_http_site_request_body_socket_data_timeout", 0))
        """
Timeout for each network read
        """
        self.timeout = int(Settings.get("pas_http_site_request_body_timeout", 7200))
        """
Absolute timeout to receive the request body
        """

        if (self.__class__.TYPE_ID is not None):
            self.received_size_max = int(Settings.get("pas_http_site_request_body_{0}_size_max".format(self.__class__.TYPE_ID), 0))
        #

        if (self.received_size_max < 1): self.received_size_max = int(Settings.get("pas_http_site_request_body_size_max", 2097152))

        if (self.socket_data_timeout < 1): self.socket_data_timeout = int(Settings.get("pas_global_client_socket_data_timeout", 0))
        if (self.socket_data_timeout < 1): self.socket_data_timeout = int(Settings.get("pas_global_socket_data_timeout", 30))
    #

    def _decompress(self, data):
        """
Decompresses incoming data.

:param data: Data read from input

:since: v0.2.00
        """

        _return = (data if (self.decompressors is None) else None)
        raw_data = data

        if (self.decompressors is not None):
            for decompressor in self.decompressors: raw_data = (decompressor.flush() if (data is None) else decompressor.decompress(raw_data))
            _return = raw_data
        #

        return _return
    #

    def define_input_chunk_encoded(self, chunk_encoded):
        """
Reads "chunked" encoded content if set to true.

:param chunk_encoded: True to active the "chunked" encoded mode

:since: v0.2.00
        """

        self.input_chunk_encoded = chunk_encoded
    #

    def define_input_compression(self, algorithms):
        """
Defines the input compression algorithms used.

:param algorithms: Input compression algorithms used

:since: v0.2.00
        """

        algorithms = (algorithms if (type(algorithms) is list) else [ algorithms ])
        self.decompressors = [ ]

        for algorithm in algorithms:
            if (algorithm == "deflate"): self.decompressors.append(decompressobj(MAX_WBITS))
            elif (algorithm == "gzip"): self.decompressors.append(decompressobj(16 + MAX_WBITS))
            else: raise ValueException("Unsupported compression definition '{0}' given".format(algorithm))
        #
    #

    def get(self, timeout = None):
        """
Returns the raw request body data.

:param timeout: Read timeout in seconds

:return: (str) Request body data
:since:  v0.2.00
        """

        self.read(timeout)
        return self.received_data
    #

    def _handle_data(self, data):
        """
Handles data received.

:param data: Data read from input

:since: v0.2.00
        """

        data = self._decompress(data)

        if (data is not None):
            self.received_data_size += len(data)
            if (self.received_size_max > 0 and self.received_data_size > self.received_size_max): raise ValueException("Input size exceeds allowed limit")
            self.received_data.write(data)
        #
    #

    def _init_read(self):
        """
Initializes internal variables for reading from input.

:since: v0.2.00
        """

        self.received_data = ByteBuffer()
        self.received_data_size = 0
    #

    def read(self, timeout = None):
        """
Reads the request body data and fills the buffer.

:param timeout: Read timeout in seconds

:since: v0.2.00
        """

        # pylint: disable=raising-bad-type

        if (self.input_ptr is not None):
            if (hasattr(self.input_ptr, "settimeout")): self.input_ptr.settimeout(self.socket_data_timeout)

            self._init_read()

            try: self._read(self._handle_data, timeout)
            finally: self.input_ptr = None
        #
    #

    def _read(self, read_callback, timeout = None):
        """
Reads data until the body has been received or timeout occurs.

:param read_callback: Callback used to handle data read
:param timeout: Read timeout in seconds

:since: v0.2.00
        """

        if (timeout is None): timeout = self.timeout

        if (self.input_size < 0 and (not self.input_chunk_encoded)): raise IOException("Input size and expected first chunk size are unknown")

        if (self.input_chunk_encoded): self._read_chunked_data(self.input_ptr.read, read_callback, timeout = timeout)
        else:
            timeout_time = time() + timeout
            size_unread = self.input_size

            while (size_unread > 0 and time() < timeout_time):
                part_size = (16384 if (size_unread > 16384) else size_unread)
                part_data = self.input_ptr.read(part_size)
                part_size = (0 if (part_data is None) else len(part_data))

                if (part_size < 1): raise IOException("Input pointer could not be read before socket timeout occurred")

                if (part_size > 0):
                    size_unread -= part_size
                    read_callback(part_data)
                #
            #

            if (size_unread > 0): raise IOException("Timeout occured before EOF")
        #

        if (self.decompressors is not None): read_callback(None)
    #

    def set_headers(self, headers):
        """
Sets the relevant request headers.

:param headers: Header dict

:since: v0.2.00
        """

        self.headers = headers
    #

    def set_input_ptr(self, input_ptr):
        """
Sets the file-like input pointer used to read the request body from.

:param instance: File-like instance

:since: v0.2.00
        """

        self.input_ptr = input_ptr
    #

    def set_input_size(self, _bytes):
        """
Sets the expected input size.

:param _bytes: Size in bytes

:since: v0.2.00
        """

        self.input_size = _bytes
    #

    def set_timeout(self, timeout):
        """
Sets the absolute timeout to receive the request body.

:param timeout: Timeout in seconds

:since: v0.2.00
        """

        self.timeout = timeout
    #
#
