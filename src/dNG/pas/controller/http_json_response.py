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

from dNG.data.json_resource import JsonResource
from dNG.pas.data.text.l10n import L10n
from .abstract_http_response import AbstractHttpResponse

class HttpJsonResponse(AbstractHttpResponse):
#
	"""
The following class implements the response object for JSON data.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(HttpJsonResponse)

:since: v0.1.03
		"""

		AbstractHttpResponse.__init__(self)

		self.supported_features['dict_result_renderer'] = True
	#

	def send(self):
	#
		"""
Sends the prepared response.

:since: v0.1.00
		"""

		if (self.data is not None or self.stream_response.is_streamer_set()):
		#
			if (not self.initialized): self.init()

			if (self.get_content_type() is None):
			#
				self.set_content_type("application/json; charset={0}".format(self.charset))
			#

			self.send_headers()

			if (self.data is not None): AbstractHttpResponse.send(self)
		#
		elif (not self.are_headers_sent()):
		#
			self.init(False, True)

			header = self.get_header("HTTP/1.1", True)
			if (header is None): self.set_header("HTTP/1.1", "HTTP/1.1 500 Internal Server Error", True)

			if (self.errors is None):
			#
				error_result = { "error": { "title": L10n.get("core_title_error"),
				                            "message": (L10n.get("errors_core_unknown_error")
				                                        if (header is None) else
				                                        header
				                                       )
				                          }
				               }

				self.set_result(error_result)
			#
			else:
			#
				error_result = { "error": ({ "messages": self.errors }
				                           if (len(self.errors) > 1) else
				                           self.errors[0]
				                          )
				               }

				self.set_result(error_result)
			#

			self.send()
		#
	#

	def set_result(self, result):
	#
		"""
Sets the response result to be send JSON encoded.

:param result: Result data

:since: v0.1.03
		"""

		self.data = JsonResource().data_to_json(result)
	#
#

##j## EOF