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

from binascii import hexlify
from time import time
from os import urandom

from dNG.pas.controller.abstract_request import AbstractRequest
from dNG.pas.data.binary import Binary
from dNG.pas.data.http.translatable_error import TranslatableError
from dNG.pas.data.text.form.processor import Processor as _Processor
from dNG.pas.data.text.key_store import KeyStore
from dNG.pas.database.nothing_matched_exception import NothingMatchedException

class Processor(_Processor):
#
	"""
"Processor" provides form methods based on XHTML.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, form_id = None):
	#
		"""
Constructor __init__(Processor)

:since: v0.1.00
		"""

		_Processor.__init__(self, form_id)

		self.form_id_value = None
		"""
Value for the given form ID
		"""
		self.form_store = None
		"""
HTTP form store
		"""

		if (self.form_id == None):
		#
			self.form_id = Binary.str(hexlify(urandom(16)))
			self.form_id_value = Binary.str(hexlify(urandom(16)))

			self.form_store = KeyStore()
			self.form_store.set_data_attributes(key = self.form_id, validity_end_time = time() + 3600)
			self.form_store.set_value_dict({ "form_id_value": self.form_id_value })
			self.form_store.save()
		#
		else:
		#
			try:
			#
				self.form_store = KeyStore.load_key(self.form_id)
				self.form_store.set_data_attributes(validity_end_time = time() + 300)
			#
			except NothingMatchedException: raise TranslatableError("core_access_denied")
		#

		form_data = self.form_store.get_value_dict()
		form_id_value = form_data.get("form_id_value")

		self.add_entry("hidden", { "name": "form_id", "content": self.form_id })
		self.add_entry("hidden", { "name": self.form_id, "content": form_id_value })
	#

	def check(self, force = False):
	#
		"""
Parses all previously defined form fields and checks them.

:return: (bool) True if all checks are passed
:since:  v0.1.00
		"""

		if (self.form_id != None):
		#
			form_data = self.form_store.get_value_dict()
			form_id_value = (self.get_input(self.form_id) if (self.form_id_value == None) else self.form_id_value)

			if (form_data.get("form_id_value") != form_id_value): raise TranslatableError("core_access_denied")
		#

		return _Processor.check(self, force)
	#

	def get_data(self, flush = True):
	#
		"""
Returns all defined fields.

:param flush: Flush the cache

:return: (list) Field data
:since:  v0.1.00
		"""

		_return = _Processor.get_data(self, flush)

		for section in _return:
		#
			for field_data in section['fields']:
			#
				if (field_data['error'] != None): field_data['error'] = self._get_error_message(field_data['error'])
			#
		#

		return _return
	#

	def get_input(self, name):
	#
		"""
"get_input()" should be used to read the input value for the field from a
source (e.g. from a HTTP POST request parameter).

:param name: Field and parameter name

:return: (mixed) Value; None if not set
:since:  v0.1.00
		"""

		return (AbstractRequest.get_instance().get_parameter(name) if (self.form_has_input) else None)
	#

	def set_input_available(self):
	#
		"""
Sets the flag for available input. Input values can be read with
"get_input()".

:since: v0.1.00
		"""

		self.form_has_input = True
	#
#

##j## EOF