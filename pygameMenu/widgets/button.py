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
from pygameMenu import config_controls as _ctrl
from pygameMenu.widgets.abstract import Widget
from pygameMenu import locals as _locals


class Button(Widget):
    """
    Button widget.
    """

    def __init__(self,
                 label,
                 onchange=None,
                 onreturn=None,
                 *args,
                 **kwargs
                 ):
        """
        Description of the specific paramaters (see Widget class for generic ones):

        :param label: Text of the button
        :param onchange: callback when changing the selector
        :param onreturn: callback when pressing return button
        :param args: Optional arguments for callbacks
        :param kwargs: Optional keyword-arguments for callbacks
        :type label: basestring
        :type onchange: function, NoneType
        :type onreturn: function, NoneType
        """
        super(Button, self).__init__(onchange=onchange, onreturn=onreturn,
                                     args=args, kwargs=kwargs)  # Button has no ID

        # Public attributs
        self.label = label

    def draw(self, surface):
        """
        See upper class doc.
        """
        self._render()

        if self._shadow:
            text_bg = self._font.render(self.label, 1, self._shadow_color)
            surface.blit(text_bg, self._rect.move(-3, -3).topleft)
        surface.blit(self._surface, self._rect.topleft)

    def _render(self):
        """
        See upper class doc.
        """
        if self.selected:
            color = self._font_selected_color
        else:
            color = self._font_color
        self._surface = self._font.render(self.label, 1, color)

    def update(self, events):
        """
        See upper class doc.
        """
        updated = False
        for event in events:

            if event.type == _pygame.locals.KEYDOWN:
                if event.key == _ctrl.MENU_CTRL_ENTER:
                    self.apply()
                    updated = True

            elif self.joystick_enabled and event.type == _pygame.JOYBUTTONDOWN:
                if event.button == _locals.JOY_BUTTON_SELECT:
                    self.apply()
                    updated = True

            elif self.mouse_enabled and event.type == _pygame.MOUSEBUTTONUP:
                if self._rect.collidepoint(*event.pos):
                    self.apply()
                    updated = True

        return updated
