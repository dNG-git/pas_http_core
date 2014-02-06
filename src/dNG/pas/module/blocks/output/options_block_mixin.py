# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.module.blocks.output.OptionsBlockMixin
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
from dNG.pas.data.text.md5 import Md5
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.xhtml.form_tags import FormTags
from dNG.pas.data.xhtml.formatting import Formatting as XHtmlFormatting
from dNG.pas.data.xhtml.link import Link

class OptionsBlockMixin(object):
#
	"""
An "OptionBlock" contains of several options formatted with title,
description and optional image.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def options_block_render_link(self, data, include_image = True):
	#
		"""
Renders a link.

:return: (str) Link (X)HTML
:since:  v0.1.01
		"""

		_return = ""

		if ("title" in data and "type" in data and "parameters" in data):
		#
			_type = (data['type'] if (type(data['type']) == int) else Link.get_type(data['type']))

			url = Link().build_url(_type, data['parameters'])
			xml_parser = XmlParser()

			is_js_required = (_type & Link.TYPE_JS_REQUIRED == Link.TYPE_JS_REQUIRED)
			link_id = None

			if (is_js_required):
			#
				link_id = "pas_id_{0}".format(Md5.hash("pas_http_core_url_{0}_{1:d}_{2:d}".format(url, id(data), id(self))))
				_return = xml_parser.dict2xml_item_encoder({ "tag": "span", "attributes": { "data-href": url, "id": link_id, "title": L10n.get("pas_http_core_js_required"), "class": "pageurl_requirements_unsupported" } }, False)
			#
			else: _return = xml_parser.dict2xml_item_encoder({ "tag": "a", "attributes": { "href": url } }, False)

			l10n_title_id = "title_{0}".format(self.request.get_lang())
			title = (data[l10n_title_id] if (l10n_title_id in data) else data['title'])

			if (include_image and "image" in data): _return += "{0}".format(xml_parser.dict2xml_item_encoder({ "tag": "img", "attributes": {
				"src": "{0}/themes/{1}/{2}.png".format(Settings.get("http_path_mmedia_versioned"), self.response.get_theme(), data['image']) }, "alt": title
			}, strict_standard = False))

			_return += "{0}".format(XHtmlFormatting.escape(title))

			l10n_description_id = "description_{0}".format(self.request.get_lang())
			description = (data[l10n_description_id] if (l10n_description_id in data) else None)
			if (description == None and "description" in data): description = data['description']
			if (description != None): _return += "<br />\n{0}".format(FormTags.render(description))

			if (is_js_required):
			#
				_return += (
"""</span><script type="text/javascript"><![CDATA[
require([ "djs/uiX.min" ], function(uiX) {{
	uiX.show_link_if_js_supported("{0}");
}});
]]></script>""".format(link_id)
				)
			#
			else: _return += "</a>"
		#

		return _return
	#
#

##j## EOF