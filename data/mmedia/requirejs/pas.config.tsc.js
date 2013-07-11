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
	formX_focused_class: "pageforminputfocused"
};

var require = {
	baseUrl: "[rewrite:settings]http_path_mmedia_versioned[/rewrite]",
	paths: {
		"djs/formX": "djs/formX.min",
		"djs/uiX": "djs/uiX.min",

		"jquery": "jquery/jquery-2.0.0.min",
	},
};

//j// EOF