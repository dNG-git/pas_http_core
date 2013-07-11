# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.controller.AbstractHttpResponse
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

from dNG.data.rfc.basics import Basics as RfcBasics
from dNG.pas.data.traced_exception import TracedException
from dNG.pas.data.translatable_exception import TranslatableException
from dNG.pas.data.settings import Settings
from .abstract_response import AbstractResponse

class AbstractHttpResponse(AbstractResponse):
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
Constructor __init__(AbstractHttpResponse)

:since: v0.1.00
		"""

		AbstractResponse.__init__(self)

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

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Response.get_content_type()- (#echo(__LINE__)#)")
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

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Response.get_header({0}, +name_as_key)- (#echo(__LINE__)#)".format(name))

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

		if (message == None and isinstance(exception, TranslatableException)): message = "{0:l10n_message}".format(exception)
		if (not isinstance(exception, TracedException)): exception = TracedException(str(exception), exception)

		AbstractResponse.handle_exception_error(self, message, exception.get_printable_trace().replace("\n", "<br />\n"))
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

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Response.init(+cache, +compress)- (#echo(__LINE__)#)")

		AbstractResponse.init(self, cache, compress)

		if (self.stream_response.supports_headers()):
		#
			output_headers = ({ "Cache-Control": "public" } if (cache) else { "Cache-Control": "no-cache, no-store, must-revalidate" })
			if (self.expires > 0): output_headers['Expires'] = RfcBasics.get_rfc1123_datetime(self.expires)
			if (self.last_modified > 0): output_headers['Last-Modified'] = RfcBasics.get_rfc1123_datetime(self.last_modified)

			"""
Send P3P header if defined
			"""

			p3p_cp = Settings.get("pas_core_p3p_cp", "")
			p3p_url = Settings.get("pas_core_p3p_url", "").replace("&", "&amp;")

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

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Response.set_content_type({0})- (#echo(__LINE__)#)".format(content_type))
		self.set_header("Content-Type", content_type)
	#

	def set_cookie(self, name, value, timeout = 1209600, secure_only = False, http_only = False, domain = None, path = None):
	#
		"""
Sets a cookie.

:param name: Cookie name
:param value: Cookue value as string
:param timeout: Cookie timeout in seconds (max-age)
:param secure_only: True if send "secure" flag
:param http_only: True if send "httpOnly" flag
:param domain: Cookie domain restriction (defaults to requested host)
:param path: Cookie path restriction (defaults to "/")

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Response.set_cookie({0}, +value, {1:d}, +secure_only, +http_only, +domain, +path)- (#echo(__LINE__)#)".format(name, timeout))
		if (self.stream_response.supports_headers()): self.stream_response.set_cookie(name, value, timeout, secure_only, http_only, domain, path)
	#

	def set_header(self, name, value, name_as_key = False, value_append = False):
	#
		"""
Sets a header.

:param name: Header name
:param value: Header value as string or list
:param name_as_key: True if the name is used as a key
:param value_append: True if headers should be appended

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Response.set_header({0}, +value, +name_as_key, +value_append)- (#echo(__LINE__)#)".format(name))
		if (self.stream_response.supports_headers()): self.stream_response.set_header(name, value, name_as_key, value_append)
	#

	def set_send_headers_only(self, headers_only):
	#
		"""
Set to true to send headers only.

:param headers_only: Usually true for HEAD requests

:since: v0.1.01
		"""

		if (self.stream_response.supports_headers()): self.stream_response.set_send_headers_only(headers_only)
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