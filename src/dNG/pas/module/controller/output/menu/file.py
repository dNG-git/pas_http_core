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
import os

from dNG.pas.data.settings import Settings
from dNG.pas.data.cache.json_file_content import JsonFileContent
from dNG.pas.data.http.translatable_error import TranslatableError
from dNG.pas.module.controller.abstract_http import AbstractHttp as AbstractHttpController
from dNG.pas.module.controller.output.filter_links_mixin import FilterLinksMixin
from dNG.pas.module.controller.output.options_block_mixin import OptionsBlockMixin
from dNG.pas.runtime.value_exception import ValueException

class File(FilterLinksMixin, OptionsBlockMixin, AbstractHttpController):
#
	"""
The "File" menu class implements a main menu for the file given.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def execute_render(self):
	#
		"""
Action for "render"

:since: v0.1.00
		"""

		if (self._is_primary_action()): raise TranslatableError("core_access_denied", 403)

		if ("file" not in self.context): raise ValueException("Menu file required is not defined")

		rendered_links = self._get_rendered_links(self.context['file'])
		if (len(rendered_links) > 0): self.set_action_result("<nav class='pagemainmenu'><ul><li>{0}</li></ul></nav>".format("</li><li>".join(rendered_links)))
	#

	def _get_rendered_links(self, file_path_name, include_image = True):
	#
		"""
Returns a list of rendered links for the main menu.

:return: (list) Links for the main menu
:since:  v0.1.01
		"""

		_return = [ ]

		links = [ ]

		if ("__lang__" in file_path_name):
		#
			expanded_file_path_name = file_path_name.replace("__lang__", self.request.get_lang())

			if (not os.access(path.join(Settings.get("path_base"), expanded_file_path_name), os.R_OK)):
			#
				expanded_file_path_name = file_path_name.replace("__lang__", Settings.get("core_lang"))
			#

			file_path_name = expanded_file_path_name
		#
		else: file_path_name = path.join(Settings.get("path_base"), file_path_name)

		json_data = JsonFileContent.read(file_path_name)
		if (type(json_data) is list): links = json_data

		for link in self._filter_links(links): _return.append(self.render_options_block_link(link, include_image))

		return _return
	#
#

##j## EOF