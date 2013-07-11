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

require['paths']['jqueryui/button'] = "jqueryui/jquery.ui.button.min";
require['paths']['jqueryui/core'] = "jqueryui/jquery.ui.core.min";
require['paths']['jqueryui/widget'] = "jqueryui/jquery.ui.widget.min";

if (!("shim" in require)) { require['shim'] = { }; }
require['shim']['jqueryui/button'] = { deps: [ "jquery", "jqueryui/core", "jqueryui/widget" ] };

//j// EOF