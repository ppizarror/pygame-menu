# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

BUTTON
Button class, manage elements and adds entries to menu.

NOTE: pygame-menu v3 will not provide new widgets or functionalities, consider
upgrading to the latest version.

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

from pygame_menu.utils import is_callable
from pygame_menu.widgets.core import Widget
import pygame
import pygame_menu.controls as _controls


class Button(Widget):
    """
    Button widget.

    :param title: Button title
    :type title: str
    :param button_id: Button ID
    :type button_id: str
    :param onreturn: Callback when pressing the button
    :type onreturn: callable, None
    :param args: Optional arguments for callbacks
    :type args: any
    :param kwargs: Optional keyword arguments
    :type kwargs: dict, any
    """

    def __init__(self,
                 title,
                 button_id='',
                 onreturn=None,
                 *args,
                 **kwargs
                 ):
        super(Button, self).__init__(
            title=title,
            widget_id=button_id,
            onreturn=onreturn,
            args=args,
            kwargs=kwargs
        )
        self.to_menu = False  # True if the button opens a new menu

    def _apply_font(self):
        pass

    def update_callback(self, callback, *args):
        """
        Update function triggered by the button; ``callback`` cannot point to a Menu, that behaviour
        is only valid using ``Menu.add_button()`` method.

        .. note::

            If button points to a submenu, and the callback is changed to a function,
            the submenu will be removed from the parent menu. Thus preserving the structure.

        :param callback: Function
        :type callback: callable
        :param args: Arguments used by the function once triggered
        :type args: any
        :return: None
        """
        assert is_callable(callback), 'only function are allowed'

        # If return is a Menu object, remove it from submenus list
        if self._menu is not None and self._on_return is not None and self.to_menu:
            assert len(self._args) == 1
            submenu = self._args[0]  # Menu
            assert self._menu.in_submenu(submenu, recursive=False), \
                'pointed menu is not in submenu list of parent container'
            # noinspection PyProtectedMember
            assert self._menu._remove_submenu(submenu, recursive=False), 'submenu could not be removed'
            self.to_menu = False

        self._args = args or []  # type: list
        self._on_return = callback

    # noinspection PyMissingOrEmptyDocstring
    def draw(self, surface):
        self._render()
        self._fill_background_color(surface)
        surface.blit(self._surface, self._rect.topleft)

    def _render(self):
        if not self._render_hash_changed(self.selected, self._title, self.visible):
            return True
        if self.selected:
            color = self._font_selected_color
        else:
            color = self._font_color
        self._surface = self._render_string(self._title, color)
        self._apply_surface_transforms()
        self._rect.width, self._rect.height = self._surface.get_size()
        self._menu_surface_needs_update = True  # Force menu update

    # noinspection PyMissingOrEmptyDocstring
    def update(self, events):
        updated = False
        rect = self.get_rect()  # Padding increases the extents of the button

        for event in events:  # type: pygame.event.Event

            if event.type == pygame.KEYDOWN and event.key == _controls.KEY_APPLY or \
                    self.joystick_enabled and event.type == pygame.JOYBUTTONDOWN and \
                    event.button == _controls.JOY_BUTTON_SELECT:
                self.sound.play_open_menu()
                self.apply()
                updated = True

            elif self.mouse_enabled and event.type == pygame.MOUSEBUTTONUP and \
                    event.button in (1, 2, 3):  # Don't consider the mouse wheel (button 4 & 5)
                self.sound.play_click_mouse()
                if rect.collidepoint(*event.pos):
                    self.apply()
                    updated = True

            elif self.touchscreen_enabled and event.type == pygame.FINGERUP:
                self.sound.play_click_mouse()
                window_size = self.get_menu().get_window_size()
                finger_pos = (event.x * window_size[0], event.y * window_size[1])
                if rect.collidepoint(*finger_pos):
                    self.apply()
                    updated = True

        if updated:
            self.apply_update_callbacks()

        return updated
