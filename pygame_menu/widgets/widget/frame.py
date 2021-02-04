"""
pygame-menu
https://github.com/ppizarror/pygame-menu

FRAME
Widget container.

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

__all__ = ['Frame']

import pygame
from pygame_menu.widgets.core import Widget
from pygame_menu.widgets.widget.none import NoneWidget
from pygame_menu._types import Optional, Tuple2IntType, NumberType


# noinspection PyMissingOrEmptyDocstring
class Frame(NoneWidget):
    """
    Frame is a widget container, it can pack many widgets.

    All widgets inside have a floating position. Widgets inside are placed using its
    margin + width/height. ``(0, 0)`` coordinate is the top-left position in frame.

    .. note::

        Frame does not implement any transformation.

    .. note::

        Frame does not accept padding.

    :param width: Frame width
    :param height: Frame height
    :param frame_id: ID of the frame
    """
    _width: int
    _height: int

    def __init__(self,
                 width: NumberType,
                 height: NumberType,
                 frame_id: str = ''
                 ) -> None:
        super(Frame, self).__init__(widget_id=frame_id)
        assert isinstance(width, (int, float)) and width > 0
        assert isinstance(height, (int, float)) and height > 0
        self._width = int(width)
        self._height = int(height)
        self._rect.width = self._width
        self._rect.height = self._height

    def set_margin(self, x: NumberType, y: NumberType) -> 'Widget':
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        self._margin = (x, y)
        self._force_render()
        return self

    def get_rect(self, inflate: Optional[Tuple2IntType] = None, apply_padding: bool = True,
                 use_transformed_padding: bool = True) -> 'pygame.Rect':
        return self._rect.copy()
