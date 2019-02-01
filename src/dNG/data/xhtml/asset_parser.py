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

import re

from dNG.controller.abstract_response import AbstractResponse
from dNG.data.file import File
from dNG.data.text.l10n import L10n
from dNG.data.text.tag_parser.abstract import Abstract as AbstractTagParser
from dNG.data.text.tag_parser.rewrite_mixin import RewriteMixin
from dNG.runtime.io_exception import IOException
from dNG.runtime.named_loader import NamedLoader

class AssetParser(RewriteMixin, AbstractTagParser):
    """
Parses files in the "assets" directory to set configured values and replace
language placeholders.

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
Constructor __init__(AssetParser)

:since: v1.0.0
        """

        AbstractTagParser.__init__(self)

        self.cache_instance = NamedLoader.get_singleton("dNG.data.cache.Content", False)
        self._log_handler = NamedLoader.get_singleton("dNG.data.logging.LogHandler", False)
    #

    def _change_match(self, tag_definition, data, tag_position, data_position, tag_end_position):
        """
Change data according to the matched tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v1.0.0
        """

        _return = data[:tag_position]

        data_closed = data[self._find_tag_end_position(data, tag_end_position):]

        if (tag_definition['tag'] == "rewrite"):
            source = re.match("^\\[rewrite:(\\w+)\\]", data[tag_position:data_position]).group(1)
            key = data[data_position:tag_end_position]

            if (source == "l10n"): _return += self.render_rewrite(L10n.get_dict(), key)
            else:
                runtime_settings_dict = AbstractResponse.get_instance().runtime_settings
                _return += self.render_rewrite(runtime_settings_dict, key)
            #
        #

        _return += data_closed

        return _return
    #

    def _check_match(self, data):
        """
Check if a possible tag match is a false positive.

:param data: Data starting with the possible tag

:return: (dict) Matched tag definition; None if false positive
:since:  v1.0.0
        """

        _return = None

        i = 0
        tags = [ "rewrite" ]
        tags_length = len(tags)

        while (_return is None and i < tags_length):
            tag = tags[i]
            data_match = data[1:1 + len(tag)]

            if (data_match == tag and data_match == "rewrite"):
                re_result = re.match("^\\[rewrite:(\\w+)\\]", data)
                if (re_result is not None and re_result.group(1) in ( "l10n", "settings" )): _return = { "tag": "rewrite", "tag_end": "[/rewrite]" }
            #

            i += 1
        #

        return _return
    #

    def render(self, file_path_name):
        """
Renders content ready for output from the given "asset" file.

:param file_path_name: Asset file path and name

:return: (str) Rendered "asset" file
:since:  v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render({1})- (#echo(__LINE__)#)", self, file_path_name, context = "pas_http_core")

        file_obj = File()
        if (not file_obj.open(file_path_name, True, "r")): raise IOException("Failed to open asset file '{0}'".format(file_path_name))

        file_content = file_obj.read()
        file_obj.close()

        if (file_content is None): raise IOException("Failed to read asset file '{0}'".format(file_path_name))

        return self._parse(file_content)
    #
#
