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
from zlib import compressobj
import re

try: from dNG.data.brotli_compressor import BrotliCompressor
except ImportError: BrotliCompressor = None

from dNG.data.binary import Binary
from dNG.data.gzip_compressor import GzipCompressor
from dNG.data.http.chunked_writer_mixin import ChunkedWriterMixin
from dNG.data.rfc.basics import Basics as RfcBasics
from dNG.runtime.io_exception import IOException
from dNG.runtime.not_implemented_exception import NotImplementedException

from .abstract_http_request import AbstractHttpRequest
from .abstract_stream_response import AbstractStreamResponse

class AbstractHttpStreamResponse(ChunkedWriterMixin, AbstractStreamResponse):
    """
A HTTP aware stream response.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    STREAM_DIRECT = 1 << 1
    """
Do not set Transfer-Encoding but output content directly as soon as it is
available.
    """
    STREAM_CHUNKED = 1 << 2
    """
Set Transfer-Encoding to chunked and encode output.
    """

    def __init__(self):
        """
Constructor __init__(AbstractHttpStreamResponse)

:since: v1.0.0
        """

        AbstractStreamResponse.__init__(self)

        self._accepted_formats = [ ]
        """
Formats the client accepts
        """
        self.compressor = None
        """
Compression object or file
        """
        self._compression_formats = None
        """
Compression formats the client accepts
        """
        self.cookies = { }
        """
True if headers are sent
        """
        self.headers = { }
        """
Headers are used by the final node
        """
        self._send_only_headers = False
        """
Send headers only (usually HEAD requests)s
        """
        self.headers_index = 0
        """
Current named headers index
        """
        self.headers_indexed = { }
        """
Headers using a header index
        """
        self.headers_sent = False
        """
True if headers are sent
        """
        self._http_code = None
        """
HTTP result code
        """
        self._http_version = 2
        """
HTTP request version
        """

        self.set_header("Server", "directPAS/#echo(pasHttpCoreIVersion)# [direct Netware Group]")

        self.supported_features['compression'] = True
        self.supported_features['headers'] = True
        self.supported_features['streaming'] = True
    #

    @property
    def accepted_formats(self):
        """
Returns the formats the client accepts.

:return: (list) Accepted formats
:since:  v1.0.0
        """

        return self._accepted_formats
    #

    @accepted_formats.setter
    def accepted_formats(self, accepted_formats):
        """
Sets the formats the client accepts.

:param accepted_formats: List of accepted formats

:since: v1.0.0
        """

        if (isinstance(accepted_formats, list)): self._accepted_formats = accepted_formats
    #

    @property
    def are_headers_sent(self):
        """
Returns true if headers are already sent.

:return: (bool) True if sent
:since:  v1.0.0
        """

        return self.headers_sent
    #

    @property
    def compress_output(self):
        """
Returns true if the response will be compressed.

:return: (bool) True if compression is used for the response
:since:  v1.0.0
        """

        return (self.compressor is not None)
    #

    @compress_output.setter
    def compress_output(self, compress):
        """
Activates or deactivates response compression.

:param compress: True to compress the response

:since: v1.0.0
        """

        if (not compress or self.send_only_headers):
            self.compressor = None
            self.set_header("Content-Encoding", None)
        elif (self._compression_formats is not None):
            if (BrotliCompressor is not None and "br" in self._compression_formats):
                self.compressor = BrotliCompressor()
                self.set_header("Content-Encoding", "br")
            elif ("gzip" in self._compression_formats):
                self.compressor = GzipCompressor()
                self.set_header("Content-Encoding", "gzip")
            elif ("deflate" in self._compression_formats):
                self.compressor = compressobj()
                self.set_header("Content-Encoding", "deflate")
            #
        #

        self.update_stream_mode()
    #

    @property
    def compression_formats(self):
        """
Returns the compression formats the client accepts.

:return: (list) Compression formats supported
:since:  v1.0.0
        """

        return self._compression_formats
    #

    @compression_formats.setter
    def compression_formats(self, compression_formats):
        """
Sets the compression formats the client accepts.

:param compression_formats: List of accepted compression formats

:since: v1.0.0
        """

        if (isinstance(compression_formats, list)): self._compression_formats = compression_formats
    #

    @property
    def http_code(self):
        """
Returns the HTTP response code.

:return: (int) HTTP code
:since:  v1.0.0
        """

        return (200 if (self._http_code is None) else self._http_code)
    #

    @http_code.setter
    def http_code(self, http_code):
        """
Sets the HTTP response code.

:param http_code: HTTP code

:since: v1.0.0
        """

        self._http_code = http_code
    #

    @property
    def http_version(self):
        """
Returns the HTTP protocol version in use.

:return: (float) HTTP version in use
:since:  v1.0.0
        """

        return self._http_version
    #

    @http_version.setter
    def http_version(self, http_version):
        """
Sets the HTTP protocol version.

:param http_version: HTTP version

:since: v1.0.0
        """

        if (type(http_version) not in ( int, float )): http_version = float(http_version)
        self._http_version = http_version
    #

    @property
    def send_only_headers(self):
        """
Returns true to send headers only.

:return: (bool) Usually true for HEAD requests
:since:  v1.0.0
        """

        return self._send_only_headers
    #

    @send_only_headers.setter
    def send_only_headers(self, headers_only):
        """
Set to true to send headers only.

:param headers_only: Usually true for HEAD requests

:since: v1.0.0
        """

        self._send_only_headers = headers_only
    #

    @AbstractStreamResponse.streamer.setter
    def streamer(self, streamer):
        """
Sets the streamer to create response data when requested.

:since: v1.0.0
        """

        AbstractStreamResponse.streamer.fset(self, streamer)
        self.update_stream_mode()
    #

    def _filter_headers(self):
        """
Filter response headers to remove conflicting ones.

:return: (dict) Filtered headers
:since:  v1.0.0
        """

        _return = self.headers.copy()

        if ((self.compressor is not None
             or self.stream_mode & AbstractHttpStreamResponse.STREAM_CHUNKED == AbstractHttpStreamResponse.STREAM_CHUNKED
            )
            and "content-length" in _return
           ): del(_return['content-length'])

        if (len(self.cookies) > 0):
            if ("set-cookie" not in _return): _return['set-cookie'] = [ ]
            elif (type(_return['set-cookie']) is not list): _return['set-cookie'] = [ _return['set-cookie'] ]

            for cookie_name in self.cookies: _return['set-cookie'].append(self.cookies[cookie_name])
        #

        return _return
    #

    def finish(self):
        """
Finish transmission and cleanup resources.

:since: v1.0.0
        """

        if (self.active):
            is_chunked_response = False

            if (self.stream_mode & AbstractHttpStreamResponse.STREAM_CHUNKED == AbstractHttpStreamResponse.STREAM_CHUNKED):
                is_chunked_response = True
                self.send()
            #

            if (is_chunked_response or self.compressor is not None): self.send_data(None)

            AbstractStreamResponse.finish(self)
            self.compressor = None
        #
    #

    def get_header(self, name, name_as_key = True):
        """
Returns an already defined header.

:param name: Header name
:param name_as_key: True if the name is used as a key

:return: (str) Header value if set; None otherwise
:since:  v1.0.0
        """

        name = name.lower()

        if (name in self.headers): _return = self.headers[name]
        elif (name_as_key and name in self.headers_indexed): _return = self.headers[self.headers_indexed[name]]
        else: _return = None

        return _return
    #

    def _prepare_output_data(self, data):
        """
Prepare data for output. Compress and transform it if required.

:param data: Data for output

:return: (bytes) Transformed data
:since:  v1.0.0
        """

        is_chunked_response = (self.stream_mode & AbstractHttpStreamResponse.STREAM_CHUNKED == AbstractHttpStreamResponse.STREAM_CHUNKED)

        if (self.compressor is not None):
            if (data is None): data = self.compressor.flush()
            elif (len(data) > 0): data = self.compressor.compress(Binary.bytes(data))
        #

        if (is_chunked_response): data = self.chunkify(data)

        return data
    #

    def send_data(self, data):
        """
Sends response data.

:param data: Additional data to be send

:since: v1.0.0
        """

        if (self.active):
            if (not self.headers_sent):
                if (self._http_code is None): self.http_code = 200
                self.send_headers()
            #

            if (not self._send_only_headers): AbstractStreamResponse.send_data(self, self._prepare_output_data(data))
        #
    #

    def send_headers(self):
        """
Sends the prepared response headers.

:since: v1.0.0
        """

        raise NotImplementedException()
    #

    def set_cookie(self, name, value, timeout = 1209600, secure_only = False, http_only = False, domain = None, path = None):
        """
Sets a cookie.

:param name: Cookie name
:param value: Cookue value as string
:param timeout: Cookie timeout in seconds (max-age)
:param secure_only: True if send "secure" flag
:param http_only: True if send "httpOnly" flag
:param domain: Cookie domain restriction (defaults to requested host)
:param path: Cookie path restriction (defaults to "/")

:since: v1.0.0
        """

        if (";" in value or '"' in value):
            value = value.replace('"', '\"')
            value = '"{0}"'.format(value)
        #

        timeout = (time() + timeout if (timeout > 0) else time() - 3600)

        cookie = "{0}={1};Expires={2}".format(name, value, RfcBasics.get_rfc5322_datetime(timeout))
        if (secure_only): cookie += ";Secure="
        if (http_only): cookie += ";HttpOnly="

        if (domain is None):
            request = AbstractHttpRequest.get_instance()
            if (request is not None): cookie += ";Domain={0}".format(request.server_host)
        else: cookie += ";Domain={0}".format(domain)

        if (path is None): path = "/"
        cookie += ";Path={0}".format(path)

        self.cookies[name] = cookie
    #

    def set_header(self, name, value, name_as_key = False, value_append = False):
        """
Sets a header.

:param name: Header name
:param value: Header value as string or array
:param name_as_key: True if the name is used as a key
:param value_append: True if headers should be appended

:since: v1.0.0
        """

        if (self.headers_sent): raise IOException("Headers are already sent")
        name = name.lower()

        if (name_as_key and name == "http"):
            http_values = value.split(" ", 2)

            if (len(http_values) == 3):
                self.http_code = int(http_values[1])
                http_version = self.http_version

                if (http_version == 1):
                    if (http_values[2] == "Non-Authoritative Information"): value = "HTTP/2.0 200 OK"
                    elif (http_values[2] == "See Other"): value = "HTTP/2.0 302 Found"
                    elif (http_values[2] == "Temporary Redirect"): value = "HTTP/2.0 302 Found"
                #

                if (http_version % 1 == 0): http_version = "{0:0.0f}.0".format(http_version)
                else: http_version = str(http_version)

                value = re.sub("HTTP/\\d\\.\\d (\\d+ .+)$",
                               "HTTP/{0} \\1".format(http_version),
                               value
                              )
            #
        #

        if (name_as_key):
            if (name in self.headers_indexed):
                if (value is None): del(self.headers[self.headers_indexed[name]])
                elif (value_append):
                    if (type(self.headers[self.headers_indexed[name]]) is list): self.headers[self.headers_indexed[name]].append(value)
                    else: self.headers[self.headers_indexed[name]] = [ self.headers[self.headers_indexed[name]], value ]
                else: self.headers[self.headers_indexed[name]] = value
            elif (value is not None):
                self.headers[self.headers_index] = value
                self.headers_indexed[name] = self.headers_index
                self.headers_index += 1
            #
        elif (value is None):
            if (name in self.headers): del(self.headers[name])
        elif (type(value) is list): self.headers[name] = (value if (len(value) > 1) else value.pop())
        elif (value_append and name in self.headers):
            if (type(self.headers[name]) is list): self.headers[name].append(value)
            else: self.headers[name] = [ self.headers[name], value ]
        else: self.headers[name] = value
    #

    def update_stream_mode(self):
        """
Sets the stream mode or updates the stream mode algorithm selected to send
output as soon as available instead of caching it.

:since: v1.0.0
        """

        is_chunked_mode_required = (self.get_header("Content-Length") is None
                                    or self.compressor is not None
                                   )

        is_chunked_mode_supported = (self.stream_mode_supported & AbstractHttpStreamResponse.STREAM_CHUNKED == AbstractHttpStreamResponse.STREAM_CHUNKED
                                     and self.http_version > 1
                                    )

        if (is_chunked_mode_supported
            and (not is_chunked_mode_required)
            and self.stream_mode & AbstractHttpStreamResponse.STREAM_CHUNKED == AbstractHttpStreamResponse.STREAM_CHUNKED
           ):
            if (self.get_header("Transfer-Encoding") == "chunked"): self.set_header("Transfer-Encoding", None)
            self.stream_mode ^= AbstractHttpStreamResponse.STREAM_CHUNKED
        #

        is_direct_mode_supported = (self.stream_mode_supported & AbstractHttpStreamResponse.STREAM_DIRECT == AbstractHttpStreamResponse.STREAM_DIRECT)

        if ((not is_direct_mode_supported)
            and self.stream_mode & AbstractHttpStreamResponse.STREAM_DIRECT == AbstractHttpStreamResponse.STREAM_DIRECT
           ): self.stream_mode ^= AbstractHttpStreamResponse.STREAM_DIRECT

        if (is_chunked_mode_supported and is_chunked_mode_required):
            self.set_header("Transfer-Encoding", "chunked")
            self.stream_mode |= AbstractHttpStreamResponse.STREAM_CHUNKED
        elif (is_direct_mode_supported): self.stream_mode |= AbstractHttpStreamResponse.STREAM_DIRECT
    #
#
