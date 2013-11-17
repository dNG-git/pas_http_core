# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.InputForm
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

from dNG.pas.data.settings import Settings
from dNG.pas.data.text.md5 import Md5
from dNG.pas.data.text.tmd5 import Tmd5
from dNG.pas.data.text.url import Url

from .input_filter import InputFilter

class InputForm(object):
#
	"""
"InputForm" provides basic form methods used in protocol / format
specific form instances.

TODO: Code incomplete

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
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
	PASSWORD_TMD5 = 4
	"""
Triple encoded MD5 with bytemix
	"""
	PASSWORD_WITH_REPETITION = 8
	"""
Password input repetition
	"""

	def __init__(self):
	#
		"""
Constructor __init__(InputForm)

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

	def entry_add(self, field_type, field_data = { }):
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

		if (field_type == "hidden"or field_type == "element" or field_type == "info" or field_type == "spacer" or field_type == "subtitle"):
		#
			_return = True
			field_data = self._entry_defaults_set(field_data, None, None, None)
			self._entry_set(field_type, field_data)
		#
		else: _return = False

		return _return
	#

	def entry_add_email(self, field_data):
	#
		"""
A single line text input field for eMail addresses.

:param field_data: Form field data

:return: (bool) False if the content was not accepted
:since:  v0.1.00
		"""

		field_data = self._entry_defaults_set(field_data, "", "", None)
		field_data = self._entry_field_size_set(field_data)
		field_data = self._entry_limits_set(field_data)

		field_data['error'] = self._entry_length_check(field_data['content'], field_data['min'], field_data['max'], field_data['required'])
		if (len(field_data['content']) > 0 and InputFilter.filter_email_address(field_data['content']) == None): field_data['error'] = "format_invalid"

		self._entry_set("email", field_data)
		return (field_data['error'] == None)
	#

	def entry_add_embed(self, field_data, url_parameters, is_iframe_only = False):
	#
		"""
Embeds external resources into the current form.

:param field_data: Form field data
:param url_parameters: URL parameters for the embedded resource
:param is_iframe_only: True if we should not try AJAX to embed the given URL

:return: (bool) Currently always true
:since:  v0.1.00
		"""

		field_data = self._entry_defaults_set(field_data, "", "", None)
		field_data = self._entry_field_size_set(field_data)

		if (len(field_data['content']) < 1): field_data['content'] = hexlify(urandom(10))

		field_data['iframe_only'] = is_iframe_only
		url_parameters['tid'] = field_data['content']

		field_data['url'] = Url().build_url(Url.TYPE_RELATIVE, url_parameters)

		self._entry_set("embed", field_data)
		return True
	#

	def entry_add_file_ftg(self, field_data, file_pathname):
	#
		"""
Adds a preformatted text from an external file.

:param field_data: Form field data
:param file_pathname: Path to the FTG file

:return: (bool) Currently always true
:since:  v0.1.00
		"""

		"""$f_file_path = $direct_globals['basic_functions']->varfilter ($f_file_path,"settings");
		$f_return = false;

		if (file_exists ($f_file_path))
		{
			$f_file_data = direct_file_get ("s",$f_file_path);
			$f_file_data = $direct_globals['formtags']->decode (str_replace ("\n","[newline]",$f_file_data));

			$f_return = true;
		}
		else { $f_file_data = (direct_local_get ("formbuilder_error_file_not_found_1")).(direct_html_encode_special ($f_file_path)).(direct_local_get ("formbuilder_error_file_not_found_2")); }

		$f_entry = $this->entryDefaultsSet ($f_entry,"","",$f_file_data);
		$f_entry = $this->entryFieldSizeSet ($f_entry,"s");

		$this->entrySet ("fileFtg",$f_entry);
		return /*#ifdef(DEBUG):direct_debug (7,"sWG/#echo(__FILEPATH__)# -formbuilder->entryAddFileFtg ()- (#echo(__LINE__)#)",:#*/$f_return/*#ifdef(DEBUG):,true):#*/;
		"""
		return False
	#

	def entry_add_multiselect(self, field_data):
	#
		"""
Inserts a selectbox for multiple selectable options.

:param field_data: Form field data

:return: (bool) False if the content was not accepted
:since:  v0.1.00
		"""

		field_data = self._entry_defaults_set(field_data,"" ,"", None)
		field_data = self._entry_field_size_set(field_data, "s")

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

			if (field_data['required'] and len(field_data['content']) < 1): field_data['error'] = "required_element"
		#

		self._entry_set("multiselect", field_data)
		return (field_data['error'] == None)
	#

	def entry_add_password(self, field_data, mode = None, bytemix = ""):
	#
		"""
Insert passwords (including optional a repetition check)

:param field_data: Form field data
:param mode: Password and encryption mode
:param bytemix: Bytemix to use for TMD5 (None for none)

:return: (bool) False if the content was not accepted
:since:  v0.1.00
		"""

		_return = True

		field_data = self._entry_defaults_set(field_data, "", "", None)
		field_data = self._entry_field_size_set(field_data)
		field_data = self._entry_limits_set(field_data)

		field_data['error'] = self._entry_length_check(field_data['content'], field_data['min'], field_data['max'], field_data['required'])

		if (bytemix == None): bytemix = ""
		elif (len(bytemix) < 1): bytemix = Settings.get("pas_user_profile_password_bytemix")

		if (bytemix == None): field_data['error'] = "internal_error"

		if (mode & InputForm.PASSWORD_WITH_REPETITION == InputForm.PASSWORD_WITH_REPETITION):
		#
			repetition_name = "{0}_repetition".format(field_data['name'])
			repetition_content = self.get_input(repetition_name)

			if (field_data['content'] != repetition_content): field_data['error'] = "password_repetition"
			_type = "password_with_repetition"
		#
		else: _type = "password"

		if (field_data['error'] != None): _return = False
		elif (mode & InputForm.PASSWORD_MD5 == InputForm.PASSWORD_MD5): field_data['content_result'] = Md5.hash(field_data['content'])
		elif (mode & InputForm.PASSWORD_TMD5 == InputForm.PASSWORD_TMD5): field_data['content_result'] = Tmd5.hash(field_data['content'], bytemix)

		self._entry_set(_type, field_data)
		return _return
	#

	def entry_add_radio(self, field_data):
	#
		"""
Inserts radio fields for exact one selected option.

:param field_data: Form field data

:return: (bool) False if the content was not accepted
:since:  v0.1.00
		"""

		field_data = self._entry_defaults_set(field_data,"" ,"", None)

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

		self._entry_set("radio", field_data)
		return (field_data['error'] == None)
	#

	"""
/**
	* Number (integer) input mechanism
	*
	* @param  array $f_entry Form field data
	* @return boolean False if the content was not accepted
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddNumber ($f_entry)
	{
		global $direct_cachedata;
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -formbuilder->entryAddNumber (+f_entry)- (#echo(__LINE__)#)"); }

		$f_return = true;

		$f_entry = $this->entryDefaultsSet ($f_entry,"","",NULL);
		$f_entry = $this->entryFieldSizeSet ($f_entry);
		$f_entry = $this->entryLimitsSet ($f_entry);

		$f_entry['content'] = str_replace (" ","",$f_entry['content']);
		$f_entry['error'] = $this->entryRangeCheck ($f_entry['content'],$f_entry['min'],$f_entry['max'],$f_entry['required']);

		if ($f_entry['error']) { $f_return = false; }
		else { $direct_cachedata["i_".$f_entry['name']] = $f_entry['content']; }

		$this->entrySet ("number",$f_entry);
		return /*#ifdef(DEBUG):direct_debug (7,"sWG/#echo(__FILEPATH__)# -formbuilder->entryAddNumber ()- (#echo(__LINE__)#)",:#*/$f_return/*#ifdef(DEBUG):,true):#*/;
	}

/**
	* Inserts a range input.
	*
	* @param  array $f_entry Form field data
	* @return boolean False if the content was not accepted
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddRange ($f_entry)
	{
		global $direct_cachedata;
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -formbuilder->entryAddRange (+f_entry)- (#echo(__LINE__)#)"); }

		$f_entry = $this->entryDefaultsSet ($f_entry,"","",NULL);
		$f_entry = $this->entryFieldSizeSet ($f_entry,"s");
		$f_entry = $this->entryLimitsSet ($f_entry,0,100);

		$f_entry['error'] = $this->entryRangeCheck ($f_entry['content'],$f_entry['min'],$f_entry['max'],$f_entry['required']);

		if ($f_entry['error']) { $f_return = false; }
		else { $direct_cachedata["i_".$f_entry['name']] = $f_entry['content']; }

		$f_entry['content'] = direct_html_encode_special ($f_entry['content']);

		$this->entrySet ("range",$f_entry);

		if ($f_entry['error']) { return /*#ifdef(DEBUG):direct_debug (7,"sWG/#echo(__FILEPATH__)# -formbuilder->entryAddRadio ()- (#echo(__LINE__)#)",:#*/false/*#ifdef(DEBUG):,true):#*/; }
		else { return /*#ifdef(DEBUG):direct_debug (7,"sWG/#echo(__FILEPATH__)# -formbuilder->entryAddRadio ()- (#echo(__LINE__)#)",:#*/true/*#ifdef(DEBUG):,true):#*/; }
	}

/**
	* A rcp enhanced text input field.
	*
	* @param  array $f_entry Form field data
	* @return boolean False if the content was not accepted
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddRcpText ($f_entry)
	{
		global $direct_cachedata,$direct_settings;
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -formbuilder->entryAddRcpText (+f_entry)- (#echo(__LINE__)#)"); }

		if ($direct_settings['formbuilder_rcp_supported'])
		{
			$f_return = true;

			$f_entry = $this->entryDefaultsSet ($f_entry,"","",NULL);
			$f_entry = $this->entryFieldSizeSet ($f_entry);
			$f_entry = $this->entryLimitsSet ($f_entry);

			$f_entry['content'] = str_replace (array ("\n","&lt;","&gt;","<br />"),(array ("[newline]","<",">","[newline]")),$f_entry['content']);
			$f_entry['error'] = $this->entryLengthCheck ($f_entry['content'],$f_entry['min'],$f_entry['max'],$f_entry['required']);

			if ($f_entry['error']) { $f_return = false; }
			else { $direct_cachedata["i_".$f_entry['name']] = $f_entry['content']; }

			$f_entry['content'] = direct_html_encode_special ($f_entry['content']);

			$this->entrySet ("rcpText",$f_entry);
		}
		else { $f_return = $this->entryAddText ($f_entry); }

		return /*#ifdef(DEBUG):direct_debug (7,"sWG/#echo(__FILEPATH__)# -formbuilder->entryAddRcpText ()- (#echo(__LINE__)#)",:#*/$f_return/*#ifdef(DEBUG):,true):#*/;
	}

/**
	* A rcp enhanced textarea input field.
	*
	* @param  array $f_entry Form field data
	* @return boolean False if the content was not accepted
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddRcpTextarea ($f_entry)
	{
		global $direct_cachedata,$direct_settings;
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -formbuilder->entryAddRcpTextarea (+f_entry)- (#echo(__LINE__)#)"); }

		if ($direct_settings['formbuilder_rcp_supported'])
		{
			$f_return = true;

			$f_entry = $this->entryDefaultsSet ($f_entry,"","",NULL);
			$f_entry = $this->entryFieldSizeSet ($f_entry);
			$f_entry = $this->entryLimitsSet ($f_entry);

			$f_entry['content'] = str_replace (array ("[newline]","&lt;","&gt;","<br />"),(array ("\n","<",">","\n")),$f_entry['content']);
			$f_entry['error'] = $this->entryLengthCheck ($f_entry['content'],$f_entry['min'],$f_entry['max'],$f_entry['required']);

			if ($f_entry['error']) { $f_return = false; }
			else { $direct_cachedata["i_".$f_entry['name']] = $f_entry['content']; }

			$f_entry['content'] = direct_html_encode_special ($f_entry['content']);

			$this->entrySet ("rcpTextarea",$f_entry);
		}
		else { $f_return = $this->entryAddTextarea ($f_entry); }

		return /*#ifdef(DEBUG):direct_debug (7,"sWG/#echo(__FILEPATH__)# -formbuilder->entryAddRcpTextarea ()- (#echo(__LINE__)#)",:#*/$f_return/*#ifdef(DEBUG):,true):#*/;
	}

/**
	* Inserts a selectbox for exact one selected option.
	*
	* @param  array $f_entry Form field data
	* @return boolean False if the content was not accepted
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddSelect ($f_entry)
	{
		global $direct_cachedata;
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -formbuilder->entryAddSelect (+f_entry)- (#echo(__LINE__)#)"); }

		$f_entry = $this->entryDefaultsSet ($f_entry,"","",NULL);
		$f_entry = $this->entryFieldSizeSet ($f_entry,"s");

		$f_choices_array = direct_evars_get ($f_entry['content']);
		$f_entry['content'] = array ();
		$f_selected_value = "";

		if (is_array ($f_choices_array))
		{
			foreach ($f_choices_array as $f_choice_array)
			{
				$f_choice_array['value'] = direct_html_encode_special ($f_choice_array['value']);
				$f_choice_array['text'] = str_replace ('"',"&quot;",$f_choice_array['text']);
				if (!strlen ($f_choice_array['text'])) { $f_choice_array['text'] = $f_choice_array['value']; }
				if (isset ($f_choice_array['selected'])) { $f_selected_value = $f_choice_array['value']; }

				$f_entry['content'][] = $f_choice_array;
			}
		}

		$direct_cachedata["i_".$f_entry['name']] = $f_selected_value;
		$f_entry['error'] = ((($f_entry['required'])&&(!strlen ($f_selected_value))) ? "required_element" : "");

		$this->entrySet ("select",$f_entry);

		if ($f_entry['error']) { return /*#ifdef(DEBUG):direct_debug (7,"sWG/#echo(__FILEPATH__)# -formbuilder->entryAddRadio ()- (#echo(__LINE__)#)",:#*/false/*#ifdef(DEBUG):,true):#*/; }
		else { return /*#ifdef(DEBUG):direct_debug (7,"sWG/#echo(__FILEPATH__)# -formbuilder->entryAddRadio ()- (#echo(__LINE__)#)",:#*/true/*#ifdef(DEBUG):,true):#*/; }
	}

/**
	* A standard textarea input field.
	*
	* @param  array $f_entry Form field data
	* @return boolean False if the content was not accepted
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddTextarea ($f_entry)
	{
		global $direct_cachedata;
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -formbuilder->entryAddTextarea (+f_entry)- (#echo(__LINE__)#)"); }

		$f_return = true;

		$f_entry = $this->entryDefaultsSet ($f_entry,"","",NULL);
		$f_entry = $this->entryFieldSizeSet ($f_entry);
		$f_entry = $this->entryLimitsSet ($f_entry);

		$f_entry['content'] = str_replace (array ("[newline]","&lt;","&gt;","<br />"),(array ("\n","<",">","\n")),$f_entry['content']);
		$f_entry['error'] = $this->entryLengthCheck ($f_entry['content'],$f_entry['min'],$f_entry['max'],$f_entry['required']);

		if ($f_entry['error']) { $f_return = false; }
		else { $direct_cachedata["i_".$f_entry['name']] = $f_entry['content']; }

		$f_entry['content'] = direct_html_encode_special ($f_entry['content']);

		$this->entrySet ("textarea",$f_entry);
		return /*#ifdef(DEBUG):direct_debug (7,"sWG/#echo(__FILEPATH__)# -formbuilder->entryAddTextarea ()- (#echo(__LINE__)#)",:#*/$f_return/*#ifdef(DEBUG):,true):#*/;
	}

	"""
	#

	def entry_add_text(self, field_data):
	#
		"""
A single line text input field.

:param field_data: Form field data

:return: (bool) False if the content was not accepted
:since:  v0.1.00
		"""

		field_data = self._entry_defaults_set(field_data, "", "", None)
		field_data = self._entry_field_size_set(field_data)
		field_data = self._entry_limits_set(field_data)

		field_data['error'] = self._entry_length_check(field_data['content'], field_data['min'], field_data['max'], field_data['required'])

		self._entry_set("text", field_data)
		return (field_data['error'] == None)
	#

	def _entry_defaults_set(self, field_data, name = "", title = None, content = "", required = False):
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

			if ("content" not in field_data):
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

	def entry_error_set(self, section, name, error):
	#
		"""
Set an external error message for the given form field.

:param section: Form section
:param name: Field name
:param error: Error message definition

:since: v0.1.00
		"""

		_type = type(error)
		if (_type == str or _type == tuple): self.entry_update(section, name, { "error": error })
	#

	def _entry_field_size_set(self, field_data, size = "m"):
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

	def _entry_length_check(self, data, _min = None, _max = None, required = False):
	#
		"""
Checks the size for a given string.

:param data: The string that should be checked
:param _min: Defines the minimal length for a string or None to ignore
:param _max: Defines the maximal length for a string or None for an unlimited
            size
:param required: True if the field is required to continue

:return: (bool) False if a required field is empty, it is smaller than the
         minimum or larger than the maximum
:since:  v0.1.00
		"""

		data_length = (0 if (data == None) else len(data))

		if (required and data_length < 1): _return = "required_element"
		elif (_min != None and _min > data_length): _return = ( "string_min", str(_min) )
		elif (_max != None and _max < data_length): _return = ( "string_max", str(_max) )
		else: _return = None

		return _return
	#

	def _entry_limits_set(self, field_data, _min = None, _max = None):
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

	def _entry_range_check(self, data, _min = None, _max = None, required = False):
	#
		"""
Checks the size for a given string.

:param data: The string that should be checked
:param _min: Defines the minimal range for a number or None to ignore
:param _max: Defines the maximal range for a number or None for an unlimited
            size
:param required: True if the field is required to continue

:return: (bool) False if a required field is empty, it is smaller than the
         minimum or larger than the maximum
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

	def _entry_set(self, field_type, field_data):
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
			else: name = hexlify(urandom(10))

			if (field_data['section'] not in self.cache_sections):
			#
				position = len(self.cache)
				section = { "fields": [ ], "name": field_data['section'], "positions": { } }

				self.cache.append(section)
				self.cache_sections[field_data['section']] = position
			#

			cache = self.cache[self.cache_sections[field_data['section']]]

			if (name in cache['positions']): self.entry_update(field_data['section'], name, field_data)
			else:
			#
				position = len(cache['fields'])

				cache['fields'].append(field_data)
				cache['positions'][name] = position

				self.form_is_valid = None
			#
		#
	#

	def entry_update(self, section, name, field_data):
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

	def _error_get_message(self, error_data):
	#
		"""
Returns the error message for the error data given. Returned message is
implementation specific.

:param error_data: Field error data

:return: (str) Implementation specific error message
:since:  v0.1.00
		"""

		return (error_data[0] if (type(error_data) == tuple) else error_data)
	#

	def get_data(self, flush = True):
	#
		"""
Returns all defined fields.

:param flush: Flush the cache

:return: (list) Field data
:since:  v0.1.00
		"""

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
					if (field_data['error'] != None): _return.append({ "name": field_data['name'], "error_data": field_data['error'], "error_message": self._error_get_message(field_data['error']) })
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

	def set_input_available(self):
	#
		"""
Sets the flag for available input. Input values can be read with
"get_input()".

:since: v0.1.00
		"""

		self.form_has_input = True
	#
#

##j## EOF