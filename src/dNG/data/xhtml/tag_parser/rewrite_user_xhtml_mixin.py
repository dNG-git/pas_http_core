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

# pylint: disable=invalid-name

from dNG.data.binary import Binary
from dNG.data.text.date_time import DateTime
from dNG.data.text.l10n import L10n
from dNG.data.text.tag_parser.rewrite_mixin import RewriteMixin
from dNG.data.xhtml.form_tags_renderer import FormTagsRenderer
from dNG.data.xhtml.link import Link
from dNG.data.xml_parser import XmlParser
from dNG.module.named_loader import NamedLoader

try: from dNG.database.nothing_matched_exception import NothingMatchedException
except ImportError: from dNG.runtime.value_exception import ValueException as NothingMatchedException

class RewriteUserXhtmlMixin(RewriteMixin):
#
	"""
This tag parser mixin provides support for rewrite statements to generate
safe XHTML compliant output.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(RewriteUserXhtmlMixin)

:since: v0.2.00
		"""

		RewriteMixin.__init__(self)

		L10n.init("pas_http_core")
	#

	def _get_user_profile(self, user_value):
	#
		"""
Returns the user profile instance for the given user ID.

:param user_value: User value from TagParser

:return: (object) User profile instance; None if not found
:since:  v0.2.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}._get_user_profile()- (#echo(__LINE__)#)", self, context = "pas_tag_parser")
		_return = None

		user_profile_class = NamedLoader.get_class("dNG.data.user.Profile")

		if (user_profile_class is not None and user_value is not None):
		#
			try:
			#
				if (type(user_value) is dict and "id" in user_value): _return = user_profile_class.load_id(user_value['id'])
				else:
				#
					user_value = Binary.str(user_value)
					if (type(user_value) is str): _return = user_profile_class.load_id(user_value)
				#
			#
			except NothingMatchedException: pass
		#

		return _return
	#

	def render_rewrite_user_xhtml_author_bar(self, source, key):
	#
		"""
Renders a XHTML based author user bar with avatar, user name and link.

:param source: Source for rewrite
:param key: Key in source for rewrite

:return: (str) Rendered XHTML content
:since:  v0.2.00
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
:since:  v0.2.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render_rewrite_user_xhtml_bar({1}, {2})- (#echo(__LINE__)#)", self, key, bar_type, context = "pas_tag_parser")

		user_bar_data = self.get_source_value(source, key)
		user_profile = self._get_user_profile(user_bar_data)

		content = ("{0}<strong>{1}</strong>{2}".format(L10n.get("pas_http_core_user_{0}_bar_1".format(bar_type)),
		                              DateTime.format_l10n(DateTime.TYPE_DATE_TIME_SHORT, int(user_bar_data['time_published'])),
		                              L10n.get("pas_http_core_user_{0}_bar_2".format(bar_type))
		                             )
		           if (user_bar_data is not None and "time_published" in user_bar_data) else
		           L10n.get("pas_http_core_user_{0}_bar_0".format(bar_type))
		          )

		content = "<small>{0}</small><br />".format(content)

		if (user_profile is None): content += "<b>{0}</b>".format(L10n.get("core_unknown_entity"))
		else:
		#
			user_profile_data = user_profile.get_data_attributes("id", "name")

			source_iline = Link().build_url(Link.TYPE_QUERY_STRING, { "__request__": True })

			user_link = Link().build_url(Link.TYPE_RELATIVE_URL,
			                             { "m": "user",
			                               "s": "profile",
			                               "dsd": { "upid": user_profile_data['id'],
			                                        "source": source_iline
			                                      }
			                             }
			                            )

			user = XmlParser().dict_to_xml_item_encoder({ "tag": "a",
		                                                  "attributes": { "href": user_link },
		                                                  "value": user_profile_data['name']
		                                                },
		                                                strict_standard_mode = False
		                                               )

			content += "<strong>{0}</strong>".format(user)
		#

		return "<div class='pagecontent_box pagecontent_user_bar pagecontent_user_{0}_bar'><div>{1}</div></div>".format(bar_type, content)
	#

	def render_rewrite_user_xhtml_link(self, source, key):
	#
		"""
Renders the user name and link to the profile.

:param source: Source for rewrite
:param key: Key in source for rewrite

:return: (str) Rendered XHTML content
:since:  v0.2.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render_rewrite_user_xhtml_link({1})- (#echo(__LINE__)#)", self, key, context = "pas_tag_parser")
		_return = L10n.get("core_unknown_entity")

		user_profile = self._get_user_profile(self.get_source_value(source, key))

		if (user_profile is not None):
		#
			user_profile_data = user_profile.get_data_attributes("id", "name")

			source_iline = Link().build_url(Link.TYPE_QUERY_STRING, { "__request__": True })

			user_link = Link().build_url(Link.TYPE_RELATIVE_URL,
			                             { "m": "user",
			                               "s": "profile",
			                               "dsd": { "upid": user_profile_data['id'],
			                                        "source": source_iline
			                                      }
			                             }
			                            )

			user = XmlParser().dict_to_xml_item_encoder({ "tag": "a",
		                                                  "attributes": { "href": user_link },
		                                                  "value": user_profile_data['name']
		                                                },
		                                                strict_standard_mode = False
		                                               )

			_return = "<strong>{0}</strong>".format(user)
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
:since:  v0.2.00
		"""

		return self._render_rewrite_user_xhtml_bar(source, key, "publisher")
	#

	def render_rewrite_user_xhtml_signature_box(self, source, key):
	#
		"""
Renders a XHTML based publisher user bar with avatar, user name and link.

:param source: Source for rewrite
:param key: Key in source for rewrite

:return: (str) Rendered XHTML content
:since:  v0.2.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render_rewrite_user_xhtml_signature_box({1})- (#echo(__LINE__)#)", self, key, context = "pas_tag_parser")
		_return = ""

		signature = ""
		user_profile = self._get_user_profile(self.get_source_value(source, key))

		if (user_profile is not None):
		#
			user_profile_data = user_profile.get_data_attributes("signature")
			if (user_profile_data['signature'] is not None): signature = user_profile_data['signature'].strip()
		#

		if (len(signature) > 0):
		#
			renderer = FormTagsRenderer()
			renderer.set_blocks_supported(False)
			renderer.set_xhtml_title_top_level(2)

			_return = "<div class='pagecontent_box pagecontent_user_signature_box'>{0}</div>".format(renderer.render(signature))
		#

		return _return
	#
#

##j## EOF