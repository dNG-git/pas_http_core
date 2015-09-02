//j// BOF

/*
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
*/

/**
 * @module HttpJsonApiRequest
 */
define([ 'jquery', 'djs/HttpJsonRequest.min' ], function($, _super) {
	/**
	 * "HttpJsonApiRequest" instances provide easier access to the "direct PAS"
	 * API endpoints.
	 *
	 * @class HttpJsonApiRequest
	 * @param {Object} args Arguments to initialize a given HttpJsonApiRequest
	 */
	function HttpJsonApiRequest(args) {
		if (args === undefined) {
			args = { };
		}

		this.base_url = null;
		this.endpoint = null;
		this.final_error_codes = [ 400, 402, 410, 411, 413, 414, 500, 501, 505 ];
		this.reload_error_codes = [ 401, 403 ];
		this.timeout = 30;
		this.uuid = '';

		if (!('url' in args)) {
			if ('base_url' in args) {
				this.base_url = args.base_url;
			} else if ('pas_config' in self && 'HttpJsonApiRequest_base_url' in self.pas_config) {
				this.base_url = self.pas_config.HttpJsonApiRequest_base_url;
			}
		}

		if ('endpoint' in args) {
			this.endpoint = args.endpoint;
		}

		if ('timeout' in args) {
			this.timeout = args.timeout;
		} else if ('pas_config' in self && 'HttpJsonApiRequest_timeout' in self.pas_config) {
			this.timeout = self.pas_config.HttpJsonApiRequest_timeout;
		}

		if ('uuid' in args) {
			this.uuid = args.uuid;
		} else if ('pas_config' in self && 'HttpJsonApiRequest_session_uuid' in self.pas_config) {
			this.uuid = self.pas_config.HttpJsonApiRequest_session_uuid;
		}

		_super.call(args);
	}

	$.extend(HttpJsonApiRequest.prototype, _super.prototype);

	/**
	 * Returns the error codes a call should not be retried.
	 *
	 * @method
	 * @return {Array} List of HTTP codes
	 */
	HttpJsonApiRequest.prototype.get_final_error_codes = function() {
		return this.final_error_codes;
	}

	/**
	 * Returns the error codes the page should be reloaded.
	 *
	 * @method
	 * @return {Array} List of HTTP codes
	 */
	HttpJsonApiRequest.prototype.get_reload_error_codes = function() {
		return this.reload_error_codes;
	}

	/**
	 * Initializes a repetitive API ping call.
	 *
	 * @method
	 * @param {Object} args Arguments to override default call parameter
	 */
	HttpJsonApiRequest.prototype.init_ping = function(args) {
		var _return = null;

		if (args === undefined) {
			args = { };
		}

		if (this.base_url != null && this.endpoint == null && (!('endpoint' in args))) {
			throw new Error('Missing required argument');
		}

		if ('delay' in args) {
			var _this = this;
			self.setTimeout(function () { _this._ping(args); }, 1000 * args.delay);
		} else {
			this._ping(args);
		}
	}

	/**
	 * Prepares the query string.
	 *
	 * @method
	 * @param {Object} args Query string arguments
	 * @return {String} Prepared query string
	 */
	HttpJsonApiRequest.prototype._prepare_query_string = function(args) {
		var _return = _super.prototype._prepare_query_string.call(this, args);

		if (this.uuid != '') {
			var is_uuid_defined = false;

			if (_return.length > 0) {
				is_uuid_defined = (_return.search(/(;|^)uuid=/) < 0);

				if (!(is_uuid_defined)) {
					_return += ';';
				}
			}

			if (is_uuid_defined) {
				_return = _return.replace(/(;|^)uuid=\w+(;|$)/, "$1uuid=" + this.uuid + "$2");
			} else {
				_return += "uuid=" + this.uuid;
			}
		}

		return _return;
	}

	/**
	 * Prepares and extends the given request arguments.
	 *
	 * @method
	 * @param {Object} args Base arguments
	 * @return {Object} Prepared and extended arguments
	 */
	HttpJsonApiRequest.prototype._prepare_request_args = function(args) {
		var _return = _super.prototype._prepare_request_args.call(this, args);

		if (this.base_url != null) {
			var endpoint = this.endpoint;

			if (endpoint == null) {
				if (!('endpoint' in args)) {
					throw new Error('Missing required arguments');
				}

				endpoint = args.endpoint;
			}

			_return['url'] = this.base_url + "apis/" + endpoint;
		}

		_return['timeout'] = 1000 * this.timeout;

		return _return;
	}

	/**
	 * Executes an API ping call.
	 *
	 * @method
	 * @param {Object} args Arguments to override default call parameter
	 */
	HttpJsonApiRequest.prototype._ping = function(args) {
		var promise = this.call(args);
		var _this = this;

		promise.done(function(data, status, jQxhr) {
			if ('expires_in' in data) {
				self.setTimeout(function () { _this._ping(args); }, 900 * data.expires_in);
			} else if ('delay' in args) {
				self.setTimeout(function () { _this._ping(args); }, 1000 * args.delay);
			}
		});

		promise.fail(function(jQxhr, status, error) {
			if ($.inArray(jQxhr.status, _this.get_reload_error_codes())) {
				self.location.reload(true);
			} else if ($.inArray(jQxhr.status, _this.get_final_error_codes()) < 0) {
				self.setTimeout(function () { _this._ping(args); }, 1000);
			}
		});
	}

	return HttpJsonApiRequest;
});

//j// EOF