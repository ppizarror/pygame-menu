# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

RIGHT ARROW CLASS
Selector with a right arrow on the item.

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
from pygame_menu.widgets.core.selection import Selection
from pygame_menu.utils import assert_vector2


class RightArrowSelection(Selection):
    """
    Widget selection right arrow class.
    Creates an arrow to the right of the selected menu item.

    :param arrow_size: Size of arrow on x,y axis (width, height)
    :type arrow_size: tuple, list
    :param arrow_left_margin: Distance from the arrow to the widget
    :type arrow_left_margin: int, float
    :param arrow_vertical_offset: Vertical offset of the arrow
    :type arrow_vertical_offset: int
    """

    def __init__(self, arrow_size=(10, 15), arrow_left_margin=3, arrow_vertical_offset=0):
        assert_vector2(arrow_size)
        assert isinstance(arrow_left_margin, (int, float))
        assert isinstance(arrow_vertical_offset, (int, float))
        assert arrow_left_margin >= 0, 'margin cannot be negative'
        assert arrow_size[0] > 0 and arrow_size[1] > 0, 'arrow size must be greater than zero'

        super(RightArrowSelection, self).__init__(margin_left=0, margin_right=arrow_size[0] + arrow_left_margin,
                                                  margin_top=0, margin_bottom=0)

        self._arrow_size = (arrow_size[0], arrow_size[1])  # type: tuple
        self._arrow_left_margin = arrow_left_margin
        self._arrow_vertical_offset = arrow_vertical_offset

    def draw(self, surface, widget):
        """
        Draw the selection.

        :param surface: Surface to draw
        :type surface: pygame.surface.SurfaceType
        :param widget: Widget object
        :type widget: :py:class:`pygame_menu.widgets.Widget`
        :return: None
        """
        #                 /A
        # widget        B
        #                \ C
        #       <------>
        #        margin
        a = (widget.get_rect().topright[0] + self._arrow_size[0] + self._arrow_left_margin,
             widget.get_rect().midright[1] - self._arrow_size[1] / 2 + self._arrow_vertical_offset)
        b = (widget.get_rect().midright[0] + self._arrow_left_margin,
             widget.get_rect().midright[1] + self._arrow_vertical_offset)
        c = (widget.get_rect().bottomright[0] + self._arrow_size[0] + self._arrow_left_margin,
             widget.get_rect().midright[1] + self._arrow_size[1] / 2 + self._arrow_vertical_offset)
        pygame.draw.polygon(surface, self.color, [a, b, c])
