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

from calendar import timegm
from time import gmtime, strftime, strptime

from dNG.pas.data.binary import Binary
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.xhtml.formatting import Formatting
from dNG.pas.runtime.value_exception import ValueException
from .abstract_field import AbstractField
from .placeholder_mixin import PlaceholderMixin

class AbstractDateTimeField(PlaceholderMixin, AbstractField):
#
	"""
"AbstractDateTimeField" provides common methods for date and time input
fields.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.03
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	TYPE_YEAR = 1
	"""
Input type flag for years
	"""
	TYPE_MONTH = 2
	"""
Input type flag for months
	"""
	TYPE_WEEK = 4
	"""
Input type flag for week numbers (W__)
	"""
	TYPE_DAY = 8
	"""
Input type flag for days
	"""
	TYPE_DATE = 11
	"""
Input type flag for years, month and days
	"""
	TYPE_TIME = 16
	"""
Input type flag for times
	"""

	def __init__(self, name = None):
	#
		"""
Constructor __init__(AbstractDateTimeField)

:param name: Form field name

:since: v0.1.03
		"""

		AbstractField.__init__(self, name)
		PlaceholderMixin.__init__(self)

		self.input_type_flags = 0
		"""
Input type flags defined for this field.
		"""
		self.parsed_time_struct = None
		"""
Value based Python "time_struct"
		"""
	#

	def _check(self):
	#
		"""
Executes checks if the field value is valid.

:return: (bool) True if all checks are passed
:since:  v0.1.03
		"""

		_return = AbstractField._check(self)
		if (_return): _return = self._check_format()

		return _return
	#

	def _check_format(self):
	#
		"""
Checks the format of value.

:return: (bool) True if all checks are passed
:since:  v0.1.00
		"""

		data_length = (0 if (self.value is None) else len(self.value))
		error_data = None

		if (self.required and data_length < 1): error_data = "required_element"
		else:
		#
			try: self._parse_value()
			except ValueException: error_data = "format_invalid"
		#

		if (error_data is None
		    and (self.limit_min is not None or self.limit_max is not None)
		   ):
		#
			timestamp = self.get_timestamp()

			if (self.limit_min is not None and self.limit_min > timestamp): error_data = ( "date_time_min", str(self.limit_min) )
			elif (self.limit_max is not None and self.limit_max < timestamp): error_data = ( "date_time_max", str(self.limit_max) )
		#

		if (error_data is not None): self.error_data = error_data
		return (error_data is None)
	#

	def get_format(self):
	#
		"""

:since: v0.1.03
		"""

		_return = ("%Y"
		           if (self.input_type_flags & AbstractDateTimeField.TYPE_YEAR == AbstractDateTimeField.TYPE_YEAR) else
		           ""
		          )

		if (self.input_type_flags & AbstractDateTimeField.TYPE_MONTH == AbstractDateTimeField.TYPE_MONTH):
		#
			if (_return != ""): _return += "-"
			_return += "%m"
		#

		if (self.input_type_flags & AbstractDateTimeField.TYPE_DAY == AbstractDateTimeField.TYPE_DAY):
		#
			_return += "-%d"
		#

		if (self.input_type_flags & AbstractDateTimeField.TYPE_WEEK == AbstractDateTimeField.TYPE_WEEK):
		#
			if (_return != ""): _return += "-"
			_return += "W%W"
		#

		if (self.input_type_flags & AbstractDateTimeField.TYPE_TIME == AbstractDateTimeField.TYPE_TIME):
		#
			if (_return != ""): _return += "T"
			_return += "%H:%M:%S"
		#

		return _return
	#

	def get_format_placeholder(self):
	#
		"""

:since: v0.1.03
		"""

		_return = ""

		if (self.input_type_flags & AbstractDateTimeField.TYPE_YEAR == AbstractDateTimeField.TYPE_YEAR):
		#
			_return = L10n.get("pas_http_core_form_date_time_placeholder_year")
		#

		if (self.input_type_flags & AbstractDateTimeField.TYPE_MONTH == AbstractDateTimeField.TYPE_MONTH):
		#
			if (_return != ""): _return += "-"
			_return += L10n.get("pas_http_core_form_date_time_placeholder_month")
		#

		if (self.input_type_flags & AbstractDateTimeField.TYPE_DAY == AbstractDateTimeField.TYPE_DAY):
		#
			_return += "-{0}".format(L10n.get("pas_http_core_form_date_time_placeholder_day"))
		#

		if (self.input_type_flags & AbstractDateTimeField.TYPE_WEEK == AbstractDateTimeField.TYPE_WEEK):
		#
			if (_return != ""): _return += "-"
			_return += "W{0}".format(L10n.get("pas_http_core_form_date_time_placeholder_week"))
		#

		if (self.input_type_flags & AbstractDateTimeField.TYPE_TIME == AbstractDateTimeField.TYPE_TIME):
		#
			if (_return != ""): _return += "T"

			_return += "{0}:{1}:{2}".format(L10n.get("pas_http_core_form_date_time_placeholder_hours"),
			                                       L10n.get("pas_http_core_form_date_time_placeholder_minutes"),
			                                       L10n.get("pas_http_core_form_date_time_placeholder_seconds")
			                                      )
		#

		return _return
	#

	def _get_render_context(self):
	#
		"""
Returns the context used for rendering the given field.

:return: (dict) Renderer context
:since:  v0.1.03
		"""

		placeholder = Formatting.escape(self.get_format_placeholder()
		                                if (self.placeholder is None) else
		                                self.get_placeholder()
		                               )

		return { "type": Formatting.escape(self.get_type()),
		         "id": "pas_{0}".format(Formatting.escape(self.get_id())),
		         "name": Formatting.escape(self.name),
		         "title": Formatting.escape(self.get_title()),
		         "placeholder": placeholder,
		         "value": self._get_content(),
		         "required": self.required,
		         "error_message": ("" if (self.error_data is None) else Formatting.escape(self.get_error_message()))
		       }
	#

	def get_timestamp(self):
	#
		"""
Returns the field value as an UNIX timestamp without timezone offset.

:return: (int) UNIX timestamp
:since:  v0.1.03
		"""

		if (self.parsed_time_struct is None): self._parse_value()
		return timegm(self.parsed_time_struct)
	#

	def get_value(self, _raw_input = False):
	#
		"""
Returns the field value given or transmitted.

:param raw_input: True to return the raw (transmitted) value.

:return: (mixed) Field value; None on error
:since:  v0.1.03
		"""

		if (_raw_input): _return = self.value
		else: _return = self.get_timestamp()

		return _return
	#

	def _parse_value(self):
	#
		"""
Parses the raw value.

:since: v0.1.00
		"""

		if (self.input_type_flags < 1): raise ValueException("Input type flags are not set")

		data_length = (0 if (self.value is None) else len(self.value))
		if (data_length < 1): raise ValueException("No data has been provided")

		try: self.parsed_time_struct = strptime(self.value, self.get_format())
		except ValueError as handled_exception: raise ValueException("Value given does not contain the format specified", _exception = handled_exception)
	#

	def render(self):
	#
		"""
Renders the given field.

:return: (str) Valid XHTML form field definition
:since:  v0.1.03
		"""

		return self._render_oset_file("core/form/text", self._get_render_context())
	#

	def set_value(self, value):
	#
		"""
Sets the field value.

:param value: Field value

:since: v0.1.03
		"""

		value = (strftime(self.get_format(), gmtime(value))
		         if (type(value) in ( float, int )) else
		         Binary.str(value)
		        )

		if (not isinstance(value, str)):
		#
			value = Binary.str(value)
			if (type(value) is not str): value = str(value)
		#

		self.value = value

		self.valid = None
	#
#

##j## EOF