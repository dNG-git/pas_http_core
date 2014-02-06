# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.module.blocks.output.Form
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

from dNG.pas.data.xhtml.link import Link
from dNG.pas.data.xhtml.form.renderer import Renderer
from dNG.pas.module.blocks.abstract_block import AbstractBlock

class Form(AbstractBlock):
#
	"""
The "Form" class implements the form view.

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

		if ("object" in self.context and "url_parameters" in self.context):
		#
			link = Link()
			form_parameters = link.build_url(Link.TYPE_FORM_FIELDS, self.context['url_parameters'])
			form_url = link.build_url(Link.TYPE_FORM_URL, self.context['url_parameters'])

			self.set_action_result("<form action=\"{0}\" method='post' enctype='application/x-www-form-urlencoded' target='_self'>{1}{2}</form>".format(form_url, form_parameters, self._parse()))
		#
	#

	def _parse(self):
	#
		"""
Parses, renders and returns the given form.

:return: (str) Valid XHTML form
:since:  v0.1.00
		"""

		renderer = Renderer()
		renderer.set_data(self.context['object'].get_data())
		renderer.set_oset(self.response.get_oset())

		_return = renderer.render()

		button_title = (self.context['button_title'] if ("button_title" in self.context) else "core_continue")
		_return += (renderer.render_submit_button(button_title) if (_return == "") else "\n{0}".format(renderer.render_submit_button(button_title)))

		return _return
	#
#

##j## EOF