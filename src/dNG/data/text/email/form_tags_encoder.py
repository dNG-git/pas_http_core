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

from dNG.data.text.form_tags_encoder import FormTagsEncoder as _FormTagsEncoder

class FormTagsEncoder(_FormTagsEncoder):
    """
Encodes data as well as some typical structured e-mail text elements and
validates FormTags.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def process(self, content):
        """
Process the given content.

:param content: Raw content

:return: (str) FormTags encoded content
:since:  v0.2.00
        """

        content = re.sub("/(.+?)/", "[i]\\1[/i]", content)
        content = re.sub("\\*(.+?)\\*", "[b]\\1[/b]", content)
        content = re.sub("-(.+?)-", "[s]\\1[/s]", content)
        content = re.sub("\\_(.+?)\\_", "[u]\\1[/u]", content)

        return _FormTagsEncoder.process(content)
    #
#
