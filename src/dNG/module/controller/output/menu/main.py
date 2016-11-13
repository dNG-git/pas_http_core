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

from dNG.data.http.translatable_error import TranslatableError
from dNG.data.xhtml.link import Link
from dNG.module.controller.abstract_http import AbstractHttp as AbstractHttpController
from dNG.module.controller.output.filter_links_mixin import FilterLinksMixin
from dNG.module.controller.output.options_block_mixin import OptionsBlockMixin

class Main(FilterLinksMixin, OptionsBlockMixin, AbstractHttpController):
    """
The "Main" menu class implements a main menu based on the "mainmenu" link
store.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def execute_render(self):
        """
Action for "render"

:since: v0.2.00
        """

        if (self._is_primary_action()): raise TranslatableError("core_access_denied", 403)

        rendered_links = self._get_rendered_links()
        if (len(rendered_links) > 0): self.set_action_result("<nav class='pagemainmenu'><ul><li>{0}</li></ul></nav>".format("</li><li>".join(rendered_links)))
    #

    def _get_rendered_links(self, include_image = True):
        """
Returns a list of rendered links for the main menu.

:return: (list) Links for the main menu
:since:  v0.2.00
        """

        _return = [ ]

        links = Link.get_store("mainmenu")

        if (links is not None):
            for link in self._filter_links(links): _return.append(self.render_options_block_link(link, include_image))
        #

        return _return
    #
#
