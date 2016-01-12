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
from dNG.pas.runtime.not_implemented_exception import NotImplementedException
from dNG.pas.runtime.type_exception import TypeException

class ChoicesMixin(object):
#
	"""
"ChoicesMixin" provides methods to handle selectable options.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(ChoicesMixin)

:since: v0.1.01
		"""

		self.choices = [ ]
		"""
Form field choices
		"""
		self.values_selected = [ ]
		"""
Prepared form field value choices
		"""
	#

	def _check_selected_value(self, value):
	#
		"""
Check if the given value has been selected.

:param value: Value

:return: (bool) True if selected
:since:  v0.1.01
		"""

		parent = super(ChoicesMixin, self)
		if (not hasattr(parent, "_check_selected_value")): raise NotImplementedException()

		return parent._check_selected_value(value)
	#

	def _check_values_selected_size(self, limit_max_supported = -1):
	#
		"""
Checks if the field value has the expected number of entries.

:param limit_max_supported: Maximum number of entries supported

:return: (bool) True if all checks are passed
:since:  v0.1.03
		"""

		error_data = None
		limit_max = self.limit_max
		values_selected_size = len(self.values_selected)

		if (limit_max is not None and limit_max > limit_max_supported): limit_max = limit_max_supported

		if (len(self.choices) < 1): error_data = "internal_error"
		elif (self.required and values_selected_size < 1): error_data = "required_element"
		elif (self.limit_min is not None
		      and (self.required or values_selected_size > 0)
		      and self.limit_min > values_selected_size
		     ): error_data = ( "limit_min", str(self.limit_min) )
		elif (limit_max is not None and limit_max < values_selected_size): error_data = ( "limit_max", str(limit_max) )

		if (error_data is not None): self.error_data = error_data
		return (error_data is None)
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
			value = ""

			if ("value" in choice):
			#
				value = Binary.str(choice['value'])
				value = Formatting.escape(value if (isinstance(value, str)) else str(value))

				choice['value'] = value
			#

			choice['title'] = (Formatting.escape(choice['title'])
			                   if ("title" in choice) else
			                   value
			                  )

			_return.append(choice)
		#

		return _return
	#

	def _prepare_choices(self):
	#
		"""
Parses the given choices to find selected values.

:since: v0.1.01
		"""

		choice_position = 0
		self.values_selected = [ ]

		for choice in self.choices:
		#
			if ("id" not in choice):
			#
				choice['id'] = "pas_{0}_{1:d}".format(self.id, choice_position)
				choice_position += 1
			#

			if ("value" in choice and self._check_selected_value(choice['value'])):
			#
				choice['selected'] = True
				self.values_selected.append(choice['value'])
			#
		#
	#

	def set_choices(self, choices):
	#
		"""
Sets the available choices.

:param choices: Selectable choices

:since: v0.1.01
		"""

		if (not isinstance(choices, list)): raise TypeException("Given choices type is invalid")
		self.choices = [ ]

		for choice in choices:
		#
			if ("value" in choice):
			#
				choice['value'] = Binary.str(choice['value'])
				if (not isinstance(choice['value'], str)): choice['value'] = str(choice['value'])
			#

			self.choices.append(choice)
		#
	#

	def _set_form(self, form):
	#
		"""
Sets the form this field is part of.

:param form: Form

:since: v0.1.03
		"""

		self._prepare_choices()
	#
#

##j## EOF