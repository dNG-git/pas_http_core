# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.oset.file_parser
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
import os

from dNG.data.file import direct_file
from dNG.pas.data.settings import direct_settings
from dNG.pas.data.text.l10n import direct_l10n
from dNG.pas.module.named_loader import direct_named_loader
from .parser import direct_parser

class direct_file_parser(direct_parser):
#
	"""
The OSet file parser takes a file to render the output.

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
Constructor __init__(direct_file_parser)

:since: v0.1.00
		"""

		direct_parser.__init__(self)

		self.cache_instance = direct_named_loader.get_singleton("dNG.pas.data.cache", False)
		"""
Cache instance
		"""
		self.oset = None
		"""
OSet requested
		"""
		self.path = direct_settings.get("path_osets", "{0}/osets".format(direct_settings.get("path_data")))
		"""
Path to the osets directory
		"""
	#

	def __del__(self):
	#
		"""
Destructor __del__(direct_file_parser)

:since: v0.1.00
		"""

		if (self.cache_instance != None): self.cache_instance.return_instance()
		if (direct_parser != None): direct_parser.__del__(self)
	#

	def render(self, template_name, content, default = None):
	#
		"""
Renders content ready for output from the given OSet template.

:param template_name: OSet template name
:param content: Content object

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -osetParser.render({0}, +content)- (#echo(__LINE__)#)".format(template_name))
		var_return = (direct_l10n.get("pas_http_core_oset_not_viewable") if (default == None) else default)

		try:
		#
			file_pathname = path.normpath("{0}/{1}/{2}.tsc".format(self.path, self.oset, template_name.replace(".", "/")))
			if (not os.access(file_pathname, os.R_OK)): file_pathname = path.normpath("{0}/{1}/{2}.tsc".format(self.path, direct_settings.get("pas_http_theme_oset_default", "xhtml5"), template_name.replace(".", "/")))

			template_data = (None if (self.cache_instance == None) else self.cache_instance.get_file(file_pathname))

			if (template_data == None):
			#
				file_obj = direct_file()

				if (file_obj.open(file_pathname, True, "r")): template_data = file_obj.read()
				else: raise RuntimeError("Failed to open OSet file for '{0}'".format(template_name), 77)

				file_obj.close()

				if (template_data == False): raise RuntimeError("Failed to read OSet file for '{0}'".format(template_name), 5)
				elif (self.cache_instance != None): self.cache_instance.set_file(file_pathname, template_data)
			#

			var_return = direct_parser.render(self, template_data, content)
		#
		except Exception as handled_exception:
		#
			if (self.log_handler != None): self.log_handler.error(handled_exception)
		#

		return var_return
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
#

##j## EOF