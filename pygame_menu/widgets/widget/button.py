# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

BUTTON
Button class, manage elements and adds entries to menu.

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

from pygame_menu.widgets.core import Widget
import pygame
import pygame_menu.controls as _controls
import types


class Button(Widget):
    """
    Button widget.

    :param title: Button title
    :type title: str
    :param button_id: Button ID
    :type button_id: str
    :param onchange: Callback when changing the selector
    :type onchange: callable, None
    :param onreturn: Callback when pressing return button
    :type onreturn: callable, None
    :param args: Optional arguments for callbacks
    :type args: any
    :param kwargs: Optional keyword arguments
    :type kwargs: dict
    """

    def __init__(self,
                 title,
                 button_id='',
                 onchange=None,
                 onreturn=None,
                 *args,
                 **kwargs):
        super(Button, self).__init__(
            title=title,
            widget_id=button_id,
            onchange=onchange,
            onreturn=onreturn,
            args=args,
            kwargs=kwargs
        )

    def _apply_font(self):
        pass

    def update_callback(self, func, *args):
        """
        Update function triggered by the button. Button cannot point to a Menu, as that is only
        valid using Menu.add_button() method

        :param func: Function
        :type func: Callable
        :param args: Arguments used by the function once triggered
        :type args: any
        :return: None
        """
        assert isinstance(func, (types.FunctionType, types.MethodType)) or callable(func), 'Only function are allowed'
        self._args = args or []  # type: list
        self._on_change = None  # type: callable
        self._on_return = func

    # noinspection PyMissingOrEmptyDocstring
    def draw(self, surface):
        self._render()
        self._fill_background_color(surface)
        surface.blit(self._surface, self._rect.topleft)

    def _render(self):
        if not self._render_hash_changed(self.selected, self._title):
            return
        if self.selected:
            color = self._font_selected_color
        else:
            color = self._font_color
        self._surface = self._render_string(self._title, color)
        self._rect.width, self._rect.height = self._surface.get_size()

    # noinspection PyMissingOrEmptyDocstring
    def update(self, events):
        updated = False
        for event in events:  # type: pygame.event.Event

            if event.type == pygame.KEYDOWN and event.key == _controls.KEY_APPLY or \
                    self.joystick_enabled and event.type == pygame.JOYBUTTONDOWN and event.button == _controls.JOY_BUTTON_SELECT:
                self.sound.play_open_menu()
                self.apply()
                updated = True

            elif self.mouse_enabled and event.type == pygame.MOUSEBUTTONUP:
                self.sound.play_click_mouse()
                if self._rect.collidepoint(*event.pos):
                    self.apply()
                    updated = True

            elif self.touchscreen_enabled and event.type == pygame.FINGERUP:
                self.sound.play_click_mouse()
                window_size = self.get_menu().get_window_size()
                finger_pos = (event.x * window_size[0], event.y * window_size[1])
                if self._rect.collidepoint(finger_pos):
                    self.apply()
                    updated = True

        return updated
