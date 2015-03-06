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

from dNG.pas.data.text.md5 import Md5
from dNG.pas.data.xhtml.formatting import Formatting
from .placeholder_mixin import PlaceholderMixin
from .text_field import TextField

class PasswordField(TextField, PlaceholderMixin):
#
	"""
"PasswordField" provides  password fields (including optional a repetition
check).

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	PASSWORD_CLEARTEXT = 1
	"""
Only recommended for separate encryption operations
	"""
	PASSWORD_MD5 = 2
	"""
MD5 encoded password
	"""
	PASSWORD_WITH_REPETITION = 4
	"""
Password input repetition
	"""

	def __init__(self, name = None):
	#
		"""
Constructor __init__(AbstractField)

:param name: Form field name

:since: v0.1.01
		"""

		TextField.__init__(self, name)
		PlaceholderMixin.__init__(self)

		self.mode = PasswordField.PASSWORD_MD5
		"""
Password field mode
		"""
		self.raw_value = None
		"""
Encrypted field value
		"""
		self.repetition_value = None
		"""
Encrypted repetition field value
		"""
	#

	def check(self, force = False):
	#
		"""
Checks if the field value is valid.

:param force: True to force revalidation

:return: (bool) True if all checks are passed
:since:  v0.1.01
		"""

		_return = TextField.check(self, force)

		if (_return
		    and self.mode & PasswordField.PASSWORD_WITH_REPETITION == PasswordField.PASSWORD_WITH_REPETITION
		    and self.value != self.repetition_value
		   ):
		#
			_return = False

			self.error_data = "password_repetition"
			self.valid = False
		#

		return _return
	#

	def _check_length(self):
	#
		"""
Checks the length of value.

:return: (bool) True if all checks are passed
:since:  v0.1.00
		"""

		data_length = (0 if (self.raw_value is None) else len(self.raw_value))
		error_data = None

		if (self.required and data_length < 1): error_data = "required_element"
		elif (self.limit_min is not None
		      and (self.required or data_length > 0)
		      and self.limit_min > data_length
		     ): error_data = ( "string_min", str(self.limit_min) )
		elif (self.limit_max is not None and self.limit_max < data_length): error_data = ( "string_max", str(self.limit_max) )

		if (error_data is not None): self.error_data = error_data
		return (error_data is None)
	#

	def _encrypt_value(self, value):
	#
		"""
Encrypts the given form field value based on the defined mode.

:param value: Original value

:return: (str) Encrypted value
		"""

		return (value if (value is None) else Md5.hash(value))
	#

	def get_type(self):
	#
		"""
Returns the field type.

:return: (str) Field type
:since:  v0.1.01
		"""

		return ("password_with_repetition"
		        if (self.mode & PasswordField.PASSWORD_WITH_REPETITION == PasswordField.PASSWORD_WITH_REPETITION) else
		        "password"
		       )
	#

	def get_value(self, _raw_input = False):
	#
		"""
Returns the field value given or transmitted.

:param raw_input: True to return the raw (transmitted) value.

:return: (mixed) Field value; None on error
:since:  v0.1.01
		"""

		return (self.raw_value if (_raw_input) else self.value)
	#

	def load_definition(self, field_definition):
	#
		"""
Loads the field configuration from the given definition.

:param field_definition: Field definition dict

:since: v0.1.01
		"""

		TextField.load_definition(self, field_definition)

		mode = field_definition.get("mode")
		if (mode is not None): self.set_mode(self.__class__.get_mode_int(mode))
	#

	def render(self):
	#
		"""
Renders the given field.

:return: (str) Valid XHTML form field definition
:since:  v0.1.01
		"""

		context = { "type": Formatting.escape(self.get_type()),
		            "id": "pas_{0}".format(Formatting.escape(self.get_id())),
		            "name": Formatting.escape(self.name),
		            "title": Formatting.escape(self.get_title()),
		            "placeholder": Formatting.escape(self.get_placeholder()),
		            "value": self._get_content(),
		            "required": self.required,
		            "error_message": ("" if (self.error_data is None) else Formatting.escape(self.get_error_message()))
		          }

		if (self.size == TextField.SIZE_SMALL):
		#
			context['size'] = 10
			context['size_percentage'] = "30%"
		#
		elif (self.size == TextField.SIZE_LARGE):
		#
			context['size'] = 26
			context['size_percentage'] = "80%"
		#
		else:
		#
			context['size'] = 18
			context['size_percentage'] = "55%"
		#

		return self._render_oset_file("core/form/password", context)
	#

	def _set_form_value(self, form):
	#
		"""
Sets the field value based on the given form.

:param form: Form

:since: v0.1.01
		"""

		TextField._set_form_value(self, form)

		repetition_name = "{0}_repetition".format(self.name)

		value = form.get_input(repetition_name)

		if (self.mode & PasswordField.PASSWORD_CLEARTEXT != PasswordField.PASSWORD_CLEARTEXT): value = self._encrypt_value(value)
		self.repetition_value = value
	#

	def set_mode(self, mode):
	#
		"""
Sets the password field mode.

:param mode: Password field mode

:since: v0.1.01
		"""

		if (type(mode) is not int): mode = self.__class__.get_mode_int(mode)
		self.mode = mode
	#

	def set_value(self, value):
	#
		"""
Sets the field value.

:param value: Field value

:since: v0.1.01
		"""

		self.raw_value = value

		if (self.mode & PasswordField.PASSWORD_CLEARTEXT != PasswordField.PASSWORD_CLEARTEXT): value = self._encrypt_value(value)
		self.value = value

		self.valid = None
	#

	@staticmethod
	def get_mode_int(mode):
	#
		"""
Parses the given password mode parameter given as a string value.

:param mode: String mode

:return: (int) Internal mode
:since:  v0.1.01
		"""

		_return = 0

		mode_set = mode.split("+")

		for mode in mode_set:
		#
			if (mode == "cleartext"): _return |= PasswordField.PASSWORD_CLEARTEXT
			elif (mode == "md5"): _return |= PasswordField.PASSWORD_MD5
			elif (mode == "repetition"): _return |= PasswordField.PASSWORD_WITH_REPETITION
		#

		return _return
	#
#

##j## EOF