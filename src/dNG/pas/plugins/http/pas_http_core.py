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

# pylint: disable=unused-argument

from dNG.pas.data.http.virtual_config import VirtualConfig
from dNG.pas.plugins.hook import Hook

def register_plugin():
#
	"""
Register plugin hooks.

:since: v0.1.00
	"""

	Hook.register("dNG.pas.http.Server.onStartup", on_startup)
	Hook.register("dNG.pas.http.Wsgi.onStartup", on_startup)
#

def on_startup(params, last_return = None):
#
	"""
Called for "dNG.pas.http.Server.onStartup" and "dNG.pas.http.Wsgi.onStartup"

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
	"""

	VirtualConfig.set_virtual_path("/contentfile/", { "path": "cid" })
	if (not VirtualConfig.isset_virtual_path("/favicon.ico")): VirtualConfig.set_virtual_path("/favicon.ico", { "s": "cache", "dsd": { "dfile": "favicon.ico" } })
	VirtualConfig.set_virtual_path("/robots.txt", { "m": "output", "s": "http", "a": "error", "dsd": { "code": "404" } })

	return last_return
#

def unregister_plugin():
#
	"""
Unregister plugin hooks.

:since: v0.1.00
	"""

	Hook.unregister("dNG.pas.http.Server.onStartup", on_startup)
	Hook.unregister("dNG.pas.http.Wsgi.onStartup", on_startup)
#

##j## EOF