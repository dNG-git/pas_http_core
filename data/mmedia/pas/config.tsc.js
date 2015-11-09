//j// BOF

/*
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
*/

var djt_config = {
	FixableBlock_fixed_class: 'pagecontent_box_fixed',
	ResponsiveTable_class: 'pagetable_responsive',
	XHtml5FormElement_focused_class: 'pageform_input_focused'
};

var pas_config = {
	lang: '[rewrite:l10n]lang_code[/rewrite]',
	mmedia_base_path: '[rewrite:settings]x_pas_http_path_mmedia_versioned[/rewrite]',
	theme: '[rewrite:settings]x_pas_http_theme[/rewrite]',
	HttpJsonApiRequest_base_url: '[rewrite:settings]x_pas_http_base_url[/rewrite]',
	HttpJsonApiRequest_session_uuid: '[rewrite:settings]x_pas_http_session_uuid[/rewrite]'
};

var require = {
	baseUrl: pas_config.mmedia_base_path,
	paths: {
		'Hammer': 'input/hammer.min',
		'jquery': 'jquery/jquery.min',
		'jquery.placeholder': 'jquery/jquery.placeholder.min',
		'Modernizr': 'xhtml5/modernizr.min'
	},
	shim: {
		'Hammer': { exports: 'Hammer' },
		'Modernizr': { exports: 'Modernizr' }
	}
};

//j// EOF