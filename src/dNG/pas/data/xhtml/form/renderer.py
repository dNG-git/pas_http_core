# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.xhtml.form.Renderer
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

from binascii import hexlify
from os import urandom

from dNG.pas.data.binary import Binary
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.xhtml.formatting import Formatting as XHtmlFormatting
from dNG.pas.module.named_loader import NamedLoader

class Renderer(object):
#
	"""
"Renderer" renders forms for output as (X)HTML.

TODO: Code incomplete

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
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
		elif (sections_count > 0): _return = self._render_section(0)

		return _return
	#

	def render_oset_file(self, template_name, content = None):
	#
		"""
Render the form field using the given OSet template.

:param template_name: OSet template name
:param content: Content object

:since: v0.1.00
		"""

		try:
		#
			parser = NamedLoader.get_instance("dNG.pas.data.oset.FileParser")
			parser.set_oset(self.oset)
			_return = parser.render(template_name, content)
		#
		except Exception: _return = "<div class='pageform_error'>{0}</div>".format(L10n.get("errors_pas_http_core_form_internal_error"))

		return _return
	#

	def render_password(self, field_data, rcp_active = False):
	#
		"""
Format and return XHTML for a password input field.

:param field_data: Dict containing information about the form field

:return: (str) Valid XHTML form field definition
:since:  v0.1.00
		"""

		context = {
			"id": XHtmlFormatting.escape(field_data['id']),
			"name": XHtmlFormatting.escape(field_data['name']),
			"title": XHtmlFormatting.escape(field_data['title']),
			"value": ("" if (field_data['content'] == None) else XHtmlFormatting.escape(field_data['content'])),
			"required": (True if (field_data['required']) else False),
			"error_message": ("" if (field_data['error'] == None) else XHtmlFormatting.escape(field_data['error']))
		}

		if (field_data['size'] == "s"):
		#
			context['size'] = 10
			context['size_percentage'] = "30%"
		#
		elif (field_data['size'] == "m"):
		#
			context['size'] = 18;
			context['size_percentage'] = "55%"
		#
		else:
		#
			context['size'] = 26
			context['size_percentage'] = "80%"
		#

		_return = self.render_oset_file("core/form/password", context)

		"""
		global $direct_cachedata,$direct_globals,$direct_settings;
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -outputFormbuilder->entryAddPassword (+f_data)- (#echo(__LINE__)#)"); }

		$f_js_id = "swg_formbuilder_".$direct_cachedata['formbuilder_element_counter'];
		$direct_cachedata['formbuilder_element_counter']++;

		$f_js_helper = ($f_data['helper_text'] ? "\n".($direct_globals['output']->jsHelper ($f_data['helper_text'],$f_data['helper_url'],$f_js_id)) : "");

		$f_return = "<tr>\n<td class='pageextrabg pageextracontent' style='width:25%;padding:$direct_settings[theme_form_td_padding];text-align:right;vertical-align:middle'><strong>";

		if ($f_data['required'])
		{
			$f_required = " required='required'";
			$f_return .= $direct_settings['swg_required_marker']." ";
		}
		else { $f_required = ""; }

$f_return .= ($f_data['title'].":</strong></td>
<td class='pagebg pagecontent' style='width:75%;padding:$direct_settings[theme_form_td_padding];text-align:center;vertical-align:middle'><input type='password' name='$f_data[name]' id='$f_js_id' value=''$f_required size='$f_width' class='pagecontentinputtextnpassword' style='width:$f_css_width' /><script type='text/javascript'><![CDATA[
jQuery (function () { {$direct_settings['theme_form_js_init']} ({ id:'$f_js_id' }); });
]]></script>$f_js_helper</td>
</tr>");

		return $f_return;
		"""

		return _return
	#

	def render_radio(self, field_data):
	#
		"""
Format and return XHTML to create radio options.

:param field_data: Dict containing information about the form field

:return: (str) Valid XHTML form field definition
:since:  v0.1.00
		"""

		choices = [ ]

		for choice in field_data['choices']:
		#
			if ("title" in choice and "value" in choice):
			#
				choice['title'] = XHtmlFormatting.escape(choice['title'])
				choice['value'] = XHtmlFormatting.escape(choice['value'])

				choices.append(choice)
			#
		#

		context = {
			"id": XHtmlFormatting.escape(field_data['id']),
			"name": XHtmlFormatting.escape(field_data['name']),
			"title": XHtmlFormatting.escape(field_data['title']),
			"choices": choices,
			"required": (True if (field_data['required']) else False),
			"error_message": ("" if (field_data['error'] == None) else XHtmlFormatting.escape(field_data['error']))
		}

		_return = self.render_oset_file("core/form/radio", context)

		"""
		global $direct_globals,$direct_settings;
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -outputFormbuilder->entryAddRadio (+f_data)- (#echo(__LINE__)#)"); }

		$f_js_id = "swg_formbuilder_".$direct_cachedata['formbuilder_element_counter'];
		$direct_cachedata['formbuilder_element_counter']++;

		$f_js_helper = ($f_data['helper_text'] ? "\n".($direct_globals['output']->jsHelper ($f_data['helper_text'],$f_data['helper_url'],$f_js_id)) : "");

		$f_content = "";
		$f_input_required = ($f_data['required'] ? " required='required'" : "");

		foreach ($f_data['content'] as $f_choice_array)
		{
			if ($f_content) { $f_content .= "<br />\n"; }

			if (isset ($f_choice_array['selected'])) { $f_content .= "<input type='radio' name='{$f_data['name']}' id='{$f_choice_array['choice_id']}' value=\"{$f_choice_array['value']}\"$f_input_required checked='checked' /><label for='{$f_choice_array['choice_id']}'> {$f_choice_array['text']}</label>"; }
			else { $f_content .= "<input type='radio' name='{$f_data['name']}' id='{$f_choice_array['choice_id']}' value=\"{$f_choice_array['value']}\"$f_input_required /><label for='{$f_choice_array['choice_id']}'> {$f_choice_array['text']}</label>"; }

$f_content .= ("<script type='text/javascript'><![CDATA[
jQuery (function () { {$direct_settings['theme_form_js_init']} ({ id:'{$f_choice_array['choice_id']}' }); });
]]></script>");
		}

		$f_return = "<tr>\n<td class='pageextrabg pageextracontent' style='width:25%;padding:$direct_settings[theme_form_td_padding];text-align:right;vertical-align:top'><strong>";
		if ($f_data['required']) { $f_return .= $direct_settings['swg_required_marker']." "; }

$f_return .= ($f_data['title'].":</strong></td>
<td class='pagebg pagecontent' style='width:75%;padding:$direct_settings[theme_form_td_padding];text-align:center;vertical-align:middle'><div id='$f_js_id' style='display:inline-block;text-align:left'>$f_content</div>$f_js_helper</td>
</tr>");

		return $f_return;
	}
		"""

		return _return
	#

	def _render_section(self, position):
	#
		"""
Reads the form fields of the section at the given position and calls the
corresponding method to get valid XHTML for output.

:param position: Form section position

:return: (str) Valid XHTML form
:since:  v0.1.00
		"""

		_return = ""

		fields = self.fields[position]['fields']

		for field_data in fields:
		#
			output = None

			if ("type" in field_data):
			#
				output_function = "render_{0}".format(field_data['type'])
				if (hasattr(self, output_function)): output = getattr(self, output_function)(field_data)
			#

			if (_return != ""): _return += "\n"

			if (type(output) == str): _return += output
			else: _return += self.render_oset_file("core/form/error", { "error_message": L10n.get("errors_pas_http_core_form_internal_error") })
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

		context = {
			"type": "submit",
			"id": "{0}_submit".format(self.form_id),
			"title": XHtmlFormatting.escape(L10n.get(title))
		}

		return self.render_oset_file("core/form/button", context)
	#

	def render_text(self, field_data, rcp_active = False):
	#
		"""
Format and return XHTML for a text input field.

:param field_data: Dict containing information about the form field

:return: (str) Valid XHTML form field definition
:since:  v0.1.00
		"""

		context = {
			"type": XHtmlFormatting.escape(field_data['type']),
			"id": XHtmlFormatting.escape(field_data['id']),
			"name": XHtmlFormatting.escape(field_data['name']),
			"title": XHtmlFormatting.escape(field_data['title']),
			"value": ("" if (field_data['content'] == None) else XHtmlFormatting.escape(field_data['content'])),
			"required": (True if (field_data['required']) else False),
			"error_message": ("" if (field_data['error'] == None) else XHtmlFormatting.escape(field_data['error']))
		}

		if (field_data['size'] == "s"):
		#
			context['size'] = 10
			context['size_percentage'] = "30%"
		#
		elif (field_data['size'] == "m"):
		#
			context['size'] = 18;
			context['size_percentage'] = "55%"
		#
		else:
		#
			context['size'] = 26
			context['size_percentage'] = "80%"
		#

		_return = self.render_oset_file("core/form/text", context)

		"""$f_js_helper = ($f_data['helper_text'] ? "\n".($direct_globals['output']->jsHelper ($f_data['helper_text'],$f_data['helper_url'],$f_js_id)) : "");

		if ($f_data['size'] == "s")
		{
			$f_width = 10;
			$f_css_width = "30%";
		}
		elseif ($f_data['size'] == "m")
		{
			$f_width = 18;
			$f_css_width = "55%";
		}
		else
		{
			$f_width = 26;
			$f_css_width = "80%";
		}

		$f_return = "<tr>\n<td class='pageextrabg pageextracontent' style='width:25%;padding:$direct_settings[theme_form_td_padding];text-align:right;vertical-align:middle'><strong>";

		if ($f_data['required'])
		{
			$f_required = " required='required'";
			$f_return .= $direct_settings['swg_required_marker']." ";
		}
		else { $f_required = ""; }

		$f_return .= ($f_data['title'].":</strong></td>\n<td class='pagebg pagecontent' style='width:75%;padding:$direct_settings[theme_form_td_padding];text-align:center;vertical-align:middle'><input type='{$f_data['filter']}' name='$f_data[name]' id='$f_js_id' value=\"$f_data[content]\"$f_required size='$f_width' class='pagecontentinputtextnpassword' style='width:$f_css_width' /><script type='text/javascript'><![CDATA[\n");

$f_return .= ($f_rcp_active ? ("jQuery (function () {
	djs_load_functions({ file:'swg_formbuilder_rcp.php.js' }).done (function () { djs_formbuilder_rcp_init ({ id:'$f_js_id' }); });
});") : "jQuery (function () { {$direct_settings['theme_form_js_init']} ({ id:'$f_js_id',type:'{$f_data['filter']}' }); });");

		$f_return .= "\n]]></script>$f_js_helper</td>\n</tr>";
		"""

		return _return
	#

	def render_textarea(self, field_data, rcp_active = False):
	#
		"""
Format and return XHTML for a textarea input field.

:param field_data: Dict containing information about the form field

:return: (str) Valid XHTML form field definition
:since:  v0.1.00
		"""

		context = {
			"id": XHtmlFormatting.escape(field_data['id']),
			"name": XHtmlFormatting.escape(field_data['name']),
			"title": XHtmlFormatting.escape(field_data['title']),
			"value": ("" if (field_data['content'] == None) else XHtmlFormatting.escape(field_data['content'])),
			"required": (True if (field_data['required']) else False),
			"error_message": ("" if (field_data['error'] == None) else XHtmlFormatting.escape(field_data['error']))
		}

		if (field_data['size'] == "s"): context['rows'] = 5
		elif (field_data['size'] == "m"): context['rows'] = 10
		else: context['rows'] = 20

		_return = self.render_oset_file("core/form/textarea", context)

		"""
		$f_js_helper = ($f_data['helper_text'] ? "\n".($direct_globals['output']->jsHelper ($f_data['helper_text'],$f_data['helper_url'],$f_js_id)) : "");

		if ($f_data['size'] == "s") { $f_rows = 5; }
		elseif ($f_data['size'] == "m") { $f_rows = 10; }
		else { $f_rows = 20; }

		$f_return = "<tr>\n<td class='pageextrabg pageextracontent' style='width:25%;padding:$direct_settings[theme_form_td_padding];text-align:right;vertical-align:top'><strong>";

		if ($f_data['required'])
		{
			$f_required = " required='required'";
			$f_return .= $direct_settings['swg_required_marker']." ";
		}
		else { $f_required = ""; }

		$f_return .= ($f_data['title'].":</strong></td>\n<td class='pagebg pagecontent' style='width:75%;padding:$direct_settings[theme_form_td_padding];text-align:center;vertical-align:middle'><textarea name='$f_data[name]' id='$f_js_id'$f_required cols='26' rows='$f_rows' class='pagecontenttextarea' style='width:80%'>$f_data[content]</textarea><script type='text/javascript'><![CDATA[\n");

$f_return .= ($f_rcp_active ? ("jQuery (function () {
	djs_load_functions({ file:'swg_formbuilder_rcp.php.js' }).done (function () { djs_formbuilder_rcp_init ({ id:'$f_js_id' }); });
});") : "jQuery (function () { {$direct_settings['theme_form_js_init']} ({ id:'$f_js_id',type:'resizeable' }); });");

		$f_return .= "\n]]></script>$f_js_helper</td>\n</tr>";

		return $f_return;
		"""

		return _return
	#

	def set_data(self, fields):
	#
		"""
Sets defined fields for output.

:param oset: OSet requested

:since: v0.1.00
		"""

		if (type(fields) == list): self.fields = fields
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

	"""
/**
	* Add an user space defined object. Everything must be handled by user space.
	*
	* @param  array $f_data Array containing information about the form field
	* @return string Valid XHTML form field definition
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddElement ($f_data)
	{
		global $direct_globals,$direct_settings;
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -outputFormbuilder->entryAddElement (+f_data)- (#echo(__LINE__)#)"); }

		$f_js_id = "swg_formbuilder_".$direct_cachedata['formbuilder_element_counter'];
		$direct_cachedata['formbuilder_element_counter']++;

		$f_js_helper = ($f_data['helper_text'] ? "\n".($direct_globals['output']->jsHelper ($f_data['helper_text'],$f_data['helper_url'],$f_js_id)) : "");

		if (!isset ($f_data['title']))
		{
$f_return = ("<tr>
<td colspan='2' class='pagebg pagecontent' style='padding:$direct_settings[theme_form_td_padding];text-align:center'><div id='$f_js_id' style='display:inline-block;text-align:left'>$f_data[content]</div>$f_js_helper</td>
</tr>");
		}
		elseif (strlen ($f_data['content']))
		{
			$f_return = "<tr>";

			if ($f_data['title'] == "-") { $f_return .= "\n<td class='pageextrabg' style='width:25%;text-align:right;vertical-align:top;font-size:8px'>&#0160;</td>"; }
			else
			{
				$f_return .= "\n<td class='pageextrabg pageextracontent' style='width:25%;padding:$direct_settings[theme_form_td_padding];text-align:right;vertical-align:top'><strong>";
				if ($f_data['required']) { $f_return .= $direct_settings['swg_required_marker']." "; }
				$f_return .= $f_data['title'].":</strong></td>";
			}

$f_return .= ("\n<td class='pagebg pagecontent' style='width:75%;padding:$direct_settings[theme_form_td_padding];text-align:center'><div id='$f_js_id' style='display:inline-block;text-align:left'>$f_data[content]</div>$f_js_helper</td>
</tr>");
		}
		else { $f_return = ""; }

		return $f_return;
	}

/**
	* Format and return XHTML for a email input field.
	*
	* @param  array $f_data Array containing information about the form field
	* @return string Valid XHTML form field definition
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddEMail ($f_data) { return $this->entryAddText ($f_data); }

/**
	* Include an embedded page via iframe for additional and extended options.
	*
	* @param  array $f_data Array containing information about the form field
	* @return string Valid XHTML form field definition
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddEmbed ($f_data)
	{
		global $direct_globals,$direct_settings;
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -outputFormbuilder->entryAddEmbed (+f_data)- (#echo(__LINE__)#)"); }

		$f_js_id = "swg_formbuilder_".$direct_cachedata['formbuilder_element_counter'];
		$direct_cachedata['formbuilder_element_counter']++;

		if (!$f_data['iframe_only']) { $f_embed_url_ajax = direct_linker ("asisuuid","ajax_content;uuid=[uuid];{$f_data['url']}"); }
		$f_embed_url_iframe = direct_linker ("url0","xhtml_embedded;".$f_data['url']);
		$f_embed_url_error = direct_linker ("url0",$f_data['url']);

		if ($f_data['size'] == "s") { $f_height = 230; }
		elseif ($f_data['size'] == "m") { $f_height = 315; }
		else { $f_height = 400; }

		$f_js_helper = ($f_data['helper_text'] ? "\n".($direct_globals['output']->jsHelper ($f_data['helper_text'],$f_data['helper_url'],$f_js_id)) : "");

		if (isset ($f_data['title']))
		{
			$f_return = "<tr>\n<td class='pageextrabg pageextracontent' style='width:25%;padding:$direct_settings[theme_form_td_padding];text-align:right;vertical-align:top'><strong>";
			if ($f_data['required']) { $f_return .= $direct_settings['swg_required_marker']." "; }
			$f_return .= $f_data['title'].":</strong></td>\n<td class='pagebg pagecontent' style='width:75%;padding:$direct_settings[theme_form_td_padding];vertical-align:middle;text-align:center'>";
		}
		else { $f_return = "<tr>\n<td colspan='2' class='pagebg pagecontent' style='padding:$direct_settings[theme_form_td_padding];text-align:center'>"; }

		$f_embedded_code = (($f_data['size'] == "l") ? "<p id='swgAJAX_embed_{$f_data['content']}_point'>".(direct_local_get ("core_loading","text"))."</p>" : "<div id='swgAJAX_embed_box_{$f_data['content']}' class='pageembeddedborder{$direct_settings['theme_css_corners']} pageembeddedbg pageextracontent' style='margin:auto;height:{$f_height}px;overflow:auto'><p id='swgAJAX_embed_{$f_data['content']}_point'>".(direct_local_get ("core_loading","text"))."</p></div>");
		$f_return .= "<div id='$f_js_id'>";

		if ((!$f_data['iframe_only'])&&(isset ($direct_settings['swg_clientsupport']['JSDOMManipulation']))) { $f_return .= $f_embedded_code; }
		else { $f_return .= "<iframe src='$f_embed_url_iframe' id='swgAJAX_embed_{$f_data['content']}_point' class='pageembeddedborder{$direct_settings['theme_css_corners']} pageembeddedbg pageextracontent' style='width:100%;height:{$f_height}px'><strong>".(direct_local_get ("formbuilder_embed_unsupported_1"))."<a href='$f_embed_url_error' target='_blank'>".(direct_local_get ("formbuilder_embed_unsupported_2"))."</a>".(direct_local_get ("formbuilder_embed_unsupported_3"))."</strong></iframe>"; }

		$f_return .= "<input type='hidden' name='{$f_data['name']}' value='{$f_data['content']}' /><script type='text/javascript'><![CDATA[\njQuery (function () { ";

		if ($f_data['iframe_only']) { $f_return .= "{$direct_settings['theme_form_js_init']} ({ id:'swgAJAX_embed_{$f_data['content']}_point',type:'resizeable' });"; }
		else
		{
			$f_return .= "djs_load_functions({ file:'swg_AJAX.php.js',block:'djs_swgAJAX_replace' }).done (function () { ";

			if (isset ($direct_settings['swg_clientsupport']['JSDOMManipulation'])) { $f_return .= "djs_swgAJAX_replace ({ id:'swgAJAX_embed_{$f_data['content']}_point',onReplaced:{ func:'{$direct_settings['theme_form_js_init']}',params: { id:'swgAJAX_embed_box_{$f_data['content']}',type:'resizeable' } },url0:'$f_embed_url_ajax' });"; }
			else { $f_return .= "djs_DOM_replace ({ data:\"".(str_replace (array ('"',"\n"),(array ('\"',"\" +\n\"")),$f_embedded_code))."\",id:'swgAJAX_embed_{$f_data['content']}_point',id_replaced:'swgAJAX_embed_box_{$f_data['content']}',onReplaced:{ func:'djs_swgAJAX_replace',params: { id:'swgAJAX_embed_{$f_data['content']}_point',onReplaced:{ func:'{$direct_settings['theme_form_js_init']}',params: { id:'swgAJAX_embed_box_{$f_data['content']}',type:'resizeable' } },url0:'$f_embed_url_ajax' } } });"; }

			$f_return .= " });";
		}

$f_return .= (" });
]]></script></div>$f_js_helper</td>
</tr>");

		return $f_return;
	}

/**
	* Format and return XHTML to show a FormTags formatted file.
	*
	* @param  array $f_data Array containing information about the form field
	* @return string Valid XHTML form field definition
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddFileFtg ($f_data)
	{
		global $direct_settings;
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -outputFormbuilder->entryAddFileFtg (+f_data)- (#echo(__LINE__)#)"); }

		$f_css_values = "";

		if ($f_data['size'] == "s")
		{
			if (strlen ($f_data['content']) > 575) { $f_css_values = ";height:275px"; }
		}
		elseif ($f_data['size'] == "m")
		{
			if (strlen ($f_data['content']) > 675) { $f_css_values = ";height:320px"; }
		}
		else
		{
			if (strlen ($f_data['content']) > 825) { $f_css_values = ";height:400px"; }
		}

$f_return = ("<tr>
<td class='pageextrabg pageextracontent' style='width:25%;padding:$direct_settings[theme_form_td_padding];text-align:right;vertical-align:top'><strong>$f_data[title]:</strong></td>
<td class='pagebg pagecontent' style='width:75%;padding:$direct_settings[theme_form_td_padding];text-align:left;vertical-align:middle'><div style='margin:auto;padding:1px 5px;overflow:auto$f_css_values'>$f_data[content]</div></td>
</tr>");

		return $f_return;
	}

/**
	* Include a hidden form field and its value.
	*
	* @param  array $f_data Array containing information about the form field
	* @return string Valid XHTML form field definition
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddHidden ($f_data)
	{
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -outputFormbuilder->entryAddHidden (+f_data)- (#echo(__LINE__)#)"); }
		return "<input type='hidden' name='$f_data[name]' value='$f_data[content]' />";
	}

/**
	* Format and return XHTML to show developer-defined information.
	*
	* @param  array $f_data Array containing information about the form field
	* @return string Valid XHTML form field definition
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddInfo ($f_data)
	{
		global $direct_globals,$direct_settings;
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -outputFormbuilder->entryAddInfo (+f_data)- (#echo(__LINE__)#)"); }

		$f_js_id = "swg_formbuilder_".$direct_cachedata['formbuilder_element_counter'];
		$direct_cachedata['formbuilder_element_counter']++;

		$f_js_helper = ($f_data['helper_text'] ? "\n".($direct_globals['output']->jsHelper ($f_data['helper_text'],$f_data['helper_url'],$f_js_id)) : "");

		if (!isset ($f_data['title']))
		{
$f_return .= ("<tr>
<td colspan='2' class='pagebg pagecontent' style='padding:$direct_settings[theme_form_td_padding];text-align:center'><div id='$f_js_id' style='display:inline-block;text-align:left;font-size:10px'>$f_data[content]</div>$f_js_helper</td>
</tr>");
		}
		elseif (strlen ($f_data['content']))
		{
			$f_return .= "<tr>";

			if ($f_data['title'] == "-") { $f_return .= "\n<td class='pageextrabg' style='width:25%;text-align:right;vertical-align:top'><span style='font-size:8px'>&#0160;</span></td>"; }
			else
			{
				$f_return .= "\n<td class='pageextrabg pageextracontent' style='width:25%;padding:$direct_settings[theme_form_td_padding];text-align:right;vertical-align:top'><strong>";
				if ($f_data['required']) { $f_return .= $direct_settings['swg_required_marker']." "; }
				$f_return .= $f_data['title'].":</strong></td>";
			}

			$f_return .= "\n<td class='pagebg pagecontent' style='width:75%;padding:$direct_settings[theme_form_td_padding];text-align:center'><div id='$f_js_id' style='display:inline-block;text-align:left'>$f_data[content]</div>$f_js_helper</td>\n</tr>";
		}
		else { $f_return = ""; }

		return $f_return;
	}

/**
	* Format and return XHTML to create multiple choice select options.
	*
	* @param  array $f_data Array containing information about the form field
	* @return string Valid XHTML form field definition
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddMultiSelect ($f_data)
	{
		global $direct_cachedata,$direct_globals,$direct_settings;
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -outputFormbuilder->entryAddMultiSelect (+f_data)- (#echo(__LINE__)#)"); }

		$f_js_id = "swg_formbuilder_".$direct_cachedata['formbuilder_element_counter'];
		$direct_cachedata['formbuilder_element_counter']++;

		$f_js_helper = ($f_data['helper_text'] ? "\n".($direct_globals['output']->jsHelper ($f_data['helper_text'],$f_data['helper_url'],$f_js_id)) : "");

		if ($f_data['size'] == "s") { $f_rows = 2; }
		elseif ($f_data['size'] == "m") { $f_rows = 5; }
		else { $f_rows = 0; }

		$f_content = "";
		if ($f_choice_array['size'] == "l") { $f_input_required = ($f_data['required'] ? " required='required'" : ""); }

		foreach ($f_data['content'] as $f_choice_array)
		{
			if ($f_content) { $f_content .= (($f_choice_array['size'] == "l") ? "<br />\n" : "\n"); }

			if (isset ($f_choice_array['selected'])) { $f_content .= (($f_choice_array['size'] == "l") ? "<input type='checkbox' id='{$f_choice_array['choice_id']}' name=\"{$f_data['name']}[]\" value=\"{$f_choice_array['value']}\"$f_input_required checked='checked' /><label for='{$f_choice_array['choice_id']}'>{$f_choice_array['text']}</label>" : "<option value=\"{$f_choice_array['value']}\" selected='selected'>{$f_choice_array['text']}</option>"); }
			else { $f_content .= (($f_choice_array['size'] == "l") ? "<input type='checkbox' id='{$f_choice_array['choice_id']}' name=\"{$f_data['name']}[]\" value=\"{$f_choice_array['value']}\"$f_input_required /><label for='{$f_choice_array['choice_id']}'>{$f_choice_array['text']}</label>" : "<option value=\"{$f_choice_array['value']}\">{$f_choice_array['text']}</option>"); }

			if ($f_choice_array['size'] == "l")
			{
$f_content .= ("<script type='text/javascript'><![CDATA[
jQuery (function () { {$direct_settings['theme_form_js_init']} ({ id:'{$f_choice_array['choice_id']}' }); });
]]></script>");
			}
		}

		$f_return = "<tr>\n<td class='pageextrabg pageextracontent' style='width:25%;padding:$direct_settings[theme_form_td_padding];text-align:right;vertical-align:top'><strong>";

		if ($f_data['required'])
		{
			$f_required = " required='required'";
			$f_return .= $direct_settings['swg_required_marker']." ";
		}
		else { $f_required = ""; }

		$f_return .= $f_data['title'].":</strong></td>\n<td class='pagebg pagecontent' style='width:75%;padding:$direct_settings[theme_form_td_padding];text-align:center;vertical-align:middle'>";

		if ($f_rows)
		{
$f_return .= ("<select name='{$f_data['name']}[]' id='$f_js_id'$f_required size='$f_rows' multiple='multiple' class='pagecontentselect'>$f_content</select><script type='text/javascript'><![CDATA[
jQuery (function () { {$direct_settings['theme_form_js_init']} ({ id:'$f_js_id',type:'resizeable' }); });
]]></script>");
		}
		else { $f_return .= "<div style='display:inline-block;text-align:left'>$f_content</div>"; }

		$f_return .= $f_js_helper."</td>\n</tr>";

		return $f_return;
	}

/**
	* Format and return XHTML for a number input field.
	*
	* @param  array $f_data Array containing information about the form field
	* @return string Valid XHTML form field definition
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddNumber ($f_data) { return $this->entryAddText ($f_data); }

/**
	* Format and return XHTML for a password and a confirmation field.
	*
	* @param  array $f_data Array containing information about the form field
	* @return string Valid XHTML form field definition
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddPassword2 ($f_data)
	{
		global $direct_cachedata,$direct_globals,$direct_settings;
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -outputFormbuilder->entryAddPassword2 (+f_data)- (#echo(__LINE__)#)"); }

		$f_js_id = "swg_formbuilder_".$direct_cachedata['formbuilder_element_counter'];
		$direct_cachedata['formbuilder_element_counter']++;

		$f_js_helper = ($f_data['helper_text'] ? "\n".($direct_globals['output']->jsHelper ($f_data['helper_text'],$f_data['helper_url'],$f_js_id)) : "");

		if ($f_data['size'] == "s")
		{
			$f_width = 10;
			$f_css_width = "30%";
		}
		elseif ($f_data['size'] == "m")
		{
			$f_width = 18;
			$f_css_width = "55%";
		}
		else
		{
			$f_width = 26;
			$f_css_width = "80%";
		}

		$f_return = "<tr>\n<td class='pageextrabg pageextracontent' style='width:25%;padding:$direct_settings[theme_form_td_padding];text-align:right;vertical-align:top'><strong>";

		if ($f_data['required'])
		{
			$f_required = " required='required'";
			$f_return .= $direct_settings['swg_required_marker']." ";
		}
		else { $f_required = ""; }

$f_return .= ($f_data['title'].":</strong></td>
<td class='pagebg pagecontent' style='width:75%;padding:$direct_settings[theme_form_td_padding];text-align:center;vertical-align:middle'><p><input type='password' name='$f_data[name]' id='$f_js_id' value=''$f_required size='$f_width' class='pagecontentinputtextnpassword' style='width:$f_css_width' /></p>
<p style='font-size:10px'>".(direct_local_get ("formbuilder_form_password_repetition")).":<br />
<input type='password' name='{$f_data['name']}_repetition' id='{$f_js_id}r' value=''$f_required size='$f_width' class='pagecontentinputtextnpassword' style='width:$f_css_width' /></p><script type='text/javascript'><![CDATA[
jQuery (function ()
{
	{$direct_settings['theme_form_js_init']} ({ id:'$f_js_id' });
	{$direct_settings['theme_form_js_init']} ({ id:'{$f_js_id}r' });
});
]]></script>$f_js_helper</td>
</tr>");

		return $f_return;
	}

/**
	* Format and return XHTML to create a range input.
	*
	* @param  array $f_data Array containing information about the form field
	* @return string Valid XHTML form field definition
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddRange ($f_data)
	{
		global $direct_cachedata,$direct_globals,$direct_settings;
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -outputFormbuilder->entryAddRange (+f_data)- (#echo(__LINE__)#)"); }

		$f_js_id = "swg_formbuilder_".$direct_cachedata['formbuilder_element_counter'];
		$direct_cachedata['formbuilder_element_counter']++;

		$f_js_helper = ($f_data['helper_text'] ? "\n".($direct_globals['output']->jsHelper ($f_data['helper_text'],$f_data['helper_url'],$f_js_id)) : "");

		$f_return = "<tr>\n<td class='pageextrabg pageextracontent' style='width:25%;padding:$direct_settings[theme_form_td_padding];text-align:right;vertical-align:middle'><strong>";

		if ($f_data['required'])
		{
			$f_required = " required='required'";
			$f_return .= $direct_settings['swg_required_marker']." ";
		}
		else { $f_required = ""; }

		$f_return .= $f_data['title'].":</strong></td>\n<td class='pagebg pagecontent' style='width:75%;padding:$direct_settings[theme_form_td_padding];text-align:center;vertical-align:middle'>";

		if ($f_data['size'] == "s") { $f_css_width = "30%"; }
		elseif ($f_data['size'] == "m") { $f_css_width = "55%"; }
		else { $f_css_width = "80%"; }

		$f_unit = (isset ($f_data['unit']) ? "<br />\n<span style='font-size:10px'>($f_data[unit])</span>" : "");

$f_return .= ("<div style='width:$f_css_width;margin:auto;text-align:center'><input name='$f_data[name]' id='$f_js_id'$f_required type='range' min=\"$f_data[min]\" max=\"$f_data[max]\" value=\"$f_data[content]\" class='pagecontentinputtextnpassword' style='width:$f_css_width' />$f_unit<script type='text/javascript'><![CDATA[
jQuery (function () { {$direct_settings['theme_form_js_init']} ({ id:'$f_js_id',type:'range' }); });
]]></script></div>$f_js_helper</td>
</tr>");

		return $f_return;
	}

/**
	* Format and return XHTML for a text input field.
	*
	* @param  array $f_data Array containing information about the form field
	* @return string Valid XHTML form field definition
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddRcpText ($f_data)
	{
		$f_data['filter'] = "text";
		return $this->entryAddText ($f_data,true);
	}

/**
	* Format and return XHTML for a textarea input field.
	*
	* @param  array $f_data Array containing information about the form field
	* @return string Valid XHTML form field definition
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddRcpTextarea ($f_data) { return $this->entryAddTextarea ($f_data,true); }

/**
	* Format and return XHTML to create select options.
	*
	* @param  array $f_data Array containing information about the form field
	* @return string Valid XHTML form field definition
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddSelect ($f_data)
	{
		global $direct_cachedata,$direct_globals,$direct_settings;
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -outputFormbuilder->entryAddSelect (+f_data)- (#echo(__LINE__)#)"); }

		$f_js_id = "swg_formbuilder_".$direct_cachedata['formbuilder_element_counter'];
		$direct_cachedata['formbuilder_element_counter']++;

		$f_js_helper = ($f_data['helper_text'] ? "\n".($direct_globals['output']->jsHelper ($f_data['helper_text'],$f_data['helper_url'],$f_js_id)) : "");

		if ($f_data['size'] == "s") { $f_rows = 1; }
		elseif ($f_data['size'] == "m") { $f_rows = 4; }
		else { $f_rows = 8; }

		$f_content = "";

		foreach ($f_data['content'] as $f_choice_array)
		{
			if ($f_content) { $f_content .= "\n"; }

			if (isset ($f_choice_array['selected'])) { $f_content .= "<option value=\"{$f_choice_array['value']}\" selected='selected'>{$f_choice_array['text']}</option>"; }
			else { $f_content .= "<option value=\"{$f_choice_array['value']}\">{$f_choice_array['text']}</option>"; }
		}

		$f_return = "<tr>\n<td class='pageextrabg pageextracontent' style='width:25%;padding:$direct_settings[theme_form_td_padding];text-align:right;vertical-align:".(($f_data['size'] == "s") ? "middle" : "top")."'><strong>";

		if ($f_data['required'])
		{
			$f_required = " required='required'";
			$f_return .= $direct_settings['swg_required_marker']." ";
		}
		else { $f_required = ""; }

		$f_resizeable = (($f_rows > 1) ? ",type:'resizeable'" : "");

$f_return .= ($f_data['title'].":</strong></td>
<td class='pagebg pagecontent' style='width:75%;padding:$direct_settings[theme_form_td_padding];text-align:center;vertical-align:middle'><select name='$f_data[name]' id='$f_js_id'$f_required size='$f_rows' class='pagecontentselect'>$f_content</select><script type='text/javascript'><![CDATA[
jQuery (function () { {$direct_settings['theme_form_js_init']} ({ id:'$f_js_id'$f_resizeable }); });
]]></script>$f_js_helper</td>
</tr>");

		return $f_return;
	}

/**
	* Format and return XHTML for a spacer.
	*
	* @param  array $f_data Array containing information about the form field
	* @return string Valid XHTML form field definition
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddSpacer ($f_data)
	{
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -outputFormbuilder->entryAddSpacer (+f_data)- (#echo(__LINE__)#)"); }
		return "<tr>\n<td colspan='2' class='pagebg' style='font-size:8px'>&#0160;</td>\n</tr>";
	}

/**
	* Add a title line (subtitle for the form).
	*
	* @param  array $f_data Array containing information about the form field
	* @return string Valid XHTML form field definition
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function entryAddSubTitle ($f_data)
	{
		global $direct_settings;
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -outputFormbuilder->entryAddSubTitle (+f_data)- (#echo(__LINE__)#)"); }

		return "<tr>\n<td colspan='2' class='pagetitlecell' style='padding:$direct_settings[theme_td_padding];text-align:center'>$f_data[title]</td>\n</tr>";
	}

/**
	* Reads an array of form elements and calls the corresponding function to get
	* valid XHTML for output.
	*
	* @param  array $f_data Array containing information about form fields
	* @return string Valid XHTML form
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function formGet ($f_data,$f_form_id = NULL)
	{
		global $direct_globals,$direct_settings;
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -outputFormbuilder->formGet (+f_data,+f_form_id)- (#echo(__LINE__)#)"); }

/* -------------------------------------------------------------------------
Add additional HTML headers
------------------------------------------------------------------------- */

		$direct_globals['output']->headerElements ("<script src='".(direct_linker_dynamic ("url0","s=cache;dsd=dfile+$direct_settings[path_mmedia]/swg_formbuilder.php.js++dbid+".$direct_settings['product_buildid'],true,false))."' type='text/javascript'></script><!-- // FormBuilder javascript functions // -->","script_formbuilder");
		#if ($direct_settings['formbuilder_rcp_supported']) { $direct_globals['output']->headerElements ("<link rel='stylesheet' type='text/css' href='".(direct_linker_dynamic ("url0","s=cache;dsd=dfile+data/mmedia/swg_formbuilder_rcp.css",true,false))."' />"); }

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

		return $f_return;
	}

/**
	* Reads an array of form elements and calls the corresponding function to get
	* valid XHTML for output.
	*
	* @param  array $f_data Array containing information about form fields
	* @return string Valid XHTML form
	* @since  v0.1.00
*/
	/*#ifndef(PHP4) */public /* #*/function formGetResults ($f_data,$f_show_all = false,$f_types_hidden = NULL)
	{
		global $direct_globals,$direct_settings;
		if (USE_debug_reporting) { direct_debug (5,"sWG/#echo(__FILEPATH__)# -outputFormbuilder->formGetResults (+f_data,+f_show_all,+f_types_hidden)- (#echo(__LINE__)#)"); }

		$f_types_hidden = (isset ($f_types_hidden) ? array_merge (array ("hidden","info","subtitle"),$f_types_hidden) : array ("hidden","info","subtitle"));
		$f_return = "";
		$f_return_all = "";

		if (isset ($f_data['']))
		{
			$f_section_array = $f_data[''];
			unset ($f_data['']);
		}
		else { $f_section_array = array_shift ($f_data); }

		while ($f_section_array != NULL)
		{
			foreach ($f_section_array as $f_element_array)
			{
				if ((isset ($f_element_array['filter']))&&($f_element_array['filter'] != "hidden")&&($f_element_array['filter'] != "element")&&($f_element_array['filter'] != "info")&&($f_element_array['filter'] != "spacer")&&($f_element_array['filter'] != "subtitle")&&((direct_class_function_check ($direct_globals['output_formbuilder'],"entry_add_".$f_element_array['filter']))||(is_callable ($f_element_array['filter']))))
				{
					if ($f_return_all) { $f_return_all .= (($f_element_array['filter'] == "spacer") ? "</p>\n<p>" : "<br />\n"); }
					else { $f_return_all = "<p>"; }

					$f_return_all .= "<strong>";
					if ($f_element_array['required']) { $f_return_all .= $direct_settings['swg_required_marker']." "; }
					$f_return_all .= $f_element_array['title'].":</strong> ";

					if ((isset ($f_element_array['error']))&&($f_element_array['error']))
					{
						$f_return_all .= $f_element_array['error'];

						if (!$f_show_all)
						{
							if ($f_return) { $f_return .= (($f_element_array['filter'] == "spacer") ? "</p>\n<p>" : "<br />\n"); }
							else { $f_return = "<p>"; }

							$f_return .= "<strong>{$f_element_array['title']}:</strong> ".$f_element_array['error'];
						}
					}
					else { $f_return_all .= direct_local_get ("formbuilder_field_accepted"); }
				}
			}

			$f_section_array = array_shift ($f_data);
		}

		if (($f_return)&&(!$f_show_all)) { $f_return .= "</p>"; }
		elseif ($f_return_all) { $f_return = $f_return_all."</p>"; }
		else { $f_return .= direct_local_get ("core_unknown"); }

		return $f_return;
	}
	"""

#

##j## EOF