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

from pygame_menu.widgets.selection.arrow_selection import ArrowSelection


class LeftArrowSelection(ArrowSelection):
    """
    Widget selection left arrow class.
    Creates an arrow to the left of the selected menu item.

    :param arrow_size: Size of arrow on x,y axis (width, height)
    :type arrow_size: tuple, list
    :param arrow_right_margin: Distance from the arrow to the widget
    :type arrow_right_margin: int, float
    """

    def __init__(self, arrow_size=(10, 15), arrow_right_margin=3):
        assert isinstance(arrow_right_margin, (int, float))
        assert arrow_right_margin >= 0, 'margin cannot be negative'
        super(LeftArrowSelection, self).__init__(margin_left=arrow_size[0] + arrow_right_margin, margin_right=0,
                                                 margin_top=0, margin_bottom=0)
        self._arrow_right_margin = arrow_right_margin

    def draw(self, surface, widget):
        """
        Draw the selection.

        :param surface: Surface to draw
        :type surface: pygame.surface.SurfaceType
        :param widget: Widget object
        :type widget: :py:class:`pygame_menu.widgets.Widget`
        :return: None
        """
        # A
        #   \B      widget
        # C /
        #    <------>
        #     margin
        a = (widget.get_rect().topleft[0] - self._arrow_size[0] - self._arrow_right_margin,
             widget.get_rect().midleft[1] - self._arrow_size[1] / 2 + self._arrow_vertical_offset)
        b = (widget.get_rect().midleft[0] - self._arrow_right_margin,
             widget.get_rect().midleft[1] + self._arrow_vertical_offset)
        c = (widget.get_rect().bottomleft[0] - self._arrow_size[0] - self._arrow_right_margin,
             widget.get_rect().midleft[1] + self._arrow_size[1] / 2 + self._arrow_vertical_offset)
        if self._blink_enabled:
            self.blink(a, b, c, surface)
        else:
            pygame.draw.polygon(surface, self.color, [a, b, c])
