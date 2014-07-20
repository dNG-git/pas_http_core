# -*- coding: utf-8 -*-
##j## BOF

"""
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
"""

from time import time

from dNG.data.rfc.basics import Basics as RfcBasics
from dNG.pas.data.binary import Binary
from dNG.pas.data.traced_exception import TracedException
from dNG.pas.data.translatable_exception import TranslatableException
from dNG.pas.data.http.translatable_error import TranslatableError as HttpTranslatableError
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
		self.content_is_dynamic = False
		"""
True if the content is dynamic
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

		self.supported_features['headers'] = True
		self.supported_features['script_name'] = True
		self.supported_features['streaming'] = self._supports_streaming
	#

	def are_headers_sent(self):
	#
		"""
Sends the prepared response headers.

:since: v0.1.00
		"""

		return (self.stream_response.are_headers_sent() if (self.stream_response.is_supported("headers")) else None)
	#

	def get_content_type(self):
	#
		"""
Returns the current HTTP Content-Type header.

:return: (str) HTTP Content-Type header; None if undefined
:since:  v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.get_content_type()- (#echo(__LINE__)#)", self, context = "pas_http_core")
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

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.get_header({1})- (#echo(__LINE__)#)", self, name, context = "pas_http_core")

		if (not self.stream_response.is_supported("headers")): return None
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

		is_critical = True

		if (self.get_header("HTTP/1.1", True) == None):
		#
			self.set_header("HTTP/1.1", "HTTP/1.1 500 Internal Server Error", True)

			if (isinstance(exception, HttpTranslatableError)):
			#
				code = exception.get_http_code()
				is_critical = isinstance(exception, HttpTranslatableException)

				if (code == 200): self.set_header("HTTP/1.1", "HTTP/1.1 200 OK", True)
				elif (code == 400): self.set_header("HTTP/1.1", "HTTP/1.1 400 Bad Request", True)
				elif (code == 402): self.set_header("HTTP/1.1", "HTTP/1.1 402 Payment Required", True)
				elif (code == 403): self.set_header("HTTP/1.1", "HTTP/1.1 403 Forbidden", True)
				elif (code == 404): self.set_header("HTTP/1.1", "HTTP/1.1 404 Not Found", True)
			#
		#

		title = (L10n.get("core_title_error_critical") if (is_critical) else L10n.get("core_title_error"))

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

		if (self.errors == None): self.errors = [ { "title": title, "message": message, "details": details } ]
		else: self.errors.append({ "title": title, "message": message, "details": details })
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

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.init()- (#echo(__LINE__)#)", self, context = "pas_http_core")

		expires = self.expires
		last_modified = self.last_modified

		if (self.content_is_dynamic):
		#
			cache = False
			current_time = int(time())

			expires = current_time
			last_modified = current_time
		#
		elif (not cache):
		#
			if (expires < 1): expires = int(time())
			if (last_modified < 1): last_modified = int(time())
		#

		if (self.stream_response.is_supported("compression")): self.stream_response.set_compression(compress)

		self.initialized = True

		if (self.stream_response.is_supported("headers")):
		#
			output_headers = ({ "Cache-Control": "public" } if (cache) else { "Cache-Control": "no-cache, no-store, must-revalidate" })
			if (not cache): output_headers['X-Robots-Tag'] = "noindex"

			for header in output_headers:
			#
				self.stream_response.set_header(header, output_headers[header])
			#

			if (expires > 0): self._set_expires(expires)
			if (last_modified > 0): self._set_last_modified(last_modified)
		#
	#

	def redirect(self, url):
	#
		"""
Redirect the requesting client to the given URL.

:param url: Target URL

:since: v0.1.00
		"""

		if (not self.initialized): self.init()

		if (self.expires <= time()): self.set_header("HTTP/1.1", "HTTP/1.1 307 Temporary Redirect", True)
		else: self.set_header("HTTP/1.1", "HTTP/1.1 303 See Other", True)

		self.set_header("Location", url)
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

		if (self.stream_response.is_supported("headers") and (not self.headers_sent)):
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

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_charset({1})- (#echo(__LINE__)#)", self, charset, context = "pas_http_core")
		self.charset = charset
	#

	def set_compression_formats(self, compression_formats):
	#
		"""
Sets the compression formats the client accepts.

:param compression_formats: List of accepted compression formats

:since: v0.1.01
		"""

		if (self.stream_response.is_supported("compression")): self.stream_response.set_compression_formats(compression_formats)
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

	def set_content_dynamic(self, mode):
	#
		"""
Sets the dynamic content mode of the response. Dynamic content overrides
the last modified timestamp with the current time.

:param mode: True if page contains dynamic content

:since: v0.1.01
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_content_dynamic()- (#echo(__LINE__)#)", self, context = "pas_http_core")

		if (mode and self.initialized):
		#
			current_time = int(time())

			self.set_expires(current_time)
			self.set_last_modified(current_time)
		#

		self.content_is_dynamic = mode
	#

	def set_content_type(self, content_type):
	#
		"""
Sets the HTTP Content-Type header.

:param content_type: HTTP Content-Type header

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_content_type({1})- (#echo(__LINE__)#)", self, content_type, context = "pas_http_core")
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

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_cookie({1}, {2:d})- (#echo(__LINE__)#)", self, name, timeout, context = "pas_http_core")
		if (self.stream_response.is_supported("headers")): self.stream_response.set_cookie(name, value, timeout, secure_only, http_only, domain, path)
	#

	def set_expires(self, timestamp):
	#
		"""
Sets a expires value if the response is not in dynamic mode.

:param timestamp: UNIX timestamp

:since: v0.1.01
		"""

		if (not self.content_is_dynamic): self._set_expires(int(timestamp))
	#

	def _set_expires(self, timestamp):
	#
		"""
Sets a expires value.

:param timestamp: UNIX timestamp

:since: v0.1.01
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}._set_expires({1:d})- (#echo(__LINE__)#)", self, timestamp, context = "pas_http_core")

		self.expires = timestamp
		if (self.initialized and self.stream_response.is_supported("headers") and (not self.headers_sent)): self.stream_response.set_header("Expires", RfcBasics.get_rfc5322_datetime(self.expires))
	#

	def set_expires_relative(self, timespan):
	#
		"""
Sets a expires value based on the current time if the response is not in
dynamic mode. For better readability we recommend using +5/-5.

:param timestamp: Timespan in seconds

:since: v0.1.01
		"""

		self.set_expires(int(time() + timespan))
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

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_header({1})- (#echo(__LINE__)#)", self, name, context = "pas_http_core")
		if (self.stream_response.is_supported("headers")): self.stream_response.set_header(name, value, name_as_key, value_append)
	#

	def set_last_modified(self, timestamp):
	#
		"""
Sets a last modified value if the response is not in dynamic mode.

:param timestamp: UNIX timestamp

:since: v0.1.00
		"""

		if (not self.content_is_dynamic): self._set_last_modified(int(timestamp))
	#

	def _set_last_modified(self, timestamp):
	#
		"""
Sets a last modified value.

:param timestamp: UNIX timestamp

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}._set_last_modified({1:d})- (#echo(__LINE__)#)", self, timestamp, context = "pas_http_core")

		self.last_modified = timestamp
		if (self.initialized and self.stream_response.is_supported("headers") and (not self.headers_sent)): self.stream_response.set_header("Last-Modified", RfcBasics.get_rfc5322_datetime(self.last_modified))
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

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_script_name({1})- (#echo(__LINE__)#)", self, script_name, context = "pas_http_core")
		self.script_name = script_name
	#

	def set_send_headers_only(self, headers_only):
	#
		"""
Set to true to send headers only.

:param headers_only: Usually true for HEAD requests

:since: v0.1.01
		"""

		if (self.stream_response.is_supported("headers")): self.stream_response.set_send_headers_only(headers_only)
	#

	def set_stream_mode(self):
	#
		"""
Sets the stream mode to send output as soon as available instead of caching
it.

:since: v0.1.00
		"""

		if (self.stream_response.is_supported("streaming")): self.stream_response.set_stream_mode()
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

		if (self.log_handler != None): self.log_handler.debug("{0!r} starts streaming with an IO chunk size of {1:d}", self, streamer.get_io_chunk_size(), context = "pas_http_core")
		self.stream_response.set_streamer(streamer)
	#

	def set_title(self, title):
	#
		"""
Sets the title set for the response.

:param title: Response title

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_title({1})- (#echo(__LINE__)#)", self, title, context = "pas_http_core")
		self.title = title
	#

	def _supports_streaming(self):
	#
		"""
Returns false if responses can not be streamed.

:return: (bool) True if streaming is supported.
:since:  v0.1.00
		"""

		return (False if (self.stream_response == None) else self.stream_response.is_supported("streaming"))
	#
#

##j## EOF