# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.controller.xhtml_response
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

from dNG.data.rfc.basics import direct_basics as direct_rfc_basics
from dNG.pas.data.exception import direct_exception
from dNG.pas.data.translatable_exception import direct_translatable_exception
from dNG.pas.data.settings import direct_settings
from .abstract_response import direct_abstract_response

class direct_abstract_http_response(direct_abstract_response):
#
	"""
The following class implements HTTP header specific methods.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(direct_abstract_http_response)

:since: v0.1.00
		"""

		direct_abstract_response.__init__(self)

		self.headers_sent = False
		"""
True if headers are sent
		"""
	#

	def are_headers_sent(self):
	#
		"""
Sends the prepared response headers.

:since: v0.1.00
		"""

		return (self.stream_response.are_headers_sent() if (self.stream_response.supports_headers()) else None)
	#

	def get_content_type(self):
	#
		"""
Returns the current HTTP Content-Type header.

:return: (str) HTTP Content-Type header; None if undefined
:since:  v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.get_content_type()- (#echo(__LINE__)#)")
		self.get_header("Content-Type")
	#

	def get_header(self, name, name_as_key = True):
	#
		"""
Returns an already defined header.

:param name: Header name
:param name_as_key: True if the name is used as a key

:return: (str) Header value if set; None otherwise
:since:  v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.get_header({0}, +name_as_key)- (#echo(__LINE__)#)".format(name))

		if (not self.stream_response.supports_headers()): return None
		else: return self.stream_response.get_header(name, name_as_key)
	#

	def get_http_code(self):
	#
		"""
Returns the HTTP response code.

:return: (int) HTTP code
:since:  v0.1.00
		"""

		return self.stream_response.get_http_code()
	#

	def handle_exception_error(self, message, exception):
	#
		"""
"handle_exception_error()" is called if an exception occurs and should be
send.

:param message: Message (will be translated if possible)
:param exception: Original exception (should be shown in dev mode)

:since: v0.1.00
		"""

		if (self.get_header("HTTP/1.1", True) == None): self.set_header("HTTP/1.1", "HTTP/1.1 500 Internal Server Error", True)

		if (message == None and isinstance(exception, direct_translatable_exception)): message = "{0:l10n_message}".format(exception)
		if (not isinstance(exception, direct_exception)): exception = direct_exception(str(exception), exception)

		direct_abstract_response.handle_exception_error(self, message, exception.get_printable_trace().replace("\n", "<br />\n"))
	#

	def init(self, cache = False, compress = True):
	#
		"""
Important headers will be created here. This includes caching, cookies, the
compression setting and information about P3P.

:param cache: Allow caching at client
:param compress: Send page GZip encoded (if supported)
:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.init(+cache, +compress)- (#echo(__LINE__)#)")

		direct_abstract_response.init(self, cache, compress)

		if (self.stream_response.supports_headers()):
		#
			output_headers = ({ "Cache-Control": "public" } if (cache) else { "Cache-Control": "no-cache, must-revalidate", "Pragma": "no-cache" })
			if (self.expires > 0): output_headers['Expires'] = direct_rfc_basics.get_rfc1123_datetime(self.expires)
			if (self.last_modified > 0): output_headers['Last-Modified'] = direct_rfc_basics.get_rfc1123_datetime(self.last_modified)

			"""
Send P3P header if defined
			"""

			p3p_cp = direct_settings.get("pas_core_p3p_cp", "")
			p3p_url = direct_settings.get("pas_core_p3p_url", "").replace("&", "&amp;")

			if (p3p_cp + p3p_url != ""):
			#
				p3p_data = ("" if (p3p_url == "") else "policyref=\"{0}\"".format(p3p_url))

				if (p3p_cp != ""):
				#
					if (p3p_data != ""): p3p_data += ","
					p3p_data += "CP=\"{0}\"".format(p3p_cp)
				#

				output_headers['P3P'] = p3p_data
			#

			for header in output_headers:
			#
				self.stream_response.set_header(header, output_headers[header])
			#
		#
	#

	def send_headers(self):
	#
		"""
Sends the prepared response headers.

:since: v0.1.00
		"""

		if (self.stream_response.supports_headers() and (not self.headers_sent)):
		#
			if (direct_settings.get("pas_core_cookies", True) and len(self.cookies)> 0): self.set_header("Set-Cookie", self.cookies)
			self.headers_sent = True
			self.stream_response.send_headers()
		#
	#

	def set_content_type(self, content_type):
	#
		"""
Sets the HTTP Content-Type header.

:param content_type: HTTP Content-Type header

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.set_content_type({0})- (#echo(__LINE__)#)".format(content_type))
		self.set_header("Content-Type", content_type)
	#

	def set_header(self, name, value, name_as_key = False, value_append = False):
	#
		"""
Sets a header.

:param name: Header name
:param value: Header value as string or array
:param name_as_key: True if the name is used as a key
:param value_append: True if headers should be appended

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.set_header({0}, +value, +name_as_key, +value_append)- (#echo(__LINE__)#)".format(name))
		if (self.stream_response.supports_headers()): self.stream_response.set_header(name, value, name_as_key, value_append)
	#

	def supports_headers(self):
	#
		"""
Returns false if headers are not supported.

:return: (bool) True if the response contain headers.
:since:  v0.1.00
		"""

		return True
	#
#

##j## EOF