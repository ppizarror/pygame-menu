"""
pygame-menu
https://github.com/ppizarror/pygame-menu

VERTICAL MARGIN
Vertical box margin.
"""

__all__ = [
    'VMargin',
    'VMarginManager'
]

import pygame
import pygame_menu

from abc import ABC
from pygame_menu.widgets.core.widget import AbstractWidgetManager
from pygame_menu.widgets.widget.none import NoneWidget

from pygame_menu._types import NumberType, NumberInstance


# noinspection PyMissingOrEmptyDocstring
class VMargin(NoneWidget):
    """
    Vertical margin widget. VMargin only accepts margin, not padding.

    .. note::

        VMargin does not accept any transformation.

    :param margin: Vertical margin in px
    :param widget_id: ID of the widget
    """

    def __init__(
            self,
            margin: NumberType,
            widget_id: str = ''
    ) -> None:
        assert isinstance(margin, NumberInstance)
        assert margin > 0, 'negative or zero margin is not valid'
        super(VMargin, self).__init__(widget_id=widget_id)
        self._rect.width = 0
        self._rect.height = int(margin)

    def get_rect(self, *args, **kwargs) -> 'pygame.Rect':
        return self._rect.copy()


class VMarginManager(AbstractWidgetManager, ABC):
    """
    VMargin manager.
    """

    def vertical_margin(
            self,
            margin: NumberType,
            margin_id: str = ''
    ) -> 'pygame_menu.widgets.VMargin':
        """
        Adds a vertical margin to the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
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
