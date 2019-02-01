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
from dNG.data.text.tag_parser.source_value_mixin import SourceValueMixin
from dNG.data.xhtml.form_tags import FormTags

class RewriteFormTagsXhtmlMixin(SourceValueMixin):
    """
This tag parser mixin provides support for rewrite statements to generate
safe XHTML compliant output.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def render_rewrite_form_tags_xhtml(self, source, key):
        """
Renders the FormTags content for XHTML output.

:param source: Source for rewrite
:param key: Key in source for rewrite

:return: (str) Rendered XHTML content
:since:  v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render_rewrite_formtags_xhtml({1})- (#echo(__LINE__)#)", self, key, context = "pas_tag_parser")

        content = None
        data = self.get_source_value(source, key)
        main_id = None

        if (not isinstance(data, dict)): content = Binary.str(data)
        elif ("content" in data):
            content = Binary.str(data['content'])
            if ("main_id" in data): main_id = data['main_id']
        #

        _return = (FormTags.render(content, main_id = main_id)
                   if (type(content) is str) else
                   ""
                  )

        return _return
    #
#
