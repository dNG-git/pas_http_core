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

from binascii import hexlify
from time import time
from os import urandom

from dNG.controller.abstract_request import AbstractRequest
from dNG.data.binary import Binary
from dNG.data.http.translatable_error import TranslatableError

try:
    from dNG.data.text.key_store import KeyStore
    from dNG.database.nothing_matched_exception import NothingMatchedException
except ImportError: KeyStore = None

from .read_only_hidden_field import ReadOnlyHiddenField
from .view import View

class Processor(View):
    """
"Processor" provides form methods based on XHTML.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self, form_id = None):
        """
Constructor __init__(Processor)

:param form_id: Form ID used for CSRF protection; Use false to explicitly
                deactive this feature.

:since: v0.2.00
        """

        View.__init__(self, form_id)

        self.input_available = False
        """
Can be set to true using "set_input_available()"
        """
        self.input_data = None
        """
Dictionary containing form data
        """
        self.form_id_value = None
        """
Value for the given form ID
        """
        self.form_store = None
        """
HTTP form store
        """
        self.valid = None
        """
Form validity check result variable
        """

        if (form_id != False and KeyStore is not None):
            if (form_id is None or len(form_id) < 1):
                self.form_id_value = Binary.str(hexlify(urandom(16)))

                self.form_store = KeyStore()
                self.form_store.set_data_attributes(key = self.form_id, validity_end_time = time() + 3600)
                self.form_store.set_value_dict({ "form_id_value": self.form_id_value })
                self.form_store.save()
            else:
                try: self.form_store = Processor.load_form_store_id(self.form_id)
                except NothingMatchedException as handled_exception: raise TranslatableError("core_access_denied", 403, _exception = handled_exception)
            #
        #

        if (self.form_store is not None):
            form_data = self.form_store.get_value_dict()
            form_id_value = form_data.get("form_id_value")

            field = ReadOnlyHiddenField("form_id")
            field.set_value(self.form_id)
            self.add(field)

            field = ReadOnlyHiddenField(self.form_id)
            field.set_value(form_id_value)
            self.add(field)
        #

        self.supported_features['form_store'] = (self.form_store is not None)
    #

    def check(self, force = False):
        """
Parses all previously defined form fields and checks them.

:return: (bool) True if all checks are passed
:since:  v0.2.00
        """

        _return = (self.valid if (self.valid is not None) else True)

        if (self.form_store is not None):
            form_data = self.form_store.get_value_dict()
            form_id_value = (self.get_input(self.form_id) if (self.form_id_value is None) else self.form_id_value)

            if (form_data.get("form_id_value") != form_id_value): raise TranslatableError("core_access_denied")
        #

        if (len(self.cache) > 0 and (force or self.valid is None)):
            for section in self.cache:
                for field in section['fields']:
                    result = field.check()
                    if (not result): _return = False
                #
            #
        #

        self.valid = _return
        return _return
    #

    def get_form_store(self):
        """
Returns the form store.

:return: (object) Form store; None if undefined
:since:  v0.2.00
        """

        return self.form_store
    #

    def get_input(self, name):
        """
"get_input()" should be used to read the input value for the field from a
source (e.g. from a HTTP POST request parameter).

:param name: Field and parameter name

:return: (mixed) Value; None if not set
:since:  v0.2.00
        """

        if (self.input_data is None and self.input_available): self.input_data = AbstractRequest.get_instance().get_parameters()
        return (self.input_data.get(name) if (self.input_data is not None) else None)
    #

    def set_input_available(self):
        """
Sets the flag for available input. Input values can be read with
"get_input()".

:since: v0.2.00
        """

        self.input_available = True
    #

    def set_input_data(self, data):
        """
Sets the dictionary of available input data.

:since: v0.2.00
        """

        self.input_data = data
        self.set_input_available()
    #

    @staticmethod
    def load_form_store_id(form_id):
        """
Loads the KeyStore instance based form store by ID.

:param form_id: Form store ID

:return: (object) KeyStore instance based form store
:since:  v0.2.00
        """

        _return = KeyStore.load_key(form_id)
        _return.set_data_attributes(validity_end_time = time() + 300)

        return _return
    #
#
