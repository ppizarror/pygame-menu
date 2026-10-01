"""
pygame-menu
https://github.com/ppizarror/pygame-menu

HORIZONTAL MARGIN
Horizontal box margin.
"""

from __future__ import annotations

__all__ = ["HMarginManager"]

from abc import ABC
from typing import TYPE_CHECKING

from pygame_menu.widgets.core.abstract_widget import AbstractWidgetManager
from pygame_menu.widgets.widget.hmargin import HMargin

if TYPE_CHECKING:
    from pygame_menu._types import NumberType


class HMarginManager(AbstractWidgetManager, ABC):
    """
    HMargin manager.
    """

    def horizontal_margin(self, margin: NumberType, margin_id: str = "") -> HMargin:
        """
        Adds a horizontal margin to the Menu. Only useful in frames.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behavior apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param margin: Horizontal margin in px
        :param margin_id: ID of the horizontal margin
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.HMargin`
        """
        attributes = self._filter_widget_attributes({})
        widget = HMargin(margin, widget_id=margin_id)
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget
