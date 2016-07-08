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

from dNG.data.settings import Settings
from dNG.data.text.input_filter import InputFilter
from dNG.data.text.l10n import L10n
from dNG.data.text.l10n_instance import L10nInstance
from dNG.module.controller.abstract_http import AbstractHttp as AbstractHttpController
from dNG.runtime.io_exception import IOException

class Lang(AbstractHttpController):
#
	"""
The "Lang" class provides access to the language files.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def execute_api_get(self):
	#
		"""
Action for "api_get"

:since: v0.2.00
		"""

		if (not self.response.is_supported("dict_result_renderer")): raise IOException("Unsupported response object for action")
		lang_request = self.request.get_dsd("lang_request")

		lang = L10n.get_default_lang()
		lang_request_list = lang_request.split(" ")

		instance = L10nInstance(lang)

		for file_id in lang_request_list:
		#
			relative_file_path_name = InputFilter.filter_file_path(L10n.get_relative_file_path_name(file_id))
			file_path_name = "{0}/{1}/{2}.json".format(Settings.get("path_lang"), lang, relative_file_path_name)

			instance.read_file(file_path_name, True)
		#

		self.response.init(True)
		self.response.set_content_dynamic(False)
		self.response.set_expires_relative(+3600)
		self.response.set_result(instance)
	#
#

##j## EOF