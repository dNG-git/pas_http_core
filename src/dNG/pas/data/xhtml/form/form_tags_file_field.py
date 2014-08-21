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

from dNG.pas.data.cache.file_content import FileContent
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.xhtml.form_tags_renderer import FormTagsRenderer
from dNG.pas.data.xhtml.formatting import Formatting
from .abstract_field import AbstractField
from .read_only_field_mixin import ReadOnlyFieldMixin

class FormTagsFileField(AbstractField, ReadOnlyFieldMixin):
#
	"""
"FormTagsFileField" adds a pre-formatted text from an external file.

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
Constructor __init__(AbstractField)

:param name: Form field name

:since: v0.1.01
		"""

		AbstractField.__init__(self, name)
		ReadOnlyFieldMixin.__init__(self)

		self.formtags_content = None
		"""
Cached field FormTags content
		"""
		self.formtags_filepath = None
		"""
Field FormTags file path
		"""

		self.size = FormTagsFileField.SIZE_SMALL
	#

	def _get_content(self):
	#
		"""
Returns the field content.

:return: (str) Field content
:since:  v0.1.01
		"""

		if (self.formtags_content == None
		    and self.formtags_filepath != None
		   ): self.formtags_content = FileContent.read(self.formtags_filepath)

		return ("" if (self.formtags_content == None) else self.formtags_content)
	#

	def get_type(self):
	#
		"""
Returns the field type.

:return: (str) Field type
:since:  v0.1.01
		"""

		return "formtags_file"
	#

	def render(self):
	#
		"""
Renders the given field.

:return: (str) Valid XHTML form field definition
:since:  v0.1.01
		"""

		renderer = FormTagsRenderer()
		renderer.set_xhtml_allowed(True)

		content = self._get_content()

		context = { "id": "pas_{0}".format(Formatting.escape(self.get_id())),
		            "name": Formatting.escape(self.name),
		            "title": Formatting.escape(self.get_title()),
		            "content": (L10n.get("pas_http_core_form_error_internal_error")
		                        if (content == None) else
		                        renderer.render(content)
		                       ),
		            "error_message": ("" if (self.error_data == None) else Formatting.escape(self.get_error_message()))
		          }

		if (self.size == FormTagsFileField.SIZE_MEDIUM): context['size_percentage'] = "55%"
		elif (self.size == FormTagsFileField.SIZE_LARGE): context['size_percentage'] = "80%"
		else: context['size_percentage'] = "30%"

		return self._render_oset_file("core/form/formtags_content", context)
	#

	def set_formtags_filepath(self, filepath):
	#
		"""
Sets the FormTags file path.

:param filepath: FormTags file path

:since: v0.1.01
		"""

		self.formtags_filepath = filepath
	#
#

##j## EOF