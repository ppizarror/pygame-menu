# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SELECTOR
Selector class, manage elements and adds entries to menu.

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


class Selector(Widget):
    """
    Selector widget.
    """

    def __init__(self,
                 title,
                 elements,
                 selector_id='',
                 default=0,
                 onchange=None,
                 onreturn=None,
                 **kwargs
                 ):
        """
        Description of the specific paramaters (see Widget class for generic ones):

        :param title: Title of the selector
        :type title: basestring
        :param elements: Elements of the selector
        :type elements: list
        :param selector_id: ID of the selector
        :type selector_id: basestring
        :param default: Index of default element to display
        :type default: int
        :param onchange: Callback when changing the selector
        :type onchange: function, NoneType
        :param onreturn: Callback when pressing return button
        :type onreturn: function, NoneType
        :param kwargs: Optional keyword-arguments for callbacks
        """
        assert isinstance(title, str)
        assert isinstance(elements, list)
        assert isinstance(selector_id, str)
        assert isinstance(default, int)

        super(Selector, self).__init__(widget_id=selector_id,
                                       onchange=onchange,
                                       onreturn=onreturn,
                                       kwargs=kwargs)

        self._elements = elements
        self._index = 0
        self._label = title
        self._labelsize = 0
        self._sformat = '{0} < {1} >'

        # Apply default item
        default %= len(self._elements)
        for k in range(0, default):
            self.right()

    def _apply_font(self):
        """
        See upper class doc.
        """
        self._labelsize = self._font.size(self._label)[0]

    def draw(self, surface):
        """
        See upper class doc.
        """
        self._render()
        surface.blit(self._surface, self._rect.topleft)

    def get_value(self):
        """
        Return the current value of the selector.

        :return: Value and index as a tuple
        :rtype: tuple
        """
        return self._elements[self._index][0], self._index

    def left(self):
        """
        Move selector to left.

        :return: None
        """
        self._index = (self._index - 1) % len(self._elements)
        self.change(*self._elements[self._index][1:])

    def right(self):
        """
        Move selector to right.

        :return: None
        """
        self._index = (self._index + 1) % len(self._elements)
        self.change(*self._elements[self._index][1:])

    def _render(self):
        """
        See upper class doc.
        """
        string = self._sformat.format(self._label, self.get_value()[0])
        if self.selected:
            color = self._font_selected_color
        else:
            color = self._font_color
        self._surface = self.render_string(string, color)

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
        for event in events:  # type: _pygame.event.EventType

            if event.type == _pygame.KEYDOWN:  # Check key is valid
                if not self.check_key_pressed_valid(event):
                    continue

            # Events
            keydown = event.type == _pygame.KEYDOWN
            joy_hatmotion = self.joystick_enabled and event.type == _pygame.JOYHATMOTION
            joy_axismotion = self.joystick_enabled and event.type == _pygame.JOYAXISMOTION
            joy_button_down = self.joystick_enabled and event.type == _pygame.JOYBUTTONDOWN

            if keydown and event.key == _ctrl.KEY_LEFT or \
                    joy_hatmotion and event.value == _ctrl.JOY_LEFT or \
                    joy_axismotion and event.axis == _ctrl.JOY_AXIS_X and event.value < _ctrl.JOY_DEADZONE:
                self.sound.play_key_add()
                self.left()
                updated = True

            elif keydown and event.key == _ctrl.KEY_RIGHT or \
                    joy_hatmotion and event.value == _ctrl.JOY_RIGHT or \
                    joy_axismotion and event.axis == _ctrl.JOY_AXIS_X and event.value > -_ctrl.JOY_DEADZONE:
                self.sound.play_key_add()
                self.right()
                updated = True

            elif keydown and event.key == _ctrl.KEY_APPLY or \
                    joy_button_down and event.button == _ctrl.JOY_BUTTON_SELECT:
                self.sound.play_open_menu()
                self.apply(*self._elements[self._index][1:])
                updated = True

            elif self.mouse_enabled and event.type == _pygame.MOUSEBUTTONUP:
                if self._rect.collidepoint(*event.pos):
                    # Check if mouse collides left or right as percentage, use only X coordinate
                    mousex, _ = event.pos
                    topleft, _ = self._rect.topleft
                    topright, _ = self._rect.topright
                    dist = mousex - (topleft + self._labelsize)  # Distance from label
                    if dist > 0:  # User clicked options, not label

                        # Position in percentage, if <0.5 user clicked left
                        pos = dist / float(topright - topleft - self._labelsize)
                        if pos <= 0.5:
                            self.left()
                        else:
                            self.right()
                        updated = True

        return updated

    def update_elements(self, elements):
        """
        Update selector elements.

        :param elements: Elements of the selector
        :type elements: Object
        :return: None
        """
        for elem in elements:  # Check value list
            assert len(elem) >= 1, 'Length of each element in value list must be greater than 1'
            assert isinstance(elem[0], str), 'First element of value list component must be a string'
        selected_element = self._elements[self._index]
        self._elements = elements
        try:
            self._index = self._elements.index(selected_element)
        except ValueError:
            if self._index >= len(self._elements):
                self._index = len(self._elements) - 1
