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

import copy
import pygame
import pygame_menu

from pygame_menu.utils import assert_color

from pygame_menu._types import NumberType, ColorType, ColorInputType, Tuple2IntType, \
    Tuple4IntType, NumberInstance, Optional


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
        assert isinstance(margin_left, NumberInstance)
        assert isinstance(margin_right, NumberInstance)
        assert isinstance(margin_top, NumberInstance)
        assert isinstance(margin_bottom, NumberInstance)
        assert margin_left >= 0, 'left margin of widget selection cannot be negative'
        assert margin_right >= 0, 'right margin of widget selection cannot be negative'
        assert margin_top >= 0, 'top margin of widget selection cannot be negative'
        assert margin_bottom >= 0, 'bottom margin of widget selection cannot be negative'
        self.color = (0, 0, 0)
        self.margin_bottom = margin_bottom
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.margin_top = margin_top

    def margin_xy(self, x: NumberType, y: NumberType) -> 'Selection':
        """
        Set margins at left-right / top-bottom.

        :param x: Left-Right margin in px
        :param y: Top-Bottom margin in px
        :return: Self reference
        """
        assert isinstance(x, NumberInstance) and x >= 0
        assert isinstance(y, NumberInstance) and y >= 0
        self.margin_left = x
        self.margin_right = x
        self.margin_top = y
        self.margin_bottom = y
        return self

    def zero_margin(self) -> 'Selection':
        """
        Makes selection margin zero.

        :return: Self reference
        """
        self.margin_top = 0
        self.margin_left = 0
        self.margin_right = 0
        self.margin_bottom = 0
        return self

    def copy(self) -> 'Selection':
        """
        Creates a deep copy of the object.

        :return: Copied selection effect
        """
        return copy.deepcopy(self)

    def __copy__(self) -> 'Selection':
        """
        Copy method.

        :return: Copied selection
        """
        return self.copy()

    def set_color(self, color: ColorInputType) -> 'Selection':
        """
        Set the selection effect color.

        :param color: Selection color
        :return: Self reference
        """
        self.color = assert_color(color)
        return self

    def get_margin(self) -> Tuple4IntType:
        """
        Return the top, left, bottom and right margins of the selection.

        :return: Tuple of (top, left, bottom, right) margins in px
        """
        return int(self.margin_top), int(self.margin_left), \
               int(self.margin_bottom), int(self.margin_right)

    def get_xy_margin(self) -> Tuple2IntType:
        """
        Return the x/y margins of the selection.

        :return: Margin tuple on x-axis and y-axis (x, y) in px
        """
        return int(self.margin_left + self.margin_right), \
               int(self.margin_top + self.margin_bottom)

    def get_width(self) -> int:
        """
        Return the selection width as sum of left and right margins.

        :return: Width in px
        """
        _, l, _, r = self.get_margin()
        return l + r

    def get_height(self) -> int:
        """
        Return the selection height as sum of top and bottom margins.

        :return: Height in px
        """
        t, _, b, _ = self.get_margin()
        return t + b

    def inflate(
            self,
            rect: 'pygame.Rect', inflate: Optional[Tuple2IntType] = None
    ) -> 'pygame.Rect':
        """
        Grow or shrink the rectangle size according to margins.

        :param rect: Rect object
        :param inflate: Extra border inflate
        :return: Inflated rect
        """
        if inflate is None:
            inflate = (0, 0)
        assert isinstance(rect, pygame.Rect)
        return pygame.Rect(
            int(rect.x - self.margin_left - inflate[0] / 2),
            int(rect.y - self.margin_top - inflate[1] / 2),
            int(rect.width + self.margin_left + self.margin_right + inflate[0]),
            int(rect.height + self.margin_top + self.margin_bottom + inflate[1])
        )

    def draw(self, surface: 'pygame.Surface', widget: 'pygame_menu.widgets.Widget') -> 'Selection':
        """
        Draw the selection.

        :param surface: Surface to draw
        :param widget: Widget object
        :return: Self reference
        """
        raise NotImplementedError('override is mandatory')
