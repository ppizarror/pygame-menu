"""
pygame-menu
https://github.com/ppizarror/pygame-menu

LEFT ARROW CLASS
Selector with a left arrow on the item.

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

__all__ = ['LeftArrowSelection']

import pygame
import pygame_menu

from pygame_menu.widgets.core import Selection
from pygame_menu.widgets.selection.arrow_selection import ArrowSelection

from pygame_menu._types import Tuple2IntType, NumberType, NumberInstance


class LeftArrowSelection(ArrowSelection):
    """
    Widget selection left arrow class.
    Creates an arrow to the left of the selected Menu item.

    :param arrow_size: Size of arrow on x-axis and y-axis (width, height) in px
    :param arrow_right_margin: Distance from the arrow to the widget
    :param arrow_vertical_offset: Vertical offset of the arrow
    :param blink_ms: Milliseconds between each blink, if ``0`` blinking is disabled
    """
    _arrow_right_margin: int

    def __init__(
            self,
            arrow_size: Tuple2IntType = (10, 15),
            arrow_right_margin: int = 5,
            arrow_vertical_offset: int = 0,
            blink_ms: NumberType = 0
    ) -> None:
        assert isinstance(arrow_right_margin, NumberInstance)
        assert arrow_right_margin >= 0, 'margin cannot be negative'
        super(LeftArrowSelection, self).__init__(
            margin_left=arrow_size[0] + arrow_right_margin,
            margin_right=0,
            margin_top=0,
            margin_bottom=0,
            arrow_vertical_offset=arrow_vertical_offset,
            blink_ms=blink_ms
        )
        self._arrow_right_margin = arrow_right_margin

    # noinspection PyMissingOrEmptyDocstring
    def draw(self, surface: 'pygame.Surface', widget: 'pygame_menu.widgets.Widget') -> 'Selection':
        # A
        #   \B        widget
        # C /
        #     <------>
        #      margin
        rect = widget.get_rect()
        a = (rect.topleft[0] - self._arrow_size[0] - self._arrow_right_margin,
             int(rect.midleft[1] - self._arrow_size[1] / 2 + self._arrow_vertical_offset))
        b = (rect.midleft[0] - self._arrow_right_margin,
             rect.midleft[1] + self._arrow_vertical_offset)
        c = (rect.bottomleft[0] - self._arrow_size[0] - self._arrow_right_margin,
             int(rect.midleft[1] + self._arrow_size[1] / 2 + self._arrow_vertical_offset))
        super(LeftArrowSelection, self)._draw_arrow(surface, widget, a, b, c)
        return self
