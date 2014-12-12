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
import re

from dNG.data.rfc.basics import Basics as RfcBasics
from dNG.pas.data.settings import Settings
from dNG.pas.data.cache.file_content import FileContent
from dNG.pas.data.http.streaming import Streaming
from dNG.pas.data.text.input_filter import InputFilter
from dNG.pas.data.xhtml.mmedia_parser import MmediaParser
from dNG.pas.module.named_loader import NamedLoader
from .module import Module

class Cache(Module):
#
	"""
Service for "s=cache"

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def execute_index(self):
	#
		"""
Action for "index"

:since: v0.1.00
		"""

		dfile = InputFilter.filter_file_path(self.request.get_dsd("dfile", ""))

		file_path_name = ""

		self.response.set_header("X-Robots-Tag", "noindex")

		if (dfile != None and dfile != ""):
		#
			file_path_name = path.abspath("{0}/mmedia/{1}".format(Settings.get("path_data"), dfile))

			if (path.exists(file_path_name) and os.access(file_path_name, os.R_OK)):
			#
				if (file_path_name.endswith(".paslink.url")):
				#
					file_content = FileContent.read(file_path_name)
					if (file_content != None): file_content = path.normpath(file_content)
					file_path_name = ("" if (file_content == None or (not path.exists(file_content)) or (not os.access(file_content, os.R_OK))) else file_content)
				#
			#
			else: file_path_name = ""
		#

		is_last_modified_supported = (Settings.get("pas_http_cache_modification_check", True))
		is_modified = True
		is_valid = False
		last_modified_on_server = 0

		if (file_path_name != ""):
		#
			is_valid = True

			if (is_last_modified_supported and self.request.get_header("If-Modified-Since") != None):
			#
				last_modified_on_client = RfcBasics.get_rfc7231_timestamp(self.request.get_header("If-Modified-Since").split(";")[0])

				if (last_modified_on_client > -1):
				#
					last_modified_on_server = int(os.stat(file_path_name).st_mtime)

					if (last_modified_on_server <= last_modified_on_client):
					#
						is_modified = False
						self.response.set_content_dynamic(False)

						self.response.init(True)
						self.response.set_header("HTTP/1.1", "HTTP/1.1 304 Not Modified", True)
						self.response.set_expires_relative(+63072000)
						self.response.set_last_modified(last_modified_on_server)

						self.response.set_raw_data("")
					#
				#
			#
		#

		if (is_valid and is_modified):
		#
			re_tsc_result = re.search("\\.tsc\\.(css|js|min\\.css|min\\.js|min\\.svg|svg)$", file_path_name, re.I)

			self.response.set_content_dynamic(re_tsc_result != None)
			self.response.init(True)

			if (is_last_modified_supported):
			#
				if (last_modified_on_server < 1): last_modified_on_server = int(os.stat(file_path_name).st_mtime)
				self.response.set_last_modified(last_modified_on_server)
			#

			if (re_tsc_result != None):
			#
				file_extension = re_tsc_result.group(1)

				if (file_extension == "css"): self.response.set_header("Content-Type", "text/css")
				elif (file_extension == "js"): self.response.set_header("Content-Type", "text/javascript")
				elif (file_extension == "svg"): self.response.set_header("Content-Type", "text/svg+xml")

				parser = MmediaParser()
				self.response.set_raw_data(parser.render(file_path_name))
			#
			else:
			#
				self.response.set_expires_relative(+63072000)

				streamer = NamedLoader.get_instance("dNG.pas.data.streamer.File", False)

				if (streamer == None): self.response.set_header("HTTP/1.1", "HTTP/1.1 500 Internal Server Error", True)
				else: Streaming.handle_url(self.request, streamer, "file:///{0}".format(file_path_name), self.response)
			#
		#
		elif (not is_valid):
		#
			if (self.log_handler != None): self.log_handler.warning("#echo(__FILEPATH__)# -Cache.execute_index()- reporting: Failed opening {0} - file not readable", dfile, context = "pas_http_core")
			self.response.set_header("HTTP/1.1", "HTTP/1.1 404 Not Found", True)
		#
	#
#

##j## EOF