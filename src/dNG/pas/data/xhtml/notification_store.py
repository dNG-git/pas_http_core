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

from copy import copy

from dNG.pas.controller.abstract_response import AbstractResponse
from dNG.pas.runtime.io_exception import IOException

class NotificationStore(object):
#
	"""
"NotificationStore" creates a message flow for later output.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	TYPE_COMPLETED_INFO = 1
	"""
Notification about a completed task
	"""
	TYPE_ERROR = 2
	"""
Notification about a task error
	"""
	TYPE_INFO = 3
	"""
Informational notification
	"""

	def __init__(self, store):
	#
		"""
Constructor __init__(NotificationStore)

:since: v0.1.00
		"""

		self.store = store
		"""
Notification store
		"""
	#

	def add_error(self, message):
	#
		"""
Adds a new notification about a task error.

:param message: Notification message

:since: v0.1.00
		"""

		self.store.append({ "type": NotificationStore.TYPE_ERROR, "message": message })
	#

	def add_completed_info(self, message):
	#
		"""
Adds a new notification about a completed task.

:param message: Notification message

:since: v0.1.00
		"""

		self.store.append({ "type": NotificationStore.TYPE_COMPLETED_INFO, "message": message })
	#

	def add_info(self, message):
	#
		"""
Adds a new informational notification about a task.

:param message: Notification message

:since: v0.1.00
		"""

		self.store.append({ "type": NotificationStore.TYPE_INFO, "message": message })
	#

	def export(self):
	#
		"""
Exports and flushes notifications from the store.

:since: v0.1.00
		"""

		_return = (self.store.copy() if (hasattr(self.store, "copy")) else copy(self.store))
		del(self.store[:])

		return _return
	#

	@staticmethod
	def get_instance(context = "site"):
	#
		"""
Get the NotificationStore singleton.

:return: (object) Object on success
:since:  v0.1.00
		"""

		store = AbstractResponse.get_instance_store()

		if (store is None): raise IOException("Response store not available")
		if ("dNG.pas.data.xhtml.NotificationStore" not in store): store['dNG.pas.data.xhtml.NotificationStore'] = { }
		if (context not in store['dNG.pas.data.xhtml.NotificationStore']): store['dNG.pas.data.xhtml.NotificationStore'][context] = [ ]

		return NotificationStore(store['dNG.pas.data.xhtml.NotificationStore'][context])
	#

	@staticmethod
	def get_type_int(_type):
	#
		"""
Parses the given type parameter given as a string value.

:param _type: String type

:return: (int) Internal type
:since:  v0.1.01
		"""

		if (_type == "completed_info"): _return = NotificationStore.TYPE_COMPLETED_INFO
		elif (_type == "info"): _return = NotificationStore.TYPE_INFO
		elif (_type == "error"): _return = NotificationStore.TYPE_ERROR
		else: _return = 0

		return _return
	#

	@staticmethod
	def get_type_string(_type):
	#
		"""
Returns a string representing the given type.

:return: (str) Type as string
:since:  v0.1.00
		"""

		if (type(_type) is not int): _type = NotificationStore.get_type_int(_type)

		if (_type & NotificationStore.TYPE_COMPLETED_INFO == NotificationStore.TYPE_COMPLETED_INFO): _return = "completed_info"
		elif (_type & NotificationStore.TYPE_INFO == NotificationStore.TYPE_INFO): _return = "info"
		elif (_type & NotificationStore.TYPE_ERROR == NotificationStore.TYPE_ERROR): _return = "error"
		else: _return = "unknown"

		return _return
	#
#

##j## EOF