# -*- coding: utf-8 -*-

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

from dNG.data.http.virtual_route import VirtualRoute
from dNG.plugins.hook import Hook

def on_shutdown(params, last_return = None):
    """
Called for "dNG.pas.http.Server.onShutdown" and "dNG.pas.http.Wsgi.onShutdown"

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v1.0.0
    """

    VirtualRoute.unset("/contentfile/")
    VirtualRoute.unset("/favicon.ico$")
    VirtualRoute.unset("/robots.txt$")

    return last_return
#

def on_startup(params, last_return = None):
    """
Called for "dNG.pas.http.Server.onStartup" and "dNG.pas.http.Wsgi.onStartup"

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v1.0.0
    """

    VirtualRoute.set("/contentfile/", { "path_parameter_key": "cid" })

    if (not VirtualRoute.is_defined("/favicon.ico$")): VirtualRoute.set("/favicon.ico", { "s": "cache", "parameters": { "dfile": "favicon.ico" } })
    if (not VirtualRoute.is_defined("/robots.txt$")): VirtualRoute.set("/robots.txt", { "m": "output", "s": "http", "a": "error", "parameters": { "code": "404" } })

    return last_return
#

def register_plugin():
    """
Register plugin hooks.

:since: v1.0.0
    """

    Hook.register("dNG.pas.http.Server.onShutdown", on_shutdown)
    Hook.register("dNG.pas.http.Server.onStartup", on_startup)
    Hook.register("dNG.pas.http.Wsgi.onShutdown", on_shutdown)
    Hook.register("dNG.pas.http.Wsgi.onStartup", on_startup)
#

def unregister_plugin():
    """
Unregister plugin hooks.

:since: v1.0.0
    """

    Hook.unregister("dNG.pas.http.Server.onShutdown", on_shutdown)
    Hook.unregister("dNG.pas.http.Server.onStartup", on_startup)
    Hook.unregister("dNG.pas.http.Wsgi.onShutdown", on_shutdown)
    Hook.unregister("dNG.pas.http.Wsgi.onStartup", on_startup)
#
