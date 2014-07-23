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

from dNG.pas.data.binary import Binary
from dNG.pas.data.text.input_filter import InputFilter
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.xhtml.oset.file_parser import FileParser
from dNG.pas.runtime.not_implemented_exception import NotImplementedException
from dNG.pas.runtime.type_exception import TypeException

class AbstractField(object):
#
	"""
"AbstractField" defines basic methods used by the form processor.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	SIZE_SMALL = "s"
	"""
Small field size
	"""
	SIZE_MEDIUM = "m"
	"""
Medium field size
	"""
	SIZE_LARGE = "l"
	"""
Large field size
	"""

	def __init__(self, name = None):
	#
		"""
Constructor __init__(AbstractField)

:param name: Form field name

:since: v0.1.01
		"""

		self.form_context = { }
		"""
Form context
		"""
		self.error_data = None
		"""
Field error data
		"""
		self.id = None
		"""
Field ID
		"""
		self.limit_max = None
		"""
Field value maximum
		"""
		self.limit_min = None
		"""
Field value minimum
		"""
		self.name = name
		"""
Field name
		"""
		self.oset = None
		"""
OSet requested
		"""
		self.required = False
		"""
True if the field is required
		"""
		self.size = AbstractField.SIZE_MEDIUM
		"""
Field size
		"""
		self.title = None
		"""
Field title
		"""
		self.valid = None
		"""
True if the field check has been passed
		"""
		self.validators = [ ]
		"""
List of custom validators that must be passed
		"""
		self.value = None
		"""
Field value
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

		self.valid = (self.valid if (self.valid != None) else (self.error_data == None))
		if (self.valid): self.valid = self._check_validators()

		return self.valid
	#

	def _check_length(self):
	#
		"""
Checks the length of value.

:return: (bool) True if all checks are passed
:since:  v0.1.00
		"""

		data_length = (0 if (self.value == None) else len(self.value))
		error_data = None

		if (self.required and data_length < 1): error_data = "required_element"
		elif (self.limit_min != None
		      and (self.required or data_length > 0)
		      and self.limit_min > data_length
		     ): error_data = ( "string_min", str(self.limit_min) )
		elif (self.limit_max != None and self.limit_max < data_length): error_data = ( "string_max", str(self.limit_max) )

		if (error_data != None): self.error_data = error_data
		return (error_data == None)
	#

	def _check_range(self):
	#
		"""
Checks the range of value.

:return: (bool) True if all checks are passed
:since:  v0.1.00
		"""

		error_data = None

		if (self.value != None and len(self.value) > 0):
		#
			number = InputFilter.filter_float(self.value)

			if (number != None):
			#
				if (self.limit_min != None and self.limit_min > number): error_data = ( "number_min", str(self.limit_min) )
				elif (self.limit_max != None and self.limit_max < number): error_data = ( "number_max", str(self.limit_max) )
			#
			else: error_data = "format_invalid"
		#
		elif (self.required): error_data = "required_element"

		if (error_data != None): self.error_data = error_data
		return (error_data == None)
	#

	def _check_validators(self):
	#
		"""
Checks for validator callbacks, executes them and exits on the first error.

:return: (bool) True if all validators are passed
:since:  v0.1.01
		"""

		_return = True

		for _callable in self.validators:
		#
			result = _callable(self, self.form_context)

			if (result != None):
			#
				_return = False

				self.error_data = (result
				                   if (type(result) == tuple) else
				                   ( "validator_failed", result )
				                  )

				break
			#
		#

		return _return
	#

	def _get_content(self):
	#
		"""
Returns the field content.

:return: (str) Field content
:since:  v0.1.01
		"""

		_return = ("" if (self.value == None) else Binary.str(self.value))
		if (type(_return) != str): _return = str(_return)

		return _return
	#

	def get_error_data(self):
	#
		"""
Returns the error data.

:return: (mixed) Error data string or tuple; None if valid
:since:  v0.1.01
		"""

		return self.error_data
	#

	def get_error_message(self):
	#
		"""
Returns the error message.

:return: (str) Implementation specific error message; None if valid
:since:  v0.1.01
		"""

		_return = None

		error_type = (self.error_data[0] if (type(self.error_data) == tuple) else self.error_data)

		if (error_type == "number_max"):
		#
			_return = "{0}{1}{2}".format(L10n.get("pas_http_core_form_error_number_max_1"),
			                             self.error_data[1],
			                             L10n.get("pas_http_core_form_error_number_max_2")
			                            )
		#
		elif (error_type == "number_min"):
		#
			_return = "{0}{1}{2}".format(L10n.get("pas_http_core_form_error_number_min_1"),
			                             self.error_data[1],
			                             L10n.get("pas_http_core_form_error_number_min_2")
			                            )
		#
		elif (error_type == "string_max"):
		#
			_return = "{0}{1}{2}".format(L10n.get("pas_http_core_form_error_string_max_1"),
			                             self.error_data[1],
			                             L10n.get("pas_http_core_form_error_string_max_2")
			                            )
		#
		elif (error_type == "string_min"):
		#
			_return = "{0}{1}{2}".format(L10n.get("pas_http_core_form_error_string_min_1"),
			                             self.error_data[1],
			                             L10n.get("pas_http_core_form_error_string_min_2")
			                            )
		#
		elif (error_type == "validator_failed"): _return = self.error_data[1]
		elif (error_type != None): _return = L10n.get("pas_http_core_form_error_{0}".format(error_type))

		return _return
	#

	def get_id(self):
	#
		"""
Returns the field ID.

:return: (str) Field ID
:since:  v0.1.01
		"""

		return self.id
	#

	def get_name(self):
	#
		"""
Returns the field name.

:return: (str) Field name
:since:  v0.1.01
		"""

		return self.name
	#

	def get_size(self):
	#
		"""
Returns the field size.

:return: (str) Field size identifier "s", "m" or "l"
:since:  v0.1.01
		"""

		return self.size
	#

	def get_title(self):
	#
		"""
Returns the field title.

:return: (str) Field title
:since:  v0.1.01
		"""

		return ("" if (self.title == None) else self.title)
	#

	def get_type(self):
	#
		"""
Returns the field type.

:return: (str) Field type
:since:  v0.1.01
		"""

		raise NotImplementedException()
	#

	def get_value(self, _raw_input = False):
	#
		"""
Returns the field value given or transmitted.

:param raw_input: True to return the raw (transmitted) value.

:return: (str) Field value; None on error
:since:  v0.1.01
		"""

		return self.value
	#

	def is_id_set(self):
	#
		"""
Returns true if a field ID has been set.

:return: (bool) True if Field ID has been set
:since: v0.1.01
		"""

		return (self.id != None)
	#

	def is_required(self):
	#
		"""
Returns if this field is required.

:return: (bool) True if required
:since:  v0.1.01
		"""

		return self.valid
	#

	def is_valid(self):
	#
		"""
Returns the validation result.

:return: (bool) True if the last validation was successful
:since:  v0.1.01
		"""

		return self.valid
	#

	def load_definition(self, field_definition):
	#
		"""
Loads the field configuration from the given definition.

:param field_definition: Field definition dict

:since: v0.1.01
		"""

		self._validate_definition(field_definition)

		self.id = field_definition.get("id")
		self.name = field_definition['name']
		self.title = field_definition.get("title")

		value = field_definition.get("content")
		if (value != None): self.set_value(value)

		required = field_definition.get("required", False)
		self.required = (required == True or required == "1")

		_max = field_definition.get("max")
		_min = field_definition.get("min")

		if (_max != None or _min != None): self.set_limits(_min, _max)

		size = field_definition.get("size")
		if (size != None): self.set_size(size)
	#

	def render(self):
	#
		"""
Renders the given field.

:return: (str) Valid XHTML form field definition
:since:  v0.1.01
		"""

		raise NotImplementedException()
	#

	def _render_oset_file(self, file_pathname, content):
	#
		"""
Render the form field using the given OSet template.

:param template_name: OSet template name
:param content: Content object

:since: v0.1.00
		"""

		# pylint: disable=broad-except

		parser = FileParser()
		parser.set_oset(self.oset)
		return parser.render(file_pathname, content)
	#

	def _set_form_context(self, context):
	#
		"""
Sets the form context.

:param context: Form context dict

:since: v0.1.01
		"""

		self.form_context = context
	#

	def _set_form_value(self, form):
	#
		"""
Sets the field value based on the given form.

:param form: Form

:since: v0.1.01
		"""

		value = form.get_input(self.name)
		if (value != None): self.set_value(value)
	#

	def set_id(self, _id):
	#
		"""
Sets the field ID.

:param _id: Field ID

:since: v0.1.01
		"""

		self.id = _id
	#

	def set_limits(self, _min = None, _max = None):
	#
		"""
Set field limits. Values are field type specific.

:param _min: Defines the minimal value or None to ignore
:param _max: Defines the maximal value or None for no limit

:since: v0.1.01
		"""

		self.limit_max = _max
		self.limit_min = _min
	#

	def set_name(self, name):
	#
		"""
Sets the field name if not already set.

:param name: Field name

:since: v0.1.01
		"""

		if (self.name == None): self.name = name
	#

	def set_oset(self, oset):
	#
		"""
Sets the OSet to use.

:param oset: OSet requested

:since: v0.1.00
		"""

		self.oset = oset
	#

	def set_required(self):
	#
		"""
Sets this field to be required.

:since: v0.1.01
		"""

		self.required = True
	#

	def set_size(self, size):
	#
		"""
Sets the field size.

:param size: Field size

:since: v0.1.01
		"""

		self.size = size
	#

	def set_title(self, title):
	#
		"""
Sets the field title.

:param title: Field title

:since: v0.1.01
		"""

		self.title = title
	#

	def set_validators(self, validators):
	#
		"""
Sets custom validators to be called during execution of "check()".

:param validators: List of validator callbacks

:since: v0.1.01
		"""

		if (not isinstance(validators, list)): raise TypeException("Given validator list type is invalid")
		self.validators = validators
	#

	def set_value(self, value):
	#
		"""
Sets the field value.

:param value: Field value

:since: v0.1.01
		"""

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

		if (not isinstance(field_definition, dict)): raise TypeException("Given form field definition type is invalid")

		if ("name" not in field_definition): raise TypeException("'name' is missing in the given form field definition")
	#
#

##j## EOF