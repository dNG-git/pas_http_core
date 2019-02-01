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

from os import path
import re

from dNG.controller.abstract_http_response import AbstractHttpResponse
from dNG.data.mime_type import MimeType
from dNG.data.streamer.abstract import Abstract as AbstractStreamer
from dNG.data.translatable_exception import TranslatableException

from .translatable_exception import TranslatableException as TranslatableHttpException

class Streaming(object):
    """
HTTP streaming returns data on demand for output.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    @staticmethod
    def handle(request, streamer, response):
        """
Uses the given streamer if all prerequisites are met.

:since: v1.0.0
        """

        if (not isinstance(streamer, AbstractStreamer)): raise TranslatableException("pas_http_core_400")
        if (not isinstance(response, AbstractHttpResponse)): raise TranslatableException("pas_http_core_500")

        if (not streamer.is_resource_valid
            or response.get_header("Content-Type") is None
           ): raise TranslatableException("pas_http_core_500")

        if (response.get_header("Accept-Ranges") is None): response.set_header("Accept-Ranges", "bytes")
        if (response.get_header("X-Content-Type-Options") is None): response.set_header("X-Content-Type-Options", "nosniff")

        is_content_length_set = False
        is_valid = True

        if (is_valid and request.get_header('range') is not None):
            is_valid = False
            streamer_size = streamer.size
            re_result = re.match("^bytes(.*)=(.*)-(.*)$", request.get_header('range'), re.I)

            if (re_result is not None):
                range_start = re.sub("(\\D+)", "", re_result.group(2))
                range_end = re.sub("(\\D+)", "", re_result.group(3))

                if (range_start != ""): range_start = int(range_start)

                if (range_end != ""):
                    range_end = int(range_end)
                    if (range_start >= 0 and range_start <= range_end and range_end < streamer_size): is_valid = True
                elif (range_start >= 0 and range_start < streamer_size):
                    is_valid = True
                    range_end = streamer_size - 1
                #

                if (is_valid):
                    response.set_header("HTTP", "HTTP/2.0 206 Partial Content", True)
                    response.set_header("Content-Length", 1 + (range_end - range_start))
                    response.set_header("Content-Range", "bytes {0:d}-{1:d}/{2:d}".format(range_start, range_end, streamer_size))

                    is_content_length_set = True
                    is_valid = streamer.set_range(range_start, range_end)
                #
            #
        elif (streamer.is_supported("seeking")): streamer.seek(0)

        if (not is_valid): raise TranslatableHttpException("pas_http_core_400", 400)
        if (not is_content_length_set): response.set_header("Content-Length", streamer.size)
        response.streamer = streamer
    #

    @staticmethod
    def handle_url(request, streamer, url, response):
        """
Uses the given streamer and URL if all prerequisites are met.

:since: v1.0.0
        """

        if (not isinstance(streamer, AbstractStreamer)): raise TranslatableException("pas_http_core_400")
        if (not isinstance(response, AbstractHttpResponse)): raise TranslatableException("pas_http_core_500")

        if (streamer is None): response.set_header("HTTP", "HTTP/2.0 501 Not Implemented", True)
        elif (streamer.open_url(url)):
            if (response.get_header("Content-Type") is None):
                url_ext = path.splitext(url)[1]
                mimetype_definition = MimeType.get_instance().get(url_ext[1:])

                mimetype = (mimetype_definition['type']
                            if (mimetype_definition is not None) else
                            "application/octet-stream"
                           )

                response.set_header("Content-Type", mimetype)
            #

            Streaming.handle(request, streamer, response)
        else: response.set_header("HTTP", "HTTP/2.0 404 Not Found", True)
    #
#
