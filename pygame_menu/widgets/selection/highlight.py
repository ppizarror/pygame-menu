# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

HIGHLIGHT
Widget selection highlight box effect.

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


class HighlightSelection(Selection):
    """
    Widget selection highlight class.

    :param border_width: Border width of the highlight box
    :type border_width: int
    :param margin_x: X margin of selected highlight box
    :type margin_x: int, float
    :param margin_y: X margin of selected highlight box
    :type margin_y: int, float
    """

    def __init__(self,
                 border_width=1,
                 margin_x=16.0,
                 margin_y=8.0,
                 ):
        assert isinstance(border_width, int)
        assert margin_x >= 0 and margin_y >= 0
        assert border_width >= 0
        margin_x = float(margin_x)
        margin_y = float(margin_y)
        super(HighlightSelection, self).__init__(margin_left=margin_x / 2 + border_width,
                                                 margin_right=margin_x / 2 + border_width,
                                                 margin_top=margin_y / 2 + border_width,
                                                 margin_bottom=margin_y / 2 + border_width)
        self._border_width = border_width

    # noinspection PyMissingOrEmptyDocstring
    def draw(self, surface, widget):
        pygame.draw.rect(surface,
                         self.color,
                         self.inflate(widget.get_rect()),
                         self._border_width)
