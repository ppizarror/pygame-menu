"""
pygame-menu
https://github.com/ppizarror/pygame-menu

MENU
Menu class.

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
# File constants no. 0

__all__ = ['Menu']

from uuid import uuid4
import os
import sys
import time
import warnings

import pygame
import pygame.gfxdraw as gfxdraw
import pygame_menu.controls as _controls
import pygame_menu.events as _events
import pygame_menu.locals as _locals
import pygame_menu.themes as _themes
import pygame_menu.utils as _utils
import pygame_menu.widgets as _widgets
from pygame_menu._widgetmanager import WidgetManager
from pygame_menu._decorator import Decorator
from pygame_menu.scrollarea import ScrollArea, get_scrollbars_from_position
from pygame_menu.sound import Sound

# Import types
from pygame_menu._types import Callable, Any, Dict, NumberType, VectorType, Vector2NumberType, \
    Union, Tuple, List, Vector2IntType, Vector2BoolType, Tuple4Tuple2IntType, Tuple2IntType, \
    MenuColumnMaxWidthType, MenuColumnMinWidthType, MenuRowsType, Optional, Tuple2BoolType

# Joy events
JOY_EVENT_LEFT = 1
JOY_EVENT_RIGHT = 2
JOY_EVENT_UP = 4
JOY_EVENT_DOWN = 8


class Menu(object):
    """
    Menu object.

     Menu can receive many callbacks; callbacks ``onclose`` and ``onreset`` are fired
    (if them are callable-type). They can only receive 1 argument maximum, if so,
    the Menu instance is provided

    .. code-block:: python

        onclose() <or> onclose(Menu)
        onreset() <or> onreset(Menu)

    Callback ``onupdate`` is executed before updating the Menu, it receives the event
    list and the menu reference:

    .. code-block:: python

        onupdate(event_list, Menu)

    Callback ``onbeforeopen`` is executed before opening the Menu, it receives the
    current Menu and the next Menu.

    .. code-block:: python

        onbeforeopen(current Menu <from>, next Menu <to>)

    .. note::

        Menu cannot be copied or deepcopied.

    :param title: Title of the Menu
    :param width: Width of the Menu (px)
    :param height: Height of the Menu (px)
    :param center_content: Auto centers the Menu on the vertical position after a widget is added/deleted
    :param column_max_width: List/Tuple representing the maximum width of each column in px, ``None`` equals no limit. For example ``column_max_width=500`` (each column width can be 500px max), or ``column_max_width=(400,500)`` (first column 400px, second 500). If ``0`` uses the Menu width. This method does not resize the widgets, only determines the dynamic width of the column layout
    :param column_min_width: List/Tuple representing the minimum width of each column in px. For example ``column_min_width=500`` (each column width is 500px min), or ``column_max_width=(400,500)`` (first column 400px, second 500). Negative values are not accepted
    :param columns: Number of columns
    :param enabled: Menu is enabled. If ``False`` Menu cannot be drawn or updated
    :param joystick_enabled: Enable/disable joystick on the Menu
    :param menu_id: ID of the Menu
    :param menu_position: Position in *(x, y)* axis (%) respect to the window size
    :param mouse_enabled: Enable/disable mouse click inside the Menu
    :param mouse_motion_selection: Select widgets using mouse motion. If ``True`` menu draws a ``focus`` on the selected widget
    :param mouse_visible: Set mouse visible on Menu
    :param onclose: Event or function executed when closing the Menu. If not ``None`` the menu disables and executes the event or function it points to. If a function (callable) is provided it can be both non-argument or single argument (Menu instance)
    :param onreset: Function executed when resetting the Menu. The function must be non-argument or single argument (Menu instance)
    :param onupdate: Function executed when updating the Menu. The function receives the list of gathered pygame events, and the Menu reference
    :param overflow: Enables overflow in x/y axes. If ``False`` then scrollbars will not work and the maximum width/height of the scrollarea is the same as the Menu container. Style: *(overflow_x, overflow_y)*
    :param rows: Number of rows of each column, if there's only 1 column ``None`` can be used for no-limit. Also a tuple can be provided for defining different number of rows for each column, for example ``rows=10`` (each column can have a maximum 10 widgets), or ``rows=[2, 3, 5]`` (first column has 2 widgets, second 3, and third 5)
    :param screen_dimension: List/Tuple representing the dimensions the Menu should reference for sizing/positioning, if ``None`` pygame is queried for the display mode. This value defines the ``window_size`` of the Menu
    :param theme: Menu theme
    :param touchscreen: Enable/disable touch action inside the Menu. Only available on pygame 2
    :param touchscreen_motion_selection: Select widgets using touchscreen motion. If ``True`` menu draws a ``focus`` on the selected widget
    """
    _attributes: Dict[str, Any]
    _auto_centering: bool
    _background_function: Tuple[bool, Optional[Union[Callable[['Menu'], Any], Callable[[], Any]]]]
    _clock: 'pygame.time.Clock'
    _column_max_width: VectorType
    _column_min_width: VectorType
    _column_pos_x: List[NumberType]
    _column_widths: List[NumberType]
    _columns: int
    _current: 'Menu'
    _decorator: 'Decorator'
    _enabled: bool
    _height: int
    _id: str
    _index: int
    _joy_event: int
    _joy_event_repeat: int
    _joystick: bool
    _max_row_column_elements: int
    _menubar: '_widgets.MenuBar'
    _mouse: bool
    _mouse_motion_selection: bool
    _mouse_visible: bool
    _mouse_visible_default: bool
    _onbeforeopen: Optional[Callable[['Menu', 'Menu'], Any]]
    _onclose: Optional[Union['_events.MenuAction', Callable[[], Any], Callable[['Menu'], Any]]]
    _onreset: Optional[Union[Callable[[], Any], Callable[['Menu'], Any]]]
    _onupdate: Optional[Callable[[List['pygame.event.Event'], 'Menu'], Any]]
    _overflow: Tuple2BoolType
    _position: Tuple2IntType
    _prev: Optional[List[Union['Menu', List['Menu']]]]
    _runtime_errors: '_MenuRuntimeErrorConfig'
    _scroll: 'ScrollArea'
    _scrollarea_margin: List[int]
    _sound: 'Sound'
    _stats: '_MenuStats'
    _submenus: List['Menu']
    _theme: '_themes.Theme'
    _top: 'Menu'
    _touchscreen: bool
    _touchscreen_motion_selection: bool
    _used_columns: int
    _widget_columns: Dict[int, List['_widgets.core.Widget']]
    _widget_max_position: Tuple2IntType
    _widget_min_position: Tuple2IntType
    _widget_offset: List[int]
    _widget_surface_cache_enabled: bool
    _widget_surface_cache_need_update: bool
    _widgets: List['_widgets.core.Widget']
    _widgets_surface: Optional['pygame.Surface']
    _widgets_surface_last: Tuple[int, int, Optional['pygame.Surface']]
    _widgets_surface_need_update: bool
    _width: int
    _window_size: Tuple2IntType
    add: 'WidgetManager'
    disable_draw: bool
    disable_update: bool

    def __init__(self,
                 title: str,
                 width: NumberType,
                 height: NumberType,
                 center_content: bool = True,
                 column_max_width: MenuColumnMaxWidthType = None,
                 column_min_width: MenuColumnMinWidthType = 0,
                 columns: int = 1,
                 enabled: bool = True,
                 joystick_enabled: bool = True,
                 menu_id: str = '',
                 menu_position: Vector2NumberType = (50, 50),
                 mouse_enabled: bool = True,
                 mouse_motion_selection: bool = False,
                 mouse_visible: bool = True,
                 onbeforeopen: Optional[Callable[['Menu', 'Menu'], Any]] = None,
                 onclose: Optional[Union['_events.MenuAction', Callable[[], Any], Callable[['Menu'], Any]]] = None,
                 onreset: Optional[Union[Callable[[], Any], Callable[['Menu'], Any]]] = None,
                 onupdate: Optional[Callable[[List['pygame.event.Event'], 'Menu'], Any]] = None,
                 overflow: Vector2BoolType = (True, True),
                 rows: MenuRowsType = None,
                 screen_dimension: Optional[Vector2IntType] = None,
                 theme: '_themes.Theme' = _themes.THEME_DEFAULT.copy(),
                 touchscreen: bool = False,
                 touchscreen_motion_selection: bool = False
                 ) -> None:
        assert isinstance(width, (int, float))
        assert isinstance(height, (int, float))

        assert isinstance(center_content, bool)
        assert isinstance(column_max_width, (tuple, list, type(None), int, float))
        assert isinstance(column_min_width, (tuple, list, int, float))
        assert isinstance(columns, int)
        assert isinstance(enabled, bool)
        assert isinstance(joystick_enabled, bool)
        assert isinstance(menu_id, str)
        assert isinstance(menu_position, (tuple, list))
        assert isinstance(mouse_enabled, bool)
        assert isinstance(mouse_motion_selection, bool)
        assert isinstance(mouse_visible, bool)
        assert isinstance(overflow, (tuple, list))
        assert isinstance(rows, (int, type(None), tuple, list))
        assert isinstance(screen_dimension, (tuple, list, type(None)))
        assert isinstance(theme, _themes.Theme), 'theme bust be an pygame_menu.themes.Theme object instance'
        assert isinstance(touchscreen, bool)
        assert isinstance(touchscreen_motion_selection, bool)

        # Assert theme
        theme.validate()

        # Assert pygame was initialized
        assert not hasattr(pygame, 'get_init') or pygame.get_init(), 'pygame is not initialized'

        # Assert python version is greater than 3.6
        assert sys.version_info >= (3, 6, 0), \
            'pygame-menu only supports python equal or greater than version 3.6.0'

        # Column/row asserts
        assert columns >= 1, \
            'the number of columns must be equal or greater than 1 (current={0})'.format(columns)
        if columns > 1:

            assert rows is not None, 'rows cannot be None if the number of columns is greater than 1'
            if isinstance(rows, int):
                msg = 'if number of columns is greater than 1 (current={0}) then the number ' \
                      'of rows must be equal or greater than 1 (current={1})'.format(columns, rows)
                assert rows >= 1, msg
                rows = [rows for _ in range(columns)]
            assert isinstance(rows, (tuple, list)), 'if rows is not an integer it must be a tuple/list'
            msg = 'the length of the rows vector must be the ' \
                  'same as the number of columns (current={0}, expected={1})'.format(len(rows), columns)
            assert len(rows) == columns, msg

            for i in rows:
                assert isinstance(i, int), 'each item of rows tuple/list must be an integer'
                assert i >= 1, 'each item of the rows tuple/list must be equal or greater than one'

        else:

            if rows is None:
                rows = 10000000  # Set rows as a big number
            else:
                assert isinstance(rows, int), 'rows cannot be a tuple/list as there\'s only 1 column'
                assert rows >= 1, \
                    'number of rows must be equal or greater than 1. If there is no limit rows must be None'
            rows = [rows]

        # Set column min width
        if isinstance(column_min_width, (int, float)):
            assert column_min_width >= 0, 'column_min_width must be equal or greater than zero'
            msg = 'column_min_width can be a single number if there is only 1 column, but ' \
                  'there is {0} columns. Thus, column_min_width should be a vector of {0} items. ' \
                  'By default a vector has been created using the same value for each column'.format(columns)
            if columns != 1:
                if column_min_width > 0:  # Ignore the default value
                    warnings.warn(msg)
                column_min_width = [column_min_width for _ in range(columns)]
            else:
                column_min_width = [column_min_width]

        msg = 'column_min_width length must be the same as the ' \
              'number of columns, but size is different {0}!={1}'.format(len(column_min_width), columns)
        assert len(column_min_width) == columns, msg
        for i in column_min_width:
            assert isinstance(i, (int, float)), \
                'each item of column_min_width must be an integer/float'
            assert i >= 0, \
                'each item of column_min_width must be equal or greater than zero'

        # Set column max width
        if column_max_width is not None:
            # if isinstance(column_max_width, (tuple, list)) and len(column_max_width) == 1:
            #     msg = 'as there is only 1 column, prefer using ' \
            #           'column_max_width as a number (int, float) instead a list/tuple'
            #     warnings.warn(msg)

            if isinstance(column_max_width, (int, float)):
                assert column_max_width >= 0, 'column_max_width must be equal or greater than zero'
                msg = 'column_max_width can be a single number if there is only 1 column, but ' \
                      'there is {0} columns. Thus, column_max_width must be a vector of {0} items. ' \
                      'By default a vector has been created using the same value for each column'.format(columns)
                if columns != 1:
                    warnings.warn(msg)
                    column_max_width = [column_max_width for _ in range(columns)]
                else:
                    column_max_width = [column_max_width]

            msg = 'column_max_width length must be the same as the ' \
                  'number of columns, but size is different {0}!={1}'.format(len(column_max_width), columns)
            assert len(column_max_width) == columns, msg

            for i in column_max_width:
                assert isinstance(i, type(None)) or isinstance(i, (int, float)), \
                    'each item of column_max_width can be None (no limit) or an integer/float'
                assert i is None or i >= 0, \
                    'each item of column_max_width must be equal or greater than zero or None'

        else:
            column_max_width = [None for _ in range(columns)]

        # Check that every column max width is equal or greater than minimum width
        for i in range(len(column_max_width)):
            if column_max_width[i] is not None:
                msg = 'item {0} of column_max_width ({1}) ' \
                      'must be equal or greater than column_min_width ' \
                      '({2})'.format(i, column_max_width[i], column_min_width[i])
                assert column_max_width[i] >= column_min_width[i], msg

        # Element size and position asserts
        _utils.assert_vector(menu_position, 2)
        assert width > 0 and height > 0, \
            'menu width and height must be greater than zero'

        # Get window size if not given explicitly
        if screen_dimension is not None:
            _utils.assert_vector(screen_dimension, 2)
            assert screen_dimension[0] > 0, 'screen width must be higher than zero'
            assert screen_dimension[1] > 0, 'screen height must be higher than zero'
            self._window_size = screen_dimension
        else:
            surface = pygame.display.get_surface()
            if surface is None:
                raise RuntimeError('pygame surface could not be retrieved, check '
                                   'if pygame.display.set_mode() was called')
            self._window_size = surface.get_size()
        self._window_size = (int(self._window_size[0]), int(self._window_size[1]))
        window_width, window_height = self._window_size
        assert width <= window_width and height <= window_height, \
            'menu size ({0}x{1}) must be lower or equal than the size of the window ({2}x{3})'.format(
                width, height, window_width, window_height)

        # Assert overflow
        assert len(overflow) == 2, 'overflow must be a 2-item tuple/list of booleans (x-axis,y-axis)'
        assert isinstance(overflow[0], bool), 'overflow in x axis must be a boolean object'
        assert isinstance(overflow[1], bool), 'overflow in y axis must be a boolean object'

        # Generate ID if empty
        if len(menu_id) == 0:
            menu_id = str(uuid4())

        # General properties of the Menu
        self._attributes = {}
        self._auto_centering = center_content
        self._background_function = (False, None)  # Accept menu as argument, callable object
        self._clock = pygame.time.Clock()
        self._decorator = Decorator(self)
        self._enabled = enabled  # Menu is enabled or not. If disabled menu can't update or draw
        self._height = int(height)
        self._id = menu_id
        self._index = -1  # Selected index, if -1 the widget does not have been selected yet
        self._onclose = None  # Function or event called on Menu close
        self._sound = Sound()
        self._stats = _MenuStats()
        self._submenus = []
        self._theme = theme
        self._width = int(width)

        # Set callbacks
        self.set_onbeforeopen(onbeforeopen)
        self.set_onclose(onclose)
        self.set_onreset(onreset)
        self.set_onupdate(onupdate)

        # Menu links (pointer to previous and next menus in nested submenus), for public methods
        # accessing self should be through "_current", because user can move through submenus
        # and self pointer should target the current Menu object. Private methods access
        # through self (not _current) because these methods are called by public (_current) or
        # by themselves. _top is only used when moving through menus (open,reset)
        self._current = self  # Current Menu

        # Prev stores a list of Menu pointers, when accessing a submenu, prev grows as
        # prev = [prev, new_pointer]
        self._prev = None

        # Top is the same for the menus and submenus if the user moves through them
        self._top = self

        # Position of Menu
        self._position = (0, 0)
        self.set_relative_position(menu_position[0], menu_position[1])

        # Menu widgets, it should not be accessed outside the object as strange issues can occur
        self.add = WidgetManager(self)
        self._widgets = []
        self._widget_offset = [theme.widget_offset[0], theme.widget_offset[1]]

        if abs(self._widget_offset[0]) < 1:
            self._widget_offset[0] *= self._width
        if abs(self._widget_offset[1]) < 1:
            self._widget_offset[1] *= self._height

        # Cast to int offset
        self._widget_offset[0] = int(self._widget_offset[0])
        self._widget_offset[1] = int(self._widget_offset[1])

        # Widget surface
        self._widgets_surface = None
        self._widgets_surface_need_update = False
        self._widgets_surface_last = (0, 0, None)

        # Precache widgets surface draw
        self._widget_surface_cache_enabled = True
        self._widget_surface_cache_need_update = True

        # If centering is enabled, but widget offset in the vertical is different than zero a warning is raised
        if self._auto_centering and self._widget_offset[1] != 0:
            msg = 'menu (title "{0}") is vertically centered (center_content=True), but widget offset (from theme) is different than zero ({1}px). Auto-centering has been disabled'
            msg = msg.format(title, self._widget_offset[1])
            warnings.warn(msg)
            self._auto_centering = False

        # Scroll area outer margin
        self._scrollarea_margin = [theme.scrollarea_outer_margin[0], theme.scrollarea_outer_margin[1]]
        if abs(self._scrollarea_margin[0]) < 1:
            self._scrollarea_margin[0] *= self._width
        if abs(self._scrollarea_margin[1]) < 1:
            self._scrollarea_margin[1] *= self._height

        self._scrollarea_margin[0] = int(self._scrollarea_margin[0])
        self._scrollarea_margin[1] = int(self._scrollarea_margin[1])

        # If centering is enabled, but scroll area margin in the vertical is different than zero a warning is raised
        if self._auto_centering and self._scrollarea_margin[1] != 0:
            msg = 'menu (title "{0}") is vertically centered (center_content=True), but scroll area outer margin (from theme) is different than zero ({1}px). Auto-centering has been disabled'
            msg = msg.format(title, round(self._scrollarea_margin[1], 3))
            warnings.warn(msg)
            self._auto_centering = False

        # Columns and rows
        for i in range(len(column_max_width)):
            if column_max_width[i] == 0:
                column_max_width[i] = width

        self._column_max_width = column_max_width
        self._column_min_width = column_min_width
        self._column_pos_x = []  # Stores the center x position of each column
        self._column_widths = []
        self._columns = columns
        self._max_row_column_elements = 0
        self._rows = rows
        self._used_columns = 0  # Total columns used in widget positioning
        self._widget_columns = {}
        self._widget_max_position = (0, 0)
        self._widget_min_position = (0, 0)

        for r in self._rows:
            self._max_row_column_elements += r

        # Init joystick
        self._joystick = joystick_enabled
        if self._joystick:
            if not pygame.joystick.get_init():
                pygame.joystick.init()
            for i in range(pygame.joystick.get_count()):
                pygame.joystick.Joystick(i).init()
        self._joy_event = 0
        self._joy_event_repeat = pygame.NUMEVENTS - 1

        # Init mouse
        if mouse_motion_selection:
            assert mouse_visible, 'mouse motion cannot be enabled if mouse is not visible'
            assert hasattr(pygame, 'MOUSEMOTION'), \
                'pygame MOUSEMOTION does not exist, thus, mouse motion selection cannot be enabled'
        self._mouse = mouse_enabled and mouse_visible
        self._mouse_motion_selection = mouse_motion_selection and mouse_visible
        self._mouse_visible = mouse_visible
        self._mouse_visible_default = mouse_visible

        # Init touchscreen
        if touchscreen:
            version_major, _, _ = pygame.version.vernum
            assert version_major >= 2, 'touchscreen is only supported in pygame v2+'
        if touchscreen_motion_selection:
            assert touchscreen, \
                'touchscreen_motion_selection cannot be enabled if touchscreen is disabled'
            assert hasattr(pygame, 'FINGERMOTION'), \
                'pygame FINGERMOTION does not exist, thus, touchscreen motion selection cannot be enabled'
        self._touchscreen = touchscreen
        self._touchscreen_motion_selection = touchscreen_motion_selection

        # Create menubar (title)
        self._menubar = _widgets.MenuBar(
            back_box=theme.title_close_button,
            background_color=self._theme.title_background_color,
            mode=self._theme.title_bar_style,
            modify_scrollarea=self._theme.title_bar_modify_scrollarea,
            offsetx=theme.title_offset[0],
            offsety=theme.title_offset[1],
            onreturn=self._back,
            title=title,
            width=self._width
        )
        self._menubar.set_menu(self)
        self._menubar.set_font(
            antialias=self._theme.title_font_antialias,
            background_color=None,
            color=self._theme.title_font_color,
            font=self._theme.title_font,
            font_size=self._theme.title_font_size,
            readonly_color=self._theme.readonly_color,
            readonly_selected_color=self._theme.readonly_selected_color,
            selected_color=self._theme.title_font_color
        )
        self._menubar.set_shadow(
            color=self._theme.title_shadow_color,
            enabled=self._theme.title_shadow,
            offset=self._theme.title_shadow_offset,
            position=self._theme.title_shadow_position
        )
        self._menubar.set_controls(self._joystick, self._mouse, self._touchscreen)
        if self._theme.title_floating:
            self._menubar.set_float()

        # Scrolling area
        menubar_height = self._menubar.get_height()
        if self._height - menubar_height <= 0:
            raise ValueError('menubar is higher than menu height. Try increasing the later value')
        self._scroll = ScrollArea(
            area_color=self._theme.background_color,
            area_height=self._height - menubar_height,
            area_width=self._width,
            extend_y=menubar_height,
            menubar=self._menubar,
            scrollbar_color=self._theme.scrollbar_color,
            scrollbar_slider_color=self._theme.scrollbar_slider_color,
            scrollbar_slider_pad=self._theme.scrollbar_slider_pad,
            scrollbar_thick=self._theme.scrollbar_thick,
            scrollbars=get_scrollbars_from_position(self._theme.scrollarea_position),
            shadow=self._theme.scrollbar_shadow,
            shadow_color=self._theme.scrollbar_shadow_color,
            shadow_offset=self._theme.scrollbar_shadow_offset,
            shadow_position=self._theme.scrollbar_shadow_position
        )
        self._scroll.set_menu(self)
        self._overflow = tuple(overflow)

        # Controls the behaviour of runtime errors
        self._runtime_errors = _MenuRuntimeErrorConfig()

        # Public properties. These can be changed without any major problem
        self.disable_draw = False
        self.disable_update = False

    def __copy__(self) -> 'Menu':
        """
        Copy method.

        :return: Raises copy exception
        """
        raise _MenuCopyException('Menu class cannot be copied')

    def __deepcopy__(self, memodict: Dict) -> 'Menu':
        """
        Deepcopy method.

        :param memodict: Memo dict
        :return: Raises copy exception
        """
        raise _MenuCopyException('Menu class cannot be deep-copied')

    def force_surface_update(self) -> 'Menu':
        """
        Forces current Menu surface update after next rendering call.

        ..note ::

            This method is expensive, as menu surface update forces re-rendering of
            all widgets (because them can change in size, position, etc...).

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.Menu.get_current`,
            for example, ``menu.get_current().update(...)``

        :return: Self reference
        """
        self._current._widgets_surface_need_update = True
        return self

    def force_surface_cache_update(self) -> 'Menu':
        """
        Forces current Menu surface cache to update after next drawing call.

        .. note::

            This method only updates the surface cache, without forcing re-rendering
            of all Menu widgets.

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.Menu.get_current`,
            for example, ``menu.get_current().update(...)``

        :return: Self reference
        """
        self._current._widget_surface_cache_need_update = True
        self._current._decorator.force_cache_update()
        return self

    def set_onbeforeopen(self,
                         onbeforeopen: Optional[Callable[['Menu', 'Menu'], Any]]
                         ) -> 'Menu':
        """
        Set ``onbeforeopen`` callback.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param onbeforeopen: Onbeforeopen callback, it can be a function or None
        :return: Self reference
        """
        assert _utils.is_callable(onbeforeopen) or onbeforeopen is None, \
            'onbeforeopen must be callable (function-type) or None'
        self._onbeforeopen = onbeforeopen
        return self

    def set_onupdate(self,
                     onupdate: Optional[Callable[[List['pygame.event.Event'], 'Menu'], Any]]
                     ) -> 'Menu':
        """
        Set ``onupdate`` callback.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param onupdate: Onupdate callback, it can be a function or None
        :return: Self reference
        """
        assert _utils.is_callable(onupdate) or onupdate is None, \
            'onupdate must be a callable (function-type) or None'
        self._onupdate = onupdate
        return self

    def set_onclose(self,
                    onclose: Optional[Union['_events.MenuAction', Callable[[], Any], Callable[['Menu'], Any]]]
                    ) -> 'Menu':
        """
        Set ``onclose`` callback.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param onclose: Onclose callback, it can be a function, an event, or None
        :return: Self reference
        """
        assert _utils.is_callable(onclose) or _events.is_event(onclose) or onclose is None, \
            'onclose must be a MenuAction, callable (function-type) or None'
        if onclose == _events.NONE:
            onclose = None
        self._onclose = onclose
        return self

    def set_onreset(self,
                    onreset: Optional[Union[Callable[[], Any], Callable[['Menu'], Any]]]
                    ) -> 'Menu':
        """
        Set ``onreset`` callback.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param onreset: Onreset callback, it can be a function or None
        :return: Self reference
        """
        assert _utils.is_callable(onreset) or onreset is None, \
            'onreset must be a callable (function-type) or None'
        self._onreset = onreset
        return self

    def get_current(self) -> 'Menu':
        """
        Get **current** active Menu. If the user has not opened any submenu
        the pointer object must be the same as the base. If not, this
        will return the opened Menu pointer.

        :return: Menu object **(current)**
        """
        return self._current

    @staticmethod
    def _warn_widgetmanager(method: str, new_method: str) -> None:
        """
        Warn about a deprecated method.

        :param method: Method's name to warn about
        :param new_method: New method's
        :return: None
        """
        warnings.warn('Menu method {} is deprecated. Use menu.add.{} instead, (see docs). '
                      'This method will be removed in v4.1'.format(method, new_method))

    def add_button(self, *args, **kwargs) -> '_widgets.Button':
        """
        Use py:meth:`pygame_menu._widgetmanager.WidgetManager.button` instead. This
        method shorthand will be removed in version 4.1.
        """
        self._warn_widgetmanager('add_button', 'button')
        return self.add.button(*args, **kwargs)

    def add_color_input(self, *args, **kwargs) -> '_widgets.ColorInput':
        """
        Use py:meth:`pygame_menu._widgetmanager.WidgetManager.color_input` instead. This
        method shorthand will be removed in version 4.1.
        """
        self._warn_widgetmanager('add_color_input', 'color_input')
        return self.add.color_input(*args, **kwargs)

    def add_image(self, *args, **kwargs) -> '_widgets.Image':
        """
        Use py:meth:`pygame_menu._widgetmanager.WidgetManager.image` instead. This
        method shorthand will be removed in version 4.1.
        """
        self._warn_widgetmanager('add_image', 'image')
        return self.add.image(*args, **kwargs)

    def add_label(self, *args, **kwargs) -> Union['_widgets.Label', List['_widgets.Label']]:
        """
        Use py:meth:`pygame_menu._widgetmanager.WidgetManager.image` instead. This
        method shorthand will be removed in version 4.1.
        """
        self._warn_widgetmanager('add_label', 'label')
        return self.add.label(*args, **kwargs)

    def add_selector(self, *args, **kwargs) -> '_widgets.Selector':
        """
        Use py:meth:`pygame_menu._widgetmanager.WidgetManager.selector` instead. This
        method shorthand will be removed in version 4.1.
        """
        self._warn_widgetmanager('add_selector', 'selector')
        return self.add.selector(*args, **kwargs)

    def add_toggle_switch(self, *args, **kwargs) -> '_widgets.ToggleSwitch':
        """
        Use py:meth:`pygame_menu._widgetmanager.WidgetManager.toggle_switch` instead. This
        method shorthand will be removed in version 4.1.
        """
        self._warn_widgetmanager('add_toggle_switch', 'toggle_switch')
        return self.add.toggle_switch(*args, **kwargs)

    def add_text_input(self, *args, **kwargs) -> '_widgets.TextInput':
        """
        Use py:meth:`pygame_menu._widgetmanager.WidgetManager.text_input` instead. This
        method shorthand will be removed in version 4.1.
        """
        self._warn_widgetmanager('add_text_input', 'text_input')
        return self.add.text_input(*args, **kwargs)

    def add_vertical_margin(self, *args, **kwargs) -> '_widgets.VMargin':
        """
        Use py:meth:`pygame_menu._widgetmanager.WidgetManager.vertical_margin` instead. This
        method shorthand will be removed in version 4.1.
        """
        self._warn_widgetmanager('add_vertical_margin', 'vertical_margin')
        return self.add.vertical_margin(*args, **kwargs)

    def add_none_widget(self, *args, **kwargs) -> '_widgets.NoneWidget':
        """
        Use py:meth:`pygame_menu._widgetmanager.WidgetManager.none_widget` instead. This
        method shorthand will be removed in version 4.1.
        """
        self._warn_widgetmanager('add_none_widget', 'none_widget')
        return self.add.none_widget(*args, **kwargs)

    def add_generic_widget(self, *args, **kwargs) -> '_widgets.core.Widget':
        """
        Use py:meth:`pygame_menu._widgetmanager.WidgetManager.generic_widget` instead. This
        method shorthand will be removed in version 4.1.
        """
        self._warn_widgetmanager('add_generic_widget', 'generic_widget')
        return self.add.generic_widget(*args, **kwargs)

    def select_widget(self, widget: '_widgets.core.Widget') -> 'Menu':
        """
        Select a widget from the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param widget: Widget to be selected
        :return: Self reference
        """
        assert isinstance(widget, _widgets.core.Widget)
        if not widget.is_selectable:
            raise ValueError('widget is not selectable')
        if not widget.is_visible():
            raise ValueError('widget is not visible')
        try:
            index = self._widgets.index(widget)  # If not exists this raises ValueError
        except ValueError:
            raise ValueError('widget is not in Menu, check if exists on the current '
                             'with menu.get_current().remove_widget(widget)')
        self._select(index)
        return self

    def remove_widget(self, widget: '_widgets.core.Widget') -> 'Menu':
        """
        Remove the ``widget`` from the Menu. If widget not exists on Menu this
        method raises a ``ValueError`` exception.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param widget: Widget object
        :return: Self reference
        """
        assert isinstance(widget, _widgets.core.Widget)

        try:
            index = self._widgets.index(widget)  # If not exists this raises ValueError
        except ValueError:
            raise ValueError('widget is not in Menu, check if exists on the current '
                             'with menu.get_current().remove_widget(widget)')
        self._widgets.pop(index)
        self._update_after_remove_or_hidden(index)
        self._stats.removed_widgets += 1
        widget.set_menu(None)  # Removes Menu reference from widget
        return self

    def get_sound(self) -> 'Sound':
        """
        Return the Menu sound engine.

        :return: Sound API
        """
        return self._sound

    def _update_after_remove_or_hidden(self, index: int, update_surface: bool = True) -> None:
        """
        Update widgets after removal or hidden.

        :param index: Removed index, if ``-1`` then select next index, if equal to ``self._index`` select the same
        :param update_surface: Updates Menu surface
        :return: None
        """
        # Check if there's more selectable widgets
        nselect = 0
        last_selectable = 0
        for indx in range(len(self._widgets)):
            wid = self._widgets[indx]
            if wid.is_selectable and wid.is_visible():
                nselect += 1
                last_selectable = indx

        if nselect == 0:
            self._index = -1  # Any widget is selected
        elif nselect == 1:
            self._select(last_selectable)  # Select the unique selectable option
        elif nselect > 1:
            if index == -1:  # Index was hidden
                self._select(self._index + 1)
            elif self._index > index:  # If the selected widget was after this
                self._select(self._index - 1)
            else:
                self._select(self._index)
        self._update_widget_position()
        if update_surface:
            self._widgets_surface = None  # If added on execution time forces the update of the surface

    def _back(self) -> None:
        """
        Go to previous Menu or close if top Menu is currently displayed.

        :return: None
        """
        if self._top._prev is not None:
            self.reset(1)
        else:
            self._close()

    def _update_selection_if_hidden(self) -> None:
        """
        Updates Menu widget selection if a widget was hidden.

        :return: None
        """
        if len(self._widgets) > 0:
            if self._index != -1:
                selected_widget = self._widgets[self._index % len(self._widgets)]
                if not selected_widget.is_visible():
                    selected_widget.select(False)  # Unselect
                    self._update_after_remove_or_hidden(-1, update_surface=False)
            else:
                self._update_after_remove_or_hidden(0, update_surface=False)

    def _update_widget_position(self) -> None:
        """
        Update the position of each widget.

        :return: None
        """
        # Store widget rects
        widget_rects = {}
        for widget in self._widgets:
            widget_rects[widget.get_id()] = widget.get_rect()

        # Column widgets
        self._widget_columns = {}
        for i in range(self._columns):
            self._widget_columns[i] = []

        # Set the column widths (minimum values)
        self._column_widths = [self._column_min_width[i] for i in range(self._columns)]

        # Set column/row of each widget and compute maximum width of each column if None
        self._used_columns = 0
        max_elements_msg = 'total visible/non-floating widgets cannot exceed columns*rows ({0} elements). ' \
                           'Menu position update failed'.format(self._max_row_column_elements)
        i_index = 0
        for index in range(len(self._widgets)):
            widget = self._widgets[index]

            # If not visible, continue to the next widget
            if not widget.is_visible():
                widget.set_col_row_index(-1, -1, index)
                continue

            # Check if the maximum number of elements was reached, if so raise an exception
            assert i_index < self._max_row_column_elements, max_elements_msg

            # Set the widget column/row position
            row = i_index
            col = 0
            max_rows = 0
            for col in range(self._columns):  # Find which column it belongs to
                max_rows += self._rows[col]
                if i_index < max_rows:
                    break
                row -= self._rows[col]  # Subtract the number of rows of such column

            widget.set_col_row_index(col, row, index)
            self._widget_columns[col].append(widget)

            # Update used columns
            self._used_columns = max(self._used_columns, col + 1)

            # Get the next widget, if don't exist use the same
            next_widget = widget
            if index < len(self._widgets) - 1:
                next_widget = self._widgets[index + 1]

            # If widget is floating don't update the next
            if not next_widget.is_floating():
                i_index += 1

            # If floating, don't contribute to the column width
            else:
                continue

            self._column_widths[col] = max(
                self._column_widths[col],
                widget.get_width(apply_selection=True)
            )

        # Apply max width column limit
        for col in range(self._used_columns):
            if self._column_max_width[col] is not None:
                self._column_widths[col] = min(self._column_widths[col], self._column_max_width[col])

        # If some columns were not used, set these widths to zero
        for col in range(self._used_columns, self._columns):
            self._column_widths.pop()
            del self._widget_columns[col]

        # If the total weight is less than the window width (so there's no horizontal scroll), scale the columns
        # only None column_max_widths and columns less than the maximum are scaled
        sum_width_columns = sum(self._column_widths)
        max_width = self.get_width()
        if 0 <= sum_width_columns < max_width and len(self._widgets) > 0:

            # First, scale columns to its maximum
            sum_contrib = []
            for col in range(self._used_columns):
                if self._column_max_width[col] is None:
                    sum_contrib.append(0)
                elif self._column_widths[col] < self._column_max_width[col]:
                    sum_contrib.append(self._column_max_width[col] - self._column_widths[col])
                else:
                    sum_contrib.append(0)

            delta = max_width - sum(sum_contrib) - sum_width_columns
            if delta < 0:  # Scale contrib back
                scale = (max_width - sum_width_columns) / sum(sum_contrib)
                sum_contrib = [sum_contrib[i] * scale for i in range(len(sum_contrib))]

            # Increase to its maximums
            for col in range(self._used_columns):
                if sum_contrib[col] > 0:
                    self._column_widths[col] += sum_contrib[col]

            # Scale column widths if None
            sum_width_columns = sum(self._column_widths)
            sum_contrib = []
            for col in range(self._used_columns):
                if self._column_max_width[col] is None:
                    sum_contrib.append(self._column_widths[col])
                else:
                    sum_contrib.append(0)

            delta = max_width - sum_width_columns
            if delta > 0:
                for col in range(self._used_columns):
                    if sum_contrib[col] > 0:
                        self._column_widths[col] += delta * sum_contrib[col] / sum(sum_contrib)

            # Re-compute sum
            sum_width_columns = sum(self._column_widths)

            # If column width still 0, set all the column the same width (only used)
            # This only can happen if column_min_width was not set
            if sum_width_columns < max_width and self._used_columns >= 1:

                # The width it would be added for each column
                modwidth = max_width  # Available left width for non max columns
                nonmax = self._used_columns

                # First fill all maximum width columns
                for col in range(self._used_columns):
                    if self._column_max_width[col] is not None:
                        self._column_widths[col] = min(self._column_max_width[col], max_width / self._used_columns)
                        modwidth -= self._column_widths[col]
                        nonmax -= 1

                # Now, update the rest (non maximum set)
                if nonmax > 0:
                    for col in range(self._used_columns):
                        if self._column_max_width[col] is None:
                            self._column_widths[col] = modwidth / nonmax

        # Final column width
        total_col_width = sum(self._column_widths)
        if self._used_columns > 1:
            # Calculate column width scale (weights)
            column_weights = tuple(
                float(self._column_widths[i]) / max(total_col_width, 1) for i in range(self._used_columns))

            # Calculate the position of each column
            self._column_pos_x = []
            cumulative = 0
            for i in range(self._used_columns):
                w = column_weights[i]
                self._column_pos_x.append(total_col_width * (cumulative + 0.5 * w))
                cumulative += w
        else:
            self._column_pos_x = [total_col_width * 0.5]
            self._column_widths = [total_col_width]

        # Update title position
        self._menubar.set_position(self._position[0], self._position[1])

        # Widget max/min position
        min_max_updated = False
        max_x, max_y = -1e8, -1e8
        min_x, min_y = 1e8, 1e8

        # Update appended widgets
        for index in range(len(self._widgets)):
            widget = self._widgets[index]
            rect = widget_rects[widget.get_id()]
            selection_effect = widget.get_selection_effect()

            if not widget.is_visible():
                widget.set_position(0, 0)
                continue

            # Get column and row position
            col, row, _ = widget.get_col_row_index()

            # Calculate X position
            column_width = self._column_widths[col]
            selection_margin = 0
            align = widget.get_alignment()
            if align == _locals.ALIGN_CENTER:
                dx = -widget.get_width() / 2
            elif align == _locals.ALIGN_LEFT:
                selection_margin = selection_effect.get_margin()[1]  # left
                dx = -column_width / 2 + selection_margin
            elif align == _locals.ALIGN_RIGHT:
                selection_margin = selection_effect.get_margin()[3]  # right
                dx = column_width / 2 - rect.width - selection_margin
            else:
                dx = 0
            x_coord = self._column_pos_x[col] + dx + widget.get_margin()[0] + widget.get_padding()[3]
            x_coord = max(selection_margin, x_coord)
            x_coord += max(0, self._widget_offset[0])

            # Calculate Y position
            ysum = 1  # Compute the total height from the current row position to the top of the column
            for rwidget in self._widget_columns[col]:
                _, r, _ = rwidget.get_col_row_index()
                if r >= row:
                    break
                if rwidget.is_visible() and not rwidget.is_floating():
                    ysum += widget_rects[rwidget.get_id()].height  # Height
                    ysum += rwidget.get_margin()[1]  # Vertical margin (bottom)

                    # If no widget is before add the selection effect
                    yselh = rwidget.get_selection_effect().get_margin()[0]
                    if r == 0 and self._widget_offset[1] <= yselh:
                        if rwidget.is_selectable:
                            ysum += yselh - self._widget_offset[1]

            # If the widget offset is zero, then add the selection effect to the height
            # of the widget to avoid visual glitches
            yselh = widget.get_selection_effect().get_margin()[0]
            if ysum == 1 and self._widget_offset[1] <= yselh:  # No widget is before
                if widget.is_selectable:  # Add top margin
                    ysum += yselh - self._widget_offset[1]

            y_coord = max(0, self._widget_offset[1]) + ysum + widget.get_padding()[0]

            # Update the position of the widget
            widget.set_position(int(x_coord), int(y_coord))

            # Update max/min position, minus padding
            min_max_updated = True
            max_x = max(max_x, x_coord + rect.width - widget.get_padding()[1])  # minus right padding
            max_y = max(max_y, y_coord + rect.height - widget.get_padding()[2])  # minus bottom padding
            min_x = min(min_x, x_coord - widget.get_padding()[3])
            min_y = min(min_y, y_coord - widget.get_padding()[0])

        # Update position
        if min_max_updated:
            self._widget_max_position = (max_x, max_y)
            self._widget_min_position = (min_x, min_y)
        else:
            self._widget_max_position = (0, 0)
            self._widget_min_position = (0, 0)

        self._stats.position_update += 1

    def _build_widget_surface(self) -> None:
        """
        Create the surface used to draw widgets according the required width and height.

        :return: None
        """
        self._stats.build_surface += 1
        t0 = time.time()

        # Update internals
        self._update_selection_if_hidden()
        self._update_widget_position()

        menubar_height = self._menubar.get_height()
        max_x, max_y = self._widget_max_position

        # Get scrollbars size
        sx = self._scroll.get_scrollbar_thickness(_locals.ORIENTATION_HORIZONTAL, real=True)
        sy = self._scroll.get_scrollbar_thickness(_locals.ORIENTATION_VERTICAL, real=True)

        # Remove the thick of the scrollbar to avoid displaying an horizontal one
        # If overflow in both axis
        if max_x > self._width and max_y > self._height - menubar_height:
            width, height = max_x + sy * 0.5, max_y + sx * 0.25
            if not self._mouse_visible:
                self._mouse_visible = True

        # If horizontal overflow
        elif max_x > self._width:
            width, height = max_x + 0.5 * sx, self._height - menubar_height - sx
            self._mouse_visible = self._mouse_visible_default

        # If vertical overflow
        elif max_y > self._height - menubar_height:
            width, height = self._width - sy, max_y + sy * 0.35
            if not self._mouse_visible:
                self._mouse_visible = True

        # No overflow
        else:
            width, height = self._width, self._height - menubar_height
            self._mouse_visible = self._mouse_visible_default

        # Checks overflow
        if not self._overflow[0]:
            width = self._width
        if not self._overflow[1]:
            height = self._height - menubar_height

        # Adds scroll area margin
        width += self._scrollarea_margin[0]
        height += self._scrollarea_margin[1]

        # Cast to int
        width = int(width)
        height = int(height)

        # Get the previous surface if the width/height is the same
        if width == self._widgets_surface_last[0] and height == self._widgets_surface_last[1]:
            self._widgets_surface = self._widgets_surface_last[2]
        else:
            self._widgets_surface = _utils.make_surface(width, height)
            self._widgets_surface_last = (width, height, self._widgets_surface)

        # Set position
        self._scroll.set_world(self._widgets_surface)
        self._scroll.set_position(self._position[0], self._position[1] + menubar_height)

        # Update times
        dt = time.time() - t0
        self._stats.total_building_time += dt
        self._stats.last_build_surface_time = dt

    def _check_id_duplicated(self, widget_id: str) -> None:
        """
        Check if widget ID is duplicated. Throws ``IndexError`` if the index is duplicated.

        :param widget_id: New widget ID
        :return: None
        """
        assert isinstance(widget_id, str)
        for widget in self._widgets:
            if widget.get_id() == widget_id:
                raise IndexError('widget ID="{0}" already exists on the current menu'.format(widget_id))

    def _close(self) -> bool:
        """
        Execute close callbacks and disable the Menu, only if ``onclose``
        is not None (or NONE event).

        :return: ``True`` if Menu has executed the ``onclose`` callback
        """
        onclose = self._onclose

        # Apply action
        if onclose is None or onclose == _events.NONE:
            return False

        else:
            # Closing disables the Menu
            self.disable()

            # If action is an event
            if _events.is_event(onclose):

                # Sort through events
                if onclose == _events.BACK:
                    self.reset(1)
                elif onclose == _events.CLOSE:
                    pass
                elif onclose == _events.EXIT:
                    self._exit()
                elif onclose == _events.RESET:
                    self.full_reset()

            # If action is callable (function)
            elif _utils.is_callable(onclose):
                try:
                    onclose(self)
                except TypeError:
                    onclose()

        return True

    def close(self) -> bool:
        """
        Closes the **current** Menu firing ``onclose`` callback. If ``callback=None`` this
        method does nothing.

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.Menu.get_current`,
            for example, ``menu.get_current().reset(...)``

        :return: None
        """
        if not self.is_enabled():
            self._current._runtime_errors.throw(self._current._runtime_errors.close, 'menu already closed')
        return self._current._close()

    def _get_depth(self) -> int:
        """
        Return the Menu depth.

        :return: Menu depth
        """
        if self._top is None:
            return 0
        prev = self._top._prev
        depth = 0
        while True:
            if prev is not None:
                prev = prev[0]
                depth += 1
            else:
                break
        return depth

    def disable(self) -> 'Menu':
        """
        Disables the Menu *(doesn't check events and draw on the surface)*.

        .. note::

            This method does not fires ``onclose`` callback. Use ``Menu.close()``
            instead.

        :return: Self reference
        """
        self._top._enabled = False
        return self

    def set_relative_position(self, position_x: NumberType, position_y: NumberType) -> 'Menu':
        """
        Set the Menu position relative to the window.

        .. note::

            - Menu left position (x) must be between 0 and 100, if 0 the margin
              is at the left of the window, if 100 the Menu is at the right
              of the window.

            - Menu top position (y) must be between 0 and 100, if 0 the margin is
              at the top of the window, if 100 the margin is at the bottom of
              the window.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param position_x: Left position of the window
        :param position_y: Top position of the window
        :return: Self reference
        """
        assert isinstance(position_x, (int, float))
        assert isinstance(position_y, (int, float))
        assert 0 <= position_x <= 100
        assert 0 <= position_y <= 100
        position_x = float(position_x) / 100
        position_y = float(position_y) / 100
        window_width, window_height = self._window_size
        self._position = (int((window_width - self._width) * position_x),
                          int((window_height - self._height) * position_y))
        self._widgets_surface = None  # This forces an update of the widgets
        return self

    def center_content(self) -> 'Menu':
        """
        Centers the content of the Menu vertically. This action rewrites ``widget_offset``.

        .. note::

            If the height of the widgets is greater than the height of the Menu,
            the drawing region will cover all Menu inner surface.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: Self reference
        """
        self._stats.center_content += 1
        if len(self._widgets) == 0:  # If this happen, get_widget_max returns an immense value
            self._widget_offset[1] = 0
            return self
        if self._widgets_surface is None:
            self._update_widget_position()  # For position (max/min)
        available = self.get_height(inner=True)
        widget_height = self.get_height(widget=True)
        if widget_height >= available:  # There's nothing to center
            if self._widget_offset[1] != 0:
                self._widgets_surface = None
                self._widget_offset[1] = 0
                return self
        new_offset = int(max(float(available - widget_height) / 2, 0))
        if abs(new_offset - self._widget_offset[1]) > 1:
            self._widget_offset[1] = new_offset
            self._widgets_surface = None  # Rebuild on the next draw
        return self

    def get_width(self, inner: bool = False, widget: bool = False) -> int:
        """
        Get menu width.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param inner: If ``True`` returns the available width (menu width minus scroll if visible)
        :param widget: If ``True`` returns the total width used by the widgets
        :return: Width in px
        """
        if widget:
            return int(self._widget_max_position[0] - self._widget_min_position[0])
        if not inner:
            return int(self._width)
        vertical_scroll = self._scroll.get_scrollbar_thickness(_locals.ORIENTATION_VERTICAL)
        return int(self._width - vertical_scroll)

    def get_height(self, inner: bool = False, widget: bool = False) -> int:
        """
        Get menu height.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param inner: If ``True`` returns the available height (menu height minus scroll and menubar)
        :param widget: If ``True`` returns the total height used by the widgets
        :return: Height in px
        """
        if widget:
            return int(self._widget_max_position[1] - self._widget_min_position[1])
        if not inner:
            return int(self._height)
        horizontal_scroll = self._scroll.get_scrollbar_thickness(_locals.ORIENTATION_HORIZONTAL)
        return int(self._height - self._menubar.get_height() - horizontal_scroll)

    def get_size(self, inner: bool = False, widget: bool = False) -> Vector2IntType:
        """
        Return the Menu size (px) as a tuple of *(width, height)*.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param inner: If ``True`` returns the available *(width, height)* (menu height minus scroll and menubar)
        :param widget: If ``True`` returns the total *(width, height)* used by the widgets
        :return: Tuple of *(width, height)* in px
        """
        return self.get_width(inner=inner, widget=widget), self.get_height(inner=inner, widget=widget)

    def render(self) -> 'Menu':
        """
        Force **current** Menu rendering. Useful to force widget update.

        .. note::

            This method should not be called if the Menu is being drawn as
            this method is called by :py:meth:`pygame_menu.Menu.draw`

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.Menu.get_current`,
            for example, ``menu.get_current().render(...)``

        :return: Self reference **(current)**
        """
        self._current._widgets_surface = None
        self._current._render()
        self._current._stats.render_public += 1
        return self

    def _render(self) -> bool:
        """
        Menu rendering.

        :return: ``True`` if the surface has changed (if it was None)
        """
        t0 = time.time()
        changed = False

        if self._widgets_surface_need_update:
            self._widgets_surface = None

        if self._widgets_surface is None:
            if self._auto_centering:
                self.center_content()
            self._build_widget_surface()
            self._stats.render_private += 1
            self._widgets_surface_need_update = False
            changed = True

        self._stats.total_rendering_time += time.time() - t0
        return changed

    def draw(self, surface: 'pygame.Surface', clear_surface: bool = False) -> 'Menu':
        """
        Draw the **current** Menu into the given surface.

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.Menu.get_current`,
            for example, ``menu.get_current().draw(...)``

        :param surface: Pygame surface to draw the Menu
        :param clear_surface: Clear surface using theme default color
        :return: Self reference **(curent)**
        """
        assert isinstance(surface, pygame.Surface)
        assert isinstance(clear_surface, bool)

        if not self.is_enabled():
            self._current._runtime_errors.throw(self._current._runtime_errors.draw, 'menu is not enabled')
            return self._current
        if self._current.disable_draw:
            return self._current

        # Render menu
        render = self._current._render()  # If True, the surface widget has changed, thus cache should change if enabled

        # Updates title
        if self._current._theme.title_updates_pygame_display and \
                pygame.display.get_caption()[0] != self._current.get_title():
            pygame.display.set_caption(self._current.get_title())

        # Clear surface
        if clear_surface:
            surface.fill(self._current._theme.surface_clear_color)

        # Call background function (set from mainloop)
        if self._top._background_function[1] is not None:
            if self._top._background_function[0]:
                self._top._background_function[1](self._current)
            else:
                self._top._background_function[1]()

        # Draw the prev decorator
        self._current._decorator.draw_prev(surface)

        # print('value', self._current.get_title(), self._current._widget_surface_cache_need_update, id(self._current._widget_surface_cache_need_update))
        # print(self._current._scroll.get_decorator()._decor)

        # Draw widgets, update cache if enabled
        if not self._current._widget_surface_cache_enabled or \
                (render or self._current._widget_surface_cache_need_update):

            # This should be update before drawing widgets. As widget
            # draw may trigger surface cache updating. Don't move this
            # line or unexpected errors may occur
            self._current._widget_surface_cache_need_update = False

            # Fill the scrolling surface (clear previous state)
            self._current._widgets_surface.fill((255, 255, 255, 0))

            # Call scrollarea draw decorator. This must be done before filling the
            # surface
            scrollarea_decorator = self._current._scroll.get_decorator()
            scrollarea_decorator.force_cache_update()
            scrollarea_decorator.draw_prev(self._current._widgets_surface)

            # Iterate through widgets and draw them
            for widget in self._current._widgets:
                if not widget.is_visible():
                    continue
                widget.draw(self._current._widgets_surface)
                if widget.is_selected():
                    widget.draw_selection(self._current._widgets_surface)

            self._current._stats.draw_update_cached += 1

        self._current._scroll.draw(surface)
        self._current._menubar.draw(surface)

        # Draw focus on selected if the widget is active
        self._current._draw_focus_widget(surface, self._current.get_selected_widget())
        self._current._decorator.draw_post(surface)
        self._current._stats.draw += 1
        return self._current

    def _draw_focus_widget(self, surface: 'pygame.Surface', widget: Optional['_widgets.core.Widget']
                           ) -> Optional[Dict[int, Tuple4Tuple2IntType]]:
        """
        Draw the focus background from a given widget. Widget must be selectable,
        active, selected. Not all widgets requests the active status, then focus may not
        be drawn.

        :param surface: Pygame surface to draw the Menu
        :param widget: Focused widget
        :return: Returns the focus region, ``None`` if the focus could not be possible
        """
        assert isinstance(surface, pygame.Surface)
        assert isinstance(widget, (_widgets.core.Widget, type(None)))

        if widget is None or not widget.active or not widget.is_selectable or not widget.is_selected() or \
                not (self._mouse_motion_selection or self._touchscreen_motion_selection) or not widget.is_visible():
            return
        window_width, window_height = self._window_size

        self._render()  # Surface may be none, then update the positioning
        rect = widget.get_rect()

        # Apply selection effect
        rect = widget.get_selection_effect().inflate(rect)
        rect = self._scroll.to_real_position(rect, visible=True)

        if rect.width == 0 or rect.height == 0:
            return

        x1, y1, x2, y2 = rect.topleft + rect.bottomright

        # Convert to integer
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        coords = {}

        if abs(y1 - y2) <= 4 or abs(x1 - x2) <= 4:
            # If the area of the selected widget is too small, draw focus over the entire menu
            # .------------------.
            # |                  |
            # |        1         |
            # |                  |
            # .------------------.
            coords[1] = (0, 0), (window_width, 0), (window_width, window_height), (0, window_height)

        else:
            # Draw 4 areas:
            # .------------------.
            # |________1_________|
            # |  2  |******|  3  |
            # |_____|******|_____|
            # |        4         |
            # .------------------.
            coords[1] = (0, 0), (window_width, 0), (window_width, y1 - 1), (0, y1 - 1)
            coords[2] = (0, y1), (x1 - 1, y1), (x1 - 1, y2 - 1), (0, y2 - 1)
            coords[3] = (x2, y1), (window_width, y1), (window_width, y2 - 1), (x2, y2 - 1)
            coords[4] = (0, y2), (window_width, y2), (window_width, window_height), (0, window_height)

        for area in coords:
            gfxdraw.filled_polygon(surface, coords[area], self._theme.focus_background_color)
        return coords

    def enable(self) -> 'Menu':
        """
        Enables Menu (can check events and draw).

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: Self reference
        """
        self._top._enabled = True
        return self

    def toggle(self) -> 'Menu':
        """
        Switch between enable/disable Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: Self reference
        """
        self._top._enabled = not self._top._enabled
        return self

    def _exit(self) -> None:
        """
        Internal exit function.

        :return: None
        """
        self.disable()
        pygame.quit()
        try:
            sys.exit(0)
        except SystemExit:
            # noinspection PyUnresolvedReferences,PyProtectedMember
            os._exit(1)
        # This should be unreachable
        exit(0)

    def is_enabled(self) -> bool:
        """
        Return ``True`` if the Menu is enabled.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: Menu enabled status
        """
        return self._top._enabled

    def _move_selected_left_right(self, pos: int) -> None:
        """
        Move selected to left/right position (column support).

        :param pos: If ``+1`` selects right column, ``-1`` left column
        :return: None
        """
        if not (pos == 1 or pos == -1):
            raise ValueError('pos must be +1 or -1')

        def _default() -> None:
            if pos == -1:
                self._select(0, 1)
            else:
                self._select(-1, -1)

        if self._used_columns > 1:

            # Get current widget
            sel_widget = self.get_selected_widget()

            # No widget is selected
            if sel_widget is None:
                return _default()

            # Get column row position
            col, row, _ = sel_widget.get_col_row_index()

            # Move column to position
            col = (col + pos) % self._used_columns

            # Get the first similar row in that column, if no widget is found then select the first widget
            for widget in self._widget_columns[col]:
                c, r, i = widget.get_col_row_index()
                if r == row:
                    return self._select(i, 1)

            # If no widget is in that column
            if len(self._widget_columns[col]) == 0:
                return _default()

            # If the number of rows in that column is less than current, select the first one
            first_widget = self._widget_columns[col][0]
            _, _, i = first_widget.get_col_row_index()
            self._select(i, 1)

        else:
            _default()

    def _handle_joy_event(self) -> None:
        """
        Handle joy events.

        :return: None
        """
        if self._joy_event & JOY_EVENT_UP:
            self._select(self._index - 1)
        if self._joy_event & JOY_EVENT_DOWN:
            self._select(self._index + 1)
        if self._joy_event & JOY_EVENT_LEFT:
            self._move_selected_left_right(-1)
        if self._joy_event & JOY_EVENT_RIGHT:
            self._move_selected_left_right(1)

    def update(self, events: List['pygame.event.Event']) -> bool:
        """
        Update the status of the Menu using external events.
        The update event is applied only on the **current** Menu.

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.Menu.get_current`,
            for example, ``menu.get_current().update(...)``

        :param events: Pygame events as a list
        :return: ``True`` if mainloop must be stopped
        """
        # Check events
        assert isinstance(events, list)

        # If menu is not enabled
        if not self.is_enabled():
            self._current._runtime_errors.throw(self._current._runtime_errors.update, 'menu is not enabled')
            return False
        self._current._stats.update += 1

        # Call onupdate callback
        if self._current._onupdate is not None:
            self._current._onupdate(events, self._current)
        if self._current.disable_update:
            return False

        # Check if window closed
        for event in events:
            if event.type == _events.PYGAME_QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and (
                    event.mod == pygame.KMOD_LALT or event.mod == pygame.KMOD_RALT)) or \
                    event.type == _events.PYGAME_WINDOWCLOSE:
                self._current._exit()
                return True

        # If any widget status changes, set the status as True
        updated = False

        # Update mouse
        pygame.mouse.set_visible(self._current._mouse_visible)

        selected_widget: Optional['_widgets.core.Widget'] = None
        if len(self._current._widgets) >= 1:
            index = self._current._index % len(self._current._widgets)
            selected_widget = self._current._widgets[index]
            if not selected_widget.is_visible() or not selected_widget.is_selectable:
                selected_widget = None

        # Update scroll bars
        if self._current._scroll.update(events):
            updated = True

        # Update the menubar, it may change the status of the widget because
        # of the button back/close
        elif self._current._menubar.update(events):
            updated = True

        # Check selected widget
        elif selected_widget is not None and selected_widget.update(events):
            updated = True

        # Check others
        else:

            # If mouse motion enabled, add the current mouse position to event list
            if self._current._mouse_motion_selection:
                mousex, mousey = pygame.mouse.get_pos()
                events.append(pygame.event.Event(pygame.MOUSEMOTION, {'pos': (mousex, mousey)}))

            for event in events:

                if event.type == pygame.KEYDOWN:
                    # Check key event is valid
                    if not _utils.check_key_pressed_valid(event):
                        continue

                    if event.key == _controls.KEY_MOVE_DOWN:
                        self._current._select(self._current._index - 1)
                        self._current._sound.play_key_add()

                    elif event.key == _controls.KEY_MOVE_UP:
                        self._current._select(self._current._index + 1)
                        self._current._sound.play_key_add()

                    elif event.key == _controls.KEY_LEFT and self._current._used_columns > 1:
                        self._current._move_selected_left_right(-1)
                        self._current._sound.play_key_add()

                    elif event.key == _controls.KEY_RIGHT and self._current._used_columns > 1:
                        self._current._move_selected_left_right(1)
                        self._current._sound.play_key_add()

                    elif event.key == _controls.KEY_BACK and self._top._prev is not None:
                        self._current._sound.play_close_menu()
                        self.reset(1)  # public, do not use _current

                    elif event.key == _controls.KEY_CLOSE_MENU:
                        self._current._sound.play_close_menu()
                        if self._current._close():
                            updated = True

                elif self._current._joystick and event.type == pygame.JOYHATMOTION:
                    if event.value == _controls.JOY_UP:
                        self._current._select(self._current._index - 1)

                    elif event.value == _controls.JOY_DOWN:
                        self._current._select(self._current._index + 1)

                    elif event.value == _controls.JOY_LEFT and self._current._used_columns > 1:
                        self._current._move_selected_left_right(-1)

                    elif event.value == _controls.JOY_RIGHT and self._current._used_columns > 1:
                        self._current._move_selected_left_right(1)

                elif self._current._joystick and event.type == pygame.JOYAXISMOTION:
                    prev = self._current._joy_event
                    self._current._joy_event = 0

                    if event.axis == _controls.JOY_AXIS_Y and event.value < -_controls.JOY_DEADZONE:
                        self._current._joy_event |= JOY_EVENT_UP

                    elif event.axis == _controls.JOY_AXIS_Y and event.value > _controls.JOY_DEADZONE:
                        self._current._joy_event |= JOY_EVENT_DOWN

                    elif event.axis == _controls.JOY_AXIS_X and event.value < -_controls.JOY_DEADZONE and \
                            self._current._used_columns > 1:
                        self._current._joy_event |= JOY_EVENT_LEFT

                    elif event.axis == _controls.JOY_AXIS_X and event.value > _controls.JOY_DEADZONE and \
                            self._current._used_columns > 1:
                        self._current._joy_event |= JOY_EVENT_RIGHT

                    if self._current._joy_event:
                        self._current._handle_joy_event()
                        if self._current._joy_event == prev:
                            pygame.time.set_timer(self._current._joy_event_repeat, _controls.JOY_REPEAT)
                        else:
                            pygame.time.set_timer(self._current._joy_event_repeat, _controls.JOY_DELAY)
                    else:
                        pygame.time.set_timer(self._current._joy_event_repeat, 0)

                elif event.type == self._current._joy_event_repeat:
                    if self._current._joy_event:
                        self._current._handle_joy_event()
                        pygame.time.set_timer(self._current._joy_event_repeat, _controls.JOY_REPEAT)
                    else:
                        pygame.time.set_timer(self._current._joy_event_repeat, 0)

                # Select widget by clicking
                elif self._current._mouse and event.type == pygame.MOUSEBUTTONDOWN and \
                        event.button in (1, 2, 3):  # Don't consider the mouse wheel (button 4 & 5)

                    # If the mouse motion selection is disabled then select a widget by clicking
                    if not self._current._mouse_motion_selection:
                        for index in range(len(self._current._widgets)):
                            widget = self._current._widgets[index]
                            if widget.is_selectable and widget.is_visible() and \
                                    self._current._scroll.collide(widget, event):
                                self._current._select(index)

                    # If mouse motion selection, clicking will disable the active state
                    # only if the user clicked outside the widget
                    else:
                        if selected_widget is not None:
                            if not self._current._scroll.collide(selected_widget, event):
                                selected_widget.active = False

                # Select widgets by mouse motion, this is valid only if the current selected widget
                # is not active and the pointed widget is selectable
                elif self._current._mouse_motion_selection and event.type == pygame.MOUSEMOTION and \
                        selected_widget is not None and not selected_widget.active:
                    for index in range(len(self._current._widgets)):
                        widget = self._current._widgets[index]
                        if widget.is_selectable and widget.is_visible() and \
                                self._current._scroll.collide(widget, event):
                            self._current._select(index)

                # Mouse events in selected widget
                elif self._current._mouse and event.type == pygame.MOUSEBUTTONUP and selected_widget is not None and \
                        event.button in (1, 2, 3):  # Don't consider the mouse wheel (button 4 & 5)
                    self._current._sound.play_click_mouse()

                    if self._current._scroll.collide(selected_widget, event):
                        new_event = pygame.event.Event(event.type, **event.dict)
                        new_event.dict['origin'] = self._current._scroll.to_real_position((0, 0))
                        new_event.pos = self._current._scroll.to_world_position(event.pos)
                        selected_widget.update((new_event,))  # This widget can change the current Menu to a submenu
                        updated = True  # It is updated
                        break

                # Touchscreen event:
                elif self._current._touchscreen and event.type == pygame.FINGERDOWN:

                    # If the touchscreen motion selection is disabled then select a widget by clicking
                    if not self._current._touchscreen_motion_selection:
                        for index in range(len(self._current._widgets)):
                            widget = self._current._widgets[index]
                            if widget.is_selectable and widget.is_visible() and \
                                    self._current._scroll.collide(widget, event):
                                self._current._select(index)

                    # If touchscreen motion selection, clicking will disable the active state
                    # only if the user clicked outside the widget
                    else:
                        if selected_widget is not None:
                            if not self._current._scroll.collide(selected_widget, event):
                                selected_widget.active = False

                # Select widgets by touchscreen motion, this is valid only if the current selected widget
                # is not active and the pointed widget is selectable
                elif self._current._touchscreen_motion_selection and event.type == pygame.FINGERMOTION and \
                        selected_widget is not None and not selected_widget.active:
                    for index in range(len(self._current._widgets)):
                        widget = self._current._widgets[index]
                        if widget.is_selectable and self._current._scroll.collide(widget, event):
                            self._current._select(index)

                # Touchscreen events in selected widget
                elif self._current._touchscreen and event.type == pygame.FINGERUP and selected_widget is not None:
                    self._current._sound.play_click_mouse()

                    if self._current._scroll.collide(selected_widget, event):
                        new_event = pygame.event.Event(pygame.MOUSEBUTTONUP, **event.dict)
                        new_event.dict['origin'] = self._current._scroll.to_real_position((0, 0))
                        finger_pos = (event.x * self._current._window_size[0],
                                      event.y * self._current._window_size[1])
                        new_event.pos = self._current._scroll.to_world_position(finger_pos)
                        selected_widget.update((new_event,))  # This widget can change the current Menu to a submenu
                        updated = True  # It is updated
                        break

        # If cache is enabled, always force a rendering (user may have have changed any status)
        if self._current._widget_surface_cache_enabled and updated:
            self._current._widget_surface_cache_need_update = True

        # A widget has closed the Menu
        if not self.is_enabled():
            updated = True

        return updated

    def mainloop(self,
                 surface: 'pygame.Surface',
                 bgfun: Optional[Union[Callable[['Menu'], Any], Callable[[], Any]]] = None,
                 **kwargs
                 ) -> 'Menu':
        """
        Main loop of the **current** Menu. In this function, the Menu handle exceptions and draw.
        The Menu pauses the application and checks :py:mod:`pygame` events itself.
        This method returns until the Menu is updated (a widget status has changed).

        The execution of the mainloop is at the current Menu level.

        .. code-block:: python

            menu = pygame_menu.Menu(...)
            menu.mainloop(surface)

        The ``bgfun`` callable (if not None) can receive 1 argument maximum, if so,
        the Menu instance is provided:

        .. code-block:: python

            draw(...):
                bgfun() <or> bgfun(Menu)

        kwargs (Optional)
            - ``clear_surface``     *(bool)* - If ``True`` surface is cleared using ``theme.surface_clear_color``
            - ``disable_loop``      *(bool)* - If ``True`` the mainloop only runs once. Use for running draw and update in a single call
            - ``fps_limit``         *(int)* - Maximum FPS of the loop. Default equals to ``theme.fps``. If ``0`` there's no limit

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.Menu.get_current`,
            for example, ``menu.get_current().mainloop(...)``

        :param surface: Pygame surface to draw the Menu
        :param bgfun: Background function called on each loop iteration before drawing the Menu
        :param kwargs: Optional keyword arguments
        :return: Self reference **(current)**
        """
        # Unpack kwargs
        clear_surface = kwargs.get('clear_surface', True)
        disable_loop = kwargs.get('disable_loop', False)
        fps_limit = kwargs.get('fps_limit', self._theme.fps)

        assert isinstance(clear_surface, bool)
        assert isinstance(disable_loop, bool)
        assert isinstance(fps_limit, (int, float))
        assert isinstance(surface, pygame.Surface)

        assert fps_limit >= 0, 'fps limit cannot be negative'

        # NOTE: For Menu accessor, use only _current, as the Menu pointer can change through the execution
        if not self.is_enabled():
            self._current._runtime_errors.throw(self._current._runtime_errors.mainloop, 'menu is not enabled')
            return self._current

        # Check background function
        bgfun_accept_menu = False
        if bgfun:
            assert _utils.is_callable(bgfun), \
                'background function must be callable (function-type) object'
            try:
                bgfun(self._current)
                bgfun_accept_menu = True
            except TypeError:
                pass

        # Store background function and force render
        self._current._background_function = (bgfun_accept_menu, bgfun)

        # Force rendering before loop
        self._current._widgets_surface = None

        # Start loop
        while True:
            self._current._stats.loop += 1
            self._current._clock.tick(fps_limit)

            # Draw the menu
            self.draw(surface=surface, clear_surface=clear_surface)

            # Gather events by Menu
            self.update(pygame.event.get())

            # Flip contents to screen
            pygame.display.flip()

            # Menu closed or disabled
            if not self.is_enabled() or disable_loop:
                return self._current

    def get_input_data(self, recursive: bool = False) -> Dict[str, Any]:
        """
        Return input data from a Menu. The results are given as a dict object.
        The keys are the ID of each element.

        With ``recursive=True`` it collect also data inside the all sub-menus.

        .. note::

            This is applied only to the base Menu (not the currently displayed),
            for such behaviour apply to :py:meth:`pygame_menu.Menu.get_current` object.

        :param recursive: Look in Menu and sub-menus
        :return: Input dict e.g.: ``{'id1': value, 'id2': value, ...}``
        """
        assert isinstance(recursive, bool)
        return self._get_input_data(recursive, depth=0)

    def _get_input_data(self, recursive: bool, depth: int) -> Dict[str, Any]:
        """
        Return input data from a Menu. The results are given as a dict object.
        The keys are the ID of each element.

        With ``recursive=True``: it collect also data inside the all sub-menus.

        :param recursive: Look in Menu and sub-menus
        :param depth: Depth of the input data
        :return: Input dict e.g.: ``{'id1': value, 'id2': value, ...}``
        """
        data = {}
        for widget in self._widgets:
            try:
                data[widget.get_id()] = widget.get_value()
            except ValueError:  # Widget does not return data
                pass
        if recursive:
            depth += 1
            for menu in self._submenus:
                data_submenu = menu._get_input_data(recursive=recursive, depth=depth)

                # Check if there is a collision between keys
                data_keys = data.keys()
                subdata_keys = data_submenu.keys()
                for key in subdata_keys:
                    if key in data_keys:
                        msg = 'collision between widget data ID="{0}" at depth={1}'.format(key, depth)
                        raise ValueError(msg)

                # Update data
                data.update(data_submenu)
        return data

    def get_rect(self) -> 'pygame.Rect':
        """
        Return the Menu rect.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: Rect
        """
        return pygame.Rect(int(self._position[0]), int(self._position[1]), int(self._width), int(self._height))

    def set_sound(self, sound: Optional['Sound'], recursive: bool = False) -> 'Menu':
        """
        Add a sound engine to the Menu. If ``recursive=True``, the sound is
        applied to all submenus.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param sound: Sound object
        :param recursive: Set the sound engine to all submenus
        :return: Self reference
        """
        assert isinstance(sound, (type(self._sound), type(None))), \
            'sound must be pygame_menu.Sound type or None'
        if sound is None:
            sound = Sound()
        self._sound = sound
        for widget in self._widgets:
            widget.set_sound(sound)
        if recursive:
            for menu in self._submenus:
                menu.set_sound(sound, recursive=True)
        return self

    def get_title(self) -> str:
        """
        Return the title of the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: Menu title
        """
        return self._menubar.get_title()

    def set_title(self, title: Any, offset: Optional[Vector2NumberType] = None) -> 'Menu':
        """
        Set the title of the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param title: New menu title
        :param offset: If ``None`` uses theme offset, else it defines the title offset in *(x, y)*
        :return: Self reference
        """
        if offset is None:
            offset = self._theme.title_offset
        else:
            _utils.assert_vector(offset, 2)
        self._menubar.set_title(title, offsetx=offset[0], offsety=offset[1])
        return self

    def full_reset(self) -> 'Menu':
        """
        Reset the Menu back to the first opened Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: Self reference
        """
        depth = self._get_depth()
        if depth > 0:
            self.reset(depth)
        return self

    def clear(self, reset: bool = True) -> 'Menu':
        """
        Clears all widgets.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param reset: If ``True`` the menu full-resets
        :return: Self reference
        """
        if reset:
            self.full_reset()
        del self._widgets[:]
        del self._submenus[:]
        self._index = -1
        self._stats.clear += 1
        self._render()
        return self

    def _open(self, menu: 'Menu') -> None:
        """
        Open the given Menu.

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.Menu.get_current`,
            for example, ``menu.get_current().reset(...)``

        :param menu: Menu object
        :return: None
        """
        current = self

        # Update pointers
        menu._top = self._top
        self._top._current = menu._current
        self._top._prev = [self._top._prev, current]

        # Call event
        if menu._onbeforeopen is not None:
            menu._onbeforeopen(current, menu)

        # Select the first widget
        self._select(0, 1)

    def reset(self, total: int) -> 'Menu':
        """
        Go back in Menu history a certain number of times from the **current** Menu.
        This method operates through the **current** Menu pointer.

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.Menu.get_current`,
            for example, ``menu.get_current().reset(...)``

        :param total: How many menus to go back
        :return: Self reference **(current)**
        """
        assert isinstance(total, int)
        assert total > 0, 'total must be greater than zero'

        i = 0
        while True:
            if self._top._prev is not None:
                prev = self._top._prev
                self._top._current = prev[1]  # This changes the "current" pointer
                self._top._prev = prev[0]  # Eventually will reach None
                i += 1
                if i == total:
                    break
            else:
                break

        # Execute onreset callback
        if self._current._onreset is not None:
            try:
                self._current._onreset(self._current)
            except TypeError:
                self._current._onreset()

        self._current._select(self._top._current._index)
        self._current._stats.reset += 1
        return self._current

    def _select(self, new_index: int, dwidget: int = 0) -> None:
        """
        Select the widget at the given index and unselect others. Selection forces
        rendering of the widget. Also play widget selection sound.

        :param new_index: Widget index
        :param dwidget: Direction to search if ``new_index`` widget is non selectable
        :return: None
        """
        curr_widget = self._top._current
        if len(curr_widget._widgets) == 0:
            return

        # This stores +/-1 if the index increases or decreases
        # Used by non-selectable selection
        if dwidget == 0:
            if new_index < curr_widget._index:
                dwidget = -1
            else:
                dwidget = 1

        # Limit the index to the length
        total_curr_widgets = len(curr_widget._widgets)
        new_index %= total_curr_widgets
        if new_index == curr_widget._index:  # Index has not changed
            return

        # Get both widgets
        if curr_widget._index >= total_curr_widgets:  # The length of the Menu changed during execution time
            for i in range(total_curr_widgets):  # Unselect all possible candidates
                curr_widget._widgets[i].select(False)
            curr_widget._index = 0

        old_widget = curr_widget._widgets[curr_widget._index]
        new_widget = curr_widget._widgets[new_index]

        # If new widget is not selectable or visible
        if not new_widget.is_selectable or not new_widget.is_visible():
            if curr_widget._index >= 0:  # There's at least 1 selectable option
                curr_widget._select(new_index + dwidget, dwidget)
                return
            else:  # No selectable options, quit
                return

        # Selecting widgets forces rendering
        old_widget.select(False)
        curr_widget._index = new_index  # Update selected index
        new_widget.select()

        # Scroll to rect
        rect = new_widget.get_rect()
        if curr_widget._index == 0:  # Scroll to the top of the Menu
            rect = pygame.Rect(int(rect.x), 0, int(rect.width), int(rect.height))

        # Get scroll thickness
        sx = self._scroll.get_scrollbar_thickness(_locals.ORIENTATION_HORIZONTAL)
        sy = self._scroll.get_scrollbar_thickness(_locals.ORIENTATION_VERTICAL)  # scroll
        col, _, _ = new_widget.get_col_row_index()
        if col != -1:  # Select widget but the menu has not been rendered yet
            rx_min = rect.x
            rect.x = self._column_pos_x[col] - self._column_widths[col] / 2
            if col > 0:
                rect.x += sx / 2
            rect.x = min(rect.x, rx_min)
            rect.width = int(max(rect.width, self._column_widths[col])) - sy
            curr_widget._scroll.scroll_to_rect(rect)

        # Play widget selection sound
        self._sound.play_widget_selection()
        self._stats.select += 1

    def get_id(self) -> str:
        """
        Return the ID of the base Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: Menu ID
        """
        return self._id

    def get_window_size(self) -> Tuple2IntType:
        """
        Return the window size (px) as a tuple of *(width, height)*.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: Window size in px
        """
        return self._window_size

    def get_widgets(self) -> Tuple['_widgets.core.Widget']:
        """
        Return the Menu widgets as a tuple.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        .. warning::

            Use with caution.

        :return: Widgets tuple
        """
        return tuple(self._widgets)

    def get_menubar_widget(self) -> '_widgets.MenuBar':
        """
        Return menubar widget.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        .. warning::

            Use with caution.

        :return: MenuBar widget
        """
        return self._menubar

    def get_scrollarea(self) -> 'ScrollArea':
        """
        Return the Menu scroll area.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        .. warning::

            Use with caution.

        :return: ScrollArea object
        """
        return self._scroll

    def get_widget(self, widget_id: str, recursive: bool = False) -> Optional['_widgets.core.Widget']:
        """
        Return a widget by a given ID from the Menu.

        With ``recursive=True`` it looks for a widget in the Menu and all sub-menus.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        .. note::

            ``None`` is returned if no widget is found.

        :param widget_id: Widget ID
        :param recursive: Look in Menu and submenus
        :return: Widget object
        """
        assert isinstance(widget_id, str)
        assert isinstance(recursive, bool)
        for widget in self._widgets:
            if widget.get_id() == widget_id:
                return widget
        if recursive:
            for menu in self._submenus:
                widget = menu.get_widget(widget_id, recursive)
                if widget:
                    return widget
        return None

    def reset_value(self, recursive: bool = False) -> 'Menu':
        """
        Reset all widget values to default.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param recursive: Set value recursively
        :return: Self reference
        """
        for widget in self._widgets:
            widget.reset_value()
        if recursive:
            for sm in self._submenus:
                sm.reset_value(recursive)
        return self

    def in_submenu(self, menu: 'Menu', recursive: bool = False) -> bool:
        """
        Return ``True`` if ``menu`` is a submenu of the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param menu: Menu to check
        :param recursive: Check recursively
        :return: ``True`` if ``menu`` is in the submenus
        """
        if menu in self._submenus:
            return True
        if recursive:
            for sm in self._submenus:
                if sm.in_submenu(menu, recursive):
                    return True
        return False

    def _remove_submenu(self, menu: 'Menu', recursive: bool = False) -> bool:
        """
        Removes Menu from submenu if ``menu`` is a submenu of the Menu.

        :param menu: Menu to remove
        :param recursive: Check recursively
        :return: ``True`` if ``menu`` was removed
        """
        if menu in self._submenus:
            self._submenus.remove(menu)
            self._update_after_remove_or_hidden(self._index)
            return True
        if recursive:
            for sm in self._submenus:
                if sm._remove_submenu(menu, recursive):
                    return True
        return False

    def get_theme(self) -> '_themes.Theme':
        """
        Return the Menu theme.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        .. warning::

            Use with caution.

        :return: Menu theme
        """
        return self._theme

    def get_clock(self) -> 'pygame.time.Clock':
        """
        Return the pygame Menu timer.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: Pygame clock object
        """
        return self._clock

    def get_index(self) -> int:
        """
        Get selected widget index from the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: Selected widget index
        """
        return self._index

    def get_selected_widget(self) -> Optional['_widgets.core.Widget']:
        """
        Return the selected widget on the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: Widget object, ``None`` if no widget is selected
        """
        if not isinstance(self._index, int):
            self._index = 0
            return None
        if self._index < 0:
            return None
        try:
            return self._widgets[self._index % len(self._widgets)]
        except (IndexError, ZeroDivisionError):
            return None

    def set_attribute(self, key: str, value: Any) -> 'Menu':
        """
        Set an attribute value.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param key: Key of the attribute
        :param value: Value of the attribute
        :return: Self reference
        """
        assert isinstance(key, str)
        self._attributes[key] = value
        return self

    def get_attribute(self, key: str, default: Any = None) -> Any:
        """
        Get an attribute value.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param key: Key of the attribute
        :param default: Value if does not exists
        :return: Attribute data
        """
        assert isinstance(key, str)
        if not self.has_attribute(key):
            return default
        return self._attributes[key]

    def has_attribute(self, key: str) -> bool:
        """
        Return ``True`` if the Menu has the given attribute.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param key: Key of the attribute
        :return: ``True`` if exists
        """
        assert isinstance(key, str)
        return key in self._attributes.keys()

    def remove_attribute(self, key: str) -> 'Menu':
        """
        Removes the given attribute. Throws ``IndexError`` if given key does not exist.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param key: Key of the attribute
        :return: Self reference
        """
        if not self.has_attribute(key):
            raise IndexError('attribute "{0}" does not exists on menu'.format(key))
        del self._attributes[key]
        return self

    def get_decorator(self) -> 'Decorator':
        """
        Return the Menu decorator API.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: Decorator API
        """
        return self._decorator


class _MenuStats(object):
    """
    Menu stats.
    """

    def __init__(self) -> None:
        # Widget addition
        self.add_button = 0
        self.add_color_input = 0
        self.add_generic_widget = 0
        self.add_image = 0
        self.add_label = 0
        self.add_none_widget = 0
        self.add_selector = 0
        self.add_text_input = 0
        self.add_toggle_switch = 0
        self.add_vertical_margin = 0

        # Widget update
        self.added_widgets = 0
        self.removed_widgets = 0

        # Widget position
        self.build_surface = 0
        self.position_update = 0
        self.center_content = 0

        # Render
        self.last_build_surface_time = 0
        self.render_private = 0
        self.render_public = 0
        self.total_building_time = 0
        self.total_rendering_time = 0

        # Other
        self.clear = 0
        self.draw = 0
        self.draw_update_cached = 0
        self.loop = 0
        self.reset = 0
        self.select = 0
        self.update = 0


class _MenuCopyException(Exception):
    """
    If user tries to copy a Menu.
    """
    pass


class _MenuRuntimeErrorConfig(object):
    """
    Controls the runtime errors of the Menu.
    """

    def __init__(self) -> None:
        self.close = True
        self.draw = True
        self.mainloop = True
        self.update = True  # It should be True, as non active Menus SHOULD NOT receive updates

    @staticmethod
    def throw(throw_runtime: bool, msg: str) -> None:
        """
        Throws an error, if ``throw_runtime=True`` throws a ``RuntimeError``, otherwise
        only a warning.

        :param throw_runtime: If error is raised
        :param msg: Message
        :return: None
        """
        if throw_runtime:
            raise RuntimeError(msg)
        warnings.warn(msg)
