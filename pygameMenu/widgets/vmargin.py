# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

VERTICAL MARGIN
Vertical box margin.

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

from pygameMenu.widgets.widget import Widget, make_surface


class VMargin(Widget):
    """
    Vertical margin widget.
    """

    def __init__(self):
        super(VMargin, self).__init__()
        self.is_selectable = False

    def _apply_font(self):
        self._font_size = 0
        self._shadow = False

    # noinspection PyMissingOrEmptyDocstring
    def draw(self, surface):
        if self._surface is None:
            self._render()
        surface.blit(self._surface, self._rect.topleft)

    # noinspection PyMissingOrEmptyDocstring
    def draw_selected_rect(self, surface, selected_color, inflatex, inflatey, border_width):
        pass  # Nothing to select

    def _render(self):
        self._surface = make_surface(1, 1, alpha=True)
        self._rect.width = 0
        self._rect.height = 0

    # noinspection PyMissingOrEmptyDocstring
    def update(self, events):
        return False
