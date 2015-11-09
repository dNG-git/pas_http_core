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
 * @module L10n
 */
define([ 'jquery', 'pas/HttpJsonApiRequest.min' ], function($, HttpJsonApiRequest) {
	/**
	 * L10n (localization) dictionary
	 */
	var dict = { };
	/**
	 * Object holding a list of files loaded
	 */
	var files_loaded = { };
	/**
	 * List of currently loading jQuery Promise objects
	 */
	var files_loading = { };
	/**
	 * Array of files not yet requested for bulk-loading
	 */
	var files_pending = [ ];

	/**
	 * "L10n" provides static functions to access server-side language files.
	 *
	 * @namespace L10n
	 */
	var L10n = new Object();

	/**
	 * Add the given language section for loading.
	 *
	 * @function
	 * @memberof L10n
	 * @static
	 *
	 * @param {string} file_id L10n file ID
	 */
	L10n.init = function(file_id) {
		if (!(file_id in files_loaded || $.inArray(file_id, files_pending) > -1)) {
			files_pending.push(file_id);
		}
	}

	/**
	 * Returns the value with the specified key or the default one if undefined.
	 *
	 * @function
	 * @memberof L10n
	 * @static
	 *
	 * @param {string} key L10n key
	 * @param {string} default Default value if not translated
	 *
	 * @return {string} Value
	 */
	L10n.get = function(key, _default) {
		if (_default === undefined) {
			_default = key;
		}

		return ((key in dict) ? dict[key] : _default);
	}

	/**
	 * Calls the given callback as soon as bulk-loading the requested language
	 * section has been completed.
	 *
	 * @function
	 * @memberof L10n
	 * @static
	 *
	 * @param {string} file_id L10n file ID
	 * @param {function} callback Callback
	 */
	L10n.when_loaded = function(file_id, callback) {
		if (!(file_id in files_loaded || $.inArray(file_id, files_pending) > -1)) {
			this.init(file_id);
		}

		if (files_pending.length > 0) {
			this._load_files_pending();
		}

		if (file_id in files_loading) {
			files_loading[file_id].always(callback);
		} else {
			callback();
		}
	}

	/**
	 * Start bulk-loading of pending language sections.
	 *
	 * @function
	 * @memberof L10n
	 * @static
	 */
	L10n._load_files_pending = function() {
		var files = files_pending.join(' ');

		if (!('pas_config' in self && 'lang' in self.pas_config)) {
			throw new Error('Language is not specified in PAS configuration');
		}

		var hjs_request = new HttpJsonApiRequest({ endpoint: 'pas/lang/get/1.0/' + encodeURIComponent(files) });
		var hjs_promise = hjs_request.call({ data: { lang: self.pas_config.lang }, cache: true });

		for (var i = 0; i < files_pending.length; i++) {
			var file = files_pending[i];

			files_loaded[file] = false;
			files_loading[file] = hjs_promise;

			hjs_promise.always(function() {
				files_loaded[file] = true;
				delete files_loading[file];
			});
		}

		hjs_promise.done(function(data, status, jQxhr) {
			$.extend(dict, data);
		});

		files_pending = [ ];
	}

	return L10n;
});

//j// EOF