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

from .form_tags_renderer import FormTagsRenderer

class FormTagsSanitizer(FormTagsRenderer):
    """
Sanitizes FormTags data.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    _change_match_center = FormTagsRenderer._change_plain_content
    """
Change data according to the "center" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v1.0.0
    """

    def _change_match_code(self, data, tag_position, data_position, tag_end_position):
        """
Change data according to the "code" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v1.0.0
        """

        _return = data[data_position:tag_end_position]

        if (len(_return) > 0 and "[" in _return):
            self.null_byte_markup = True

            _return = _return.replace("[", "\x00#91;")
            _return = _return.replace("]", "\x00#93;")
        #

        return _return
    #

    _change_match_highlight = FormTagsRenderer._change_plain_content
    """
Change data according to the "highlight" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v1.0.0
    """

    _change_match_justify = FormTagsRenderer._change_plain_content
    """
Change data according to the "justify" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v1.0.0
    """

    _change_match_right = FormTagsRenderer._change_plain_content
    """
Change data according to the "right" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v1.0.0
    """

    _change_match_title = FormTagsRenderer._change_plain_content
    """
Change data according to the "title" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v1.0.0
    """

    def process(self, content):
        """
Process the given content.

:param content: Raw content

:return: (str) FormTags encoded content
:since:  v1.0.0
        """

        return self.render(content)
    #
#
