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

from copy import copy
from os import path
import os
import re

from dNG.controller.abstract_request import AbstractRequest
from dNG.controller.abstract_response import AbstractResponse
from dNG.data.binary import Binary
from dNG.data.file import File
from dNG.data.settings import Settings
from dNG.data.text.input_filter import InputFilter
from dNG.data.text.l10n import L10n
from dNG.data.text.tag_parser.abstract import Abstract as AbstractTagParser
from dNG.data.text.tag_parser.each_mixin import EachMixin
from dNG.data.text.tag_parser.if_condition_mixin import IfConditionMixin
from dNG.data.text.tag_parser.rewrite_mixin import RewriteMixin
from dNG.data.xhtml.content_link_renderer import ContentLinkRenderer
from dNG.data.xhtml.formatting import Formatting
from dNG.data.xhtml.link import Link
from dNG.data.xhtml.tag_parser.block_mixin import BlockMixin
from dNG.module.named_loader import NamedLoader
from dNG.runtime.io_exception import IOException

class Renderer(BlockMixin, EachMixin, IfConditionMixin, RewriteMixin, AbstractTagParser):
    """
The theme renderer parses and renders a template file.

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
Constructor __init__(Renderer)

:since: v0.2.00
        """

        AbstractTagParser.__init__(self)
        BlockMixin.__init__(self)
        EachMixin.__init__(self)
        IfConditionMixin.__init__(self)
        RewriteMixin.__init__(self)

        self.cache_instance = NamedLoader.get_singleton("dNG.data.cache.Content", False)
        """
Cache instance
        """
        self.canonical_url = ""
        """
(X)HTML canonical URL of the response
        """
        self.content = None
        """
Content cache for OSet template replacements
        """
        self.css_files = [ ]
        """
CSS files to be added.
        """
        self.js_files = [ ]
        """
JavaScript files to be added.
        """
        self.log_handler = NamedLoader.get_singleton("dNG.data.logging.LogHandler", False)
        """
The LogHandler is called whenever debug messages should be logged or errors
happened.
        """
        self.page_description = ""
        """
(X)HTML head description
        """
        self.path = Settings.get("path_themes", "{0}/themes".format(Settings.get("path_data")))
        """
Path to the themes directory
        """
        self.theme = None
        """
Selected output theme
        """
        self.theme_subtype = "site"
        """
Output theme subtype
        """
        self.title = None
        """
Page title
        """
    #

    def add_css_file(self, css_file):
        """
Add the defined Cascading Stylesheet file to the output.

:param css_file: CSS file name

:since: v0.2.00
        """

        if (css_file not in self.css_files): self.css_files.append({ "name": css_file })
    #

    def add_js_file(self, js_file):
        """
Add the defined JavaScript file to the output.

:param js_file: JS file name

:since: v0.2.00
        """

        if (js_file not in self.js_files): self.js_files.append({ "name": js_file })
    #

    def is_supported(self, theme, subtype = None):
        """
Checks if the given theme and subtype is supported.

:param theme: Output theme
:param subtype: Output theme subtype

:return: (bool) True if supported
:since:  v0.2.00
        """

        _return = False

        if (theme is not None):
            file_path_name = path.join(self.path, theme.replace(".", "/"), "{0}.tsc".format("site" if (subtype is None) else subtype))
            _return = os.access(file_path_name, os.R_OK)
        #

        return _return
    #

    def _change_match(self, tag_definition, data, tag_position, data_position, tag_end_position):
        """
Change data according to the matched tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.2.00
        """

        _return = data[:tag_position]

        data_closed = data[self._find_tag_end_position(data, tag_end_position):]

        if (tag_definition['tag'] == "block"):
            re_result = re.match("^\\[block(:(\\w+):([\\w\\.]+)){0,1}\\]", data[tag_position:data_position])

            if (re_result is not None):
                if (re_result.group(1) is not None):
                    source = re_result.group(2)
                    key = re_result.group(3)
                else: source = None

                if (source is None): _return += self.render_block(data[data_position:tag_end_position])
                elif (source == "content"): _return += self.render_block(data[data_position:tag_end_position], "content", self._update_mapped_element("content", self.content), key)
                elif (source == "settings"):
                    runtime_settings_dict = AbstractResponse.get_instance().get_runtime_settings()
                    _return += self.render_block(data[data_position:tag_end_position], "settings", self._update_mapped_element("settings", runtime_settings_dict), key)
                #
            #
        elif (tag_definition['tag'] == "each"):
            re_result = re.match("^\\[each:(\\w+):([\\w\\.]+):([\\w\\.]+)\\]", data[tag_position:data_position])

            source = (None if (re_result is None) else re_result.group(1))

            if (source is not None):
                key = re_result.group(2)
                mapping_key = re_result.group(3)

                if (source == "content"): _return += self.render_each(data[data_position:tag_end_position], "content", self._update_mapped_element("content", self.content), key, mapping_key)
                elif (source == "settings"):
                    runtime_settings_dict = AbstractResponse.get_instance().get_runtime_settings()
                    _return += self.render_each(data[data_position:tag_end_position], "settings", self._update_mapped_element("settings", runtime_settings_dict), key, mapping_key)
                #
            #
        elif (tag_definition['tag'] == "if"):
            re_result = re.match("^\\[if:(\\w+):([\\w\\.]+)(\\s*)(\\!=|==)(.*?)\\]", data[tag_position:data_position])

            source = (None if (re_result is None) else re_result.group(1))

            if (source is not None):
                key = re_result.group(2)
                operator = re_result.group(4)
                value = re_result.group(5).strip()

                if (source == "content"): _return += self.render_if_condition(self._update_mapped_element("content", self.content), key, operator, value, data[data_position:tag_end_position])
                elif (source == "request"):
                    request = AbstractRequest.get_instance()
                    _return += self.render_if_condition({ 'lang': request.get_lang() } , key, operator, value, data[data_position:tag_end_position])
                elif (source == "settings"):
                    runtime_settings_dict = AbstractResponse.get_instance().get_runtime_settings()
                    _return += self.render_if_condition(self._update_mapped_element("settings", runtime_settings_dict), key, operator, value, data[data_position:tag_end_position])
                #
            #
        elif (tag_definition['tag'] == "link"):
            renderer = ContentLinkRenderer()
            tag_params = Renderer.parse_tag_parameters("link", data, tag_position, data_position)

            _return += renderer.render(data[data_position:tag_end_position], tag_params)
        elif (tag_definition['tag'] == "rewrite"):
            source = re.match("^\\[rewrite:(\\w+)(:.*)?\\]", data[tag_position:data_position]).group(1)
            key = data[data_position:tag_end_position]

            if (source == "content"): _return += self.render_rewrite(self._update_mapped_element("content", self.content), key)
            elif (source == "l10n"): _return += self.render_rewrite(self._update_mapped_element("l10n", L10n.get_dict()), key)
            elif (source == "settings"):
                runtime_settings_dict = AbstractResponse.get_instance().get_runtime_settings()
                _return += self.render_rewrite(self._update_mapped_element("settings", runtime_settings_dict), key)
            #
        #

        _return += data_closed

        return _return
    #

    def _check_match(self, data):
        """
Check if a possible tag match is a false positive.

:param data: Data starting with the possible tag

:return: (dict) Matched tag definition; None if false positive
:since:  v0.2.00
        """

        _return = None

        i = 0
        tags = [ "block", "each", "if", "rewrite" ]
        tags_length = len(tags)

        while (_return is None and i < tags_length):
            tag = tags[i]
            data_match = data[1:1 + len(tag)]

            if (data_match == "block"):
                re_result = re.match("^\\[block(:\\w+:[\\w\\.]+){0,1}\\]", data)
                if (re_result is not None): _return = { "tag": "block", "tag_end": "[/block]", "type": "top_down" }
            elif (data_match == "each"):
                re_result = re.match("^\\[each:\\w+:[\\w\\.]+:[\\w\\.]+\\]", data)
                if (re_result is not None): _return = { "tag": "each", "tag_end": "[/each]", "type": "top_down" }
            elif (data_match == "if"):
                re_result = re.match("^\\[if:\\w+:[\\w\\.]+\\s*(\\!=|==).*?\\]", data)
                if (re_result is not None): _return = { "tag": "if", "tag_end": "[/if]", "type": "top_down" }
            elif (data_match == "link"):
                re_result = re.match("^\\[link:(.+)\\]", data)
                if (re_result is not None): _return = { "tag": "link", "tag_end": "[/link]" }
            elif (data_match == "rewrite"):
                re_result = re.match("^\\[rewrite:(\\w+)(:.*)?\\]", data)

                if (re_result is not None
                    and re_result.group(1) in ( "content", "l10n", "settings" )
                   ): _return = { "tag": "rewrite", "tag_end": "[/rewrite]" }
            #

            i += 1
        #

        return _return
    #

    def render(self, content):
        """
Renders content ready for output from the given OSet template.

:param content: Content data

:return: (str) Rendered content
:since:  v0.2.00
        """

        # pylint: disable=no-member

        if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render()- (#echo(__LINE__)#)", self, context = "pas_http_core")

        theme = self.theme
        theme_subtype = self.theme_subtype

        file_path_name = path.join(self.path, theme, "{0}.tsc".format(theme_subtype))

        if (theme_subtype != "site" and (not os.access(file_path_name, os.R_OK))):
            file_path_name = path.join(self.path, theme, "site.tsc")
            theme_subtype = "site"
        #

        theme_data = (None if (self.cache_instance is None) else self.cache_instance.get_file(file_path_name))

        if (theme_data is None):
            file_obj = File()
            if (not file_obj.open(file_path_name, True, "r")): raise IOException("Failed to open theme file for '{0}'".format(self.theme))

            theme_data = file_obj.read()
            file_obj.close()

            if (theme_data is None): raise IOException("Failed to read theme file for '{0}'".format(self.theme))
            if (self.cache_instance is not None): self.cache_instance.set_file(file_path_name, theme_data)
        #

        """
Read corresponding theme configuration
        """

        file_path_name = file_path_name[:-3] + "json"
        Settings.read_file(file_path_name)

        if (self.title is None): self.title = Settings.get("pas_html_title", "Unconfigured site")

        self.content = { "head_canonical_url": self.canonical_url,
                         "head_page_description": self.page_description,
                         "page_title": self.title,
                         "page_content": content
                       }

        theme_settings = Settings.get("pas_http_theme_{0}".format(theme))

        css_files = (self.css_files.copy() if (hasattr(self.css_files, "copy")) else copy(self.css_files))
        js_files = (self.js_files.copy() if (hasattr(self.js_files, "copy")) else copy(self.js_files))

        if (theme_settings is not None and theme_subtype in theme_settings):
            if ("css_files" in theme_settings[theme_subtype]): css_files += theme_settings[theme_subtype]['css_files']
            if ("js_files" in theme_settings[theme_subtype]): js_files += theme_settings[theme_subtype]['js_files']

            if ("l10n_inits" in theme_settings[theme_subtype]):
                for file_basename in theme_settings[theme_subtype]['l10n_inits']: L10n.init(file_basename)
            #
        #

        css_files = InputFilter.filter_unique_list(css_files)
        if (len(css_files) > 0): self.content['css_files'] = css_files

        js_files = InputFilter.filter_unique_list(js_files)
        if (len(js_files) > 0): self.content['js_files'] = js_files

        return self._parse(theme_data)
    #

    def set(self, theme):
        """
Sets the theme to use.

:param theme: Output theme

:since: v0.2.00
        """

        theme = Binary.str(theme)
        if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set({1})- (#echo(__LINE__)#)", self, theme, context = "pas_http_core")

        theme = theme.replace(".", "/")
        file_path_name = path.join(self.path, theme, "site.tsc")

        """
Retry with default theme
        """

        if (os.access(file_path_name, os.R_OK)): self.theme = theme
        else:
            self.theme = Settings.get("pas_http_theme_default", "simple").replace(".", "/")
            file_path_name = path.normpath(self.path, self.theme, "site.tsc")
        #

        """
Read corresponding theme configuration
        """

        file_path_name = file_path_name[:-3] + "json"
        Settings.read_file(file_path_name)
    #

    def set_canonical_url(self, url):
        """
Sets the (X)HTML canonical URL of the response.

:param url: Canonical URL

:since: v0.2.00
        """

        self.canonical_url = url
    #

    def set_canonical_url_parameters(self, parameters):
        """
Sets the (X)HTML canonical URL of the response based on the parameters
given.

:param parameters: Parameters dict

:since: v0.2.00
        """

        _type = (Link.TYPE_RELATIVE_URL
                 if (Settings.get("pas_http_site_canonical_url_type", "absolute") == "relative") else
                 Link.TYPE_ABSOLUTE_URL
                )

        self.set_canonical_url(Link().build_url(_type, parameters))
    #

    def set_log_handler(self, log_handler):
        """
Sets the LogHandler.

:param log_handler: LogHandler to use

:since: v0.2.00
        """

        self.log_handler = log_handler
    #

    def set_page_description(self, description):
        """
Sets the (X)HTML head description of the response.

:param description: Head description

:since: v0.2.00
        """

        self.page_description = Formatting.escape(description)
    #

    def set_subtype(self, subtype):
        """
Sets the theme subtype to use.

:param subtype: Output theme subtype

:since: v0.2.00
        """

        subtype = Binary.str(subtype)
        if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_subtype({1})- (#echo(__LINE__)#)", self, subtype, context = "pas_http_core")

        self.theme_subtype = subtype
    #

    def set_title(self, title):
        """
Sets the title to use.

:param title: Page title

:since: v0.2.00
        """

        title = Binary.str(title)
        if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_title({1})- (#echo(__LINE__)#)", self, title, context = "pas_http_core")

        self.title = title
    #

    @staticmethod
    def get_default_theme():
        """
Returns the default theme name.

:return: (str) Theme name
:since:  v0.2.00
        """

        return Settings.get("pas_http_site_theme_default", "simple")
    #
#
