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

# pylint: disable=import-error,invalid-name,no-name-in-module

from os import path
from time import time, timezone
from weakref import ref
import os
import re

try: from collections.abc import Mapping
except ImportError: from collections import Mapping

from dNG.data.http.request_body.data import Data as RequestBodyData
from dNG.data.http.request_body.multipart_form_data import MultipartFormData as RequestBodyMultipartFormData
from dNG.data.http.request_body.urlencoded import Urlencoded as RequestBodyUrlencoded
from dNG.data.http.virtual_route import VirtualRoute
from dNG.data.rfc.header import Header
from dNG.data.settings import Settings
from dNG.data.text.input_filter import InputFilter
from dNG.data.text.l10n import L10n
from dNG.data.text.uri import Uri
from dNG.plugins.hook import Hook
from dNG.runtime.exception_log_trap import ExceptionLogTrap
from dNG.runtime.named_loader import NamedLoader
from dNG.runtime.type_exception import TypeException

try:
    from dNG.database.connection import Connection
    from dNG.database.transaction_context import TransactionContext
except ImportError: Connection = None

try:
    from dNG.data.session.http_adapter import HttpAdapter as HttpSessionAdapter
    from dNG.data.session.implementation import Implementation as Session
except ImportError: Session = None

from .abstract_http_mixin import AbstractHttpMixin
from .abstract_inner_request import AbstractInnerRequest
from .abstract_request import AbstractRequest
from .abstract_response import AbstractResponse
from .stdout_stream_response import StdoutStreamResponse

class AbstractHttpRequest(AbstractRequest, AbstractHttpMixin):
    """
"AbstractHttpRequest" implements HTTP request related methods.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=unused-argument

    RE_PARAMETER_FILTERED_CHARS = re.compile("[/\\\\?:@=&.]")
    """
RegExp to find characters to be filtered out
    """

    def __init__(self):
        """
Constructor __init__(AbstractHttpRequest)

:since: v1.0.0
        """

        AbstractRequest.__init__(self)
        AbstractHttpMixin.__init__(self)

        self.body_fp = None
        """
Request body pointer
        """
        self._executing_request = None
        """
A reference of the currently executing instance.
        """
        self._inner_request = None
        """
A inner request is used to support protocols based on other ones (e.g.
JSON-RPC based on HTTP).
        """
        self._query_string = ""
        """
Request query string
        """
        self._session = None
        """
Associated session to request
        """

        self._log_handler = NamedLoader.get_singleton("dNG.data.logging.LogHandler", False)

        self.supported_features['executing_request'] = True
        self.supported_features['inner_request'] = True
        self.supported_features['query_string'] = True
    #

    @property
    def executing_request(self):
        """
Returns the currently executing request instance.

:return: (object) Request instance; None if not available
:since:  v1.0.0
        """

        return (None if (self._executing_request is None) else self._executing_request())
    #

    @property
    def inner_request(self):
        """
Returns the inner request instance.

:return: (object) Request instance; None if not available
:since:  v1.0.0
        """

        return self._inner_request
    #

    @inner_request.setter
    def inner_request(self, request):
        """
Sets the inner request object.

:param request: Request object

:since: v1.0.0
        """

        if (not isinstance(request, AbstractInnerRequest)): raise TypeException("Inner request given is invalid")
        self._inner_request = request
    #

    @property
    def query_string(self):
        """
Returns the raw request query string.

:return: (str) Raw query string
:since:  v1.0.0
        """

        return self._query_string
    #

    @property
    def session(self):
        """
Returns the associated session.

:return: (object) Session instance
:since:  v1.0.0
        """

        return self._session
    #

    @session.setter
    def session(self, session):
        """
Sets the associated session.

:param session: Session instance

:since: v1.0.0
        """

        self._session = session

        response = AbstractResponse.get_instance()

        if (response is not None
            and session is not None
            and (not session.is_persistent)
           ): response.runtime_settings['x_pas_http_session_uuid'] = session.uuid
    #

    def execute(self):
        """
Executes the incoming request.

:since: v1.0.0
        """

        # pylint: disable=broad-except

        if (self.inner_request is None and Settings.get("pas_http_site_call_init_inner_request", True)):
            Hook.call("dNG.pas.http.Request.initInnerRequest", request = self)
        #

        if (self.inner_request is not None):
            request = self.inner_request

            request_output_handler = request.output_handler
            if (request_output_handler is not None): self._output_handler = request_output_handler
        else: request = self

        response = self._init_response()

        if (request.is_supported("type")
            and request.type == "HEAD"
            and response.is_supported("headers")
           ): response.send_only_headers = True

        try:
            if (self.is_supported("accepted_formats")):
                accepted_formats = self.accepted_formats
                if (len(accepted_formats) > 0): response.accepted_formats = accepted_formats
            #

            if (self.is_supported("compression")):
                compression_formats = self.compression_formats
                if (len(compression_formats) > 0): response.compression_formats = compression_formats
            #

            if (response.is_supported("script_name")): response.script_name = request.script_name

            if (Settings.get("pas_http_site_events_call_on_execute", False)): Hook.call("dNG.pas.http.Request.onExecute", request = request, response = response)

            self._executing_request = ref(request)

            if (request.is_supported("execution")): request.execute(response)
            else: self._execute(request, response)
        except Exception as handled_exception:
            if (self._log_handler is not None): self._log_handler.error(handled_exception, context = "pas_http_core")
            response.handle_exception(None, handled_exception)
        finally: self._executing_request = None

        if (Settings.get("pas_http_site_events_call_on_response", False)): Hook.call("dNG.pas.http.Request.onResponse", request = request, response = response)
        self._respond(response)
    #

    def _execute(self, request, response):
        """
Executes the given request and generate content for the given response.

:param request: Request to be executed
:param response: Response instance to be used

:since: v1.0.0
        """

        module_package = request.module_package

        service_package_and_module_data = request.service_package_and_module.rsplit(".", 1)
        service_class_name = NamedLoader.get_camel_case_class_name(service_package_and_module_data.pop())
        service_package_and_module_data.append(service_class_name)

        service_package_and_module = ".".join(service_package_and_module_data)

        if (self._log_handler is not None): self._log_handler.debug("{0!r} has been called for 'dNG.module.{1}.{2}'", self, module_package, service_package_and_module, context = "pas_http_core")

        if (NamedLoader.is_defined("dNG.module.{0}.{1}".format(module_package, service_package_and_module))):
            instance = NamedLoader.get_instance("dNG.module.{0}.{1}".format(module_package, service_package_and_module))
            instance.init(request, response)
            instance.execute()

            del(instance)
        else: self.handle_missing_service(response)
    #

    def handle_missing_service(self, response):
        """
"handle_missing_service()" is called if the requested service has not been
found.

:param response: Waiting response object

:since: v1.0.0
        """

        if (response.is_supported("headers")): response.set_header("HTTP", "HTTP/2.0 404 Not Found", True)

        response.handle_error("core_unsupported_command"
                              if (self.path == "/services/index/index/") else
                              "pas_http_core_404"
                             )
    #

    def _handle_upgrade(self, virtual_path_name, stream_response):
        """
Handles an intercepted HTTP upgrade request.

:return: (bool) True if handled successfully
:since:  v1.0.0
        """

        return (True
                if (Hook.call("dNG.pas.http.Request.handleUpgrade",
                              request = self,
                              virtual_request_path_name = virtual_path_name,
                              stream_response = stream_response
                             )
                   ) else
                False
               )
    #

    def _init_request(self):
        """
Do preparations for request handling.

:since: v1.0.0
        """

        """
Set source variables. The server timezone will be changed if a user is
logged in and/or its timezone is identified.
        """

        if (Settings.get("x_pas_http_base_url") is None):
            link_class = NamedLoader.get_class("dNG.data.text.Link")
            Settings.set("x_pas_http_base_url", link_class().build_url(link_class.TYPE_ABSOLUTE_URL | link_class.TYPE_BASE_PATH))
        #

        content_type = self.get_header("Content-Type")

        if (content_type is not None):
            content_type = content_type.lower()

            if (content_type not in ( "text/html", "application/xhtml+xml" )):
                content_type_output_handler = Hook.call("dNG.pas.http.Request.getOutputHandlerForContentType", request = self)
                if (content_type_output_handler is not None): self._output_handler = content_type_output_handler
            #
        #

        self._parse_parameters()
        self.timezone = float(Settings.get("core_timezone", (timezone / 3600)))
    #

    def _init_request_body(self, content_type):
        """
Returns the RequestBody instance to be read by the Request implementation
matching the given content type.

:param content_type: Content type to be handled by the RequestBody instance

:return: (object) RequestBody instance; None if not supported
:since:  v1.0.0
        """

        _return = None

        if (content_type == "application/x-www-form-urlencoded"): _return = RequestBodyUrlencoded()
        elif (content_type[:19] == "multipart/form-data"): _return = RequestBodyMultipartFormData()
        elif (self.get_header("Content-Length") is not None
              or self.get_header("Transfer-Encoding") is not None
             ): _return = RequestBodyData()

        return _return
    #

    def _init_response(self):
        """
Initializes the matching response instance.

:return: (object) Response object
:since:  v1.0.0
        """

        # pylint: disable=broad-except

        response = NamedLoader.get_instance("dNG.controller.{0}Response".format("".join([word.capitalize() for word in self.output_handler.split("_")])))

        if (Connection is not None):
            with Connection.get_instance(), ExceptionLogTrap("pas_http_core"):
                session = self.session

                if (Session is not None):
                    Session.get_class().set_adapter(HttpSessionAdapter)

                    if (session is None):
                        session = Session.load(session_create = False)
                        self.session = session
                    else: session.set_thread_default()
                #

                if (session is not None):
                    if (not session.is_persistent): response.runtime_settings['x_pas_http_session_uuid'] = session.uuid
                    response.content_uncachable = True

                    if (self.lang == ""):
                        user_profile = session.user_profile
                        if (user_profile is not None): self._lang = user_profile.lang
                    #
                #
            #
        #

        if (self.lang == ""): self._lang = self.lang_default
        L10n.set_thread_lang(self.lang)

        L10n.init("core")
        L10n.init("pas_core")
        L10n.init("pas_http_core")

        if (self._log_handler is not None): response.log_handler = self._log_handler
        response.charset = L10n.get("lang_charset", "UTF-8")
        response.stream_response = self._init_stream_response()

        if (response.is_supported("headers") and self.type == "HEAD"): response.send_only_headers = True

        return response
    #

    def _init_stream_response(self):
        """
Initializes the matching stream response instance.

:return: (object) Stream response object
:since:  v1.0.0
        """

        return StdoutStreamResponse()
    #

    def _parse_parameters(self):
        """
Parses request parameters.

:since: v1.0.0
        """

        if (self.lang_default == ""):
            lang = InputFilter.filter_control_chars(self.get_header("Accept-Language"))

            if (lang is not None):
                lang = lang.lower().split(",", 1)[0]

                self._lang_default = AbstractHttpRequest.RE_PARAMETER_FILTERED_CHARS.sub("", lang)
            #
        #

        parameters = self._read_parameters()
        self._parameters = parameters

        if ("ohandler" in parameters
            and len(parameters['ohandler']) > 0
           ): self._output_handler = AbstractHttpRequest.RE_PARAMETER_FILTERED_CHARS.sub("", parameters['ohandler'])

        """
Initialize l10n
        """

        lang = (AbstractHttpRequest.RE_PARAMETER_FILTERED_CHARS.sub("", parameters['lang'])
                if ("lang" in parameters) else
                ""
               )

        if (lang != "" and os.access(path.join(Settings.get("path_lang"), lang, "core.json"), os.R_OK)): self._lang = lang
        else:
            if (self.lang_default == ""): lang_rfc_region = Settings.get("core_lang", "en_US")
            else: lang_rfc_region = self.lang_default.lower()

            lang_rfc_region = re.sub("\\W", "", lang_rfc_region)
            lang_domain = lang_rfc_region[:2]

            if (Settings.is_defined("pas_http_site_lang_{0}".format(lang_rfc_region))): lang_rfc_region = Settings.get("pas_http_site_lang_{0}".format(lang_rfc_region))
            elif (Settings.is_defined("pas_http_site_lang_{0}".format(lang_domain))): lang_domain = Settings.get("pas_http_site_lang_{0}".format(lang_domain))

            if (os.access(path.join(Settings.get("path_lang"), lang_rfc_region, "core.json"), os.R_OK)): self._lang_default = lang_rfc_region
            elif (os.access(path.join(Settings.get("path_lang"), lang_domain, "core.json"), os.R_OK)): self._lang_default = lang_domain
            else: self._lang_default = Settings.get("core_lang", "en")
        #
    #

    def _parse_virtual_route_config(self, virtual_route_config, virtual_path_name):
        """
Parses the given virtual config and returns a matching inner request
instance.

:return: (object) Inner request instance; None if not matched
:since:  v1.0.0
        """

        if (virtual_route_config is None): _return = None
        elif (virtual_route_config.get("path_parameters", False)):
            _return = NamedLoader.get_instance("dNG.controller.PredefinedHttpRequest")
            if ("ohandler" in virtual_route_config): _return.output_handler = virtual_route_config['ohandler']

            module_package = None
            service_package_and_module = None
            action = None

            parameters = None

            if ("m" in virtual_route_config): module_package = virtual_route_config['m']
            if ("s" in virtual_route_config): service_package_and_module = virtual_route_config['s']
            if ("a" in virtual_route_config): action = virtual_route_config['a']

            if (module_package is None
                and service_package_and_module is None
                and action is None
               ): _return.path = virtual_path_name[len(virtual_route_config['_path_prefix']):]
            else:
                _return.module_package = (self.module_package if (module_package is None) else module_package)

                _return.service_package_and_module = (self.service_package_and_module
                                                      if (service_package_and_module is None) else
                                                      service_package_and_module
                                                     )

                _return.action = ("-" if (action is None) else action)

                path_data = virtual_path_name[len(virtual_route_config['_path_prefix']):].rsplit("/", 1)
                parameters = (None if (len(path_data) < 2 or path_data[1] == "") else VirtualRoute.parse_dsd(path_data[1]))

                if ("path_parameter_key" in virtual_route_config):
                    if (parameters is None): parameters = { }
                    parameters[virtual_route_config['path_parameter_key']] = path_data[0]
                else: _return.set_parameter("path_raw_data", path_data[0])
            #

            if (parameters is not None): _return.parameters = parameters
        else:
            path_data = None

            if ("path_parameter_key" in virtual_route_config):
                path_data = (virtual_path_name[len(virtual_route_config['_path_prefix']):]
                             if ("_path_prefix" in virtual_route_config
                                 and virtual_path_name.lower().startswith(virtual_route_config['_path_prefix'])
                                ) else
                             virtual_path_name
                            )
            #

            if ("setup_callback" in virtual_route_config):
                if (path_data is not None): self._parameters[virtual_route_config['path_parameter_key']] = path_data
                _return = virtual_route_config['setup_callback'](self, virtual_route_config)
            elif ("m" in virtual_route_config or "s" in virtual_route_config or "a" in virtual_route_config or "path_parameter_key" in virtual_route_config):
                _return = NamedLoader.get_instance("dNG.controller.PredefinedHttpRequest")
                if ("ohandler" in virtual_route_config): _return.output_handler = virtual_route_config['ohandler']

                _return.module_package = virtual_route_config.get("m", self.module_package)
                _return.service_package_and_module = virtual_route_config.get("s", self.service_package_and_module)
                _return.action = virtual_route_config.get("a", self.action)

                if ("parameters" in virtual_route_config and isinstance(virtual_route_config['parameters'], Mapping)):
                    _return.parameters = virtual_route_config['parameters']
                #

                if (path_data is not None): _return.set_parameter(virtual_route_config['path_parameter_key'], path_data)
            #
        #

        if (isinstance(_return, AbstractInnerRequest)): _return.init(self)

        return _return
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

        content_type = InputFilter.filter_control_chars(self.get_header("Content-Type"))
        if (content_type is not None): content_type = content_type.split(";", 1)[0].lower()

        _return = (self._init_request_body(content_type)
                   if (request_body_instance is None) else
                   request_body_instance
                  )

        if (isinstance(_return, RequestBodyData)):
            content_length = InputFilter.filter_int(self.get_header("Content-Length"))

            if (content_type_expected is None): content_type_expected = [ content_type ]
            elif (not isinstance(content_type_expected, list)): content_type_expected = [ content_type_expected ]

            if (self.body_fp is not None
                and (content_type in content_type_expected)
                and ((content_length is not None and content_length > 0)
                     or "chunked" not in Header.get_field_list_dict(self.get_header("Transfer-Encoding"))
                    )
               ):
                if (content_length is not None): _return.size = content_length
                else: _return.chunk_encoded = True

                content_encoding = self.get_header("Content-Encoding")
                if (content_encoding is not None): _return.compression = content_encoding

                _return.headers = self.headers
                _return.input_ptr = self.body_fp

                self.body_fp = None
            else: _return = None
        #

        return _return
    #

    def _read_parameters(self):
        """
Reads and returns the request parameters from the incoming request.

:return: (dict) Request parameters
:since:  v1.0.0
        """

        return AbstractHttpRequest.parse_friendly_query_string(self.query_string)
    #

    def _respond(self, response):
        """
Respond the request with the given response.

:since: v1.0.0
        """

        # pylint: disable=broad-except,star-args

        if (Connection is not None):
            with Connection.get_instance(), ExceptionLogTrap("pas_http_core"):
                session = self.session

                if (session is not None and session.is_active):
                    user_profile = session.user_profile

                    if (user_profile is not None):
                        user_profile_data = { "lang": self.lang,
                                              "lastvisit_time": time(),
                                              "lastvisit_ip": self.client_host
                                            }

                        if ("theme" in self.parameters): user_profile_data['theme'] = self.parameters['theme']

                        with TransactionContext():
                            user_profile.set_data_attributes(**user_profile_data)
                            user_profile.save()

                            session.save()
                        #
                    #
                #
            #
        #

        AbstractRequest._respond(self, response)
    #

    @staticmethod
    def parse_friendly_query_string(query_string):
        """
Parses an (X)HTML friendly query string variant using ";" instead of "&".

:param query_string: Query string to be parsed

:return: (dict) Query string parameters
:since:  v1.0.0
        """

        _return = { }

        entry_list = query_string.split(";")

        for entry_value in entry_list:
            entry = entry_value.split("=", 1)

            if (len(entry[0]) > 0):
                entry_key = InputFilter.filter_control_chars(Uri.decode_query_value(entry[0]))

                entry_value = (Uri.decode_query_value(entry[1]) if (len(entry) == 2) else None)
                if (entry_key[-2:] == "[]"): entry_value = [ entry_value ]

                if (type(entry_value) is list and entry_key in _return): _return[entry_key].append(entry_value[0])
                else: _return[entry_key] = entry_value
            #
        #

        return _return
    #
#
