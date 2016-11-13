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
from dNG.module.controller.abstract_http import AbstractHttp as AbstractHttpController
from dNG.runtime.value_exception import ValueException

from .service_list_mixin import ServiceListMixin

class ServiceList(ServiceListMixin, AbstractHttpController):
    """
"ServiceList" is a navigation element providing links to other services.

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

        if ("css_sprite" in self.context): self._add_options_block_css_sprite(self.context['css_sprite'])

        if ("file" in self.context): self.set_action_result(self.render_service_list_file(self.context['file']))
        elif (isinstance(self.context.get("entries"), list)): self.set_action_result(self.render_service_list_entries(self.context['entries']))
        else: raise ValueException("Missing service list to render")
    #
#
