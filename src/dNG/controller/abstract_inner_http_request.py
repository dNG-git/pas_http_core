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
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self):
        """
Constructor __init__(AbstractInnerHttpRequest)

:since: v1.0.0
        """

        AbstractInnerRequest.__init__(self)
        AbstractHttpMixin.__init__(self)

        self._accepted_formats = None
        """
Formats the client accepts
        """
        self._compression_formats = None
        """
Compression formats the client accepts
        """
    #

    @property
    def accepted_formats(self):
        """
Returns the formats the client accepts.

:return: (list) Accepted formats
:since:  v1.0.0
        """

        return self._accepted_formats
    #

    @property
    def compression_formats(self):
        """
Returns the compression formats the client accepts.

:return: (list) Compression formats supported
:since:  v1.0.0
        """

        return self._compression_formats
    #

    @property
    def session(self):
        """
Returns the associated session.

:return: (object) Session instance
:since:  v1.0.0
        """

        return (None
                if (self._parent_request is None) else
                self._parent_request.session
               )
    #

    @session.setter
    def session(self, session):
        """
Sets the associated session.

:param session: (object) Session instance

:since: v1.0.0
        """

        if (self._parent_request is not None): self._parent_request.set_session(session)
    #

    def init(self, connection_or_request):
        """
Initializes default values from the a connection or request instance.

:param connection_or_request: (object) Connection or request instance

:since: v1.0.0
        """

        if (not isinstance(connection_or_request, AbstractHttpMixin)): raise TypeException("Request instance given is invalid")
        AbstractInnerRequest.init(self, connection_or_request)

        self._parent_request = connection_or_request._parent_request
        if (self._parent_request is None): self._parent_request = connection_or_request

        if (connection_or_request.is_supported("accepted_formats")): self._accepted_formats = connection_or_request.accepted_formats
        if (connection_or_request.is_supported("compression")): self._compression_formats = connection_or_request.compression_formats
        if (connection_or_request.is_supported("headers")): self._headers = connection_or_request.headers
        self._lang = connection_or_request.lang
        self._lang_default = connection_or_request.lang_default
        if (connection_or_request.is_supported("type")): self._type = connection_or_request.type

        self.script_path_name = connection_or_request.script_path_name
    #

    def prepare_body_instance(self, request_body_instance = None, content_type_expected = None):
        """
Returns a configured RequestBody instance to be read by the Request
implementation.

:param request_body_instance: RequestBody instance to be configured
:param content_type_expected: Expected Content-Type header if any to use the
                              RequestBody instance.

:return: (object) Configured RequestBody instance
:since:  v1.0.0
        """

        parent_request = self._parent_request

        return (None
                if (parent_request is None) else
                parent_request.prepare_body_instance(request_body_instance, content_type_expected)
               )
    #

    def _supports_accepted_formats(self):
        """
Returns false if accepted formats can not be identified.

:return: (bool) True if accepted formats are identified.
:since:  v1.0.0
        """

        return (self._accepted_formats is not None)
    #

    def _supports_compression(self):
        """
Returns false if supported compression formats can not be identified.

:return: (bool) True if compression formats are identified.
:since:  v1.0.0
        """

        return (self._compression_formats is not None)
    #
#
