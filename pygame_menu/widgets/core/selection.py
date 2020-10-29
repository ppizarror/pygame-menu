# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SELECTION
Widget selection class.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2020 Pablo Pizarro R. @ppizarror

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

import pygame
from pygame_menu.utils import assert_color


class Selection(object):
    """
    Widget selection class.

    :param margin_left: Left margin
    :type margin_left: int, float
    :param margin_right: Right margin
    :type margin_right: int, float
    :param margin_top: Top margin
    :type margin_top: int, float
    :param margin_bottom: Bottom margin
    :type margin_bottom: int, float
    """

    def __init__(self, margin_left, margin_right, margin_top, margin_bottom):
        assert margin_left >= 0, 'left margin of widget cannot be negative'
        assert margin_right >= 0, 'right margin of widget cannot be negative'
        assert margin_top >= 0, 'top margin of widget cannot be negative'
        assert margin_bottom >= 0, 'bottom margin of widget cannot be negative'
        self.color = (0, 0, 0)
        self.margin_bottom = margin_bottom
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.margin_top = margin_top

    def set_color(self, color):
        """
        Set the selection color.

        :param color: Selection color
        :type color: tuple, list
        :return: None
        """
        assert_color(color)
        self.color = color

    def get_margin(self):
        """
        Return the top, left, bottom and right margins of the selection.

        :return: Tuple of (t,l,b,r) margins in px
        :rtype: tuple, list
        """
        return self.margin_top, self.margin_left, self.margin_bottom, self.margin_right

    def get_width(self):
        """
        Return the selection width (px) as sum of left and right margins.

        :return: Width in px
        :rtype: int, float
        """
        _, l, _, r = self.get_margin()
        return l + r

    def inflate(self, rect):
        """
        Grow or shrink the rectangle size according to margins.

        :param rect: rectangle
        :type rect: :py:class:`pygame.Rect`
        :return: Inflated rect
        :rtype: :py:class:`pygame.Rect`
        """
        assert isinstance(rect, pygame.Rect)
        return pygame.Rect(int(rect.x - self.margin_left),
                           int(rect.y - self.margin_top),
                           int(rect.width + self.margin_left + self.margin_right),
                           int(rect.height + self.margin_top + self.margin_bottom))

    def get_height(self):
        """
        Return the selection height (px) as sum of top and bottom margins.

        :return: Height in px
        :rtype: int, float
        """
        t, _, b, _ = self.get_height()
        return t + b

    def draw(self, surface, widget):
        """
        Draw the selection.

        :param surface: Surface to draw
        :type surface: :py:class:`pygame.Surface`
        :param widget: Widget object
        :type widget: :py:class:`pygame_menu.widgets.core.Widget`
        :return: None
        """
        raise NotImplementedError('override is mandatory')
