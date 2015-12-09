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

import re

from dNG.pas.controller.predefined_http_request import PredefinedHttpRequest
from dNG.pas.data.http.translatable_exception import TranslatableException
from dNG.pas.data.text.input_filter import InputFilter
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.xhtml.link import Link
from dNG.pas.data.xhtml.notification_store import NotificationStore
from dNG.pas.data.xhtml.form.processor import Processor as FormProcessor
from dNG.pas.database.connection import Connection
from dNG.pas.module.controller.abstract_http import AbstractHttp as AbstractHttpController
from dNG.pas.runtime.not_implemented_exception import NotImplementedException
from dNG.pas.runtime.value_exception import ValueException

class AbstractMultiForm(AbstractHttpController):
#
	"""
The "AbstractMultiForm" class implements helper methods to implement a
wizard-like feature more easily.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.03
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(AbstractMultiForm)

:since: v0.1.03
		"""

		AbstractHttpController.__init__(self)

		self.multi_form_actions = [ ]
		"""
List of form page actions
		"""
	#

	def __getattr__(self, name):
	#
		"""
python.org: Called when an attribute lookup has not found the attribute in
the usual places (i.e. it is not an instance attribute nor is it found in the
class tree for self).

:param name: Attribute name

:return: (mixed) Instance attribute
:since:  v0.1.01
		"""

		_return = None

		form_action = self.action
		is_save_mode = False

		if (form_action[-5:] == "-save"):
		#
			form_action = form_action[:-5]
			is_save_mode = True
		#

		if (form_action == "init"): _return = self._execute_init
		elif (form_action == "save"): _return = self._execute_save
		elif (self._is_multi_form_action_defined(form_action)):
		#
			_return = (self._execute_form_save if (is_save_mode) else self._execute_form)
		#

		if (_return is None): self._raise_executable_not_found()
		return _return
	#

	def _check_multi_form(self):
	#
		"""
Returns true if all fields of the wizard-like context report to be valid.

:return: (bool) True if valid
:since:  v0.1.03
		"""

		form_id = self._get_multi_form_id()
		form = FormProcessor(form_id)

		form.set_input_data(self._get_multi_form_input_values(form))

		for action_definition in self.multi_form_actions:
		#
			method = getattr(self, "apply_multi_form_action_{0}".format(action_definition['id']))
			method(form)
		#

		return form.check()
	#

	def _execute_init(self, source = None, target = None):
	#
		"""
Executes the initialization of a form.

:since: v0.1.03
		"""

		if (len(self.multi_form_actions) < 1): raise TranslatableException("core_unknown_error")
		form_action = self.multi_form_actions[0]['id']

		redirect_request = PredefinedHttpRequest()
		redirect_request.set_module(self.request.get_module())
		redirect_request.set_service(self.request.get_service())
		redirect_request.set_action(form_action)
		redirect_request.set_dsd_dict(self.request.get_dsd_dict())

		if (source is not None): redirect_request.set_dsd("source", source)

		if (target is not None): redirect_request.set_dsd("target", target)
		elif (not self.request.is_dsd_set("target")): redirect_request.set_dsd("target", redirect_request.get_dsd("source"))

		self.request.redirect(redirect_request)
	#

	def _execute_form(self, is_save_mode = False):
	#
		"""
Action to show and handle a form action.

:since: v0.1.03
		"""

		form_action = self._get_multi_form_action()
		form_action_position = self._get_multi_form_action_position(form_action)
		form_id = self._get_multi_form_id()

		if (self.response.is_supported("html_css_files")): self.response.add_theme_css_file("mini_default_sprite.min.css")

		if (form_action_position > 0):
		#
			last_form_action = self.multi_form_actions[form_action_position - 1]['id']
			back_link_params = { "__request__": True, "a": last_form_action, "form_id": form_id }
		#
		else:
		#
			source = InputFilter.filter_control_chars(self.request.get_dsd("source", "")).strip()
			back_link_params = { "__query__": re.sub("\\_\\_\\w+\\_\\_", "", source) }
		#

		Link.set_store("servicemenu",
		               Link.TYPE_RELATIVE_URL,
		               L10n.get("core_back"),
		               back_link_params,
		               icon = "mini-default-back",
		               priority = 7
		              )

		form = FormProcessor(form_id)

		if (is_save_mode): form.set_input_available()
		elif (form.get_form_id() == form_id): form.set_input_data(self._get_multi_form_input_values(form))

		method = getattr(self, "apply_multi_form_action_{0}".format(form_action))
		method(form)

		if (is_save_mode and form.check()):
		#
			self._set_multi_form_input_values(form)

			NotificationStore.get_instance().add_completed_info(L10n.get("pas_http_core_form_done_data_saved_temporarily"))

			Link.clear_store("servicemenu")

			next_form_action = ("save"
			                    if (len(self.multi_form_actions) <= form_action_position) else
			                    self.multi_form_actions[1 + form_action_position]['id']
			                   )

			redirect_request = PredefinedHttpRequest()
			redirect_request.set_module(self.request.get_module())
			redirect_request.set_service(self.request.get_service())
			redirect_request.set_action(next_form_action)

			redirect_request.set_parameter_chained("form_id", form_id)
			redirect_request.set_dsd_dict(self.request.get_dsd_dict())

			self.request.redirect(redirect_request)
		#
		else:
		#
			content = { "title": self.multi_form_actions[form_action_position]['title'] }

			button_title = ("pas_core_save"
			                if (len(self.multi_form_actions) <= form_action_position) else
			                "core_continue"
			               )

			content['form'] = { "object": form,
			                    "post_encoding": "multipart/form-data",
			                    "url_parameters": { "__request__": True,
			                                        "a": "{0}-save".format(form_action)
			                                      },
			                    "button_title": button_title
			                  }

			self.response.init()
			self.response.set_title(content['title'])
			self.response.add_oset_content("core.form", content)
		#
	#

	def _execute_form_save(self):
	#
		"""
Action called to save the form data.

:since: v0.1.03
		"""

		self._execute_form(self.request.get_type() == "POST")
	#

	def _execute_save(self):
	#
		"""
Saves all data of the form.

:since: v0.1.03
		"""

		raise NotImplementedException()
	#

	def _get_multi_form_action(self):
	#
		"""
Returns the current form action used in a wizard-like context.

:return: (str) Form action
:since:  v0.1.03
		"""

		form_action = (self.action[:-5]
		               if (self.action[-5:] == "-save") else
		               self.action
		              )

		return re.sub("\\W", "_", form_action)
	#

	def _get_multi_form_action_position(self, form_action):
	#
		"""
Returns the position of the given form action in a wizard-like context.

:return: (int) Position of the form action
:since:  v0.1.03
		"""

		position = 0
		_return = -1

		for action_definition in self.multi_form_actions:
		#
			if (action_definition['id'] == form_action):
			#
				_return = position
				break
			#

			position += 1
		#

		if (_return < 0): raise ValueException("Form action given is invalid")
		return _return
	#

	def _get_multi_form_id(self):
	#
		"""
Returns the form ID used in a wizard-like context.

:since: v0.1.03
		"""

		return (self.request.get_parameter_chained("form_id")
		        if (self.request.is_supported("parameters_chained")) else
		        InputFilter.filter_control_chars(self.request.get_parameter("form_id"))
		       )
	#

	@Connection.wrap_callable
	def _get_multi_form_input_values(self, form):
	#
		"""
Returns temporarily saved form input data.

:return: (dict) Form input data
:since:  v0.1.03
		"""

		form_data = form.get_form_store().get_value_dict()
		return form_data.get("multi_form_data", { })
	#

	def _is_multi_form_action_defined(self, form_action):
	#
		"""
Returns true if the given form action is defined for the wizard-like
context.

:return: (bool) True if defined
:since:  v0.1.03
		"""

		_return = True

		try: self._get_multi_form_action_position(form_action)
		except ValueException: _return = False

		return _return
	#

	@Connection.wrap_callable
	def _set_multi_form_input_values(self, form):
	#
		"""
Sets and saves the given form input data temporarily.

:since: v0.1.03
		"""

		form_store = form.get_form_store()

		form_data = form_store.get_value_dict()
		if ("multi_form_data" not in form_data): form_data['multi_form_data'] = { }

		field_list = form.get_field_list()

		for field in field_list:
		#
			value = InputFilter.filter_control_chars(form.get_value(field['name']))
			form_data['multi_form_data'][field['name']] = value
		#

		form_store.set_value_dict(form_data)
		form_store.save()
	#
#

##j## EOF