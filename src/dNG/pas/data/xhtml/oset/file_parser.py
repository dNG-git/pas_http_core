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

from os import path
import os

from dNG.data.file import File
from dNG.pas.data.settings import Settings
from dNG.pas.data.text.l10n import L10n
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.runtime.exception_log_trap import ExceptionLogTrap
from dNG.pas.runtime.io_exception import IOException
from dNG.pas.runtime.type_exception import TypeException
from .parser import Parser

class FileParser(Parser):
#
	"""
The OSet file parser takes a file to render the output.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	# pylint: disable=arguments-differ

	def __init__(self):
	#
		"""
Constructor __init__(FileParser)

:since: v0.1.00
		"""

		Parser.__init__(self)

		self.cache_instance = NamedLoader.get_singleton("dNG.pas.data.cache.Content", False)
		"""
Cache instance
		"""
		self.oset = None
		"""
OSet requested
		"""
		self.path = Settings.get("path_osets", "{0}/osets".format(Settings.get("path_data")))
		"""
Path to the osets directory
		"""
	#

	def render(self, template_name, content, default = None):
	#
		"""
Renders content ready for output from the given OSet template.

:param template_name: OSet template name
:param content: Content object

:return: (str) Rendered content
:since:  v0.1.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render({1})- (#echo(__LINE__)#)", self, template_name, context = "pas_http_core")
		_return = ("<span>{0}</span>".format(L10n.get("errors_pas_http_core_oset_not_viewable")) if (default is None) else default)

		with ExceptionLogTrap("pas_http_core"):
		#
			if (type(template_name) is not str): raise TypeException("Given OSet template name is not valid")

			file_path_name = path.join(self.path, self.oset, "{0}.tsc".format(template_name.replace(".", "/")))

			if (not os.access(file_path_name, os.R_OK)):
			#
				file_path_name = path.join(self.path,
				                          Settings.get("pas_http_theme_oset_default", "xhtml5"),
				                          "{0}.tsc".format(template_name.replace(".", "/"))
				                         )
			#

			template_data = (None if (self.cache_instance is None) else self.cache_instance.get_file(file_path_name))

			if (template_data is None):
			#
				file_obj = File()
				if (not file_obj.open(file_path_name, True, "r")): raise IOException("Failed to open OSet file for '{0}'".format(template_name))

				template_data = file_obj.read()
				file_obj.close()

				if (template_data == False): raise IOException("Failed to read OSet file for '{0}'".format(template_name))
				if (self.cache_instance is not None): self.cache_instance.set_file(file_path_name, template_data)
			#

			_return = Parser.render(self, template_data, content)
		#

		return _return
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