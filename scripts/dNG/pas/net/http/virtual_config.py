# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.net.http.tornado_handler
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;http;core

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasHttpCoreVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from threading import RLock

class direct_virtual_config(object):
#
	"""
Virtual paths are used to run service actions for URIs not calling the
controller directly.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	synchronized = RLock()
	"""
Lock used in multi thread environments.
	"""
	virtuals = [ ]
	"""
List with registered virtual paths
	"""

	@staticmethod
	def get_config(pathname):
	#
		"""
Return the config for the given virtual path.

:param pathname: Virtual path to check

:return: (dict) Config if matched; None otherwise
:since:  v0.1.00
		"""

		var_return = None

		if (len(pathname) > 0):
		#
			with direct_virtual_config.synchronized:
			#
				pathname = pathname.lower()

				for virtual_path_config in direct_virtual_config.virtuals:
				#
					if (pathname.startswith(virtual_path_config['path'])):
					#
						var_return = virtual_path_config['config']
						break
					#
				#
			#
		#

		return var_return
	#

	@staticmethod
	def set_virtual_path(path, config, py_setup_function = None):
	#
		"""
Set the config for the given virtual path.

:param path: Virtual path
:param config: Config dict
:param py_function: Alternative request setup function

:since: v0.1.00
		"""

		if (py_setup_function != None): config['setup_function'] = py_setup_function
		virtual_config = { "path": path.lower(), "config": config }

		direct_virtual_config.virtuals.append(virtual_config)
	#

	@staticmethod
	def unset_virtual_path(path):
	#
		"""
Remove the config for the given virtual path.

:param path: Virtual path

:since: v0.1.00
		"""

		with direct_virtual_config.synchronized:
		#
			index = 0

			for virtual_config in direct_virtual_config.virtuals:
			#
				if (path == virtual_config['path']):
				#
					direct_virtual_config.virtuals.pop(index)
					break
				#
				else: index += 1
			#
		#
	#
#

##j## EOF