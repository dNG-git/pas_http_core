//j// BOF

/* -------------------------------------------------------------------------
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
------------------------------------------------------------------------- */

var djs_config = {
	formX_focused_class: 'pageform_input_focused',
	ResponsiveTable_class: 'pagetable_responsive',
	uiX_option_button_class: 'pageoptionsbar_button',
	uiX_option_widget_class: 'pageoptionsbar_widget'
};

var require = {
	baseUrl: '[rewrite:settings]http_path_mmedia_versioned[/rewrite]',
	paths: {
		'Hammer': 'input/hammer.min',
		'jquery': 'jquery/jquery-2.1.1.min',
		'jquery.placeholder': 'jquery/jquery.placeholder.min',
		'Modernizr': 'xhtml5/modernizr.min'
	},
	shim: {
		'Hammer': { exports: 'Hammer' },
		'Modernizr': { exports: 'Modernizr' }
	}
};

//j// EOF