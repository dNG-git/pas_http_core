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

from .abstract_form_tags import AbstractFormTags

class FormTagsEncoder(AbstractFormTags):
    """
Encodes data and validates FormTags.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def _change_match_box(self, data, tag_position, data_position, tag_end_position):
        """
Change data according to the "box" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v1.0.0
        """

        _return = ""

        tag_params = AbstractFormTags.parse_tag_parameters("box", data, tag_position, data_position)

        re_result = re.match("^(\\d+)$", tag_params.get("width", ""))

        if (re_result is not None):
            value = int(re_result.group(1))

            if (value > 0 and value <= 100): tag_params['width'] = "{0:d}%".format(re_result.group(1))
            else: del(tag_params['width'])

            enclosed_data = data[data_position:tag_end_position]

            if (len(tag_params) > 0):
                tag_params_encoded = ":".join([ "{0}={1}".format(key, value) for ( key, value ) in tag_params.items() ])
                _return = "[box:{0}]{1}[/box]".format(tag_params_encoded, enclosed_data)
            else: _return = enclosed_data
        #

        return _return
    #

    def _change_match_highlight(self, data, tag_position, data_position, tag_end_position):
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

        _return = ""

        tag_params = AbstractFormTags.parse_tag_parameters("highlight", data, tag_position, data_position)

        re_result = re.match("^(\\d+)$", tag_params.get("width", ""))

        if (re_result is not None):
            enclosed_data = data[data_position:tag_end_position]
            value = int(re_result.group(1))

            _return = ("[highlight:width={0:d}%]{1}[/highlight]".format(value, enclosed_data)
                       if (value > 0 and value <= 100) else
                       enclosed_data
                      )
        #

        return _return
    #

    def _change_match_hr(self, data, tag_position, data_position, tag_end_position):
        """
Change data according to the "hr" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v1.0.0
        """

        _return = ""

        re_result = re.match("^\\[hr=(\\d+)\\]", data[tag_position:data_position])

        if (re_result is not None):
            value = int(re_result.group(1))
            if (value > 0 and value <= 100): _return = "[hr={0:d}%]".format(value)
        #

        return _return
    #

    def _change_match_margin(self, data, tag_position, data_position, tag_end_position):
        """
Change data according to the "margin" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v1.0.0
        """

        _return = ""

        re_result = re.match("^\\[margin=(\\d+)\\]", data[tag_position:data_position])

        if (re_result is not None):
            enclosed_data = data[data_position:tag_end_position]
            value = int(re_result.group(1))

            _return = ("[margin={0:d}%]{1}[/margin]".format(value, enclosed_data) if (value > 0 and value <= 100) else enclosed_data)
        #

        return _return
    #

    def _change_match_size(self, data, tag_position, data_position, tag_end_position):
        """
Change data according to the "size" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v1.0.0
        """

        _return = ""

        re_result = re.match("^\\[size=(\\d+)\\]", data[tag_position:data_position])

        if (re_result is not None):
            enclosed_data = data[data_position:tag_end_position]
            value = int(re_result.group(1))

            if (value >= 8 and value <= 80): _return = "[size={0:d}px]{1}[/size]".format(value, enclosed_data)
            elif (value > 0 and value <= 100): _return = "[size={0:d}%]{1}[/size]".format(value, enclosed_data)
            else: _return = enclosed_data
        #

        return _return
    #

    def _check_match_b(self, data):
        """
Check if a possible tag match is a valid "b" tag that needs to be changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return False
    #

    def _check_match_box(self, data):
        """
Check if a possible tag match is a valid "box" tag that needs to be changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        _return = False

        tag_element_end_position = self._find_tag_end_position(data, 4)

        if (tag_element_end_position > 5):
            tag_params = FormTagsEncoder.parse_tag_parameters("box", data, 0, tag_element_end_position)
            _return = ("width" in tag_params and re.match("^\\d+$", tag_params['width']) is not None)
        #

        return _return
    #

    def _check_match_center(self, data):
        """
Check if a possible tag match is a valid "center" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return False
    #

    def _check_match_color(self, data):
        """
Check if a possible tag match is a valid "color" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return False
    #

    def _check_match_code(self, data):
        """
Check if a possible tag match is a valid "code" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return False
    #

    def _check_match_del(self, data):
        """
Check if a possible tag match is a valid "del" tag that needs to be changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return False
    #

    def _check_match_face(self, data):
        """
Check if a possible tag match is a valid "face" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return False
    #

    def _check_match_highlight(self, data):
        """
Check if a possible tag match is a valid "highlight" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        tag_element_end_position = self._find_tag_end_position(data, 10)

        if (tag_element_end_position > 11):
            tag_params = FormTagsEncoder.parse_tag_parameters("highlight", data, 0, tag_element_end_position)
            _return = ("width" in tag_params and re.match("^\\d+$", tag_params['width']) is not None)
        #

        return (re.match("^\\[highlight\\:width=(\\d+)\\]", data) is not None)
    #

    def _check_match_hr(self, data):
        """
Check if a possible tag match is a valid "hr" tag that needs to be changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return (re.match("^\\[hr=(\\d+)\\]", data) is not None)
    #

    def _check_match_i(self, data):
        """
Check if a possible tag match is a valid "i" tag that needs to be changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return False
    #

    def _check_match_img(self, data):
        """
Check if a possible tag match is a valid "img" tag that needs to be changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return False
    #

    def _check_match_justify(self, data):
        """
Check if a possible tag match is a valid "justify" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return False
    #

    def _check_match_left(self, data):
        """
Check if a possible tag match is a valid "left" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return False
    #

    def _check_match_link(self, data):
        """
Check if a possible tag match is a valid "link" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return False
    #

    def _check_match_list(self, data):
        """
Check if a possible tag match is a valid "list" tag that needs to be changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return False
    #

    def _check_match_margin(self, data):
        """
Check if a possible tag match is a valid "margin" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return (re.match("^\\[margin=(\\d+)\\]", data) is not None)
    #

    def _check_match_quote(self, data):
        """
Check if a possible tag match is a valid "quote" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return False
    #

    def _check_match_right(self, data):
        """
Check if a possible tag match is a valid "right" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return False
    #

    def _check_match_s(self, data):
        """
Check if a possible tag match is a valid "s" tag that needs to be changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return False
    #

    def _check_match_size(self, data):
        """
Check if a possible tag match is a valid "size" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return (re.match("^\\[size=(\\d+)\\]", data) is not None)
    #

    def _check_match_title(self, data):
        """
Check if a possible tag match is a valid "title" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return False
    #

    def _check_match_u(self, data):
        """
Check if a possible tag match is a valid "u" tag that needs to be changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return False
    #

    def _check_match_url(self, data):
        """
Check if a possible tag match is a valid "url" tag that needs to be
changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v1.0.0
        """

        return False
    #

    def process(self, content):
        """
Process the given content.

:param content: Raw content

:return: (str) FormTags encoded content
:since:  v1.0.0
        """

        return self._parse(content)
    #
#
