# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.tag_parser.EachMixin
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

from .mapped_element_mixin import MappedElementMixin
from .source_value_mixin import SourceValueMixin

class EachMixin(MappedElementMixin, SourceValueMixin):
#
	"""
This tag parser mixin provides support for each loop statements.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def render_each(self, data, source_key, source, key, mapping_key):
	#
		"""
Checks and renders the each statement.

:param data: Element template data
:param source_key: Originating source key
:param source: Source for comparison
:param key: Key in source for comparison
:param mapping_key: Element mapping key

:return: (str) Rewritten statement if successful
:since:  v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -TagParser.render_each(data, {0}, source, {1}, {2})- (#echo(__LINE__)#)".format(source_key, key, mapping_key))
		_return = ""

		elements = self.source_get_value(source, key)

		if (isinstance(elements, list)):
		#
			for element in elements:
			#
				element_mapped_key = "{0}.{1}.{2}".format(source_key, key, mapping_key)
				self._mapped_element_set(element_mapped_key, element)

				try: _return += self._parser(data)
				except:
				#
					self._mapped_element_remove(element_mapped_key)
					raise
				#

				self._mapped_element_remove(element_mapped_key)
			#
		#

		return _return
	#
#

##j## EOF