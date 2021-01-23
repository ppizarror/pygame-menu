"""
pygame-menu
https://github.com/ppizarror/pygame-menu

VERTICAL MARGIN
Vertical box margin.

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

__all__ = ['VMargin']

from pygame_menu.widgets.core import Widget
from pygame_menu.widgets.widget.none import NoneWidget


# noinspection PyMissingOrEmptyDocstring
class VMargin(NoneWidget):
    """
    Vertical margin widget.

    .. note::

        This widget does not implement any transformation.

    :param widget_id: ID of the widget
    """

    def __init__(self, widget_id: str = '') -> None:
        super(VMargin, self).__init__(widget_id=widget_id)

    def set_margin(self, x: int, y: int) -> 'Widget':
        self._margin = (x, y)
        return self
