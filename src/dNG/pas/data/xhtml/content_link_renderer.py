# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.xhtml.ContentLinkRenderer
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

import re

from dNG.data.xml_parser import XmlParser
from dNG.pas.data.xhtml.link import Link

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
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
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

	def render(self, content, data):
	#
		"""
Renders a link ready for output.

:param content: Content data
:param data: Link parameters

:return: (str) Rendered content
:since:  v0.1.01
		"""

		_return = content

		if ("type" in data): _type = (data['type'] if (type(data['type']) == int) else Link.get_type(data['type']))
		else: _type = Link.TYPE_RELATIVE

		if ("id" in data): parameters = { "m": "datalinker", "a": "related", "dsd": { "oid": data['id'] } }
		elif ("link" in data and data['link'] == "params"):
		#
			parameters = { }
			if ("m" in data): parameters['m'] = data['m']
			if ("s" in data): parameters['s'] = data['s']
			if ("a" in data): parameters['a'] = data['a']

			if ("dsd" in data):
			#
				parameters['dsd'] = data['dsd']
				if ("__source__" in data['dsd']): parameters['dsd'] = re.sub("\\_\\_source\\_\\_", Link.query_param_encode(Link().build_url(Link.TYPE_QUERY_STRING, { "__request__": True })), parameters['dsd'])
				parameters['dsd'] = re.sub("\\[\\w+\\]", "", parameters['dsd'])
			#
		#
		elif ("tag" in data and self.datalinker_main_id != None): parameters = { "m": "datalinker", "a": "related", "dsd": { "otag": data['tag'], "omid": self.datalinker_main_id } }
		else: parameters = { }

		if (len(parameters) > 0):
		#
			_return = "{0}{1}</a>".format(XmlParser().dict_to_xml_item_encoder({
				"tag": "a",
				"attributes": { "href": Link().build_url(_type, parameters) }
			}, False), content)

		return _return
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