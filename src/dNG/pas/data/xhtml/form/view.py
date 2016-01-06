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
from os import urandom

from dNG.pas.data.binary import Binary
from dNG.pas.data.supports_mixin import SupportsMixin
from dNG.pas.data.text.l10n import L10n
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.runtime.type_exception import TypeException
from .abstract_field import AbstractField

class View(SupportsMixin):
#
	"""
"View" provides methods for a form-like view based on XHTML.

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
Constructor __init__(View)

:param form_id: Form ID

:since: v0.1.03
		"""

		SupportsMixin.__init__(self)

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
		self.form_id = None
		"""
Form ID
		"""
		self.form_render_id = None
		"""
Form render ID
		"""

		L10n.init("pas_http_core_form")

		if (form_id == False): self.form_id = Binary.str(hexlify(urandom(16)))
		else:
		#
			self.form_id = (Binary.str(hexlify(urandom(16)))
			                if (form_id is None or len(form_id) < 1) else
			                form_id
			               )
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

		field._set_form(self)

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

	def get_context(self):
	#
		"""
Returns the validator context used for defined callbacks.

:return: (dict) Form validator context dict
:since:  v0.1.03
		"""

		return self.context
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

	def get_field_list(self, section = None):
	#
		"""
Returns a list of all input field defined.

:param section: Form section

:return: (list) List of dictionaries with the field name and section
:since:  v0.1.00
		"""

		_return = [ ]

		if (section is None): sections = self.cache
		else: sections = ([ self.cache[self.cache_sections[section]] ] if (section in self.cache_sections) else [ ])

		for section in sections:
		#
			for field_name in section['positions']: _return.append({ "name": field_name, "section": section['name'] })
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

	def get_form_render_id(self):
	#
		"""
Returns the form render ID.

:return: (str) Form render ID
:since:  v0.1.03
		"""

		return (self.get_form_id() if (self.form_render_id is None) else self.form_render_id)
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

	def set_form_render_id(self, form_render_id):
	#
		"""
Sets a form render ID.

:param form_render_id: Form render ID

:since: v0.1.03
		"""

		self.form_render_id = form_render_id
	#
#

##j## EOF