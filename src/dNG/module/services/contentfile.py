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

from os import path
import re

from dNG.data.cache.file_content import FileContent
from dNG.data.http.translatable_error import TranslatableError
from dNG.data.settings import Settings
from dNG.data.text.input_filter import InputFilter
from dNG.data.text.l10n import L10n
from dNG.data.xhtml.form_tags import FormTags
from dNG.data.xhtml.link import Link
from dNG.module.http import Http as HttpModule

class Contentfile(HttpModule):
    """
Service for "/services/contentfile"

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def execute_index(self):
        """
Action for "index"

:since: v1.0.0
        """

        self.get_view()
    #

    def get_view(self):
        """
Action for "view"

:since: v1.0.0
        """

        cid = InputFilter.filter_file_path(self.request.get_parameter("cid", ""))

        source_iline = InputFilter.filter_control_chars(self.request.get_parameter("source", "")).strip()

        L10n.init("pas_http_core_contentfile")

        Settings.read_file("{0}/settings/pas_http_contentfiles.json".format(Settings.get("path_data")))

        contentfiles = Settings.get("pas_http_contentfiles_list", { })
        if (type(contentfiles) is not dict): raise TranslatableError("pas_http_core_contentfile_cid_invalid", 404)

        if (source_iline != ""):
            if (self.response.is_supported("html_css_files")): self.response.add_theme_css_file("mini_default_sprite.css")

            Link.set_store("servicemenu",
                           Link.TYPE_RELATIVE_URL,
                           L10n.get("core_back"),
                           { "__query__": re.sub("\\_\\_\\w+\\_\\_", "", source_iline) },
                           icon = "mini-default-back",
                           priority = 7
                          )
        #

        if (cid not in contentfiles
            or "title" not in contentfiles[cid]
            or "filepath" not in contentfiles[cid]
           ): raise TranslatableError("pas_http_core_contentfile_cid_invalid", 404)

        file_content = FileContent.read(contentfiles[cid]['filepath'])
        if (file_content is None): raise TranslatableError("pas_http_core_contentfile_cid_invalid", 404)

        if (path.splitext(contentfiles[cid]['filepath'])[1].lower() == ".ftg"): file_content = FormTags.render(file_content)

        content = { "title": contentfiles[cid]['title'],
                    "content": file_content
                  }

        self.response.init()
        self.response.page_title = contentfiles[cid]['title']

        self.response.add_oset_content("core.simple_content", content)
    #
#
