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
from .abstract_select_field import AbstractSelectField
from .choices_mixin import ChoicesMixin

class SelectField(ChoicesMixin, AbstractSelectField):
#
	"""
"SelectField" provides a selectbox to select one option.

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
Constructor __init__(SelectField)

:param name: Form field name

:since: v0.1.01
		"""

		AbstractSelectField.__init__(self, name)
		ChoicesMixin.__init__(self)
	#

	def load_definition(self, field_definition):
	#
		"""
Loads the field configuration from the given definition.

:param field_definition: Field definition dict

:since: v0.1.01
		"""

		AbstractSelectField.load_definition(self, field_definition)

		self.set_choices(field_definition['choices'])
	#

	def _set_form(self, form):
	#
		"""
Sets the form this field is part of.

:param form: Form

:since: v0.1.03
		"""

		AbstractSelectField._set_form(self, form)
		ChoicesMixin._set_form(self, form)
	#

	def _validate_definition(self, field_definition):
	#
		"""
Validates that all relevant values are present for this field type.

:param field_definition: Field definition dict

:since: v0.1.01
		"""

		AbstractSelectField._validate_definition(self, field_definition)

		if ("choices" not in field_definition): raise TypeException("'choices' is missing in the given form field definition")
	#
#

##j## EOF