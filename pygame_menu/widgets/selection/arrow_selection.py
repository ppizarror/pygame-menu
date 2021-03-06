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

__all__ = ['ArrowSelection']

import pygame
import pygame_menu

from pygame_menu.utils import assert_vector
from pygame_menu.widgets.core import Selection

from pygame_menu._types import NumberType, Tuple2IntType, Optional, NumberInstance

SELECTOR_CLOCK = pygame.time.Clock()


class ArrowSelection(Selection):
    """
    Widget selection arrow class.
    Parent class for left and right arrow selection classes.

    :param margin_left: Left margin
    :param margin_right: Right margin
    :param margin_top: Top margin
    :param margin_bottom: Bottom margin
    :param arrow_size: Size of arrow on x-axis and y-axis (width, height) in px
    :param arrow_vertical_offset: Vertical offset of the arrow
    :param blink_ms: Milliseconds between each blink, if ``0`` blinking is disabled
    """
    _arrow_vertical_offset: int
    _arrow_size: Tuple2IntType
    _blink_ms: NumberType
    _blink_time: NumberType
    _blink_status: bool
    _last_widget: Optional['pygame_menu.widgets.Widget']

    def __init__(self, margin_left: NumberType, margin_right: NumberType, margin_top: NumberType,
                 margin_bottom: NumberType, arrow_size: Tuple2IntType = (10, 15),
                 arrow_vertical_offset: NumberType = 0, blink_ms: NumberType = 0) -> None:
        super(ArrowSelection, self).__init__(
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            margin_bottom=margin_bottom
        )

        assert_vector(arrow_size, 2, int)
        assert isinstance(arrow_vertical_offset, NumberInstance)
        assert isinstance(blink_ms, int)
        assert arrow_size[0] > 0 and arrow_size[1] > 0, 'arrow size must be greater than zero'
        assert blink_ms >= 0, 'blinking milliseconds must be greater than or equal to zero'

        self._arrow_vertical_offset = int(arrow_vertical_offset)
        self._arrow_size = (arrow_size[0], arrow_size[1])
        self._blink_ms = blink_ms
        self._blink_time = 0
        self._blink_status = True
        self._last_widget = None

    # noinspection PyMissingOrEmptyDocstring
    def draw(self, surface: 'pygame.Surface', widget: 'pygame_menu.widgets.Widget') -> 'Selection':
        raise NotImplementedError('override is mandatory')

    def _draw_arrow(self, surface: 'pygame.Surface', widget: 'pygame_menu.widgets.Widget',
                    a: Tuple2IntType, b: Tuple2IntType, c: Tuple2IntType) -> None:
        """
        Draw the selection arrow.

        :param surface: Surface to draw
        :param widget: Widget object
        :param a: Arrow coord A
        :param b: Arrow coord B
        :param c: Arrow coord C
        :return: None
        """
        SELECTOR_CLOCK.tick(60)  # As blink is in ms
        self._blink_time += SELECTOR_CLOCK.get_time()

        # Switch the blinking if the time exceeded or the widget has changed
        if self._blink_ms != 0 and (self._blink_time > self._blink_ms or self._last_widget != widget):
            self._blink_status = not self._blink_status or self._last_widget != widget
            self._blink_time = 0
            self._last_widget = widget

        # Draw the arrow only if blinking is enabled
        if self._blink_status:
            pygame.draw.polygon(surface, self.color, [a, b, c])
