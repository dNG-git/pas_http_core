# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.module.blocks.output.ServiceListMixin
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

from dNG.pas.data.cached_json_file import CachedJsonFile
from .filter_links_mixin import FilterLinksMixin
from .options_block_mixin import OptionsBlockMixin

class ServiceListMixin(FilterLinksMixin, OptionsBlockMixin):
#
	"""
The "ServiceListMixin" provides a standardized list of services view.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def _service_list_get_rendered_links(self, links):
	#
		"""
Returns a list of rendered links for the service menu.

:return: (list) Links for the service menu
:since:  v0.1.01
		"""

		_return = [ ]

		if (links != None):
		#
			links = self._filter_links(links)
			for link in links: _return.append(self.options_block_render_link(link))
		#

		return _return
	#

	def service_list_render_file(self, file_pathname):
	#
		"""
Action for "render"

:since: v0.1.00
		"""

		_return = ""

		json_data = CachedJsonFile.read(file_pathname)

		if (type(json_data) == list):
		#
			rendered_links = self._service_list_get_rendered_links(json_data)
			if (len(rendered_links) > 0): _return = "<nav class='pageoptionsblock pageservicelist'><ul><li>{0}</li></ul></nav>".format("</li><li>".join(rendered_links))
		#

		return _return
	#
#

##j## EOF