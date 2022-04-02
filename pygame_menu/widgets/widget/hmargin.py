"""
pygame-menu
https://github.com/ppizarror/pygame-menu

HORIZONTAL MARGIN
Horizontal box margin.
"""

__all__ = [
    'HMargin',
    'HMarginManager'
]

import pygame
import pygame_menu

from abc import ABC
from pygame_menu.widgets.core.widget import AbstractWidgetManager
from pygame_menu.widgets.widget.none import NoneWidget

from pygame_menu._types import NumberType, NumberInstance


# noinspection PyMissingOrEmptyDocstring
class HMargin(NoneWidget):
    """
    Horizontal margin widget.

    .. note::

        HMargin does not accept any transformation.

    :param margin: Horizontal margin in px
    :param widget_id: ID of the widget
    """

    def __init__(
            self,
            margin: NumberType,
            widget_id: str = ''
    ) -> None:
        assert isinstance(margin, NumberInstance)
        assert margin > 0, \
            'zero margin is not valid, prefer adding a NoneWidget menu.add.none_widget()'
        super(HMargin, self).__init__(widget_id=widget_id)
        self._rect.width = int(margin)
        self._rect.height = 0

    def get_rect(self, *args, **kwargs) -> 'pygame.Rect':
        return self._rect.copy()


class HMarginManager(AbstractWidgetManager, ABC):
    """
    HMargin manager.
    """

    def horizontal_margin(
            self,
            margin: NumberType,
            margin_id: str = ''
    ) -> 'pygame_menu.widgets.HMargin':
        """
        Adds a horizontal margin to the Menu. Only useful in frames.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
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
