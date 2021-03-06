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

from collections import Iterable
from math import floor
import re

try: from urllib.parse import urlsplit
except ImportError: from urlparse import urlsplit

from dNG.controller.abstract_http_request import AbstractHttpRequest
from dNG.data.binary import Binary
from dNG.data.settings import Settings
from dNG.runtime.value_exception import ValueException

from .input_filter import InputFilter
from .uri import Uri

try: from dNG.data.session.implementation import Implementation as Session
except ImportError: Session = None

class Link(Uri):
    """
"Link" provides common methods to build them from parameters.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=unused-argument

    TYPE_ABSOLUTE_URL = 1
    """
Absolute URLs like "http://localhost/index.py?..."
    """
    TYPE_BASE_PATH = 1 << 3
    """
Generates URLs to the base path of this application.
    """
    TYPE_OPTICAL = 1 << 4
    """
Optical URLs are used to show the target address.
    """
    TYPE_PARAMETER_LESS = 1 << 6
    """
Generated URL will not handle parameters
    """
    TYPE_PREDEFINED_URL = 1 << 2
    """
Predefined URL
    """
    TYPE_RELATIVE_URL = 1 << 1
    """
Relative URLs like "index.py?..."
    """
    TYPE_VIRTUAL_PATH = 1 << 5
    """
Generates absolute URLs based on the "__virtual__" path parameter.
    """

    """
---i---
Inherited TYPE_* constants should start at 1 << 16.
---i---
    """

    def __init__(self, scheme = None, host = None, port = None, path = None):
        """
Constructor __init__(Link)

:param scheme: URL scheme
:param host: URL host
:param port: URL port
:param path: URL path

:since: v0.2.00
        """

        self.host = host
        """
Override for the URL host
        """
        self.path = path
        """
Override for the URL path
        """
        self.port = port
        """
Override for the URL port
        """
        self.scheme = scheme
        """
Override for the URL scheme
        """

        if (not Settings.is_defined("pas_http_site_preferred_url_base")): Settings.read_file("{0}/settings/pas_http.json".format(Settings.get("path_data")))
    #

    def _add_default_parameters(self, parameters):
        """
This method appends default parameters if not already set.

:param parameters: Parameters dict

:return: (dict) Appended parameters dict
:since:  v0.2.00
        """

        _return = parameters
        request = None

        if ("lang" not in _return):
            request = AbstractHttpRequest.get_instance()
            if (request is not None and request.get_lang() != request.get_lang_default()): _return['lang'] = request.get_lang()
        #

        if ("uuid" not in _return and Session is not None):
            if (request is None): request = AbstractHttpRequest.get_instance()
            session = (None if (request is None) else request.get_session())
            if (session is not None and session.is_active() and (not session.is_persistent())): _return['uuid'] = Session.get_thread_uuid()
        #

        return _return
    #

    def build_url(self, _type, parameters = None):
        """
Builds an URL string. You may use internal links "index.py?...", external
links like "http://localhost/index.py?...", input (hidden) forms or an URL,
replacing parts of it if it's larger than x characters. This function uses
"shadow" URLs to be search engine friendly if applicable and the request URI
as a source for parameters.

:param _type: Link type (see constants)
:param parameters: Parameters dict
:param escape: True to URL escape input

:return: (str) Formatted URL string
:since:  v0.2.00
        """

        if (type(_type) is not int): _type = self.__class__.get_type_int(_type)

        _return = self.get_url_base(_type, parameters)

        if (parameters is None
            or _type & Link.TYPE_BASE_PATH in ( Link.TYPE_BASE_PATH,
                                                Link.TYPE_PREDEFINED_URL
                                              )
           ): _type |= Link.TYPE_PARAMETER_LESS

        parameters = ({ }
                      if (_type & Link.TYPE_PARAMETER_LESS == Link.TYPE_PARAMETER_LESS) else
                      self._filter_parameters(parameters)
                     )

        if (_type & Link.TYPE_VIRTUAL_PATH == Link.TYPE_VIRTUAL_PATH):
            if (parameters is None or "__virtual__" not in parameters): raise ValueException("Virtual path URL requested but base path not defined")

            virtual_parameters = parameters.copy()

            virtual_base_path = (virtual_parameters['__virtual__'][1:]
                                 if (virtual_parameters['__virtual__'][:1] == "/") else
                                 virtual_parameters['__virtual__']
                                )

            del(virtual_parameters['__virtual__'])

            dsds = virtual_parameters.get("dsd")
            if (dsds is not None): del(virtual_parameters['dsd'])

            _return += virtual_base_path
            if (len(virtual_parameters) > 0): _return += "/" + self._build_url_formatted("{0}+{1}", "/", virtual_parameters)
            if (dsds is not None): _return += "/" + self._build_url_formatted("dsd+{0}+{1}", "/", dsds)
        else:
            if (_type & Link.TYPE_PARAMETER_LESS != Link.TYPE_PARAMETER_LESS):
                parameters = self._add_default_parameters(parameters)
            #

            if (len(parameters) > 0):
                if ("?" not in _return): _return += "?"
                elif (_return[-1:] != ";"): _return += ";"

                _return += self._build_url_formatted("{0}={1}", ";", parameters)
            #
        #

        if (_type & Link.TYPE_OPTICAL == Link.TYPE_OPTICAL):
            """
A filter is required for really long URLs. First we will have a look at the
"optical maximal length" setting, then if the URL is larger than the setting
            """

            length_available = int(Settings.get("pas_http_url_optical_max_length", 100))

            if (len(_return) > length_available):
                url_elements = urlsplit(_return)

                _return = "{0}://".format(url_elements.scheme)

                if (url_elements.username is not None or url_elements.password is not None):
                    _return += "{0}:{1}@".format(("" if (url_elements.username is None) else url_elements.username),
                                                 ("" if (url_elements.password is None) else url_elements.password)
                                                )
                #

                _return += ("" if (url_elements.hostname is None) else url_elements.hostname)

                if (url_elements.port is not None): _return += ":{0:d}".format(url_elements.port)
                path_length = len(url_elements.path)
                if (path_length > 0): basepath_position = (url_elements[:-1] if (url_elements[-1:] == "/") else url_elements).path.rfind("/")

                if (path_length > 0 and basepath_position > 0):
                    basepath_position += 1

                    file_name = url_elements.path[basepath_position:]
                    _return += url_elements.path[:basepath_position]
                else: file_name = url_elements.path

                if (len(url_elements.query + url_elements.fragment) > 0):
                    one_eighth = int(floor((length_available - 3) / 8))
                    one_fourth = one_eighth * 2
                    three_eigths = length_available - (one_fourth * 2) - one_eighth

                    """
Now we will find out, how to remove unimportant parts of the given URL
                    """

                    if (len(_return) < 3 + three_eigths + one_eighth):
                        """
The URL (excluding the file name) is small enough. We will add the whole
string to our result
                        """

                        length_available -= len(_return)
                    else:
                        """
The source URL is too large - we will strip everything, that's larger than
our projected size
                        """

                        _return = "{0} ... {1}".format(_return[:three_eigths], _return[-1 * one_eighth:])
                        length_available -= 3 + three_eigths + one_eighth
                    #

                    """
The next few lines will check the size of the filename and remove parts of
it if required
                    """

                    if (len(file_name) < 3 + one_fourth):
                        """
Again, the filename is small enough - no action is required
                        """

                        _return += file_name
                        length_available -= len(file_name)
                    else:
                        """
Unfortunately, the filename is too long - we will remove the first part
                        """

                        _return += " ... {0}".format(file_name[-1 * one_fourth])
                        length_available -= 3 + one_fourth
                    #

                    """
Our last step is to add the whole or the last part of the query string, once
more depending on the string length
                    """

                    query_fragment = ""
                    if (url_elements.query != ""): query_fragment += "?{0}".format(url_elements.query)
                    if (url_elements.fragment != ""): query_fragment += "#{0}".format(url_elements.fragment)

                    if (len(query_fragment) < 3 + length_available): _return += query_fragment
                    else: _return += " ... {0}".format(query_fragment[-1 * length_available:])
                #
            #
        #

        return _return
    #

    def _build_url_formatted(self, link_template, link_separator, parameters, _escape = None):
        """
Builds a template-defined string containing the given URL parameters.

:param link_template: Link template
:param link_separator: Link separator
:param parameters: Parameters dict
:param _escape: Data escape method

:return: (str) Formatted URL string
:since:  v0.2.00
        """

        # pylint: disable=protected-access

        _return = ""

        if (_escape is None): _escape = Link.encode_query_value

        for key in self.__class__._build_url_sorted_parameters(parameters.keys()):
            escaped_key = _escape(key)

            if (key == "dsd"):
                dsd_value = self._build_url_dsd_formatted(parameters[key], _escape)

                if (len(dsd_value) > 0):
                    if (_return != ""): _return += link_separator
                    _return += link_template.format("dsd", dsd_value)
                #
            elif (isinstance(parameters[key], dict)):
                for value_key in parameters[key]:
                    escaped_key = "{0}[{1}]".format(_escape(key), _escape(value_key))
                    escaped_value = _escape(parameters[key][value_key])

                    if (_return != ""): _return += link_separator
                    _return += link_template.format(escaped_key, escaped_value)
                #
            elif (isinstance(parameters[key], list)):
                for value in parameters[key]:
                    escaped_value = _escape(value)

                    if (_return != ""): _return += link_separator
                    _return += link_template.format("{0}[]".format(escaped_key), escaped_value)
                #
            else:
                escaped_value = _escape(parameters[key])

                if (_return != ""): _return += link_separator
                _return += link_template.format(escaped_key, escaped_value)
            #
        #

        return _return
    #

    def _build_url_dsd_formatted(self, parameters, _escape):
        """
Builds a URL DSD string.

:param parameters: Parameters dict
:param _escape: Data escape method

:return: (str) URL DSD string
:since:  v0.2.00
        """

        _return = ""
        _type = type(parameters)

        if (_type == dict):
            for key in sorted(parameters.keys()):
                escaped_key = _escape(key)
                escaped_value = Link.encode_query_value(parameters[key])

                if (_return != ""): _return += "++"
                _return += "{0}+{1}".format(escaped_key, escaped_value)
            #
        elif (_type == str): _return = parameters

        return _return
    #

    def _filter_parameters(self, parameters):
        """
This method filters parameters like "__<KEYWORD>__".

:param parameters: Parameters dict

:return: (dict) Filtered parameters dict
:since:  v0.2.00
        """

        if ("__query__" in parameters):
            _return = { }

            if (len(parameters) == 1 and len(parameters['__query__']) > 0):
                parameters = AbstractHttpRequest.parse_iline(InputFilter.filter_control_chars(parameters['__query__']))

                for parameter in parameters:
                    _return[parameter] = (AbstractHttpRequest.parse_dsd(parameters['dsd'])
                                          if (parameter == "dsd") else
                                          Link.decode_query_value(parameters[parameter])
                                         )
                #
            #
        else: _return = parameters.copy()

        if (_return.get("__link__", False)): del(_return['__link__'])
        elif (_return.get("__request__", False)):
            request = AbstractHttpRequest.get_instance()

            if (request.is_supported("executing_request")):
                executing_request = request.get_executing_request()
                if (executing_request is not None): request = executing_request
            #

            if (request.is_supported("inner_request")):
                inner_request = request.get_inner_request()
                if (inner_request is not None): request = inner_request
            #

            if (request is not None):
                if ("ohandler" not in _return
                    and request.get_parameter("ohandler") is not None
                   ): _return['ohandler'] = request.get_output_handler()

                if ("m" not in _return): _return['m'] = request.get_module()
                if ("s" not in _return): _return['s'] = request.get_service()
                if ("a" not in _return): _return['a'] = request.get_action()

                dsd_dict = request.get_dsd_dict()
                if (len(dsd_dict) and "dsd" not in _return): _return['dsd'] = { }

                for key in dsd_dict:
                    if (key not in _return['dsd']): _return['dsd'][key] = dsd_dict[key]
                #
            #

            del(_return['__request__'])
        #

        if ("s" in _return): _return['s'] = _return['s'].replace(".", " ")

        return self._filter_remove_parameters(_return)
    #

    def _filter_remove_parameters(self, parameters):
        """
This method removes all parameters marked as "__remove__" or special ones.

:param parameters: Parameters dict

:return: (dict) Filtered parameters dict
:since:  v0.2.00
        """

        _return = parameters.copy()

        for key in parameters:
            if (isinstance(parameters[key], dict) and len(parameters[key]) > 0): _return[key] = self._filter_remove_parameters(parameters[key])
            elif (parameters[key] == "__remove__"): del(_return[key])
        #

        if ("__host__" in parameters): del(_return['__host__'])
        if ("__path__" in parameters): del(_return['__path__'])
        if ("__port__" in parameters): del(_return['__port__'])
        if ("__scheme__" in parameters): del(_return['__scheme__'])

        return _return
    #

    def get_url_base(self, _type, parameters):
        """
Returns the base URL for the given type and parameters.

:param _type: Link type (see constants)
:param parameters: Link parameters

:return: (str) Base URL
:since:  v0.2.00
        """

        _return = ""

        if (_type & Link.TYPE_PREDEFINED_URL == Link.TYPE_PREDEFINED_URL):
            if ("__link__" not in parameters): raise ValueException("Required parameter not defined for the predefined URL")
            _return = parameters['__link__']
        elif (self.path is not None):
            if (_type & Link.TYPE_RELATIVE_URL != Link.TYPE_RELATIVE_URL):
                if (self.scheme is None): raise ValueException("Can't construct an absolute URL without an URI scheme")
                _return = "{0}://".format(Binary.str(self.scheme))

                if (self.host is None): raise ValueException("Can't construct an absolute URL without a host")
                _return += Binary.str(self.host)

                if (self.port is not None):
                    port = Link.filter_well_known_port(self.scheme, self.port)
                    if (port > 0): _return += ":{0:d}".format(port)
                #
            #

            path = ("/" if (self.path is None) else Binary.str(self.path))
            _return += ("/" if (path == "") else path)
        else:
            request = AbstractHttpRequest.get_instance()
            if (request is None): raise ValueException("Can't construct an URL from a request instance if it is not provided")

            if (_type & Link.TYPE_ABSOLUTE_URL == Link.TYPE_ABSOLUTE_URL):
                scheme = request.get_server_scheme()

                _return = "{0}://".format(Binary.str(scheme))

                host = request.get_server_host()
                if (host is not None): _return += Binary.str(host)

                port = Link.filter_well_known_port(scheme, request.get_server_port())
                if (port > 0): _return += ":{0:d}".format(port)

                if (_type & Link.TYPE_BASE_PATH == Link.TYPE_BASE_PATH
                    or _type & Link.TYPE_VIRTUAL_PATH == Link.TYPE_VIRTUAL_PATH
                   ): _return += self._get_url_path(request, False)
                else: _return += self._get_url_path(request)
            else: _return = self._get_url_path(request)
        #

        return _return
    #

    def _get_url_path(self, request = None, include_script_name = True):
        """
Returns the base URL path for the given URL or the current handled one.

:return: (str) Base URL path
:since:  v0.2.00
        """

        if (self.path is None):
            if (request is None): request = AbstractHttpRequest.get_instance()
            if (request is None): raise ValueException("Can't construct an URL from a request instance if it is not provided")

            script_name = request.get_script_name()

            if ((not include_script_name) or script_name == ""): path = "/"
            else:
                script_name = Binary.str(script_name)
                path = (script_name if (script_name[:1] == "/") else "/{0}".format(script_name))
            #
        else: path = Binary.str(self.path)

        return ("/" if (path == "") else path)
    #

    @staticmethod
    def _build_url_sorted_parameters(parameter_keys):
        """
Builds a sorted list for the parameter key list given.

:param parameter_keys: Parameter key list

:return: (list) Sorted parameter key list
:since:  v0.2.00
        """

        _return = [ ]

        if (isinstance(parameter_keys, Iterable)):
            _return = sorted(parameter_keys)

            if ("a" in _return):
                _return.remove("a")
                _return.insert(0, "a")
            #

            if ("s" in _return):
                _return.remove("s")
                _return.insert(0, "s")
            #

            if ("m" in _return):
                _return.remove("m")
                _return.insert(0, "m")
            #

            if ("lang" in _return):
                _return.remove("lang")
                _return.append("lang")
            #

            if ("uuid" in _return):
                _return.remove("uuid")
                _return.append("uuid")
            #
        #

        return _return
    #

    @staticmethod
    def filter_well_known_port(scheme, port):
        """
Filter well known ports defined for the given scheme.

:param scheme: Scheme
:param port: Port number

:return: (int) Port not equal to zero if not specified for the given scheme
:since:  v0.2.00
        """

        _return = 0

        if (port is not None):
            port = int(port)

            if ((scheme in ( "http", "ws" ) and port == 80)
                or (scheme in ( "https", "wss" ) and port == 443)
               ): _return = 0
            else: _return = port
        #

        return _return
    #

    @staticmethod
    def get_preferred(context = None):
        """
Returns a "Link" instance based on the defined preferred URL.

:param context: Context for the preferred link

:return: (object) Link instance
:since:  v0.2.00
        """

        if (not Settings.is_defined("pas_http_site_preferred_url_base")): Settings.read_file("{0}/settings/pas_http.json".format(Settings.get("path_data")))

        url = None

        if (context is not None): url = Settings.get("pas_http_site_preferred_url_base_{0}".format(re.sub("\\W+", "_", context)))
        if (url is None): url = Settings.get("pas_http_site_preferred_url_base")

        if (url is None): raise ValueException("Preferred URL base setting is not defined")
        url_elements = urlsplit(url)

        return Link(url_elements.scheme, url_elements.hostname, url_elements.port, url_elements.path)
    #

    @staticmethod
    def get_type_int(_type):
        """
Parses the given type parameter given as a string value.

:param _type: String type

:return: (int) Internal type
:since:  v0.2.00
        """

        _return = 0

        type_set = _type.split("+")

        for _type in type_set:
            if (_type == "elink"): _return |= Link.TYPE_ABSOLUTE_URL
            elif (_type == "ilink"): _return |= Link.TYPE_RELATIVE_URL
            elif (_type == "optical"): _return |= Link.TYPE_OPTICAL
            elif (_type == "plink"): _return |= Link.TYPE_PREDEFINED_URL
            elif (_type == "vlink"): _return |= Link.TYPE_VIRTUAL_PATH
        #

        return _return
    #

    @staticmethod
    def is_preferred_defined(context = None):
        """
Returns true if a defined preferred URL exists for the given context.

:param context: Context for the preferred link

:return: (bool) True if defined
:since:  v0.2.00
        """

        url = None

        if (context is not None): url = Settings.get("pas_http_site_preferred_url_base_{0}".format(re.sub("\\W+", "_", context)))
        if (url is None): url = Settings.get("pas_http_site_preferred_url_base")

        return (url is not None)
    #
#
