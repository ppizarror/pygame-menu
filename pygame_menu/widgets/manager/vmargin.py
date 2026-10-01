"""
pygame-menu
https://github.com/ppizarror/pygame-menu

VERTICAL MARGIN
Vertical box margin.
"""

from __future__ import annotations

__all__ = ["VMarginManager"]

from abc import ABC
from typing import TYPE_CHECKING

from pygame_menu.widgets.core.abstract_widget import AbstractWidgetManager
from pygame_menu.widgets.widget.vmargin import VMargin

if TYPE_CHECKING:
    from pygame_menu._types import NumberType


class VMarginManager(AbstractWidgetManager, ABC):
    """
    VMargin manager.
    """

    def vertical_margin(self, margin: NumberType, margin_id: str = "") -> VMargin:
        """
        Adds a vertical margin to the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behavior apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param margin: Vertical margin in px
        :param margin_id: ID of the vertical margin
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.VMargin`
        """
        attributes = self._filter_widget_attributes({})
        widget = VMargin(margin, widget_id=margin_id)
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)
        return widget
