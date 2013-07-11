# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.module.blocks.output.menu.Service
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

from dNG.data.xml_parser import XmlParser
from dNG.pas.data.settings import Settings
from dNG.pas.data.http.url import Url
from dNG.pas.data.xhtml.formatting import Formatting as XHtmlFormatting
from dNG.pas.module.blocks.abstract_block import AbstractBlock

class Service(AbstractBlock):
#
	"""
The "Service" class implements a service menu view.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def execute_render_primary(self):
	#
		"""
Action for "render_primary"

:since: v0.1.01
		"""

		rendered_links = self._get_rendered_links()
		if (len(rendered_links) > 0): self.set_action_result("<nav class='pageservicemenu pageservicemenu_p ui-corner-all'><ul><li>{0}</li></ul></nav>".format("</li>\n<li>".join(rendered_links)))
	#

	def execute_render_secondary(self):
	#
		"""
Action for "render_secondary"

:since: v0.1.01
		"""

		rendered_links = self._get_rendered_links(False)
		if (len(rendered_links) > 0): self.set_action_result("<nav class='pageservicemenu pageservicemenu_s ui-corner-all'><ul><li>{0}</li></ul></nav>".format("</li>\n<li>".join(rendered_links)))
	#

	def _get_rendered_links(self, include_image = True):
	#
		"""
Returns a list of rendered links for the service menu.

:return: (list) Links for the service menu
:since:  v0.1.01
		"""

		_return = [ ]

		links = Url.store_get("servicemenu")
		for link in links: _return.append(self._render_link(link, include_image))

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
			url = Url().build_url(data['type'], data['parameters'])
			xml_parser = XmlParser()

			_return = xml_parser.dict2xml_item_encoder({ "tag": "a", "attributes": { "href": url } }, False)
			if (include_image and "image" in data): _return += "{0} ".format(xml_parser.dict2xml_item_encoder({ "tag": "img", "attributes": { "src": "{0}/themes/{1}/{2}.png".format(Settings.get("http_path_mmedia_versioned"), self.response.get_theme(), data['image']) }, "alt": data['title'], "title": data['image'] }, strict_standard = False))
			_return += "{0} </a>".format(XHtmlFormatting.escape(data['title']))
		#

		return _return
	#
#

##j## EOF