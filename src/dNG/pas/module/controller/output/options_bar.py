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

from dNG.data.xml_parser import XmlParser
from dNG.pas.module.controller.abstract_http import AbstractHttp as AbstractHttpController
from .options_block_mixin import OptionsBlockMixin

class OptionsBar(OptionsBlockMixin, AbstractHttpController):
#
	"""
An "OptionsBar" contains of several options formatted with title and
optional image.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def execute_render(self, _id = None):
	#
		"""
Renders an options bar.

:since: v0.1.01
		"""

		self.set_action_result(self._render_options_bar_links())
	#

	def _get_rendered_options_bar_links(self, links):
	#
		"""
Returns a list of rendered links for the options bar.

:return: (list) Links for the options bar
:since:  v0.1.01
		"""

		_return = [ ]

		if (isinstance(links, list)):
		#
			for link in links: _return.append(self.render_options_block_link(link))
		#

		return _return
	#

	def _render_options_bar_links(self, _id = None):
	#
		"""
Returns rendered XHTML for the options bar.

:return: (str) Options bar XHTML
:since:  v0.1.01
		"""

		_return = ""

		rendered_links = self._get_rendered_options_bar_links(self.context.get("entries"))

		if (len(rendered_links) > 0):
		#
			nav_attributes = { "tag": "nav",
			                   "attributes": { "class": "pageoptionsbar" }
			                 }

			if (_id is not None): nav_attributes['attributes']['id'] = _id

			_return = "{0}<ul><li>{1}</li></ul></nav>".format(XmlParser().dict_to_xml_item_encoder(nav_attributes, False),
			                                                  "</li><li>".join(rendered_links)
			                                                 )
		#

		return _return
	#
#

##j## EOF