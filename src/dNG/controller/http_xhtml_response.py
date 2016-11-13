# -*- coding: utf-8 -*-

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

from dNG.data.binary import Binary
from dNG.data.settings import Settings
from dNG.data.text.l10n import L10n
from dNG.data.xhtml.formatting import Formatting
from dNG.module.named_loader import NamedLoader
from dNG.plugins.hook import Hook
from dNG.runtime.io_exception import IOException

from .abstract_http_request import AbstractHttpRequest
from .abstract_http_response import AbstractHttpResponse

class HttpXhtmlResponse(AbstractHttpResponse):
    """
The following class implements the response object for XHTML content.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self):
        """
Constructor __init__(HttpXhtmlResponse)

:since: v0.2.00
        """

        AbstractHttpResponse.__init__(self)

        self.content = None
        """
Content to be shown
        """
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
        self.theme_active_base_path = None
        """
Selected output theme file base path
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
        """
Add the defined Cascading Stylesheet file to the output.

:param css_file: CSS file name

:since: v0.2.00
        """

        if (self.theme_renderer is None): self.css_files_cache.append(css_file)
        else: self.theme_renderer.add_css_file(css_file)
    #

    def add_js_file(self, js_file):
        """
Add the defined JavaScript file to the output.

:param js_file: JS file name

:since: v0.2.00
        """

        common_names = Settings.get("pas_http_theme_oset_js_aliases", { "jquery/jquery.min.js": "jquery/jquery-2.1.1.min.js" })
        if (js_file in common_names): js_file = common_names[js_file]

        if (self.theme_renderer is None): self.js_files_cache.append(js_file)
        else: self.theme_renderer.add_js_file(js_file)
    #

    def add_oset_content(self, template_name, content = None):
        """
Add output content from an OSet template.

:param template_name: OSet template name
:param content: Content object

:since: v0.2.00
        """

        if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.add_oset_content({1})- (#echo(__LINE__)#)", self, template_name, context = "pas_http_core")

        parser = NamedLoader.get_instance("dNG.data.xhtml.oset.FileParser")
        parser.set_oset(self.oset)

        data = parser.render(template_name, content)

        if (data != ""):
            if (self.content is None): self.content = ""
            self.content += data
        #
    #

    def add_theme_css_file(self, css_file):
        """
Adds the requested theme CSS sprites to the output.

:param css_file: Theme CSS file

:since: v0.2.00
        """

        if (self.theme_renderer is None): self.theme_css_files_cache.append(css_file)
        else:
            css_file_path = path.join(self.get_theme_active_mmedia_base_path(),
                                      css_file
                                     )

            theme_name = (self.get_theme_active()
                          if (os.access(css_file_path, os.R_OK)) else
                          "default"
                         )

            theme_css_file = "themes/{0}/{1}".format(theme_name, css_file)

            self.add_css_file(theme_css_file)
        #
    #

    def get_oset(self):
        """
Returns the OSet in use.

:return: (str) OSet name
:since:  v0.2.00
        """

        return self.oset
    #

    def get_theme(self):
        """
Returns the theme to use.

:return: (str) Output theme
:since:  v0.2.00
        """

        return self.theme
    #

    def get_theme_active(self):
        """
Returns the active theme in use. This could be different from the requested
theme if plugins changed the selected theme renderer.

:return: (str) Active output theme
:since:  v0.2.00
        """

        return self.theme_active
    #

    def get_theme_active_mmedia_base_path(self):
        """
Returns the active output theme file base path.

:return: (str) Output theme file base path
:since:  v0.2.00
        """

        return self.theme_active_base_path
    #

    def init(self, cache = False, compress = True):
        """
Important headers will be created here. This includes caching, cookies and
compression setting used.

:param cache: Allow caching at client
:param compress: Send page GZip encoded (if supported)

:since: v0.2.00
        """

        if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.init()- (#echo(__LINE__)#)", self, context = "pas_http_core")

        AbstractHttpResponse.init(self, cache, compress)

        self._init_theme_renderer()

        if (self.oset is None):
            oset = Settings.get("pas_http_theme_{0}_oset".format(self.theme_active))
            if (oset is None): oset = Settings.get("pas_http_theme_oset_default", "xhtml5")

            self.set_oset(oset)
        #
    #

    def _init_theme_renderer(self):
        """
Set up theme framework if renderer has not already been initialized.

:since: v0.2.00
        """

        if (self.theme_renderer is None):
            if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}._init_theme_renderer()- (#echo(__LINE__)#)", self, context = "pas_http_core")

            Settings.read_file("{0}/settings/pas_http_theme.json".format(Settings.get("path_data")))

            if (self.theme is None):
                theme = AbstractHttpRequest.get_instance().get_parameter("theme")
                if (theme is not None): self._set_theme(theme)
            #

            theme = (Hook.call("dNG.pas.http.Theme.checkCandidates", theme = self.theme)
                     if (Settings.get("pas_http_theme_plugins_supported", True)) else
                     None
                    )

            self.theme_renderer = NamedLoader.get_instance("dNG.data.xhtml.theme.Renderer")

            if (theme is not None):
                theme = re.sub("\\W", "", theme)

                if (self.theme_renderer.is_supported(theme)): self.theme_active = theme
                else: theme = None
            #

            if (theme is None
                and (not self.theme_renderer.is_supported(self.theme))
               ): self.theme = self.theme_renderer.__class__.get_default_theme()

            if (self.theme_active is None):
                self.theme_active = (self.theme if (self.theme_renderer.is_supported(self.theme)) else "simple")
            #

            Settings.set("x_pas_http_theme", self.theme)

            self.theme_active_base_path = path.join(Settings.get("path_data"),
                                                    "mmedia",
                                                    "themes",
                                                    self.theme_active
                                                   )

            self.theme_renderer.set(self.theme_active)
            self.theme_renderer.set_log_handler(self.log_handler)
            self.theme_renderer.set_subtype(self.theme_subtype)

            if (len(self.html_canonical_url_parameters) > 0):
                self.theme_renderer.set_canonical_url_parameters(self.html_canonical_url_parameters)
            elif (self.html_canonical_url != ""): self.theme_renderer.set_canonical_url(self.html_canonical_url)

            if (self.html_page_description != ""): self.theme_renderer.set_page_description(self.html_page_description)

            for css_file in self.css_files_cache: self.add_css_file(css_file)
            self.css_files_cache = [ ]

            for js_file in self.js_files_cache: self.add_js_file(js_file)
            self.js_files_cache = [ ]

            for theme_css_file in self.theme_css_files_cache: self.add_theme_css_file(theme_css_file)
            self.theme_css_files_cache = [ ]
        #
    #

    def reset(self):
        """
Resets all cached values.

:since: v0.2.00
        """

        AbstractHttpResponse.reset(self)
        self.content = None
    #

    def send(self):
        """
Sends the prepared response.

:since: v0.2.00
        """

        if (self.data is not None or self.stream_response.is_streamer_set()):
            if (not self.initialized): self.init()
            self.send_headers()

            if (self.data is not None): AbstractHttpResponse.send(self)
        elif (self.content is not None):
            self._init_theme_renderer()
            if (self.title is not None): self.theme_renderer.set_title(self.title)

            is_xhtml_supported = ("application/xhtml+xml" in self.stream_response.get_accepted_formats())

            if (not is_xhtml_supported):
                self.stream_response.set_compression(False)
                self.theme_renderer.add_js_file("xhtml5/html5shiv.min.js")
            #

            if (self.get_content_type() is None):
                if (is_xhtml_supported): self.set_content_type("application/xhtml+xml; charset={0}".format(self.charset))
                else: self.set_content_type("text/html; charset={0}".format(self.charset))
            #

            data = self.theme_renderer.render(self.content)
            if (not is_xhtml_supported): data = Formatting.rewrite_legacy_html(data)

            self.data = Binary.utf8_bytes(data)
            self.send()
        elif (not self.are_headers_sent()):
            """
If raw data are send using "send_raw_data()" headers will be sent. An error
occurred if they are not sent and all buffers are "None".
            """

            self.init()
            self.content = ""

            if (self.errors is None):
                header = self.get_header("HTTP/1.1", True)
                if (header is None): self.set_header("HTTP/1.1", "HTTP/1.1 500 Internal Server Error", True)

                error = { "title": L10n.get("core_title_error_critical"),
                          "message": (L10n.get("errors_core_unknown_error") if (header is None) else header)
                        }

                self.add_oset_content("core.error", error)
                self.set_title(error['title'])
            else:
                for error in self.errors:
                    self.add_oset_content("core.error", error)
                    self.set_title(error['title'])
                #
            #

            self.send()
        #
    #

    def set_content(self, content):
        """
Sets the content for the response.

:param content: Content to be send

:since: v0.2.00
        """

        if (self.data is not None): raise IOException("Can't combine content and raw data in one response.")
        if (self.stream_response.is_streamer_set()): raise IOException("Can't combine a streaming object with content.")

        self.content = content
    #

    def set_html_canonical_url(self, url):
        """
Sets the (X)HTML canonical URL of the response.

:param url: Canonical URL

:since: v0.2.00
        """

        self.html_canonical_url = url
        if (self.initialized and self.theme_renderer is not None): self.theme_renderer.set_canonical_url(url)
    #

    def set_html_canonical_url_parameters(self, parameters):
        """
Sets the (X)HTML canonical URL of the response based on the parameters
given.

:param parameters: Parameters dict

:since: v0.2.00
        """

        self.html_canonical_url_parameters = parameters
        if (self.initialized and self.theme_renderer is not None): self.theme_renderer.set_canonical_url_parameters(parameters)
    #

    def set_html_page_description(self, description):
        """
Sets the (X)HTML head description of the response.

:param description: Head description

:since: v0.2.00
        """

        self.html_page_description = description
        if (self.initialized and self.theme_renderer is not None): self.theme_renderer.set_page_description(description)
    #

    def set_oset(self, oset):
        """
Sets the OSet to use.

:param oset: OSet name

:since: v0.2.00
        """

        if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_oset({1})- (#echo(__LINE__)#)", self, oset, context = "pas_http_core")

        self.oset = oset
        Settings.set("x_pas_http_oset", self.oset)
    #

    def set_raw_data(self, data):
        """
"set_raw_data()" ignores any protocol specification and buffer the data as
given.

:param data: Data to be send

:since: v0.2.00
        """

        if (self.content is not None): raise IOException("Can't combine raw data and content in one response.")
        AbstractHttpResponse.set_raw_data(self, data)
    #

    def _set_theme(self, theme):
        """
Sets the theme to use. This function does not change CSS and JavaScript
files already set. Use with care.

:param theme: Output theme

:since: v0.2.00
        """

        if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}._set_theme({1})- (#echo(__LINE__)#)", self, theme, context = "pas_http_core")
        self.theme = re.sub("\\W", "", theme)

        if (self.theme_renderer is not None and self.theme_renderer.is_supported(theme)):
            self.theme_active_base_path = path.join(Settings.get("path_data"),
                                                    "mmedia",
                                                    "themes",
                                                    theme
                                                   )

            self.theme_renderer.set(theme)
            Settings.set("x_pas_http_theme", theme)
        #
    #

    def set_theme_subtype(self, subtype):
        """
Sets the theme subtype to use.

:param subtype: Output theme subtype

:since: v0.2.00
        """

        subtype = Binary.str(subtype)
        if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_theme_subtype({1})- (#echo(__LINE__)#)", self, subtype, context = "pas_http_core")

        self.theme_subtype = subtype
    #

    def set_title(self, title):
        """
Sets the response page title.

:param title: Response page title

:since: v0.2.00
        """

        if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_title({1})- (#echo(__LINE__)#)", self, title, context = "pas_http_core")

        self.title = title
    #
#
