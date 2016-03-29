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

from dNG.pas.data.binary import Binary
from dNG.pas.data.xhtml.formatting import Formatting
from dNG.pas.runtime.type_exception import TypeException
from .abstract_field import AbstractField
from .choices_mixin import ChoicesMixin

class RadioField(ChoicesMixin, AbstractField):
#
	"""
"RadioField" provides a selectbox to select one option.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, name = None):
	#
		"""
Constructor __init__(RadioField)

:param name: Form field name

:since: v0.1.01
		"""

		AbstractField.__init__(self, name)
		ChoicesMixin.__init__(self)

		self.size = RadioField.SIZE_SMALL
	#

	def _check(self):
	#
		"""
Executes checks if the field value is valid.

:return: (bool) True if all checks are passed
:since:  v0.1.03
		"""

		_return = AbstractField._check(self)
		if (_return): _return = self._check_values_selected_size()

		if (_return):
		#
			_return = False

			for choice in self.choices:
			#
				if ("value" in choice and choice['value'] == self.value):
				#
					_return = True
					break
				#
			#

			if (not _return): self.error_data = "format_invalid"
		#

		return _return
	#

	def _check_selected_value(self, value):
	#
		"""
Check if the given value has been selected.

:param value: Value

:return: (bool) True if selected
:since:  v0.1.01
		"""

		return (self.value == value)
	#

	def get_type(self):
	#
		"""
Returns the field type.

:return: (str) Field type
:since:  v0.1.01
		"""

		return "radio"
	#

	def get_value(self, _raw_input = False):
	#
		"""
Returns the field value given or transmitted.

:param raw_input: True to return the raw (transmitted) value.

:return: (mixed) Field value; None on error
:since:  v0.1.01
		"""

		if (_raw_input): _return = self.value
		else: _return = (self.values_selected[0] if (len(self.values_selected) > 0) else None)

		return _return
	#

	def load_definition(self, field_definition):
	#
		"""
Loads the field configuration from the given definition.

:param field_definition: Field definition dict

:since: v0.1.01
		"""

		AbstractField.load_definition(self, field_definition)

		self.set_choices(field_definition['choices'])
	#

	def render(self):
	#
		"""
Renders the given field.

:return: (str) Valid XHTML form field definition
:since:  v0.1.01
		"""

		context = { "id": "pas_{0}".format(Formatting.escape(self.get_id())),
		            "name": Formatting.escape(self.name),
		            "title": Formatting.escape(self.get_title()),
		            "choices": self._get_content(),
		            "required": self.required,
		            "error_message": ("" if (self.error_data is None) else Formatting.escape(self.get_error_message()))
		          }

		return self._render_oset_file("core/form/radio", context)
	#

	def set_value(self, value):
	#
		"""
Sets the field value.

:param value: Field value

:since: v0.1.01
		"""

		value = Binary.str(value)

		if (not isinstance(value, str)):
		#
			value = Binary.str(value)
			if (type(value) is not str): value = str(value)
		#

		self.value = value

		self.valid = None
	#

	def _validate_definition(self, field_definition):
	#
		"""
Validates that all relevant values are present for this field type.

:param field_definition: Field definition dict

:since: v0.1.01
		"""

		AbstractField._validate_definition(self, field_definition)

		if ("choices" not in field_definition): raise TypeException("'choices' is missing in the given form field definition")

		for choice in field_definition['choices']:
		#
			if ("value" not in choice): raise TypeException("Radio form field choice value is missing")
		#
	#
#

##j## EOF