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

from dNG.data.binary import Binary
from dNG.data.http.translatable_error import TranslatableError as HttpTranslatableError
from dNG.data.http.translatable_exception import TranslatableException as HttpTranslatableException
from dNG.data.rfc.basics import Basics as RfcBasics
from dNG.data.settings import Settings
from dNG.data.text.l10n import L10n
from dNG.data.traced_exception import TracedException
from dNG.data.translatable_exception import TranslatableException
from dNG.runtime.io_exception import IOException
from dNG.runtime.type_exception import TypeException

from .abstract_response import AbstractResponse
from .abstract_stream_response import AbstractStreamResponse

class AbstractHttpResponse(AbstractResponse):
    """
The following abstract class implements HTTP response specific methods.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self):
        """
Constructor __init__(AbstractHttpResponse)

:since: v1.0.0
        """

        AbstractResponse.__init__(self)

        self._charset = "utf-8"
        """
Charset used for response
        """
        self._content_uncachable = False
        """
True if the content is dynamic
        """
        self.cookies = { }
        """
Cookies to be send
        """
        self._data = None
        """
Data to be send
        """
        self.errors = None
        """
Errors that should be shown.
        """
        self._expires = 0
        """
Expiring UNIX timestamp
        """
        self.headers_sent = False
        """
True if headers are sent
        """
        self.initialized = False
        """
True if "init()" has been called
        """
        self._last_modified = 0
        """
Last modified UNIX timestamp
        """
        self._script_name = None
        """
Called script
        """
        self._stream_response = None
        """
Stream response object
        """

        self.supported_features['buffered_data'] = True
        self.supported_features['headers'] = True
        self.supported_features['raw_buffered_data'] = True
        self.supported_features['script_name'] = True
        self.supported_features['streaming'] = self._supports_streaming
    #

    @property
    def accepted_formats(self):
        """
Returns the formats the client accepts.

:return: (list) Accepted formats
:since:  v1.0.0
        """

        return self.stream_response.accepted_formats
    #

    @accepted_formats.setter
    def accepted_formats(self, accepted_formats):
        """
Sets the formats the client accepts.

:param accepted_formats: List of accepted formats

:since: v1.0.0
        """

        self.stream_response.accepted_formats = accepted_formats
    #

    @property
    def are_headers_sent(self):
        """
Returns true if headers are already sent.

:return: (bool) True if sent
:since:  v1.0.0
        """

        return (self.stream_response.are_headers_sent if (self.stream_response.is_supported("headers")) else None)
    #

    @property
    def charset(self):
        """
Gets the charset defined for the response.

:return: (str) Charset used for response
:since:  v1.0.0
        """

        return self._charset
    #

    @charset.setter
    def charset(self, charset):
        """
Sets the charset used for the response.

:param charset: Charset used for response

:since: v1.0.0
        """

        self._charset = charset
    #

    @property
    def compression_formats(self):
        """
Returns the compression formats the client accepts.

:return: (list) Compression formats supported
:since:  v1.0.0
        """

        return self.stream_response.get_compression_formats()
    #

    @compression_formats.setter
    def compression_formats(self, compression_formats):
        """
Sets the compression formats the client accepts.

:param compression_formats: List of accepted compression formats

:since: v1.0.0
        """

        if (self.stream_response.is_supported("compression")): self.stream_response.compression_formats = compression_formats
    #

    @property
    def content_type(self):
        """
Returns the current HTTP Content-Type header.

:return: (str) HTTP Content-Type header; None if undefined
:since:  v1.0.0
        """

        return self.get_header("Content-Type")
    #

    @content_type.setter
    def content_type(self, content_type):
        """
Sets the HTTP Content-Type header.

:param content_type: HTTP Content-Type header

:since: v1.0.0
        """

        self.set_header("Content-Type", content_type)
    #

    @property
    def content_uncachable(self):
        """
Returns if the content is uncacheable. This overrides the last modified
timestamp with the current time.

:return: (bool) True if the content is uncacheable
:since:  v1.0.0
        """

        return self._content_uncachable
    #

    @content_uncachable.setter
    def content_uncachable(self, mode):
        """
Sets if the content is uncacheable.

:param mode: True if the content is uncacheable

:since: v1.0.0
        """

        if (mode and self.initialized):
            current_time = int(time())

            self._expires = current_time
            self._last_modified = current_time
        #

        self._content_uncachable = mode
    #

    @property
    def data(self):
        """
Returns buffered data to be transmitted.

:return: (bytes) Data to be send
:since:  v1.0.0
        """

        return Binary.bytes(self._data)
    #

    @property
    def expires(self):
        """
Returns an expires value set.

:return: (int) UNIX timestamp
:since:  v1.0.0
        """

        return self._expires
    #

    @expires.setter
    def expires(self, timestamp):
        """
Sets a expires value if the response is not in dynamic mode.

:param timestamp: UNIX timestamp

:since: v1.0.0
        """

        if (not self._content_uncachable): self._set_expires(int(timestamp))
    #

    @property
    def http_code(self):
        """
Returns the HTTP response code.

:return: (int) HTTP code
:since:  v1.0.0
        """

        return self.stream_response.http_code
    #

    @property
    def last_modified(self):
        """
Returns a last modified value set.

:return: (int) UNIX timestamp
:since:  v1.0.0
        """

        return self._last_modified
    #

    @last_modified.setter
    def last_modified(self, timestamp):
        """
Sets a last modified value if the response is not in dynamic mode.

:param timestamp: UNIX timestamp

:since: v1.0.0
        """

        if (not self._content_uncachable): self._set_last_modified(int(timestamp))
    #

    @property
    def raw_data(self):
        """
Raw data ignores any protocol specific transformation and returns the data
as given.

:return: (mixed) Data to be send
:since:  v1.0.0
        """

        return self._data
    #

    @raw_data.setter
    def raw_data(self, data):
        """
Raw data ignores any protocol specific transformation and buffers the data as
given.

:param data: Data to be send

:since: v1.0.0
        """

        if (self.stream_response.is_streamer_set): raise IOException("Can't combine a streaming object with raw data.")
        self._data = data
    #

    @property
    def script_name(self):
        """
Returns the called script name.

:return: File name
:since:  v1.0.0
        """

        return self._script_name
    #

    @script_name.setter
    def script_name(self, script_name):
        """
Sets the called script name.

:param script_name: File name

:since: v1.0.0
        """

        self._script_name = script_name
    #

    @property
    def send_only_headers(self):
        """
Returns true to send headers only.

:return: (bool) Usually true for HEAD requests
:since:  v1.0.0
        """

        return (self.stream_response.send_only_headers if (self.stream_response.is_supported("headers")) else False)
    #

    @send_only_headers.setter
    def send_only_headers(self, headers_only):
        """
Set to true to send headers only.

:param headers_only: Usually true for HEAD requests

:since: v1.0.0
        """

        if (self.stream_response.is_supported("headers")): self.stream_response.send_only_headers = headers_only
    #

    @property
    def stream_response(self):
        """
Sets the stream response object used to send data to.

:return: (bool) Stream response
:since:  v1.0.0
        """

        if (self._stream_response is None): raise IOException("Response instance has not been successfully configured")
        return self._stream_response
    #

    @stream_response.setter
    def stream_response(self, stream_response):
        """
Sets the stream response object used to send data to.

:param stream_response: Stream response

:since: v1.0.0
        """

        if (not isinstance(stream_response, AbstractStreamResponse)): raise TypeException("Stream response given is invalid")
        self._stream_response = stream_response
    #

    @property
    def streamer(self):
        """
Returns the streamer to create response data when requested.

:return: (object) Streamer instance if set
:since:  v1.0.0
        """

        return self.stream_response.streamer
    #

    @streamer.setter
    def streamer(self, streamer):
        """
Sets the streamer to create response data when requested.

:return: (object) Streamer instance to be set

:since: v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("{0!r} starts streaming with an IO chunk size of {1:d}", self, streamer.io_chunk_size, context = "pas_http_core")
        self.stream_response.streamer = streamer
    #

    def get_header(self, name, name_as_key = True):
        """
Returns an already defined header.

:param name: Header name
:param name_as_key: True if the name is used as a key

:return: (str) Header value if set; None otherwise
:since:  v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -{0!r}.get_header({1})- (#echo(__LINE__)#)", self, name, context = "pas_http_core")

        if (not self.stream_response.is_supported("headers")): return None
        else: return self.stream_response.get_header(name, name_as_key)
    #

    def handle_critical_error(self, message):
        """
"handle_critical_error()" is called to send a critical error message.

:param message: Message (will be translated if possible)

:since: v1.0.0
        """

        message = L10n.get("errors_{0}".format(message), message)

        if (self.errors is None): self.errors = [ { "title": L10n.get("core_title_error_critical"), "message": message } ]
        else: self.errors.append({ "title": L10n.get("core_title_error_critical"), "message": message })
    #

    def handle_error(self, message):
        """
"handle_error()" is called to send a error message.

:param message: Message (will be translated if possible)

:since: v1.0.0
        """

        message = L10n.get("errors_{0}".format(message), message)

        if (self.errors is None): self.errors = [ { "title": L10n.get("core_title_error"), "message": message } ]
        else: self.errors.append({ "title": L10n.get("core_title_error"), "message": message })
    #

    def handle_exception(self, message, exception):
        """
"handle_exception()" is called if an exception occurs and should be
send.

:param message: Message (will be translated if possible)
:param exception: Original exception or formatted string (should be shown in
                  dev mode)

:since: v1.0.0
        """

        is_critical = True

        if (self.get_header("HTTP", True) is None):
            if (isinstance(exception, HttpTranslatableError)):
                code = exception.http_code
                header_message = exception.http_message

                is_critical = isinstance(exception, HttpTranslatableException)

                if (header_message is not None):
                    self.set_header("HTTP", "HTTP/2.0 {0:d} {1}".format(code, header_message), True)
                elif (code == 200): self.set_header("HTTP", "HTTP/2.0 200 OK", True)
                elif (code == 201): self.set_header("HTTP", "HTTP/2.0 201 Created", True)
                elif (code == 202): self.set_header("HTTP", "HTTP/2.0 202 Accepted", True)
                elif (code == 204): self.set_header("HTTP", "HTTP/2.0 204 No Content", True)
                elif (code == 205): self.set_header("HTTP", "HTTP/2.0 205 Reset Content", True)
                elif (code == 400): self.set_header("HTTP", "HTTP/2.0 400 Bad Request", True)
                elif (code == 401): self.set_header("HTTP", "HTTP/2.0 401 Unauthorized", True)
                elif (code == 402): self.set_header("HTTP", "HTTP/2.0 402 Payment Required", True)
                elif (code == 403): self.set_header("HTTP", "HTTP/2.0 403 Forbidden", True)
                elif (code == 404): self.set_header("HTTP", "HTTP/2.0 404 Not Found", True)
                elif (code == 405): self.set_header("HTTP", "HTTP/2.0 405 Method Not Allowed", True)
                elif (code == 410): self.set_header("HTTP", "HTTP/2.0 410 Gone", True)
                elif (code == 500): self.set_header("HTTP", "HTTP/2.0 500 Internal Server Error", True)
                elif (code == 501): self.set_header("HTTP", "HTTP/2.0 501 Not Implemented", True)
                elif (code == 502): self.set_header("HTTP", "HTTP/2.0 502 Bad Gateway", True)
                elif (code == 503): self.set_header("HTTP", "HTTP/2.0 503 Service Unavailable", True)
                elif (code == 504): self.set_header("HTTP", "HTTP/2.0 504 Gateway Timeout", True)
                else: self.set_header("HTTP", "HTTP/2.0 {0:d} Code {0:d}".format(code), True)
            else:
                self.set_header("HTTP", "HTTP/2.0 500 Internal Server Error", True)
            #
        #

        title = (L10n.get("core_title_error_critical") if (is_critical) else L10n.get("core_title_error"))

        if (message is None and isinstance(exception, TranslatableException)): message = "{0:l10n_message}".format(exception)
        if (not isinstance(exception, TracedException)): exception = TracedException(message, exception)

        if (message is None): message = L10n.get("errors_core_unknown_error")
        else: message = L10n.get("errors_{0}".format(message), message)

        error_data = { "title": title,
                       "message": message,
                       "details": (exception.printable_trace
                                   if (Settings.get("pas_core_dev_mode", False)) else
                                   str(exception)
                                  )
                     }

        if (self.errors is None): self.errors = [ error_data ]
        else: self.errors.append(error_data)
    #

    def init(self, cache = False, compress = True):
        """
Important headers will be created here. This includes caching, cookies and
compression setting used.

:param cache: Allow caching at client
:param compress: Send page GZip encoded (if supported)

:since: v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -{0!r}.init()- (#echo(__LINE__)#)", self, context = "pas_http_core")

        expires = self.expires
        last_modified = self._last_modified

        if (self._content_uncachable):
            cache = False
            current_time = int(time())

            expires = current_time
            last_modified = current_time
        elif (not cache):
            if (expires < 1): expires = int(time())
            if (last_modified < 1): last_modified = int(time())
        #

        if (self.stream_response.is_supported("compression")): self.stream_response.compress_output = compress

        self.initialized = True

        if (self.stream_response.is_supported("headers")):
            output_headers = ({ "Cache-Control": "public" } if (cache) else { "Cache-Control": "no-cache, no-store, must-revalidate" })
            if (not cache): output_headers['X-Robots-Tag'] = "noindex"

            csp = Settings.get("pas_http_core_csp_header", "")
            if (csp != ""): output_headers['Content-Security-Policy'] = csp

            for header in output_headers:
                self.stream_response.set_header(header, output_headers[header])
            #

            if (expires > 0): self._set_expires(expires)
            if (last_modified > 0): self._set_last_modified(last_modified)
        #
    #

    def redirect(self, url):
        """
Redirect the requesting client to the given URL.

:param url: Target URL

:since: v1.0.0
        """

        if (not self.initialized): self.init()

        if (self._content_uncachable
            or self.expires <= time()
           ): self.set_header("HTTP", "HTTP/2.0 307 Temporary Redirect", True)
        else: self.set_header("HTTP", "HTTP/2.0 303 See Other", True)

        self.set_header("Location", url)
    #

    def reset(self):
        """
Resets all cached values.

:since: v1.0.0
        """

        self._content_uncachable = False
        self._data = None
        self.errors = None
        self._expires = 0
        self.initialized = False
        self._last_modified = 0
    #

    def send(self):
        """
Sends the prepared response.

:since: v1.0.0
        """

        if (self._data is None): self.stream_response.send()
        else: self.stream_response.send_data(self.data)
    #

    def send_and_finish(self):
        """
Sends the prepared response and finishes all related tasks.

:since: v1.0.0
        """

        if (self.stream_response.is_supported("headers")
            and self._data is not None
            and (not self.headers_sent)
           ): self.set_header("Content-Length", len(self._data))

        AbstractResponse.send_and_finish(self)
        self.reset()
    #

    def send_headers(self):
        """
Sends the prepared response headers.

:since: v1.0.0
        """

        if (self.stream_response.is_supported("headers") and (not self.headers_sent)):
            self.headers_sent = True
            self.stream_response.send_headers()
        #
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

        if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_cookie({1}, {2:d})- (#echo(__LINE__)#)", self, name, timeout, context = "pas_http_core")
        if (self.stream_response.is_supported("headers")): self.stream_response.set_cookie(name, value, timeout, secure_only, http_only, domain, path)
    #

    def _set_expires(self, timestamp):
        """
Sets a expires value.

:param timestamp: UNIX timestamp

:since: v1.0.0
        """

        self._expires = timestamp
        if (self.initialized and self.stream_response.is_supported("headers") and (not self.headers_sent)): self.stream_response.set_header("Expires", RfcBasics.get_rfc5322_datetime(self._expires))
    #

    def set_expires_relative(self, timespan):
        """
Sets a expires value based on the current time if the response is not in
dynamic mode. For better readability we recommend using +5/-5.

:param timespan: Timespan in seconds

:since: v1.0.0
        """

        self.expires = int(time() + timespan)
    #

    def set_header(self, name, value, name_as_key = False, value_append = False):
        """
Sets a header.

:param name: Header name
:param value: Header value as string or list
:param name_as_key: True if the name is used as a key
:param value_append: True if headers should be appended

:since: v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_header({1})- (#echo(__LINE__)#)", self, name, context = "pas_http_core")
        if (self.stream_response.is_supported("headers")): self.stream_response.set_header(name, value, name_as_key, value_append)
    #

    def _set_last_modified(self, timestamp):
        """
Sets a last modified value.

:param timestamp: UNIX timestamp

:since: v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -{0!r}._set_last_modified({1:d})- (#echo(__LINE__)#)", self, timestamp, context = "pas_http_core")

        self._last_modified = timestamp
        if (self.initialized and self.stream_response.is_supported("headers") and (not self.headers_sent)): self.stream_response.set_header("Last-Modified", RfcBasics.get_rfc5322_datetime(self._last_modified))
    #

    def _supports_streaming(self):
        """
Returns false if responses can not be streamed.

:return: (bool) True if streaming is supported.
:since:  v1.0.0
        """

        return (False if (self._stream_response is None) else self.stream_response.is_supported("streaming"))
    #
#
