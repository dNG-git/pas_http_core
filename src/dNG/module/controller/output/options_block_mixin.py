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

from dNG.data.settings import Settings
from dNG.data.text.md5 import Md5
from dNG.data.text.l10n import L10n
from dNG.data.xhtml.form_tags import FormTags
from dNG.data.xhtml.formatting import Formatting as XHtmlFormatting
from dNG.data.xhtml.link import Link
from dNG.data.xml_parser import XmlParser

class OptionsBlockMixin(object):
    """
An "OptionBlock" contains of several options formatted with title,
description and optional image.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def _add_options_block_css_sprite(self, css_sprite_data):
        """
Adds the requested CSS sprites to the output.

:param css_sprite_data: CSS sprite as string or list

:since: v0.2.00
        """

        if (self.response.is_supported("html_css_files") and self.response.is_supported("html_theme")):
            css_sprites = [ ]

            if (isinstance(css_sprite_data, list)): css_sprites = css_sprite_data
            elif (type(css_sprite_data) is str): css_sprites.append(css_sprite_data)

            if (len(css_sprites) > 0):
                for css_sprite in css_sprites: self.response.add_theme_css_file(css_sprite)
            #
        #
    #

    def _render_options_block_icon(self, icon, title):
        """
Renders an "OptionsBlock" CSS sprite icon.

:param icon: Icon name

:return: (str) "img" XHTML tag
:since:  v0.2.00
        """

        img_attributes = { "tag": "img",
                           "attributes": { "src": "{0}/spacer.png".format(Settings.get("x_pas_http_path_mmedia_versioned")),
                                           "class": "{0}-icon".format(icon)
                                         },
                           "alt": title
                         }

        return "{0}".format(XmlParser().dict_to_xml_item_encoder(img_attributes, strict_standard_mode = False))
    #

    def _render_options_block_image(self, image, title):
        """
Renders an "OptionsBlock" image.

:param image: Relative image file path

:return: (str) "img" XHTML tag
:since:  v0.2.00
        """

        img_attributes = { "tag": "img",
                           "attributes": { "src": "{0}/themes/{1}/{2}.png".format(Settings.get("x_pas_http_path_mmedia_versioned"),
                                                                                  self.response.get_theme_active(),
                                                                                  image
                                                                                 )
                                         },
                           "alt": title
                         }

        return "{0}".format(XmlParser().dict_to_xml_item_encoder(img_attributes, strict_standard_mode = False))
    #

    def render_options_block_link(self, data, include_image = True):
        """
Renders a link.

:return: (str) Link XHTML
:since:  v0.2.00
        """

        _return = ""

        if ("title" in data and "type" in data and "parameters" in data):
            _type = (data['type'] if (type(data['type']) is int) else Link.get_type_int(data['type']))

            url = Link().build_url(_type, data['parameters'])
            xml_parser = XmlParser()

            is_js_required = (_type & Link.TYPE_JS_REQUIRED == Link.TYPE_JS_REQUIRED)
            link_id = data.get("id")

            if (is_js_required):
                if (link_id is None): link_id = "pas_http_core_{0}_{1:d}_{2:d}".format(Md5.hash(url), id(data), id(self))

                _return = xml_parser.dict_to_xml_item_encoder({ "tag": "span",
                                                                "attributes": { "data-href": url,
                                                                                "id": link_id,
                                                                                "title": L10n.get("pas_http_core_js_required"),
                                                                                "class": "pageurl_requirements_unsupported"
                                                                              }
                                                              },
                                                              False
                                                             )
            else:
                link_attributes = { "href": url }
                if (link_id is not None): link_attributes['id'] = link_id

                _return = xml_parser.dict_to_xml_item_encoder({ "tag": "a", "attributes": link_attributes }, False)
            #

            if ("title_l10n" in data and L10n.is_defined(data['title_l10n'])): title = L10n.get(data['title_l10n'])
            else:
                l10n_title_id = "title_{0}".format(self.request.get_lang())
                title = (data[l10n_title_id] if (l10n_title_id in data) else data['title'])
            #

            if (include_image):
                if ("icon" in data): _return += self._render_options_block_icon(data['icon'], title)
                elif ("image" in data): _return += self._render_options_block_image(data['image'], title)
            #

            _return += "{0}".format(XHtmlFormatting.escape(title))

            description = None

            if ("description_l10n" in data and L10n.is_defined(data['description_l10n'])): description = L10n.get(data['description_l10n'])
            else:
                l10n_description_id = "description_{0}".format(self.request.get_lang())

                if (l10n_description_id in data): description = data[l10n_description_id]
                elif ("description" in data): description = data['description']
            #

            if (description is not None): _return += "<br />\n{0}".format(FormTags.render(description))

            if (is_js_required):
                _return += """
</span><script type="text/javascript"><![CDATA[
require([ "djt/JsLink.min" ], function(JsLink) {{
    new JsLink({{ id: "{0}" }});
}});
]]></script>
                """.format(link_id).strip()
            else: _return += "</a>"

            if (include_image and "css_sprite" in data and "icon" in data): self._add_options_block_css_sprite(data['css_sprite'])
        #

        return _return
    #
#
