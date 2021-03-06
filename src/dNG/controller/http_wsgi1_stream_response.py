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
from dNG.data.streamer.abstract import Abstract as AbstractStreamer
from dNG.data.streamer.http_wsgi1 import HttpWsgi1 as HttpWsgi1Streamer

from .abstract_http_cgi_stream_response import AbstractHttpCgiStreamResponse

class HttpWsgi1StreamResponse(AbstractHttpCgiStreamResponse):
    """
This stream response instance will write all data to the underlying WSGI 1.0
implementation.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self, wsgi_header_response, wsgi_file_wrapper = None):
        """
Constructor __init__(HttpWsgi1StreamResponse)

:param wsgi_header_response: WSGI header response callback
:param wsgi_file_wrapper: The WSGI file wrapper callback

:since: v1.0.0
        """

        AbstractHttpCgiStreamResponse.__init__(self)

        self.wsgi_file_wrapper = wsgi_file_wrapper
        """
The WSGI file wrapper callback
        """
        self.wsgi_header_response = wsgi_header_response
        """
The WSGI header response callback
        """
        self.wsgi_write = None
        """
The WSGI response writer callback
        """
    #

    def __iter__(self):
        """
python.org: Return an iterator object.

:return: (object) Iterator object
:since:  v1.0.0
        """

        _return = AbstractHttpCgiStreamResponse.__iter__(self)

        if (isinstance(_return, AbstractStreamer)
            and self.wsgi_file_wrapper is not None
           ): _return = self.wsgi_file_wrapper(HttpWsgi1Streamer(_return))

        return _return
    #

    def close(self):
        """
PEP 333: If the iterable returned by the application has a close() method,
the server or gateway must call that method upon completion of the current
request, whether the request was completed normally, or terminated early due
to an error.

:since: v1.0.0
        """

        self.finish()
    #

    def finish(self):
        """
Finish transmission and cleanup resources.

:since: v1.0.0
        """

        if (self.active):
            AbstractHttpCgiStreamResponse.finish(self)
            self.wsgi_write = None
        #
    #

    def send_headers(self):
        """
Sends the prepared response headers.

:since: v1.0.0
        """

        http_status_line = "200 OK"

        headers = [ ]
        headers_indexed = dict([( value, key ) for ( key, value ) in self.headers_indexed.items()])
        filtered_headers = self._filter_headers()

        for header_name in filtered_headers:
            if (type(header_name) is int):
                header_value = str(filtered_headers[header_name])
                header_name = headers_indexed[header_name]

                if (header_name == "http"): http_status_line = header_value[9:]
                else: headers.append(( header_name, header_value ))
            elif (type(filtered_headers[header_name]) is list):
                for header_list_value in filtered_headers[header_name]:
                    header_list_value = str(header_list_value)
                    headers.append(( header_name, header_list_value ))
                #
            else:
                header_value = str(filtered_headers[header_name])
                headers.append(( header_name, header_value ))
            #
        #

        self.headers_sent = True
        self.wsgi_write = self.wsgi_header_response(http_status_line, headers)
        self.wsgi_header_response = None
    #

    def _write(self, data):
        """
Writes the given data.

:param data: Data to be send

:since: v1.0.0
        """

        # pylint: disable=broad-except

        if (not self.headers_sent): self.send_headers()

        try:
            if (self.active and (not self.send_only_headers) and self.wsgi_write is not None):
                data = Binary.bytes(data)
                self.wsgi_write(data)
            #
        except Exception: self.active = False
    #
#
