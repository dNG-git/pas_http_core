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

from time import time

from dNG.data.rfc.basics import Basics as RfcBasics
from dNG.pas.data.binary import Binary
from dNG.pas.data.traced_exception import TracedException
from dNG.pas.data.translatable_exception import TranslatableException
from dNG.pas.data.settings import Settings
from dNG.pas.data.http.translatable_exception import TranslatableException as HttpTranslatableException
from dNG.pas.data.text.l10n import L10n
from dNG.pas.runtime.io_exception import IOException
from .abstract_response import AbstractResponse

class AbstractHttpResponse(AbstractResponse):
#
	"""
The following abstract class implements HTTP response specific methods.

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

		self.charset = "utf-8"
		"""
Charset used for response
		"""
		self.content = None
		"""
Content to be shown
		"""
		self.cookies = { }
		"""
Cookies to be send
		"""
		self.data = None
		"""
Data to be send
		"""
		self.errors = None
		"""
Errors that should be shown.
		"""
		self.expires = 0
		"""
Expiring UNIX timestamp
		"""
		self.headers_sent = False
		"""
True if headers are sent
		"""
		self.initialized = False
		"""
True if "init()" has been called
		"""
		self.last_modified = 0
		"""
Last modified UNIX timestamp
		"""
		self.script_name = None
		"""
Called script
		"""
		self.stream_response = None
		"""
Stream response object
		"""
		self.title = None
		"""
Response title
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

	def get_accepted_formats(self):
	#
		"""
Returns the formats the client accepts.

:return: (list) Accepted formats
:since:  v0.1.00
		"""

		return self.stream_response.get_accepted_formats()
	#

	def get_charset(self):
	#
		"""
Gets the charset defined for the response.

:return: (str) Charset used for response
:since:  v0.1.00
		"""

		return self.charset
	#

	def get_compression_formats(self):
	#
		"""
Returns the compression formats the client accepts.

:return: (list) Compression formats supported
:since:  v0.1.01
		"""

		return self.stream_response.get_compression_formats()
	#

	def get_title(self):
	#
		"""
Return the title set for the response.

:return: (str) Response title
:since:  v0.1.00
		"""

		return self.title
	#

	def handle_critical_error(self, message):
	#
		"""
"handle_critical_error()" is called to send a critical error message.

:param message: Message (will be translated if possible)

:since: v0.1.00
		"""

		message = L10n.get("errors_{0}".format(message), message)

		if (self.errors == None): self.errors = [ { "title": L10n.get("core_title_error_critical"), "message": message } ]
		else: self.errors.append({ "title": L10n.get("core_title_error_critical"), "message": message })
	#

	def handle_error(self, message):
	#
		"""
"handle_error()" is called to send a error message.

:param message: Message (will be translated if possible)

:since: v0.1.00
		"""

		message = L10n.get("errors_{0}".format(message), message)

		if (self.errors == None): self.errors = [ { "title": L10n.get("core_title_error"), "message": message } ]
		else: self.errors.append({ "title": L10n.get("core_title_error"), "message": message })
	#

	def handle_exception(self, message, exception):
	#
		"""
"handle_exception()" is called if an exception occurs and should be
send.

:param message: Message (will be translated if possible)
:param exception: Original exception or formatted string (should be shown in
                  dev mode)

:since: v0.1.00
		"""

		if (self.get_header("HTTP/1.1", True) == None):
		#
			self.set_header("HTTP/1.1", "HTTP/1.1 500 Internal Server Error", True)

			if (isinstance(exception, HttpTranslatableException)):
			#
				code = exception.get_http_code()

				if (code == 400): self.set_header("HTTP/1.1", "HTTP/1.1 400 Bad Request", True)
				elif (code == 402): self.set_header("HTTP/1.1", "HTTP/1.1 402 Payment Required", True)
				elif (code == 403): self.set_header("HTTP/1.1", "HTTP/1.1 403 Forbidden", True)
				elif (code == 404): self.set_header("HTTP/1.1", "HTTP/1.1 404 Not Found", True)
			#
		#

		if (message == None and isinstance(exception, TranslatableException)): message = "{0:l10n_message}".format(exception)
		if (not isinstance(exception, TracedException)): exception = TracedException(str(exception), exception)

		if (message == None): message = L10n.get("errors_core_unknown_error")
		else: message = L10n.get("errors_{0}".format(message), message)

		if (isinstance(exception, TracedException)): details = Binary.str(exception.get_printable_trace().replace("\n", "<br />\n"))
		else:
		#
			exception = TracedException(str(exception), exception)
			details = exception.get_printable_trace()
		#

		if (self.errors == None): self.errors = [ { "title": L10n.get("core_title_error_critical"), "message": message, "details": details } ]
		else: self.errors.append({ "title": L10n.get("core_title_error_critical"), "message": message, "details": details })
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

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Response.init(cache, compress)- (#echo(__LINE__)#)")

		if (not cache):
		#
			if (self.expires < 1): self.expires = time()
			if (self.last_modified < 1): self.last_modified = time()
		#
		elif (self.expires < 1): self.expires = time() + 63072000

		if (self.stream_response.supports_compression()): self.stream_response.set_compression(compress)

		self.initialized = True

		if (self.stream_response.supports_headers()):
		#
			output_headers = ({ "Cache-Control": "public" } if (cache) else { "Cache-Control": "no-cache, no-store, must-revalidate" })
			if (self.expires > 0): output_headers['Expires'] = RfcBasics.get_rfc1123_datetime(self.expires)
			if (self.last_modified > 0): output_headers['Last-Modified'] = RfcBasics.get_rfc1123_datetime(self.last_modified)

			"""
Send P3P header if defined
			"""

			p3p_cp = Settings.get("pas_http_core_p3p_cp", "")
			p3p_url = Settings.get("pas_http_core_p3p_url", "").replace("&", "&amp;")

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

	def reset(self):
	#
		"""
Resets all cached values.

:since: v0.1.00
		"""

		self.content = None
		self.data = None
		self.errors = None
		self.expires = 0
		self.initialized = False
		self.last_modified = 0
		self.title = None
	#

	def send(self):
	#
		"""
Sends the prepared response.

:since: v0.1.00
		"""

		if (self.data == None): self.stream_response.send()
		else: self.stream_response.send_data(self.data)
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

	def set_accepted_formats(self, accepted_formats):
	#
		"""
Sets the formats the client accepts.

:param accepted_formats: List of accepted formats

:since: v0.1.00
		"""

		self.stream_response.set_accepted_formats(accepted_formats)
	#

	def set_charset(self, charset):
	#
		"""
Sets the charset used for the response.

:param charset: Charset used for response

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Response.set_charset({0})- (#echo(__LINE__)#)".format(charset))
		self.charset = charset
	#

	def set_compression_formats(self, compression_formats):
	#
		"""
Sets the compression formats the client accepts.

:param compression_formats: List of accepted compression formats

:since: v0.1.01
		"""

		if (self.stream_response.supports_compression()): self.stream_response.set_compression_formats(compression_formats)
	#

	def set_content(self, content):
	#
		"""
Sets the content for the response.

:param content: Content to be send

:since: v0.1.00
		"""

		if (self.data != None): raise IOException("Can't combine content and raw data in one response.")
		if (self.stream_response.is_streamer_set()): raise IOException("Can't combine a streaming object with content.")

		self.content = content
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

	def set_last_modified(self, timestamp):
	#
		"""
Sets a last modified value.

:param timestamp: UNIX timestamp

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Response.set_last_modified({0:d})- (#echo(__LINE__)#)".format(timestamp))
		self.last_modified = timestamp
	#

	def set_raw_data(self, data):
	#
		"""
"set_raw_data()" ignores any protocol specification and buffer the data as
given.

:param data: Data to be send

:since: v0.1.00
		"""

		if (self.content != None): raise IOException("Can't combine raw data and content in one response.")
		if (self.stream_response.is_streamer_set()): raise IOException("Can't combine a streaming object with raw data.")

		self.data = data
	#

	def set_script_name(self, script_name):
	#
		"""
Sets the called script name.

:param script_name: Filename

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Response.set_script_name({0})- (#echo(__LINE__)#)".format(script_name))
		self.script_name = script_name
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

	def set_stream_mode(self):
	#
		"""
Sets the stream mode to send output as soon as available instead of caching
it.

:since: v0.1.00
		"""

		if (self.stream_response.supports_streaming()): self.stream_response.set_stream_mode()
	#

	def set_stream_response(self, stream_response):
	#
		"""
Sets the stream response object used to send data to.

:param stream_response: Stream response

:since: v0.1.00
		"""

		self.stream_response = stream_response
	#

	def set_streamer(self, streamer):
	#
		"""
Sets the streamer to create response data when requested.

:since: v0.1.01
		"""

		self.stream_response.set_streamer(streamer)
	#

	def set_title(self, title):
	#
		"""
Sets the title set for the response.

:param title: Response title

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Response.set_title({0})- (#echo(__LINE__)#)".format(title))
		self.title = title
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

	def supports_script_name(self):
	#
		"""
Returns false if the script name is not needed for execution.

:return: (bool) True if the controller should call "setScriptName()".
:since:  v0.1.00
		"""

		return True
	#

	def supports_streaming(self):
	#
		"""
Returns false if responses can not be streamed.

:return: (bool) True if streaming is supported.
:since:  v0.1.00
		"""

		return (False if (self.stream_response == None) else self.stream_response.supports_streaming())
	#
#

##j## EOF