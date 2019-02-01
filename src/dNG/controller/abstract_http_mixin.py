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

from os import path
import re

from dNG.data.rfc.header import Header
from dNG.data.text.input_filter import InputFilter
from dNG.data.text.uri import Uri
from dNG.data.translatable_exception import TranslatableException
from dNG.runtime.not_implemented_exception import NotImplementedException

from .abstract_inner_request import AbstractInnerRequest
from .abstract_response import AbstractResponse

class AbstractHttpMixin(object):
    """
"AbstractHttpMixin" is used to support common methods for HTTP request
instances.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    RE_NON_WORD_CHARS = re.compile("\\W+")
    """
RegExp to find non-word characters
    """

    def __init__(self):
        """
Constructor __init__(AbstractInnerHttpRequest)

:since: v1.0.0
        """

        self._action = None
        """
Requested action
        """
        self._headers = { }
        """
HTTP request headers
        """
        self._lang = ""
        """
User requested language
        """
        self._lang_default = ""
        """
Request based default language
        """
        self._module_package = None
        """
Request package name the module file belongs to
        """
        self._service_package_and_module = None
        """
Request package name the module file belongs to
        """
        self._parent_request_instance = None
        """
Executable parent request
        """
        self._path = None
        """
Request path
        """
        self._script_name = None
        """
Called script
        """
        self._script_path_name = None
        """
Request path to the script
        """
        self.timezone = None
        """
Source timezone
        """
        self._type = None
        """
Request type
        """
        self._output_handler = None
        """
Requested response format handler
        """

        self._server_scheme = "http"

        self.supported_features['accepted_formats'] = self._supports_accepted_formats
        self.supported_features['compression'] = self._supports_compression
        self.supported_features['headers'] = self._supports_headers
        self.supported_features['session'] = True
        self.supported_features['type'] = self._supports_type
    #

    @property
    def accepted_formats(self):
        """
Returns the formats the client accepts.

:return: (list) Accepted formats
:since:  v1.0.0
        """

        _return = [ ]

        formats = self.get_header("Accept")
        if (formats is not None): formats = Header.get_field_list_dict(formats, field_separator = None)
        if (formats is None): formats = [ ]

        for _format in formats: _return.append(_format.split(";")[0])

        return _return
    #

    @property
    def action(self):
        """
Returns the requested action.

:return: (str) Action requested
:since:  v1.0.0
        """

        return ("index" if (self._action is None) else self._action)
    #

    @action.setter
    def action(self, action):
        """
Sets the requested action.

:param action: Action requested

:since: v1.0.0
        """

        action = action.strip()
        if (action not in ( "", "-" )): self._action = AbstractHttpMixin.RE_NON_WORD_CHARS.sub("_", action)
    #

    @property
    def compression_formats(self):
        """
Returns the compression formats the client accepts.

:return: (list) Accepted compression formats
:since:  v1.0.0
        """

        _return = [ ]

        formats = self.get_header("Accept-Encoding")
        if (formats is not None): formats = Header.get_field_list_dict(formats, field_separator = None)
        if (formats is None): formats = [ ]

        for _format in formats: _return.append(_format.split(";")[0])

        return _return
    #

    @property
    def cookies(self):
        """
Returns request cookies.

:return: (dict) Request cookie name as key and value
:since:  v1.0.0
        """

        _return = { }

        cookies = Header.get_field_list_dict(InputFilter.filter_control_chars(self.get_header("Cookie")), ";", "=")
        for cookie in cookies: _return[cookie['key']] = cookie['value']

        return _return
    #

    @property
    def headers(self):
        """
Returns the request headers as dict.

:return: (dict) Headers
:since:  v1.0.0
        """

        return self._headers.copy()
    #

    @property
    def module_package(self):
        """
Returns the requested module package name.

:return: (str) Module package name requested
:since:  v1.0.0
        """

        return ("services" if (self._module_package is None) else self._module_package)
    #

    @module_package.setter
    def module_package(self, name):
        """
Sets the requested module package name.

:param name: Module package name requested

:since: v1.0.0
        """

        name = name.strip()
        if (name not in ( "", "-" )): self._module_package = AbstractHttpMixin.RE_NON_WORD_CHARS.sub("_", name)
    #

    @property
    def lang(self):
        """
Returns the requested or supported language.

:return: (str) Language identifier
:since:  v1.0.0
        """

        return self._lang
    #

    @property
    def lang_default(self):
        """
Returns the default language.

:return: (str) Language identifier
:since:  v1.0.0
        """

        return self._lang_default
    #

    @property
    def output_handler(self):
        """
Returns the requested output format.

:return: (str) Requested output format
:since:  v1.0.0
        """

        return ("http_xhtml" if (self._output_handler is None) else self._output_handler)
    #

    @property
    def path(self):
        """
Returns the request path.

:return: (str) Request path
:since:  v1.0.0
        """

        return self._path
    #

    @path.setter
    def path(self, _path):
        """
Sets the request path.

:param _path: Request path

:since: v1.0.0
        """

        if (_path[:1] == "/"):
            _path = _path[1:]
        #

        self._parameters['_raw_path'] = _path

        path_data = _path.strip().split("/", 3)
        path_data_length = len(path_data)

        self.module_package = Uri.decode_query_value(path_data[0])

        service_package_and_module = ""
        action = ""

        if (path_data_length > 1):
            if (path_data_length == 2): action = Uri.decode_query_value(path_data[1])
            else:
                service_package_and_module = Uri.decode_query_value(path_data[1]).replace(" ", ".")
                action = Uri.decode_query_value(path_data[2])
            #
        #

        self.service_package_and_module = service_package_and_module
        self.action = action

        if (path_data_length == 4 and path_data[3] != ""): self._parameters['path_raw_data'] = path_data[3]

        self._path = "/{0}/{1}/{2}/{3}".format(Uri.encode_query_value(self.module_package),
                                               Uri.encode_query_value(self.service_package_and_module.replace(".", " ")),
                                               Uri.encode_query_value(self.action),
                                               self.get_parameter("path_raw_data", "")
                                              )
    #

    @property
    def _parent_request(self):
        """
Returns the parent request if any.

:return: (dict) Request instance
:since:  v1.0.0
        """

        return self._parent_request_instance
    #

    @_parent_request.setter
    def _parent_request(self, parent_request):
        """
Sets the parent request used for execution of chained requests.

:param parent_request: Executable parent request

:since: v1.0.0
        """

        self._parent_request_instance = parent_request
    #

    @property
    def script_name(self):
        """
Returns the script name.

:return: (str) Script name
:since:  v1.0.0
        """

        return self._script_name
    #

    @property
    def script_path_name(self):
        """
Returns the script path and name of the request.

:return: (str) Script path and name
:since:  v1.0.0
        """

        return self._script_path_name
    #

    @script_path_name.setter
    def script_path_name(self, script_path_name):
        """
Sets the script path and name of the request.

:param script_path_name: Script path and name

:since: v1.0.0
        """

        if (script_path_name is not None):
            self._script_name = path.basename(script_path_name)
            self._script_path_name = script_path_name
        #
    #

    @property
    def session(self):
        """
Returns the associated session.

:return: (object) Session instance
:since:  v1.0.0
        """

        raise NotImplementedException()
    #

    @session.setter
    def session(self, session):
        """
Sets the associated session.

:param session: (object) Session instance

:since: v1.0.0
        """

        raise NotImplementedException()
    #

    @property
    def service_package_and_module(self):
        """
Returns the requested service package and module name.

:return: (str) Service package and module requested
:since:  v1.0.0
        """

        return ("index" if (self._service_package_and_module is None) else self._service_package_and_module)
    #

    @service_package_and_module.setter
    def service_package_and_module(self, name):
        """
Sets the requested service package and module name.

:param name: Service package and module requested

:since: v1.0.0
        """

        name = name.strip()

        if (name != "-"):
            name = re.sub("(\\.){2,}", ".", re.sub("[^\\w.]+", "_", name))
            if (name != ""): self._service_package_and_module = name
        #
    #

    @property
    def type(self):
        """
Returns the request type.

:return: (str) Request type
:since:  v1.0.0
        """

        return self._type
    #

    def get_cookie(self, name):
        """
Returns the request cookie if defined.

:param name: Cookie name

:return: (str) Cookie value if set; None otherwise
:since:  v1.0.0
        """

        cookies = self.cookies
        return (cookies[name] if (name in cookies) else None)
    #

    def get_header(self, name):
        """
Returns the request header if defined.

:param name: Header name

:return: (str) Header value if set; None otherwise
:since:  v1.0.0
        """

        name = name.lower()
        return self._headers.get(name)
    #

    def redirect(self, request, response = None):
        """
A request redirect executes the given new request as if it has been
requested by the client. It will reset the response and its cached values.

:param request: Request instance to be redirected to
:param response: Waiting response object

:since: v1.0.0
        """

        # pylint: disable=protected-access

        if (isinstance(request, AbstractInnerRequest)):
            parent_request = self._parent_request
            if (parent_request is None): parent_request = self

            request.init(self)
            if (not isinstance(response, AbstractResponse)): response = AbstractResponse.get_instance()

            parent_request._execute(request, response)
        else: raise TranslatableException("core_unsupported_command")
    #

    def set_header(self, name, value):
        """
Set the header with the given name and value.

:param name: Header name
:param value: Header value

:since: v1.0.0
        """

        name = name.lower()

        self._headers[name] = ("{0},{1}".format(self._headers[name], value)
                               if (name in self._headers) else
                               value
                              )
    #

    def _supports_accepted_formats(self):
        """
Returns false if accepted formats can not be identified.

:return: (bool) True if accepted formats are identified.
:since:  v1.0.0
        """

        return (self._supports_headers() and self.get_header("Accept") is not None)
    #

    def _supports_compression(self):
        """
Returns false if supported compression formats can not be identified.

:return: (bool) True if compression formats are identified.
:since:  v1.0.0
        """

        return (self._supports_headers() and self.get_header("Accept-Encoding") is not None)
    #

    def _supports_headers(self):
        """
Returns false if headers are not received.

:return: (bool) True if the request contains headers.
:since:  v1.0.0
        """

        return (self.headers is not None)
    #

    def _supports_type(self):
        """
Returns true if the request type is known.

:return: (bool) True if request type is known
:since:  v1.0.0
        """

        return (self._type is not None)
    #
#
