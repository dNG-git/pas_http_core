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

from dNG.pas.data.xhtml.formatting import Formatting as XHtmlFormatting
from .abstract_field import AbstractField

class TextareaField(AbstractField):
#
	"""
"TextareaField" provides a textarea field.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def check(self, force = False):
	#
		"""
Checks if the field value is valid.

:param force: True to force revalidation

:return: (bool) True if all checks are passed
:since:  v0.1.01
		"""

		if (self.valid == None or force): self.valid = self._check_length()
		return AbstractField.check(self, force)
	#

	def _get_content(self):
	#
		"""
Returns the field content.

:return: (str) Field content
:since:  v0.1.01
		"""

		return XHtmlFormatting.escape(AbstractField._get_content(self))
	#

	def get_type(self):
	#
		"""
Returns the field type.

:return: (str) Field type
:since:  v0.1.01
		"""

		return "textarea"
	#

	def render(self):
	#
		"""
Renders the given field.

:return: (str) Valid XHTML form field definition
:since:  v0.1.01
		"""

		context = { "id": XHtmlFormatting.escape(self.get_id()),
		            "name": XHtmlFormatting.escape(self.name),
		            "title": XHtmlFormatting.escape(self.get_title()),
		            "value": self._get_content(),
		            "required": self.required,
		            "error_message": ("" if (self.error_data == None) else XHtmlFormatting.escape(self.get_error_message()))
		          }

		if (self.size == TextareaField.SIZE_SMALL): context['rows'] = 5
		elif (self.size == TextareaField.SIZE_LARGE): context['rows'] = 20
		else: context['rows'] = 10

		return self._render_oset_file("core/form/textarea", context)
	#
#

##j## EOF