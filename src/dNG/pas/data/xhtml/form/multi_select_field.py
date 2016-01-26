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

from dNG.pas.runtime.type_exception import TypeException
from .abstract_multi_select_field import AbstractMultiSelectField
from .choices_mixin import ChoicesMixin

class MultiSelectField(ChoicesMixin, AbstractMultiSelectField):
#
	"""
"MultiSelectField" provides a selectbox for multiple selectable options.

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
Constructor __init__(MultiSelectField)

:param name: Form field name

:since: v0.1.01
		"""

		AbstractMultiSelectField.__init__(self, name)
		ChoicesMixin.__init__(self)

		self.size = MultiSelectField.SIZE_SMALL
	#

	def _check(self):
	#
		"""
Executes checks if the field value is valid.

:return: (bool) True if all checks are passed
:since:  v0.1.03
		"""

		_return = AbstractMultiSelectField._check(self)
		if (_return): _return = self._check_values_selected_size()

		return _return
	#

	def load_definition(self, field_definition):
	#
		"""
Loads the field configuration from the given definition.

:param field_definition: Field definition dict

:since: v0.1.01
		"""

		AbstractMultiSelectField.load_definition(self, field_definition)

		self.set_choices(field_definition['choices'])
	#

	def _validate_definition(self, field_definition):
	#
		"""
Validates that all relevant values are present for this field type.

:param field_definition: Field definition dict

:since: v0.1.01
		"""

		AbstractMultiSelectField._validate_definition(self, field_definition)

		if ("choices" not in field_definition): raise TypeException("'choices' is missing in the given form field definition")
	#
#

##j## EOF