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

from dNG.data.rfc.basics import Basics as RfcBasics
from dNG.data.text.l10n import L10n
from dNG.data.text.tag_parser.rewrite_date_time_mixin import RewriteDateTimeMixin
from dNG.data.xml_parser import XmlParser

class RewriteDateTimeXhtmlMixin(RewriteDateTimeMixin):
    """
This tag parser mixin provides support for rewrite statements to generate
formatted date and time XHTML tagged strings.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def render_rewrite_date_time_xhtml(self, source, key, _type):
        """
Renders a date and time XHTML 5 tag based on the given presentation type.

:param source: Source for rewrite
:param key: Key in source for rewrite
:param _type: Presentation type

:return: (str) Rewritten statement if successful
:since:  v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render_rewrite_date_time_xhtml({1}, {2})- (#echo(__LINE__)#)", self, key, _type, context = "pas_tag_parser")
        _return = L10n.get("core_unknown")

        timestamp = self.get_source_value(source, key)

        if (timestamp is not None):
            time_attributes = { "tag": "time", "attributes": { "datetime": "{0}+00:00".format(RfcBasics.get_iso8601_datetime(timestamp)) } }

            _return = "{0}{1}</time>".format(XmlParser().dict_to_xml_item_encoder(time_attributes, False),
                                             self.render_rewrite_date_time(source, key, _type)
                                            )
        #

        return _return
    #
#
