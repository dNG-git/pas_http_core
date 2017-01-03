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

try: from urllib.parse import quote_plus, unquote_plus
except ImportError: from urllib import quote_plus, unquote_plus

from dNG.data.http.request_body.data import Data as RequestBodyData
from dNG.data.http.request_body.multipart_form_data import MultipartFormData as RequestBodyMultipartFormData
from dNG.data.http.request_body.urlencoded import Urlencoded as RequestBodyUrlencoded
from dNG.data.rfc.header import Header
from dNG.data.settings import Settings
from dNG.data.text.input_filter import InputFilter
from dNG.data.text.l10n import L10n
from dNG.module.named_loader import NamedLoader
from dNG.plugins.hook import Hook
from dNG.runtime.exception_log_trap import ExceptionLogTrap

try:
    from dNG.database.connection import Connection
    from dNG.database.transaction_context import TransactionContext
except ImportError: Connection = None

from .abstract_http_mixin import AbstractHttpMixin
from .abstract_inner_request import AbstractInnerRequest
from .abstract_request import AbstractRequest
from .abstract_response import AbstractResponse
from .stdout_stream_response import StdoutStreamResponse

try:
    from dNG.data.session.http_adapter import HttpAdapter as HttpSessionAdapter
    from dNG.data.session.implementation import Implementation as Session
except ImportError: Session = None

class AbstractHttpRequest(AbstractRequest, AbstractHttpMixin):
    """
"AbstractHttpRequest" implements HTTP request related methods.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=unused-argument

    RE_PARAMETER_DSD_PLUS_SPAM_CHAR = re.compile("(\\+){3,}")
    """
RegExp to find more than 3 plus characters in a row
    """
    RE_PARAMETER_FILTERED_CHARS = re.compile("[/\\\\\\?:@\\=\\&\\.]")
    """
RegExp to find characters to be filtered out
    """
    RE_PARAMETER_FILTERED_WORD_CHARS = re.compile("[;\\x20\\+]")
    """
RegExp to find characters to be filtered out
    """
    RE_PARAMETER_NON_WORD_END = re.compile("\\W+$")
    """
RegExp to find non-word characters at the end of the string
    """
    RE_PARAMETER_NON_WORD_START = re.compile("^\\W+")
    """
RegExp to find non-word characters at the beginning of the string
    """
    RE_PARAMETER_PLUS_ENCODED_CHAR = re.compile("%2b", re.I)
    """
RegExp to find URL-encoded plus characters
    """
    RE_PARAMETER_PLUS_CHAR = re.compile("\\+")
    """
RegExp to find plus characters
    """
    RE_PARAMETER_SPACE_CHAR = re.compile("\\x20")
    """
RegExp to find space characters
    """

    def __init__(self):
        """
Constructor __init__(AbstractHttpRequest)

:since: v0.2.00
        """

        AbstractRequest.__init__(self)
        AbstractHttpMixin.__init__(self)

        self.body_fp = None
        """
Request body pointer
        """
        self.executing_request = None
        """
A reference of the currently executing instance.
        """
        self.inner_request = None
        """
A inner request is used to support protocols based on other ones (e.g.
JSON-RPC based on HTTP).
        """
        self.query_string = ""
        """
Request query string
        """
        self.session = None
        """
Associated session to request
        """

        self.log_handler = NamedLoader.get_singleton("dNG.data.logging.LogHandler", False)

        self.supported_features['executing_request'] = True
        self.supported_features['inner_request'] = True
        self.supported_features['query_string'] = True
    #

    def execute(self):
        """
Executes the incoming request.

:since: v0.2.00
        """

        # pylint: disable=broad-except

        if (self.inner_request is not None):
            request = self.inner_request
            request_output_handler = request.get_output_handler()
            if (request_output_handler is not None): self.output_handler = request_output_handler
        else: request = self

        response = self._init_response()

        if (request.is_supported("type")
            and request.get_type() == "HEAD"
            and response.is_supported("headers")
           ): response.set_send_headers_only(True)

        try:
            if (self.is_supported("accepted_formats")):
                accepted_formats = self.get_accepted_formats()
                if (len(accepted_formats) > 0): response.set_accepted_formats(accepted_formats)
            #

            if (self.is_supported("compression")):
                compression_formats = self.get_compression_formats()
                if (len(compression_formats) > 0): response.set_compression_formats(compression_formats)
            #

            if (response.is_supported("script_name")): response.set_script_name(request.get_script_name())

            if (Settings.get("pas_http_site_events_call_on_execute", False)): Hook.call("dNG.pas.http.Request.onExecute", request = request, response = response)
            self._execute(request, response)
        except Exception as handled_exception:
            if (self.log_handler is not None): self.log_handler.error(handled_exception, context = "pas_http_core")
            response.handle_exception(None, handled_exception)
        #

        if (Settings.get("pas_http_site_events_call_on_reponse", False)): Hook.call("dNG.pas.http.Request.onResponse", request = request, response = response)
        self._respond(response)
    #

    def _execute(self, request, response):
        """
Executes the given request and generate content for the given response.

:since: v0.2.00
        """

        self.executing_request = ref(request)

        requested_module = request.get_module()

        requested_service_path_elements = request.get_service().rsplit(".", 1)

        requested_service_class_name = requested_service_path_elements.pop()
        requested_service_class_name = "".join([word.capitalize() for word in requested_service_class_name.split("_")])

        requested_service = ".".join(requested_service_path_elements + [ requested_service_class_name ])

        if (self.log_handler is not None): self.log_handler.debug("{0!r} has been called for 'dNG.module.controller.{1}.{2}'", self, requested_module, requested_service, context = "pas_http_core")

        if (NamedLoader.is_defined("dNG.module.controller.{0}.{1}".format(requested_module, requested_service))):
            instance = NamedLoader.get_instance("dNG.module.controller.{0}.{1}".format(requested_module, requested_service))
            instance.init(request, response)
            instance.execute()

            del(instance)
        else:
            if (NamedLoader.is_defined("dNG.module.controller.{0}.Module".format(requested_module))):
                instance = NamedLoader.get_instance("dNG.module.controller.{0}.Module".format(requested_module))
                instance.init(request, response)

                del(instance)
            #

            self.handle_missing_service(response)
        #
    #

    def get_executing_request(self):
        """
Returns the currently executing request instance.

:return: (object) Request instance; None if not available
:since:  v0.2.00
        """

        return (None if (self.executing_request is None) else self.executing_request())
    #

    def get_inner_request(self):
        """
Returns the inner request instance.

:return: (object) Request instance; None if not available
:since:  v0.2.00
        """

        return self.inner_request
    #

    def get_query_string(self):
        """
Returns the raw request query string.

:return: (str) Raw query string
:since:  v0.2.00
        """

        return self.query_string
    #

    def get_session(self):
        """
Returns the associated session.

:return: (object) Session instance
:since:  v0.2.00
        """

        return self.session
    #

    def handle_missing_service(self, response):
        """
"handle_missing_service()" is called if the requested service has not been
found.

:param response: Waiting response object

:since: v0.2.00
        """

        if (response.is_supported("headers")): response.set_header("HTTP/1.1", "HTTP/1.1 404 Not Found", True)
        response.handle_critical_error("core_unsupported_command")
    #

    def _handle_upgrade(self, virtual_path_name, stream_response):
        """
Handles an intercepted HTTP upgrade request.

:return: (bool) True if handled successfully
:since:  v0.2.00
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

:since: v0.2.00
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
                if (content_type_output_handler is not None): self.output_handler = content_type_output_handler
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
:since:  v0.2.00
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
:since:  v0.2.00
        """

        # pylint: disable=broad-except

        response = NamedLoader.get_instance("dNG.controller.{0}Response".format("".join([word.capitalize() for word in self.output_handler.split("_")])))

        if (Connection is not None):
            with Connection.get_instance(), ExceptionLogTrap("pas_http_core"):
                session = self.get_session()

                if (Session is not None):
                    Session.get_class().set_adapter(HttpSessionAdapter)

                    if (session is None):
                        session = Session.load(session_create = False)
                        self.set_session(session)
                    else: session.set_thread_default()
                #

                if (session is not None):
                    if (not session.is_persistent()): response.get_runtime_settings()['x_pas_http_session_uuid'] = session.get_uuid()
                    response.set_content_dynamic(True)

                    if (self.lang == ""):
                        user_profile = session.get_user_profile()
                        if (user_profile is not None): self.lang = user_profile.get_lang()
                    #
                #
            #
        #

        if (self.lang == ""): self.lang = self.lang_default
        L10n.set_thread_lang(self.lang)

        L10n.init("core")
        L10n.init("pas_core")
        L10n.init("pas_http_core")

        if (self.log_handler is not None): response.set_log_handler(self.log_handler)
        response.set_charset(L10n.get("lang_charset", "UTF-8"))
        response.set_stream_response(self._init_stream_response())

        if (response.is_supported("headers") and self.type == "HEAD"): response.set_send_headers_only(True)

        return response
    #

    def _init_stream_response(self):
        """
Initializes the matching stream response instance.

:return: (object) Stream response object
:since:  v0.2.00
        """

        return StdoutStreamResponse()
    #

    def _parse_parameters(self):
        """
Parses request parameters.

:since: v0.2.00
        """

        if (self.lang_default == ""):
            lang = InputFilter.filter_control_chars(self.get_header("Accept-Language"))
            if (lang is not None): self.lang_default = lang.lower().split(",", 1)[0]
        #

        self.parameters = self._get_request_parameters()

        if ("a" in self.parameters): self.action = AbstractHttpRequest.filter_parameter_word(self.parameters['a'])
        if ("m" in self.parameters): self.module = AbstractHttpRequest.filter_parameter_word(self.parameters['m'])
        if ("s" in self.parameters): self.service = AbstractHttpRequest.filter_parameter_service(self.parameters['s'])

        if ("dsd" in self.parameters): self.dsd = AbstractHttpRequest.parse_dsd(self.parameters['dsd'])

        if ("ohandler" in self.parameters
            and len(self.parameters['ohandler']) > 0
           ): self.output_handler = AbstractHttpRequest.filter_parameter_word(self.parameters['ohandler'])

        """
Initialize l10n
        """

        lang = (AbstractHttpRequest.filter_parameter(self.parameters['lang']) if ("lang" in self.parameters) else "")

        if (lang != "" and os.access(path.join(Settings.get("path_lang"), lang, "core.json"), os.R_OK)): self.lang = lang
        else:
            if (self.lang_default == ""): lang_rfc_region = Settings.get("core_lang", "en_US")
            else: lang_rfc_region = self.lang_default.lower()

            lang_rfc_region = re.sub("\\W", "", lang_rfc_region)
            lang_domain = lang_rfc_region[:2]

            if (Settings.is_defined("pas_http_site_lang_{0}".format(lang_rfc_region))): lang_rfc_region = Settings.get("pas_http_site_lang_{0}".format(lang_rfc_region))
            elif (Settings.is_defined("pas_http_site_lang_{0}".format(lang_domain))): lang_domain = Settings.get("pas_http_site_lang_{0}".format(lang_domain))

            if (os.access(path.join(Settings.get("path_lang"), lang_rfc_region, "core.json"), os.R_OK)): self.lang_default = lang_rfc_region
            elif (os.access(path.join(Settings.get("path_lang"), lang_domain, "core.json"), os.R_OK)): self.lang_default = lang_domain
            else: self.lang_default = Settings.get("core_lang", "en")
        #
    #

    def _parse_virtual_config(self, virtual_config, virtual_pathname):
        """
Parses the given virtual config and returns a matching inner request
instance.

:return: (object) Inner request instance; None if not matched
:since:  v0.2.00
        """

        if (virtual_config is None): _return = None
        elif (virtual_config.get("path_parameters", False)):
            _return = NamedLoader.get_instance("dNG.controller.PredefinedHttpRequest")

            encoded_parameters = virtual_pathname[len(virtual_config['_path_prefix']):].split("/")

            parameters = { }
            dsds = { }

            for encoded_parameter in encoded_parameters:
                parameter = encoded_parameter.split("+", 2)

                if (len(parameter) == 2): parameters[parameter[0]] = unquote_plus(parameter[1])
                elif (len(parameter) == 3 and parameter[0] == "dsd"): dsds[parameter[1]] = unquote_plus(parameter[2])
            #

            if ("ohandler" in virtual_config): _return.set_output_handler(virtual_config['ohandler'])

            is_module_set = True
            is_service_set = True
            is_action_set = True

            if ("m" in virtual_config): _return.set_module(virtual_config['m'])
            elif ("m" in parameters): _return.set_module(parameters['m'])
            else: is_module_set = False

            if ("s" in virtual_config): _return.set_service(virtual_config['s'])
            elif ("s" in parameters): _return.set_service(parameters['s'])
            else: is_service_set = False

            if ("a" in virtual_config): _return.set_action(virtual_config['a'])
            elif ("a" in parameters): _return.set_action(parameters['a'])
            else: is_action_set = False

            if (is_module_set or is_service_set or is_action_set):
                for key in dsds: _return.set_dsd(key, dsds[key])
            else:
                _return.set_module(self.get_module())
                _return.set_service(self.get_service())
                _return.set_action(self.get_action())
                _return.set_dsd_dict(self.get_dsd_dict())
            #
        elif ("setup_callback" in virtual_config):
            if ("path" in virtual_config):
                path = (virtual_pathname[len(virtual_config['_path_prefix']):]
                        if ("_path_prefix" in virtual_config and virtual_pathname.lower().startswith(virtual_config['_path_prefix'])) else
                        virtual_pathname
                       )

                self.set_dsd(virtual_config['path'], path)
            #

            _return = virtual_config['setup_callback'](self, virtual_config)
        elif ("m" in virtual_config or "s" in virtual_config or "a" in virtual_config or "path" in virtual_config):
            _return = NamedLoader.get_instance("dNG.controller.PredefinedHttpRequest")

            if ("ohandler" in virtual_config): _return.set_output_handler(virtual_config['ohandler'])

            if ("m" in virtual_config): _return.set_module(virtual_config['m'])
            if ("s" in virtual_config): _return.set_service(virtual_config['s'])
            if ("a" in virtual_config): _return.set_action(virtual_config['a'])

            if ("dsd" in virtual_config and isinstance(virtual_config['dsd'], dict)):
                for key in virtual_config['dsd']: _return.set_dsd(key, virtual_config['dsd'][key])
            #

            if ("path" in virtual_config):
                path = (virtual_pathname[len(virtual_config['_path_prefix']):]
                        if ("_path_prefix" in virtual_config and virtual_pathname.lower().startswith(virtual_config['_path_prefix'])) else
                        virtual_pathname
                       )

                _return.set_dsd(virtual_config['path'], path)
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
:since:  v0.2.00
        """

        content_type = InputFilter.filter_control_chars(self.get_header("Content-Type"))
        if (content_type is not None): content_type = content_type.split(";", 1)[0].lower()

        _return = (self._init_request_body(content_type)
                   if (request_body_instance is None) else
                   request_body_instance
                  )

        if (isinstance(_return, RequestBodyData)):
            content_length = InputFilter.filter_int(self.get_header("Content-Length"))

            if (self.body_fp is None
                or (content_type is not None and content_type != content_type_expected)
                or (content_length is None
                    and "chunked" not in Header.get_field_list_dict(self.get_header("Transfer-Encoding"))
                   )
                or (content_length is not None and content_length < 1)
               ): _return = None
            else:
                if (content_length is not None): _return.set_input_size(content_length)
                else: _return.define_input_chunk_encoded(True)

                content_encoding = self.get_header("Content-Encoding")
                if (content_encoding is not None): _return.define_input_compression(content_encoding)

                _return.set_headers(self.get_headers())
                _return.set_input_ptr(self.body_fp)

                self.body_fp = None
            #
        #

        return _return
    #

    def _respond(self, response):
        """
Respond the request with the given response.

:since: v0.2.00
        """

        # pylint: disable=broad-except,star-args

        if (Connection is not None):
            with Connection.get_instance(), ExceptionLogTrap("pas_http_core"):
                if (self.session is not None and self.session.is_active()):
                    user_profile = self.session.get_user_profile()

                    if (user_profile is not None):
                        user_profile_data = { "lang": self.lang,
                                              "lastvisit_time": time(),
                                              "lastvisit_ip": self.client_host
                                            }

                        if ("theme" in self.parameters): user_profile_data['theme'] = self.parameters['theme']

                        with TransactionContext():
                            user_profile.set_data_attributes(**user_profile_data)
                            user_profile.save()

                            self.session.save()
                        #
                    #
                #
            #
        #

        AbstractRequest._respond(self, response)
    #

    def set_inner_request(self, request):
        """
Sets the inner request object.

:param request: Request object

:since: v0.2.00
        """

        if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_inner_request()- (#echo(__LINE__)#)", self, context = "pas_http_core")
        self.inner_request = request
    #

    def set_session(self, session):
        """
Sets the associated session.

:param session: (object) Session instance

:since: v0.2.00
        """

        self.session = session

        response = AbstractResponse.get_instance()

        if (response is not None
            and session is not None
            and (not session.is_persistent())
           ): response.get_runtime_settings()['x_pas_http_session_uuid'] = session.get_uuid()
    #

    @staticmethod
    def filter_parameter(value):
        """
Filters the given parameter value.

:param value: Request parameter

:return: (str) Filtered parameter
:since:  v0.2.00
        """

        value = InputFilter.filter_control_chars(value)

        if (" " in value): value = quote_plus(value, "")
        value = AbstractHttpRequest.RE_PARAMETER_NON_WORD_START.sub("", value)
        value = AbstractHttpRequest.RE_PARAMETER_FILTERED_CHARS.sub("", value)

        return AbstractHttpRequest.RE_PARAMETER_NON_WORD_END.sub("", value)
    #

    @staticmethod
    def filter_parameter_service(value):
        """
Filter service like parameters.

:param value: Request parameter

:return: (str) Filtered parameter
:since:  v0.2.00
        """

        value = AbstractHttpRequest.filter_parameter(value)
        value = AbstractHttpRequest.RE_PARAMETER_PLUS_CHAR.sub(" ", value)
        return AbstractHttpRequest.RE_PARAMETER_SPACE_CHAR.sub(".", value)
    #

    @staticmethod
    def filter_parameter_word(value):
        """
Filter word parameters used for module and action statements.

:param value: Request parameter

:return: (str) Filtered parameter
:since:  v0.2.00
        """

        value = AbstractHttpRequest.filter_parameter(value)
        return AbstractHttpRequest.RE_PARAMETER_FILTERED_WORD_CHARS.sub("", unquote_plus(value))
    #

    @staticmethod
    def parse_dsd(dsd):
        """
DSD stands for dynamic service data and should be used for transfering IDs for
news, topics, ... Take care for injection attacks!

:param dsd: DSD string for parsing

:return: (dict) Parsed DSD
:since:  v0.2.00
        """

        dsd = InputFilter.filter_control_chars(dsd)

        if ("+" not in dsd and AbstractHttpRequest.RE_PARAMETER_PLUS_ENCODED_CHAR.search(dsd) is not None): dsd = unquote_plus(dsd)
        elif (" " in dsd): dsd = quote_plus(dsd, "")

        dsd = AbstractHttpRequest.RE_PARAMETER_DSD_PLUS_SPAM_CHAR.sub("++", dsd)

        dsd_list = dsd.split("++")
        _return = { }

        for dsd in dsd_list:
            dsd_element = dsd.strip().split("+", 1)

            if (len(dsd_element) > 1): _return[dsd_element[0]] = InputFilter.filter_control_chars(unquote_plus(dsd_element[1]))
            elif (len(dsd_element[0]) > 0): _return[dsd_element[0]] = ""
        #

        return _return
    #

    @staticmethod
    def parse_iline(iline):
        """
Parse the input variables given as an URI query string.

:param iline: Input query string with ";" delimiter.

:return: (dict) Parsed query string
:since:  v0.2.00
        """

        _return = { }

        if (iline is not None):
            iline_list = iline.split(";")

            for iline in iline_list:
                value_element = iline.split("=", 1)
                if (len(value_element) > 1): _return[value_element[0]] = value_element[1]
            #
        #

        return _return
    #
#
