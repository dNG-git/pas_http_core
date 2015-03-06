# -*- coding: utf-8 -*-
##j## BOF

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

from dNG.pas.runtime.instance_lock import InstanceLock

class VirtualConfig(object):
#
	"""
Virtual paths are used to run service actions for URIs not calling the
controller directly.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
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
	#
		"""
Return the config for the given virtual path.

:param path: Virtual path to check

:return: (dict) Config if matched; None otherwise
:since:  v0.1.00
		"""

		_return = None

		if (len(path) > 0):
		#
			with VirtualConfig._lock:
			#
				path = path.lower()

				for virtual_path_config in VirtualConfig._virtuals:
				#
					if (path.startswith(virtual_path_config['path'])):
					#
						_return = virtual_path_config['config']
						break
					#
				#
			#
		#

		return _return
	#

	@staticmethod
	def isset_virtual_path(path):
	#
		"""
Returns true if the given virtual path is already defined.

:param path: Virtual path

:return: (bool) True if found
:since:  v0.1.00
		"""

		_return = False

		if (len(path) > 0):
		#
			with VirtualConfig._lock:
			#
				path = path.lower()

				for virtual_path_config in VirtualConfig._virtuals:
				#
					if (path.startswith(virtual_path_config['path'])):
					#
						_return = True
						break
					#
				#
			#
		#

		return _return
	#

	@staticmethod
	def set_virtual_path(path, config, setup_callback = None):
	#
		"""
Set the config for the given virtual path.

:param path: Virtual path
:param config: Config dict
:param setup_callback: Alternative request setup function

:since: v0.1.00
		"""

		if (setup_callback is not None): config['setup_callback'] = setup_callback
		path_normalized = path.lower()

		if ("_path_prefix" not in config): config['_path_prefix'] = path_normalized
		virtual_config = { "path": path_normalized, "config": config }

		with VirtualConfig._lock: VirtualConfig._virtuals.append(virtual_config)
	#

	@staticmethod
	def unset_virtual_path(path):
	#
		"""
Remove the config for the given virtual path.

:param path: Virtual path

:since: v0.1.00
		"""

		with VirtualConfig._lock:
		#
			index = 0

			for virtual_config in VirtualConfig._virtuals:
			#
				if (path == virtual_config['path']):
				#
					VirtualConfig._virtuals.pop(index)
					break
				#
				else: index += 1
			#
		#
	#
#

##j## EOF