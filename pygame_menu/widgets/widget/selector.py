"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SELECTOR
Selector class, contains several items that can be changed in a horizontal way
(left/right). Items are solely displayed.
"""

__all__ = [

    # Main class
    'Selector',
    'SelectorManager',

    # Constants
    'SELECTOR_STYLE_CLASSIC',
    'SELECTOR_STYLE_FANCY',

    # Utils
    'check_selector_items',

    # Types
    'SelectorStyleType'

]

import pygame
import pygame_menu

from abc import ABC
from pygame_menu.locals import FINGERUP
from pygame_menu.utils import check_key_pressed_valid, assert_color, assert_vector, \
    make_surface, get_finger_pos
from pygame_menu.widgets.core.widget import Widget, AbstractWidgetManager

from pygame_menu._types import Tuple, Union, List, Any, Optional, CallbackType, \
    Literal, ColorType, ColorInputType, Tuple2IntType, Tuple3IntType, EventVectorType, \
    Tuple2NumberType, Callable

SELECTOR_STYLE_CLASSIC = 'classic'
SELECTOR_STYLE_FANCY = 'fancy'

SelectorStyleType = Literal[SELECTOR_STYLE_CLASSIC, SELECTOR_STYLE_FANCY]


def check_selector_items(items: Union[Tuple, List]) -> None:
    """
    Check the items list.

    :param items: Items list
    """
    assert len(items) > 0, 'item list cannot be empty'
    for e in items:
        assert len(e) >= 1, \
            'length of each item on item list must be equal or greater than 1 ' \
            '(i.e. cannot be empty)'
        assert isinstance(e[0], (str, bytes)), \
            f'first element of each item on list must be a string ' \
            f'(the title of each item), but received "{e[0]}"'


# noinspection PyMissingOrEmptyDocstring
class Selector(Widget):
    """
    Selector widget: several items and two functions that are executed when changing
    the selector (left/right) and pressing return (apply) on the selected item.

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

    .. note::

        Selector accepts all transformations.

    :param title: Selector title
    :param items: Items of the selector
    :param selector_id: ID of the selector
    :param default: Index of default item to display
    :param onchange: Callback when changing the selector
    :param onreturn: Callback when pressing return (apply) on the selector
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

        self._accept_events = True
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
        self._style_fancy_box_margin = (int(style_fancy_box_margin[0]), int(style_fancy_box_margin[1]))

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
                int(title.get_width() + self._style_fancy_arrow_margin[0] + self._style_fancy_box_margin[0]),
                int(self._style_fancy_arrow_margin[2] + self._style_fancy_box_inflate[1] / 2),
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
                int(title.get_width()
                    + 2 * self._style_fancy_arrow_margin[0]
                    + self._style_fancy_box_margin[0]
                    + self._style_fancy_arrow_margin[1] + current.get_width()
                    ),
                int(self._style_fancy_arrow_margin[2]
                    + self._style_fancy_box_inflate[1] / 2
                    + self._style_fancy_box_margin[1]),
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
            self._surface.blit(title, (0, int(self._style_fancy_box_inflate[1] / 2)))
            current_rect_bg = current.get_rect()
            current_rect_bg.x += title.get_width() + self._style_fancy_box_margin[0]
            current_rect_bg.y += int(self._style_fancy_box_inflate[1] / 2 + self._style_fancy_box_margin[1])
            current_rect_bg.width += 2 * (self._style_fancy_arrow_margin[0]
                                          + self._style_fancy_arrow_margin[1]
                                          + arrow_left.width)
            current_rect_bg = current_rect_bg.inflate(self._style_fancy_box_inflate)
            pygame.draw.rect(self._surface, self._style_fancy_bgcolor, current_rect_bg)
            pygame.draw.rect(self._surface, self._style_fancy_bordercolor, current_rect_bg,
                             self._style_fancy_borderwidth)
            self._surface.blit(
                current, (int(title.get_width()
                              + arrow_left.width
                              + self._style_fancy_arrow_margin[0]
                              + self._style_fancy_arrow_margin[1]
                              + self._style_fancy_box_margin[0]),
                          int(self._style_fancy_box_inflate[1] / 2
                              + self._style_fancy_box_margin[1])))
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

    def get_items(self) -> Union[List[Tuple[Any, ...]], List[str]]:
        """
        Return a copy of the select items.

        :return: Select items list
        """
        return self._items.copy()

    def get_value(self) -> Tuple[Union[Tuple[Any, ...], str], int]:
        """
        Return the current value of the selected index.

        :return: Value and index as a tuple, (value, index)
        """
        return self._items[self._index], self._index

    def value_changed(self) -> bool:
        return self._index != self._default_value

    def _left(self) -> None:
        """
        Move selector to left.
        """
        if self.readonly:
            return
        self._index = (self._index - 1) % len(self._items)
        self.change(*self._items[self._index][1:])
        self._sound.play_key_add()

    def _right(self) -> None:
        """
        Move selector to right.
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

        For example, if widget item list is ``[['a', 0], ['b', 1], ['a', 2]]``:

        - *widget*.set_value('a') -> Widget selects the first item (index 0)
        - *widget*.set_value(2) -> Widget selects the third item (index 2)

        .. note::

            This method does not trigger any event (change).

        :param item: Item to select, can be a string or an integer
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
                raise ValueError(f'no value "{item}" found in selector')
        elif isinstance(item, int):
            assert 0 <= item < len(self._items), \
                'item index must be greater than zero and lower than the number ' \
                'of items on the selector'
            self._index = item
        self._render()

    def update_items(self, items: Union[List[Tuple[Any, ...]], List[str]]) -> None:
        """
        Update selector items.

        .. note::

            If the length of the list is different from the previous one,
            the new index of the selector will be the first item of the list.

        :param items: New selector items; format ``[('Item1', a, b, c...), ('Item2', d, e, f...)]``
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
            self._readonly_check_mouseover(events)
            return False

        for event in events:

            if event.type == pygame.KEYDOWN:  # Check key is valid
                if self._ignores_keyboard_nonphysical() and not check_key_pressed_valid(event):
                    continue

            # Check mouse over
            self._check_mouseover(event)

            # Events
            keydown = self._keyboard_enabled and event.type == pygame.KEYDOWN
            joy_hatmotion = self._joystick_enabled and event.type == pygame.JOYHATMOTION
            joy_axismotion = self._joystick_enabled and event.type == pygame.JOYAXISMOTION
            joy_button_down = self._joystick_enabled and event.type == pygame.JOYBUTTONDOWN

            # Left button
            if keydown and self._ctrl.left(event, self) or \
                    joy_hatmotion and self._ctrl.joy_left(event, self) or \
                    joy_axismotion and self._ctrl.joy_axis_x_left(event, self):
                self._left()
                return True

            # Right button
            elif keydown and self._ctrl.right(event, self) or \
                    joy_hatmotion and self._ctrl.joy_right(event, self) or \
                    joy_axismotion and self._ctrl.joy_axis_x_right(event, self):
                self._right()
                return True

            # Press enter
            elif keydown and self._ctrl.apply(event, self) or \
                    joy_button_down and self._ctrl.joy_select(event, self):
                self._sound.play_key_add()
                self.apply(*self._items[self._index][1:])
                return True

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
                    mouse_x, _ = event_pos
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
                        return True

        return False


class SelectorManager(AbstractWidgetManager, ABC):
    """
    Selector manager.
    """

    def selector(
            self,
            title: Any,
            items: Union[List[Tuple[Any, ...]], List[str]],
            default: int = 0,
            onchange: CallbackType = None,
            onreturn: CallbackType = None,
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            selector_id: str = '',
            style: SelectorStyleType = SELECTOR_STYLE_CLASSIC,
            **kwargs
    ) -> 'pygame_menu.widgets.Selector':
        """
        Add a selector to the Menu: several items and two functions that are
        executed when changing the selector (left/right) and pressing return
        (apply) on the selected item.

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

        If ``onselect`` is defined, the callback is executed as follows, where
        ``selected`` is a boolean representing the selected status:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over
            - ``float``                         (bool) - If ``True`` the widget don't contribute width/height to the Menu widget positioning computation, and don't add one unit to the rows
            - ``float_origin_position``         (bool) - If ``True`` the widget position is set to the top-left position of the Menu if the widget is floating
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``readonly_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode
            - ``readonly_selected_color``       (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode and is selected
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect
            - ``shadow_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget shadow
            - ``shadow_radius``                 (int) - Border radius of the shadow
            - ``shadow_type``                   (str) - Shadow type, it can be ``'rectangular'`` or ``'ellipse'``
            - ``shadow_width``                  (int) - Width of the shadow. If ``0`` the shadow is disabled
            - ``style_fancy_arrow_color``       (tuple, list, str, int, :py:class:`pygame.Color`) – Arrow color of fancy style
            - ``style_fancy_arrow_margin``      (tuple, list) – Margin of arrows on x-axis and y-axis in px; format: (left, right, vertical)
            - ``style_fancy_bgcolor``           (tuple, list, str, int, :py:class:`pygame.Color`) – Background color of fancy style
            - ``style_fancy_bordercolor``       (tuple, list, str, int, :py:class:`pygame.Color`) – Border color of fancy style
            - ``style_fancy_borderwidth``       (int) – Border width of fancy style; ``1`` by default
            - ``style_fancy_box_inflate``       (tuple, list) – Box inflate of fancy style on x-axis and y-axis (x, y) in px
            - ``style_fancy_box_margin``        (tuple, list) – Box margin on x-axis and y-axis (x, y) in fancy style from title in px
            - ``tab_size``                      (int) – Width of a tab character

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Title of the selector
        :param items: Item list of the selector; format ``[('Item1', a, b, c...), ('Item2', d, e, f...)]``
        :param default: Index of default item to display
        :param onchange: Callback executed when changing the selector
        :param onreturn: Callback executed when pressing return (apply)
        :param onselect: Callback executed when selecting the widget
        :param selector_id: ID of the selector
        :param style: Selector style (visual)
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Selector`
        """
        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        # Get fancy style attributes
        style_fancy_arrow_color = kwargs.pop('style_fancy_arrow_color', self._theme.widget_box_arrow_color)
        style_fancy_arrow_margin = kwargs.pop('style_fancy_arrow_margin', self._theme.widget_box_arrow_margin)
        style_fancy_bgcolor = kwargs.pop('style_fancy_bgcolor', self._theme.widget_box_background_color)
        style_fancy_bordercolor = kwargs.pop('style_fancy_bordercolor', self._theme.widget_box_border_color)
        style_fancy_borderwidth = kwargs.pop('style_fancy_borderwidth', self._theme.widget_box_border_width)
        style_fancy_box_inflate = kwargs.pop('style_fancy_box_inflate', self._theme.widget_box_inflate)
        style_fancy_box_margin = kwargs.pop('style_fancy_box_margin', self._theme.widget_box_margin)

        widget = Selector(
            default=default,
            items=items,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            selector_id=selector_id,
            style=style,
            style_fancy_arrow_color=style_fancy_arrow_color,
            style_fancy_arrow_margin=style_fancy_arrow_margin,
            style_fancy_bgcolor=style_fancy_bgcolor,
            style_fancy_bordercolor=style_fancy_bordercolor,
            style_fancy_borderwidth=style_fancy_borderwidth,
            style_fancy_box_inflate=style_fancy_box_inflate,
            style_fancy_box_margin=style_fancy_box_margin,
            title=title,
            **kwargs
        )

        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget
