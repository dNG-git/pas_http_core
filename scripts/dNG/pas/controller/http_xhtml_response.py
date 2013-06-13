# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.controller.http_xhtml_response
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

import re

from dNG.pas.data.binary import Binary
from dNG.pas.data.settings import Settings
from dNG.pas.data.text.l10n import L10n
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.plugins.hooks import Hooks
from .abstract_http_response import AbstractHttpResponse

class HttpXhtmlResponse(AbstractHttpResponse):
#
	"""
The following class implements the response object for XHTML content.

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
Constructor __init__(HttpXhtmlResponse)

:since: v0.1.00
		"""

		AbstractHttpResponse.__init__(self)

		self.oset = None
		"""
OSet in use (requested or configured)
		"""
		self.theme = None
		"""
Output theme (requested or configured)
		"""
		self.theme_active = None
		"""
Selected output theme
		"""
		self.theme_renderer = None
		"""
Selected theme renderer
		"""
		self.theme_subtype = "site"
		"""
Output theme subtype
		"""
	#

	def add_js_file(self, js_file):
	#
		"""
Add the defined javascript file to the output.

:param js_file: JS file name

:since: v0.1.00
		"""

		common_names = Settings.get("pas_http_theme_oset_js_aliases", { "jquery/jquery.min.js": "jquery/jquery-2.0.0.min.js" })
		if (js_file in common_names): js_file= common_names[js_file]
		self.theme_renderer.add_js_file(js_file)
	#

	def add_oset_content(self, template_name, content = None):
	#
		"""
Add output content from an OSet template.

:param template_name: OSet template name
:param content: Content object

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.add_oset_content({0}, content)- (#echo(__LINE__)#)".format(template_name))

		parser = NamedLoader.get_instance("dNG.pas.data.oset.FileParser")
		parser.set_oset(self.oset)

		data = parser.render(template_name, content)

		if (data != ""):
		#
			if (self.content == None): self.content = ""
			self.content += data
		#
	#

	def get_oset(self):
	#
		"""
Returns the OSet in use.

:return: (str) OSet name
:since:  v0.1.00
		"""

		return self.oset
	#

	def get_theme(self):
	#
		"""
Returns the theme to use.

:return: (str) Output theme
:since:  v0.1.00
		"""

		return self.theme
	#

	def get_theme_active(self):
	#
		"""
Returns the active theme in use. This could be different from the requested
theme if plugins changed the selected theme renderer.

:return: (str) Active output theme
:since:  v0.1.00
		"""

		return self.theme_active
	#

	def init(self, cache = False, compress = True):
	#
		"""
Important headers will be created here. This includes caching, cookies, the
compression setting and information about P3P.

:param cache: Allow caching at client
:param compress: Send page GZip encoded (if supported)

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.init(cache, compress)- (#echo(__LINE__)#)")

		AbstractHttpResponse.init(self, cache, compress)

		if (self.theme_renderer == None):
		#
			"""
Set up theme framework
			"""

			Settings.read_file("{0}/settings/pas_http_theme.json".format(Settings.get("path_data")))
			theme = (Hooks.call("dNG.pas.http.theme.check_candidates", theme = self.theme) if (Settings.get("pas_http_theme_plugins_supported", True)) else None)
			self.theme_renderer = NamedLoader.get_instance("dNG.pas.data.theme.Renderer")

			if (theme != None):
			#
				theme = re.sub("\W", "", theme)

				if (self.theme_renderer.is_supported(theme)): self.theme_active = theme
				else: theme = None
			#

			if (theme == None and (not self.theme_renderer.is_supported(self.theme))): self.theme = Settings.get("pas_http_theme_default", "simple")

			if (self.theme_active == None): self.theme_active = self.theme
			self.theme_renderer.set(self.theme_active)
			self.theme_renderer.set_log_handler(self.log_handler)
			self.theme_renderer.set_subtype(self.theme_subtype)
		#

		if (self.oset == None):
		#
			"""
Get the corresponding OSet name
			"""

			self.oset = Settings.get("pas_http_theme_{0}_oset".format(re.sub("\W", "_", self.theme)))
			if (self.oset == None): self.oset = Settings.get("pas_http_theme_oset_default", "xhtml5")
		#
	#

	def send(self):
	#
		"""
Sends the prepared response.

:since: v0.1.00
		"""

		if (self.data != None or self.stream_response.is_streamer_set()):
		#
			if (not self.initialized): self.init()
			self.send_headers()

			if (self.data != None): AbstractHttpResponse.send(self)
		#
		elif (self.content != None):
		#
			if (self.title != None): self.theme_renderer.set_title(self.title)

			self.data = Binary.utf8_bytes(self.theme_renderer.render(self.content))

			if ("application/xhtml+xml" in self.stream_response.get_accepted_formats()):
			#
				if (self.get_content_type() == None): self.set_content_type("application/xhtml+xml; charset={0}".format(self.charset))
			#
			elif (self.get_content_type() == None):
			#
				self.set_content_type("text/html; charset={0}".format(self.charset))
			#

			self.send()
		#
		elif (not self.are_headers_sent()):
		#
			"""
If raw data are send using "send_raw_data()" headers will be sent. An error
occurred if they are not sent and all buffers are "None".
			"""

			self.init(False, True)
			self.content = ""

			if (self.errors == None):
			#
				header = self.get_header("HTTP/1.1", True)
				if (header == None): self.set_header("HTTP/1.1", "HTTP/1.1 500 Internal Server Error", True)

				error = { "title": L10n.get("core_title_error_critical"), "message": (L10n.get("errors_core_unknown_error") if (header == None) else header) }

				self.add_oset_content("core.error", error)
				self.set_title(error['title'])
			#
			else:
			#
				for error in self.errors:
				#
					self.add_oset_content("core.error", error)
					self.set_title(error['title'])
				#
			#

			self.send()
		#
	#

	def set_oset(self, oset):
	#
		"""
Sets the OSet to use.

:param oset: OSet name

:since: v0.1.00
		"""

		self.oset = oset
	#

	def set_theme(self, theme):
	#
		"""
Sets the theme to use.

:param theme: Output theme

:since: v0.1.00
		"""

		self.theme = re.sub("\\W", "", theme)
		if (self.theme_renderer != None and self.theme_renderer.is_supported(theme)): self.theme_renderer.set(theme)
	#
#

##j## EOF