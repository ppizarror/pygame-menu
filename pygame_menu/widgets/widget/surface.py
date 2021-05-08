"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SURFACE
Surface widget. This widget contains an external surface.

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

__all__ = ['SurfaceWidget']

import pygame

from pygame_menu.widgets import Widget

from pygame_menu._types import NumberType, CallbackType, Optional, EventVectorType


# noinspection PyMissingOrEmptyDocstring
class SurfaceWidget(Widget):
    """
    Surface widget. Implements a widget from a external surface.

    .. note::

        This class only implements translation transformation.

    :param surface: Pygame surface object
    :param surface_id: Surface ID
    :param onselect: Function when selecting the widget
    """
    _surface_obj: 'pygame.Surface'

    def __init__(
            self,
            surface: 'pygame.Surface',
            surface_id: str = '',
            onselect: CallbackType = None
    ) -> None:
        assert isinstance(surface, pygame.Surface)
        assert isinstance(surface_id, str)

        super(SurfaceWidget, self).__init__(
            onselect=onselect,
            widget_id=surface_id
        )
        self._surface_obj = surface

    def set_title(self, title: str) -> 'SurfaceWidget':
        return self

    def set_surface(self, surface: 'pygame.Surface') -> 'SurfaceWidget':
        """
        Update the widget surface.
        
        :param surface: New surface
        :return: Self reference
        """
        assert isinstance(surface, pygame.Surface)
        self._surface_obj = surface
        self._render()
        self.force_menu_surface_update()
        return self

    def _apply_font(self) -> None:
        pass

    def rotate(self, angle: NumberType) -> 'SurfaceWidget':
        return self

    def flip(self, x: bool, y: bool) -> 'SurfaceWidget':
        return self

    def scale(self, width: NumberType, height: NumberType, smooth: bool = False) -> 'SurfaceWidget':
        return self

    def resize(self, width: NumberType, height: NumberType, smooth: bool = False) -> 'SurfaceWidget':
        return self

    def set_max_width(self, *args, **kwargs) -> 'SurfaceWidget':
        return self

    def set_max_height(self, *args, **kwargs) -> 'SurfaceWidget':
        return self

    def _draw(self, surface: 'pygame.Surface') -> None:
        surface.blit(self._surface_obj, self._rect.topleft)

    def get_surface(self) -> 'pygame.Surface':
        return self._surface_obj

    def _render(self) -> Optional[bool]:
        self._rect.width, self._rect.height = self._surface_obj.get_size()
        return

    def update(self, events: EventVectorType) -> bool:
        self.apply_update_callbacks(events)
        for event in events:
            if self._check_mouseover(event):
                break
        return False
