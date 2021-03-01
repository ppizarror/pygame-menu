"""
pygame-menu
https://github.com/ppizarror/pygame-menu

LABEL
Label class, adds a simple text to the Menu.

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

__all__ = ['Label']

import pygame

from pygame_menu.utils import assert_color
from pygame_menu.widgets.core import Widget

from pygame_menu._types import Any, CallbackType, List, Union, Tuple, Optional, ColorType, \
    ColorInputType, EventVectorType


# noinspection PyMissingOrEmptyDocstring
class Label(Widget):
    """
    Label widget.

    :param title: Label title/text
    :param label_id: Label ID
    :param onselect: Function when selecting the label widget
    """
    _last_underline: List[Union[str, Optional[Tuple[ColorType, int, int]]]]  # deco id, (color, offset, width)

    def __init__(
            self,
            title: Any,
            label_id: str = '',
            onselect: CallbackType = None,
    ) -> None:
        super(Label, self).__init__(
            title=title,
            onselect=onselect,
            widget_id=label_id
        )
        self._last_underline = ['', None]

    def add_underline(
            self,
            color: ColorInputType,
            offset: int,
            width: int,
            force_render: bool = False
    ) -> 'Label':
        """
        Adds a underline to text. This is added if widget is rendered

        :param color: Underline color
        :param offset: Underline offset
        :param width: Underline width
        :param force_render: If ``True`` force widget render after addition
        :return: Self reference
        """
        color = assert_color(color)
        assert isinstance(offset, int)
        assert isinstance(width, int) and width > 0
        self._last_underline[1] = (color, offset, width)
        if force_render:
            self._force_render()
        return self

    def remove_underline(self) -> 'Label':
        """
        Remove underline of the label.

        :return: Self reference
        """
        if self._last_underline[0] != '':
            self._decorator.remove(self._last_underline[0])
            self._last_underline[0] = ''
        return self

    def _apply_font(self) -> None:
        pass

    def _draw(self, surface: 'pygame.Surface') -> None:
        if self._title == '':  # The minimal width of any surface is 1px, so the background will be a line
            return
        surface.blit(self._surface, self._rect.topleft)

    def _render(self) -> Optional[bool]:
        if not self._render_hash_changed(self._title, self._font_color, self._visible, self._last_underline[1]):
            return True

        # Render surface
        self._surface = self._render_string(self._title, self._font_color)
        self._apply_transforms()
        self._rect.width, self._rect.height = self._surface.get_size()

        # Add underline if enabled
        self.remove_underline()
        if self._last_underline[1] is not None:
            w = self._surface.get_width()
            h = self._surface.get_height()
            color, offset, width = self._last_underline[1]
            if w > 0 and h > 0:
                self._last_underline[0] = self._decorator.add_line(
                    pos1=(-w / 2, h / 2 + offset),
                    pos2=(w / 2, h / 2 + offset),
                    color=color,
                    width=width
                )

        self.force_menu_surface_update()

    def update(self, events: EventVectorType) -> bool:
        for event in events:
            if self._check_mouseover(event):
                break
        return False
