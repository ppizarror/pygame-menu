"""
pygame-menu
https://github.com/ppizarror/pygame-menu

NONE WIDGET
None widget definition.

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

__all__ = ['NoneWidget']

import pygame

from pygame_menu.utils import make_surface
from pygame_menu.widgets.core import Widget

from pygame_menu._types import Optional, NumberType


# noinspection PyMissingOrEmptyDocstring
class NoneWidget(Widget):
    """
    None widget. Useful if used for filling column/row layout. None widget don't
    accept padding, margin, cannot be selected or updated.

    .. note::

        This widget does not implement any transformation.

    :param widget_id: ID of the widget
    """

    def __init__(
            self,
            widget_id: str = ''
    ) -> None:
        super(NoneWidget, self).__init__(widget_id=widget_id)
        self.is_selectable = False
        self._surface = make_surface(0, 0, alpha=True)

    def _apply_font(self) -> None:
        pass

    def set_padding(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def get_selected_time(self) -> NumberType:
        return 0

    def set_title(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def get_rect(self, *args, **kwargs) -> 'pygame.Rect':
        return pygame.Rect(0, 0, 0, 0)

    def set_background_color(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def _draw_background_color(self, *args, **kwargs) -> None:
        pass

    def _draw_border(self, *args, **kwargs) -> None:
        pass

    def set_selection_effect(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def apply(self, *args) -> None:
        pass

    def change(self, *args) -> None:
        pass

    def _draw(self, *args, **kwargs) -> None:
        pass

    def _render(self, *args, **kwargs) -> Optional[bool]:
        pass

    def set_margin(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def _apply_transforms(self, *args, **kwargs) -> None:
        pass

    def set_font(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def update_font(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def set_position(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def flip(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def set_max_width(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def set_max_height(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def scale(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def resize(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def translate(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def rotate(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def set_alignment(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def select(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def set_font_shadow(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def set_sound(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def set_cursor(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def set_controls(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def set_value(self, *args, **kwargs) -> None:
        pass

    def add_update_callback(self, *args, **kwargs) -> None:
        pass

    def remove_update_callback(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def apply_update_callbacks(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def set_border(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def _check_mouseover(self, *args, **kwargs) -> bool:
        self._mouseover = False
        return False

    def mouseleave(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def mouseover(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def set_onchange(self, *args, **kwargs) -> 'NoneWidget':
        self._onchange = None
        return self

    def set_onreturn(self, *args, **kwargs) -> 'NoneWidget':
        self._onreturn = None
        return self

    def set_onmouseleave(self, *args, **kwargs) -> 'NoneWidget':
        self._onmouseleave = None
        return self

    def set_onmouseover(self, *args, **kwargs) -> 'NoneWidget':
        self._onmouseover = None
        return self

    def set_onselect(self, *args, **kwargs) -> 'NoneWidget':
        self._onselect = None
        return self

    def set_tab_size(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def set_default_value(self, *args, **kwargs) -> 'NoneWidget':
        return self

    def update(self, *args, **kwargs) -> bool:
        return False
