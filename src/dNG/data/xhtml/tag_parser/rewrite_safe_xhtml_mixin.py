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

from dNG.data.text.tag_parser.rewrite_mixin import RewriteMixin
from dNG.data.xhtml.formatting import Formatting

class RewriteSafeXhtmlMixin(RewriteMixin):
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

    def render_rewrite_safe_xhtml(self, source, key):
        """
Renders the content for safe (escaped) XHTML output.

:param source: Source for rewrite
:param key: Key in source for rewrite

:return: (str) Rendered XHTML content
:since:  v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render_rewrite_safe_xhtml({1})- (#echo(__LINE__)#)", self, key, context = "pas_tag_parser")
        return Formatting.escape(self.render_rewrite(source, key))
    #
#
