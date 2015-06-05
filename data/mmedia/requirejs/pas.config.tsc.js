//j// BOF

/* -------------------------------------------------------------------------
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
------------------------------------------------------------------------- */

var djs_config = {
	FixableBlock_fixed_class: 'pagecontent_box_fixed',
	ResponsiveTable_class: 'pagetable_responsive',
	XHtml5FormElement_focused_class: 'pageform_input_focused',
};

var require = {
	baseUrl: '[rewrite:settings]http_path_mmedia_versioned[/rewrite]',
	paths: {
		'Hammer': 'input/hammer.min',
		'jquery': 'jquery/jquery-2.1.4.min',
		'jquery.placeholder': 'jquery/jquery.placeholder.min',
		'Modernizr': 'xhtml5/modernizr.min'
	},
	shim: {
		'Hammer': { exports: 'Hammer' },
		'Modernizr': { exports: 'Modernizr' }
	}
};

//j// EOF