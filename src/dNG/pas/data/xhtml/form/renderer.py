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
			section_position = 0

			"""
		if (isset ($f_data['']))
		{
			if (count ($f_data) > 1)
			{
				if (!isset ($f_form_id)) { $f_form_id = uniqid ('swg_form_'); }
				$f_return = "<div id='{$f_form_id}_sections'>".($this->formGetSection ($f_data[''],(direct_local_get ("formbuilder_section_general"))));
			}
			else { $f_return = $this->formGetSection ($f_data['']); }

			unset ($f_data['']);
		}
		else { $f_return = ""; }

		if (!empty ($f_data))
		{
			if (!isset ($f_form_id)) { $f_form_id = uniqid ('swg_form_'); }

			if (!$f_return) { $f_return .= "<div id='{$f_form_id}_sections'>"; }
			foreach ($f_data as $f_section => $f_elements_array) { $f_return .= $this->formGetSection ($f_elements_array,$f_section); }
			$f_return .= "</div><script type='text/javascript'><![CDATA[\njQuery (function () { {$direct_settings['theme_form_js_init']} ({ id:'{$f_form_id}_sections',type:'form_sections' }); });\n]]></script>";
		}
$f_return = ((isset ($f_section) ? "<p class='pagecontenttitle ui-accordion-header'><a href='#swg_form_".(md5 ($f_section))."'>".(direct_html_encode_special ($f_section))."</a></p><div>" : "")."
<table class='pagetable' style='width:100%;table-layout:auto'>
<tbody>");
			"""
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

		if (type(section) == str):
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
		elif (type(section) == int): position = section

		if (position < 0 or len(self.fields) < position): raise ValueException("Given section not found")

		fields = self.fields[position]['fields']

		for field in fields:
		#
			if (not isinstance(field, AbstractField)): raise TypeException("Given field type is invalid")
			field.set_oset(self.oset)

			output = field.render()

			if (_return != ""): _return += "\n"

			if (type(output) == str): _return += output
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

		self.form_id = ("pas_form_{0}".format(Binary.str(hexlify(urandom(10)))) if (form_id == None) else form_id)
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