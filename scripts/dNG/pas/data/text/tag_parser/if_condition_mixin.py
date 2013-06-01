# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.tag_parser.if_condition_mixin
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

from dNG.pas.data.binary import direct_binary
from .source_value_mixin import direct_source_value_mixin

class direct_if_condition_mixin(direct_source_value_mixin):
#
	"""
This tag parser mixin provides support for if conditions.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def render_if_condition(self, source, key, operator, value, data):
	#
		"""
Checks and renders the content of the "if" condition.

:param data: Conditional data
:param source: Source for comparison
:param key: Key in source for comparison
:param operator: Comparison operator
:param value: Comparison value

:access: protected
:return: (str) Conditional data if successful
:since:  v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -tagParser.render_if_condition(source, {0}, {1}, {2}, data)- (#echo(__LINE__)#)".format(key, operator, value))
		var_return = ""

		is_valid = False
		source_value = self.source_get_value(source, key)

		source_value = ("" if (source_value == None) else direct_binary.str(source_value))
		if (type(source_value) != str): source_value = str(source_value)

		if (operator == "==" and source_value == value): is_valid = True
		if (operator == "!=" and source_value != value): is_valid = True

		if (is_valid): var_return = data
		return var_return
	#
#

##j## EOF