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

import os
import re
import traceback

from dNG.data.http.streaming import Streaming
from dNG.data.http.translatable_error import TranslatableError
from dNG.data.rfc.basics import Basics as RfcBasics
from dNG.data.settings import Settings
from dNG.data.streamer.file import File
from dNG.data.text.input_filter import InputFilter
from dNG.data.xhtml.asset_parser import AssetParser
from dNG.module.http import Http as HttpModule
from dNG.vfs.implementation import Implementation

class Cache(HttpModule):
    """
Service for "/services/cache"

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def get_index(self):
        """
Action for "index"

:since: v1.0.0
        """

        dfile_chained = (self.request.get_parameter_chained("dfile")
                         if (self.request.is_supported("parameters_chained")) else
                         None
                        )

        dfile = InputFilter.filter_file_path(self.request.get_parameter("dfile", ""))

        file_path_name = ""

        self.response.set_header("X-Robots-Tag", "noindex")

        if (dfile_chained is not None): file_path_name = dfile_chained
        elif (dfile != ""): file_path_name = "{0}/assets/{1}".format(Settings.get("path_data"), dfile)

        if (file_path_name == ""): raise TranslatableError("pas_http_core_404", 404)

        vfs_object = Implementation.load_vfs_url("file:///{0}".format(file_path_name))

        if (not vfs_object.is_valid):
            raise TranslatableError("pas_http_core_404", 404, "'{0}' not found".format(file_path_name))
        #

        is_last_modified_supported = (Settings.get("pas_http_site_cache_modification_check", True))
        is_modified = True
        last_modified_on_server = 0

        if (is_last_modified_supported
            and (not vfs_object.is_supported("filesystem_path_name"))
           ): raise TranslatableError("pas_http_core_500", 500)

        if (is_last_modified_supported and self.request.get_header("If-Modified-Since") is not None):
            last_modified_on_client = RfcBasics.get_rfc7231_timestamp(self.request.get_header("If-Modified-Since").split(";")[0])

            if (last_modified_on_client > -1):
                last_modified_on_server = int(os.stat(vfs_object.filesystem_path_name).st_mtime)

                if (last_modified_on_server <= last_modified_on_client):
                    is_modified = False
                    self.response.content_uncachable = False
                    self.response.send_only_headers = True

                    self.response.init(True)
                    self.response.set_header("HTTP", "HTTP/2.0 304 Not Modified", True)
                    self.response.set_expires_relative(+63072000)

                    self.response.last_modified = last_modified_on_server
                    self.response.raw_data = ""
                #
            #
        #

        if (is_modified):
            re_tsc_result = re.search("\\.tsc\\.(min\\.)?(css|js|svg)$", file_path_name, re.I)

            self.response.content_uncachable = (re_tsc_result is not None)

            self.response.init(True)

            if (is_last_modified_supported):
                if (last_modified_on_server < 1):
                    last_modified_on_server = int(os.stat(vfs_object.filesystem_path_name).st_mtime)
                #

                self.response.last_modified = last_modified_on_server
            #

            if (re_tsc_result is not None):
                file_extension = re_tsc_result.group(2)

                if (file_extension == "css"): self.response.set_header("Content-Type", "text/css")
                elif (file_extension == "js"): self.response.set_header("Content-Type", "text/javascript")
                elif (file_extension == "svg"): self.response.set_header("Content-Type", "text/svg+xml")

                parser = AssetParser()

                self.response.raw_data = parser.render(file_path_name)
            else:
                self.response.set_expires_relative(+63072000)

                Streaming.handle_url(self.request, File(), "file:///{0}".format(file_path_name), self.response)
            #
        #
    #
#
