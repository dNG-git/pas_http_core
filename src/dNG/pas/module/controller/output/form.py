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

from time import time

from dNG.pas.data.http.translatable_error import TranslatableError
from dNG.pas.data.text.input_filter import InputFilter
from dNG.pas.data.xhtml.formatting import Formatting as XHtmlFormatting
from dNG.pas.data.xhtml.link import Link
from dNG.pas.data.xhtml.form.processor import Processor
from dNG.pas.database.connection import Connection
from dNG.pas.database.nothing_matched_exception import NothingMatchedException
from dNG.pas.module.controller.abstract_http import AbstractHttp as AbstractHttpController
from .form_parse_mixin import FormParseMixin

class Form(FormParseMixin, AbstractHttpController):
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

	@Connection.wrap_callable
	def execute_api_ping(self):
	#
		"""
Action for "api_ping"

:since: v0.1.03
		"""

		if (not self.response.is_supported("dict_result_renderer")): raise TranslatableError("core_access_denied", 403)
		form_id = InputFilter.filter_control_chars(self.request.get_dsd("form_id"))

		# TODO: Check if constant or setting makes more sense
		validity_time = 300

		try: form_store = Processor.load_form_store_id(form_id)
		except NothingMatchedException as handled_exception: raise TranslatableError("core_access_denied", 403, _exception = handled_exception)

		form_store.set_data_attributes(validity_end_time = time() + validity_time)
		form_store.save()

		self.response.set_result({ "expires_in": validity_time })
	#

	def execute_render(self):
	#
		"""
Action for "render"

:since: v0.1.00
		"""

		if (self._is_primary_action()): raise TranslatableError("core_access_denied", 403)

		form_content = self._parse_context_form()
		form_id = XHtmlFormatting.escape(self.context['object'].get_form_render_id())

		if ("url_parameters" in self.context):
		#
			link = Link()

			form_parameters = link.build_url(Link.TYPE_FORM_FIELDS, self.context['url_parameters'])

			form_post_encoding = (self.context['post_encoding']
			                      if ("post_encoding" in self.context) else
			                      "application/x-www-form-urlencoded"
			                     )

			form_url = link.build_url(Link.TYPE_FORM_URL, self.context['url_parameters'])

			form = "<form id=\"pas_{0}\" action=\"{1}\" method='post' enctype=\"{2}\" target='_self'>{3}{4}</form>"
			form = form.format(form_id, form_url, form_post_encoding, form_parameters, form_content)
		#
		else: form = "<form id=\"pas_{0}\">{1}</form>".format(form_id, form_content)

		if (self.context['object'].is_supported("form_store")):
		#
			form += """
<script type="text/javascript"><![CDATA[
require([ "pas/HttpJsonApiRequest.min" ], function(HttpJsonApiRequest) {{
var hjapi_request = new HttpJsonApiRequest();
hjapi_request.init_ping({{ id: "pas.Form.ping.{0}", endpoint: "pas/form/ping/1.0/{0}", delay: 60 }});
}});
]]></script>
			""".format(form_id).strip()
		#

		self.set_action_result(form)
	#

	def execute_render_view(self):
	#
		"""
Action for "render_view"

:since: v0.1.00
		"""

		if (self._is_primary_action()): raise TranslatableError("core_access_denied", 403)

		form_content = self._parse_context_form()
		form_id = XHtmlFormatting.escape(self.context['object'].get_form_id())

		self.set_action_result("<div id=\"pas_{0}\">{1}</div>".format(form_id, form_content))
	#
#

##j## EOF