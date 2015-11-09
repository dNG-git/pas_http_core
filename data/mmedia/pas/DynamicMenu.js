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
 * @module DynamicMenu
 */
define([ 'jquery',
         'Hammer',
         'djt/NodePosition.min',
         'pas/L10n.min'
       ],
function($, Hammer, NodePosition, L10n) {
	/**
	 * Timeout to wait before closing a menu in ms.
	 *
	 * @constant
	 */
	var CLOSE_TIMEOUT = 125;

	/**
	 * "DynamicMenu" is used to show sub-menus placed next to an parent on hovering
	 * over the parent or tapping on it.
	 *
	 * @class DynamicMenu
	 *
	 * @param {object} args Arguments to initialize a given DynamicMenu
	 */
	function DynamicMenu(args) {
		if (args === undefined || (!('id' in args))) {
			throw new Error('Missing required argument');
		}

		var $nodes = $("#" + args.id + " > ul > li");
		var _this = this;

		$nodes.each(function() {
			_this._init_menu_item($(this));
		});
	}

	/**
	 * Hide sub menu.
	 *
	 * @method
	 *
	 * @param {object} $link jQuery link node
	 * @param {object} $menu jQuery sub menu node
	 */
	DynamicMenu.prototype._hide_sub_menu = function($link, $menu) {
		if ($menu.data('pas-dynamic-menu-sub-menu-visible') == '1') {
			$menu.css('display', 'none');
			$menu.data('pas-dynamic-menu-sub-menu-node-position').destroy();

			if ($menu.data('pas-dynamic-menu-sub-menu-deep-structure') == '1') {
				var _this = this;

				$menu.find('ul').each(function() {
					var $sub_menu = $(this);

					if ($sub_menu.data('pas-dynamic-menu-sub-menu-visible') == '1') {
						var $sub_menu_link = $sub_menu.data('pas-dynamic-menu-link');
						_this._hide_sub_menu($sub_menu_link, $sub_menu);
					}
				});
			}

			$menu.removeData('pas-dynamic-menu-sub-menu-node-position');
			$menu.data('pas-dynamic-menu-sub-menu-visible', '0');
		}

		var timeout_id = $link.data('pas-dynamic-menu-timeout');

		if (timeout_id !== undefined) {
			self.clearTimeout(timeout_id);
			$link.removeData('pas-dynamic-menu-timeout');
		}

		var $tap_close_menu_item = $menu.data('pas-dynamic-menu-sub-menu-close-item');

		if ($tap_close_menu_item !== undefined) {
			$menu.removeData('pas-dynamic-menu-sub-menu-close-item');
			$tap_close_menu_item.remove();
		}
	}

	/**
	 * Initialize the menu item.
	 *
	 * @TODO: Add support for sub menus
	 *
	 * @method
	 *
	 * @param {object} $menu_item jQuery menu item node
	 */
	DynamicMenu.prototype._init_menu_item = function($menu_item) {
		var $sub_menu = $menu_item.children('ul').first();

		if ($sub_menu.length > 0) {
			var $link = $menu_item.children('a').first();

			if ($link.length > 0) {
				$link.data('pas-dynamic-menu-href', $link.attr('href'));
				$link.attr('href', 'javascript:');

				$link.data('pas-dynamic-menu-sub-menu', $sub_menu);

				var link_listener = new Hammer($link.get(0));
				var _this = this;

				link_listener.on('tap', function(event) {
					_this._on_tap(event);
				});

				$link.on('mouseenter', function($event) {
					_this._on_mouseenter($event);
				});

				$link.on('mouseleave', function($event) {
					$link.data('pas-dynamic-menu-timeout',
					           self.setTimeout(function() { _this._on_mouseleave($event); }, CLOSE_TIMEOUT)
					          );
				});

				$sub_menu.data('pas-dynamic-menu-link', $link);

				$sub_menu.on('mouseenter', function($event) {
					_this._on_mouseenter($event);
				});

				$sub_menu.on('mouseleave', function($event) {
					$link.data('pas-dynamic-menu-timeout',
					           self.setTimeout(function() { _this._on_mouseleave($event); }, CLOSE_TIMEOUT)
					          );
				});
			}
		}
	}

	/**
	 * "mouseenter" event listener.
	 *
	 * @method
	 *
	 * @param {object} $event jQuery event instance
	 */
	DynamicMenu.prototype._on_mouseenter = function($event) {
		var $link = null;
		var $node = $($event.currentTarget);
		var $sub_menu = null;

		if ($node.data('pas-dynamic-menu-sub-menu') !== undefined) {
			$link = $node;
			$sub_menu = $node.data('pas-dynamic-menu-sub-menu');
		} else {
			$link = $node.data('pas-dynamic-menu-link');
			$sub_menu = $node;
		}

		this._show_sub_menu($link, $sub_menu);
	}

	/**
	 * "mouseleave" event listener.
	 *
	 * @method
	 *
	 * @param {object} $event jQuery event instance
	 */
	DynamicMenu.prototype._on_mouseleave = function($event) {
		var $link = null;
		var $node = $($event.currentTarget);
		var $sub_menu = null;

		if ($node.data('pas-dynamic-menu-sub-menu') !== undefined) {
			$link = $node;
			$sub_menu = $node.data('pas-dynamic-menu-sub-menu');
		} else {
			$link = $node.data('pas-dynamic-menu-link');
			$sub_menu = $node;
		}

		this._hide_sub_menu($link, $sub_menu);
	}

	/**
	 * "tap" event listener
	 *
	 * @method
	 *
	 * @param {object} event Hammer event instance
	 */
	DynamicMenu.prototype._on_tap = function(event) {
		var $link = $(event.target);
		var $sub_menu = $link.data('pas-dynamic-menu-sub-menu');

		if ($sub_menu.data('pas-dynamic-menu-sub-menu-visible') == '1') {
			var link_href = $link.data('pas-dynamic-menu-href');

			if (link_href !== undefined && link_href != '') {
				self.document.location.href = link_href;
			}
		} else {
			var _this = this;

			L10n.when_loaded('core', function() {
				var $tap_close_menu_item = $("<li><a href='javascript:'><small>" + L10n.get('core_close') + "</small></a></li>");

				$sub_menu.append($tap_close_menu_item);
				$sub_menu.data('pas-dynamic-menu-sub-menu-close-item', $tap_close_menu_item);

				var link_listener = new Hammer($tap_close_menu_item.get(0));

				link_listener.on('tap', function(event) {
					_this._hide_sub_menu($link, $sub_menu);
				});

				_this._show_sub_menu($link, $sub_menu);
			});
		}
	}

	/**
	 * Show sub menu next to the parent.
	 *
	 * @method
	 *
	 * @param {object} $link jQuery link node
	 * @param {object} $menu jQuery sub menu node
	 */
	DynamicMenu.prototype._show_sub_menu = function($link, $menu) {
		if ($menu.data('pas-dynamic-menu-sub-menu-visible') != '1') {
			$menu.css('min-width', $link.parent().width() + 'px');

			var my_reference = 'top left';
			var at_reference = 'bottom left';

			if ($menu.data('pas-dynamic-menu-sub-menu-child') == '1') {
				my_reference = 'top left';
				at_reference = 'top right';
			}

			var node_position = new NodePosition({ jQmy: $menu,
			                                       jQat: $link,
			                                       my_reference: my_reference,
			                                       at_reference: at_reference,
			                                       my_dom_restructure: true,
			                                       my_reposition_on_scroll: true
			                                     });

			$menu.css('display', 'block');
			$menu.data('pas-dynamic-menu-sub-menu-node-position', node_position);
			$menu.data('pas-dynamic-menu-sub-menu-visible', '1');
		}

		var timeout_id = $link.data('pas-dynamic-menu-timeout');

		if (timeout_id !== undefined) {
			self.clearTimeout(timeout_id);
			$link.removeData('pas-dynamic-menu-timeout');
		}
	}

	return DynamicMenu;
});

//j// EOF