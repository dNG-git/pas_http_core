# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.tag_parser.source_value_mixin
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

class direct_source_value_mixin(object):
#
	"""
This tag parser mixin provides support to find a key in a given source dict.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def source_get_value(self, source, key):
	#
		"""
Checks and renders the rewrite statement.

:param source: Source for rewrite
:param key: Key in source for rewrite

:access: protected
:return: (str) Rewritten statement if successful
:since:  v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -tagParser.source_get_value(source, {0})- (#echo(__LINE__)#)".format(key))
		var_return = None

		if (isinstance(source, dict)):
		#
			key_list = key.split(".", 1)

			if (key_list[0] in source):
			#
				if (len(key_list) > 1): var_return = self.source_get_value(source[key_list[0]], key_list[1])
				else: var_return = source[key]
			#
		#

		return var_return
	#
#

##j## EOF