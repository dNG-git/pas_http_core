# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.http.TranslatableError
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;http;core

The following license agreement remains valid unless any additions or
changes are being made by direct Netware Group in a written form.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc.,
59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;gpl
----------------------------------------------------------------------------
#echo(pasHttpCoreVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from dNG.pas.data.translatable_exception import TranslatableException

class TranslatableError(TranslatableException):
#
	"""
This exception is used for non-critical, translatable error messages.
Non-critical errors are usually expected like wrong entity IDs.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;gpl
             GNU General Public License 2
	"""

	def __init__(self, l10n_id, http_code = 200, value = None, _exception = None):
	#
		"""
Constructor __init__(TranslatableError)

:param l10n_id: L10n translatable key (prefixed with "errors_")
:param http_code: HTTP code
:param value: Exception message value
:param _exception: Inner exception

:since: v0.1.01
		"""

		TranslatableException.__init__(self, l10n_id, value, _exception)

		self.http_code = http_code
		"""
HTTP error code
		"""
	#

	def get_http_code(self):
	#
		"""
Return the HTTP error code.

:return: (int) HTTP error code
:since:  v0.1.01
		"""

		return self.http_code
	#
#

##j## EOF