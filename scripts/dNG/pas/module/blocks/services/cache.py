# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.module.blocks.services.cache
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
import os, re

from dNG.data.file import direct_file
from dNG.data.rfc.basics import direct_basics as direct_rfc_basics
from dNG.pas.data.settings import direct_settings
from dNG.pas.data.http.streaming import direct_streaming
from dNG.pas.data.text.input_filter import direct_input_filter
from dNG.pas.data.xhtml.mmedia_parser import direct_mmedia_parser
from dNG.pas.module.named_loader import direct_named_loader
from .module import direct_module

class direct_cache(direct_module):
#
	"""
Service for "m=services;s=cache"

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def execute_index(self):
	#
		"""
Action for "index"

:since: v0.1.00
		"""

		dfile = direct_input_filter.filter_file_path(self.request.get_dsd("dfile", ""))
		file_pathname = ""

		if (dfile != None and dfile != ""):
		#
			file_pathname = path.abspath("{0}/mmedia/{1}".format(direct_settings.get("path_data"), dfile))

			if (path.exists(file_pathname) and os.access(file_pathname, os.R_OK)):
			#
				if (file_pathname.endswith(".paslink.url")):
				#
					file_content = (None if (self.cache_instance == None) else self.cache_instance.get_file(file_pathname))

					if (file_content == None):
					#
						file_obj = direct_file()

						if (file_obj.open(file_pathname, True, "r")):
						#
							file_content = file_obj.read()
							if (file_content != False and self.cache_instance != None): self.cache_instance.set_file(file_pathname, file_content)
						#
					#

					file_pathname = ("" if (file_content == None or file_content == False or (not path.exists(file_pathname)) or (not os.access(file_pathname, os.R_OK))) else file_content)
				#
			#
			else: file_pathname = ""
		#

		is_last_modified_supported = (direct_settings.get("pas_http_cache_modification_check", "1") == "1")
		is_modified = True
		is_valid = False
		last_modified_on_server = 0

		if (file_pathname != ""):
		#
			is_valid = True

			if (is_last_modified_supported and self.request.get_header("If-Modified-Since") != None):
			#
				last_modified_on_client = direct_rfc_basics.get_rfc2616_timestamp(self.request.get_header("If-Modified-Since"))

				if (last_modified_on_client > -1):
				#
					last_modified_on_server = int(os.stat(file_pathname).st_mtime)

					if (last_modified_on_server <= last_modified_on_client):
					#
						is_modified = False

						self.response.init(True)
						self.response.set_header("HTTP/1.1", "HTTP/1.1 304 Not Modified", True)
						self.response.set_last_modified(last_modified_on_server)

						self.response.set_raw_data("")
					#
				#
			#
		#

		if (is_valid and is_modified):
		#
			if (is_last_modified_supported):
			#
				if (last_modified_on_server < 1): last_modified_on_server = int(os.stat(file_pathname).st_mtime)
				self.response.set_last_modified(last_modified_on_server)
			#

			re_tsc_result = re.search("\.tsc\.(css|js|svg)$", file_pathname, re.I)
			re_result = (re.search("\.(css|gif|jar|jpg|jpeg|js|png|svg|swf)$", file_pathname, re.I) if (re_tsc_result == None) else None)

			if (re_tsc_result != None):
			#
				file_extension = re_tsc_result.group(1)

				if (file_extension == "css"): self.response.set_header("Content-Type", "text/css")
				elif (file_extension == "js"): self.response.set_header("Content-Type", "text/javascript")
				elif (file_extension == "svg"): self.response.set_header("Content-Type", "text/svg+xml")

				parser = direct_mmedia_parser()

				self.response.init(True)
				self.response.set_raw_data(parser.render(file_pathname))
			#
			elif (re_result != None):
			#
				streamer = direct_named_loader.get_instance("dNG.pas.data.streamer.file", False)

				if (streamer == None): self.response.set_header("HTTP/1.1", "HTTP/1.1 500 Internal Server Error", True)
				else: direct_streaming.run(self.request, streamer, ("file://" if (file_pathname[:1] == "/") else "file:///") + file_pathname, self.response)
			#
			else: self.response.set_header("HTTP/1.1", "HTTP/1.1 415 Unsupported Media Type", True)
		#
		elif (not is_valid): self.response.set_header("HTTP/1.1", "HTTP/1.1 404 Not Found", True)
	#
#

##j## EOF