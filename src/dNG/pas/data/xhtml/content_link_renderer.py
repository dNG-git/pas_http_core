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

import re

from dNG.data.xml_parser import XmlParser
from dNG.pas.data.text.content_link_renderer import ContentLinkRenderer as _ContentLinkRenderer
from dNG.pas.data.xhtml.link import Link

class ContentLinkRenderer(_ContentLinkRenderer):
#
	"""
The link renderer parses and renders internal links to DataLinker and other
sources.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def _get_link_parameters(self, data):
	#
		"""
Returns a dict of parameters to be used with a Link instance.

:param data: Link definition

:return: (dict) Link parameters
:since:  v0.1.01
		"""

		_return = { }

		if ("id" in data): _return = _ContentLinkRenderer._get_link_parameters(self, data)
		elif ("link" in data and data['link'] == "params"):
		#
			if ("m" in data): _return['m'] = data['m']
			if ("s" in data): _return['s'] = data['s']
			if ("a" in data): _return['a'] = data['a']

			if ("dsd" in data):
			#
				_return['dsd'] = data['dsd']
				if ("__source__" in data['dsd']): _return['dsd'] = re.sub("\\_\\_source\\_\\_", Link.encode_query_value(Link().build_url(Link.TYPE_QUERY_STRING, { "__request__": True })), _return['dsd'])
				_return['dsd'] = re.sub("\\_\\_\\w+\\\\_\\_", "", _return['dsd'])
			#
		#
		elif ("tag" in data and self.datalinker_main_id != None): _ContentLinkRenderer._get_link_parameters(self, data)

		return _return
	#

	def _render(self, content, link_type, link_parameters):
	#
		"""
Renders a link with the parsed parameters ready for output.

:param content: Content data
:param link_type: Link type
:param link_parameters: Link parameters

:return: (str) Rendered content
:since:  v0.1.01
		"""

		link_arguments = { "tag": "a",
		                   "attributes": { "href": Link().build_url(link_type, link_parameters) }
		                 }

		return "{0}{1}</a>".format(XmlParser().dict_to_xml_item_encoder(link_arguments, False), content)
	#
#

##j## EOF