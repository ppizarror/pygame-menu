"""
pygame-menu
https://github.com/ppizarror/pygame-menu

HORIZONTAL MARGIN
Horizontal box margin.
"""

__all__ = ['HMargin']

import pygame

from pygame_menu.widgets.widget.none import NoneWidget

from pygame_menu._types import NumberType


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
        super(HMargin, self).__init__(widget_id=widget_id)
        self._rect.width = int(margin)
        self._rect.height = 0

    def get_rect(self, *args, **kwargs) -> 'pygame.Rect':
        return self._rect.copy()
