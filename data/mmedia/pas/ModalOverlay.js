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
 * @module ModalOverlay
 */
define([ 'jquery', 'Hammer', 'djt/NodePosition.min', 'pas/L10n.min' ], function($, Hammer, NodePosition, L10n) {
	/**
	 * "ModalOverlay" is used to generate a viewport overlay for modal content.
	 * The "xdomremove" event can be used to detect closing of the modal
	 * overlay.
	 *
	 * @class ModalOverlay
	 *
	 * @param {object} args Arguments to initialize a given ModalOverlay
	 */
	function ModalOverlay(args) {
		if (args === undefined) {
			throw new Error('Missing required arguments');
		}

		this.$modal_node = null;

		if ('id' in args) {
			this.$modal_node = $("#" + args.id);
		} else if ('jQmodal' in args) {
			this.$modal_node = args.jQmodal;
		}

		if (this.$modal_node == null) {
			throw new Error('Missing required arguments');
		}

		var $overlayed_node = null;

		if ('overlayed_id' in args) {
			$overlayed_node = $("#" + args.overlayed_id);
		} else if ('jQoverlayed' in args) {
			$overlayed_node = args.jQoverlayed;
		}

		if ($overlayed_node == null) {
			throw new Error('Missing required arguments');
		}

		var at_reference = (('at_reference' in args) ? args.at_reference : 'top center');
		var my_reference = (('my_reference' in args) ? args.my_reference : 'top center');

		$overlayed_node.wrap('<div class="pagecontent_box pagecontent_overlayed_box" style="pointer-events: none"></div>');

		this.$overlay_node = $overlayed_node.parent();

		this.modal_node_position = new NodePosition({ jQat: this.$overlay_node,
		                                              jQmy: this.$modal_node,
		                                              at_reference: at_reference,
		                                              my_reference: my_reference
		                                            });
	}

	/**
	 * Destroys the overlay event listeners.
	 *
	 * @method
	 */
	ModalOverlay.prototype.destroy = function() {
		this.destroy_listeners();

		this.$modal_node.triggerHandler('xdomremove');

		var $wrapped_children = this.$overlay_node.children();
		$wrapped_children.detach();

		this.$overlay_node.after($wrapped_children);
		this.$overlay_node.remove();

		$wrapped_children.parent().trigger('xdomchanged');
	}

	/**
	 * Destroys the DOM listeners of the overlay node.
	 *
	 * @method
	 */
	ModalOverlay.prototype.destroy_listeners = function() {
		if (this.modal_node_position != null) {
			this.modal_node_position.destroy();
			this.modal_node_position = null;
		}
	}

	/**
	 * Returns the overlayed node jQuery instance.
	 *
	 * @method
	 *
	 * @return {object} jQuery instance
	 */
	ModalOverlay.prototype.get_jQoverlayed_node = function() {
		return this.$overlay_node.children();
	}

	return ModalOverlay;
});

//j// EOF