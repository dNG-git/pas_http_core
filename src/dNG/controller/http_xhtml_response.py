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
from dNG.data.xhtml.link import Link
from dNG.plugins.hook import Hook
from dNG.runtime.io_exception import IOException
from dNG.runtime.named_loader import NamedLoader

from .abstract_http_request import AbstractHttpRequest
from .abstract_http_response import AbstractHttpResponse

class HttpXhtmlResponse(AbstractHttpResponse):
    """
The following class implements the response object for XHTML content.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self):
        """
Constructor __init__(HttpXhtmlResponse)

:since: v1.0.0
        """

        AbstractHttpResponse.__init__(self)

        self._content = None
        """
Content to be shown
        """
        self.css_files_cache = [ ]
        """
CSS files to be added.
        """
        self._description = None
        """
(X)HTML head description
        """
        self._canonical_url = None
        """
(X)HTML canonical URL of the response
        """
        self.js_files_cache = [ ]
        """
JavaScript files to be added.
        """
        self._oset = None
        """
OSet in use (requested or configured)
        """
        self._theme = None
        """
Output theme (requested or configured)
        """
        self._theme_active = None
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
        self._theme_renderer = None
        """
Selected theme renderer
        """
        self._theme_subtype = "site"
        """
Output theme subtype
        """
        self._title = None
        """
(X)HTML head title
        """
        self.webc_files_cache = [ ]
        """
WebComponents files to be added.
        """

        self.supported_features['canonical_url'] = True
        self.supported_features['html_content'] = True
        self.supported_features['html_css_files'] = True
        self.supported_features['html_js_files'] = True
        self.supported_features['html_page_description'] = True
        self.supported_features['html_page_title'] = True
        self.supported_features['html_oset'] = True
        self.supported_features['html_theme'] = True
        self.supported_features['html_webc_files'] = True
    #

    @property
    def canonical_url(self):
        """
Returns the (X)HTML canonical URL of the response.

:return: (str) Canonical URL
:since:  v1.0.0
        """

        return ("" if (self._canonical_url is None) else self._canonical_url)
    #

    @canonical_url.setter
    def canonical_url(self, url):
        """
Sets the (X)HTML canonical URL of the response.

:param url: Canonical URL

:since: v1.0.0
        """

        self._canonical_url = url
        if (self.initialized and self._theme_renderer is not None): self.theme_renderer.canonical_url = url
    #

    @property
    def content(self):
        """
Returns the content for the response.

:return: (str) Content to be send
:since:  v1.0.0
        """

        return self._content
    #

    @content.setter
    def content(self, content):
        """
Sets the content for the response.

:param content: Content to be send

:since: v1.0.0
        """

        if (self.raw_data is not None): raise IOException("Can't combine content and raw data in one response.")
        if (self.stream_response.is_streamer_set): raise IOException("Can't combine a streaming object with content.")

        self._content = content
    #

    @property
    def data(self):
        """
Returns buffered data to be transmitted.

:return: (bytes) Data to be send
:since:  v1.0.0
        """

        return Binary.utf8_bytes(self._data)
    #

    @property
    def page_description(self):
        """
Returns the (X)HTML head description of the response.

:return: (str) Response description
:since:  v1.0.0
        """

        return ("" if (self._description is None) else self._description)
    #

    @page_description.setter
    def page_description(self, description):
        """
Sets the (X)HTML head description of the response.

:param description: Response description

:since: v1.0.0
        """

        self._description = description
        if (self.initialized and self._theme_renderer is not None): self.theme_renderer.description = description
    #

    @property
    def page_title(self):
        """
Return the (X)HTML head title set for the response.

:return: (str) Response title
:since:  v1.0.0
        """

        return self._title
    #

    @page_title.setter
    def page_title(self, title):
        """
Sets the (X)HTML head title set for the response.

:param title: Response title

:since: v1.0.0
        """

        self._title = title
        if (self.initialized and self._theme_renderer is not None): self.theme_renderer.title = title
    #

    @property
    def oset(self):
        """
Returns the OSet in use.

:return: (str) OSet name
:since:  v1.0.0
        """

        return self._oset
    #

    @oset.setter
    def oset(self, oset):
        """
Sets the OSet to use.

:param oset: OSet name

:since: v1.0.0
        """

        self._oset = oset
        Settings.set("x_pas_http_oset", self._oset)
    #

    @AbstractHttpResponse.raw_data.setter
    def raw_data(self, data):
        """
Raw data ignores any protocol specific transformation and buffers the data as
given.

:param data: Data to be send

:since: v1.0.0
        """

        if (self.content is not None): raise IOException("Can't combine raw data and content in one response.")
        AbstractHttpResponse.raw_data.fset(self, data)
    #

    @property
    def theme(self):
        """
Returns the theme to use.

:return: (str) Output theme
:since:  v1.0.0
        """

        return (self.theme_active if (self._theme is None) else self._theme)
    #

    @property
    def theme_active(self):
        """
Returns the active theme in use. This could be different from the requested
theme if plugins changed the selected theme renderer.

:return: (str) Active output theme
:since:  v1.0.0
        """

        return self._theme_active
    #

    @property
    def theme_renderer(self):
        """
Returns the theme renderer selected.

:return: (str) Selected theme renderer
:since:  v1.0.0
        """

        if (self._theme_renderer is None): self._init_theme_renderer()
        return self._theme_renderer
    #

    @property
    def theme_subtype(self):
        """
Returns the theme subtype to use.

:return: (str) Output theme subtype
:since:  v1.0.0
        """

        return self._theme_subtype
    #

    @theme_subtype.setter
    def theme_subtype(self, subtype):
        """
Sets the theme subtype to use.

:param subtype: Output theme subtype

:since: v1.0.0
        """

        self._theme_subtype = subtype
        if (self._theme_renderer is not None): self._theme_renderer.theme_subtype = subtype
    #

    def add_css_file(self, css_file):
        """
Add the defined Cascading Stylesheet file to the output.

:param css_file: CSS file name

:since: v1.0.0
        """

        if (self._theme_renderer is None): self.css_files_cache.append(css_file)
        else: self.theme_renderer.add_css_file(css_file)
    #

    def add_js_file(self, js_file):
        """
Add the defined JavaScript file to the output.

:param js_file: JS file name

:since: v1.0.0
        """

        common_names = Settings.get("pas_http_theme_oset_js_aliases", { })
        if (js_file in common_names): js_file = common_names[js_file]

        if (self._theme_renderer is None): self.js_files_cache.append(js_file)
        else: self.theme_renderer.add_js_file(js_file)
    #

    def add_oset_content(self, template_name, content = None):
        """
Add output content from an OSet template.

:param template_name: OSet template name
:param content: Content object

:since: v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -{0!r}.add_oset_content({1})- (#echo(__LINE__)#)", self, template_name, context = "pas_http_core")

        parser = NamedLoader.get_instance("dNG.data.xhtml.oset.FileParser")
        parser.oset = self.oset

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

:since: v1.0.0
        """

        if (self._theme_renderer is None): self.theme_css_files_cache.append(css_file)
        else:
            css_file_path = path.join(self.theme_active_base_path, css_file)
            theme_name = (self.theme_active if (os.access(css_file_path, os.R_OK)) else "default")

            theme_css_file = "themes/{0}/{1}".format(theme_name, css_file)

            self.add_css_file(theme_css_file)
        #
    #

    def add_webc_file(self, webc_file):
        """
Adds the requested theme WebComponent file to the output.

:param webc_file: WebComponent file

:since: v1.0.0
        """

        if (self._theme_renderer is None): self.webc_files_cache.append(webc_file)
        else:
            if (not os.access(webc_file, os.R_OK)):
                webc_file_path = path.join(self.theme_active_base_path, webc_file)
                theme_name = (self.theme_active if (os.access(webc_file_path, os.R_OK)) else "default")

                webc_file = "themes/{0}/{1}".format(theme_name, webc_file)
            #

            self.theme_renderer.add_webc_file(webc_file)
        #
    #

    def init(self, cache = False, compress = True):
        """
Important headers will be created here. This includes caching, cookies and
compression setting used.

:param cache: Allow caching at client
:param compress: Send page GZip encoded (if supported)

:since: v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -{0!r}.init()- (#echo(__LINE__)#)", self, context = "pas_http_core")

        AbstractHttpResponse.init(self, cache, compress)

        self._init_theme_renderer()

        if (self.oset is None):
            oset = Settings.get("pas_http_theme_{0}_oset".format(self.theme_active))
            if (oset is None): oset = Settings.get("pas_http_theme_oset_default", "xhtml5")

            self.oset = oset
        #
    #

    def _init_theme_renderer(self):
        """
Set up theme framework if renderer has not already been initialized.

:since: v1.0.0
        """

        if (self._theme_renderer is None):
            if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -{0!r}._init_theme_renderer()- (#echo(__LINE__)#)", self, context = "pas_http_core")

            Settings.read_file("{0}/settings/pas_http_theme.json".format(Settings.get("path_data")))

            if (self._theme is None):
                theme = AbstractHttpRequest.get_instance().get_parameter("theme")
                if (theme is not None): self._theme = theme
            #

            theme = (Hook.call("dNG.pas.http.Theme.checkCandidates", theme = self._theme)
                     if (Settings.get("pas_http_theme_plugins_supported", True)) else
                     None
                    )

            if (theme is not None): theme = re.sub("\\W", "", theme)

            self._theme_renderer = NamedLoader.get_instance("dNG.data.xhtml.theme.Renderer")
            self._theme_renderer.theme = (self._theme if (theme is None) else theme)

            self._theme_active = self._theme_renderer.theme

            Settings.set("x_pas_http_theme", self.theme)

            self.theme_active_base_path = path.join(Settings.get("path_data"),
                                                    "assets",
                                                    "themes",
                                                    self.theme_active
                                                   )

            self._theme_renderer.log_handler = self._log_handler
            self._theme_renderer.theme = self.theme_active
            self._theme_renderer.theme_subtype = self.theme_subtype

            if (self._description is not None): self._theme_renderer.description = self._description
            if (self._canonical_url is not None): self._theme_renderer.canonical_url = self.canonical_url

            for css_file in self.css_files_cache: self.add_css_file(css_file)
            self.css_files_cache = [ ]

            for js_file in self.js_files_cache: self.add_js_file(js_file)
            self.js_files_cache = [ ]

            for theme_css_file in self.theme_css_files_cache: self.add_theme_css_file(theme_css_file)
            self.theme_css_files_cache = [ ]

            for webc_file in self.webc_files_cache: self.add_webc_file(webc_file)
            self.webc_files_cache = [ ]
        #
    #

    def _prepare_error_response(self):
        """
Prepares an error response.

:since: v1.0.0
        """

        errors = self.errors
        self.reset()

        if (not self.are_headers_sent):
            self.init(False, True)

            header = self.get_header("HTTP", True)
            if (header is None): self.set_header("HTTP", "HTTP/2.0 500 Internal Server Error", True)
        #

        self.content = ""

        if (errors is None):
            error = { "title": L10n.get("core_title_error"),
                      "message": (L10n.get("errors_core_unknown_error") if (header is None) else header)
                    }

            self.page_title = error['title']

            self.add_oset_content("core.error", error)
        else:
            for error in errors:
                if (self.page_title is None): self.page_title = error['title']
                self.add_oset_content("core.error", error)
            #
        #
    #

    def redirect(self, url):
        """
Redirect the requesting client to the given URL.

:param url: Target URL

:since: v1.0.0
        """

        AbstractHttpResponse.redirect(self, url)

        if (self.page_title is None): self.page_title = L10n.get("pas_http_core_loading_additional_data")
        self.add_oset_content("core.redirection", { "url": url })
    #

    def reset(self):
        """
Resets all cached values.

:since: v1.0.0
        """

        AbstractHttpResponse.reset(self)

        self._content = None
        self._title = None
    #

    def send(self):
        """
Sends the prepared response.

:since: v1.0.0
        """

        if (self.errors is not None): self._prepare_error_response()

        if (self._data is not None or self.stream_response.is_streamer_set):
            if (not self.initialized): self.init()
            self.send_headers()

            AbstractHttpResponse.send(self)
        elif (self.content is not None):
            self._init_theme_renderer()
            if (self._title is not None): self.theme_renderer.title = self._title

            is_xhtml_encoded = self.theme_renderer.get_setting("xhtml5_format", True)

            accepted_formats = self.stream_response.accepted_formats

            is_xhtml_supported = ("application/xhtml+xml" in accepted_formats
                                  or len(accepted_formats) == 1 and accepted_formats[0] == "*/*"
                                 )

            if (not is_xhtml_supported):
                self.stream_response.compress_output = False
                self.theme_renderer.add_js_file("js/es5/html5shiv.min.js")
            #

            if (self.content_type is None):
                self.content_type = ("application/xhtml+xml; charset={0}"
                                     if (is_xhtml_encoded and is_xhtml_supported) else
                                     "text/html; charset={0}"
                                    ).format(self.charset)
            #

            data = self.theme_renderer.render(self.content)
            if (not is_xhtml_supported): data = Formatting.rewrite_legacy_html(data)

            self._data = data
            self.send()
        else:
            self._prepare_error_response()
            self.send()
        #
    #

    def set_canonical_url_parameters(self, parameters):
        """
Sets the (X)HTML canonical URL of the response based on the parameters
given.

:param parameters: Parameters dict

:since: v1.0.0
        """

        _type = (Link.TYPE_RELATIVE_URL
                 if (Settings.get("pas_http_site_canonical_url_type", "absolute") == "relative") else
                 Link.TYPE_ABSOLUTE_URL
                )

        self.canonical_url = Link().build_url(_type, parameters)
    #

    def _set_theme(self, theme):
        """
Sets the theme to use. This function does not change CSS and JavaScript
files already set. Use with care.

:param theme: Output theme

:since: v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -{0!r}._set_theme({1})- (#echo(__LINE__)#)", self, theme, context = "pas_http_core")
        self.theme = re.sub("\\W", "", theme)

        if (self._theme_renderer is not None and self.theme_renderer.is_supported(theme)):
            self.theme_active_base_path = path.join(Settings.get("path_data"),
                                                    "assets",
                                                    "themes",
                                                    theme
                                                   )

            self.theme_renderer.theme = theme
            Settings.set("x_pas_http_theme", theme)
        #
    #
#
