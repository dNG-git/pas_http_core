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
 * @module ExecutingSpinner
 */
define([ 'jquery', 'djt/Spinner.min', 'pas/ModalOverlay.min' ], function($, Spinner, ModalOverlay) {
	/**
	 * "ExecutingSpinner" instances provide an animation for work being done on a
	 * parent node.
	 *
	 * @class ExecutingSpinner
	 *
	 * @param {object} args Arguments to initialize a given ExecutingSpinner
	 */
	function ExecutingSpinner(args) {
		if (args === undefined || (!('id' in args))) {
			throw new Error('Missing required argument');
		}

		this.id = args.id;
		this.spinner = null;
		this.spinner_modal_overlay = null;
	}

	/**
	 * Stops and destroys the "executing spinner" animation.
	 *
	 * @method
	 */
	ExecutingSpinner.prototype.destroy = function() {
		this.destroy_listeners();

		if (this.spinner != null) {
			this.spinner_modal_overlay.destroy();
			this.spinner_modal_overlay = null;

			this.spinner.get_jQnode().remove();
			this.spinner = null;
		}
	}

	/**
	 * Destroys the DOM listeners of the "executing spinner".
	 *
	 * @method
	 */
	ExecutingSpinner.prototype.destroy_listeners = function() {
		if (this.spinner_modal_overlay != null) {
			this.spinner_modal_overlay.destroy();
		}
	}

	/**
	 * Shows the "executing spinner" animation.
	 *
	 * @method
	 */
	ExecutingSpinner.prototype.show = function() {
		if (this.spinner == null) {
			var $base_node = $("#" + this.id);
			var spinner_width = $base_node.width();
			var spinner_height = $base_node.height();
			var spinner_size = ((spinner_width < spinner_height) ? spinner_width : spinner_height);

			this.spinner = new Spinner({ jQparent: $('body'),
			                             width: spinner_size,
			                             height: spinner_size
			                           });

			var $spinner = this.spinner.get_jQnode();

			this.spinner_modal_overlay = new ModalOverlay({ jQmodal: $spinner,
			                                                jQoverlayed: $base_node
			                                              });
		}

		this.spinner.show();
	}

	return ExecutingSpinner;
});

//j// EOF