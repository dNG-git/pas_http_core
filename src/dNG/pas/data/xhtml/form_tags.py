# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.xhtml.FormTags
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

from .form_tags_encoder import FormTagsEncoder
from .form_tags_renderer import FormTagsRenderer

class FormTags(object):
#
	"""
The OSet parser takes a template string to render the output.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	@staticmethod
	def encode(content):
	#
		"""
Constructor __init__(Parser)

:since: v0.1.01
		"""

		encoder = FormTagsEncoder()
		return encoder.process(content)
	#

	@staticmethod
	def render(content, block_encoding_supported = True, main_id = None):
	#
		"""
Constructor __init__(Parser)

:since: v0.1.01
		"""

		renderer = FormTagsRenderer()
		if (not block_encoding_supported): renderer.set_blocks_supported(block_encoding_supported)
		if (main_id != None): renderer.set_datalinker_main_id(main_id)

		return renderer.render(content)
	#
#

##j## EOF