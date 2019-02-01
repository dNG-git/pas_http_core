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

from collections import OrderedDict
from time import time
from zlib import decompressobj, MAX_WBITS

try: from dNG.data.brotli_decompressor import BrotliDecompressor
except ImportError: BrotliDecompressor = None

from dNG.data.byte_buffer import ByteBuffer
from dNG.data.http.chunked_reader_mixin import ChunkedReaderMixin
from dNG.data.settings import Settings
from dNG.data.supports_mixin import SupportsMixin
from dNG.runtime.io_exception import IOException
from dNG.runtime.value_exception import ValueException

class Data(ChunkedReaderMixin, SupportsMixin):
    """
The class "Data" implements method to read the request body.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
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

:since: v1.0.0
        """

        ChunkedReaderMixin.__init__(self)
        SupportsMixin.__init__(self)

        self._chunk_encoded = False
        """
True if the input is "chunked" encoded (and the size is unknown).
        """
        self.decompressors = OrderedDict()
        """
List of decompressors
        """
        self._headers = None
        """
Dictionary with request headers
        """
        self._input_ptr = None
        """
Input pointer
        """
        self._size = -1
        """
Input size in bytes if known
        """
        self._received_data = None
        """
Received file-like data object
        """
        self._received_size = 0
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
        self._timeout = int(Settings.get("pas_http_site_request_body_timeout", 7200))
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

    @property
    def buffer(self):
        """
Returns the raw request body data.

:return: (bytes) Request body data
:since:  v1.0.0
        """

        return self.get_buffer()
    #

    @property
    def chunk_encoded(self):
        """
Returns true if input data is "chunk" encoded.

:return: (bool) True if "chunked" input mode is activated
:since:  v1.0.0
        """

        return self._chunk_encoded
    #

    @chunk_encoded.setter
    def chunk_encoded(self, chunk_encoded):
        """
Reads "chunked" encoded content if set to true.

:param chunk_encoded: True to active the "chunked" encoded mode

:since: v1.0.0
        """

        self._chunk_encoded = chunk_encoded
    #

    @property
    def compression(self):
        """
Returns the list of input compression algorithms used.

:return: (list) Input compression algorithms used
:since:  v1.0.0
        """

        return list(self.decompressors)
    #

    @compression.setter
    def compression(self, algorithms):
        """
Sets the input compression algorithms used.

:param algorithms: Input compression algorithms used

:since: v1.0.0
        """

        algorithms = (algorithms if (type(algorithms) is list) else [ algorithms ])
        self.decompressors.clear()

        for algorithm in algorithms:
            if (BrotliDecompressor is not None and algorithm == "br"): self.decompressors['br'] = BrotliDecompressor()
            elif (algorithm == "gzip"): self.decompressors['gzip'] = decompressobj(16 + MAX_WBITS)
            elif (algorithm == "deflate"): self.decompressors['deflate'] = decompressobj(MAX_WBITS)
        #
    #

    @property
    def headers(self):
        """
Returns the input request body relevant request headers.

:return: (dict) Headers dict
:since:  v1.0.0
        """

        return ({ } if (self._headers is None) else self._headers)
    #

    @headers.setter
    def headers(self, headers):
        """
Sets the input request body relevant request headers.

:param headers: Headers dict

:since: v1.0.0
        """

        self._headers = headers
    #

    @property
    def input_ptr(self):
        """
Returns the file-like input pointer used to read the request body from.

:return: (object) File-like instance
:since:  v1.0.0
        """

        return self._input_ptr
    #

    @input_ptr.setter
    def input_ptr(self, input_ptr):
        """
Sets the file-like input pointer used to read the request body from.

:param input_ptr: File-like instance

:since: v1.0.0
        """

        self._input_ptr = input_ptr
    #

    @property
    def size(self):
        """
Returns the input size read.

:return: (int) Size in bytes
:since:  v1.0.0
        """

        return self._received_size
    #

    @size.setter
    def size(self, _bytes):
        """
Sets the expected input size.

:param _bytes: Size in bytes

:since: v1.0.0
        """

        self._size = _bytes
    #

    @property
    def timeout(self):
        """
Returns the absolute timeout to receive the request body.

:return: Timeout in seconds
:since:  v1.0.0
        """

        return self._timeout
    #

    @timeout.setter
    def timeout(self, timeout):
        """
Sets the absolute timeout to receive the request body.

:param timeout: Timeout in seconds

:since: v1.0.0
        """

        self._timeout = timeout
    #

    def _decompress(self, data):
        """
Decompresses incoming data.

:param data: Data read from input

:since: v1.0.0
        """

        _return = (data if (self.decompressors is None) else None)
        raw_data = data

        if (self.decompressors is not None):
            for decompressor_name in self.decompressors:
                decompressor = self.decompressors[decompressor_name]
                raw_data = (decompressor.flush() if (data is None) else decompressor.decompress(raw_data))
            #

            _return = raw_data
        #

        return _return
    #

    def get_buffer(self, timeout = None):
        """
Returns the raw request body data.

:param timeout: Read timeout in seconds

:return: (str) Request body data
:since:  v1.0.0
        """

        self.read(timeout)
        return self._received_data
    #

    def _handle_data(self, data):
        """
Handles data received.

:param data: Data read from input

:since: v1.0.0
        """

        data = self._decompress(data)

        if (data is not None):
            self._received_size += len(data)
            if (self.received_size_max > 0 and self._received_size > self.received_size_max): raise ValueException("Input size exceeds allowed limit")
            self._received_data.write(data)
        #
    #

    def _init_read(self):
        """
Initializes internal variables for reading from input.

:since: v1.0.0
        """

        self._received_data = ByteBuffer()
        self._received_size = 0
    #

    def read(self, timeout = None):
        """
Reads the request body data and fills the buffer.

:param timeout: Read timeout in seconds

:since: v1.0.0
        """

        # pylint: disable=raising-bad-type

        if (self._input_ptr is not None):
            self._init_read()

            if (hasattr(self._input_ptr, "settimeout")):
                if (timeout is None): timeout = self.timeout
                self._input_ptr.settimeout(min(self.socket_data_timeout, timeout))
            #

            try: self._read(self._handle_data, timeout)
            finally: self._input_ptr = None
        #
    #

    def _read(self, read_callback, timeout = None):
        """
Reads data until the body has been received or timeout occurs.

:param read_callback: Callback used to handle data read
:param timeout: Read timeout in seconds

:since: v1.0.0
        """

        if (timeout is None): timeout = self.timeout
        is_chunk_encoded = self.chunk_encoded

        if (self.size < 0 and (not is_chunk_encoded)): raise IOException("Input size and expected first chunk size are unknown")

        if (is_chunk_encoded): self._read_chunked_data(self._input_ptr.read, read_callback, timeout = timeout)
        else:
            timeout_time = time() + timeout
            size_unread = self._size

            while (size_unread > 0 and time() < timeout_time):
                part_size = (16384 if (size_unread > 16384) else size_unread)
                part_data = self._input_ptr.read(part_size)
                part_size = (0 if (part_data is None) else len(part_data))

                if (part_size < 1): raise IOException("Input pointer could not be read before socket timeout occurred")

                if (part_size > 0):
                    size_unread -= part_size
                    read_callback(part_data)
                #
            #

            if (size_unread > 0): raise IOException("Timeout occured before EOF")
        #

        if (len(self.decompressors) > 0): read_callback(None)
    #
#
