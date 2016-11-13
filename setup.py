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

def get_versions():
    """
Returns the version currently in development.

:return: (tuple) Tuple of version string and internal version value
:since:  v0.1.03
    """

    return ( "v0.2.00", "0.00200" )
#

from dNG.distutils.command.build_py import BuildPy
from dNG.distutils.command.install_data import InstallData
from dNG.distutils.command.install_css_data import InstallCssData
from dNG.distutils.command.install_js_data import InstallJsData
from dNG.distutils.temporary_directory import TemporaryDirectory

from distutils.core import setup
from os import path

with TemporaryDirectory(dir = ".") as build_directory:
    css_js_copyright = "pas.http.core #echo(pasHttpCoreVersion)# - (C) direct Netware Group - All rights reserved"
    versions = get_versions()

    parameters = { "install_data_plain_copy_extensions": "crt,jpg,json,map,png,swf,tsc,wsgi,xml",
                   "pasHttpCoreVersion": versions[0], "pasHttpCoreIVersion": versions[1],
                   "css_header": css_js_copyright, "css_min_filenames": True,
                   "js_header": css_js_copyright, "js_min_filenames": True
                 }

    InstallData.add_install_data_callback(InstallData.plain_copy, [ "data", "lang" ])
    InstallData.add_install_data_callback(InstallCssData.callback, [ "data" ])
    InstallData.add_install_data_callback(InstallJsData.callback, [ "data" ])
    InstallData.set_build_target_path(build_directory)
    InstallData.set_build_target_parameters(parameters)

    _build_path = path.join(build_directory, "src")

    setup(name = "pas_http_core",
          version = versions[0],
          description = "Python Application Services",
          long_description = """"pas_http_core" provides the core infrastructure to handle HTTP requests.""",
          author = "direct Netware Group et al.",
          author_email = "web@direct-netware.de",
          license = "MPL2",
          url = "https://www.direct-netware.de/redirect?pas;http;core",

          platforms = [ "any" ],

          package_dir = { "": _build_path },
          packages = [ "dNG" ],

          data_files = [ ( "docs", [ "LICENSE", "README" ]) ],

          # Override build_py to first run builder.py over all PAS modules
          cmdclass = { "build_py": BuildPy,
                       "install_data": InstallData
                     }
         )
#
