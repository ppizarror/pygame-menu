"""
pygame-menu
https://github.com/ppizarror/pygame-menu

HIGHLIGHT
Widget selection highlight box effect.
"""

__all__ = ['HighlightSelection']

import pygame
import pygame_menu

from pygame_menu.widgets.core import Selection

from pygame_menu._types import NumberType


class HighlightSelection(Selection):
    """
    Widget selection highlight class.

    .. note::

        Widget background color may not reach the entire selection area.

    :param border_width: Border width of the highlight box (px)
    :param margin_x: X margin of selected highlight box (px)
    :param margin_y: Y margin of selected highlight box (px)
    """
    _border_width: int

    def __init__(
            self,
            border_width: int = 1,
            margin_x: NumberType = 16,
            margin_y: NumberType = 8
    ) -> None:
        assert isinstance(border_width, int)
        assert margin_x >= 0 and margin_y >= 0
        assert border_width >= 0

        margin_x = float(margin_x)
        margin_y = float(margin_y)
        super(HighlightSelection, self).__init__(
            margin_left=margin_x / 2,
            margin_right=margin_x / 2,
            margin_top=margin_y / 2,
            margin_bottom=margin_y / 2
        )

        self._border_width = border_width

    # noinspection PyMissingOrEmptyDocstring
    def draw(self, surface: 'pygame.Surface', widget: 'pygame_menu.widgets.Widget') -> 'HighlightSelection':
        if self._border_width == 0:
            return self
        # noinspection PyArgumentList
        pygame.draw.rect(
            surface,
            self.color,
            self.inflate(widget.get_rect()),
            self._border_width
        )
        return self
