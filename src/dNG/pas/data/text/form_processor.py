# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.FormProcessor
"""
"""n// NOTE
----------------------------------------------------------------------------
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
----------------------------------------------------------------------------
NOTE_END //n"""

from binascii import hexlify
from copy import copy
from os import urandom

from dNG.pas.data.binary import Binary
from dNG.pas.data.cached_file import CachedFile
from dNG.pas.runtime.type_exception import TypeException
from dNG.pas.runtime.value_exception import ValueException
from .input_filter import InputFilter
from .link import Link
from .l10n import L10n
from .md5 import Md5

class FormProcessor(object):
#
	"""
"FormProcessor" provides basic form methods used in protocol / format
specific form instances.

@TODO: Support a generic way for external field definition classes derived
from a interface with "add_instance()".

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	# pylint: disable=unused-argument

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
	SPECIAL_FIELD_TYPES = [ "element",
	                        "embed",
	                        "formtags_file",
	                        "hidden",
	                        "info",
	                        "password",
	                        "spacer",
	                        "subtitle"
	                      ]
	"""
Special field types handled by "_set_special_field_entry()"
	"""

	def __init__(self):
	#
		"""
Constructor __init__(FormProcessor)

:since: v0.1.00
		"""

		self.cache = [ ]
		"""
List of form elements
		"""
		self.cache_sections = { }
		"""
List of section positions in the cache
		"""
		self.element_counter = 0
		"""
Nameless form elements counter
		"""
		self.form_has_input = False
		"""
Can be set to true using "set_input_available()"
		"""
		self.form_is_valid = None
		"""
Form validity check result variable
		"""

		L10n.init("pas_http_core_form")
	#

	def check(self, force = False):
	#
		"""
Parses all previously defined form fields and checks them.

:return: (bool) True if all checks are passed
:since:  v0.1.00
		"""

		_return = (self.form_is_valid if (self.form_is_valid != None) else True)

		if (len(self.cache) > 0 and (force or self.form_is_valid == None)):
		#
			for section in self.cache:
			#
				for field_data in section['fields']:
				#
					if (field_data['error'] != None):
					#
						_return = False
						break
					#
				#

				if (not _return): break
			#
		#

		self.form_is_valid = _return
		return _return
	#

	def add_email(self, field_data):
	#
		"""
A single line text input field for eMail addresses.

:param field_data: Form field data

:return: (bool) False if the content was not accepted
:since:  v0.1.00
		"""

		field_data = self._set_entry_defaults(field_data)
		field_data = self._set_entry_field_size(field_data)
		field_data = self._set_entry_limits(field_data)

		field_data['error'] = self._check_entry_length(field_data['content'], field_data['min'], field_data['max'], field_data['required'])

		if (field_data['error'] == None
		    and len(field_data['content']) > 0
		    and InputFilter.filter_email_address(field_data['content']) == ""
		   ): field_data['error'] = "format_invalid"

		if (field_data['error'] == None): field_data['error'] = self._check_validators(field_data)

		self._set_entry("email", field_data)
		return (field_data['error'] == None)
	#

	def add_embedded(self, field_data, url_parameters, is_iframe_only = False):
	#
		"""
Embeds external resources into the current form.

:param field_data: Form field data
:param url_parameters: URL parameters for the embedded resource
:param is_iframe_only: True if we should not try AJAX to embed the given URL

:return: (bool) Currently always true
:since:  v0.1.00
		"""

		field_data = self._set_entry_defaults(field_data)
		field_data = self._set_entry_field_size(field_data)

		if (len(field_data['content']) < 1): field_data['content'] = Binary.str(hexlify(urandom(10)))

		field_data['iframe_only'] = is_iframe_only
		url_parameters['tid'] = field_data['content']

		field_data['url'] = Link().build_url(Link.TYPE_RELATIVE, url_parameters)

		self._set_entry("embed", field_data)
		return True
	#

	def add_entry(self, field_type, field_data = None):
	#
		"""
Creates spacing fields like "hidden", "element", "info", "spacer" or "subtitle".

:param field_type: Form field type
:param field_data: Form field data

:link: http://www.direct-netware.de/redirect.py?handbooks;pas;http;dev;formbuilder
       Click here to get a list of available form fields

:return: (bool) True if no error occured
:since:  v0.1.00
		"""

		if (field_data['type'] == "element"
		    or field_data['type'] == "hidden"
		    or field_data['type'] == "info"
		    or field_data['type'] == "spacer"
		    or field_data['type'] == "subtitle"
		   ):
		#
			if (field_data == None): field_data = { }
			field_data = self._set_entry_defaults(field_data, None, None, None)
			self._set_entry(field_type, field_data)

			_return = True
		#
		else: _return = False

		return _return
	#

	def add_formtags_file(self, field_data, file_pathname):
	#
		"""
Adds a preformatted text from an external file.

:param field_data: Form field data
:param file_pathname: Path to the FormTags file

:return: (bool) False if the file path is invalid
:since:  v0.1.01
		"""

		_return = True

		content = CachedFile.read(file_pathname)
		if (content == None): _return = False

		field_data = self._set_entry_defaults(field_data, content = content)
		field_data = self._set_entry_field_size(field_data, "s")
		self._set_entry("formtags_file", field_data)

		return _return
	#

	def add_multiselect(self, field_data):
	#
		"""
Inserts a selectbox for multiple selectable options.

:param field_data: Form field data

:return: (bool) False if the content was not accepted
:since:  v0.1.00
		"""

		field_data = self._set_entry_defaults(field_data, content = None)
		field_data = self._set_entry_field_size(field_data, "s")

		if ("choices" not in field_data or type(field_data['choices']) != list): field_data['error'] = "internal_error"
		else:
		#
			if (field_data['content'] == None): field_data['content'] = [ ]
			elif (type(field_data['content']) == str): field_data['content'] = [ field_data['content'] ]

			field_data['content_result'] = [ ]

			for choice in field_data['choices']:
			#
				if ("id" not in choice):
				#
					choice['id'] = "pas_http_form_{0:d}".format(self.element_counter)
					self.element_counter += 1
				#

				if ("value" in choice and choice['value'] in field_data['content']):
				#
					choice['selected'] = True
					field_data['content_result'].append(choice['value'])
				#
			#

			if (field_data['required'] and len(field_data['content_result']) < 1): field_data['error'] = "required_element"
		#

		if (field_data['error'] == None): field_data['error'] = self._check_validators(field_data)

		self._set_entry("multiselect", field_data)
		return (field_data['error'] == None)
	#

	def add_number(self, field_data):
	#
		"""
A number (integer) input field.

:param field_data: Form field data

:return: (bool) False if the content was not accepted
:since:  v0.1.00
		"""

		field_data = self._set_entry_defaults(field_data, content = None)
		field_data = self._set_entry_field_size(field_data)
		field_data = self._set_entry_limits(field_data)

		field_data['error'] = self._check_entry_range(field_data['content'], field_data['min'], field_data['max'], field_data['required'])
		if (field_data['error'] == None): field_data['error'] = self._check_validators(field_data)

		self._set_entry("number", field_data)
		return (field_data['error'] == None)
	#

	def add_password(self, field_data, mode = None):
	#
		"""
Insert passwords (including optional a repetition check)

:param field_data: Form field data
:param mode: Password and encryption mode (MD5 if undefined)

:return: (bool) False if the content was not accepted
:since:  v0.1.00
		"""

		_return = True

		field_data = self._set_entry_defaults(field_data)
		field_data = self._set_entry_field_size(field_data)
		field_data = self._set_entry_limits(field_data)

		field_data['error'] = self._check_entry_length(field_data['content'], field_data['min'], field_data['max'], field_data['required'])

		if (mode == None): mode = FormProcessor.PASSWORD_MD5

		if (mode & FormProcessor.PASSWORD_WITH_REPETITION == FormProcessor.PASSWORD_WITH_REPETITION):
		#
			repetition_name = "{0}_repetition".format(field_data['name'])
			repetition_content = self.get_input(repetition_name)

			if (field_data['content'] != repetition_content): field_data['error'] = "password_repetition"
			_type = "password_with_repetition"
		#
		else: _type = "password"

		if (field_data['error'] == None): field_data['error'] = self._check_validators(field_data)

		if (field_data['error'] != None): _return = False
		elif (mode & FormProcessor.PASSWORD_MD5 == FormProcessor.PASSWORD_MD5): field_data['content_result'] = Md5.hash(field_data['content'])

		self._set_entry(_type, field_data)
		return _return
	#

	def add_radio(self, field_data):
	#
		"""
Inserts radio fields for exact one selected option.

:param field_data: Form field data

:return: (bool) False if the content was not accepted
:since:  v0.1.00
		"""

		field_data = self._set_entry_defaults(field_data, content = None)

		if ("choices" not in field_data or type(field_data['choices']) != list): field_data['error'] = "internal_error"
		else:
		#
			field_data['content_result'] = None

			for choice in field_data['choices']:
			#
				if ("id" not in choice):
				#
					choice['id'] = "pas_http_form_{0:d}".format(self.element_counter)
					self.element_counter += 1
				#

				if ("value" in choice and field_data['content'] == choice['value']):
				#
					choice['selected'] = True
					field_data['content_result'] = choice['value']
				#
			#

			if (field_data['required'] and field_data['content_result'] == None): field_data['error'] = "required_element"
		#

		if (field_data['error'] == None): field_data['error'] = self._check_validators(field_data)

		self._set_entry("radio", field_data)
		return (field_data['error'] == None)
	#

	def add_range(self, field_data):
	#
		"""
A range input field between including minimum (default 0) and maximum
(default 100) values.

:param field_data: Form field data

:return: (bool) False if the content was not accepted
:since:  v0.1.00
		"""

		field_data = self._set_entry_defaults(field_data, content = None)
		field_data = self._set_entry_field_size(field_data, "s")
		field_data = self._set_entry_limits(field_data, 0, 100)

		field_data['error'] = self._check_entry_range(field_data['content'], field_data['min'], field_data['max'], field_data['required'])
		if (field_data['error'] == None): field_data['error'] = self._check_validators(field_data)

		self._set_entry("number", field_data)
		return (field_data['error'] == None)
	#

	def add_select(self, field_data):
	#
		"""
Inserts a selectbox for exact one selected option.

:param field_data: Form field data

:return: (bool) False if the content was not accepted
:since:  v0.1.00
		"""

		field_data = self._set_entry_defaults(field_data, content = None)
		field_data = self._set_entry_field_size(field_data, "s")

		if ("choices" not in field_data or type(field_data['choices']) != list): field_data['error'] = "internal_error"
		else:
		#
			if (field_data['content'] == None): field_data['content'] = [ ]
			elif (type(field_data['content']) == str): field_data['content'] = [ field_data['content'] ]

			field_data['content_result'] = ""

			for choice in field_data['choices']:
			#
				if ("id" not in choice):
				#
					choice['id'] = "pas_http_form_{0:d}".format(self.element_counter)
					self.element_counter += 1
				#

				if ("value" in choice and choice['value'] in field_data['content']):
				#
					choice['selected'] = True
					field_data['content_result'] = choice['value']
				#
			#

			if (field_data['required'] and len(field_data['content']) < 1): field_data['error'] = "required_element"
		#

		if (field_data['error'] == None): field_data['error'] = self._check_validators(field_data)

		self._set_entry("select", field_data)
		return (field_data['error'] == None)
	#

	def add_text(self, field_data):
	#
		"""
A single line text input field.

:param field_data: Form field data

:return: (bool) False if the content was not accepted
:since:  v0.1.00
		"""

		field_data = self._set_entry_defaults(field_data)
		field_data = self._set_entry_field_size(field_data)
		field_data = self._set_entry_limits(field_data)

		field_data['error'] = self._check_entry_length(field_data['content'], field_data['min'], field_data['max'], field_data['required'])
		if (field_data['error'] == None): field_data['error'] = self._check_validators(field_data)

		self._set_entry("text", field_data)
		return (field_data['error'] == None)
	#

	def add_textarea(self, field_data):
	#
		"""
A multi line textarea input field.

:param field_data: Form field data

:return: (bool) False if the content was not accepted
:since:  v0.1.00
		"""

		field_data = self._set_entry_defaults(field_data)
		field_data = self._set_entry_field_size(field_data)
		field_data = self._set_entry_limits(field_data)

		field_data['error'] = self._check_entry_length(field_data['content'], field_data['min'], field_data['max'], field_data['required'])
		if (field_data['error'] == None): field_data['error'] = self._check_validators(field_data)

		self._set_entry("textarea", field_data)
		return (field_data['error'] == None)
	#

	def _check_entry_length(self, data, _min = None, _max = None, required = False):
	#
		"""
Checks the size for a given string.

:param data: The string that should be checked
:param _min: Defines the minimal length for a string or None to ignore
:param _max: Defines the maximal length for a string or None for an unlimited
            size
:param required: True if the field is required to continue

:return: (mixed) Error definition; None if valid
:since:  v0.1.00
		"""

		data_length = (0 if (data == None) else len(data))

		if (required and data_length < 1): _return = "required_element"
		elif (_min != None and _min > data_length): _return = ( "string_min", str(_min) )
		elif (_max != None and _max < data_length): _return = ( "string_max", str(_max) )
		else: _return = None

		return _return
	#

	def _check_entry_range(self, data, _min = None, _max = None, required = False):
	#
		"""
Checks the size for a given string.

:param data: The string that should be checked
:param _min: Defines the minimal range for a number or None to ignore
:param _max: Defines the maximal range for a number or None for an unlimited
            size
:param required: True if the field is required to continue

:return: (mixed) Error definition; None if valid
:since:  v0.1.00
		"""

		_return = None

		if (data != None and len(data) > 0):
		#
			number = InputFilter.filter_float(data)

			if (number != None):
			#
				if (_min != None and _min > number): _return = ( "number_min", str(_min) )
				elif (_max != None and _max < number): _return = ( "number_max", str(_max) )
			#
			else: _return = "format_invalid"
		#
		elif (required): _return = "required_element"

		return _return
	#

	def _check_validators(self, field_data):
	#
		"""
Checks for validator callbacks, executes them and returns the first error
occuring.

:param data: The string that should be checked
:param _min: Defines the minimal range for a number or None to ignore
:param _max: Defines the maximal range for a number or None for an unlimited
            size
:param required: True if the field is required to continue

:return: (mixed) Error definition tuple; None if valid
:since:  v0.1.00
		"""

		_return = None

		if (isinstance(field_data.get("validators"), list)):
		#
			for _callable in field_data.get("validators"):
			#
				result = _callable(field_data)

				if (result != None):
				#
					_return = ( "validator_failed", result )
					break
				#
			#
		#

		return _return
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

		if (self.form_is_valid == None or (not self.form_has_input)):
		#
			for section in _return:
			#
				for field_data in section['fields']: field_data['error'] = None
			#
		#

		if (flush):
		#
			self.cache = [ ]
			self.cache_sections = { }
			self.element_counter = 0
			self.form_has_input = False
			self.form_is_valid = None
		#

		return _return
	#

	def _get_error_message(self, error_data):
	#
		"""
Returns the error message for the error data given. Returned message is
implementation specific.

:param error_data: Field error data

:return: (str) Implementation specific error message
:since:  v0.1.00
		"""

		error = (error_data[0] if (type(error_data) == tuple) else error_data)

		if (error == "number_max"):
		#
			_return = "{0}{1}{2}".format(L10n.get("pas_http_core_form_error_number_max_1"),
			                             error_data[1],
			                             L10n.get("pas_http_core_form_error_number_max_2")
			                            )
		#
		elif (error == "number_min"):
		#
			_return = "{0}{1}{2}".format(L10n.get("pas_http_core_form_error_number_min_1"),
			                             error_data[1],
			                             L10n.get("pas_http_core_form_error_number_min_2")
			                            )
		#
		elif (error == "string_max"):
		#
			_return = "{0}{1}{2}".format(L10n.get("pas_http_core_form_error_string_max_1"),
			                             error_data[1],
			                             L10n.get("pas_http_core_form_error_string_max_2")
			                            )
		#
		elif (error == "string_min"):
		#
			_return = "{0}{1}{2}".format(L10n.get("pas_http_core_form_error_string_min_1"),
			                             error_data[1],
			                             L10n.get("pas_http_core_form_error_string_min_2")
			                            )
		#
		elif (error == "validator_failed"): _return = error_data[1]
		else: _return = L10n.get("pas_http_core_form_error_{0}".format(error))

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

		if (section == None): sections = self.cache_sections
		else: sections = ([ self.cache_sections[section] ] if (section in self.cache_sections) else None)

		if (type(types_hidden) == list): types_hidden = [ "hidden", "info", "subtitle" ]
		else: types_hidden += [ "hidden", "info", "subtitle" ]

		if (sections != None):
		#
			for section in sections:
			#
				for field_data in section['fields']:
				#
					if (field_data['error'] != None): _return.append({ "name": field_data['name'], "error_data": field_data['error'], "error_message": self._get_error_message(field_data['error']) })
				#
			#
		#

		return _return
	#

	def get_input(self, name):
	#
		"""
"get_input()" should be used to read the input value for the field from a
source (e.g. from a HTTP POST request parameter).

:param name: Field and parameter name

:return: (mixed) Value; None if not set
:since:  v0.1.00
		"""

		return None
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

		if (section == None): sections = self.cache
		else: sections = ([ self.cache[self.cache_sections[section]] ] if (section in self.cache_sections) else [ ])

		for section in sections:
		#
			if (name in section['positions']):
			#
				field = section['fields'][section['positions'][name]]
				_return = (field['content_result'] if ("content_result" in field and (not _raw_input)) else field['content'])
				break
			#
		#

		return _return
	#

	def set_data(self, data):
	#
		"""
Set the fields based on the given list.

:param data: Field data list

:since: v0.1.00
		"""

		if (isinstance(data, list)):
		#
			self.cache = [ ]
			self.cache_sections = { }

			for field_data in data: self._set_entry_field(field_data)
		#
		else: raise TypeException("Given data does not reflect a form list")
	#

	def _set_entry(self, field_type, field_data):
	#
		"""
Adds a new field entry to the list.

:param field_type: Form field type
:param field_data: Form field data

:link: http://www.direct-netware.de/redirect.py?handbooks;pas;http;dev;formbuilder
       Click here to get a list of available form fields

:since: v0.1.00
		"""

		if (isinstance(field_data, dict)):
		#
			field_data['type'] = field_type

			if (len(field_data['name']) > 0): name = field_data['name']
			else: name = Binary.str(hexlify(urandom(10)))

			if (field_data['section'] not in self.cache_sections):
			#
				position = len(self.cache)
				section = { "fields": [ ], "name": field_data['section'], "positions": { } }

				self.cache.append(section)
				self.cache_sections[field_data['section']] = position
			#

			cache = self.cache[self.cache_sections[field_data['section']]]

			if (name in cache['positions']): self.update_entry(field_data['section'], name, field_data)
			else:
			#
				position = len(cache['fields'])

				cache['fields'].append(field_data)
				cache['positions'][name] = position

				self.form_is_valid = None
			#
		#
	#

	def _set_entry_defaults(self, field_data, name = "", title = "", content = "", required = False):
	#
		"""
Sets default values for the given field.

:param field_data: Form field data
:param name: Internal name of the form field
:param title: Public title for the form field
:param content: Form field related content data
:param required: True if the field is required to continue

:return: (dict) Changed field data; None on error
:since:  v0.1.00
		"""

		if (isinstance(field_data, dict)):
		#
			_return = field_data
			if ("section" not in field_data): field_data['section'] = ""

			if ("id" not in field_data):
			#
				field_data['id'] = "pas_http_form_{0:d}".format(self.element_counter)
				self.element_counter += 1
			#

			if ("name" not in field_data): field_data['name'] = name
			if ("title" not in field_data): field_data['title'] = title

			if (self.form_has_input or "content" not in field_data):
			#
				input_content = (self.get_input(field_data['name']) if (field_data['name'] != "") else None)
				field_data['content'] = (content if (input_content == None) else input_content)
			#

			if ("required" not in field_data): field_data['required'] = required
			if ("error" not in field_data): field_data['error'] = None
			if ("helper_content" not in field_data): field_data['helper_content'] = ""
			if ("helper_url" not in field_data): field_data['helper_url'] = ""
		#
		else: _return = None

		return _return
	#

	def set_entry_error(self, section, name, error):
	#
		"""
Set an external error message for the given form field.

:param section: Form section
:param name: Field name
:param error: Error message definition

:since: v0.1.00
		"""

		_type = type(error)
		if (_type == str or _type == tuple): self.update_entry(section, name, { "error": error })
	#

	def _set_entry_field_size(self, field_data, size = "m"):
	#
		"""
Sets the default requested size for the given field if not already defined.

:param field_data: Form field data
:param size: "s" = small, "m" = medium, "l" = large

:return: (dict) Changed field data; None on error
:since:  v0.1.00
		"""

		if (isinstance(field_data, dict)):
		#
			_return = field_data
			if ("size" not in field_data): field_data['size'] = size
		#
		else: _return = None

		return _return
	#

	def _set_entry_limits(self, field_data, _min = None, _max = None):
	#
		"""
Sets default limits for the given field if they are not already defined.

:param field_data: Form field data
:param _min: Minimum range of a number or length of a string
:param _max: Maximum range of a number or length of a string

:return: (dict) Changed field data; None on error
:since:  v0.1.00
		"""

		if (isinstance(field_data, dict)):
		#
			_return = field_data
			if ("min" not in field_data): field_data['min'] = _min
			if ("max" not in field_data): field_data['max'] = _max
		#
		else: _return = None

		return _return
	#

	def _set_entry_field(self, field_data):
	#
		"""
Sets an field entry based on the data given.

:param field_data: Form field data

:since: v0.1.00
		"""

		if (isinstance(field_data, dict) and "type" in field_data):
		#
			if (field_data['type'] in FormProcessor.SPECIAL_FIELD_TYPES): self._set_special_field_entry(field_data)
			else:
			#
				if (not hasattr(self, "add_{0}".format(field_data['type']))): raise ValueException("Given field type is not defined")
				method = getattr(self, "add_{0}".format(field_data['type']))
				method(field_data)
			#
		#
		else: raise TypeException("Given data does not reflect a form field")
	#

	def set_input_available(self):
	#
		"""
Sets the flag for available input. Input values can be read with
"get_input()".

:since: v0.1.00
		"""

		self.form_has_input = True
	#

	def _set_special_field_entry(self, field_data):
	#
		"""
Handles special field types defined by "SPECIAL_FIELD_TYPES".

:param field_data: Form field data

:since: v0.1.00
		"""

		if (isinstance(field_data, dict)
		    and "type" in field_data
		    and field_data['type'] in FormProcessor.SPECIAL_FIELD_TYPES
		   ):
		#
			if (field_data['type'] == "element"
			    or field_data['type'] == "hidden"
			    or field_data['type'] == "info"
			    or field_data['type'] == "spacer"
			    or field_data['type'] == "subtitle"
			   ): self.add_entry(field_data['type'], field_data)
			elif (field_data['type'] == "embed"):
			#
				if ("url_parameters" not in field_data): raise ValueException("Given field type is not defined correctly")

				is_iframe_only = field_data.get("is_iframe_only", False)
				self.add_embedded(field_data, field_data['url_parameters'], is_iframe_only)
			#
			elif (field_data['type'] == "formtags_file"):
			#
				if ("file_pathname" not in field_data): raise ValueException("Given field type is not defined correctly")
				self.add_formtags_file(field_data, field_data['file_pathname'])
			#
			elif (field_data['type'] == "password"):
			#
				mode = field_data.get("mode")
				self.add_password(field_data, mode)
			#
			else: raise ValueException("Given field type is not defined")
		#
		else: raise TypeException("Given data does not reflect a form field")
	#

	def update_entry(self, section, name, field_data):
	#
		"""
Updates existing field entries.

:param section: Form section
:param name: Field name
:param field_data: Form field data

:since: v0.1.00
		"""

		if (isinstance(field_data, dict) and section in self.cache_sections):
		#
			section_position = self.cache_sections[section]

			if (name in self.cache[section_position]['positions']):
			#
				field_position = self.cache[section_position]['positions'][name]
				self.cache[section_position]['fields'][field_position].update(field_data)
			#

			self.form_is_valid = None
		#
	#
#

##j## EOF