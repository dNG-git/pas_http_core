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

from dNG.data.http.translatable_exception import TranslatableException
from dNG.data.xhtml.form.renderer import Renderer
from dNG.data.xhtml.form.view import View

class FormParseMixin(object):
#
	"""
The "FormParseMixin" is used to parse and render a context form instance.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def _parse_context_form(self):
	#
		"""
Parses, renders and returns the context form.

:return: (str) Valid XHTML form
:since:  v0.2.00
		"""

		if (not isinstance(self.context.get("object"), View)): raise TranslatableException("core_unknown_error")

		renderer = Renderer()
		renderer.set_data(self.context['object'].get_data())
		if (self.response.is_supported("html_theme")): renderer.set_oset(self.response.get_oset())

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