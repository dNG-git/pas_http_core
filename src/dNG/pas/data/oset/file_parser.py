# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.oset.FileParser
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

from dNG.data.file import File
from dNG.pas.data.settings import Settings
from dNG.pas.data.text.l10n import L10n
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.runtime.io_exception import IOException
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
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(FileParser)

:since: v0.1.00
		"""

		Parser.__init__(self)

		self.cache_instance = NamedLoader.get_singleton("dNG.pas.data.Cache", False)
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

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render({1}, +content)- (#echo(__LINE__)#)".format(self, template_name))
		_return = ("<span>{0}</span>".format(L10n.get("errors_pas_http_core_oset_not_viewable")) if (default == None) else default)

		try:
		#
			file_pathname = path.normpath("{0}/{1}/{2}.tsc".format(self.path, self.oset, template_name.replace(".", "/")))
			if (not os.access(file_pathname, os.R_OK)): file_pathname = path.normpath("{0}/{1}/{2}.tsc".format(self.path, Settings.get("pas_http_theme_oset_default", "xhtml5"), template_name.replace(".", "/")))

			template_data = (None if (self.cache_instance == None) else self.cache_instance.get_file(file_pathname))

			if (template_data == None):
			#
				file_obj = File()
				if (not file_obj.open(file_pathname, True, "r")): raise IOException("Failed to open OSet file for '{0}'".format(template_name))

				template_data = file_obj.read()
				file_obj.close()

				if (template_data == False): raise IOException("Failed to read OSet file for '{0}'".format(template_name))
				if (self.cache_instance != None): self.cache_instance.set_file(file_pathname, template_data)
			#

			_return = Parser.render(self, template_data, content)
		#
		except Exception as handled_exception:
		#
			if (self.log_handler != None): self.log_handler.error(handled_exception)
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