"""
pygame-menu
https://github.com/ppizarror/pygame-menu

HORIZONTAL MARGIN
Horizontal box margin.

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

__all__ = ['HMargin']

import pygame

from pygame_menu.widgets.widget.none import NoneWidget

from pygame_menu._types import NumberType


# noinspection PyMissingOrEmptyDocstring
class HMargin(NoneWidget):
    """
    Horizontal margin widget.

    .. note::

        This widget does not implement any transformation.

    :param margin: Horizontal margin in px
    :param widget_id: ID of the widget
    """

    def __init__(
            self,
            margin: NumberType,
            widget_id: str = ''
    ) -> None:
        super(HMargin, self).__init__(widget_id=widget_id)
        self._rect.width = int(margin)
        self._rect.height = 0

    def get_rect(self, *args, **kwargs) -> 'pygame.Rect':
        return self._rect.copy()
