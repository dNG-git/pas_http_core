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

from copy import copy
from os import path
import os

from dNG.data.json_parser import JsonParser
from dNG.data.xml_parser import XmlParser
from dNG.pas.data.settings import Settings
from dNG.pas.data.logging.log_line import LogLine
from dNG.pas.data.text.url import Url
from dNG.pas.data.xhtml.formatting import Formatting as XHtmlFormatting
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.module.blocks.abstract_block import AbstractBlock
import dNG.data.file

class File(AbstractBlock):
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

		if (self.context != None and "file" in self.context): rendered_links = self.get_rendered_links(self.context['file'])
		else: rendered_links = self.get_rendered_links()

		if (len(rendered_links) > 0): self.set_action_result("<nav class='pagemainmenu ui-corner-all'><ul><li>{0}</li></ul></nav>".format("</li>\n<li>".join(rendered_links)))
	#

	def filter_links(self, links):
	#
		"""
Filters links based on required permissions.

:access: protected
:return: (str) Link (X)HTML
:since:  v0.1.01
		"""

		var_return = (links.copy() if (hasattr(links, "copy")) else copy(links))

		return var_return
	#

	def get_rendered_links(self, file_pathname = None, include_image = True):
	#
		"""
Returns a list of rendered links for the service menu.

:access: protected
:return: (list) Links for the service menu
:since:  v0.1.01
		"""

		var_return = [ ]

		if (file_pathname == None): links = Url.store_get("mainmenu")
		else:
		#
			is_valid = True
			links = None

			if("[lang]" in file_pathname):
			#
				expanded_file_pathname = file_pathname.replace("[lang]", self.request.get_lang())
				if (not os.access(path.normpath("{0}/{1}".format(Settings.get("path_base"), expanded_file_pathname)), os.R_OK)): expanded_file_pathname = file_pathname.replace("[lang]", Settings.get("core_lang"))
				file_pathname = expanded_file_pathname
			#

			cache_instance = NamedLoader.get_singleton("dNG.pas.data.Cache", False)
			file_content = (None if (cache_instance == None) else cache_instance.get_file(file_pathname))

			if (file_content == None):
			#
				file_object = dNG.data.file.File()

				if (file_object.open(file_pathname, True, "r")):
				#
					file_content = file_object.read()
					file_object.close()

					file_content = file_content.replace("\r", "")
					if (cache_instance != None): cache_instance.set_file(file_pathname, file_content)
				#
				else: LogLine.info("{0} not found".format(file_pathname))
			#

			if (file_content != None):
			#
				json_parser = JsonParser()
				data = json_parser.json2data(file_content)

				if (data == None or type(data) != list): is_valid = False
				else: links = data
			#

			if (not is_valid): LogLine.warning("{0} is not a valid JSON encoded menu file".format(file_pathname))
		#

		if (links != None):
		#
			links = self.filter_links(links)
			for link in links: var_return.append(self.render_link(link, include_image))
		#

		return var_return
	#

	def render_link(self, data, include_image = True):
	#
		"""
Renders a link.

:access: protected
:return: (str) Link (X)HTML
:since:  v0.1.01
		"""

		var_return = ""

		if ("title" in data and "type" in data and "parameters" in data):
		#
			xml_parser = XmlParser()
			url = Url().build_url(data['type'], data['parameters'])

			var_return = xml_parser.dict2xml_item_encoder({ "tag": "a", "attributes": { "href": url } }, False)
			if (include_image and "image" in data): var_return += "{0} ".format(xml_parser.dict2xml_item_encoder({ "tag": "img", "attributes": { "src": "{0}/themes/{1}/{2}.png".format(Settings.get("http_path_mmedia_versioned"), self.response.get_theme(), data['image']) }, "alt": data['title'], "title": data['image'] }, strict_standard = False))
			var_return += "{0} </a>".format(XHtmlFormatting.escape(data['title']))
		#

		return var_return
	#
#

##j## EOF