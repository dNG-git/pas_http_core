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

from dNG.data.logging.log_line import LogLine
from dNG.data.settings import Settings
from dNG.module.named_loader import NamedLoader

class ServerImplementation(object):
    """
"ServerImplementation" is a factory for the configured, implementing HTTP
aware instance.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    @staticmethod
    def get_class():
        """
Returns an HTTP server class based on the configuration set.

:return: (object) HTTP server class
:since:  v0.2.00
        """

        # pylint: disable=broad-except

        _return = None

        Settings.read_file("{0}/settings/pas_http.json".format(Settings.get("path_data")))
        implementation_class_name = Settings.get("pas_http_server_implementation", "Standalone")

        try: _return = NamedLoader.get_class("dNG.net.http.Server{0}".format(implementation_class_name))
        except Exception as handled_exception:
            LogLine.error(handled_exception, context = "pas_http_site")
            LogLine.warning("pas.http.core use fallback after an exception occurred while instantiating the HTTP implementation", context = "pas_http_site")
        #

        if (_return == None): _return = NamedLoader.get_class("dNG.net.http.ServerStandalone")
        return _return
    #

    @staticmethod
    def get_instance(*args, **kwargs):
        """
Returns an HTTP server instance based on the configuration set.

:return: (object) HTTP server implementation
:since:  v0.2.00
        """

        implementation_class = ServerImplementation.get_class()
        return implementation_class(*args, **kwargs)
    #
#
