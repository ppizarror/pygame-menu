"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SELECTOR
Selector class, contains several items that can be changed in a horizontal way
(left/right). Items are solely displayed.

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

__all__ = [

    # Main class
    'Selector',

    # Constants
    'SELECTOR_STYLE_CLASSIC',
    'SELECTOR_STYLE_FANCY',

    # Utils
    'check_selector_items',

    # Types
    'SelectorStyleType'

]

import pygame

from pygame_menu.controls import KEY_LEFT, KEY_RIGHT, JOY_AXIS_X, JOY_LEFT, \
    JOY_RIGHT, JOY_DEADZONE, KEY_APPLY, JOY_BUTTON_SELECT
from pygame_menu.locals import FINGERUP
from pygame_menu.utils import check_key_pressed_valid, assert_color, assert_vector, \
    make_surface, get_finger_pos
from pygame_menu.widgets.core import Widget

from pygame_menu._types import Tuple, Union, List, Any, Optional, CallbackType, \
    Literal, ColorType, ColorInputType, Tuple2IntType, Tuple3IntType, EventVectorType, \
    Tuple2NumberType

SELECTOR_STYLE_CLASSIC = 'classic'
SELECTOR_STYLE_FANCY = 'fancy'

SelectorStyleType = Literal[SELECTOR_STYLE_CLASSIC, SELECTOR_STYLE_FANCY]


def check_selector_items(items: Union[Tuple, List]) -> None:
    """
    Check the items list.

    :param items: Items list
    :return: None
    """
    assert len(items) > 0, 'item list cannot be empty'
    for e in items:
        assert len(e) >= 1, \
            'length of each item on item list must be equal or greater than 1 ' \
            '(i.e. cannot be empty)'
        assert isinstance(e[0], (str, bytes)), \
            'first element of each item on list must be a string ' \
            '(the title of each item), but received "{0}"'.format(e[0])


# noinspection PyMissingOrEmptyDocstring
class Selector(Widget):
    """
    Selector widget: several items and two functions that are executed when changing
    the selector (left/right) and pressing return button on the selected item.

    The items of the selector are like:

    .. code-block:: python

        items = [('Item1', a, b, c...), ('Item2', d, e, f...)]

    The callbacks receive the current selected item, its index in the list,
    the associated arguments, and all unknown keyword arguments, where
    ``selected_item=widget.get_value()`` and ``selected_index=widget.get_index()``:

    .. code-block:: python

        onchange((selected_item, selected_index), a, b, c..., **kwargs)
        onreturn((selected_item, selected_index), a, b, c..., **kwargs)

    For example, if ``selected_index=0`` then ``selected_item=('Item1', a, b, c...)``.

    :param title: Selector title
    :param items: Items of the selector
    :param selector_id: ID of the selector
    :param default: Index of default item to display
    :param onchange: Callback when changing the selector
    :param onreturn: Callback when pressing return on the selector
    :param onselect: Function when selecting the widget
    :param style: Selector style (visual)
    :param style_fancy_arrow_color: Arrow color of fancy style
    :param style_fancy_arrow_margin: Margin of arrows on x-axis and y-axis (x, y) in px; format: (left, right, vertical)
    :param style_fancy_bgcolor: Background color of fancy style
    :param style_fancy_bordercolor: Border color of fancy style
    :param style_fancy_borderwidth: Border width of fancy style
    :param style_fancy_box_inflate: Box inflate of fancy style on x-axis and y-axis (x, y) in px
    :param style_fancy_box_margin: Box margin on x-axis and y-axis (x, y) in fancy style from title in px
    :param kwargs: Optional keyword arguments
    """
    _index: int
    _items: Union[List[Tuple[Any, ...]], List[str]]
    _sformat: str
    _style: SelectorStyleType
    _style_fancy_arrow_color: ColorType
    _style_fancy_arrow_margin: Tuple3IntType
    _style_fancy_bgcolor: ColorType
    _style_fancy_bordercolor: ColorType
    _style_fancy_borderwidth: int
    _style_fancy_box_inflate: Tuple2IntType
    _style_fancy_box_margin: Tuple2IntType  # Box (left, top)
    _title_size: int

    def __init__(
            self,
            title: Any,
            items: Union[List[Tuple[Any, ...]], List[str]],
            selector_id: str = '',
            default: int = 0,
            onchange: CallbackType = None,
            onreturn: CallbackType = None,
            onselect: CallbackType = None,
            style: SelectorStyleType = SELECTOR_STYLE_CLASSIC,
            style_fancy_arrow_color: ColorInputType = (160, 160, 160),
            style_fancy_arrow_margin: Tuple3IntType = (5, 5, 0),
            style_fancy_bgcolor: ColorInputType = (180, 180, 180),
            style_fancy_bordercolor: ColorInputType = (0, 0, 0),
            style_fancy_borderwidth: int = 1,
            style_fancy_box_inflate: Tuple2IntType = (0, 0),
            style_fancy_box_margin: Tuple2NumberType = (25, 0),
            *args,
            **kwargs
    ) -> None:
        assert isinstance(items, list)
        assert isinstance(selector_id, str)
        assert isinstance(default, int)
        assert style in (SELECTOR_STYLE_CLASSIC, SELECTOR_STYLE_FANCY), \
            'invalid selector style'

        # Check items list
        check_selector_items(items)
        assert default >= 0, \
            'default position must be equal or greater than zero'
        assert default < len(items), \
            'default position should be lower than number of values'
        assert isinstance(selector_id, str), 'id must be a string'
        assert isinstance(default, int), 'default must be an integer'

        # Check fancy style
        style_fancy_arrow_color = assert_color(style_fancy_arrow_color)
        assert_vector(style_fancy_arrow_margin, 3, int)
        assert_vector(style_fancy_box_margin, 2)
        style_fancy_bgcolor = assert_color(style_fancy_bgcolor)
        style_fancy_bordercolor = assert_color(style_fancy_bordercolor)
        assert isinstance(style_fancy_borderwidth, int) and style_fancy_borderwidth >= 0
        assert_vector(style_fancy_box_inflate, 2, int)
        assert style_fancy_box_inflate[0] >= 0 and style_fancy_box_inflate[1] >= 0, \
            'box inflate must be equal or greater than zero on both axis'

        super(Selector, self).__init__(
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            title=title,
            widget_id=selector_id,
            args=args,
            kwargs=kwargs
        )

        self._index = 0
        self._items = items.copy()
        self._sformat = ''
        self._style = style
        self._title_size = 0

        # Store fancy style
        self._style_fancy_arrow_color = style_fancy_arrow_color
        self._style_fancy_arrow_margin = style_fancy_arrow_margin
        self._style_fancy_bgcolor = style_fancy_bgcolor
        self._style_fancy_bordercolor = style_fancy_bordercolor
        self._style_fancy_borderwidth = style_fancy_borderwidth
        self._style_fancy_box_inflate = style_fancy_box_inflate
        self._style_fancy_box_margin = (int(style_fancy_box_margin[0]),
                                        int(style_fancy_box_margin[1]))

        # Apply default item
        default %= len(self._items)
        for k in range(0, default):
            self._right()

        # Last configs
        self.set_sformat('{0}< {1} >')
        self.set_default_value(default)

    def set_sformat(self, sformat: str) -> 'Selector':
        """
        Set sformat for classic style. This receives a string which is later
        formatted with {0}: title and {1}: the current selected item.

        :param sformat: String. Must contain {0} and {1}
        :return: Self reference
        """
        assert isinstance(sformat, str)
        assert '{0}' in sformat and '{1}' in sformat and '{2}' not in sformat, \
            'sformat must contain {0} and {1}'
        self._sformat = sformat
        return self

    def set_default_value(self, index: int) -> 'Selector':
        self._default_value = index
        return self

    def _apply_font(self) -> None:
        self._title_size = self._font.size(self._title)[0]
        if self._style == SELECTOR_STYLE_FANCY:
            self._title_size += self._style_fancy_box_margin[0] \
                                - self._style_fancy_box_inflate[0] / 2 \
                                + self._style_fancy_borderwidth
        self._title_size = int(self._title_size)

    def _draw(self, surface: 'pygame.Surface') -> None:
        surface.blit(self._surface, self._rect.topleft)

    def _render(self) -> Optional[bool]:
        current_selected = self.get_value()[0][0]
        if not self._render_hash_changed(
                current_selected, self._selected, self._visible, self._index,
                self.readonly):
            return True

        color = self.get_font_color_status()

        # Render from different styles
        if self._style == SELECTOR_STYLE_CLASSIC:
            string = self._sformat.format(self._title, current_selected)
            self._surface = self._render_string(string, color)

        else:
            title = self._render_string(self._title, color)
            current = self._render_string(
                current_selected, self.get_font_color_status(check_selection=False)
            )

            # Create arrows
            arrow_left = pygame.Rect(
                title.get_width() + self._style_fancy_arrow_margin[0]
                + self._style_fancy_box_margin[0],
                self._style_fancy_arrow_margin[2] + self._style_fancy_box_inflate[1] / 2,
                title.get_height(),
                title.get_height()
            )
            arrow_left_pos = (
                (arrow_left.left + 5, arrow_left.centery),
                (arrow_left.centerx, arrow_left.top + 5),
                (arrow_left.centerx, arrow_left.centery - 2),
                (arrow_left.right - 5, arrow_left.centery - 2),
                (arrow_left.right - 5, arrow_left.centery + 2),
                (arrow_left.centerx, arrow_left.centery + 2),
                (arrow_left.centerx, arrow_left.bottom - 5),
                (arrow_left.left + 5, arrow_left.centery)
            )

            arrow_right = pygame.Rect(
                title.get_width() + 2 * self._style_fancy_arrow_margin[0]
                + self._style_fancy_box_margin[0]
                + self._style_fancy_arrow_margin[1] + current.get_width(),
                self._style_fancy_arrow_margin[2] + self._style_fancy_box_inflate[1] / 2
                + self._style_fancy_box_margin[1],
                title.get_height(),
                title.get_height()
            )
            arrow_right_pos = (
                (2 * arrow_right.right - (arrow_right.left + 5), arrow_right.centery),
                (2 * arrow_right.right - arrow_right.centerx, arrow_right.top + 5),
                (2 * arrow_right.right - arrow_right.centerx, arrow_right.centery - 2),
                (2 * arrow_right.right - (arrow_right.right - 5), arrow_right.centery - 2),
                (2 * arrow_right.right - (arrow_right.right - 5), arrow_right.centery + 2),
                (2 * arrow_right.right - arrow_right.centerx, arrow_right.centery + 2),
                (2 * arrow_right.right - arrow_right.centerx, arrow_right.bottom - 5),
                (2 * arrow_right.right - (arrow_right.left + 5), arrow_right.centery)
            )

            self._surface = make_surface(
                title.get_width()
                + 2 * self._style_fancy_arrow_margin[0]
                + 2 * self._style_fancy_arrow_margin[1]
                + self._style_fancy_box_margin[0]
                + current.get_width()
                + 2 * arrow_left.width
                + self._style_fancy_borderwidth
                + self._style_fancy_box_inflate[0] / 2,
                title.get_height() + self._style_fancy_box_inflate[1])
            self._surface.blit(title, (0, self._style_fancy_box_inflate[1] / 2))
            current_rect_bg = current.get_rect()
            current_rect_bg.x += title.get_width() + self._style_fancy_box_margin[0]
            current_rect_bg.y += self._style_fancy_box_inflate[1] / 2 \
                                 + self._style_fancy_box_margin[1]
            current_rect_bg.width += 2 * (self._style_fancy_arrow_margin[0]
                                          + self._style_fancy_arrow_margin[1]
                                          + arrow_left.width)
            current_rect_bg = current_rect_bg.inflate(self._style_fancy_box_inflate)
            pygame.draw.rect(self._surface, self._style_fancy_bgcolor, current_rect_bg)
            pygame.draw.rect(self._surface, self._style_fancy_bordercolor, current_rect_bg,
                             self._style_fancy_borderwidth)
            self._surface.blit(
                current, (title.get_width()
                          + arrow_left.width
                          + self._style_fancy_arrow_margin[0]
                          + self._style_fancy_arrow_margin[1]
                          + self._style_fancy_box_margin[0],
                          self._style_fancy_box_inflate[1] / 2
                          + self._style_fancy_box_margin[1]))
            pygame.draw.polygon(self._surface, self._style_fancy_arrow_color, arrow_left_pos)
            pygame.draw.polygon(self._surface, self._style_fancy_arrow_color, arrow_right_pos)

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
        Return the current value of the selected index.

        :return: Value and index as a tuple, (value, index)
        """
        return self._items[self._index], self._index

    def _left(self) -> None:
        """
        Move selector to left.

        :return: None
        """
        if self.readonly:
            return
        self._index = (self._index - 1) % len(self._items)
        self.change(*self._items[self._index][1:])
        self._sound.play_key_add()

    def _right(self) -> None:
        """
        Move selector to right.

        :return: None
        """
        if self.readonly:
            return
        self._index = (self._index + 1) % len(self._items)
        self.change(*self._items[self._index][1:])
        self._sound.play_key_add()

    def set_value(self, item: Union[str, int]) -> None:
        """
        Set the current value of the widget, selecting the item that matches
        the text if ``item`` is a string, or the index if ``item`` is an integer.
        This method raises ``ValueError`` if no item found.

        For example, if widget item list is ``[['a',0],['b',1],['a',2]]``:

        - *widget*.set_value('a') -> Widget selects the first item (index 0)
        - *widget*.set_value(2) -> Widget selects the third item (index 2)

        .. note::

            This method does not trigger any event (change).

        :param item: Item to select, can be a string or an integer
        :return: None
        """
        assert isinstance(item, (str, int)), 'item must be a string or an integer'
        if isinstance(item, str):
            found = False
            for i in self._items:
                if i[0] == item:
                    self._index = self._items.index(i)
                    found = True
                    break
            if not found:
                raise ValueError('no value "{}" found in selector'.format(item))
        elif isinstance(item, int):
            assert 0 <= item < len(self._items), \
                'item index must be greater than zero and lower than the number ' \
                'of items on the selector'
            self._index = item

    def update_items(self, items: Union[List[Tuple[Any, ...]], List[str]]) -> None:
        """
        Update selector items.

        .. note::

            If the length of the list is different than the previous one,
            the new index of the selector will be the first item of the list.

        :param items: New selector items; format ``[('Item1', a, b, c...), ('Item2', d, e, f...)]``
        :return: None
        """
        check_selector_items(items)
        selected_item = self._items[self._index]
        self._items = items
        try:
            self._index = self._items.index(selected_item)
        except ValueError:
            if self._index >= len(self._items):
                self._index = 0
                self._default_value = 0

    def update(self, events: EventVectorType) -> bool:
        self.apply_update_callbacks(events)

        if self.readonly or not self.is_visible():
            return False
        updated = False

        for event in events:

            if event.type == pygame.KEYDOWN:  # Check key is valid
                if not check_key_pressed_valid(event):
                    continue

            # Check mouse over
            self._check_mouseover(event)

            # Events
            keydown = self._keyboard_enabled and event.type == pygame.KEYDOWN
            joy_hatmotion = self._joystick_enabled and event.type == pygame.JOYHATMOTION
            joy_axismotion = self._joystick_enabled and event.type == pygame.JOYAXISMOTION
            joy_button_down = self._joystick_enabled and event.type == pygame.JOYBUTTONDOWN

            # Left button
            if keydown and event.key == KEY_LEFT or \
                    joy_hatmotion and event.value == JOY_LEFT or \
                    joy_axismotion and event.axis == JOY_AXIS_X and event.value < JOY_DEADZONE:
                self._left()
                updated = True

            # Right button
            elif keydown and event.key == KEY_RIGHT or \
                    joy_hatmotion and event.value == JOY_RIGHT or \
                    joy_axismotion and event.axis == JOY_AXIS_X and event.value > -JOY_DEADZONE:
                self._right()
                updated = True

            # Press enter
            elif keydown and event.key == KEY_APPLY or \
                    joy_button_down and event.button == JOY_BUTTON_SELECT:
                self._sound.play_key_add()
                self.apply(*self._items[self._index][1:])
                updated = True

            # Click on selector; don't consider the mouse wheel (button 4 & 5)
            elif event.type == pygame.MOUSEBUTTONUP and self._mouse_enabled and \
                    event.button in (1, 2, 3) or \
                    event.type == FINGERUP and self._touchscreen_enabled and \
                    self._menu is not None:
                event_pos = get_finger_pos(self._menu, event)

                # If collides
                rect = self.get_rect(to_real_position=True, apply_padding=False)
                if rect.collidepoint(*event_pos):
                    # Check if mouse collides left or right as percentage, use only X coordinate
                    mouse_x, _ = event.pos
                    topleft, _ = rect.topleft
                    topright, _ = rect.topright
                    dist = mouse_x - (topleft + self._title_size)  # Distance from title
                    if dist > 0:  # User clicked the options, not title
                        # Position in percentage, if <0.5 user clicked left
                        pos = dist / float(topright - topleft - self._title_size)
                        if pos <= 0.5:
                            self._left()
                        else:
                            self._right()
                        updated = True

        return updated
