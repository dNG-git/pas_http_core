# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.tag_parser.BlockMixin
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

from dNG.pas.module.named_loader import NamedLoader
from .mapped_element_mixin import MappedElementMixin
from .source_value_mixin import SourceValueMixin

class BlockMixin(MappedElementMixin, SourceValueMixin):
#
	"""
This tag parser mixin provides support for blocks of subelements.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def render_block(self, action, source_key = None, source = None, key = None):
	#
		"""
Checks and renders the block statement.

:param data: Element template data
:param source_key: Originating source key
:param source: Source for comparison
:param key: Key in source for comparison

:access: protected
:return: (str) Rewritten statement if successful
:since:  v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -TagParser.render_block(data, source_key, source, key)- (#echo(__LINE__)#)")
		var_return = ""

		try:
		#
			content = (self.content if (source_key == None) else self.source_get_value(source, key))

			action_definition = action.split(".")
			action = action_definition.pop()
			service = ".".join(action_definition)

			if (NamedLoader.is_defined("dNG.pas.module.blocks.{0}".format(service))):
			#
				instance = NamedLoader.get_instance("dNG.pas.module.blocks.{0}".format(service))
				if (self.log_handler != None): instance.set_log_handler(self.log_handler)
				instance.set_action(action, content)
				var_return = instance.execute()
			#
		#
		except Exception as handled_exception:
		#
			if (self.log_handler != None): self.log_handler.error(handled_exception)
		#

		return var_return
	#
#

##j## EOF