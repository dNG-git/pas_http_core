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
setup.py
"""

from os import makedirs, path

try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup
#

try:
    from dNG.distutils.command.build_py import BuildPy
    from dNG.distutils.command.install_data import InstallData
    from dNG.distutils.command.install_copied_and_extended_data import InstallCopiedAndExtendedData
    from dNG.distutils.command.sdist import Sdist
    from dNG.distutils.temporary_directory import TemporaryDirectory
except ImportError:
    raise RuntimeError("'dng-builder-suite' prerequisite not matched")
#

def get_versions():
    """
Returns the version currently in development.

:return: (tuple) Tuple of version string and internal version value
:since:  v0.1.3
    """

    return ( "v1.0.0", "1.0000" )
#

with TemporaryDirectory(dir = ".") as build_directory:
    css_js_copyright = "// Distributed with pas.http.core #echo(pasHttpCoreVersion)#"
    versions = get_versions()

    parameters = { "copy_builder_extensions": "css,js",
                   "copy_builder_header_by_extension": { "css": css_js_copyright,
                                                         "js": css_js_copyright
                                                       },
                   "install_data_plain_copy_extensions": "crt,jpg,json,map,png,swf,tsc,wsgi,xml",
                   "pasHttpCoreVersion": versions[0],
                   "pasHttpCoreIVersion": versions[1]
                 }

    BuildPy.set_build_target_path(build_directory)
    BuildPy.set_build_target_parameters(parameters)

    InstallData.add_install_data_callback(InstallData.plain_copy, [ "data", "lang" ])
    InstallData.add_install_data_callback(InstallCopiedAndExtendedData.callback, [ "data", "lang" ])
    InstallData.set_build_target_path(build_directory)
    InstallData.set_build_target_parameters(parameters)

    Sdist.set_build_target_path(build_directory)
    Sdist.set_build_target_parameters(parameters)

    makedirs(path.join(build_directory, "src", "dNG"))

    InstallData.add_install_data_callback(InstallData.plain_copy, [ "data", "lang" ])
    InstallData.add_install_data_callback(InstallCssData.callback, [ "data" ])
    InstallData.add_install_data_callback(InstallJsData.callback, [ "data" ])

    _build_path = path.join(build_directory, "src")

    _setup = { "name": "pas_http_core-core",
               "version": versions[0][1:],
               "description": "Python Application Services",
               "long_description": """"pas_http_core" provides the core infrastructure to handle HTTP requests.""",
               "author": "direct Netware Group et al.",
               "author_email": "web@direct-netware.de",
               "license": "MPL2",
               "url": "https://www.direct-netware.de/redirect?pas;http;core",

               "platforms": [ "any" ],

               "packages": [ "dNG" ],

               "data_files": [ ( "docs", [ "LICENSE", "README" ]) ]
             }

    # Override build_py to first run builder.py
    _setup['cmdclass'] = { "build_py": BuildPy, "install_data": InstallData, "sdist": Sdist }

    setup(**_setup)
#
