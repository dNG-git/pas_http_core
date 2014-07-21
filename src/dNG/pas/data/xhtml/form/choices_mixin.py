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
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
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

		raise NotImplementedException()
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
				choice['id'] = "pas_http_form_{0:d}_{1:d}".format(self.form_position, choice_position)
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
		self.choices = choices
	#
#

##j## EOF