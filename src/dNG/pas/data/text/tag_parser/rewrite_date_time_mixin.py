# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.text.tag_parser.RewriteDateTimeMixin
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

from dNG.pas.data.text.date_time import DateTime
from dNG.pas.data.text.l10n import L10n
from .rewrite_mixin import RewriteMixin

class RewriteDateTimeMixin(RewriteMixin):
#
	"""
This tag parser mixin provides support for rewrite statements to generate
formatted date and time strings.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas;http
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def render_rewrite_date_time(self, source, key, _type):
	#
		"""
Checks and renders the rewrite statement.

:param source: Source for rewrite
:param key: Key in source for rewrite

:return: (str) Rewritten statement if successful
:since:  v0.1.01
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render_rewrite_date_time(source, {1}, {2})- (#echo(__LINE__)#)".format(self, key, _type))
		_return = L10n.get("core_unknown")

		timestamp = self.source_get_value(source, key)

		if (timestamp != None):
		#
			# TODO: Timezone from session
			_return = DateTime.format_l10n(_type, int(timestamp))
		#

		return _return
	#
#

##j## EOF