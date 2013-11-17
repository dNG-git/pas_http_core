# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.module.blocks.output.menu.File
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;http;core

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasHttpCoreVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from os import path
import os

from dNG.data.xml_parser import XmlParser
from dNG.pas.data.cached_json_file import CachedJsonFile
from dNG.pas.data.settings import Settings
from dNG.pas.data.http.url import Url
from dNG.pas.data.xhtml.formatting import Formatting as XHtmlFormatting
from dNG.pas.module.blocks.abstract_block import AbstractBlock
from dNG.pas.module.blocks.output.filter_links_mixin import FilterLinksMixin

class File(AbstractBlock, FilterLinksMixin):
#
	"""
The "Main" class implements a main menu view.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def execute_render(self):
	#
		"""
Action for "render"

:since: v0.1.00
		"""

		if (self.context != None and "file" in self.context): rendered_links = self._get_rendered_links(self.context['file'])
		else: rendered_links = self._get_rendered_links()

		if (len(rendered_links) > 0): self.set_action_result("<nav class='pagemainmenu ui-corner-all'><ul><li>{0}</li></ul></nav>".format("</li>\n<li>".join(rendered_links)))
	#

	def _get_rendered_links(self, file_pathname = None, include_image = True):
	#
		"""
Returns a list of rendered links for the service menu.

:return: (list) Links for the service menu
:since:  v0.1.01
		"""

		_return = [ ]

		if (file_pathname == None): links = Url.store_get("mainmenu")
		else:
		#
			links = None

			if("[lang]" in file_pathname):
			#
				expanded_file_pathname = file_pathname.replace("[lang]", self.request.get_lang())
				if (not os.access(path.normpath("{0}/{1}".format(Settings.get("path_base"), expanded_file_pathname)), os.R_OK)): expanded_file_pathname = file_pathname.replace("[lang]", Settings.get("core_lang"))
				file_pathname = expanded_file_pathname
			#

			json_data = CachedJsonFile.read(file_pathname)
			if (type(json_data) == list): links = json_data
		#

		if (links != None):
		#
			links = self._filter_links(links)
			for link in links: _return.append(self._render_link(link, include_image))
		#

		return _return
	#

	def _render_link(self, data, include_image = True):
	#
		"""
Renders a link.

:return: (str) Link (X)HTML
:since:  v0.1.01
		"""

		_return = ""

		if ("title" in data and "type" in data and "parameters" in data):
		#
			l10n_title_id = "title_{0}".format(self.request.get_lang())
			title = (data[l10n_title_id] if (l10n_title_id in data) else data['title'])
			url = Url().build_url(data['type'], data['parameters'])
			xml_parser = XmlParser()

			_return = xml_parser.dict2xml_item_encoder({ "tag": "a", "attributes": { "href": url } }, False)
			if (include_image and "image" in data): _return += "{0} ".format(xml_parser.dict2xml_item_encoder({ "tag": "img", "attributes": { "src": "{0}/themes/{1}/{2}.png".format(Settings.get("http_path_mmedia_versioned"), self.response.get_theme(), data['image']) }, "alt": title, "title": data['image'] }, strict_standard = False))
			_return += "{0}</a>".format(XHtmlFormatting.escape(title))
		#

		return _return
	#
#

##j## EOF