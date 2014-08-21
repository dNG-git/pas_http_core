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

from dNG.pas.data.xhtml.formatting import Formatting as XHtmlFormatting
from dNG.pas.data.xhtml.link import Link
from dNG.pas.data.xhtml.form.renderer import Renderer
from dNG.pas.module.controller.abstract_http import AbstractHttp as AbstractHttpController

class Form(AbstractHttpController):
#
	"""
The "Form" class implements the form view.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def execute_render(self):
	#
		"""
Action for "render"

:since: v0.1.00
		"""

		if ("object" in self.context):
		#
			form_content = self._parse()
			form_id = XHtmlFormatting.escape(self.context['object'].get_form_id())

			if ("url_parameters" in self.context):
			#
				link = Link()
				form_parameters = link.build_url(Link.TYPE_FORM_FIELDS, self.context['url_parameters'])
				form_url = link.build_url(Link.TYPE_FORM_URL, self.context['url_parameters'])

				form = "<form id=\"pas_{0}\" action=\"{1}\" method='post' enctype='application/x-www-form-urlencoded' target='_self'>{2}{3}</form>"
				form = form.format(form_id, form_url, form_parameters, form_content)

				self.set_action_result(form)
			#
			else: self.set_action_result("<form id=\"pas_{0}\">{1}</form>".format(form_id, form_content))
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

		if ("url_parameters" in self.context):
		#
			button_title = self.context.get("button_title", "core_continue")
			_return += (renderer.render_submit_button(button_title) if (_return == "") else "\n{0}".format(renderer.render_submit_button(button_title)))
		#

		return _return
	#
#

##j## EOF