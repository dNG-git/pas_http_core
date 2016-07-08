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

from dNG.runtime.io_exception import IOException
from dNG.vfs.file_like_wrapper_mixin import FileLikeWrapperMixin

class UploadedFile(FileLikeWrapperMixin):
#
	"""
"UploadedFile" provides a file-like access for temporary, uploaded files.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	_FILE_WRAPPED_METHODS = ( "get_size",
	                          "read",
	                          "readline",
	                          "seek",
	                          "tell"
	                        )

	def __init__(self):
	#
		"""
Constructor __init__(UploadedFile)

:since: v0.2.00
		"""

		FileLikeWrapperMixin.__init__(self)

		self.client_content_type = None
		"""
The client supplied content type.
		"""
		self.client_file_name = None
		"""
The client supplied file name.
		"""
	#

	def copy_data(self, target, timeout = None):
	#
		"""
Copy data to the target.

:param target: Any object providing a "write()" method
:param timeout: Timeout for copying data

:since: v0.2.00
		"""

		timeout_time = (0 if (timeout is None) else time() + timeout)
		self.seek(0)

		while ((not self.is_eof())
		       and (timeout_time < 1 or time() < timeout_time)
		      ): target.write(self.read(16384))

		if (not self.is_eof()): raise IOException("Timeout occurred before EOF")
	#

	def get_client_content_type(self):
	#
		"""
Returns the client supplied content type.

:return: Client content type
:since:  v0.2.00
		"""

		return self.client_content_type
	#

	def get_client_file_name(self):
	#
		"""
Returns the client supplied file name.

:return: Client file name
:since:  v0.2.00
		"""

		return self.client_file_name
	#

	def is_eof(self):
	#
		"""
Checks if the uploaded file has reached EOF.

:return: (bool) True if EOF
:since:  v0.2.00
		"""

		if (self._wrapped_resource is None): _return = True
		elif (hasattr(self._wrapped_resource, "is_eof")): _return = self._wrapped_resource.is_eof()
		else: _return = (self.tell() == self.get_size())

		return _return
	#

	def set_client_content_type(self, content_type):
	#
		"""
Sets the client supplied content type.

:param file_name: Client content type

:since: v0.2.00
		"""

		self.client_content_type = content_type
	#

	def set_client_file_name(self, file_name):
	#
		"""
Sets the client supplied file name.

:param file_name: Client file name

:since: v0.2.00
		"""

		self.client_file_name = file_name
	#

	def set_file(self, resource):
	#
		"""
Sets the file-like resource to be used.

:param resource: File-like resource

:since: v0.2.00
		"""

		self._set_wrapped_resource(resource)
	#
#

##j## EOF