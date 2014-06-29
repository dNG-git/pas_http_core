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

from dNG.pas.data.text.form_tags_encoder import FormTagsEncoder as _FormTagsEncoder

class FormTagsEncoder(_FormTagsEncoder):
#
	"""
Encodes data as well as some typical (X)HTML statements and validates
FormTags.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	CSS_COLOR_NAMES = { "aliceblue":            "f0f8ff",
	                    "antiquewhite":         "faebd7",
	                    "aqua":                 "00ffff",
	                    "aquamarine":           "7fffd4",
	                    "azure":                "f0ffff",
	                    "beige":                "f5f5dc",
	                    "bisque":               "ffe4c4",
	                    "black":                "000000",
	                    "blanchedalmond":       "ffebcd",
	                    "blue":                 "0000ff",
	                    "blueviolet":           "8a2be2",
	                    "brown":                "a52a2a",
	                    "burlywood":            "deb887",
	                    "cadetblue":            "5f9ea0",
	                    "chartreuse":           "7fff00",
	                    "chocolate":            "d2691e",
	                    "coral":                "ff7f50",
	                    "cornflowerblue":       "6495ed",
	                    "cornsilk":             "fff8dc",
	                    "crimson":              "dc143c",
	                    "cyan":                 "00ffff",
	                    "darkblue":             "00008b",
	                    "darkcyan":             "008b8b",
	                    "darkgoldenrod":        "b8860b",
	                    "darkgray":             "a9a9a9",
	                    "darkgreen":            "006400",
	                    "darkkhaki":            "bdb76b",
	                    "darkmagenta":          "8b008b",
	                    "darkolivegreen":       "556b2f",
	                    "darkorange":           "ff8c00",
	                    "darkorchid":           "9932cc",
	                    "darkred":              "8b0000",
	                    "darksalmon":           "e9967a",
	                    "darkseagreen":         "8fbc8f",
	                    "darkslateblue":        "483d8b",
	                    "darkslategray":        "2f4f4f",
	                    "darkturquoise":        "00ced1",
	                    "darkviolet":           "9400d3",
	                    "deeppink":             "ff1493",
	                    "deepskyblue":          "00bfff",
	                    "dimgray":              "696969",
	                    "dodgerblue":           "1e90ff",
	                    "firebrick":            "b22222",
	                    "floralwhite":          "fffaf0",
	                    "forestgreen":          "228b22",
	                    "fuchsia":              "ff00ff",
	                    "gainsboro":            "dcdcdc",
	                    "ghostwhite":           "f8f8ff",
	                    "gold":                 "ffd700",
	                    "goldenrod":            "daa520",
	                    "gray":                 "808080",
	                    "green":                "008000",
	                    "greenyellow":          "adff2f",
	                    "honeydew":             "f0fff0",
	                    "hotpink":              "ff69b4",
	                    "indianred ":           "cd5c5c",
	                    "indigo ":              "4b0082",
	                    "ivory":                "fffff0",
	                    "khaki":                "f0e68c",
	                    "lavender":             "e6e6fa",
	                    "lavenderblush":        "fff0f5",
	                    "lawngreen":            "7cfc00",
	                    "lemonchiffon":         "fffacd",
	                    "lightblue":            "add8e6",
	                    "lightcoral":           "f08080",
	                    "lightcyan":            "e0ffff",
	                    "lightgoldenrodyellow": "fafad2",
	                    "lightgray":            "d3d3d3",
	                    "lightgreen":           "90ee90",
	                    "lightpink":            "ffb6c1",
	                    "lightsalmon":          "ffa07a",
	                    "lightseagreen":        "20b2aa",
	                    "lightskyblue":         "87cefa",
	                    "lightslategray":       "778899",
	                    "lightsteelblue":       "b0c4de",
	                    "lightyellow":          "ffffe0",
	                    "lime":                 "00ff00",
	                    "limegreen":            "32cd32",
	                    "linen":                "faf0e6",
	                    "magenta":              "ff00ff",
	                    "maroon":               "800000",
	                    "mediumaquamarine":     "66cdaa",
	                    "mediumblue":           "0000cd",
	                    "mediumorchid":         "ba55d3",
	                    "mediumpurple":         "9370db",
	                    "mediumseagreen":       "3cb371",
	                    "mediumslateblue":      "7b68ee",
	                    "mediumspringgreen":    "00fa9a",
	                    "mediumturquoise":      "48d1cc",
	                    "mediumvioletred":      "c71585",
	                    "midnightblue":         "191970",
	                    "mintcream":            "f5fffa",
	                    "mistyrose":            "ffe4e1",
	                    "moccasin":             "ffe4b5",
	                    "navajowhite":          "ffdead",
	                    "navy":                 "000080",
	                    "oldlace":              "fdf5e6",
	                    "olive":                "808000",
	                    "olivedrab":            "6b8e23",
	                    "orange":               "ffa500",
	                    "orangered":            "ff4500",
	                    "orchid":               "da70d6",
	                    "palegoldenrod":        "eee8aa",
	                    "palegreen":            "98fb98",
	                    "paleturquoise":        "afeeee",
	                    "palevioletred":        "db7093",
	                    "papayawhip":           "ffefd5",
	                    "peachpuff":            "ffdab9",
	                    "peru":                 "cd853f",
	                    "pink":                 "ffc0cb",
	                    "plum":                 "dda0dd",
	                    "powderblue":           "b0e0e6",
	                    "purple":               "800080",
	                    "red":                  "ff0000",
	                    "rosybrown":            "bc8f8f",
	                    "royalblue":            "4169e1",
	                    "saddlebrown":          "8b4513",
	                    "salmon":               "fa8072",
	                    "sandybrown":           "f4a460",
	                    "seagreen":             "2e8b57",
	                    "seashell":             "fff5ee",
	                    "sienna":               "a0522d",
	                    "silver":               "c0c0c0",
	                    "skyblue":              "87ceeb",
	                    "slateblue":            "6a5acd",
	                    "slategray":            "708090",
	                    "snow":                 "fffafa",
	                    "springgreen":          "00ff7f",
	                    "steelblue":            "4682b4",
	                    "tan":                  "d2b48c",
	                    "teal":                 "008080",
	                    "thistle":              "d8bfd8",
	                    "tomato":               "ff6347",
	                    "turquoise":            "40e0d0",
	                    "violet":               "ee82ee",
	                    "wheat":                "f5deb3",
	                    "white":                "ffffff",
	                    "whitesmoke":           "f5f5f5",
	                    "yellow":               "ffff00",
	                    "yellowgreen":          "9acd32"
	                  }

	def _change_match_color(self, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the "color" tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.01
		"""

		_return = ""
		re_object = re.match("^\\[color=(.+?)\\]", data[tag_position:data_position])

		if (re_object != None):
		#
			color = re_object.group(1)
			enclosed_data = data[data_position:tag_end_position]

			if (color[:1] == "#"):
			#
				re_color_object = re.match("^\\[color=#([0-9a-f])([0-9a-f])([0-9a-f])\\]", data[tag_position:data_position])
				_return = (enclosed_data if (re_color_object == None) else "[color=#{0}{1}{2}]{3}[/color]".format(re_color_object.group(1) * 2, re_color_object.group(2) * 2, re_color_object.group(3) * 2, enclosed_data))
			#
			else: _return = ("[color=#{0}]{1}[/color]".format(FormTagsEncoder.CSS_COLOR_NAMES[color.lower()], enclosed_data) if (color.lower() in FormTagsEncoder.CSS_COLOR_NAMES) else enclosed_data)
		#

		return _return
	#

	def _check_match_color(self, data):
	#
		"""
Check if a possible tag match is a valid "color" tag that needs to be changed.

:param data: Data starting with the possible tag

:return: (bool) True if change required
:since:  v0.1.01
		"""

		_return = False
		re_object = re.match("^\\[color=(.+?)\\]", data)

		if (re_object != None):
		#
			color = re_object.group(1)

			if (color[:1] == "#"):
			#
				re_color_object = re.match("^\\[color=#([0-9a-f]{6})\\]", data)
				if (re_color_object == None): _return = True
			#
			else: _return = True
		#

		return _return
	#
#

##j## EOF