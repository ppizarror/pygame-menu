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

from pygame_menu.widgets.selection.arrow_selection import ArrowSelection


class RightArrowSelection(ArrowSelection):
    """
    Widget selection right arrow class.
    Creates an arrow to the right of the selected menu item.

    :param arrow_size: Size of arrow on x,y axis (width, height)
    :type arrow_size: tuple, list
    :param arrow_left_margin: Distance from the arrow to the widget
    :type arrow_left_margin: int, float
    :param arrow_vertical_offset: Vertical offset of the arrow
    :type arrow_vertical_offset: int
    :param blink_ms: Milliseconds between each blink, if *0* blinking is disabled
    :type blink_ms: int
    """

    def __init__(self, arrow_size=(10, 15), arrow_left_margin=3, arrow_vertical_offset=0, blink_ms=0):
        assert isinstance(arrow_left_margin, (int, float))
        assert arrow_left_margin >= 0, 'margin cannot be negative'
        super(RightArrowSelection, self).__init__(margin_left=0,
                                                  margin_right=arrow_size[0] + arrow_left_margin,
                                                  margin_top=0,
                                                  margin_bottom=0,
                                                  arrow_vertical_offset=arrow_vertical_offset,
                                                  blink_ms=blink_ms)
        self._arrow_left_margin = arrow_left_margin

    # noinspection PyMissingOrEmptyDocstring
    def draw(self, surface, widget):
        super(RightArrowSelection, self).draw(surface, widget)
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
        super(RightArrowSelection, self)._draw_arrow(surface, widget, a, b, c)
