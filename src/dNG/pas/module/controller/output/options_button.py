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

from dNG.pas.data.http.translatable_error import TranslatableError
from dNG.pas.data.text.l10n import L10n
from .options_bar import OptionsBar

class OptionsButton(OptionsBar):
#
	"""
An "OptionsButton" contains of several options formatted with title and
optional image as a context menu of an option button.

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
Renders the options button.

:since: v0.1.01
		"""

		if (self._is_primary_action()): raise TranslatableError("core_access_denied", 403)

		_id = "pas_http_core_{0:d}_{1:d}".format(id(self.context), id(self))

		rendered_content = """
{0}<script type="text/javascript"><![CDATA[
require([ "djt/OverlayButton.min" ], function(OverlayButton) {{
	new OverlayButton({{
		id: "{1}",
		button_content: "{2}",
		OverlayButton_class: "pageoptionsbar_button",
		OverlayButton_widget_class: "pageoptionsbar_widget"
	}});
}});
]]></script>
		""".format(self._render_options_bar_links(_id), _id, L10n.get("pas_http_core_additional_options"))

		self.set_action_result(rendered_content)
	#
#

##j## EOF