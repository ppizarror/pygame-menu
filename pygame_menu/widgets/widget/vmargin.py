"""
pygame-menu
https://github.com/ppizarror/pygame-menu

VERTICAL MARGIN
Vertical box margin.
"""

__all__ = ['VMargin']

import pygame

from pygame_menu.widgets.widget.none import NoneWidget

from pygame_menu._types import NumberType


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
        super(VMargin, self).__init__(widget_id=widget_id)
        self._rect.width = 0
        self._rect.height = int(margin)

    def get_rect(self, *args, **kwargs) -> 'pygame.Rect':
        return self._rect.copy()
