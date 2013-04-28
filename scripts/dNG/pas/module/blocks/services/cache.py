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
http://www.direct-netware.de/redirect.py?pas;user_profile

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasHttpUserProfileVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from os import path
from time import time
import os, re

from dNG.data.file import direct_file
from dNG.data.rfc.basics import direct_basics as direct_rfc_basics
from dNG.pas.data.settings import direct_settings
from dNG.pas.data.text.input_filter import direct_input_filter
from dNG.pas.data.text.tag_parser.mmedia_text_file import direct_mmedia_text_file
from dNG.pas.module.named_loader import direct_named_loader
from dNG.pas.pythonback import direct_bytes
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

	def __init__(self):
	#
		"""
Constructor __init__(direct_cache)

@since v0.1.00
		"""

		direct_module.__init__(self)

		self.cache_instance = None
		"""
Cache instance
		"""
	#

	def __del__(self):
	#
		"""
Destructor __del__(direct_cache)

@since v0.1.00
		"""

		if (self.cache_instance != None): self.cache_instance.return_instance()
	#

	def execute_index(self):
	#
		"""
Action for "index"

:since: v0.1.00
		"""

		cache_max_size = int(direct_settings.get("pas_http_cache_file_size_max", 10485760))
		dfile = direct_input_filter.filter_file_path(self.request.get_dsd("dfile", ""))
		file_pathname = ""

		if (dfile != None and dfile != ""):
		#
			file_pathname = path.abspath("{0}/mmedia/{1}".format(direct_settings.get("path_data"), dfile))
			self.cache_instance = direct_named_loader.get_singleton("dNG.pas.data.cache", False)

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

						self.response.send_raw_data()
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

				parser = direct_mmedia_text_file()
				self.response.set_raw_data(parser.render(file_pathname))
			#
			elif (re_result != None):
			#
				self.response.set_stream_mode(True)

				file_size = os.stat(file_pathname).st_size
				range_start = 0
				range_size = 0
				range_end = 0

				if (self.request.get_header('range') != None):
				#
					is_valid = False
					re_result = re.match("^bytes(.*?)=(.*?)-(.*?)$", self.request.get_header('range'), re.I)

					if (re_result != None):
					#
						range_start = re.sub("(\D+)", "", re_result.group(2))
						range_end = int(re.sub("(\D+)", "", re_result.group(3)))

						if (range_start != ""):
						#
							range_start = int(range_start)

							if (range_end != ""):
							#
								range_end = int(range_end)
								if (range_start >= 0 and range_start <= range_end and range_end < file_size): is_valid = True
							#
							elif (range_start >= 0 and range_start < file_size):
							#
								is_valid = True
								range_end = file_size - 1
							#
						#
						elif (range_end != ""):
						#
							range_start = 0
							range_end = int(range_end)
							if (range_end > 0 and range_end < file_size): is_valid = True
						#

						if (is_valid):
						#
							self.response.set_header("HTTP/1.1", "HTTP/1.1 206 Partial Content", True)
							self.response.set_header("Content-Range", "{0:d}-{1:d}/{2:d}".format(range_start, range_end, file_size))

							range_size = (1 + range_end - range_start)
							self.response.set_header("Content-Length", range_size)
						#
					#
				#

				file_extension = re_result.group(1)
				is_binary = True

				if (file_extension == "css"):
				#
					self.response.set_header("Content-Type", "text/css")
					file_mode = "r"
					is_binary = False
				#
				elif (file_extension == "gif"):
				#
					self.response.set_header("Content-Type", "image/gif")
					file_mode = "rb"
				#
				elif (file_extension == "jar"):
				#
					self.response.set_header("Content-Type", "application/java-archive")
					file_mode = "rb"
				#
				elif (file_extension == "js"):
				#
					self.response.set_header("Content-Type", "text/javascript")
					file_mode = "r"
					is_binary = False
				#
				elif (file_extension == "png"):
				#
					self.response.set_header("Content-Type", "image/png")
					file_mode = "rb"
				#
				elif (file_extension == "svg"):
				#
					self.response.set_header("Content-Type", "image/svg+xml")
					file_mode = "r"
					is_binary = False
				#
				elif (file_extension == "swf"):
				#
					self.response.set_header("Content-Type", "application/x-shockwave-flash")
					file_mode = "rb"
				#
				else:
				#
					self.response.set_header("Content-Type", "image/jpeg")
					file_mode = "rb"
				#

				file_data = (None if (self.cache_instance == None) else self.cache_instance.get_file(file_pathname))

				if (file_data == None):
				#
					"""
File is not cached. Read and send data.
					"""

					file_cacheable = (False if (range_start + range_end > 0 or file_size > cache_max_size) else True)
					file_obj = direct_file()

					if (file_cacheable): range_size = file_size
					elif (range_start > 0): file_obj.seek(range_start)

					timeout_time = time() + int(direct_settings.get("pas_server_socket_data_timeout", 30))

					if (file_obj.open(file_pathname, True, file_mode)):
					#
						file_data = (direct_bytes("") if (is_binary) else "")
						self.response.init(True)

						while (range_size > 0 and (not file_obj.eof_check()) and time() < timeout_time):
						#
							block_size = (4096 if (range_size > 4096) else range_size)

							if (file_cacheable):
							#
								block_data = file_obj.read(block_size)
								file_data += block_data
								self.response.send_raw_data(block_data)
							#
							else: self.response.send_raw_data(file_obj.read(block_size))

							range_size -= block_size
						#

						if (file_cacheable and range_size < 1 and self.cache_instance != None): self.cache_instance.set_file(file_pathname, file_data)
					#
					else: self.response.set_header("HTTP/1.1", "HTTP/1.1 500 Internal Server Error", True)
				#
				else:
				#
					"""
File is cached. Send data.
					"""

					if (range_end > 0): file_data = file_data[:range_end]
					if (range_start > 0): file_data = file_data[range_start:]

					self.response.init(True)
					self.response.send_raw_data(file_data)
				#
			#
			else: self.response.set_header("HTTP/1.1", "HTTP/1.1 415 Unsupported Media Type", True)
		#
		elif (not is_valid): self.response.set_header("HTTP/1.1", "HTTP/1.1 404 Not Found", True)
	#
#

##j## EOF