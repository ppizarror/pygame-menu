"""
pygame-menu
https://github.com/ppizarror/pygame-menu

VERTICAL VILL
Vertical fill box. Fills all available vertical space.
"""

from __future__ import annotations

__all__ = ["VFillManager"]

from abc import ABC
from typing import TYPE_CHECKING

from pygame_menu.widgets.core.abstract_widget import AbstractWidgetManager
from pygame_menu.widgets.widget.vfill import VFill

if TYPE_CHECKING:
    from pygame_menu._types import NumberType


class VFillManager(AbstractWidgetManager, ABC):
    """
    VFill manager.
    """

    def vertical_fill(self, min_height: NumberType = 0, vfill_id: str = "") -> VFill:
        """
        Adds a vertical fill to the Menu. This widget fills all vertical space
        if available, else, it uses the min height.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behavior apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param min_height: Minimum height in px
        :param vfill_id: ID of the vertical fill
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.VFill`
        """
        attributes = self._filter_widget_attributes({})
        widget = VFill(min_height, widget_id=vfill_id)
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)
        return widget
