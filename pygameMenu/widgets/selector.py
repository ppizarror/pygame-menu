# -*- coding: utf-8 -*-
"""
SELECTOR
Selector class, manage elements and adds entries to menu.

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
"""

import pygame as _pygame
from pygameMenu import config_controls as _ctrl
from pygameMenu.widgets.abstract import Widget
from pygameMenu import locals as _locals


class Selector(Widget):

    """
    Selector widget
    """

    def __init__(self,
                 title,
                 elements,
                 default=0,
                 onchange=None, onreturn=None, **kwargs):
        """
        Description of the specific paramaters (see Widget class for generic ones):

        :param title: Title of the selector
        :param elements: Elements of the selector
        :param default: Index of default element to display

        :type title: str
        :type elements: list
        :type default: int
        """
        super(Selector, self).__init__(onchange, onreturn, kwargs=kwargs)
        self._elements = elements
        self._index = 0
        self._title = title
        self._total_elements = len(elements)

        # Selection format
        self._sformat = '{0} < {1} >'

        # Apply default item
        default %= self._total_elements
        for k in range(0, default):
            self.right()

    def draw(self, surface):
        """
        See upper class doc.
        """
        self._render()

        if self._shadow:
            string = self._sformat.format(self._title, self.get_value())
            text_bg = self._font.render(string, 1, self._shadow_color)
            surface.blit(text_bg, self._rect.move(-3, -3).topleft)

        surface.blit(self._surface, self._rect.topleft)

    def get_value(self):
        """
        Return the current value of the selector.

        :return: text
        :rtype: str
        """
        return self._elements[self._index][0]

    def left(self):
        """
        Move selector to left.
        :return: None
        """
        self._index = (self._index - 1) % self._total_elements
        self.change(*self._elements[self._index][1:])

    def _render(self):
        """
        See upper class doc.
        """
        string = self._sformat.format(self._title, self.get_value())
        if self.selected:
            color = self._font_selected_color
        else:
            color = self._font_color
        self._surface = self._font.render(string, 1, color)

    def right(self):
        """
        Move selector to right.
        :return: None
        """
        self._index = (self._index + 1) % self._total_elements
        self.change(*self._elements[self._index][1:])

    def set_selection_format(self, s):
        """
        Change the text format.

        :param s: Selection text
        :type s: basestring
        :return: None
        """
        self._sformat = s

    def set_value(self, text):
        """
        Set the current value of the selector.

        :return: None
        """
        for element in self._elements:
            if element[0] == text:
                self._index = self._elements.index(element)
                return
        raise ValueError("No value '{}' found in selector".format(text))

    def update(self, events):
        """
        See upper class doc.
        """
        updated = False
        for event in events:
            if event.type == _pygame.locals.KEYDOWN:
                if event.key == _ctrl.MENU_CTRL_LEFT:
                    self.left()
                    updated = True
                elif event.key == _ctrl.MENU_CTRL_RIGHT:
                    self.right()
                    updated = True
                elif event.key == _ctrl.MENU_CTRL_ENTER:
                    self.apply(*self._elements[self._index][1:])
                    updated = True

            elif self.joystick_enabled and event.type == _pygame.JOYHATMOTION:
                if event.value == _locals.JOY_LEFT:
                    self.left()
                    updated = True
                elif event.value == _locals.JOY_RIGHT:
                    self.right()
                    updated = True

            elif self.joystick_enabled and event.type == _pygame.JOYAXISMOTION:
                if event.axis == _locals.JOY_AXIS_X and event.value < _locals.JOY_DEADZONE:
                    self.left()
                    updated = True
                if event.axis == _locals.JOY_AXIS_X and event.value > -_locals.JOY_DEADZONE:
                    self.right()
                    updated = True

            elif self.mouse_enabled and event.type == _pygame.MOUSEBUTTONUP:
                if self._rect.collidepoint(*event.pos):
                    self.right()
                    updated = True

        return updated

    def update_elements(self, elements):
        """
        Update selector elements.

        :param elements: Elements of the selector
        :return: None
        """
        selected_element = self._elements[self._index]
        self._elements = elements
        self._total_elements = len(elements)
        try:
            self._index = self._elements.index(selected_element)
        except ValueError:
            if self._index >= self._total_elements:
                self._index = self._total_elements - 1
