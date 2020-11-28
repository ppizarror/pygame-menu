# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SELECTOR
Selector class, manage elements and adds entries to menu.

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

import pygame
import pygame_menu.controls as _controls
from pygame_menu.utils import check_key_pressed_valid, to_string
from pygame_menu.widgets.core import Widget


def _check_elements(elements):
    """
    Check the element list.

    :param elements: Element list
    :type elements: list
    :return: None
    """
    assert len(elements) > 0, 'item list (elements) cannot be empty'
    for e in elements:
        assert len(e) >= 1, \
            'length of each element on item list must be greater or equal to 1'
        assert isinstance(e[0], (str, bytes)), \
            'first element of each item on list must be a string (the title of each item)'


class Selector(Widget):
    """
    Selector widget: several items with values and
    two functions that are executed when changing the selector (left/right)
    and pressing return button on the selected item.

    The values of the selector are like::

        values = [('Item1', a, b, c...), ('Item2', d, e, f..)]

    The callbacks receive the current text, its index in the list,
    the associated arguments and all unknown keyword arguments::

        onchange((current_text, index), a, b, c..., **kwargs)
        onreturn((current_text, index), a, b, c..., **kwargs)

    :param title: Selector title
    :type title: str
    :param elements: Elements of the selector
    :type elements: list
    :param selector_id: ID of the selector
    :type selector_id: str
    :param default: Index of default element to display
    :type default: int
    :param onchange: Callback when changing the selector
    :type onchange: callable, None
    :param onreturn: Callback when pressing return button
    :type onreturn: callable, None
    :param kwargs: Optional keyword arguments
    :type kwargs: dict
    """

    def __init__(self,
                 title,
                 elements,
                 selector_id='',
                 default=0,
                 onchange=None,
                 onreturn=None,
                 *args,
                 **kwargs):
        assert isinstance(elements, list)
        assert isinstance(selector_id, str)
        assert isinstance(default, int)

        # Check element list
        _check_elements(elements)
        assert default >= 0, 'default position must be greater or equal than zero'
        assert default < len(elements), 'default position should be lower than number of values'
        assert isinstance(selector_id, str), 'ID must be a string'
        assert isinstance(default, int), 'default must be an integer'

        super(Selector, self).__init__(
            title=to_string(title, strict=True),  # Cannot use unicode in py2 as selector use format
            widget_id=selector_id,
            onchange=onchange,
            onreturn=onreturn,
            args=args,
            kwargs=kwargs
        )

        self._elements = elements
        self._index = 0  # type: int
        self._sformat = '{0}< {1} >'  # type: str
        self._title_size = 0.0  # type: float

        # Apply default item
        default %= len(self._elements)
        for k in range(0, default):
            self.right()

    def _apply_font(self):
        self._title_size = self._font.size(self._title)[0]

    # noinspection PyMissingOrEmptyDocstring
    def draw(self, surface):
        self._render()
        self._fill_background_color(surface)
        surface.blit(self._surface, self._rect.topleft)

    def get_value(self):
        """
        Return the current value of the selector at the selected index.

        :return: Value and index as a tuple, (value, index)
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
        string = self._sformat.format(self._title, self.get_value()[0])
        if not self._render_hash_changed(string, self.selected):
            return
        if self.selected:
            color = self._font_selected_color
        else:
            color = self._font_color
        self._surface = self._render_string(string, color)
        self._rect.width, self._rect.height = self._surface.get_size()
        self._check_render_size_changed()

    def set_value(self, item):
        """
        Set the current value of the widget, selecting the element that matches
        the text if item is a string, or the index of the position of item is an integer.

        For example, if selector is *[['a',0],['b',1],['a',2]]*:
            - *widget*.set_value('a') -> Widget selects 0 (first match)
            - *widget*.set_value(2) -> Widget selects 2.

        :param item: Item to select, can be a string or an integer.
        :type item: str, int
        :return: None
        """
        assert isinstance(item, (str, int)), 'item must be an string or an integer'
        if isinstance(item, str):
            for element in self._elements:
                if element[0] == item:
                    self._index = self._elements.index(element)
                    return
            raise ValueError('no value "{}" found in selector'.format(item))
        elif isinstance(item, int):
            assert 0 <= item < len(self._elements), \
                'item index must be greater than zero and lower than the number of elements on the selector'
            self._index = item

    # noinspection PyMissingOrEmptyDocstring
    def update(self, events):
        updated = False
        for event in events:  # type: pygame.event.Event

            if event.type == pygame.KEYDOWN:  # Check key is valid
                if not check_key_pressed_valid(event):
                    continue

            # Events
            keydown = event.type == pygame.KEYDOWN
            joy_hatmotion = self.joystick_enabled and event.type == pygame.JOYHATMOTION
            joy_axismotion = self.joystick_enabled and event.type == pygame.JOYAXISMOTION
            joy_button_down = self.joystick_enabled and event.type == pygame.JOYBUTTONDOWN

            if keydown and event.key == _controls.KEY_LEFT or \
                    joy_hatmotion and event.value == _controls.JOY_LEFT or \
                    joy_axismotion and event.axis == _controls.JOY_AXIS_X and event.value < _controls.JOY_DEADZONE:
                self.sound.play_key_add()
                self.left()
                updated = True

            elif keydown and event.key == _controls.KEY_RIGHT or \
                    joy_hatmotion and event.value == _controls.JOY_RIGHT or \
                    joy_axismotion and event.axis == _controls.JOY_AXIS_X and event.value > -_controls.JOY_DEADZONE:
                self.sound.play_key_add()
                self.right()
                updated = True

            elif keydown and event.key == _controls.KEY_APPLY or \
                    joy_button_down and event.button == _controls.JOY_BUTTON_SELECT:
                self.sound.play_open_menu()
                self.apply(*self._elements[self._index][1:])
                updated = True

            elif self.mouse_enabled and event.type == pygame.MOUSEBUTTONUP:
                if self._rect.collidepoint(*event.pos):
                    # Check if mouse collides left or right as percentage, use only X coordinate
                    mousex, _ = event.pos
                    topleft, _ = self._rect.topleft
                    topright, _ = self._rect.topright
                    dist = mousex - (topleft + self._title_size)  # Distance from label
                    if dist > 0:  # User clicked the options, not label
                        # Position in percentage, if <0.5 user clicked left
                        pos = dist / float(topright - topleft - self._title_size)
                        if pos <= 0.5:
                            self.left()
                        else:
                            self.right()
                        updated = True

            elif self.touchscreen_enabled and event.type == pygame.FINGERUP:
                window_size = self.get_menu().get_window_size()
                finger_pos = (event.x * window_size[0], event.y * window_size[1])
                if self._rect.collidepoint(finger_pos):
                    # Check if mouse collides left or right as percentage, use only X coordinate
                    mousex, _ = finger_pos
                    topleft, _ = self._rect.topleft
                    topright, _ = self._rect.topright
                    dist = mousex - (topleft + self._title_size)  # Distance from label
                    if dist > 0:  # User clicked the options, not label
                        # Position in percentage, if <0.5 user clicked left
                        pos = dist / float(topright - topleft - self._title_size)
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
        _check_elements(elements)
        selected_element = self._elements[self._index]
        self._elements = elements
        try:
            self._index = self._elements.index(selected_element)
        except ValueError:
            if self._index >= len(self._elements):
                self._index = len(self._elements) - 1
