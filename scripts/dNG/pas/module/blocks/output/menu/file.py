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

from dNG.data.json_parser import JsonParser
from dNG.data.xml_parser import XmlParser
from dNG.pas.data.settings import Settings
from dNG.pas.data.http.url import Url
from dNG.pas.data.logging.log_line import LogLine
from dNG.pas.data.text.input_filter import InputFilter
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

		if (self.context != None and "file" in self.context): rendered_links = self._get_rendered_links(self.context['file'])
		else: rendered_links = self._get_rendered_links()

		if (len(rendered_links) > 0): self.set_action_result("<nav class='pagemainmenu ui-corner-all'><ul><li>{0}</li></ul></nav>".format("</li>\n<li>".join(rendered_links)))
	#

	def _filter_links(self, links):
	#
		"""
Filters links based on required permissions.

:return: (str) Link (X)HTML
:since:  v0.1.01
		"""

		_return = [ ]

		links_count = len(links)
		session = self.request.get_session()

		for position in range(0, links_count):
		#
			link = links[position]
			is_allowed = False

			if ("required_permission" in link):
			#
				permissions = (link['required_permission'] if (type(link['required_permission']) == list) else [ link['required_permission'] ])

				if (session != None): pass
			#
			elif ("required_permissions" in link and type(link['required_permissions']) == list):
			#
				permissions = link['required_permissions']

				if (session != None): pass
			#
			elif ("required_user_type" in link):
			#
				user_profile = (None if (session == None) else session.get_user_profile())
				user_types = (link['required_user_type'] if (type(link['required_user_type']) == list) else [ link['required_user_type'] ])

				if (user_profile == None): is_allowed = ("gt" in user_types)
				else:
				#
					for user_type in user_types:
					#
						if (user_profile.is_type(user_type)):
						#
							is_allowed = True
							break
						#
					#
				#
			#
			elif ("forbidden_user_type" in link):
			#
				user_profile = (None if (session == None) else session.get_user_profile())
				user_types = (link['forbidden_user_type'] if (type(link['forbidden_user_type']) == list) else [ link['forbidden_user_type'] ])

				if (user_profile == None): is_allowed = ("gt" not in user_types)
				else:
				#
					is_allowed = True

					for user_type in user_types:
					#
						if (user_profile.is_type(user_type)):
						#
							is_allowed = False
							break
						#
					#
				#
			#
			else: is_allowed = True

			if (is_allowed and "required_setting" in link):
			#
				setting = InputFilter.filter_control_chars(link['required_setting'])
				if (Settings.get(setting, False) == False): is_allowed = False
			#

			if (is_allowed): _return.append(link)
		#

		return _return
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
			_return += "{0} </a>".format(XHtmlFormatting.escape(title))
		#

		return _return
	#
#

##j## EOF