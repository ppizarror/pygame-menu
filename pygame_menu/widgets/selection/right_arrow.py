"""
pygame-menu
https://github.com/ppizarror/pygame-menu

RIGHT ARROW CLASS
Selector with a right arrow on the item.

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

__all__ = ['RightArrowSelection']

import pygame
import pygame_menu

from pygame_menu.widgets.core import Selection
from pygame_menu.widgets.selection.arrow_selection import ArrowSelection

from pygame_menu._types import Tuple2IntType, NumberType, NumberInstance


class RightArrowSelection(ArrowSelection):
    """
    Widget selection right arrow class. Creates an arrow to the right of the
    selected Menu item.

    :param arrow_size: Size of arrow on x-axis and y-axis (width, height) in px
    :param arrow_left_margin: Distance from the arrow to the widget
    :param arrow_vertical_offset: Vertical offset of the arrow
    :param blink_ms: Milliseconds between each blink, if ``0`` blinking is disabled
    """
    _arrow_left_margin: int

    def __init__(
            self,
            arrow_size: Tuple2IntType = (10, 15),
            arrow_left_margin: int = 3,
            arrow_vertical_offset: int = 0,
            blink_ms: NumberType = 0
    ) -> None:
        assert isinstance(arrow_left_margin, NumberInstance)
        assert arrow_left_margin >= 0, 'margin cannot be negative'
        super(RightArrowSelection, self).__init__(
            margin_left=0,
            margin_right=arrow_size[0] + arrow_left_margin,
            margin_top=0,
            margin_bottom=0,
            arrow_vertical_offset=arrow_vertical_offset,
            blink_ms=blink_ms
        )
        self._arrow_left_margin = arrow_left_margin

    # noinspection PyMissingOrEmptyDocstring
    def draw(self, surface: 'pygame.Surface', widget: 'pygame_menu.widgets.Widget') -> 'Selection':
        #                 /A
        # widget        B
        #                \ C
        #       <------>
        #        margin
        rect = widget.get_rect()
        a = (rect.topright[0] + self._arrow_size[0] + self._arrow_left_margin,
             int(rect.midright[1] - self._arrow_size[1] / 2 + self._arrow_vertical_offset))
        b = (rect.midright[0] + self._arrow_left_margin,
             rect.midright[1] + self._arrow_vertical_offset)
        c = (rect.bottomright[0] + self._arrow_size[0] + self._arrow_left_margin,
             int(rect.midright[1] + self._arrow_size[1] / 2 + self._arrow_vertical_offset))
        super(RightArrowSelection, self)._draw_arrow(surface, widget, a, b, c)
        return self
