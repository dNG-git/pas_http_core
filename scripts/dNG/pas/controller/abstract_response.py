# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.controller.abstract_response
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
from weakref import proxy

from dNG.pas.data.binary import direct_binary
from dNG.pas.data.exception import direct_exception
from dNG.pas.data.text.l10n import direct_l10n

class direct_abstract_response(object):
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
Constructor __init__(direct_abstract_response)

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
		self.title = None
		"""
Response title
		"""

		direct_abstract_response.local.instance = proxy(self)
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

		message = direct_l10n.get("errors_{0}".format(message), message)

		if (self.errors == None): self.errors = [ { "title": direct_l10n.get("core_title_error_critical"), "message": message } ]
		else: self.errors.append({ "title": direct_l10n.get("core_title_error_critical"), "message": message })
	#

	def handle_error(self, message):
	#
		"""
"handle_error()" is called to send a error message.

:param message: Message (will be translated if possible)

:since: v0.1.00
		"""

		message = direct_l10n.get("errors_{0}".format(message), message)

		if (self.errors == None): self.errors = [ { "title": direct_l10n.get("core_title_error"), "message": message } ]
		else: self.errors.append({ "title": direct_l10n.get("core_title_error"), "message": message })
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

		if (message == None): message = direct_l10n.get("errors_core_unknown_error")
		else: message = direct_l10n.get("errors_{0}".format(message), message)

		exception = direct_binary.str(exception)

		if (exception == str): details = exception
		else:
		#
			if (not isinstance(exception, direct_exception)): exception = direct_exception(str(exception), exception)
			details = exception.get_printable_trace()
		#

		if (self.errors == None): self.errors = [ { "title": direct_l10n.get("core_title_error_critical"), "message": message, "details": details } ]
		else: self.errors.append({ "title": direct_l10n.get("core_title_error_critical"), "message": message, "details": details })
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

	def return_instance(self):
	#
		"""
This "return_instance()" implementation is a dummy as a thread-local weakref
is used for "get_instance()".

:since: v0.1.00
		"""

		pass
	#

	def send(self):
	#
		"""
Sends the prepared response.

:since: v0.1.00
		"""

		raise RuntimeError("Not implemented", 38)
	#

	def send_raw_data(self, data = None):
	#
		"""
"send_raw_data()" ignores any protocol specification and send the data as
given.

:param data: Data to be send (buffer will be appended)

:since: v0.1.00
		"""

		raise RuntimeError("Not implemented", 38)
	#

	def set_accepted_formats(self, accepted_formats):
	#
		"""
Sets the formats the client accepts.

:param accepted_formats: List of accepted formats

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.set_accepted_formats(accepted_formats)- (#echo(__LINE__)#)")
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

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.set_compression_formats(accepted_formats)- (#echo(__LINE__)#)")
		if (self.stream_response.supports_compression()): self.stream_response.set_compression_formats(compression_formats)
	#

	def set_content(self, content):
	#
		"""
Sets the content for the response.

:param content: Content to be send

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.set_content(data)- (#echo(__LINE__)#)")
		if (self.data != None): raise RuntimeError("Can't combine content and raw data in one response.", 95)
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

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.set_raw_data(data)- (#echo(__LINE__)#)")
		if (self.content != None): raise RuntimeError("Can't combine content and raw data in one response.", 95)

		self.data = data
	#

	def set_stream_mode(self, active):
	#
		"""
Sets the stream response object used to send data to.

:param active: True if streaming response
:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.set_stream_mode(active)- (#echo(__LINE__)#)")
		if (self.stream_response.supports_streaming()): self.stream_response.set_stream_mode(active)
	#

	def set_stream_response(self, stream_response):
	#
		"""
Sets the stream response object used to send data to.

:param stream_response: Stream response
:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.set_stream_response(stream_response)- (#echo(__LINE__)#)")
		self.stream_response = stream_response
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
	def get_instance(count = False):
	#
		"""
Get the abstract_response singleton.

:param count: Count "get()" response

:return: (direct_abstract_response) Object on success
:since:  v0.1.00
		"""

		return (direct_abstract_response.local.instance if (hasattr(direct_abstract_response.local, "instance")) else None)
	#
#

##j## EOF