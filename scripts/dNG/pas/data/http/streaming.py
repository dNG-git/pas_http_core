# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.http.streaming
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

from os import path
import re

from dNG.pas.controller.abstract_http_response import direct_abstract_http_response
from dNG.pas.data.mimetype import direct_mimetype
from dNG.pas.data.translatable_exception import direct_translatable_exception
from dNG.pas.data.streamer.abstract import direct_abstract as direct_abstract_streamer

class direct_streaming(object):
#
	"""
HTTP streaming returns data on demand for output.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.01
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	@staticmethod
	def run(request, streamer, url, response):
	#
		"""
Parses, configures and activates the given streamer if all prerequisites
are met.

:since: v0.1.01
		"""

		if (not isinstance(streamer, direct_abstract_streamer)): raise direct_translatable_exception("pas_http_error_400")
		if (not isinstance(response, direct_abstract_http_response)): raise direct_translatable_exception("pas_http_error_500")

		if (streamer == None): response.set_header("HTTP/1.1", "HTTP/1.1 501 Not Implemented", True)
		else:
		#
			mimetypes = direct_mimetype.get_instance()

			url_ext = path.splitext(url)[1]
			mimetype_definition = mimetypes.get(url_ext[1:])

			mimetypes.return_instance()

			if (mimetype_definition != None and streamer.open_url(url)):
			#
				response.set_header("Content-Type", mimetype_definition['mimetype'])

				is_content_length_set = False
				is_valid = False

				if (request.get_header('range') != None):
				#
					streamer_size = streamer.get_size()
					range_start = 0
					range_end = 0
					re_result = re.match("^bytes(.*?)=(.*?)-(.*?)$", request.get_header('range'), re.I)

					if (re_result != None):
					#
						range_start = re.sub("(\D+)", "", re_result.group(2))
						range_end = re.sub("(\D+)", "", re_result.group(3))

						if (range_start != ""):
						#
							range_start = int(range_start)

							if (range_end != ""):
							#
								range_end = int(range_end)
								if (range_start >= 0 and range_start <= range_end and range_end < streamer_size): is_valid = True
							#
							elif (range_start >= 0 and range_start < streamer_size):
							#
								is_valid = True
								range_end = streamer_size - 1
							#
						#
						elif (range_end != ""):
						#
							range_start = 0
							range_end = int(range_end)
							if (range_end > 0 and range_end < streamer_size): is_valid = True
						#

						if (is_valid and range_start > 0): is_valid = streamer.supports_seeking()

						if (is_valid and (range_start > 0 or (1 + range_end) < streamer_size)):
						#
							response.set_header("HTTP/1.1", "HTTP/1.1 206 Partial Content", True)
							response.set_header("Content-Range", "{0:d}-{1:d}/{2:d}".format(range_start, range_end, streamer_size))

							response.set_header("Content-Length", (1 + range_end - range_start))

							is_content_length_set = True
							is_valid = streamer.set_range(range_start, range_end)
						#
					#
				#

				if (not is_content_length_set): response.set_header("Content-Length", streamer.get_size())
				response.set_streamer(streamer)
			#
			else: response.set_header("HTTP/1.1", "HTTP/1.1 404 Not Found", True)
		#
	#
#

##j## EOF