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

from dNG.pas.data.settings import Settings
from dNG.pas.data.text.input_filter import InputFilter

class FilterLinksMixin(object):
#
	"""
"FilterLinksMixin" removes links from a list if it should not be available
under given restrictions.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def _filter_links(self, links):
	#
		"""
Filters links based on required permissions.

:return: (list) Links available
:since:  v0.1.01
		"""

		_return = [ ]

		links_count = len(links)
		session = self.request.get_session()

		for position in range(0, links_count):
		#
			link = links[position]
			is_allowed = False

			if ("required_permission" in link):
			#
				permissions = (link['required_permission'] if (type(link['required_permission']) == list) else [ link['required_permission'] ])

				if (session != None): pass
			#
			elif ("required_permissions" in link and type(link['required_permissions']) == list):
			#
				permissions = link['required_permissions']

				if (session != None): pass
			#
			elif ("required_user_type" in link):
			#
				user_profile = (None if (session == None) else session.get_user_profile())
				user_types = (link['required_user_type'] if (type(link['required_user_type']) == list) else [ link['required_user_type'] ])

				if (user_profile == None): is_allowed = ("gt" in user_types)
				else:
				#
					for user_type in user_types:
					#
						if (user_profile.is_type(user_type)):
						#
							is_allowed = True
							break
						#
					#
				#
			#
			elif ("forbidden_user_type" in link):
			#
				user_profile = (None if (session == None) else session.get_user_profile())
				user_types = (link['forbidden_user_type'] if (type(link['forbidden_user_type']) == list) else [ link['forbidden_user_type'] ])

				if (user_profile == None): is_allowed = ("gt" not in user_types)
				else:
				#
					is_allowed = True

					for user_type in user_types:
					#
						if (user_profile.is_type(user_type)):
						#
							is_allowed = False
							break
						#
					#
				#
			#
			else: is_allowed = True

			if (is_allowed and "required_lang" in link): is_allowed = (self.request.get_lang() == link['required_lang'])

			if (is_allowed and "required_setting" in link):
			#
				setting = InputFilter.filter_control_chars(link['required_setting'])
				if (Settings.get(setting, False) == False): is_allowed = False
			#

			if (is_allowed): _return.append(link)
		#

		return _return
	#
#

##j## EOF