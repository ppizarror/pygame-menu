"""
pygame-menu
https://github.com/ppizarror/pygame-menu

NONE WIDGET
None widget definition.
"""

from __future__ import annotations

__all__ = ["NoneWidgetManager"]

from abc import ABC

from pygame_menu.widgets.core.abstract_widget import AbstractWidgetManager
from pygame_menu.widgets.widget.none import NoneWidget


class NoneWidgetManager(AbstractWidgetManager, ABC):
    """
    NoneWidget manager.
    """

    def none_widget(self, widget_id: str = "") -> NoneWidget:
        """
        Add a none widget to the Menu.

        .. note::

            This widget is useful to fill column/rows layout without compromising
            any visuals. Also, it can be used to store information or even to add
            a ``draw_callback`` function to it for being called on each Menu draw.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behavior apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param widget_id: Widget ID
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.NoneWidget`
        """
        attributes = self._filter_widget_attributes({})

        widget = NoneWidget(widget_id=widget_id)
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget
