# -*- coding: utf-8 -*-
##j## BOF

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

from dNG.pas.data.cache.file_content import FileContent
from dNG.pas.data.settings import Settings
from dNG.pas.data.http.translatable_error import TranslatableError
from dNG.pas.data.text.input_filter import InputFilter
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.xhtml.form_tags import FormTags
from dNG.pas.data.xhtml.link import Link
from .module import Module

class Contentfile(Module):
#
	"""
Service for "s=contentfile"

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def execute_index(self):
	#
		"""
Action for "index"

:since: v0.1.00
		"""

		self.execute_view()
	#

	def execute_view(self):
	#
		"""
Action for "view"

:since: v0.1.00
		"""

		cid = InputFilter.filter_file_path(self.request.get_dsd("cid", ""))

		source_iline = InputFilter.filter_control_chars(self.request.get_dsd("source", "")).strip()

		L10n.init("pas_http_core_contentfile")

		Settings.read_file("{0}/settings/pas_http_contentfiles.json".format(Settings.get("path_data")))

		contentfiles = Settings.get("pas_http_contentfiles_list", { })
		if (type(contentfiles) != dict): raise TranslatableError("pas_http_core_contentfile_cid_invalid", 404)

		if (source_iline != ""):
		#
			if (self.response.is_supported("html_css_files")): self.response.add_theme_css_file("mini_default_sprite.min.css")

			Link.set_store("servicemenu",
			               Link.TYPE_RELATIVE,
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
		if (file_content == None): raise TranslatableError("pas_http_core_contentfile_cid_invalid", 404)

		if (path.splitext(contentfiles[cid]['filepath'])[1].lower() == ".ftg"): file_content = FormTags.render(file_content)

		content = { "title": contentfiles[cid]['title'],
		            "content": file_content
		          }

		self.response.init()
		self.response.set_title(contentfiles[cid]['title'])
		self.response.add_oset_content("core.simple_content", content)
	#
#

##j## EOF