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

class PlaceholderMixin(object):
#
	"""
"PlaceholderMixin" provides methods to support placeholder texts.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(PlaceholderMixin)

:since: v0.1.01
		"""

		self.placeholder = None
		"""
Form field placeholder value
		"""
	#

	def get_placeholder(self):
	#
		"""
Returns the placeholder.

:return: (str) Placeholder content
:since:  v0.1.01
		"""

		return ("" if (self.placeholder is None) else self.placeholder)
	#

	def set_placeholder(self, placeholder):
	#
		"""
Sets the placeholder.

:param placeholder: Placeholder content

:since: v0.1.01
		"""

		self.placeholder = placeholder
	#
#

##j## EOF