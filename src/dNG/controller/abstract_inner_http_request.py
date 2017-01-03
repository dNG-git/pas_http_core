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

from dNG.runtime.type_exception import TypeException

from .abstract_http_mixin import AbstractHttpMixin
from .abstract_inner_request import AbstractInnerRequest

class AbstractInnerHttpRequest(AbstractInnerRequest, AbstractHttpMixin):
    """
This abstract class contains HTTP methods for inner requests.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self):
        """
Constructor __init__(AbstractInnerHttpRequest)

:since: v0.2.00
        """

        AbstractInnerRequest.__init__(self)
        AbstractHttpMixin.__init__(self)

        self.accepted_formats = None
        """
Formats the client accepts
        """
        self.compression_formats = None
        """
Compression formats the client accepts
        """
    #

    def get_accepted_formats(self):
        """
Returns the formats the client accepts.

:return: (list) Accepted formats
:since:  v0.2.00
        """

        return self.accepted_formats
    #

    def get_compression_formats(self):
        """
Returns the compression formats the client accepts.

:return: (list) Compression formats supported
:since:  v0.2.00
        """

        return self.compression_formats
    #

    def get_session(self):
        """
Returns the associated session.

:return: (object) Session instance
:since:  v0.2.00
        """

        return (None
                if (self.parent_request is None) else
                self.parent_request.get_session()
               )
    #

    def init(self, connection_or_request):
        """
Initializes default values from the a connection or request instance.

:param connection_or_request: (object) Connection or request instance

:since: v0.2.00
        """

        if (not isinstance(connection_or_request, AbstractHttpMixin)): raise TypeException("Request instance given is invalid")
        AbstractInnerRequest.init(self, connection_or_request)

        self.parent_request = connection_or_request._get_parent_request()
        if (self.parent_request is None): self.parent_request = connection_or_request

        if (connection_or_request.is_supported("accepted_formats")): self.accepted_formats = connection_or_request.get_accepted_formats()
        if (connection_or_request.is_supported("compression")): self.compression_formats = connection_or_request.get_compression_formats()
        if (connection_or_request.is_supported("headers")): self.headers = connection_or_request.get_headers()
        self.lang = connection_or_request.get_lang()
        self.lang_default = connection_or_request.get_lang_default()
        if (connection_or_request.is_supported("type")): self.type = connection_or_request.get_type()

        self.set_script_path_name(connection_or_request.get_script_path_name())
    #

    def set_session(self, session):
        """
Sets the associated session.

:param session: (object) Session instance

:since: v0.2.00
        """

        if (self.parent_request is not None): self.parent_request.set_session(session)
    #

    def _supports_accepted_formats(self):
        """
Returns false if accepted formats can not be identified.

:return: (bool) True if accepted formats are identified.
:since:  v0.2.00
        """

        return (self.accepted_formats is not None)
    #

    def _supports_compression(self):
        """
Returns false if supported compression formats can not be identified.

:return: (bool) True if compression formats are identified.
:since:  v0.2.00
        """

        return (self.compression_formats is not None)
    #
#
