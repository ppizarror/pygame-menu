"""
pygame-menu
https://github.com/ppizarror/pygame-menu

BUTTON
Button class, manage elements and adds entries to Menu.

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

__all__ = ['Button']

import pygame
import pygame_menu

from pygame_menu.controls import KEY_APPLY, JOY_BUTTON_SELECT
from pygame_menu.locals import FINGERUP
from pygame_menu.utils import is_callable, assert_color
from pygame_menu.widgets.core import Widget

from pygame_menu._types import Any, CallbackType, Callable, Union, List, Tuple, \
    Optional, ColorType, ColorInputType, EventVectorType


# noinspection PyMissingOrEmptyDocstring
class Button(Widget):
    """
    Button widget.

    The arguments and unknown keyword arguments are passed to the ``onreturn``
    function:

    .. code-block:: python

        onreturn(*args, **kwargs)

    :param title: Button title
    :param button_id: Button ID
    :param onreturn: Callback when pressing the button
    :param args: Optional arguments for callbacks
    :param kwargs: Optional keyword arguments
    """
    _last_underline: List[Union[str, Optional[Tuple[ColorType, int, int]]]]  # deco id, (color, offset, width)
    to_menu: bool

    def __init__(
            self,
            title: Any,
            button_id: str = '',
            onreturn: CallbackType = None,
            *args,
            **kwargs
    ) -> None:
        super(Button, self).__init__(
            args=args,
            kwargs=kwargs,
            onreturn=onreturn,
            title=title,
            widget_id=button_id
        )
        self._last_underline = ['', None]
        self.to_menu = False  # True if the button opens a new Menu

    def _apply_font(self) -> None:
        pass

    def set_selection_callback(
            self,
            callback: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]]
    ) -> None:
        """
        Update the button selection callback, once button is selected, the callback
        function is executed as follows:

        .. code-block:: python

            callback(selected, widget, menu)

        :param callback: Callback when selecting the widget, executed in :py:meth:`pygame_menu.widgets.core.widget.Widget.set_selected`
        :return: None
        """
        if callback is not None:
            assert is_callable(callback), \
                'callback must be callable (function-type) or None'
        self._onselect = callback

    def update_callback(self, callback: Callable, *args) -> None:
        """
        Update function triggered by the button; ``callback`` cannot point to a Menu, that
        behaviour is only valid using :py:meth:`pygame_menu.menu.Menu.add.button` method.

        .. note::

            If button points to a submenu, and the callback is changed to a
            function, the submenu will be removed from the parent Menu. Thus
            preserving the structure.

        :param callback: Function
        :param args: Arguments used by the function once triggered
        :return: None
        """
        assert is_callable(callback), \
            'only callable (function-type) are allowed'

        # If return is a Menu object, remove it from submenus list
        if self._menu is not None and self._onreturn is not None and self.to_menu:
            assert len(self._args) == 1
            submenu = self._args[0]  # Menu
            assert self._menu.in_submenu(submenu), \
                'pointed menu is not in submenu list of parent container'
            # noinspection PyProtectedMember
            assert self._menu._remove_submenu(submenu), \
                'submenu could not be removed'
            self.to_menu = False

        self._args = args or []
        self._onreturn = callback

    def add_underline(
            self,
            color: ColorInputType,
            offset: int,
            width: int,
            force_render: bool = False
    ) -> 'Button':
        """
        Adds a underline to text. This is added if widget is rendered.

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

    def remove_underline(self) -> 'Button':
        """
        Remove underline of the button.

        :return: Self reference
        """
        if self._last_underline[0] != '':
            self._decorator.remove(self._last_underline[0])
            self._last_underline[0] = ''
        return self

    def _draw(self, surface: 'pygame.Surface') -> None:
        surface.blit(self._surface, self._rect.topleft)

    def _render(self) -> Optional[bool]:
        if not self._render_hash_changed(
                self._selected, self._title, self._visible, self.readonly,
                self._last_underline[1]):
            return True

        # Render surface
        self._surface = self._render_string(self._title, self.get_font_color_status())
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
        self.apply_update_callbacks(events)

        if self.readonly or not self.is_visible():
            return False
        updated = False
        rect = self.get_rect(to_real_position=True)

        for event in events:

            # Check mouse over
            self._check_mouseover(event, rect)

            # User applies with key
            if event.type == pygame.KEYDOWN and self._keyboard_enabled and \
                    event.key == KEY_APPLY or \
                    event.type == pygame.JOYBUTTONDOWN and self._joystick_enabled and \
                    event.button == JOY_BUTTON_SELECT:
                if self.to_menu:
                    self._sound.play_open_menu()
                else:
                    self._sound.play_key_add()
                self.apply()
                updated = True

            # User clicks the button; don't consider the mouse wheel (button 4 & 5)
            elif event.type == pygame.MOUSEBUTTONUP and self._mouse_enabled and \
                    event.button in (1, 2, 3):
                self._sound.play_click_mouse()
                if rect.collidepoint(*event.pos):
                    self.apply()
                    updated = True

            # User touches the button
            elif event.type == FINGERUP and self._touchscreen_enabled and self._menu is not None:
                self._sound.play_click_mouse()
                window_size = self._menu.get_window_size()
                finger_pos = (event.x * window_size[0], event.y * window_size[1])
                if rect.collidepoint(*finger_pos):
                    self.apply()
                    updated = True

        return updated
