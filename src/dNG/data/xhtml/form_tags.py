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

from dNG.data.text.form_tags_sanitizer import FormTagsSanitizer

from .form_tags_encoder import FormTagsEncoder
from .form_tags_renderer import FormTagsRenderer

class FormTags(object):
    """
The static methods of this XHTML FormTags class are used for default
rendering purposes within an "article" tag or similar block level element.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    @staticmethod
    def encode(content):
        """
Encode XHTML FormTags and some typical (X)HTML statements.

:param content: Content containing XHTML FormTags or (X)HTML statements

:return: (str) FormTags encoded data
:since:  v1.0.0
        """

        encoder = FormTagsEncoder()
        return encoder.process(content)
    #

    @staticmethod
    def render(content, block_encoding_supported = True, main_id = None):
        """
Render FormTags as XHTML output and set given restrictions.

:param content: FormTags encoded data
:param block_encoding_supported: Do show block level encoded elements.
:param main_id: DataLinker MainID for tag based links between pages

:return: (str) Rendered content
:since:  v1.0.0
        """

        renderer = FormTagsRenderer()
        renderer.set_xhtml_title_top_level(2)
        if (not block_encoding_supported): renderer.set_blocks_supported(block_encoding_supported)
        if (main_id is not None): renderer.set_datalinker_main_id(main_id)

        return renderer.render(content)
    #

    @staticmethod
    def sanitize(content):
        """
Removes all FormTags from the given content

:param content: FormTags encoded data

:return: (str) Sanitized content
:since:  v1.0.0
        """

        sanitizer = FormTagsSanitizer()
        return sanitizer.process(content)
    #
#
