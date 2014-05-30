# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.xhtml.tag_parser.RewriteUserXhtmlMixin
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

# pylint: disable=invalid-name

from dNG.pas.data.text.tag_parser.rewrite_mixin import RewriteMixin
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.xhtml.formatting import Formatting
from dNG.pas.database.nothing_matched_exception import NothingMatchedException
from dNG.pas.module.named_loader import NamedLoader

class RewriteUserXhtmlMixin(RewriteMixin):
#
	"""
This tag parser mixin provides support for rewrite statements to generate
safe XHTML compliant output.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def render_rewrite_user_xhtml_link(self, source, key):
	#
		"""
Checks and renders the rewrite statement.

:param source: Source for rewrite
:param key: Key in source for rewrite

:return: (str) Rewritten statement if successful
:since:  v0.1.01
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render_rewrite_user_xhtml_link(source, {1})- (#echo(__LINE__)#)".format(self, key))
		_return = L10n.get("core_unknown_entity")

		user_profile_class = NamedLoader.get_class("dNG.pas.data.user.Profile")

		user_definition = (None if (user_profile_class == None) else self.get_source_value(source, key))
		user_profile = None

		if (user_definition != None and type(user_definition) == dict and "id" in user_definition):
		#
			try: user_profile = user_profile_class.load_id(user_definition['id'])
			except NothingMatchedException: pass
		#

		if (user_profile != None):
		#
			user_data = user_profile.get_data_attributes("name")
			_return = Formatting.escape(user_data['name'])
		#

		return _return
	#
#

##j## EOF