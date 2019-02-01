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

from socket import error as socket_error
from socket import getaddrinfo, gethostname, getfqdn

from dNG.data.http.virtual_route import VirtualRoute
from dNG.data.settings import Settings
from dNG.data.text.link import Link
from dNG.plugins.hook import Hook
from dNG.runtime.named_loader import NamedLoader
from dNG.runtime.not_implemented_exception import NotImplementedException
from dNG.runtime.thread import Thread

class AbstractServer(Thread):
    """
"AbstractServer" is responsible to configure an HTTP aware instance.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=arguments-differ,unused-argument

    def __init__(self):
        """
Constructor __init__(AbstractServer)

:since: v1.0.0
        """

        Thread.__init__(self)

        self.host = None
        """
Configured server host
        """
        self._log_handler = NamedLoader.get_singleton("dNG.data.logging.LogHandler", False)
        """
The LogHandler is called whenever debug messages should be logged or errors
happened.
        """
        self.port = None
        """
Configured server port
        """
        self.socket_hostname = None
        """
Socket server hostname
        """

        socket_hostname = getfqdn()

        try:
            getaddrinfo(socket_hostname, None)
            self.socket_hostname = socket_hostname
        except socket_error: self.socket_hostname = gethostname()

        self.socket_hostname = self.socket_hostname.lower()

        Hook.register_weakref("dNG.pas.http.Server.getHost", self.get_host)
        Hook.register_weakref("dNG.pas.http.Server.getPort", self.get_port)
    #

    def _configure(self):
        """
Configures the server

:since: v1.0.0
        """

        site_version = Settings.get("pas_http_site_version", "")

        if (site_version == ""):
            site_version = "#echo(pasHttpCoreIVersion)#"
            Settings.set("pas_http_site_version", site_version)
        #

        if (Link.is_preferred_defined()): Settings.set("x_pas_http_base_url", Link.get_preferred().build_url(Link.TYPE_ABSOLUTE_URL | Link.TYPE_BASE_PATH))
        else: Settings.set("x_pas_http_base_url", None)

        Settings.set("x_pas_http_session_uuid", "")
        Settings.set("x_pas_http_path_assets_versioned", "/data/assets/{0}".format(site_version))

        VirtualRoute.set("/data/assets/{0}/".format(site_version), { "s": "cache", "path_parameter_key": "dfile" })
        VirtualRoute.set("/data/assets/", { "s": "cache", "path_parameter_key": "dfile" })

        Hook.call("dNG.pas.http.Server.onConfigured", server = self)
    #

    def get_host(self, params = None, last_return = None):
        """
Returns the configured server host.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v1.0.0
        """

        return (self.host if (last_return is None) else last_return)
    #

    def get_port(self, params = None, last_return = None):
        """
Returns the configured server port.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v1.0.0
        """

        return (self.port if (last_return is None) else last_return)
    #

    def start(self, params = None, last_return = None):
        """
Start the server

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v1.0.0
        """

        self._configure()
        Thread.start(self)

        Hook.call("dNG.pas.http.Server.onStartup", server = self)
        return self
    #

    def run(self):
        """
Runs the server

:since: v1.0.0
        """

        raise NotImplementedException()
    #

    def stop(self, params = None, last_return = None):
        """
Stop the server

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v1.0.0
        """

        Hook.call("dNG.pas.http.Server.onShutdown", server = self)
        return last_return
    #
#
