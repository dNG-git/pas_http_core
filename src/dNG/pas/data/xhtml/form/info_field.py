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

from dNG.data.xml_parser import XmlParser
from dNG.pas.data.xhtml.formatting import Formatting
from .abstract_field import AbstractField
from .read_only_field_mixin import ReadOnlyFieldMixin

class InfoField(AbstractField, ReadOnlyFieldMixin):
#
	"""
"InfoField" provides a read-only visible text.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, name = None):
	#
		"""
Constructor __init__(InfoField)

:param name: Form field name

:since: v0.1.01
		"""

		AbstractField.__init__(self, name)
		ReadOnlyFieldMixin.__init__(self)

		self.link = None
		"""
Link used for the field content
		"""
	#

	def _get_content(self):
	#
		"""
Returns the field content.

:return: (str) Field content
:since:  v0.1.01
		"""

		content = AbstractField._get_content(self)

		_return = (Formatting.escape(content)
		           if (self.link == None) else
		           XmlParser().dict_to_xml_item_encoder({ "tag": "a",
		                                                  "attributes": { "href": self.link },
		                                                  "value": content
		                                                },
		                                                strict_standard_mode = False
		                                               )
		          )

		return _return
	#

	def get_type(self):
	#
		"""
Returns the field type.

:return: (str) Field type
:since:  v0.1.01
		"""

		return "info"
	#

	def render(self):
	#
		"""
Renders the given field.

:return: (str) Valid XHTML form field definition
:since:  v0.1.01
		"""

		context = { "title": Formatting.escape(self.get_title()),
		            "value": self._get_content(),
		            "required": self.required,
		            "error_message": ("" if (self.error_data == None) else Formatting.escape(self.get_error_message()))
		          }

		return self._render_oset_file("core/form/info", context)
	#

	def set_link(self, link):
	#
		"""
Sets the link used for the field content.

:param link: Link URL

:since: v0.1.01
		"""

		self.link = link
	#
#

##j## EOF