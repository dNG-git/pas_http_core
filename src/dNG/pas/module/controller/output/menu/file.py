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
from dNG.pas.data.xhtml.link import Link
from dNG.pas.module.controller.abstract_http import AbstractHttp as AbstractHttpController
from dNG.pas.module.controller.output.filter_links_mixin import FilterLinksMixin
from dNG.pas.module.controller.output.options_block_mixin import OptionsBlockMixin

class File(FilterLinksMixin, OptionsBlockMixin, AbstractHttpController):
#
	"""
The "Main" class implements a main menu view.

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

		if (self.context is not None and "file" in self.context): rendered_links = self._get_rendered_links(self.context['file'])
		else: rendered_links = self._get_rendered_links()

		if (len(rendered_links) > 0): self.set_action_result("<nav class='pagemainmenu'><ul><li>{0}</li></ul></nav>".format("</li><li>".join(rendered_links)))
	#

	def _get_rendered_links(self, file_path_name = None, include_image = True):
	#
		"""
Returns a list of rendered links for the service menu.

:return: (list) Links for the service menu
:since:  v0.1.01
		"""

		_return = [ ]

		if (file_path_name is None): links = Link.get_store("mainmenu")
		else:
		#
			links = None

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
		#

		if (links is not None):
		#
			links = self._filter_links(links)
			for link in links: _return.append(self.render_options_block_link(link, include_image))
		#

		return _return
	#
#

##j## EOF