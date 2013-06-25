# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.controller.AbstractResponse
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

from threading import local
from time import time
from weakref import ref

from dNG.pas.data.binary import Binary
from dNG.pas.data.traced_exception import TracedException
from dNG.pas.data.text.l10n import L10n

class AbstractResponse(object):
#
	"""
This abstract class contains common methods for response implementations.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	local = local()
	"""
Thread-local static object
	"""

	def __init__(self):
	#
		"""
Constructor __init__(AbstractResponse)

:since: v0.1.00
		"""

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
		self.initialized = False
		"""
True if "init()" has been called
		"""
		self.last_modified = 0
		"""
Last modified UNIX timestamp
		"""
		self.log_handler = None
		"""
The log_handler is called whenever debug messages should be logged or errors
happened.
		"""
		self.script_name = None
		"""
Called script
		"""
		self.stream_response = None
		"""
Stream response object
		"""
		self.store = { }
		"""
Response specific generic cache
		"""
		self.title = None
		"""
Response title
		"""

		AbstractResponse.local.weakref_instance = ref(self)
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

	def get_store(self):
	#
		"""
Return the generic store for the response.

:return: (dict) Response store
:since:  v0.1.00
		"""

		return self.store
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

	def handle_exception_error(self, message, exception):
	#
		"""
"handle_exception_error()" is called if an exception occurs and should be
send.

:param message: Message (will be translated if possible)
:param exception: Original exception or formatted string (should be shown in
                  dev mode)

:since: v0.1.00
		"""

		if (message == None): message = L10n.get("errors_core_unknown_error")
		else: message = L10n.get("errors_{0}".format(message), message)

		exception = Binary.str(exception)

		if (exception == str): details = exception
		else:
		#
			if (not isinstance(exception, TracedException)): exception = TracedException(str(exception), exception)
			details = exception.get_printable_trace()
		#

		if (self.errors == None): self.errors = [ { "title": L10n.get("core_title_error_critical"), "message": message, "details": details } ]
		else: self.errors.append({ "title": L10n.get("core_title_error_critical"), "message": message, "details": details })
	#

	def init(self, cache = False, compress = True):
	#
		"""
Initialize runtime parameters for response.

:param cache: Allow caching at client
:param compress: Send page GZip encoded (if supported)

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.init(cache, compress)- (#echo(__LINE__)#)")

		if (not cache):
		#
			if (self.expires < 1): self.expires = time()
			if (self.last_modified < 1): self.last_modified = time()
		#
		elif (self.expires < 1): self.expires = time() + 63072000

		if (self.stream_response.supports_compression()): self.stream_response.set_compression(compress)

		self.initialized = True
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

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.set_charset({0})- (#echo(__LINE__)#)".format(charset))
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

		if (self.data != None): raise RuntimeError("Can't combine content and raw data in one response.", 95)
		if (self.stream_response.is_streamer_set()): raise RuntimeError("Can't combine a streaming object with content.", 95)

		self.content = content
	#

	def set_last_modified(self, timestamp):
	#
		"""
Sets a last modified value.

:param timestamp: UNIX timestamp
:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.set_last_modified({0:d})- (#echo(__LINE__)#)".format(timestamp))
		self.last_modified = timestamp
	#

	def set_log_handler(self, log_handler):
	#
		"""
Sets the log_handler.

:param log_handler: log_handler to use

:since: v0.1.00
		"""

		self.log_handler = log_handler
	#

	def set_raw_data(self, data):
	#
		"""
"set_raw_data()" ignores any protocol specification and buffer the data as
given.

:param data: Data to be send

:since: v0.1.00
		"""

		if (self.content != None): raise RuntimeError("Can't combine raw data and content in one response.", 95)
		if (self.stream_response.is_streamer_set()): raise RuntimeError("Can't combine a streaming object with raw data.", 95)

		self.data = data
	#

	def set_script_name(self, script_name):
	#
		"""
Sets the called script name.

:param script_name: Filename
:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.set_script_name({0})- (#echo(__LINE__)#)".format(script_name))
		self.script_name = script_name
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

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.set_title({0})- (#echo(__LINE__)#)".format(title))
		self.title = title
	#

	def supports_headers(self):
	#
		"""
Returns false if headers are not supported.

:return: (bool) True if the response contain headers.
:since:  v0.1.00
		"""

		return False
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

	@staticmethod
	def get_instance():
	#
		"""
Get the abstract_response singleton.

:return: (AbstractResponse) Object on success
:since:  v0.1.00
		"""

		return (AbstractResponse.local.weakref_instance() if (hasattr(AbstractResponse.local, "weakref_instance")) else None)
	#

	@staticmethod
	def get_instance_store():
	#
		"""
Get the abstract_response singleton.

:param count: Count "get()" response

:return: (AbstractResponse) Object on success
:since:  v0.1.00
		"""

		instance = (AbstractResponse.local.weakref_instance() if (hasattr(AbstractResponse.local, "weakref_instance")) else None)
		return (None if (instance == None) else instance.get_store())
	#
#

##j## EOF