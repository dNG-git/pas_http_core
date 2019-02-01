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

from dNG.data.file_like_copy_mixin import FileLikeCopyMixin
from dNG.vfs.file_like_wrapper_mixin import FileLikeWrapperMixin

class UploadedFile(FileLikeCopyMixin, FileLikeWrapperMixin):
    """
"UploadedFile" provides a file-like access for temporary, uploaded files.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    _FILE_WRAPPED_METHODS = ( "read",
                              "readline",
                              "seek",
                              "size",
                              "tell"
                            )

    def __init__(self):
        """
Constructor __init__(UploadedFile)

:since: v1.0.0
        """

        FileLikeCopyMixin.__init__(self)
        FileLikeWrapperMixin.__init__(self)

        self._client_content_type = None
        """
The client supplied content type.
        """
        self._client_file_name = None
        """
The client supplied file name.
        """
    #

    @property
    def client_content_type(self):
        """
Returns the client supplied content type.

:return: Client content type
:since:  v1.0.0
        """

        return self._client_content_type
    #

    @client_content_type.setter
    def client_content_type(self, content_type):
        """
Sets the client supplied content type.

:param file_name: Client content type

:since: v1.0.0
        """

        self._client_content_type = content_type
    #

    @property
    def client_file_name(self):
        """
Returns the client supplied file name.

:return: Client file name
:since:  v1.0.0
        """

        return self._client_file_name
    #

    @client_file_name.setter
    def client_file_name(self, file_name):
        """
Sets the client supplied file name.

:param file_name: Client file name

:since: v1.0.0
        """

        self._client_file_name = file_name
    #

    @property
    def is_eof(self):
        """
Checks if the uploaded file has reached EOF.

:return: (bool) True if EOF
:since:  v1.0.0
        """

        if (self._wrapped_resource is None): _return = True
        elif (hasattr(self._wrapped_resource, "is_eof")): _return = self._wrapped_resource.is_eof
        else: _return = (self.size == self.tell())

        return _return
    #

    @property
    def file(self):
        """
Returns the file-like resource to be used.

:return: (object) File-like resource
:since:  v1.0.0
        """

        return self._wrapped_resource
    #

    @file.setter
    def file(self, resource):
        """
Sets the file-like resource to be used.

:param resource: File-like resource

:since: v1.0.0
        """

        self._set_wrapped_resource(resource)
    #
#
