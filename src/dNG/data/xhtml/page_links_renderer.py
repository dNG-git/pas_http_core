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

from math import floor

from dNG.data.binary import Binary
from dNG.data.text.l10n import L10n
from dNG.data.xhtml.link import Link
from dNG.data.xml_parser import XmlParser
from dNG.runtime.type_exception import TypeException

class PageLinksRenderer(Link):
#
	"""
The "PageLinksRenderer" should be used for all page link bars used for
navigation.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, parameters, page, pages, _type = None):
	#
		"""
Constructor __init__(PageLinksRenderer)

:since: v0.2.00
		"""

		Link.__init__(self)

		self.dsd_page_key = "page"
		"""
DSD key used for the page value
		"""
		self.hidden_pages_content = "..."
		"""
Content used as replacement for a range of page link hidden
		"""
		self.hide_navigation_box = False
		"""
True to hide the surrounding navigation box
		"""
		self.max_pages = 11
		"""
Page links shown before collapsing the list of links (...)
		"""
		self.page = (0 if (page < 1) else int(page))
		"""
Active page
		"""
		self.pages = (1 if (pages < 1) else int(pages))
		"""
Pages available
		"""
		self.parameters = parameters
		"""
Parameters used to render each page link
		"""
		self.navigation_title = L10n.get("pas_http_core_pages")
		"""
Title used as prefix for the page links
		"""
		self.type = (_type if (_type is not None) else Link.TYPE_RELATIVE_URL)
		"""
Page link type
		"""
	#

	def render(self):
	#
		"""
Renders the page link navigation bar.

:return: (str) Rendered content
:since:  v0.2.00
		"""

		max_pages = (self.pages if (self.max_pages < 1) else self.max_pages)

		rendered_prefix = ""
		rendered_suffix = ""

		if (self.pages < (max_pages + 2)):
		#
			first_page = 1
			last_page = self.pages
		#
		elif (self.page > -1 and self.page < (max_pages - 2)):
		#
			rendered_suffix = "<li>{0}</li>\n<li>{1}</li>".format(self.hidden_pages_content,
			                                                      self._render_page_link(self.pages)
			                                                     )

			first_page = 1
			last_page = max_pages
		#
		elif (self.page < 0 or ((self.page + max_pages) - 3) > self.pages):
		#
			rendered_prefix = "<li>{0}</li>\n<li>{1}</li>\n".format(self._render_page_link(1),
			                                                        self.hidden_pages_content
			                                                       )

			first_page = ((self.pages - max_pages) + 3)
			last_page = self.pages
		#
		else:
		#
			rendered_prefix = "<li>{0}</li>\n<li>{1}</li>\n".format(self._render_page_link(1),
			                                                        self.hidden_pages_content
			                                                       )

			rendered_suffix = "<li>{0}</li>\n<li>{1}</li>".format(self.hidden_pages_content,
			                                                      self._render_page_link(self.pages)
			                                                     )

			first_page = (self.pages - (self.pages - self.page) - (floor(max_pages / 2)) + 2)
			last_page = (first_page + (max_pages - 4))
		#

		rendered_links = ""

		for page in range(first_page, (1 + last_page)):
		#
			rendered_links += ("<li>" +
			                   ("<em>{0:d}</em>".format(page)
			                    if (self.page == page) else
			                    self._render_page_link(page)
			                   ) +
			                   "</li>\n"
			                  )
		#

		_return = (""
		           if (self.hide_navigation_box) else
		           "<nav class='pagecontent_box pagecontent_pages_navigation_box pagecontent_pages_navigation_list'>"
		          )

		if (self.navigation_title != ""): _return += "<b>{0}</b>: ".format(self.navigation_title)
		_return += "<ul>{0}{1}{2}</ul>".format(rendered_prefix, rendered_links, rendered_suffix)

		if (not self.hide_navigation_box): _return += "</nav>"

		return _return
	#

	def _render_page_link(self, page):
	#
		"""
Renders the given page link with the defined content.

:param page: Page number

:return: (str) Rendered content
:since:  v0.2.00
		"""

		parameters = self.parameters.copy()
		if ("dsd" not in parameters): parameters['dsd'] = { }
		parameters['dsd'][self.dsd_page_key] = page

		link_attributes = { "tag": "a", "attributes": { "href": Link().build_url(self.type, parameters) } }

		return "{0}{1:d}</a>".format(XmlParser().dict_to_xml_item_encoder(link_attributes, False),
		                             page
		                            )
	#

	def set_dsd_page_key(self, key):
	#
		"""
Sets the DSD key used for the page value.

:param key: DSD key

:since: v0.2.00
		"""

		self.dsd_page_key = key
	#

	def set_navigation_box_visibility(self, visibility):
	#
		"""
Sets the visibility of the surrounding navigation box.

:param visibility: True to render the surrounding navigation box

:since: v0.2.00
		"""

		self.hide_navigation_box = (not visibility)
	#

	def set_navigation_title(self, title):
	#
		"""
Sets the navigation title to be used for rendering.

:param title: Navigation title to be used for rendering

:since: v0.2.00
		"""

		title = Binary.str(title)
		if (type(title) is not str): raise TypeException("Navigation title given is invalid")

		self.navigation_title = title
	#

	def set_max_pages(self, pages):
	#
		"""
Sets the maximum number of pages shown non-collapsed.

:param pages: Maximum number of pages shown non-collapsed

:since: v0.2.00
		"""

		self.max_pages = pages
	#
#

##j## EOF