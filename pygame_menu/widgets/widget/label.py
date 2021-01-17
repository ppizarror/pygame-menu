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
from pygame_menu.widgets.core import Widget
from pygame_menu.custom_types import Any, CallbackType, List, Union, Tuple, Optional


# noinspection PyMissingOrEmptyDocstring
class Label(Widget):
    """
    Label widget.

    :param title: Label title/text
    :param label_id: Label ID
    :param onselect: Function when selecting the widget
    """

    def __init__(self,
                 title: Any,
                 label_id: str = '',
                 onselect: CallbackType = None,
                 ) -> None:
        super(Label, self).__init__(
            title=title,
            onselect=onselect,
            widget_id=label_id
        )

    def _apply_font(self) -> None:
        pass

    def draw(self, surface: 'pygame.Surface') -> None:
        self._render()
        if self._title == '':  # The minimal width of any surface is 1px, so the background will be a line
            return
        self._fill_background_color(surface)
        surface.blit(self._surface, self._rect.topleft)
        self.apply_draw_callbacks()

    def _render(self) -> Optional[bool]:
        if not self._render_hash_changed(self._title, self._font_color, self.visible):
            return True
        self._surface = self._render_string(self._title, self._font_color)
        self._apply_transforms()
        self._rect.width, self._rect.height = self._surface.get_size()
        self._menu_surface_needs_update = True  # Force Menu update

    def update(self, events: Union[List['pygame.event.Event'], Tuple['pygame.event.Event']]) -> bool:
        return False
