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

from binascii import hexlify
from os import urandom

from dNG.pas.data.binary import Binary
from dNG.pas.data.xhtml.form_tags import FormTags
from dNG.pas.data.xhtml.notification_store import NotificationStore
from dNG.pas.data.xhtml.oset.file_parser import FileParser
from dNG.pas.module.controller.abstract_http import AbstractHttp as AbstractHttpController

class NotificationBox(AbstractHttpController):
#
	"""
"NotificationBox" is a navigation element providing links to other services.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def _render_notification(self, data):
	#
		"""
Renders a notification.

:return: (str) XHTML notification
:since:  v0.1.01
		"""

		_return = ""

		if ("type" in data and "message" in data):
		#
			if (data['type'] == NotificationStore.TYPE_COMPLETED_INFO): css_class = "pagenotification_info pagenotification_completed_info"
			elif (data['type'] == NotificationStore.TYPE_ERROR): css_class = "pagenotification_error"
			elif (data['type'] == NotificationStore.TYPE_INFO): css_class = "pagenotification_info"

			content = { "css_class": css_class,
			            "id": "pas_notification_{0}".format(Binary.str(hexlify(urandom(10)))),
			            "type": NotificationStore.get_type_string(data['type']),
			            "message": FormTags.render(data['message'], block_encoding_supported = False),
			          }

			if (data['type'] == NotificationStore.TYPE_COMPLETED_INFO): content['auto_close'] = True

			parser = FileParser()
			parser.set_oset(self.response.get_oset())
			_return = parser.render("core.notification", content)
		#

		return _return
	#

	def execute_render(self):
	#
		"""
Action for "render"

:since: v0.1.00
		"""

		messages = NotificationStore.get_instance().export()
		rendered_messages = ""

		for message_data in messages: rendered_messages += self._render_notification(message_data)

		if (len(rendered_messages) > 0): self.set_action_result(rendered_messages)
	#
#

##j## EOF