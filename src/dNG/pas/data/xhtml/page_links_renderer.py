# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.xhtml.PageLinksRenderer
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

from math import floor

from dNG.data.xml_parser import XmlParser
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.xhtml.link import Link

class PageLinksRenderer(Link):
#
	"""
The "PageLinksRenderer" should be used for all page link bars used for
navigation.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, parameters, page, pages, _type = None):
	#
		"""
Constructor __init__(PageLinksRenderer)

:since: v0.1.01
		"""

		Link.__init__(self)

		self.dsd_page_key = "page"
		"""
DSD key used for the page value
		"""
		self.first_page_content = "&#0171;"
		"""
Content used for a link to the first page
		"""
		self.hidden_pages_content = "..."
		"""
Content used as replacement for a range of page link hidden
		"""
		self.hide_navigation_links = False
		"""
True to hide the last and next link
		"""
		self.hide_navigation_title = False
		"""
True to hide the last and next link
		"""
		self.last_page_content = "&#0187;"
		"""
Content used for a link to the last page
		"""
		self.max_pages = 11
		"""
Page links shown before collapsing the list of links (...)
		"""
		self.page = page
		"""
Active page
		"""
		self.pages = pages
		"""
Pages available
		"""
		self.parameters = parameters
		"""
Parameters used to render each page link
		"""
		self.separator = " &#8226; "
		"""
Separator between links
		"""
		self.type = (_type if (_type != None) else Link.TYPE_RELATIVE)
		"""
Page link type
		"""
	#

	def render(self):
	#
		"""
Renders the page link navigation bar.

:return: (str) Rendered content
:since:  v0.1.01
		"""

		rendered_prefix = ""
		rendered_suffix = ""

		if (self.pages < (self.max_pages + 2)):
		#
			first_page = 1
			last_page = self.pages
		#
		elif (self.page < (self.max_pages - 2)):
		#
			rendered_suffix = "{0}{1}".format(self.separator, self.hidden_pages_content)
			if (not self.hide_navigation_links): rendered_suffix += " {0}".format(self._render_page_link(self.pages, self.last_page_content))

			first_page = 1
			last_page = self.max_pages
		#
		elif (((self.page + self.max_pages) - 3) > self.pages):
		#
			if (not self.hide_navigation_links): rendered_prefix += "{0} ".format(self._render_page_link(1, self.first_page_content))
			rendered_prefix += "{0}{1}".format(self.hidden_pages_content, self.separator)

			first_page = ((self.pages - self.max_pages) + 3)
			last_page = self.pages
		#
		else:
		#
			if (not self.hide_navigation_links): rendered_prefix += "{0} ".format(self._render_page_link(1, self.first_page_content))
			rendered_prefix += "{0}{1}".format(self.hidden_pages_content, self.separator)

			rendered_suffix += "{0}{1}".format(self.separator, self.hidden_pages_content)
			if (not self.hide_navigation_links): rendered_suffix += " {0}".format(self._render_page_link(self.pages, self.last_page_content))

			first_page = (self.pages - (self.pages - self.page) - (floor(self.max_pages / 2)) + 2)
			last_page = (first_page + (self.max_pages - 4))
		#

		rendered_links = "";

		for page in range(first_page, (1 + last_page)):
		#
			if (rendered_links != ""): rendered_links += self.separator

			rendered_links += (
				"<em>{0:d}</em>".format(page)
				if (self.page == page) else
				self._render_page_link(page, page)
			)
		#

		return (
			"<nav class='pagecontent_box pagecontent_page_navigation'>{0}{1}{2}</nav>".format(rendered_prefix, rendered_links, rendered_suffix)
			if (self.hide_navigation_title) else
			"<nav class='pagecontent_box pagecontent_page_navigation'><b>{0}</b>: {1}{2}{3}</nav>".format(L10n.get("pas_http_core_pages"), rendered_prefix, rendered_links, rendered_suffix)
		)
	#

	def _render_page_link(self, page, content):
	#
		"""
Renders the given page link with the defined content.

:param page: Page number
:param content: Link content

:return: (str) Rendered content
:since:  v0.1.01
		"""

		parameters = self.parameters.copy()
		if ("dsd" not in parameters): parameters['dsd'] = { }
		parameters['dsd'][self.dsd_page_key] = page

		return "{0}{1}</a>".format(XmlParser().dict_to_xml_item_encoder({
			"tag": "a",
			"attributes": { "href": Link().build_url(self.type, parameters) }
		}, False), content)
	#

	def set_dsd_page_key(self, key):
	#
		"""
Sets the DSD key used for the page value.

:param key: DSD key

:since: v0.1.01
		"""

		self.dsd_page_key = key
	#
#

##j## EOF