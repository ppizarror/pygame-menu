# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

LEFT ARROW CLASS
Selector with a left arrow on the item.

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

from pygame_menu.utils import assert_vector2
from pygame_menu.widgets import Selection

SELECTOR_CLOCK = pygame.time.Clock()


class ArrowSelection(Selection):
    """
    Widget selection arrow class.
    Parent class for left and right arrow selection classes.

    :param arrow_size: Size of arrow on x,y axis (width, height)
    :type arrow_size: tuple, list
    :param arrow_vertical_offset: Vertical offset of the arrow
    :type arrow_vertical_offset: int
    """

    def __init__(self, margin_left, margin_right, margin_top, margin_bottom, arrow_size=(10, 15),
                 arrow_vertical_offset=0, blink_ms=295):
        super().__init__(margin_left, margin_right, margin_top, margin_bottom)
        assert_vector2(arrow_size)
        assert isinstance(arrow_vertical_offset, (int, float))
        assert arrow_size[0] > 0 and arrow_size[1] > 0, 'arrow size must be greater than zero'
        self._arrow_vertical_offset = arrow_vertical_offset
        self._arrow_size = (arrow_size[0], arrow_size[1])  # type: tuple
        self._blink_ms = blink_ms
        self._blink_time = 0
        self._blink_status = True
        self._blink_enabled = True

    def draw(self, surface, widget):
        """
        Draw the selection.

        :param surface: Surface to draw
        :type surface: pygame.surface.SurfaceType
        :param widget: Widget object
        :type widget: :py:class:`pygame_menu.widgets.Widget`
        :return: None
        """
        ...

    def blink(self, a, b, c, surface):
        SELECTOR_CLOCK.tick()
        self._blink_time += SELECTOR_CLOCK.get_time()
        if self._blink_ms != 0 and self._blink_time > self._blink_ms:
            self._blink_status = not self._blink_status
            self._blink_time = 0  # Reset!!!
        if self._blink_status:
            pygame.draw.polygon(surface, self.color, [a, b, c])
