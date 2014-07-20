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

from dNG.pas.data.xhtml.formatting import Formatting as XHtmlFormatting
from dNG.pas.runtime.type_exception import TypeException
from .abstract_field import AbstractField
from .choices_mixin import ChoicesMixin

class MultiSelectField(AbstractField, ChoicesMixin):
#
	"""
"MultiSelectField" provides a selectbox for multiple selectable options.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, name = None):
	#
		"""
Constructor __init__(MultiSelectField)

:param name: Form field name

:since: v0.1.01
		"""

		AbstractField.__init__(self, name)
		ChoicesMixin.__init__(self)

		self.size = MultiSelectField.SIZE_SMALL
	#

	def check(self, force = False):
	#
		"""
Checks if the field value is valid.

:param force: True to force revalidation

:return: (bool) True if all checks are passed
:since:  v0.1.01
		"""

		if (self.valid == None or force):
		#
			if (len(self.choices) < 1): self.error_data = "internal_error"
			elif (self.required and len(self.values_selected) < 1): self.error_data = "required_element"
		#

		return AbstractField.check(self, force)
	#

	def _check_selected_value(self, value):
	#
		"""
Check if the given value has been selected.

:param value: Value

:return: (bool) True if selected
:since:  v0.1.01
		"""

		return (value in self.value)
	#

	def _get_content(self):
	#
		"""
Returns the field content.

:return: (str) Field content
:since:  v0.1.01
		"""

		_return = [ ]

		for choice in self.choices:
		#
			if ("value" in choice):
			#
				choice['value'] = XHtmlFormatting.escape(choice['value'])

				choice['title'] = (XHtmlFormatting.escape(choice['title'])
				                   if ("title" in choice) else
				                   choice['value']
				                  )

				_return.append(choice)
			#
		#

		return _return
	#

	def get_type(self):
	#
		"""
Returns the field type.

:return: (str) Field type
:since:  v0.1.01
		"""

		return "multiselect"
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

		context = { "id": XHtmlFormatting.escape(self.get_id()),
		            "name": XHtmlFormatting.escape(self.name),
		            "title": XHtmlFormatting.escape(self.get_title()),
		            "choices": self._get_content(),
		            "required": self.required,
		            "error_message": ("" if (self.error_data == None) else XHtmlFormatting.escape(self.get_error_message()))
		          }

		return self._render_oset_file("core/form/multiselect", context)
	#

	def _set_form_value(self, form):
	#
		"""
Sets the field value based on the given form.

:param form: Form

:since: v0.1.01
		"""

		AbstractField._set_form_value(self, form)
		self._prepare_choices()
	#

	def set_value(self, value):
	#
		"""
Sets the field value.

:param value: Field value

:since: v0.1.01
		"""

		if (value == None): self.value = [ ]
		elif (type(value) == str): self.value = [ value ]
		else: self.value = value

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
	#
#

##j## EOF