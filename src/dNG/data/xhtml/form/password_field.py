# -*- coding: utf-8 -*-

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

from dNG.data.text.md5 import Md5
from dNG.data.xhtml.formatting import Formatting

from .placeholder_mixin import PlaceholderMixin
from .text_field import TextField

class PasswordField(TextField, PlaceholderMixin):
    """
"PasswordField" provides  password fields (including optional a repetition
check).

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    PASSWORD_CLEARTEXT = 1
    """
Only recommended for separate encryption operations
    """
    PASSWORD_MD5 = 1 << 1
    """
MD5 encoded password
    """
    PASSWORD_WITH_REPETITION = 1 << 2
    """
Password input repetition
    """

    def __init__(self, name = None):
        """
Constructor __init__(AbstractField)

:param name: Form field name

:since: v0.2.00
        """

        TextField.__init__(self, name)
        PlaceholderMixin.__init__(self)

        self.mode = PasswordField.PASSWORD_MD5
        """
Password field mode
        """
        self.raw_value = None
        """
Encrypted field value
        """
        self.repetition_value = None
        """
Encrypted repetition field value
        """
    #

    def _check(self):
        """
Executes checks if the field value is valid.

:return: (bool) True if all checks are passed
:since:  v0.2.00
        """

        _return = TextField._check(self)
        if (_return): _return = self._check_password_requirements()

        return _return
    #

    def _check_length(self):
        """
Checks the length of value.

:return: (bool) True if all checks are passed
:since:  v0.2.00
        """

        return self._check_string_length(self.raw_value)
    #

    def _check_password_requirements(self):
        """
Checks if the field value fulfills the requirements.

:param force: True to force revalidation

:return: (bool) True if all checks are passed
:since:  v0.2.00
        """

        error_data = None

        if (self.mode & PasswordField.PASSWORD_WITH_REPETITION == PasswordField.PASSWORD_WITH_REPETITION
            and self.value != self.repetition_value
           ): error_data = "password_repetition"

        if (error_data is not None): self.error_data = error_data
        return (error_data is None)
    #

    def _encrypt_value(self, value):
        """
Encrypts the given form field value based on the defined mode.

:param value: Original value

:return: (str) Encrypted value
        """

        return (value if (value is None) else Md5.hash(value))
    #

    def get_type(self):
        """
Returns the field type.

:return: (str) Field type
:since:  v0.2.00
        """

        return ("password_with_repetition"
                if (self.mode & PasswordField.PASSWORD_WITH_REPETITION == PasswordField.PASSWORD_WITH_REPETITION) else
                "password"
               )
    #

    def get_value(self, _raw_input = False):
        """
Returns the field value given or transmitted.

:param raw_input: True to return the raw (transmitted) value.

:return: (mixed) Field value; None on error
:since:  v0.2.00
        """

        return (self.raw_value if (_raw_input) else self.value)
    #

    def load_definition(self, field_definition):
        """
Loads the field configuration from the given definition.

:param field_definition: Field definition dict

:since: v0.2.00
        """

        TextField.load_definition(self, field_definition)

        mode = field_definition.get("mode")
        if (mode is not None): self.set_mode(self.__class__.get_mode_int(mode))
    #

    def render(self):
        """
Renders the given field.

:return: (str) Valid XHTML form field definition
:since:  v0.2.00
        """

        context = { "type": Formatting.escape(self.get_type()),
                    "id": "pas_{0}".format(Formatting.escape(self.get_id())),
                    "name": Formatting.escape(self.name),
                    "title": Formatting.escape(self.get_title()),
                    "placeholder": Formatting.escape(self.get_placeholder()),
                    "value": self._get_content(),
                    "required": self.required,
                    "error_message": ("" if (self.error_data is None) else Formatting.escape(self.get_error_message()))
                  }

        if (self.size == TextField.SIZE_SMALL):
            context['size'] = 10
            context['size_percentage'] = "30%"
        elif (self.size == TextField.SIZE_LARGE):
            context['size'] = 26
            context['size_percentage'] = "80%"
        else:
            context['size'] = 18
            context['size_percentage'] = "55%"
        #

        return self._render_oset_file("core/form/password", context)
    #

    def _set_form(self, form):
        """
Sets the form this field is part of.

:param form: Form

:since: v0.2.00
        """

        TextField._set_form(self, form)

        repetition_name = "{0}_repetition".format(self.name)

        value = form.get_input(repetition_name)

        if (self.mode & PasswordField.PASSWORD_CLEARTEXT != PasswordField.PASSWORD_CLEARTEXT): value = self._encrypt_value(value)
        self.repetition_value = value
    #

    def set_mode(self, mode):
        """
Sets the password field mode.

:param mode: Password field mode

:since: v0.2.00
        """

        if (type(mode) is not int): mode = self.__class__.get_mode_int(mode)
        self.mode = mode
    #

    def set_value(self, value):
        """
Sets the field value.

:param value: Field value

:since: v0.2.00
        """

        self.raw_value = value

        if (self.mode & PasswordField.PASSWORD_CLEARTEXT != PasswordField.PASSWORD_CLEARTEXT): value = self._encrypt_value(value)
        self.value = value

        self.valid = None
    #

    @staticmethod
    def get_mode_int(mode):
        """
Parses the given password mode parameter given as a string value.

:param mode: String mode

:return: (int) Internal mode
:since:  v0.2.00
        """

        _return = 0

        mode_set = mode.split("+")

        for mode in mode_set:
            if (mode == "cleartext"): _return |= PasswordField.PASSWORD_CLEARTEXT
            elif (mode == "md5"): _return |= PasswordField.PASSWORD_MD5
            elif (mode == "repetition"): _return |= PasswordField.PASSWORD_WITH_REPETITION
        #

        return _return
    #
#
