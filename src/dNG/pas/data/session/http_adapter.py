# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;session

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasSessionVersion)#
#echo(__FILEPATH__)#
"""

from binascii import hexlify
from os import urandom
from time import time

from dNG.pas.controller.abstract_http_response import AbstractHttpResponse
from dNG.pas.data.binary import Binary
from dNG.pas.data.settings import Settings
from dNG.pas.data.text.tmd5 import Tmd5
from dNG.pas.module.named_loader import NamedLoader
from .abstract_adapter import AbstractAdapter

class HttpAdapter(AbstractAdapter):
#
	"""
A session protocol adapter for HTTP to implement methods that rely on
protocol specific functionality.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def is_persistent(self):
	#
		"""
Returns true if the uuID session is set persistently at the client.

:return: (bool) True if set
:since:  v0.1.00
		"""

		return (self.session.get("uuids.passcode") is not None)
	#

	def is_valid(self):
	#
		"""
Returns true if the defined session is valid.

:return: (bool) True if session is valid
:since:  v0.1.00
		"""

		_return = False

		passcode = self.session.get("uuids.passcode")

		if (not self.session.is_persistent()): _return = True
		elif (passcode is not None):
		#
			cookie_passcode = None
			request = NamedLoader.get_singleton("dNG.pas.controller.AbstractHttpRequest", False)
			response = AbstractHttpResponse.get_instance()

			if (request is not None):
			#
				uuids_cookie = request.get_cookie("uuids")

				if (uuids_cookie is not None):
				#
					cookie_data = uuids_cookie.split(":", 1)
					if (cookie_data[0] == self.session.get_uuid()): cookie_passcode = cookie_data[1]
				#
			#

			passcode_prev = self.session.get("uuids.passcode_prev")
			passcode_timeout = self.session.get("uuids.passcode_timeout", 0)

			if (passcode_timeout + Settings.get("pas_session_uuids_passcode_grace_period", 15) > time()):
			#
				passcode_prev_timeout = self.session.get("uuids.passcode_prev_timeout")

				if (cookie_passcode == Tmd5.hash(passcode)): _return = True
				elif (passcode_prev_timeout is not None
				      and (passcode_prev_timeout + Settings.get("pas_session_uuids_passcode_grace_period", 15) > time()
				           or (passcode_prev is not None and cookie_passcode == Tmd5.hash(passcode_prev))
				          )
				     ): _return = True
			#

			if (not _return and isinstance(response, AbstractHttpResponse)): response.set_cookie("uuids", "", 0)
		#

		return _return
	#

	def load(self):
	#
		"""
Uses protocol specific functionality to load additional information of an
session.

:since: v0.1.00
		"""

		passcode_timeout = self.session.get("uuids.passcode_timeout")

		if (passcode_timeout is not None):
		#
			self.session.set_session_time(int(Settings.get("pas_session_uuids_passcode_session_time", 604800)))
			if (passcode_timeout < time()): self._renew_passcode()
		#
	#

	def _renew_passcode(self):
	#
		"""
Saves changes of the uuIDs instance.

:return: (bool) True on success
:since: v0.1.00
		"""

		passcode = self.session.get("uuids.passcode")

		if (passcode is not None):
		#
			self.session.set("uuids.passcode_prev", passcode)
			self.session.set("uuids.passcode_prev_timeout", int(time()))
		#

		passcode = Binary.str(hexlify(urandom(16)))
		self.session.set("uuids.passcode", passcode)
		self.session.set("uuids.passcode_timeout", int(time() + int(Settings.get("pas_session_uuids_passcode_timeout", 300))))

		response = AbstractHttpResponse.get_instance()

		if (isinstance(response, AbstractHttpResponse)):
		#
			store = response.get_instance_store()
			if (store is not None): store['dNG.pas.data.session.HttpAdapter.passcode_changed'] = True
		#
	#

	def save(self):
	#
		"""
Saves changes of the uuIDs instance.

:return: (bool) True on success
:since: v0.1.00
		"""

		passcode_timeout = self.session.get("uuids.passcode_timeout")

		if (passcode_timeout is not None):
		#
			self.session.set_session_time(int(Settings.get("pas_session_uuids_passcode_session_time", 604800)))
			if (passcode_timeout < time()): self._renew_passcode()

			is_passcode_changed = False
			response = AbstractHttpResponse.get_instance()

			if (isinstance(response, AbstractHttpResponse)):
			#
				store = response.get_instance_store()

				if (store is not None and "dNG.pas.data.session.HttpAdapter.passcode_changed" in store):
				#
					is_passcode_changed = store['dNG.pas.data.session.HttpAdapter.passcode_changed']
					store['dNG.pas.data.session.HttpAdapter.passcode_changed'] = False
				#
			#

			if (is_passcode_changed):
			#
				passcode_hashed = Tmd5.hash(self.session.get("uuids.passcode"))
				response.set_cookie("uuids", "{0}:{1}".format(self.session.get_uuid(), passcode_hashed))
			#
		#
		elif (not self.is_persistent()):
		#
			instance = NamedLoader.get_singleton("dNG.pas.controller.AbstractHttpRequest", False)

			if (instance is not None and instance.get_cookie("uuids") is not None):
			#
				response = AbstractHttpResponse.get_instance()
				if (isinstance(response, AbstractHttpResponse)): response.set_cookie("uuids", "", 0)
			#
		#

		return True
	#

	def set_cookie(self, mode = True):
	#
		"""
Sets a cookie to store the uuID.

:param mode: True to use a cookie

:since: v0.1.00
		"""

		if (mode and self.session.get("uuids.passcode") is None): self.session.set("uuids.passcode_timeout", 0)
	#

	@staticmethod
	def get_uuid():
	#
		"""
Returns the uuID.

:return: (str) Unique user identification; None if unknown
:since:  v0.1.00
		"""

		instance = NamedLoader.get_singleton("dNG.pas.controller.AbstractHttpRequest", False)

		if (instance is not None):
		#
			uuids_cookie = instance.get_cookie("uuids")
			_return = (None if (uuids_cookie is None) else uuids_cookie.split(":", 1)[0])
		#
		else: _return = None

		return _return
	#
#

##j## EOF