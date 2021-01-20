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
from pygame_menu.custom_types import PaddingType, ColorType, Tuple2IntType, Optional, NumberType, Union, List, \
    TYPE_CHECKING, Dict, Any, Tuple, CallbackType

if TYPE_CHECKING:
    from pygame_menu.baseimage import BaseImage
    from pygame_menu.sound import Sound
    from pygame_menu.widgets.core.selection import Selection


# noinspection PyMissingOrEmptyDocstring
class NoneWidget(Widget):
    """
    None widget. Usefull if used for filling column/row layout.

    .. note::

        This widget does not implement any transformation.

    :param widget_id: ID of the widget
    """

    def __init__(self, widget_id: str = '') -> None:
        super(NoneWidget, self).__init__(widget_id=widget_id)
        self.is_selectable = False
        self._surface = make_surface(0, 0, alpha=True)

    def _apply_font(self) -> None:
        pass

    def set_padding(self, padding: PaddingType) -> None:
        pass

    def set_title(self, title: str) -> None:
        pass

    def get_rect(self, inflate: Optional[Tuple2IntType] = None, apply_padding: bool = True,
                 use_transformed_padding: bool = True) -> 'pygame.Rect':
        return pygame.Rect(0, 0, 0, 0)

    def set_background_color(self, color: Optional[Union[ColorType, 'BaseImage']],
                             inflate: Optional[Tuple2IntType] = (0, 0)) -> None:
        pass

    def _draw_background_color(self, surface: 'pygame.Surface') -> None:
        pass

    def set_selection_effect(self, selection: 'Selection') -> None:
        pass

    def apply(self, *args) -> None:
        pass

    def change(self, *args) -> None:
        pass

    def draw(self, surface: 'pygame.Surface') -> None:
        self.apply_draw_callbacks()

    def _render(self) -> Optional[bool]:
        pass

    def draw_selection(self, surface: pygame.Surface) -> None:
        pass

    def set_margin(self, x: int, y: int) -> None:
        pass

    def _apply_transforms(self) -> None:
        pass

    def set_font(self,
                 font: str,
                 font_size: int,
                 color: ColorType,
                 selected_color: ColorType,
                 readonly_color: ColorType,
                 readonly_selected_color: ColorType,
                 background_color: Optional[ColorType],
                 antialias: bool = True
                 ) -> None:
        pass

    def update_font(self, style: Dict[str, Any]) -> None:
        pass

    def set_position(self, posx: int, posy: int) -> None:
        pass

    def flip(self, x: bool, y: bool) -> None:
        pass

    def set_max_width(self, width: Optional[NumberType], scale_height: NumberType = False,
                      smooth: bool = True) -> None:
        pass

    def set_max_height(self, height: Optional[NumberType], scale_width: NumberType = False,
                       smooth: bool = True) -> None:
        pass

    def scale(self, width: NumberType, height: NumberType, smooth: bool = False) -> None:
        pass

    def resize(self, width: NumberType, height: NumberType, smooth: bool = False) -> None:
        pass

    def translate(self, x: int, y: int) -> None:
        pass

    def rotate(self, angle: NumberType) -> None:
        pass

    def set_alignment(self, align: str) -> None:
        pass

    def select(self, select: bool = True, update_menu: bool = False) -> None:
        pass

    def set_shadow(self, enabled: bool = True, color: bool = None, position=None, offset=None) -> None:
        pass

    def set_sound(self, sound: 'Sound') -> None:
        pass

    def set_controls(self, joystick: bool = True, mouse: bool = True, touchscreen: bool = True) -> None:
        pass

    def set_value(self, value: Any) -> None:
        pass

    def update(self, events: Union[List['pygame.event.Event'], Tuple['pygame.event.Event']]) -> bool:
        return False

    def add_update_callback(self, update_callback: CallbackType) -> None:
        pass

    def remove_update_callback(self, callback_id: str) -> None:
        pass

    def apply_update_callbacks(self) -> None:
        pass

    def set_border(self, width: int, color: ColorType, inflate: Tuple2IntType) -> None:
        pass
