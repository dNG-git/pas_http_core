# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.xhtml.form.Processor
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

from dNG.pas.controller.abstract_request import AbstractRequest
from dNG.pas.data.text.form_processor import FormProcessor

class Processor(FormProcessor):
#
	"""
"Processor" provides form methods based on (X)HTML.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def get_data(self, flush = True):
	#
		"""
Returns all defined fields.

:param flush: Flush the cache

:return: (list) Field data
:since:  v0.1.00
		"""

		_return = FormProcessor.get_data(self, flush)

		for section in _return:
		#
			for field_data in section['fields']:
			#
				if (field_data['error'] != None): field_data['error'] = self._get_error_message(field_data['error'])
			#
		#

		return _return
	#

	def get_input(self, name):
	#
		"""
"get_input()" should be used to read the input value for the field from a
source (e.g. from a HTTP POST request parameter).

:param name: Field and parameter name

:return: (mixed) Value; None if not set
:since:  v0.1.00
		"""

		return (AbstractRequest.get_instance().get_parameter(name) if (self.form_has_input) else None)
	#

	def set_input_available(self):
	#
		"""
Sets the flag for available input. Input values can be read with
"get_input()".

:since: v0.1.00
		"""

		self.form_has_input = True
	#
#

##j## EOF