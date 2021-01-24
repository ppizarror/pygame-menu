"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SELECTION
Widget selection effect.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2021 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

__all__ = ['Selection']

import pygame
from pygame_menu.utils import assert_color
from pygame_menu._types import NumberType, ColorType, TYPE_CHECKING, Tuple2IntType, Tuple4IntType

if TYPE_CHECKING:
    from pygame_menu.widgets import Widget


class Selection(object):
    """
    Widget selection effect class.

    .. note::

        All selection classes must be copyable.

    :param margin_left: Left margin
    :param margin_right: Right margin
    :param margin_top: Top margin
    :param margin_bottom: Bottom margin
    """
    color: ColorType
    margin_bottom: NumberType
    margin_left: NumberType
    margin_right: NumberType
    margin_top: NumberType

    def __init__(self, margin_left: NumberType, margin_right: NumberType,
                 margin_top: NumberType, margin_bottom: NumberType) -> None:
        assert isinstance(margin_left, (int, float))
        assert isinstance(margin_right, (int, float))
        assert isinstance(margin_top, (int, float))
        assert isinstance(margin_bottom, (int, float))
        assert margin_left >= 0, 'left margin of widget selection cannot be negative'
        assert margin_right >= 0, 'right margin of widget selection cannot be negative'
        assert margin_top >= 0, 'top margin of widget selection cannot be negative'
        assert margin_bottom >= 0, 'bottom margin of widget selection cannot be negative'
        self.color = (0, 0, 0)
        self.margin_bottom = margin_bottom
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.margin_top = margin_top

    def set_color(self, color: ColorType) -> 'Selection':
        """
        Set the selection effect color.

        :param color: Selection color
        :return: Self reference
        """
        assert_color(color)
        self.color = color
        return self

    def get_margin(self) -> Tuple4IntType:
        """
        Return the top, left, bottom and right margins of the selection.

        :return: Tuple of *(top, left, bottom, right)* margins in px
        """
        return int(self.margin_top), int(self.margin_left), int(self.margin_bottom), int(self.margin_right)

    def get_xy_margin(self) -> Tuple2IntType:
        """
        Return the x/y margins of the selection.

        :return: Tuple of *(x, y)* margins
        """
        return int(self.margin_left + self.margin_right), int(self.margin_top + self.margin_bottom)

    def get_width(self) -> int:
        """
        Return the selection width (px) as sum of left and right margins.

        :return: Width in px
        """
        _, l, _, r = self.get_margin()
        return l + r

    def get_height(self) -> int:
        """
        Return the selection height (px) as sum of top and bottom margins.

        :return: Height in px
        """
        t, _, b, _ = self.get_margin()
        return t + b

    def inflate(self, rect: 'pygame.Rect') -> 'pygame.Rect':
        """
        Grow or shrink the rectangle size according to margins.

        :param rect: Rect object
        :return: Inflated rect
        """
        assert isinstance(rect, pygame.Rect)
        return pygame.Rect(int(rect.x - self.margin_left),
                           int(rect.y - self.margin_top),
                           int(rect.width + self.margin_left + self.margin_right),
                           int(rect.height + self.margin_top + self.margin_bottom))

    def draw(self, surface: 'pygame.Surface', widget: 'Widget') -> None:
        """
        Draw the selection.

        :param surface: Surface to draw
        :param widget: Widget object
        :type widget: :py:class:`pygame_menu.widgets.core.Widget`
        :return: None
        """
        raise NotImplementedError('override is mandatory')
