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

from .link import Link

class ContentLinkRenderer(object):
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

	def __init__(self):
	#
		"""
Constructor __init__(ContentLinkRenderer)

:since: v0.1.01
		"""

		self.datalinker_main_id = None
		"""
DataLinker main ID for tags
		"""
	#

	def _get_link_parameters(self, data):
	#
		"""
Returns a dict of parameters to be used with a Link instance.

:param data: Link definition

:return: (dict) Link parameters
:since:  v0.1.01
		"""

		_return = { }

		if ("id" in data): _return = { "m": "datalinker", "a": "related", "dsd": { "oid": data['id'] } }
		elif ("link" in data and data['link'] == "params"):
		#
			if ("m" in data): _return['m'] = data['m']
			if ("s" in data): _return['s'] = data['s']
			if ("a" in data): _return['a'] = data['a']
			if ("dsd" in data): _return['dsd'] = re.sub("\\_\\_\\w+\\\\_\\_", "", data['dsd'])
		#
		elif ("tag" in data and self.datalinker_main_id != None): _return = { "m": "datalinker", "a": "related", "dsd": { "otag": data['tag'], "omid": self.datalinker_main_id } }

		return _return
	#

	def render(self, content, data):
	#
		"""
Renders a link ready for output.

:param content: Content data
:param data: Link definition

:return: (str) Rendered content
:since:  v0.1.01
		"""

		if ("type" in data): link_type = (data['type'] if (type(data['type']) == int) else Link.get_type(data['type']))
		else: link_type = Link.TYPE_RELATIVE

		link_parameters = self._get_link_parameters(data)

		return (self._render(content, link_type, link_parameters) if (len(link_parameters) > 0) else content)
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

		return "{0} ({1})".format(content, Link.get_preferred().build_url((Link.TYPE_ABSOLUTE & link_type), link_parameters))
	#

	def set_datalinker_main_id(self, id_main):
	#
		"""
Sets the DataLinker main ID for tags.

:param id_main: DataLinker main ID

:since: v0.1.01
		"""

		self.datalinker_main_id = id_main
	#
#

##j## EOF