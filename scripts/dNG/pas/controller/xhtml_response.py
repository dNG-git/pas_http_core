# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.controller.xhtml_response
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

from dNG.pas.data.settings import direct_settings
from dNG.pas.data.text.l10n import direct_l10n
from dNG.pas.module.named_loader import direct_named_loader
from dNG.pas.plugins.hooks import direct_hooks
from .abstract_http_response import direct_abstract_http_response

class direct_xhtml_response(direct_abstract_http_response):
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
Constructor __init__(direct_xhtml_response)

:since: v0.1.00
		"""

		direct_abstract_http_response.__init__(self)

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

	def add_oset_content(self, template_name, content = None):
	#
		"""
Add output content from an OSet template.

:param template_name: OSet template name
:param content: Content object

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.add_oset_content({0}, content)- (#echo(__LINE__)#)".format(template_name))

		parser = direct_named_loader.get_instance("dNG.pas.data.oset.file_parser")
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

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.get_oset()- (#echo(__LINE__)#)")
		return self.oset
	#

	def get_theme(self):
	#
		"""
Returns the theme to use.

:return: (str) Output theme
:since:  v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.get_theme()- (#echo(__LINE__)#)")
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

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.get_theme_active()- (#echo(__LINE__)#)")
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

		direct_abstract_http_response.init(self, cache, compress)

		"""
Set up theme framework
		"""

		direct_settings.read_file("{0}/settings/pas_http_theme.json".format(direct_settings.get("path_data")))
		theme = (direct_hooks.call("dNG.pas.http.theme.check_candidates", theme = self.theme) if (direct_settings.get("pas_http_theme_plugins_supported", True)) else None)
		self.theme_renderer = direct_named_loader.get_instance("dNG.pas.data.theme.renderer")

		if (theme != None):
		#
			theme = re.sub("\W", "", theme)

			if (self.theme_renderer.is_supported(theme)): self.theme_active = theme
			else: theme = None
		#

		if (theme == None and (not self.theme_renderer.is_supported(self.theme))): self.theme = direct_settings.get("pas_http_theme_default", "simple")

		if (self.theme_active == None): self.theme_active = self.theme
		self.theme_renderer.set(self.theme_active)
		self.theme_renderer.set_log_handler(self.log_handler)
		self.theme_renderer.set_subtype(self.theme_subtype)
	#

	def send(self):
	#
		"""
Sends the prepared response.

:since: v0.1.00
		"""

		if (not self.initialized): self.init()

		if (self.data != None): self.send_raw_data()
		elif (self.content != None):
		#
			if (self.title != None): self.theme_renderer.set_title(self.title)

			self.data = self.theme_renderer.render(self.content)

			if ("application/xhtml+xml" in self.get_accepted_formats()):
			#
				if (self.get_content_type() == None): self.set_content_type("application/xhtml+xml; charset={0}".format(self.charset))
			#
			elif (self.get_content_type() == None):
			#
				self.set_content_type("text/html; charset={0}".format(self.charset))
			#

			self.send()
		#
		elif (not self.headers_sent):
		#
			"""
If raw data are send using "send_raw_data()" headers will be sent. An error
occurred if they are not sent and all buffers are "None".
			"""

			header = self.get_header("HTTP/1.1", True)
			if (header == None): self.set_header("HTTP/1.1", "HTTP/1.1 500 Internal Server Error", True)

			self.content = ""

			if (self.errors == None):
			#
				error = { "title": direct_l10n.get("core_title_error_critical"), "message": (direct_l10n.get("errors_core_unknown_error") if (header == None) else header) }

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

	def send_raw_data(self, data = None):
	#
		"""
"send_raw_data()" ignores any protocol specification and send the data as
given.

:param data: Data to be send (buffer will be appended)

:since: v0.1.00
		"""

		if (not self.initialized): self.init()
		self.send_headers()

		if (self.data != None):
		#
			self.stream_response.send_data(self.data)
			self.data = None
		#

		if (data != None): self.stream_response.send_data(data)
	#

	def set_oset(self, oset):
	#
		"""
Sets the OSet to use.

:param oset: OSet name

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.set_oset({0})- (#echo(__LINE__)#)".format(oset))
		self.oset = oset
	#

	def set_theme(self, theme):
	#
		"""
Sets the theme to use.

:param theme: Output theme

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -response.set_theme()- (#echo(__LINE__)#)".format(theme))

		self.theme = re.sub("\\W", "", theme)
		if (self.theme_renderer != None and self.theme_renderer.is_supported(theme)): self.theme_renderer.set(theme)
	#
#

##j## EOF