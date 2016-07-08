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

from dNG.data.text.tag_parser.mapped_element_mixin import MappedElementMixin
from dNG.data.text.tag_parser.source_value_mixin import SourceValueMixin
from dNG.module.named_loader import NamedLoader
from dNG.runtime.exception_log_trap import ExceptionLogTrap

class BlockMixin(MappedElementMixin, SourceValueMixin):
#
	"""
This tag parser mixin provides support for blocks of subelements.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
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

:return: (str) Rewritten statement if successful
:since:  v0.2.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render_block()- (#echo(__LINE__)#)", self, context = "pas_tag_parser")
		_return = ""

		with ExceptionLogTrap("pas_tag_parser"):
		#
			content = (None if (source_key is None) else self.get_source_value(source, key))
			if (not isinstance(content, dict)): content = self.content

			action_definition = action.split(".")
			action = action_definition.pop()
			service = ".".join(action_definition)

			if (NamedLoader.is_defined("dNG.module.controller.{0}".format(service))):
			#
				instance = NamedLoader.get_instance("dNG.module.controller.{0}".format(service))
				instance.set_action(action, content)
				_return = instance.execute()
			#
		#

		return _return
	#
#

##j## EOF