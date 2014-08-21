# -*- coding: utf-8 -*-
##j## BOF

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

from dNG.pas.data.binary import Binary
from dNG.pas.data.text.tag_parser.source_value_mixin import SourceValueMixin
from dNG.pas.data.xhtml.form_tags import FormTags

class RewriteFormTagsXhtmlMixin(SourceValueMixin):
#
	"""
This tag parser mixin provides support for rewrite statements to generate
safe XHTML compliant output.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def render_rewrite_form_tags_xhtml(self, source, key):
	#
		"""
Renders the FormTags content for XHTML output.

:param source: Source for rewrite
:param key: Key in source for rewrite

:return: (str) Rendered XHTML content
:since:  v0.1.01
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render_rewrite_formtags_xhtml({1})- (#echo(__LINE__)#)", self, key, context = "pas_tag_parser")

		content = None
		data = self.get_source_value(source, key)
		main_id = None

		if (not isinstance(data, dict)): content = Binary.str(data)
		elif ("content" in data):
		#
			content = Binary.str(data['content'])
			if ("main_id" in data): main_id = data['main_id']
		#

		_return = (FormTags.render(content, main_id = main_id)
		           if (type(content) == str) else
		           ""
		          )

		return _return
	#
#

##j## EOF