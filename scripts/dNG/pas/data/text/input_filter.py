# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.input_filter
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

from unicodedata import category as unicode_category
import re

from dNG.pas.pythonback import direct_str, direct_unicode
from dNG.pas.pythonback import direct_settings as direct_pythonback_settings

class direct_input_filter(object):
#
	"""
"direct_input_filter" provides basic input filter functions.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	@staticmethod
	def filter_control_chars(data, tab_allowed = False):
	#
		"""
There are some persons out there that may want to inject control characters
into our system. The function "filter_control_chars()" will remove these
characters.

:param data: Input string

:return: (str) Filtered string
:since:  v0.1.00
		"""

		if (data != None): data = direct_unicode(data)

		if (type(data) == direct_pythonback_settings['unicode_type']):
		#
			data_position = 0
			data_length = len(data)

			while (data_position < data_length):
			#
				value = data[data_position]
				value_unicode_category = unicode_category(value)

				if ((value_unicode_category == "Cc" and value != "\n" and ((not tab_allowed) or value != "\t")) or value_unicode_category == "Cn" or value_unicode_category == "Co"):
				#
					data = data[:data_position] + data[1 + data_position:]
					data_length -= 1
				#
				else: data_position += 1
			#

			data = direct_str(data)
		#
		else: data = None

		return data
	#

	@staticmethod
	def filter_email_address(data):
	#
		"""
Checks a eMail address if it's valid (RFC822) and returns the (unfolded)
address if it is.

:param data: Input eMail

:return: (str) Filtered eMail address or empty string if the address is not
         valid
:since:  v0.1.00
		"""

		address_parsing = True
		is_valid = True
		data_part = ""

		data = direct_input_filter.filter_control_chars(data)
		if (type(data) == str): data = re.sub("\\r\\n([\\x09\\x20])+", "\\1", data)
		dot_parts = ([ ] if (data == None) else data.split("."))
		re_char_escaped = re.compile("([\\\\]+)\"$")
		re_valid_chars = re.compile("^[\\x00-\\x0c\\x0e-\\x7f]+$")
		re_valid_chars_quotes = re.compile("^\"[\\x00-\\x0c\\x0e-\\x7f]+\"$")
		re_invalid_chars = re.compile("[\\x00-\\x20\\x22\\x28\\x29\\x2c\\x2e\\x3a-\\x3c\\x3e\\x40\\x5b-\\x5d\\x7f-\\xff]")

		for dot_part in dot_parts:
		#
			if (not address_parsing): data_part += "." + dot_part
			elif (is_valid):
			#
				if (len(data_part) > 0 or dot_part[0] == "\""):
				#
					if (len(dot_part) > 1 and dot_part[-1:] == "\""):
					#
						re_result = re_char_escaped.search(dot_part)

						if (re_result != None and (len(re_result.group(1)) % 2) == 1): data_part += dot_part
						else:
						#
							data_part += dot_part
							if (re_valid_chars_quotes.search(data_part) == None): is_valid = False
						#
					#
					elif ("\"@" not in dot_part): data_part += dot_part
					else:
					#
						at_splitted = dot_part.split("\"@", 2)
						address_parsing = False

						if (re_valid_chars.search(data_part + at_splitted[0]) == None): is_valid = False
						else: data_part = at_splitted[1]
					#
				#
				else:
				#
					if ("@" not in dot_part): data_part = dot_part
					else:
					#
						at_splitted = dot_part.split("@", 2)
						address_parsing = False
						data_part = at_splitted[0]
					#

					if (not re_invalid_chars.search(data_part)): is_valid = False
					data_part = ("" if (address_parsing) else at_splitted[1])
				#
			#
		#

		if (len(data_part) < 1): is_valid = False

		dot_parts = data_part.split(".")
		data_part = ""
		re_comment = re.compile("^\[[\\x00-\\x0c\\x0e-\\x7f]+\]$")

		for dot_part in dot_parts:
		#
			if (is_valid):
			#
				if (len(data_part) > 0 or dot_part[0] == '['):
				#
					if (len(dot_part) > 1 and dot_part[-1:] == "]"):
					#
						re_result = re_char_escaped.search(dot_part)

						if (re_result != None and (len(re_result.group(1)) % 2) == 1): data_part += dot_part
						else:
						#
							data_part += dot_part

							if (re_comment.search(data_part) == None): is_valid = False
							else: data_part = ""
						#
					#
					else: data_part += dot_part
				#
				elif (re_invalid_chars.search(dot_part) != None): is_valid = False
			#
		#

		return (data if (is_valid) else None)
	#

	@staticmethod
	def filter_file_path(data, uprefs_allowed = False):
	#
		"""
File paths should never contain target definitions like directory 
traversals. We will filter them using "filterFilePath()".

:param data: Input path
:param uprefs_allowed: True to not remove references that leave the current
                       base directory

:return: (str) Filtered output path
:since:  v0.1.00
		"""

		data = direct_input_filter.filter_control_chars(data)

		if (type(data) == str):
		#
			data = re.sub("^(\w{3,5})\:\/\/", "", data)

			data = data.replace("/./", "/")
			data = data.replace("\\", "")
			data = re.sub("\w\/[\.\/]", "", data)

			if ((not uprefs_allowed) and data != "."):
			#
				data = re.sub("^[\.\/]+", "", data)
				data = re.sub("[\.\/]+$", "", data)
			#
		#

		return data
	#

	@staticmethod
	def filter_float(data):
	#
		"""
Check and convert to float.

:param data: Input string

:return: (float) Filtered output float
:since:  v0.1.00
		"""

		try:
		#
			if (data != None): data = float(data)
		#
		except: data = None

		return data
	#

	@staticmethod
	def filter_int(data):
	#
		"""
Check and convert to int.

:param data: Input string

:return: (int) Filtered output integer
:since:  v0.1.00
		"""

		try:
		#
			if (data != None): data = int(data)
		#
		except: data = None

		return data
	#
#

##j## EOF