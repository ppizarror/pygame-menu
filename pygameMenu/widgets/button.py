# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

BUTTON
Button class, manage elements and adds entries to menu.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2019 Pablo Pizarro R. @ppizarror

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

import pygame as _pygame
from pygameMenu.widgets.widget import Widget
import pygameMenu.controls as _ctrl


class Button(Widget):
    """
    Button widget.
    """

    def __init__(self,
                 label,
                 button_id='',
                 onchange=None,
                 onreturn=None,
                 *args,
                 **kwargs
                 ):
        """
        Description of the specific paramaters (see Widget class for generic ones):

        :param label: Text of the button
        :type label: basestring
        :param button_id: Button ID
        :type button_id: basestring
        :param onchange: Callback when changing the selector
        :type onchange: function, NoneType
        :param onreturn: Callback when pressing return button
        :type onreturn: function, NoneType
        :param args: Optional arguments for callbacks
        :param kwargs: Optional keyword-arguments for callbacks
        """
        assert isinstance(label, str)
        super(Button, self).__init__(widget_id=button_id,
                                     onchange=onchange,
                                     onreturn=onreturn,
                                     args=args,
                                     kwargs=kwargs
                                     )
        self._label = label

    def _apply_font(self):
        """
        See upper class doc.
        """
        pass

    def draw(self, surface):
        """
        See upper class doc.
        """
        self._render()
        surface.blit(self._surface, self._rect.topleft)

    def _render(self):
        """
        See upper class doc.
        """
        if self.selected:
            color = self._font_selected_color
        else:
            color = self._font_color
        self._surface = self.render_string(self._label, color)

    def update(self, events):
        """
        See upper class doc.
        """
        updated = False
        for event in events:  # type: _pygame.event.EventType

            if event.type == _pygame.KEYDOWN and event.key == _ctrl.KEY_APPLY or \
                    self.joystick_enabled and event.type == _pygame.JOYBUTTONDOWN and event.button == _ctrl.JOY_BUTTON_SELECT:
                self.sound.play_open_menu()
                self.apply()
                updated = True

            elif self.mouse_enabled and event.type == _pygame.MOUSEBUTTONUP:
                self.sound.play_click_mouse()
                if self._rect.collidepoint(*event.pos):
                    self.apply()
                    updated = True

        return updated
