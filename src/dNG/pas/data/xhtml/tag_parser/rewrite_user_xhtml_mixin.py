# -*- coding: utf-8 -*-
##j## BOF

"""
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
"""

# pylint: disable=invalid-name

from dNG.pas.data.binary import Binary
from dNG.pas.data.text.date_time import DateTime
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.text.tag_parser.rewrite_mixin import RewriteMixin
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

	def __init__(self):
	#
		"""
Constructor __init__(RewriteUserXhtmlMixin)

:since: v0.1.00
		"""

		RewriteMixin.__init__(self)

		L10n.init("pas_http_core")
	#

	def render_rewrite_user_xhtml_author_bar(self, source, key):
	#
		"""
Renders a XHTML based author user bar with avatar, user name and link.

:param source: Source for rewrite
:param key: Key in source for rewrite

:return: (str) Rendered XHTML content
:since:  v0.1.01
		"""

		return self._render_rewrite_user_xhtml_bar(source, key, "author")
	#

	def _render_rewrite_user_xhtml_bar(self, source, key, bar_type):
	#
		"""
Renders a XHTML based user bar with avatar, user name and link.

:param source: Source for rewrite
:param key: Key in source for rewrite
:param bar_type: User bar type

:return: (str) Rendered XHTML content
:since:  v0.1.01
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render_rewrite_user_xhtml_bar({1}, {2})- (#echo(__LINE__)#)", self, key, bar_type, context = "pas_tag_parser")

		user_profile_class = NamedLoader.get_class("dNG.pas.data.user.Profile")

		user_profile = None
		user_bar_data = (None if (user_profile_class == None) else self.get_source_value(source, key))

		if (user_bar_data != None):
		#
			try:
			#
				if ("id" in user_bar_data): user_profile = user_profile_class.load_id(user_bar_data['id'])
			#
			except NothingMatchedException: pass
		#

		content = ("{0}<strong>{1}</strong>{2}".format(L10n.get("pas_http_core_user_{0}_bar_1".format(bar_type)),
		                              DateTime.format_l10n(DateTime.TYPE_DATE_TIME_SHORT, int(user_bar_data['time_published'])),
		                              L10n.get("pas_http_core_user_{0}_bar_2".format(bar_type))
		                             )
		           if (user_bar_data != None and "time_published" in user_bar_data) else
		           L10n.get("pas_http_core_user_{0}_bar_0".format(bar_type))
		          )

		content = "<small>{0}</small><br />".format(content)

		if (user_profile != None):
		#
			user_profile_data = user_profile.get_data_attributes("name")
			content += "<strong>{0}</strong>".format(Formatting.escape(user_profile_data['name']))
		#
		else: content += "<b>{0}</b>".format(L10n.get("core_unknown_entity"))

		return "<div class='pagecontent_box pagecontent_user_bar pagecontent_user_{0}_bar'><div>{1}</div></div>".format(bar_type, content)
	#

	def render_rewrite_user_xhtml_link(self, source, key):
	#
		"""
Renders the user name and link to the profile.

:param source: Source for rewrite
:param key: Key in source for rewrite

:return: (str) Rendered XHTML content
:since:  v0.1.01
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render_rewrite_user_xhtml_link({1})- (#echo(__LINE__)#)", self, key, context = "pas_tag_parser")
		_return = L10n.get("core_unknown_entity")

		user_profile_class = NamedLoader.get_class("dNG.pas.data.user.Profile")

		user_profile = None
		user_value = (None if (user_profile_class == None) else self.get_source_value(source, key))

		if (user_value != None):
		#
			try:
			#
				if (type(user_value) == dict and "id" in user_value): user_profile = user_profile_class.load_id(user_value['id'])
				else:
				#
					user_value = Binary.str(user_value)
					if (type(user_value) == str): user_profile = user_profile_class.load_id(user_value)
				#
			#
			except NothingMatchedException: pass
		#

		if (user_profile != None):
		#
			user_profile_data = user_profile.get_data_attributes("name")
			_return = "<strong>{0}</strong>".format(Formatting.escape(user_profile_data['name']))
		#

		return _return
	#

	def render_rewrite_user_xhtml_publisher_bar(self, source, key):
	#
		"""
Renders a XHTML based publisher user bar with avatar, user name and link.

:param source: Source for rewrite
:param key: Key in source for rewrite

:return: (str) Rendered XHTML content
:since:  v0.1.01
		"""

		return self._render_rewrite_user_xhtml_bar(source, key, "publisher")
	#
#

##j## EOF