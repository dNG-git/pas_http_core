# -*- coding: utf-8 -*-
##j## BOF

"""
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
"""

import re

from dNG.pas.data.binary import Binary
from dNG.pas.data.settings import Settings
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.xhtml.formatting import Formatting
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.plugins.hook import Hook
from .abstract_http_request import AbstractHttpRequest
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

		self.css_files_cache = [ ]
		"""
CSS files to be added.
		"""
		self.js_files_cache = [ ]
		"""
JavaScript files to be added.
		"""
		self.html_canonical_url = ""
		"""
(X)HTML canonical URL of the response
		"""
		self.html_canonical_url_parameters = { }
		"""
(X)HTML canonical URL parameters of the response
		"""
		self.html_page_description = ""
		"""
(X)HTML head description
		"""
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
		self.theme_css_files_cache = [ ]
		"""
CSS files to be added.
		"""
		self.theme_renderer = None
		"""
Selected theme renderer
		"""
		self.theme_subtype = "site"
		"""
Output theme subtype
		"""
		self.title = None
		"""
Response page title
		"""

		self.supported_features['html_canonical_url'] = True
		self.supported_features['html_css_files'] = True
		self.supported_features['html_js_files'] = True
		self.supported_features['html_page_description'] = True
		self.supported_features['html_theme'] = True
	#

	def add_css_file(self, css_file):
	#
		"""
Add the defined Cascading Stylesheet file to the output.

:param css_file: CSS file name

:since: v0.1.00
		"""

		if (self.theme_renderer == None): self.css_files_cache.append(css_file)
		else: self.theme_renderer.add_css_file(css_file)
	#

	def add_js_file(self, js_file):
	#
		"""
Add the defined JavaScript file to the output.

:param js_file: JS file name

:since: v0.1.00
		"""

		common_names = Settings.get("pas_http_theme_oset_js_aliases", { "jquery/jquery.min.js": "jquery/jquery-2.1.1.min.js" })
		if (js_file in common_names): js_file = common_names[js_file]

		if (self.theme_renderer == None): self.js_files_cache.append(js_file)
		else: self.theme_renderer.add_js_file(js_file)
	#

	def add_oset_content(self, template_name, content = None):
	#
		"""
Add output content from an OSet template.

:param template_name: OSet template name
:param content: Content object

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.add_oset_content({1})- (#echo(__LINE__)#)", self, template_name, context = "pas_http_core")

		parser = NamedLoader.get_instance("dNG.pas.data.xhtml.oset.FileParser")
		parser.set_oset(self.oset)

		data = parser.render(template_name, content)

		if (data != ""):
		#
			if (self.content == None): self.content = ""
			self.content += data
		#
	#

	def add_theme_css_file(self, css_file):
	#
		"""
Adds the requested CSS sprites to the output.

:param css_file: Theme CSS file

:since: v0.1.01
		"""

		if (self.theme_renderer == None): self.theme_css_files_cache.append(css_file)
		else:
		#
			theme_css_file = "themes/{0}/{1}".format(self.get_theme_active(),
			                                         css_file
			                                        )

			self.add_css_file(theme_css_file)
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

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.init()- (#echo(__LINE__)#)", self, context = "pas_http_core")

		AbstractHttpResponse.init(self, cache, compress)

		p3p_url = ""

		if (self.stream_response.is_supported("headers")):
		#
			"""
Send P3P header if defined
			"""

			p3p_cp = Settings.get("pas_http_core_p3p_cp", "")
			p3p_url = Settings.get("pas_http_core_p3p_url", "").replace("&", "&amp;")

			if (p3p_cp + p3p_url != ""):
			#
				p3p_data = ("" if (p3p_url == "") else "policyref=\"{0}\"".format(p3p_url))

				if (p3p_cp != ""):
				#
					if (p3p_data != ""): p3p_data += ","
					p3p_data += "CP=\"{0}\"".format(p3p_cp)
				#

				self.stream_response.set_header("P3P", p3p_data)
			#
		#

		if (self.theme_renderer == None):
		#
			"""
Set up theme framework
			"""

			Settings.read_file("{0}/settings/pas_http_theme.json".format(Settings.get("path_data")))

			if (self.theme == None):
			#
				theme = AbstractHttpRequest.get_instance().get_parameter("theme")
				if (theme != None): self.set_theme(theme)
			#

			theme = (Hook.call("dNG.pas.http.Theme.checkCandidates", theme = self.theme) if (Settings.get("pas_http_theme_plugins_supported", True)) else None)
			self.theme_renderer = NamedLoader.get_instance("dNG.pas.data.xhtml.theme.Renderer")

			if (theme != None):
			#
				theme = re.sub("\\W", "", theme)

				if (self.theme_renderer.is_supported(theme)): self.theme_active = theme
				else: theme = None
			#

			if (theme == None and (not self.theme_renderer.is_supported(self.theme))): self.theme = Settings.get("pas_http_site_theme_default", "simple")
			if (self.theme_active == None): self.theme_active = (self.theme if (self.theme_renderer.is_supported(self.theme)) else "simple")

			self.theme_renderer.set(self.theme_active)
			self.theme_renderer.set_log_handler(self.log_handler)
			self.theme_renderer.set_subtype(self.theme_subtype)

			if (len(self.html_canonical_url_parameters) > 0): self.theme_renderer.set_canonical_url_parameters(self.html_canonical_url_parameters)
			elif (self.html_canonical_url != ""): self.theme_renderer.set_canonical_url(self.html_canonical_url)

			if (self.html_page_description != ""): self.theme_renderer.set_page_description(self.html_page_description)
			if (p3p_url != ""): self.theme_renderer.set_p3p_url(p3p_url)

			for css_file in self.css_files_cache: self.add_css_file(css_file)
			for js_file in self.js_files_cache: self.add_js_file(js_file)
			for theme_css_file in self.theme_css_files_cache: self.add_theme_css_file(theme_css_file)
		#

		if (self.oset == None):
		#
			"""
Get the corresponding OSet name
			"""

			self.oset = Settings.get("pas_http_theme_{0}_oset".format(self.theme_active))
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

			is_xhtml_supported = ("application/xhtml+xml" in self.stream_response.get_accepted_formats())

			if (not is_xhtml_supported):
			#
				self.stream_response.set_compression(False)
				self.theme_renderer.add_js_file("xhtml5/html5shiv.min.js")
			#

			if (self.get_content_type() == None):
			#
				if (is_xhtml_supported): self.set_content_type("application/xhtml+xml; charset={0}".format(self.charset))
				else: self.set_content_type("text/html; charset={0}".format(self.charset))
			#

			data = self.theme_renderer.render(self.content)
			if (not is_xhtml_supported): data = Formatting.rewrite_legacy_html(data)

			self.data = Binary.utf8_bytes(data)
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

	def set_html_canonical_url(self, url):
	#
		"""
Sets the (X)HTML canonical URL of the response.

:param url: Canonical URL

:since: v0.1.00
		"""

		self.html_canonical_url = url
		if (self.initialized and self.theme_renderer != None): self.theme_renderer.set_canonical_url(url)
	#

	def set_html_canonical_url_parameters(self, parameters):
	#
		"""
Sets the (X)HTML canonical URL of the response based on the parameters
given.

:param parameters: Parameters dict

:since: v0.1.00
		"""

		self.html_canonical_url_parameters = parameters
		if (self.initialized and self.theme_renderer != None): self.theme_renderer.set_canonical_url_parameters(parameters)
	#

	def set_html_page_description(self, description):
	#
		"""
Sets the (X)HTML head description of the response.

:param description: Head description

:since: v0.1.00
		"""

		self.html_page_description = description
		if (self.initialized and self.theme_renderer != None): self.theme_renderer.set_page_description(description)
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

	def set_title(self, title):
	#
		"""
Sets the response page title.

:param title: Response page title

:since: v0.1.01
		"""

		self.title = title
	#
#

##j## EOF