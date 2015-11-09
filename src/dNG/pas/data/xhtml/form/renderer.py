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

from binascii import hexlify
from os import urandom

from dNG.data.xml_parser import XmlParser
from dNG.pas.data.binary import Binary
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.xhtml.formatting import Formatting
from dNG.pas.data.xhtml.form.abstract_field import AbstractField
from dNG.pas.data.xhtml.oset.file_parser import FileParser
from dNG.pas.runtime.type_exception import TypeException
from dNG.pas.runtime.value_exception import ValueException

class Renderer(object):
#
	"""
"Renderer" renders forms for output as XHTML 5.

TODO: Code incomplete

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Renderer)

:since: v0.1.00
		"""

		self.fields = [ ]
		"""
List of form elements
		"""
		self.form_id = None
		"""
ID of the form
		"""
		self.oset = None
		"""
OSet requested
		"""
	#

	def render(self, form_id = None, section = None):
	#
		"""
Parses the list of form fields and calls the corresponding method to get
valid XHTML for output.

:param form_id: Form ID string

:return: (str) Rendered form
:since:  v0.1.00
		"""

		_return = ""

		self._set_form_id(form_id)
		sections_count = len(self.fields)

		if (sections_count > 1):
		#
			xml_parser = XmlParser()

			for section_position in range(0, sections_count):
			#
				fields = self.fields[section_position]['fields']
				is_visible = False

				for field in fields:
				#
					if (isinstance(field, AbstractField)):
					#
						if (field.get_type() != "hidden"):
						#
							is_visible = True
							break
						#
					#
				#

				if (is_visible):
				#
					section_id = "pas_form_section_{0}".format(Binary.str(hexlify(urandom(10))))

					section_attributes = { "class": "pasform_section",
					                       "id": section_id,
					                       "data-form-id": self.form_id
					                     }

					if (self.fields[section_position]['name'] != ""):
					#
						section_attributes['data-form-section-title'] = self.fields[section_position]['name']
					#

					_return += "{0}".format(xml_parser.dict_to_xml_item_encoder({ "tag": "div",
					                                                              "attributes": section_attributes
					                                                            },
					                                                            False
					                                                           )
					                       )
				#

				_return += self.render_section(section_position)

				if (is_visible):
				#
					_return += """
</div><script type="text/javascript"><![CDATA[
require([ "djt/XHtml5FormElement.min" ], function(XHtml5FormElement) {{
	new XHtml5FormElement({{ id: "{0}", type: "form_section" }});
}});
]]></script>
					""".format(section_id).strip()
				#
			#
		#
		elif (sections_count > 0): _return = self.render_section(0)

		return _return
	#

	def _render_oset_file(self, file_path_name, content):
	#
		"""
Render the form field using the given OSet template.

:param template_name: OSet template name
:param content: Content object

:since: v0.1.00
		"""

		# pylint: disable=broad-except

		try:
		#
			parser = FileParser()
			parser.set_oset(self.oset)
			_return = parser.render(file_path_name, content)
		#
		except Exception: _return = "<div class='pageform_error'>{0}</div>".format(L10n.get("pas_http_core_form_error_internal_error"))

		return _return
	#

	def render_section(self, section):
	#
		"""
Reads the form fields of the section at the given position and calls the
corresponding method to get valid XHTML for output.

:param section: Form section position (int) or name (str)

:return: (str) Valid XHTML form
:since:  v0.1.00
		"""

		_return = ""

		position = -1
		section_type = type(section)

		if (section_type is str):
		#
			section_position = 0

			for section in self.fields:
			#
				if (section['name'] == section):
				#
					position = section_position
					break
				#

				section_position += 1
			#
		#
		elif (section_type is int): position = section

		if (position < 0 or len(self.fields) < position): raise ValueException("Given section not found")

		fields = self.fields[position]['fields']

		for field in fields:
		#
			if (not isinstance(field, AbstractField)): raise TypeException("Given field type is invalid")
			field.set_oset(self.oset)

			output = field.render()

			if (_return != ""): _return += "\n"

			if (type(output) is str): _return += output
			else: _return += self._render_oset_file("core/form/error", { "error_message": L10n.get("pas_http_core_form_error_internal_error") })
		#

		return _return
	#

	def render_submit_button(self, title):
	#
		"""
Render the form submit button.

:return: (str) Valid XHTML form
:since:  v0.1.00
		"""

		context = { "type": "submit",
		            "id": "{0}_submit".format(self.form_id),
		            "title": Formatting.escape(L10n.get(title))
		          }

		return self._render_oset_file("core/form/button", context)
	#

	def set_data(self, fields):
	#
		"""
Sets defined fields for output.

:param oset: OSet requested

:since: v0.1.00
		"""

		if (isinstance(fields, list)): self.fields = fields
	#

	def _set_form_id(self, form_id):
	#
		"""
Sets the form ID currently defined with "set_data()".

:param form_id: Unique form ID
		"""

		self.form_id = ("pas_form_{0}".format(Binary.str(hexlify(urandom(10)))) if (form_id is None) else form_id)
	#

	def set_oset(self, oset):
	#
		"""
Sets the OSet to use.

:param oset: OSet requested

:since: v0.1.00
		"""

		self.oset = oset
	#
#

##j## EOF