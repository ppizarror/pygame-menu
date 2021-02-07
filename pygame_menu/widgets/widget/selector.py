"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SELECTOR
Selector class, manage elements and adds entries to Menu.

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

__all__ = ['Selector']

import pygame
import pygame_menu.controls as _controls
from pygame_menu.utils import check_key_pressed_valid
from pygame_menu.widgets.core import Widget
from pygame_menu._types import Tuple, Union, List, Any, Optional, CallbackType


def check_selector_elements(elements: Union[Tuple, List]) -> None:
    """
    Check the element list.

    :param elements: Element list
    :return: None
    """
    assert len(elements) > 0, 'item list (elements) cannot be empty'
    for e in elements:
        assert len(e) >= 1, \
            'length of each element on item list must be equal or greater than 1'
        assert isinstance(e[0], (str, bytes)), \
            'first element of each item on list must be a string (the title of each item)'


# noinspection PyMissingOrEmptyDocstring
class Selector(Widget):
    """
    Selector widget: several items with values and two functions that are executed
    when changing the selector (left/right) and pressing return button on the selected item.

    The values of the selector are like:

    .. code-block:: python

        values = [('Item1', a, b, c...), ('Item2', d, e, f...)]

    The callbacks receive the current value, its index in the list,
    the associated arguments, and all unknown keyword arguments, where
    ``selected_value=widget.get_value()`` and ``selected_index=widget.get_index()``:

    .. code-block:: python

        onchange((selected_value, index), a, b, c..., **kwargs)
        onreturn((selected_value, index), a, b, c..., **kwargs)

    For example, if ``selected_index=0`` then ``selected_value=('Item1', a, b, c...)``.

    :param title: Selector title
    :param elements: Elements of the selector
    :param selector_id: ID of the selector
    :param default: Index of default element to display
    :param onchange: Callback when changing the selector
    :param onreturn: Callback when pressing return on the selector
    :param onselect: Function when selecting the widget
    :param kwargs: Optional keyword arguments
    """
    _elements: Union[List[Tuple[Any, ...]], List[str]]
    _index: int
    _sformat: str
    _title_size: int

    def __init__(self,
                 title: Any,
                 elements: Union[List[Tuple[Any, ...]], List[str]],
                 selector_id: str = '',
                 default: int = 0,
                 onchange: CallbackType = None,
                 onreturn: CallbackType = None,
                 onselect: CallbackType = None,
                 *args,
                 **kwargs
                 ) -> None:
        assert isinstance(elements, list)
        assert isinstance(selector_id, str)
        assert isinstance(default, int)

        # Check element list
        check_selector_elements(elements)
        assert default >= 0, 'default position must be equal or greater than zero'
        assert default < len(elements), 'default position should be lower than number of values'
        assert isinstance(selector_id, str), 'id must be a string'
        assert isinstance(default, int), 'default must be an integer'

        super(Selector, self).__init__(
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            title=title,
            widget_id=selector_id,
            args=args,
            kwargs=kwargs
        )

        self._elements = elements
        self._index = 0
        self._sformat = '{0}< {1} >'
        self._title_size = 0

        # Apply default item
        default %= len(self._elements)
        for k in range(0, default):
            self._right()
        self.set_default_value(default)

    def set_default_value(self, index: int) -> 'Widget':
        self._default_value = index
        return self

    def reset_value(self) -> 'Widget':
        self._index = self._default_value
        return self

    def _apply_font(self) -> None:
        self._title_size = int(self._font.size(self._title)[0])

    def _draw(self, surface: 'pygame.Surface') -> None:
        surface.blit(self._surface, self._rect.topleft)

    def _render(self) -> Optional[bool]:
        string = self._sformat.format(self._title, self.get_value()[0][0])
        if not self._render_hash_changed(string, self._selected, self._visible, self._index, self.readonly):
            return True
        self._surface = self._render_string(string, self.get_font_color_status())
        self._apply_transforms()
        self._rect.width, self._rect.height = self._surface.get_size()
        self.force_menu_surface_update()

    def get_index(self) -> int:
        """
        Get selected index.

        :return: Selected index
        """
        return self._index

    def get_value(self) -> Tuple[Union[Tuple[Any, ...], str], int]:
        """
        Return the current value of the selector at the selected index.

        :return: Value and index as a tuple, (value, index)
        """
        return self._elements[self._index], self._index

    def _left(self) -> None:
        """
        Move selector to left.

        :return: None
        """
        if self.readonly:
            return
        self._index = (self._index - 1) % len(self._elements)
        self.change(*self._elements[self._index][1:])

    def _right(self) -> None:
        """
        Move selector to right.

        :return: None
        """
        if self.readonly:
            return
        self._index = (self._index + 1) % len(self._elements)
        self.change(*self._elements[self._index][1:])

    def set_value(self, item: Union[str, int]) -> None:
        """
        Set the current value of the widget, selecting the element that matches
        the text if item is a string, or the index of the position of item is an integer.
        This method raises ``ValueError`` if no element found.

        For example, if selector is ``[['a',0],['b',1],['a',2]]``:

        - *widget*.set_value('a') -> Widget selects the first element (index 0)
        - *widget*.set_value(2) -> Widget selects the third element (index 2)

        :param item: Item to select, can be a string or an integer.
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

    def update_elements(self, elements: Union[List[Tuple[Any, ...]], List[str]]) -> None:
        """
        Update selector elements.

        .. note::

            If the length of the list is different than the previous one,
            the new index of the selector will be the first element of the list.

        :param elements: Elements of the selector ``[('Item1', a, b, c...), ('Item2', d, e, f...)]``
        :return: None
        """
        check_selector_elements(elements)
        selected_element = self._elements[self._index]
        self._elements = elements
        try:
            self._index = self._elements.index(selected_element)
        except ValueError:
            if self._index >= len(self._elements):
                self._index = 0
                self._default_value = 0

    def update(self, events: Union[List['pygame.event.Event'], Tuple['pygame.event.Event']]) -> bool:
        if self.readonly:
            return False
        updated = False

        for event in events:

            if event.type == pygame.KEYDOWN:  # Check key is valid
                if not check_key_pressed_valid(event):
                    continue

            # Events
            keydown = self._keyboard_enabled and event.type == pygame.KEYDOWN
            joy_hatmotion = self._joystick_enabled and event.type == pygame.JOYHATMOTION
            joy_axismotion = self._joystick_enabled and event.type == pygame.JOYAXISMOTION
            joy_button_down = self._joystick_enabled and event.type == pygame.JOYBUTTONDOWN

            # Left button
            if keydown and event.key == _controls.KEY_LEFT or \
                    joy_hatmotion and event.value == _controls.JOY_LEFT or \
                    joy_axismotion and event.axis == _controls.JOY_AXIS_X and event.value < _controls.JOY_DEADZONE:
                self._sound.play_key_add()
                self._left()
                updated = True

            # Right button
            elif keydown and event.key == _controls.KEY_RIGHT or \
                    joy_hatmotion and event.value == _controls.JOY_RIGHT or \
                    joy_axismotion and event.axis == _controls.JOY_AXIS_X and event.value > -_controls.JOY_DEADZONE:
                self._sound.play_key_add()
                self._right()
                updated = True

            # Press enter
            elif keydown and event.key == _controls.KEY_APPLY or \
                    joy_button_down and event.button == _controls.JOY_BUTTON_SELECT:
                self._sound.play_open_menu()
                self.apply(*self._elements[self._index][1:])
                updated = True

            # Click on selector
            elif self._mouse_enabled and event.type == pygame.MOUSEBUTTONUP and event.button in (1, 2, 3) or \
                    self._touchscreen_enabled and event.type == pygame.FINGERUP:  # Don't consider the mouse wheel (button 4 & 5)

                # Get event position based on input type
                if self._touchscreen_enabled and event.type == pygame.FINGERUP:
                    window_size = self.get_menu().get_window_size()
                    event_pos = (event.x * window_size[0], event.y * window_size[1])
                else:
                    event_pos = event.pos

                # If collides
                rect = self.get_rect(to_real_position=True)
                if rect.collidepoint(*event_pos):
                    # Check if mouse collides left or right as percentage, use only X coordinate
                    mousex, _ = event.pos
                    topleft, _ = rect.topleft
                    topright, _ = rect.topright
                    dist = mousex - (topleft + self._title_size)  # Distance from title
                    if dist > 0:  # User clicked the options, not title
                        # Position in percentage, if <0.5 user clicked left
                        pos = dist / float(topright - topleft - self._title_size)
                        if pos <= 0.5:
                            self._left()
                        else:
                            self._right()
                        updated = True

        if updated:
            self.apply_update_callbacks()

        return updated
