"""
pygame-menu
https://github.com/ppizarror/pygame-menu

VERTICAL VILL
Vertical fill box. Fills all available vertical space.
"""

__all__ = [
    'VFill',
    'VFillManager'
]

import pygame
import pygame_menu

from abc import ABC
from pygame_menu.widgets.core.widget import AbstractWidgetManager
from pygame_menu.widgets.widget.none import NoneWidget

from pygame_menu._types import NumberType, NumberInstance


# noinspection PyMissingOrEmptyDocstring
class VFill(NoneWidget):
    """
    Vertical fill widget. This widget fills all vertical space if available, else,
    it uses the min height.

    .. note::

        VMargin does not accept any transformation.

    :param min_height: Minimum height in px
    :param widget_id: ID of the widget
    """
    _min_height: int

    def __init__(
            self,
            min_height: NumberType,
            widget_id: str = ''
    ) -> None:
        assert isinstance(min_height, NumberInstance)
        assert min_height > 0, 'negative or zero margin is not valid'
        super(VFill, self).__init__(widget_id=widget_id)
        self._min_height = min_height

    def get_rect(self, *args, **kwargs) -> 'pygame.Rect':
        return self._rect.copy()


class VFillManager(AbstractWidgetManager, ABC):
    """
    VFil manager.
    """

    def vertical_fill(
            self,
            min_height: NumberType = 0,
            vfill_id: str = ''
    ) -> 'pygame_menu.widgets.VFill':
        """
        Adds a vertical fill to the Menu. This widget fills all vertical space
        if available, else, it uses the min height.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
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
