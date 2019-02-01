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

import re

from dNG.data.binary import Binary
from dNG.data.text.input_filter import InputFilter
from dNG.data.text.uri import Uri
from dNG.runtime.instance_lock import InstanceLock

class VirtualRoute(object):
    """
Virtual paths are used to run service actions for URIs not calling the
controller directly.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    RE_DSD_PLUS_SPAM_CHAR = re.compile("(\\+){3,}")
    """
RegExp to find more than 3 plus characters in a row
    """
    RE_PLUS_ENCODED_CHAR = re.compile("%2b", re.I)
    """
RegExp to find URL-encoded plus characters
    """

    _lock = InstanceLock()
    """
Thread safety lock
    """
    _virtuals = [ ]
    """
List with registered virtual paths
    """

    @staticmethod
    def get_config(path):
        """
Return the config for the given virtual path.

:param path: Virtual path to check

:return: (dict) Config if matched; None otherwise
:since:  v1.0.0
        """

        _return = None

        path = Binary.str(path)

        if (len(path) > 0):
            with VirtualRoute._lock:
                is_fully_qualified_name = (path[-1:] == "$")

                if (is_fully_qualified_name): path = path[:-1]
                path = path.lower()

                for virtual_path_config in VirtualRoute._virtuals:
                    if (is_fully_qualified_name):
                        if (path == virtual_path_config['path']):
                            _return = virtual_path_config['config']
                            break
                        #
                    elif (path.startswith(virtual_path_config['path'])):
                        _return = virtual_path_config['config']
                        break
                    #
                #
            #
        #

        return _return
    #

    @staticmethod
    def is_defined(path):
        """
Returns true if the given virtual path is already defined.

:param path: Virtual path

:return: (bool) True if found
:since:  v1.0.0
        """

        return (VirtualRoute.get_config(path) is not None)
    #

    @staticmethod
    def parse_dsd(dsd):
        """
DSD stands for dynamic service data and should be used for transfering IDs for
news, topics, ... Take care for injection attacks!

:param dsd: DSD string for parsing

:return: (dict) Parsed DSD
:since:  v1.0.0
        """

        dsd = InputFilter.filter_control_chars(dsd)

        if ("+" not in dsd and VirtualRoute.RE_PLUS_ENCODED_CHAR.search(dsd) is not None): dsd = Uri.decode_query_value(dsd)
        elif (" " in dsd): dsd = Uri.encode_query_value(dsd)

        dsd = VirtualRoute.RE_DSD_PLUS_SPAM_CHAR.sub("++", dsd)

        dsd_list = dsd.split("++")
        _return = { }

        for dsd in dsd_list:
            dsd_element = dsd.strip().split("+", 1)

            if (len(dsd_element) > 1):
                _return[dsd_element[0]] = InputFilter.filter_control_chars(Uri.decode_query_value(dsd_element[1]))
            elif (len(dsd_element[0]) > 0): _return[dsd_element[0]] = ""
        #

        return _return
    #

    @staticmethod
    def set(path, config, setup_callback = None):
        """
Set the config for the given virtual path.

:param path: Virtual path
:param config: Config dict
:param setup_callback: Alternative request setup function

:since: v1.0.0
        """

        if (setup_callback is not None): config['setup_callback'] = setup_callback
        path_normalized = path.lower()

        if ("_path_prefix" not in config): config['_path_prefix'] = path_normalized
        virtual_config = { "path": path_normalized, "config": config }

        with VirtualRoute._lock: VirtualRoute._virtuals.append(virtual_config)
    #

    @staticmethod
    def unset(path):
        """
Remove the config for the given virtual path.

:param path: Virtual path

:since: v1.0.0
        """

        with VirtualRoute._lock:
            index = 0

            for virtual_config in VirtualRoute._virtuals:
                if (path == virtual_config['path']):
                    VirtualRoute._virtuals.pop(index)
                    break
                else: index += 1
            #
        #
    #
#
