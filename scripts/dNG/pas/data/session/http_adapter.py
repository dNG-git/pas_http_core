# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.session.HttpAdapter
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;session

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasSessionVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from binascii import hexlify
from os import urandom
from time import time

from dNG.pas.controller.abstract_http_response import AbstractHttpResponse
from dNG.pas.data.binary import Binary
from dNG.pas.data.settings import Settings
from dNG.pas.data.text.tmd5 import Tmd5
from dNG.pas.module.named_loader import NamedLoader
from .abstract_adapter import AbstractAdapter

class HttpAdapter(AbstractAdapter):
#
	"""
A session protocol adapter for HTTP to implement methods that rely on
protocol specific functionality.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def is_persistent(self):
	#
		"""
Returns true if the uuID session set persistently at the client.

:return: (bool) True if set
:since:  v0.1.00
		"""

		return (self.session.get("uuids.passcode") != None)
	#

	def is_valid(self):
	#
		"""
Returns true if the defined session is valid.

:return: (bool) True if session is valid
:since:  v0.1.00
		"""

		var_return = True

		if (self.session.get("uuids.passcode") != None):
		#
			pass
		#

		return var_return
	#

	def save(self):
	#
		"""
Saves changes of the uuIDs instance.

:return: (bool) True on success
:since: v0.1.00
		"""

		passcode_timeout = self.session.get("uuids.passcode_timeout")
		response = AbstractHttpResponse.get_instance()

		if (passcode_timeout != None and isinstance(response, AbstractHttpResponse) and passcode_timeout < time()):
		#
			self.session.set("uuids.passcode_prev", self.session.get("uuids.passcode"))

			passcode = Binary.str(hexlify(urandom(16)))
			self.session.set("uuids.passcode", passcode)
			self.session.set("uuids.passcode_timeout", int(time() + int(Settings.get("pas_session_uuids_passcode_timeout", 300))))

			passcode = Tmd5.encode(passcode)
			response.set_cookie("uuids", "{0}:{1}".format(self.session.uuid, passcode))
		#

		return True
	#

	def set_cookie(self, mode):
	#
		"""
Sets a cookie to store the uuID.

:param mode: True to use a cookie

:since: v0.1.00
		"""

		if (mode and self.session.get("uuids.passcode") == None):
		#
			self.session.set("uuids.passcode_timeout", 0)
			self.session.set_session_time(int(Settings.get("pas_session_uuids_passcode_session_time", 604800)))
		#
	#

	@staticmethod
	def get_uuid():
	#
		"""
Returns the uuID.

:return: (str) Unique user identification; None if unknown
:since:  v0.1.00
		"""

		instance = NamedLoader.get_singleton("dNG.pas.controller.AbstractHttpRequest", False)

		if (instance != None and hasattr(instance, "get_cookie")):
		#
			uuids_cookie = instance.get_cookie("uuids")
			var_return = (None if (uuids_cookie == None) else uuids_cookie.split(":", 1)[0])
		#
		else: var_return = None

		return var_return
	#

	"""
		
	}

	if (($this->uuid_status != "verified")&&($this->uuid))
	{
		$direct_globals['db']->initSelect ($direct_settings['uuids_table']);
		$direct_globals['db']->defineAttributes ($direct_settings['uuids_table'].".*");

$f_select_criteria = ("<sqlconditions>
".($direct_globals['db']->defineRowConditionsEncode ($direct_settings['uuids_table'].".ddbuuids_list_id",$this->uuid,"string"))."
".($direct_globals['db']->defineRowConditionsEncode ($direct_settings['uuids_table'].".ddbuuids_list_maxage_inactivity",$direct_cachedata['core_time'],"number",">"))."
</sqlconditions>");

		$direct_globals['db']->defineRowConditions ($f_select_criteria);
		$direct_globals['db']->defineLimit (1);

		$f_uuid_array = $direct_globals['db']->queryExec ("sa");
	}

	if (!trim ($this->uuid)) { $this->uuid_status = "invalid"; }
	elseif ($this->uuid_status == "new")
	{
		$this->uuid_status = "verified";
		$this->uuid_cookie_mode = $f_cookie_mode;
		$this->uuid_data = "";
		$this->uuid_insert_mode = true;
		$f_return = "";

		if ($f_cookie_mode)
		{
			mt_srand (/*#ifdef(PHP4):((double)microtime ()) * 1000000:#*/);
			$this->uuid_passcode = $direct_globals['basic_functions']->tmd5 (uniqid (mt_rand ()));
			$this->uuid_passcode_prev = $this->uuid_passcode;
		}
	}
	elseif ($this->uuid_status == "verified")
	{
		if ($f_type == "a") { $f_return = explode ("\n",(trim ($this->uuid_data))); }
		else { $f_return = trim ($this->uuid_data); }
	}
	elseif ($f_uuid_array)
	{
		$f_timeout_check = (((!$this->uuid_cookie_timeout)||(($f_uuid_array['ddbuuids_list_maxage_inactivity'] + $direct_settings['uuids_cookie_interaction_timeout']) >= $this->uuid_cookie_timeout)) ? true : false);
		$f_validation_check = false;

		if (($f_uuid_array['ddbuuids_list_passcode_timeout'])||($this->uuid_passcode))
		{
			if (($f_uuid_array['ddbuuids_list_passcode'])&&($f_uuid_array['ddbuuids_list_passcode'] == $this->uuid_passcode)) { $f_validation_check = true; }
/* -------------------------------------------------------------------------
Parallel requests are supported. For a time of usually 30 seconds we accept
both the old and new passcode.
------------------------------------------------------------------------- */

			if ((!$f_validation_check)&&($direct_cachedata['core_time'] <= ($f_uuid_array['ddbuuids_list_passcode_timeout'] - $direct_settings['uuids_passcode_timeout'] + $direct_settings['uuids_cookie_interaction_timeout']))&&($this->uuid_passcode == $f_uuid_array['ddbuuids_list_passcode_prev'])) { $f_validation_check = true; }
		}
		elseif ($f_uuid_array['ddbuuids_list_ip'] == $direct_settings['user_ip']) { $f_validation_check = true; }

		if (($f_timeout_check)&&($f_validation_check)&&($f_uuid_array['ddbuuids_list_maxage_inactivity'] > $direct_cachedata['core_time']))
		{
			$this->uuid_status = "verified";

			if ($f_uuid_array['ddbuuids_list_passcode_timeout'])
			{
				$this->uuid_cookie_mode = true;

				if (($f_uuid_array['ddbuuids_list_passcode_timeout'] < $direct_cachedata['core_time'])&&(!$direct_settings['swg_cookies_deactivated']))
				{
					mt_srand (/*#ifdef(PHP4):((double)microtime ()) * 1000000:#*/);
					$this->uuid_passcode_prev = $f_uuid_array['ddbuuids_list_passcode'];
					$this->uuid_passcode = $direct_globals['basic_functions']->tmd5 (uniqid (mt_rand ()));

					$this->uuidWrite ($f_uuid_array['ddbuuids_list_data']);
					$this->uuidCookieSave ();
				}
			}
			else { $this->uuid_cookie_mode = false; }

			if ($f_uuid_array['ddbuuids_list_ip'] == $direct_settings['user_ip']) { $direct_settings['user_ipcwarn'] = false; }
			else
			{
				$direct_globals['output']->warning (direct_local_get ("core_user_warning"),(direct_local_get ("core_user_warning_ip")));
				$direct_settings['user_ipcwarn'] = true;
			}

			$this->uuid_data = $f_uuid_array['ddbuuids_list_data'];
			$f_return = (($f_type == "a") ? explode ("\n",(trim ($this->uuid_data))) : trim ($this->uuid_data));
		}
		else { $this->uuid_status = "invalid"; }
	}
	else { $this->uuid_status = "invalid"; }

	if ($this->uuid_status == "invalid")
	{
		$direct_globals['db']->initDelete ($direct_settings['uuids_table']);

		$f_select_criteria = "<sqlconditions>".($direct_globals['db']->defineRowConditionsEncode ($direct_settings['uuids_table'].".ddbuuids_list_id",$this->uuid,"string"))."</sqlconditions>";
		$direct_globals['db']->defineRowConditions ($f_select_criteria);

		$direct_globals['db']->defineLimit (1);
		if (($direct_globals['db']->queryExec ("co"))&&(!$direct_settings['uuids_auto_maintenance'])) { $direct_globals['db']->vOptimize ($direct_settings['uuids_table']); }

		$this->uuid = md5 (uniqid ($direct_settings['user_ip']."_".(mt_rand ())."_"));
		$this->uuid_status = "verified";
		$this->uuid_cookie_mode = $f_cookie_mode;
		$this->uuid_data = "";
		$this->uuid_insert_mode = true;

		$direct_globals['input']->uuidSet ($this->uuid);
		$f_return = "";

		if ($f_cookie_mode)
		{
			mt_srand (/*#ifdef(PHP4):((double)microtime ()) * 1000000:#*/);
			$this->uuid_passcode = $direct_globals['basic_functions']->tmd5 (uniqid (mt_rand ()));
			$this->uuid_passcode_prev = $this->uuid_passcode;
		}
	}

	return /*#ifdef(DEBUG):direct_debug (7,"sWG/#echo(__FILEPATH__)# -kernel->uuidGet ()- (#echo(__LINE__)#)",:#*/$f_return/*#ifdef(DEBUG):,true):#*/;
	"""
#

##j## EOF