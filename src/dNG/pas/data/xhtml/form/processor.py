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

from binascii import hexlify
from copy import copy
from time import time
from os import urandom

from dNG.pas.controller.abstract_request import AbstractRequest
from dNG.pas.data.binary import Binary
from dNG.pas.data.http.translatable_error import TranslatableError
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.text.key_store import KeyStore
from dNG.pas.database.nothing_matched_exception import NothingMatchedException
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.runtime.type_exception import TypeException
from .abstract_field import AbstractField
from .read_only_hidden_field import ReadOnlyHiddenField

class Processor(object):
#
	"""
"Processor" provides form methods based on XHTML.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, form_id = None):
	#
		"""
Constructor __init__(Processor)

:param form_id: Form ID used for CSRF protection; Use false to explicitly
                deactive this feature.

:since: v0.1.00
		"""

		self.cache = [ ]
		"""
List of form elements
		"""
		self.cache_sections = { }
		"""
List of section positions in the cache
		"""
		self.context = { }
		"""
Form validator context
		"""
		self.field_counter = 0
		"""
Nameless form field counter
		"""
		self.input_available = False
		"""
Can be set to true using "set_input_available()"
		"""
		self.form_id = None
		"""
Form ID
		"""
		self.form_id_value = None
		"""
Value for the given form ID
		"""
		self.form_store = None
		"""
HTTP form store
		"""
		self.valid = None
		"""
Form validity check result variable
		"""

		L10n.init("pas_http_core_form")

		if (form_id == False): self.form_id = Binary.str(hexlify(urandom(16)))
		elif (form_id is None or len(form_id) < 1):
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
				self.form_store = KeyStore.load_key(form_id)
				self.form_store.set_data_attributes(validity_end_time = time() + 300)
			#
			except NothingMatchedException: raise TranslatableError("core_access_denied")

			self.form_id = form_id
		#

		if (self.form_store is not None):
		#
			form_data = self.form_store.get_value_dict()
			form_id_value = form_data.get("form_id_value")

			field = ReadOnlyHiddenField("form_id")
			field.set_value(self.form_id)
			self.add(field)

			field = ReadOnlyHiddenField(self.form_id)
			field.set_value(form_id_value)
			self.add(field)
		#
	#

	def add(self, field, section = ""):
	#
		"""
Adds a custom form field.

:param field: Form field
:param section: Form section name the field is part of

:return: (bool) False if the content caused an error condition
:since:  v0.1.01
		"""

		if (not isinstance(field, AbstractField)): raise TypeException("Given field type is invalid")

		if (self.form_id is not None
		    and (not field.is_id_set())
		   ): field.set_id("{0}_{1:d}".format(self.get_form_id(), self.field_counter))

		self.field_counter += 1

		field._set_form_context(self.context)
		field._set_form_value(self)

		name = field.get_name()

		if (section not in self.cache_sections):
		#
			position = len(self.cache)
			section_dict = { "fields": [ ], "name": section, "positions": { } }

			self.cache.append(section_dict)
			self.cache_sections[section] = position
		#

		cache = self.cache[self.cache_sections[section]]

		if (name in cache['positions']): self.update(section, name, field)
		else:
		#
			position = len(cache['fields'])

			cache['fields'].append(field)
			cache['positions'][name] = position

			self.valid = None
		#

		return field.is_valid()
	#

	def check(self, force = False):
	#
		"""
Parses all previously defined form fields and checks them.

:return: (bool) True if all checks are passed
:since:  v0.1.00
		"""

		_return = (self.valid if (self.valid is not None) else True)

		if (self.form_store is not None):
		#
			form_data = self.form_store.get_value_dict()
			form_id_value = (self.get_input(self.form_id) if (self.form_id_value is None) else self.form_id_value)

			if (form_data.get("form_id_value") != form_id_value): raise TranslatableError("core_access_denied")
		#

		if (len(self.cache) > 0 and (force or self.valid is None)):
		#
			for section in self.cache:
			#
				for field in section['fields']:
				#
					result = field.check()
					if (not result): _return = False
				#
			#
		#

		self.valid = _return
		return _return
	#

	def get_data(self, flush = True):
	#
		"""
Returns all defined fields.

:param flush: Flush the cache

:return: (list) Field data
:since:  v0.1.00
		"""

		# pylint: disable=no-member

		_return = (self.cache.copy() if (hasattr(self.cache, "copy")) else copy(self.cache))

		if (flush):
		#
			self.cache = [ ]
			self.cache_sections = { }
			self.field_counter = 0
			self.input_available = False
			self.valid = None
		#

		return _return
	#

	def get_errors(self, section = None, types_hidden = None):
	#
		"""
Returns detected errors as a list of dicts containing the field name, the
untranslated as well as the translated error message.

:param section: If given will only return error messages for the given
                section.
:param types_hidden: A list of form fields for which error messages are
                     ignored.

:return: (list) List of dicts with "name", "error_data" and "error_message"
:since:  v0.1.00
		"""

		_return =  [ ]

		if (section is None): sections = self.cache_sections
		else: sections = ([ self.cache_sections[section] ] if (section in self.cache_sections) else None)

		if (type(types_hidden) is list): types_hidden = [ "hidden", "info", "subtitle" ]
		else: types_hidden += [ "hidden", "info", "subtitle" ]

		if (sections is not None):
		#
			for section in sections:
			#
				for field in section['fields']:
				#
					if ((not field.check())
					    and field.get_type() not in types_hidden
					   ):
					#
						_return.append({ "name": field.get_name(),
						                 "error_data": field.get_error_data(),
						                 "error_message": field.get_error_message()
						               })
					#
				#
			#
		#

		return _return
	#

	def get_form_id(self):
	#
		"""
Returns the form ID.

:return: (str) Form ID
:since:  v0.1.01
		"""

		return self.form_id
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

		return (AbstractRequest.get_instance().get_parameter(name) if (self.input_available) else None)
	#

	def get_value(self, name, section = None, _raw_input = False):
	#
		"""
Returns the field value given or transmitted.

:param name: Field name
:param section: Form section

:return: (str) Field value; None on error
:since:  v0.1.00
		"""

		_return = None

		if (section is None): sections = self.cache
		else: sections = ([ self.cache[self.cache_sections[section]] ] if (section in self.cache_sections) else [ ])

		for section in sections:
		#
			if (name in section['positions']):
			#
				field = section['fields'][section['positions'][name]]
				_return = field.get_value(_raw_input)
				break
			#
		#

		return _return
	#

	def load_definition(self, field_list):
	#
		"""
Loads all fields from the given form definition.

:param field_list: List of fields

:since: v0.1.01
		"""

		if (not isinstance(field_list, list)): raise TypeException("Given form definition type is invalid")

		for field_definition in field_list:
		#
			if (not isinstance(field_definition, dict) or "type" not in field_definition): raise TypeException("Given form field definition type is invalid")
			field = NamedLoader.get_instance("dNG.pas.data.xhtml.form.{0}".format(field_definition['type']))
			field.load_definition(field_definition)

			self.add(field, field_definition.get("section", ""))
		#
	#

	def set_context(self, context):
	#
		"""
Sets the validator context used for defined callbacks.

:param context: Form validator context dict

:since: v0.1.00
		"""

		self.context = context
	#

	def set_input_available(self):
	#
		"""
Sets the flag for available input. Input values can be read with
"get_input()".

:since: v0.1.00
		"""

		self.input_available = True
	#
#

##j## EOF