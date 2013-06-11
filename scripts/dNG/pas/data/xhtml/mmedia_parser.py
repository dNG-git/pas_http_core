# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.xhtml.mmedia_parser
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

from os import path
import re

from dNG.data.file import direct_file
from dNG.pas.data.settings import direct_settings
from dNG.pas.data.tag_parser.abstract_impl import direct_abstract_impl
from dNG.pas.data.text.l10n import direct_l10n
from dNG.pas.data.text.tag_parser.rewrite_mixin import direct_rewrite_mixin
from dNG.pas.module.named_loader import direct_named_loader

class direct_mmedia_parser(direct_abstract_impl, direct_rewrite_mixin):
#
	"""
Parses files in the "mmedia" directory to set configured values and replace
language placeholders.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(direct_mmedia_parser)

:since: v0.1.00
		"""

		direct_abstract_impl.__init__(self)

		self.cache_instance = direct_named_loader.get_singleton("dNG.pas.data.cache", False)
		self.log_handler = direct_named_loader.get_singleton("dNG.pas.data.logging.log_handler", False)
	#

	def __del__(self):
	#
		"""
Destructor __del__(direct_mmedia_parser)

:since: v0.1.00
		"""

		if (self.cache_instance != None): self.cache_instance.return_instance()
		if (direct_abstract_impl != None): direct_abstract_impl.__del__(self)
	#

	def parser_change(self, tag_definition, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the matched tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:access: protected
:return: (str) Converted data
:since:  v0.1.00
		"""

		var_return = data[:tag_position]

		data_closed = data[self.parser_tag_find_end_position(data, tag_end_position):]

		if (tag_definition['tag'] == "rewrite"):
		#
			source = re.match("^\[rewrite:(\w+)\]", data[tag_position:data_position]).group(1)
			key = data[data_position:tag_end_position]

			if (source == "l10n"): var_return += self.render_rewrite(direct_l10n.get_instance(), key)
			else: var_return += self.render_rewrite(direct_settings.get_instance(), key)

			var_return += data_closed
		#
		else: var_return += data_closed

		return var_return
	#

	def parser_check(self, data):
	#
		"""
Check if a possible tag match is a false positive.

:param data: Data starting with the possible tag

:access: protected
:return: (dict) Matched tag definition; None if false positive
:since:  v0.1.00
		"""

		var_return = None

		i = 0
		tags = [ "rewrite" ]
		tags_length = len(tags)

		while (var_return == None and i < tags_length):
		#
			tag = tags[i]
			data_match = data[1:1 + len(tag)]

			if (data_match == tag and data_match == "rewrite"):
			#
				re_result = re.match("^\[rewrite:(\w+)\]", data)
				if (re_result != None and re_result.group(1) in [ "l10n", "settings" ]): var_return = { "tag": "rewrite", "tag_end": "[/rewrite]" }
			#

			i += 1
		#

		return var_return
	#

	def render(self, file_pathname):
	#
		"""
Renders content ready for output from the given "mmedia" file.

:param file_pathname: mmedia file path and name

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -mmediaParser.render({0})- (#echo(__LINE__)#)".format(file_pathname))

		file_pathname = path.normpath(file_pathname)
		file_content = (None if (self.cache_instance == None) else self.cache_instance.get_file(file_pathname))

		if (file_content == None):
		#
			file_obj = direct_file()

			if (file_obj.open(file_pathname, True, "r")): file_content = file_obj.read()
			else: raise RuntimeError("Failed to open mmedia file '{0}'".format(file_pathname), 77)

			file_obj.close()

			if (file_content == False): raise RuntimeError("Failed to read mmedia file '{0}'".format(file_pathname), 5)
			elif (self.cache_instance != None): self.cache_instance.set_file(file_pathname, file_content)
		#

		return self.parser(file_content)
	#
#

##j## EOF