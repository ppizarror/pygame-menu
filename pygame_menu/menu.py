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

import math
import os
import sys
import time

import pygame
import pygame.gfxdraw as gfxdraw
import pygame_menu.events as _events

from pygame_menu._base import Base
from pygame_menu._decorator import Decorator
from pygame_menu._widgetmanager import WidgetManager
from pygame_menu.controls import KEY_LEFT, KEY_RIGHT, KEY_MOVE_UP, KEY_MOVE_DOWN, \
    KEY_BACK, KEY_CLOSE_MENU, JOY_LEFT, JOY_RIGHT, JOY_DEADZONE, JOY_UP, JOY_DOWN, \
    JOY_AXIS_X, JOY_DELAY, JOY_AXIS_Y, JOY_REPEAT
from pygame_menu.locals import ALIGN_CENTER, ALIGN_LEFT, ALIGN_RIGHT, \
    ORIENTATION_HORIZONTAL, ORIENTATION_VERTICAL, FINGERDOWN, FINGERUP, FINGERMOTION
from pygame_menu._scrollarea import ScrollArea, get_scrollbars_from_position
from pygame_menu.sound import Sound
from pygame_menu.themes import Theme, THEME_DEFAULT
from pygame_menu.utils import widget_terminal_title, TerminalColors, is_callable, \
    assert_vector, make_surface, check_key_pressed_valid, mouse_motion_current_mouse_position, \
    get_finger_pos, warn
from pygame_menu.widgets import Frame, Widget, MenuBar
from pygame_menu.widgets.core.widget import check_widget_mouseleave, WIDGET_MOUSEOVER

# Import types
from pygame_menu._types import Callable, Any, Dict, NumberType, VectorType, \
    Vector2NumberType, Union, Tuple, List, Vector2IntType, Vector2BoolType, \
    Tuple4Tuple2IntType, Tuple2IntType, MenuColumnMaxWidthType, MenuColumnMinWidthType, \
    MenuRowsType, Optional, Tuple2BoolType, NumberInstance, VectorInstance, EventType, \
    EventVectorType, EventListType

# Joy events
JOY_EVENT_LEFT = 1
JOY_EVENT_RIGHT = 2
JOY_EVENT_UP = 4
JOY_EVENT_DOWN = 8

# Select types
SELECT_KEY = 'key'
SELECT_MOUSE_BUTTON_DOWN = 'mouse_button_down'
SELECT_MOUSE_MOTION = 'mouse_motion'
SELECT_MOVE = 'move'
SELECT_OPEN = 'open'
SELECT_RECURSIVE = 'recursive'
SELECT_REMOVE = 'removehidden'
SELECT_RESET = 'reset'
SELECT_TOUCH = 'touch'
SELECT_WIDGET = 'widget'


class Menu(Base):
    """
    Menu object.

    Menu can receive many callbacks; callbacks ``onclose`` and ``onreset`` are fired
    (if them are callable-type). They can only receive 1 argument maximum, if so,
    the Menu instance is provided

    .. code-block:: python

        onclose() <or> onclose(Menu)
        onreset() <or> onreset(Menu)

    .. note::

        Menu cannot be copied or deepcopied.

    :param title: Title of the Menu
    :param width: Width of the Menu in px
    :param height: Height of the Menu in px
    :param center_content: Auto centers the Menu on the vertical position after a widget is added/deleted
    :param column_max_width: List/Tuple representing the maximum width of each column in px, ``None`` equals no limit. For example ``column_max_width=500`` (each column width can be 500px max), or ``column_max_width=(400,500)`` (first column 400px, second 500). If ``0`` uses the Menu width. This method does not resize the widgets, only determines the dynamic width of the column layout
    :param column_min_width: List/Tuple representing the minimum width of each column in px. For example ``column_min_width=500`` (each column width is 500px min), or ``column_max_width=(400,500)`` (first column 400px, second 500). Negative values are not accepted
    :param columns: Number of columns
    :param enabled: Menu is enabled. If ``False`` the Menu cannot be drawn or updated
    :param joystick_enabled: Enable/disable joystick events on the Menu
    :param keyboard_enabled: Enable/disable keyboard events on the Menu
    :param menu_id: ID of the Menu
    :param mouse_enabled: Enable/disable mouse click inside the Menu
    :param mouse_motion_selection: Select widgets using mouse motion. If ``True`` menu draws a ``focus`` on the selected widget
    :param mouse_visible: Set mouse visible on Menu
    :param onclose: Event or function executed when closing the Menu. If not ``None`` the menu disables and executes the event or function it points to. If a function (callable) is provided it can be both non-argument or single argument (Menu instance)
    :param onreset: Function executed when resetting the Menu. The function must be non-argument or single argument (Menu instance)
    :param overflow: Enables overflow on x/y axes. If ``False`` then scrollbars will not work and the maximum width/height of the scrollarea is the same as the Menu container. Style: (overflow_x, overflow_y). If ``False`` or ``True`` the value will be set on both axis
    :param position: Position on x-axis and y-axis (%) respect to the window size
    :param rows: Number of rows of each column, if there's only 1 column ``None`` can be used for no-limit. Also a tuple can be provided for defining different number of rows for each column, for example ``rows=10`` (each column can have a maximum 10 widgets), or ``rows=[2, 3, 5]`` (first column has 2 widgets, second 3, and third 5)
    :param screen_dimension: List/Tuple representing the dimensions the Menu should reference for sizing/positioning, if ``None`` pygame is queried for the display mode. This value defines the ``window_size`` of the Menu
    :param theme: Menu theme
    :param touchscreen: Enable/disable touch action inside the Menu. Only available on pygame 2
    :param touchscreen_motion_selection: Select widgets using touchscreen motion. If ``True`` menu draws a ``focus`` on the selected widget
    """
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
    _disable_draw: bool
    _disable_update: bool
    _enabled: bool
    _height: int
    _index: int
    _joy_event: int
    _joy_event_repeat: int
    _joystick: bool
    _keyboard: bool
    _last_scroll_thickness: List[Union[Tuple2IntType, int]]
    _last_selected_type: str
    _mainloop: bool
    _max_row_column_elements: int
    _menubar: 'MenuBar'
    _mouse: bool
    _mouse_motion_selection: bool
    _mouse_visible: bool
    _mouse_visible_default: bool
    _mouseover: bool
    _onbeforeopen: Optional[Callable[['Menu', 'Menu'], Any]]
    _onclose: Optional[Union['_events.MenuAction', Callable[[], Any], Callable[['Menu'], Any]]]
    _onmouseleave: Optional[Callable[['Menu', EventType], Any]]
    _onmouseover: Optional[Callable[['Menu', EventType], Any]]
    _onreset: Optional[Union[Callable[[], Any], Callable[['Menu'], Any]]]
    _onupdate: Optional[Callable[[EventListType, 'Menu'], Any]]
    _onwindowmouseleave: Optional[Callable[['Menu'], Any]]
    _onwindowmouseover: Optional[Callable[['Menu'], Any]]
    _overflow: Tuple2BoolType
    _position: Tuple2IntType
    _prev: Optional[List[Union['Menu', List['Menu']]]]
    _runtime_errors: '_MenuRuntimeErrorConfig'
    _scrollarea: 'ScrollArea'
    _scrollarea_margin: List[int]
    _sound: 'Sound'
    _stats: '_MenuStats'
    _submenus: List['Menu']
    _theme: 'Theme'
    _top: 'Menu'
    _touchscreen: bool
    _touchscreen_motion_selection: bool
    _translate: Tuple2IntType
    _update_frames: List['Frame']  # Stores the reference of scrollable frames to check inputs
    _update_widgets: List['Widget']  # Stores widgets which should always update
    _used_columns: int
    _validate_frame_widgetmove: bool
    _widget_columns: Dict[int, List['Widget']]
    _widget_max_position: Tuple2IntType
    _widget_min_position: Tuple2IntType
    _widget_offset: List[int]
    _widget_surface_cache_enabled: bool
    _widget_surface_cache_need_update: bool
    _widgets: List['Widget']
    _widgets_surface: Optional['pygame.Surface']
    _widgets_surface_last: Tuple[int, int, Optional['pygame.Surface']]
    _widgets_surface_need_update: bool
    _width: int
    _window_size: Tuple2IntType
    add: 'WidgetManager'

    def __init__(
            self,
            title: str,
            width: NumberType,
            height: NumberType,
            center_content: bool = True,
            column_max_width: MenuColumnMaxWidthType = None,
            column_min_width: MenuColumnMinWidthType = 0,
            columns: int = 1,
            enabled: bool = True,
            joystick_enabled: bool = True,
            keyboard_enabled: bool = True,
            menu_id: str = '',
            mouse_enabled: bool = True,
            mouse_motion_selection: bool = False,
            mouse_visible: bool = True,
            onclose: Optional[Union['_events.MenuAction', Callable[[], Any], Callable[['Menu'], Any]]] = None,
            onreset: Optional[Union[Callable[[], Any], Callable[['Menu'], Any]]] = None,
            overflow: Union[Vector2BoolType, bool] = (True, True),
            position: Vector2NumberType = (50, 50),
            rows: MenuRowsType = None,
            screen_dimension: Optional[Vector2IntType] = None,
            theme: 'Theme' = THEME_DEFAULT.copy(),
            touchscreen: bool = False,
            touchscreen_motion_selection: bool = False
    ) -> None:
        super(Menu, self).__init__(object_id=menu_id)

        # Compatibility from (height, width, title) to (title, width, height)
        if not isinstance(title, str) and isinstance(height, str):
            _title = title
            title = height
            height = _title
            warn('Menu constructor changed from Menu(height, width, title, ...) to '
                 'Menu(title, width, height, ...). This alert will be removed in v4.1')

        # Check events compatibility
        if onclose == _events.DISABLE_CLOSE:
            warn('DISABLE_CLOSE event is deprecated and it will be removed in v4.1. '
                 'Use events.NONE instead (or None)')
            onclose = None

        assert isinstance(width, NumberInstance)
        assert isinstance(height, NumberInstance)
        assert isinstance(center_content, bool)
        assert isinstance(column_max_width, (VectorInstance, type(None), NumberInstance))
        assert isinstance(column_min_width, (VectorInstance, NumberInstance))
        assert isinstance(columns, int)
        assert isinstance(enabled, bool)
        assert isinstance(joystick_enabled, bool)
        assert isinstance(keyboard_enabled, bool)
        assert isinstance(mouse_enabled, bool)
        assert isinstance(mouse_motion_selection, bool)
        assert isinstance(mouse_visible, bool)
        assert isinstance(overflow, (VectorInstance, bool))
        assert isinstance(rows, (int, type(None), VectorInstance))
        assert isinstance(theme, Theme), \
            'theme bust be a pygame_menu.themes.Theme object instance'
        assert isinstance(touchscreen, bool)
        assert isinstance(touchscreen_motion_selection, bool)

        # Assert theme
        theme.validate()

        # Assert pygame was initialized
        assert not hasattr(pygame, 'get_init') or pygame.get_init(), \
            'pygame is not initialized'

        # Assert python version is greater than 3.6
        assert sys.version_info >= (3, 6, 0), \
            'pygame-menu only supports python equal or greater than version 3.6.0'

        # Column/row asserts
        assert columns >= 1, \
            'the number of columns must be equal or greater than 1 (current={0})'.format(columns)
        if columns > 1:
            assert rows is not None, \
                'rows cannot be None if the number of columns is greater than 1'
            if isinstance(rows, int):
                assert rows >= 1, \
                    'if number of columns is greater than 1 (current={0}) then the number ' \
                    'of rows must be equal or greater than 1 (current={1})'.format(columns, rows)
                rows = [rows for _ in range(columns)]
            assert isinstance(rows, VectorInstance), \
                'if rows is not an integer it must be a tuple/list'
            assert len(rows) == columns, \
                'the length of the rows vector must be the ' \
                'same as the number of columns (current={0}, expected={1})'.format(len(rows), columns)

            for i in rows:
                assert isinstance(i, int), \
                    'each item of rows tuple/list must be an integer'
                assert i >= 1, \
                    'each item of the rows tuple/list must be equal or greater than one'

        else:
            if rows is None:
                rows = 10000000  # Set rows as a big number
            else:
                assert isinstance(rows, int), \
                    'rows cannot be a tuple/list as there\'s only 1 column'
                assert rows >= 1, \
                    'number of rows must be equal or greater than 1. If there is ' \
                    'no limit rows must be None'
            rows = [rows]

        # Set column min width
        if isinstance(column_min_width, NumberInstance):
            assert column_min_width >= 0, \
                'column_min_width must be equal or greater than zero'
            if columns != 1:
                if column_min_width > 0:  # Ignore the default value
                    warn(
                        'column_min_width can be a single number if there is only '
                        '1 column, but there is {0} columns. Thus, column_min_width '
                        'should be a vector of {0} items. By default a vector has '
                        'been created using the same value for each column'.format(columns)
                    )
                column_min_width = [column_min_width for _ in range(columns)]
            else:
                column_min_width = [column_min_width]

        assert len(column_min_width) == columns, \
            'column_min_width length must be the same as the number of columns, ' \
            'but size is different {0}!={1}'.format(len(column_min_width), columns)
        for i in column_min_width:
            assert isinstance(i, NumberInstance), \
                'each item of column_min_width must be an integer/float'
            assert i >= 0, \
                'each item of column_min_width must be equal or greater than zero'

        # Set column max width
        if column_max_width is not None:
            # if isinstance(column_max_width, (tuple, list)) and len(column_max_width) == 1:
            #     warn(
            #       'as there is only 1 column, prefer using column_max_width as a number '
            #       'NumberInstance instead a list/tuple'
            #     )

            if isinstance(column_max_width, NumberInstance):
                assert column_max_width >= 0, \
                    'column_max_width must be equal or greater than zero'
                if columns != 1:
                    column_max_width = [column_max_width for _ in range(columns)]
                else:
                    column_max_width = [column_max_width]

            assert len(column_max_width) == columns, \
                'column_max_width length must be the same as the number of columns, ' \
                'but size is different {0}!={1}'.format(len(column_max_width), columns)

            for i in column_max_width:
                assert isinstance(i, type(None)) or isinstance(i, NumberInstance), \
                    'each item of column_max_width can be None (no limit) or an integer/float'
                assert i is None or i >= 0, \
                    'each item of column_max_width must be equal or greater than zero or None'

        else:
            column_max_width = [None for _ in range(columns)]

        # Check that every column max width is equal or greater than minimum width
        for i in range(len(column_max_width)):
            if column_max_width[i] is not None:
                assert column_max_width[i] >= column_min_width[i], \
                    'item {0} of column_max_width ({1}) must be equal or greater ' \
                    'than column_min_width ({2})' \
                    ''.format(i, column_max_width[i], column_min_width[i])

        # Element size and position asserts
        assert_vector(position, 2)
        assert width > 0 and height > 0, \
            'menu width and height must be greater than zero'

        # Get window size if not given explicitly
        if screen_dimension is not None:
            assert_vector(screen_dimension, 2)
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
            'menu size ({0}x{1}) must be lower or equal than the size of the ' \
            'window ({2}x{3})'.format(width, height, window_width, window_height)

        # Assert overflow
        if isinstance(overflow, bool):  # If single value
            overflow = overflow, overflow
        assert len(overflow) == 2, \
            'overflow must be a 2-item tuple/list of booleans (x-axis, y-axis)'
        assert isinstance(overflow[0], bool), \
            'overflow on x-axis must be a boolean object'
        assert isinstance(overflow[1], bool), \
            'overflow on y-axis must be a boolean object'

        # General properties of the Menu
        self._auto_centering = center_content
        self._background_function = (False, None)  # Accept menu as argument, callable object
        self._clock = pygame.time.Clock()
        self._decorator = Decorator(self)
        self._enabled = enabled  # Menu is enabled or not. If disabled menu can't update or draw
        self._height = int(height)
        self._index = -1  # Selected index, if -1 the widget does not have been selected yet
        self._last_scroll_thickness = [(0, 0), 0]  # scroll and the number of recursive states
        self._last_selected_type = ''  # Last type selection, used for test purposes
        self._mainloop = False  # Menu is in mainloop state
        self._onclose = None  # Function or event called on Menu close
        self._sound = Sound()
        self._stats = _MenuStats()
        self._submenus = []
        self._theme = theme
        self._width = int(width)

        # Set callbacks
        self.set_onclose(onclose)
        self.set_onreset(onreset)

        self._onbeforeopen = None
        self._onmouseleave = None
        self._onmouseover = None
        self._onupdate = None
        self._onwindowmouseleave = None
        self._onwindowmouseover = None

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
        self._translate = (0, 0)
        self.set_relative_position(position[0], position[1])

        # Menu widgets, it should not be accessed outside the object as strange issues can occur
        self.add = WidgetManager(self)
        self._widget_offset = [theme.widget_offset[0], theme.widget_offset[1]]
        self._widgets = []  # This list may change during execution (replaced by a new one)

        self._update_frames = []  # Stores the frames which receive update events
        self._update_widgets = []  # Stores the widgets which receive update even if not selected or events is empty

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
            warn(
                'menu (title "{0}") is vertically centered (center_content=True), '
                'but widget offset (from theme) is different than zero ({1}px). '
                'Auto-centering has been disabled'.format(title, self._widget_offset[1])
            )
            self._auto_centering = False

        # Scroll area outer margin
        self._scrollarea_margin = [theme.scrollarea_outer_margin[0], theme.scrollarea_outer_margin[1]]
        if abs(self._scrollarea_margin[0]) < 1:
            self._scrollarea_margin[0] *= self._width
        if abs(self._scrollarea_margin[1]) < 1:
            self._scrollarea_margin[1] *= self._height

        self._scrollarea_margin[0] = int(self._scrollarea_margin[0])
        self._scrollarea_margin[1] = int(self._scrollarea_margin[1])

        # If centering is enabled, but ScrollArea margin in the vertical is different than zero a warning is raised
        if self._auto_centering and self._scrollarea_margin[1] != 0:
            warn(
                'menu (title "{0}") is vertically centered (center_content=True)'
                ', but ScrollArea outer margin (from theme) is different than '
                'zero ({1}px). Auto-centering has been disabled'
                ''.format(title, round(self._scrollarea_margin[1], 3))
            )
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

        # Init keyboard
        self._keyboard = keyboard_enabled

        # Init mouse
        if mouse_motion_selection:
            assert mouse_enabled, \
                'mouse motion selection cannot be enabled if mouse is disabled'
            assert mouse_visible, \
                'mouse motion cannot be enabled if mouse is not visible'
            assert hasattr(pygame, 'MOUSEMOTION'), \
                'pygame MOUSEMOTION does not exist, thus, mouse motion selection' \
                ' cannot be enabled'
        self._mouse = mouse_enabled and mouse_visible
        self._mouseover = False
        self._mouse_motion_selection = mouse_motion_selection
        self._mouse_visible = mouse_visible
        self._mouse_visible_default = mouse_visible

        # Init touchscreen
        if touchscreen:
            version_major, _, _ = pygame.version.vernum
            assert version_major >= 2, 'touchscreen is only supported in pygame v2+'
        if touchscreen_motion_selection:
            assert touchscreen, \
                'touchscreen motion selection cannot be enabled if touchscreen is disabled'
            assert hasattr(pygame, 'FINGERMOTION'), \
                'pygame FINGERMOTION does not exist, thus, touchscreen motion ' \
                'selection cannot be enabled'
        self._touchscreen = touchscreen
        self._touchscreen_motion_selection = touchscreen_motion_selection

        # Create menubar (title)
        self._menubar = MenuBar(
            back_box=theme.title_close_button,
            back_box_background_color=theme.title_close_button_background_color,
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
        self._menubar.set_cursor(self._theme.title_close_button_cursor)
        self._menubar.set_font_shadow(
            color=self._theme.title_font_shadow_color,
            enabled=self._theme.title_font_shadow,
            offset=self._theme.title_font_shadow_offset,
            position=self._theme.title_font_shadow_position
        )
        self._menubar.set_controls(
            joystick=self._joystick,
            mouse=self._mouse,
            touchscreen=self._touchscreen,
            keyboard=self._keyboard
        )
        self._menubar.set_position(*self.get_position())
        if self._theme.title_floating:
            self._menubar.set_float()
        if not self._theme.title:
            self._menubar.hide()
        self._menubar.configured = True
        self._menubar.fixed = self._theme.title_fixed

        # Scrolling area
        menubar_height = self._menubar.get_height()
        if self._height - menubar_height <= 0:
            raise ValueError('menubar is higher than menu height ({0} > {1})'
                             .format(menubar_height, self._height))

        extend_y = 0 if self._theme.title_fixed else menubar_height

        self._scrollarea = ScrollArea(
            area_color=self._theme.background_color,
            area_height=self._height - extend_y,
            area_width=self._width,
            extend_y=extend_y,
            menubar=self._menubar,
            scrollbar_color=self._theme.scrollbar_color,
            scrollbar_cursor=self._theme.scrollbar_cursor,
            scrollbar_slider_color=self._theme.scrollbar_slider_color,
            scrollbar_slider_hover_color=self._theme.scrollbar_slider_hover_color,
            scrollbar_slider_pad=self._theme.scrollbar_slider_pad,
            scrollbar_thick=self._theme.scrollbar_thick,
            scrollbars=get_scrollbars_from_position(self._theme.scrollarea_position),
            shadow=self._theme.scrollbar_shadow,
            shadow_color=self._theme.scrollbar_shadow_color,
            shadow_offset=self._theme.scrollbar_shadow_offset,
            shadow_position=self._theme.scrollbar_shadow_position
        )
        self._scrollarea.set_menu(self)
        self._scrollarea.set_position(*self.get_position())
        self._overflow = tuple(overflow)

        # Controls the behaviour of runtime errors
        self._runtime_errors = _MenuRuntimeErrorConfig()

        # These can be changed without any major problem
        self._disable_draw = False
        self._disable_widget_update_mousepos_mouseselection = False
        self._disable_update = False
        self._validate_frame_widgetmove = True

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

        .. note::

            This method is expensive, as menu surface update forces re-rendering
            of all widgets (because them can change in size, position, etc...).

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.menu.Menu.get_current`,
            for example, ``menu.get_current().update(...)``.

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

            This method should not be used along :py:meth:`pygame_menu.menu.Menu.get_current`,
            for example, ``menu.get_current().update(...)``.

        :return: Self reference
        """
        self._current._widget_surface_cache_need_update = True
        self._current._decorator.force_cache_update()
        return self

    def set_onbeforeopen(
            self,
            onbeforeopen: Optional[Callable[['Menu', 'Menu'], Any]]
    ) -> 'Menu':
        """
        Set ``onbeforeopen`` callback. Callback is executed before opening the
        Menu, it receives the current Menu and the next Menu:

        .. code-block:: python

            onbeforeopen(current Menu <from>, next Menu <to>)

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param onbeforeopen: Onbeforeopen callback, it can be a function or None
        :return: Self reference
        """
        assert is_callable(onbeforeopen) or onbeforeopen is None, \
            'onbeforeopen must be callable (function-type) or None'
        self._onbeforeopen = onbeforeopen
        return self

    def set_onupdate(
            self,
            onupdate: Optional[Callable[[EventListType, 'Menu'], Any]]
    ) -> 'Menu':
        """
        Set ``onupdate`` callback. Callback is executed before updating the Menu,
        it receives the event list and the menu reference:

        .. code-block:: python

            onupdate(event_list, Menu)

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param onupdate: Onupdate callback, it can be a function or None
        :return: Self reference
        """
        assert is_callable(onupdate) or onupdate is None, \
            'onupdate must be a callable (function-type) or None'
        self._onupdate = onupdate
        return self

    def set_onclose(
            self,
            onclose: Optional[Union['_events.MenuAction', Callable[[], Any], Callable[['Menu'], Any]]]
    ) -> 'Menu':
        """
        Set ``onclose`` callback. Callback can only receive 1 argument maximum
        (if not ``None``), if so, the Menu instance is provided:

        .. code-block:: python

            onclose() <or> onclose(Menu)

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param onclose: Onclose callback, it can be a function, a pygame-menu event, or None
        :return: Self reference
        """
        assert is_callable(onclose) or _events.is_event(onclose) or onclose is None, \
            'onclose must be a MenuAction (event), callable (function-type), or None'
        if onclose == _events.NONE:
            onclose = None
        self._onclose = onclose
        return self

    def set_onreset(
            self,
            onreset: Optional[Union[Callable[[], Any], Callable[['Menu'], Any]]]
    ) -> 'Menu':
        """
        Set ``onreset`` callback. Callback can only receive 1 argument maximum
        (if not ``None``), if so, the Menu instance is provided:

        .. code-block:: python

            onreset() <or> onreset(Menu)

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param onreset: Onreset callback, it can be a function or None
        :return: Self reference
        """
        assert is_callable(onreset) or onreset is None, \
            'onreset must be a callable (function-type) or None'
        self._onreset = onreset
        return self

    def set_onwindowmouseover(
            self,
            onwindowmouseover: Optional[Callable[['Menu'], Any]]
    ) -> 'Menu':
        """
        Set ``onwindowmouseover`` callback. This method is executed in
        :py:meth:`pygame_menu.menu.Menu.update` method. The callback function
        receives the following arguments:

        .. code-block:: python

            onwindowmouseover(menu)

        :param onwindowmouseover: Callback executed if user enters the window with the mouse; it can be a function or None
        :return: Self reference
        """
        if onwindowmouseover:
            assert is_callable(onwindowmouseover), \
                'onwindowmouseover must be callable (function-type) or None'
        self._onwindowmouseover = onwindowmouseover
        return self

    def set_onwindowmouseleave(
            self,
            onwindowmouseleave: Optional[Callable[['Menu'], Any]]
    ) -> 'Menu':
        """
        Set ``onmouseleave`` callback. This method is executed in
        :py:meth:`pygame_menu.menu.Menu.update` method. The callback function
        receives the following arguments:

        .. code-block:: python

            onwindowmouseleave(menu)

        :param onwindowmouseleave: Callback executed if user leaves the window with the mouse; it can be a function or None
        :return: Self reference
        """
        if onwindowmouseleave:
            assert is_callable(onwindowmouseleave), \
                'onwindowmouseleave must be callable (function-type) or None'
        self._onwindowmouseleave = onwindowmouseleave
        return self

    def set_onmouseover(
            self,
            onmouseover: Optional[Callable[['Menu', EventType], Any]]
    ) -> 'Menu':
        """
        Set ``onmouseover`` callback. This method is executed in
        :py:meth:`pygame_menu.menu.Menu.update` method. The callback function
        receives the following arguments:

        .. code-block:: python

            onmouseover(menu, event)

        :param onmouseover: Callback executed if user enters the Menu with the mouse; it can be a function or None
        :return: Self reference
        """
        if onmouseover:
            assert is_callable(onmouseover), \
                'onmouseover must be callable (function-type) or None'
        self._onmouseover = onmouseover
        return self

    def set_onmouseleave(
            self,
            onmouseleave: Optional[Callable[['Menu', EventType], Any]]
    ) -> 'Menu':
        """
        Set ``onmouseleave`` callback. This method is executed in
        :py:meth:`pygame_menu.menu.Menu.update` method. The callback function
        receives the following arguments:

        .. code-block:: python

            onmouseleave(menu, event)

        :param onmouseleave: Callback executed if user leaves the Menu with the mouse; it can be a function or None
        :return: Self reference
        """
        if onmouseleave:
            assert is_callable(onmouseleave), \
                'onmouseleave must be callable (function-type) or None'
        self._onmouseleave = onmouseleave
        return self

    def get_current(self) -> 'Menu':
        """
        Get the **current** active Menu. If the user has not opened any submenu the
        pointer object must be the same as the base. If not, this will return the
        opened Menu pointer.

        :return: Menu object **(current)**
        """
        return self._current

    def translate(self, x: NumberType, y: NumberType) -> 'Menu':
        """
        Translate to (+x, +y) according to the default position.

        .. note::

            To revert changes, only set to ``(0, 0)``.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param x: +X in px
        :param y: +Y in px
        :return: None
        """
        assert isinstance(x, NumberInstance)
        assert isinstance(y, NumberInstance)
        self._translate = (int(x), int(y))
        self._widgets_surface = None
        self._render()
        return self

    def get_translate(self) -> Tuple2IntType:
        """
        Get Menu translate on x-axis and y-axis (x, y) in px.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :return: Translation on both axis
        """
        return self._translate

    def get_position(self) -> Tuple2IntType:
        """
        Return the menu position (constructor + translation).

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :return: Position on x-axis and y-axis (x,y) in px
        """
        return self._position[0] + self._translate[0], self._position[1] + self._translate[1]

    @staticmethod
    def _warn_widgetmanager(method: str, new_method: str) -> None:
        """
        Warn about a deprecated method.

        :param method: Method's name to warn about
        :param new_method: New method name
        :return: None
        """
        warn(
            'Menu method {0} is deprecated. Use menu.add.{1} instead, (see docs). '
            'This method will be removed in v4.1'.format(method, new_method)
        )

    def add_button(self, *args, **kwargs) -> 'pygame_menu.widgets.Button':
        """
        Use :py:meth:`pygame_menu._widgetmanager.WidgetManager.button` instead.
        This method shorthand will be removed in version 4.1.
        """
        self._warn_widgetmanager('add_button', 'button')
        return self.add.button(*args, **kwargs)

    def add_color_input(self, *args, **kwargs) -> 'pygame_menu.widgets.ColorInput':
        """
        Use :py:meth:`pygame_menu._widgetmanager.WidgetManager.color_input` instead.
        This method shorthand will be removed in version 4.1.
        """
        self._warn_widgetmanager('add_color_input', 'color_input')
        return self.add.color_input(*args, **kwargs)

    def add_image(self, *args, **kwargs) -> 'pygame_menu.widgets.Image':
        """
        Use :py:meth:`pygame_menu._widgetmanager.WidgetManager.image` instead.
        This method shorthand will be removed in version 4.1.
        """
        self._warn_widgetmanager('add_image', 'image')
        return self.add.image(*args, **kwargs)

    def add_label(self, *args, **kwargs) -> Union['pygame_menu.widgets.Label', List['pygame_menu.widgets.Label']]:
        """
        Use :py:meth:`pygame_menu._widgetmanager.WidgetManager.label` instead.
        This method shorthand will be removed in version 4.1.
        """
        self._warn_widgetmanager('add_label', 'label')
        return self.add.label(*args, **kwargs)

    def add_selector(self, *args, **kwargs) -> 'pygame_menu.widgets.Selector':
        """
        Use :py:meth:`pygame_menu._widgetmanager.WidgetManager.selector` instead.
        This method shorthand will be removed in version 4.1.
        """
        self._warn_widgetmanager('add_selector', 'selector')
        return self.add.selector(*args, **kwargs)

    def add_text_input(self, *args, **kwargs) -> 'pygame_menu.widgets.TextInput':
        """
        Use :py:meth:`pygame_menu._widgetmanager.WidgetManager.text_input` instead.
        This method shorthand will be removed in version 4.1.
        """
        self._warn_widgetmanager('add_text_input', 'text_input')
        return self.add.text_input(*args, **kwargs)

    def add_vertical_margin(self, *args, **kwargs) -> 'pygame_menu.widgets.VMargin':
        """
        Use :py:meth:`pygame_menu._widgetmanager.WidgetManager.vertical_margin` instead.
        This method shorthand will be removed in version 4.1.
        """
        self._warn_widgetmanager('add_vertical_margin', 'vertical_margin')
        return self.add.vertical_margin(*args, **kwargs)

    def add_generic_widget(self, *args, **kwargs) -> 'Widget':
        """
        Use :py:meth:`pygame_menu._widgetmanager.WidgetManager.generic_widget` instead.
        This method shorthand will be removed in version 4.1.
        """
        self._warn_widgetmanager('add_generic_widget', 'generic_widget')
        return self.add.generic_widget(*args, **kwargs)

    def select_widget(self, widget: Optional[Union['Widget', str]]) -> 'Menu':
        """
        Select a widget from the Menu. If ``None`` unselect the current one.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param widget: Widget to be selected or Widget ID. If ``None`` unselect the current
        :return: Self reference
        """
        if widget is None:
            for w in self._widgets:
                w.select(False)
            self._index = -1
            return self
        if isinstance(widget, str):
            widget = self.get_widget(widget)
        assert isinstance(widget, Widget)
        if not widget.is_selectable:
            raise ValueError('{0} is not selectable'.format(widget.get_class_id()))
        if not widget.is_visible():  # Considers frame
            raise ValueError('{0} is not visible'.format(widget.get_class_id()))
        try:
            index = self._widgets.index(widget)  # If not exists this raises ValueError
        except ValueError:
            raise ValueError('{0} is not in Menu, check if exists on the current '
                             'with menu.get_current().remove_widget(widget)'.format(widget.get_class_id()))
        self._select(index, 1, SELECT_WIDGET, False)
        return self

    def remove_widget(self, widget: Union['Widget', str]) -> 'Menu':
        """
        Remove the ``widget`` from the Menu. If widget not exists on Menu this
        method raises a ``ValueError`` exception.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param widget: Widget object or Widget ID
        :return: Self reference
        """
        if isinstance(widget, str):
            widget = self.get_widget(widget)
        assert isinstance(widget, Widget)

        try:
            index = self._widgets.index(widget)  # If not exists this raises ValueError
        except ValueError:
            raise ValueError('widget is not in Menu, check if exists on the current '
                             'with menu.get_current().remove_widget(widget)')
        self._widgets.pop(index)
        self._update_after_remove_or_hidden(index)  # This forces surface update
        self._stats.removed_widgets += 1

        # If widget is within a frame, remove from frame
        frame = widget.get_frame()
        if frame is not None:
            frame.unpack(widget)

        widget.on_remove_from_menu()
        widget.set_menu(None)  # Removes Menu reference from widget

        # Remove widget from update lists
        if isinstance(widget, Frame) and widget in self._update_frames:
            self._update_frames.remove(widget)
        if widget in self._update_widgets:
            self._update_widgets.remove(widget)

        check_widget_mouseleave()
        return self

    def get_sound(self) -> 'Sound':
        """
        Return the Menu sound engine.

        :return: Sound API
        """
        return self._sound

    def _update_after_remove_or_hidden(
            self,
            index: int,
            update_surface: bool = True
    ) -> None:
        """
        Update widgets after removal or hidden.

        :param index: Removed index, if ``-1`` then select next index, if equal to ``self._index`` select the same
        :param update_surface: Updates Menu surface
        :return: None
        """
        # Check if there's more selectable widgets
        n_select = 0
        last_selectable = 0
        for indx in range(len(self._widgets)):
            wid = self._widgets[indx]
            if wid.is_selectable and wid.is_visible():  # Considers frame
                n_select += 1
                last_selectable = indx

        # Any widget is selected
        if n_select == 0:
            self._index = -1

        # Select the unique selectable option
        elif n_select == 1:
            self._select(last_selectable, 0, SELECT_REMOVE, False)

        # There is at least 1 option to select from
        elif n_select > 1:
            if index == -1:  # Index was hidden
                self._select(self._index + 1, 1, SELECT_REMOVE, False)
            elif self._index > index:  # If the selected widget was after this
                self._select(self._index - 1, -1, SELECT_REMOVE, False)
            else:
                self._select(self._index, 1, SELECT_REMOVE, False)
        self._update_widget_position()
        if update_surface:
            self._widgets_surface = None  # If added on execution time forces the update of the surface

    def _back(self) -> None:
        """
        Go to previous Menu or close if the top Menu is currently displayed.

        :return: None
        """
        if self._top._prev is not None:
            self.reset(1)
        else:
            self._close()

    def _update_selection_if_hidden(self) -> None:
        """
        Updates the Menu widget selection if a widget was hidden.

        :return: None
        """
        if len(self._widgets) > 0:
            if self._index != -1:
                selected_widget = self._widgets[self._index % len(self._widgets)]
                if not selected_widget.is_visible():  # Considers frame
                    selected_widget.select(False)  # Unselect
                    self._update_after_remove_or_hidden(-1, update_surface=False)
            else:
                self._update_after_remove_or_hidden(0, update_surface=False)

    def _update_widget_position(self) -> None:
        """
        Update the position of each widget. Also checks widget consistency.

        :return: None
        """
        # Column widgets
        self._widget_columns = {}
        for i in range(self._columns):
            self._widget_columns[i] = []

        # Set the column widths (minimum values)
        self._column_widths = []  # Safe for certain widgets that request the width on rendering
        column_widths = [self._column_min_width[i] for i in range(self._columns)]

        # Set column/row of each widget and compute maximum width of each column if None
        self._used_columns = 0
        max_elements_msg = \
            'total visible/non-floating widgets ([widg]) cannot exceed columns*rows' \
            '({0} elements). Menu position update failed. If using frames, please' \
            'pack before adding new widgets' \
            ''.format(self._max_row_column_elements)
        i_index = 0
        has_frame = False

        # Checks for widget selection consistency
        has_selected_widget = False
        invalid_selection_widgets: List[str] = []
        selected_widget = None

        for index in range(len(self._widgets)):
            widget = self._widgets[index]

            # Check widget selection
            if widget.is_selected():
                if not has_selected_widget:
                    has_selected_widget = True
                    selected_widget = widget.get_class_id()
                    self._index = index
                else:
                    widget.select(False)
                    invalid_selection_widgets.append(widget.get_class_id())

            # If widget is frame
            if isinstance(widget, Frame):
                try:
                    widget.update_position()
                except:
                    warn('{0} failed to update'.format(widget.get_class_id()))
                    raise
                has_frame = True

            # If not visible, or within frame, continue to the next widget
            if not widget.is_visible() or widget.get_frame() is not None:
                widget.set_col_row_index(-1, -1, index)
                continue

            # Check if the maximum number of elements was reached, if so raise an exception
            # If menu has frames, this check is disabled
            if not has_frame and not i_index < self._max_row_column_elements:
                raise _MenuWidgetOverflow(max_elements_msg.replace('[widg]', str(i_index)))

            # Set the widget column/row position
            row = i_index
            col = 0
            max_rows = 0
            for col in range(self._columns):  # Find which column it belongs to
                max_rows += self._rows[col]
                if i_index < max_rows:
                    break
                row -= self._rows[col]  # Subtract the number of rows of such column

            # Important before getting widget width as some widgets require the
            # column max width
            widget.set_col_row_index(col, row, index)
            self._widget_columns[col].append(widget)

            # Update used columns
            self._used_columns = max(self._used_columns, col + 1)

            # Get the next widget, if don't exist use the same
            next_widget = widget
            if index < len(self._widgets) - 1:
                next_widget = self._widgets[index + 1]

            # If widget is floating don't update the next
            if not (next_widget.is_floating() and next_widget.get_frame() is None):
                i_index += 1

            # If floating, don't contribute to the column width
            else:
                continue

            column_widths[col] = max(
                column_widths[col],
                widget.get_width(apply_selection=True)  # This forces rendering
            )

        if len(invalid_selection_widgets) > 0:
            self._index = -1
            raise _MenuMultipleSelectedWidgetsException(
                'several widgets are selected at the same time, current selected '
                '(sorted by index): {0}, but the following are also selected: {1}. '
                'If widget is selected outside the menu, use widget.select(update_menu=True)'
                ''.format(selected_widget, ','.join(invalid_selection_widgets))
            )

        # Apply max width column limit
        for col in range(self._used_columns):
            if self._column_max_width[col] is not None:
                column_widths[col] = min(column_widths[col], self._column_max_width[col])

        # If some columns were not used, set these widths to zero
        for col in range(self._used_columns, self._columns):
            column_widths.pop()
            del self._widget_columns[col]

        # If the total weight is less than the window width (so there's no horizontal
        # scroll), scale the columns. Only None column_max_widths and columns less
        # than the maximum are scaled
        sum_width_columns = sum(column_widths)
        max_width = self.get_width(inner=True)
        if 0 <= sum_width_columns < max_width and len(self._widgets) > 0:

            # First, scale columns to its maximum
            sum_contrib = []
            for col in range(self._used_columns):
                if self._column_max_width[col] is None:
                    sum_contrib.append(0)
                elif column_widths[col] < self._column_max_width[col]:
                    sum_contrib.append(self._column_max_width[col] - column_widths[col])
                else:
                    sum_contrib.append(0)

            delta = max_width - sum(sum_contrib) - sum_width_columns
            if delta < 0:  # Scale contrib back
                scale = (max_width - sum_width_columns) / sum(sum_contrib)
                sum_contrib = [sum_contrib[i] * scale for i in range(len(sum_contrib))]

            # Increase to its maximums
            for col in range(self._used_columns):
                if sum_contrib[col] > 0:
                    column_widths[col] += sum_contrib[col]

            # Scale column widths if None
            sum_width_columns = sum(column_widths)
            sum_contrib = []
            for col in range(self._used_columns):
                if self._column_max_width[col] is None:
                    sum_contrib.append(column_widths[col])
                else:
                    sum_contrib.append(0)

            delta = max_width - sum_width_columns
            if delta > 0:
                for col in range(self._used_columns):
                    if sum_contrib[col] > 0:
                        column_widths[col] += delta * sum_contrib[col] / sum(sum_contrib)

            # Re-compute sum
            sum_width_columns = sum(column_widths)

            # If column width still 0, set all the column the same width (only used)
            # This only can happen if column_min_width was not set
            if sum_width_columns < max_width and self._used_columns >= 1:

                # The width it would be added for each column
                mod_width = max_width  # Available left width for non max columns
                non_max = self._used_columns

                # First fill all maximum width columns
                for col in range(self._used_columns):
                    if self._column_max_width[col] is not None:
                        column_widths[col] = min(self._column_max_width[col],
                                                 max_width / self._used_columns)
                        mod_width -= column_widths[col]
                        non_max -= 1

                # Now, update the rest (non maximum set)
                if non_max > 0:
                    for col in range(self._used_columns):
                        if self._column_max_width[col] is None:
                            column_widths[col] = mod_width / non_max

        # Cast to int
        for col in range(self._used_columns):
            column_widths[col] = int(math.ceil(column_widths[col]))

        # Final column width
        total_col_width = sum(column_widths)
        if self._used_columns > 1:
            # Calculate column width scale (weights)
            column_weights = tuple(
                float(column_widths[i]) / max(total_col_width, 1) for i in range(self._used_columns))

            # Calculate the position of each column
            self._column_pos_x = []
            cumulative = 0
            for i in range(self._used_columns):
                w = column_weights[i]
                self._column_pos_x.append(int(total_col_width * (cumulative + 0.5 * w)))
                cumulative += w
        else:
            self._column_pos_x = [total_col_width * 0.5]
            column_widths = [total_col_width]

        # Now updates the column width's
        self._column_widths = column_widths

        # Update title position
        self._menubar.set_position(*self.get_position())

        # Widget max/min position
        min_max_updated = False
        max_x, max_y = -1e8, -1e8
        min_x, min_y = 1e8, 1e8

        # Cache rects
        rects_cache: Dict[str, 'pygame.Rect'] = {}

        def get_rect(wid: 'Widget') -> 'pygame.Rect':
            """
            Get rect cache from widget.

            :param wid: Widget
            :return: Rect cache
            """
            try:
                return rects_cache[wid.get_id()]
            except KeyError:
                rects_cache[wid.get_id()] = wid.get_rect(render=True)
            return rects_cache[wid.get_id()]

        # Get menubar height, if fixed then move all widgets within area
        menubar_height = self._menubar.get_height() if self._menubar.fixed else 0

        # Update appended widgets
        for index in range(len(self._widgets)):
            widget = self._widgets[index]

            align = widget.get_alignment()
            margin = widget.get_margin()
            padding = widget.get_padding()
            selection_effect = widget.get_selection_effect()
            width = get_rect(widget).width

            if not widget.is_visible():
                widget.set_position(0, 0)
                continue

            # If widget within frame update col/row position
            if widget.get_frame() is not None:
                widget.set_position_relative_to_frame(index)
                continue

            # Get column and row position
            col, row, _ = widget.get_col_row_index()

            # Calculate X position
            column_width = self._column_widths[col]
            selection_margin = 0
            if align == ALIGN_CENTER:
                dx = -width / 2
            elif align == ALIGN_LEFT:
                selection_margin = selection_effect.get_margin()[1]  # left
                dx = -column_width / 2 + selection_margin
            elif align == ALIGN_RIGHT:
                selection_margin = selection_effect.get_margin()[3]  # right
                dx = column_width / 2 - width - selection_margin
            else:
                dx = 0
            dx_border = int(math.ceil(widget.get_border()[1] / 2))
            x_coord = self._column_pos_x[col] + dx + margin[0] + padding[3]
            x_coord = max(selection_margin, x_coord)
            x_coord += max(0, self._widget_offset[0]) + dx_border

            # Check if widget width exceeds column max width
            max_column_width = self._column_max_width[col]
            if max_column_width is not None and width > max_column_width:
                raise _MenuSizingException(
                    '{0} widget width ({1}) exceeds column {2} max width ({3})'
                    ''.format(widget.get_class_id(), width, col + 1, max_column_width)
                )

            # Calculate Y position
            y_sum = 1  # Compute the total height from the current row position to the top of the column
            for r_widget in self._widget_columns[col]:
                _, r, _ = r_widget.get_col_row_index()
                if r >= row:
                    break
                if r_widget.is_visible() and \
                        not r_widget.is_floating() and \
                        not r_widget.get_frame() is not None:
                    y_sum += get_rect(r_widget).height  # Height
                    y_sum += r_widget.get_margin()[1]  # Vertical margin (bottom)

                    # If no widget is before add the selection effect
                    y_sel_h = r_widget.get_selection_effect().get_margin()[0]
                    if r == 0 and self._widget_offset[1] <= y_sel_h:
                        if r_widget.is_selectable:
                            y_sum += y_sel_h - self._widget_offset[1]

            # If the widget offset is zero, then add the selection effect to the height
            # of the widget to avoid visual glitches
            y_sel_h = widget.get_selection_effect().get_margin()[0]
            if y_sum == 1 and self._widget_offset[1] <= y_sel_h:  # No widget is before
                if widget.is_selectable:  # Add top margin
                    y_sum += y_sel_h - self._widget_offset[1]

            y_coord = max(0, self._widget_offset[1]) + y_sum + padding[0] + menubar_height

            # Update the position of the widget
            widget.set_position(x_coord, y_coord)

            # Add the widget translation to the widget for computing the min/max position. This
            # feature does not work as intended as there's edge cases not covered, and centering makes
            # the translation more difficult
            # tx, ty = widget.get_translate()
            tx, ty = 0, 0

            # Update max/min position, minus padding
            min_max_updated = True
            max_x = max(max_x, x_coord + width - padding[1] + tx)  # minus right padding
            max_y = max(max_y, y_coord + get_rect(widget).height - padding[2] + ty)  # minus bottom padding
            min_x = min(min_x, x_coord - padding[3])
            min_y = min(min_y, y_coord - padding[0])

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
        Create the surface used to draw widgets according the required width and
        height.

        :return: None
        """
        self._stats.build_surface += 1
        t0 = time.time()

        # Update internals
        self._update_selection_if_hidden()
        self._update_widget_position()

        menubar_height = self._menubar.get_height() if not self._menubar.fixed else 0
        max_x, max_y = self._widget_max_position

        # Get scrollbars size
        sx, sy = self._get_scrollbar_thickness()

        # Remove the thick of the scrollbar to avoid displaying a horizontal one
        # If overflow on both axis
        if max_x > self._width - sy and max_y > self._height - sx - menubar_height:
            width, height = max_x, max_y
            if not self._mouse_visible:
                self._mouse_visible = True

        # If horizontal overflow
        elif max_x > self._width - sy:
            width, height = max_x, self._height - menubar_height - sx
            self._mouse_visible = self._mouse_visible_default

        # If vertical overflow
        elif max_y > self._height - sx - menubar_height:
            width, height = self._width - sy, max_y
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

        # Adds ScrollArea margin
        width += self._scrollarea_margin[0]
        height += self._scrollarea_margin[1]

        # Cast to int
        width = int(width)
        height = int(height)

        # Get the previous surface if the width/height is the same
        if width == self._widgets_surface_last[0] and \
                height == self._widgets_surface_last[1]:
            self._widgets_surface = self._widgets_surface_last[2]
        else:
            self._widgets_surface = make_surface(width, height)
            self._widgets_surface_last = (width, height, self._widgets_surface)

        # Set position
        self._scrollarea.set_world(self._widgets_surface)
        self._scrollarea.set_position(*self.get_position())

        # Check if the scrollbars changed
        sx, sy = self._get_scrollbar_thickness()
        if (sx, sy) != self._last_scroll_thickness[0] and \
                self._last_scroll_thickness[1] == 0:
            self._last_scroll_thickness[0] = (sx, sy)
            self._last_scroll_thickness[1] += 1
            self._widgets_surface_need_update = True
            self._render()
        else:
            self._last_scroll_thickness[1] = 0

        # Update times
        dt = time.time() - t0
        self._stats.total_building_time += dt
        self._stats.last_build_surface_time = dt

    def _check_id_duplicated(self, widget_id: str) -> None:
        """
        Check if widget ID is duplicated. Throws ``IndexError`` if the index is
        duplicated.

        :param widget_id: New widget ID
        :return: None
        """
        assert isinstance(widget_id, str)
        for widget in self._widgets:
            if widget.get_id() == widget_id:
                raise IndexError(
                    'widget id "{0}" already exists on the current menu ({1})'
                    ''.format(widget_id, widget.get_class_id())
                )

    def _close(self) -> bool:
        """
        Execute close callbacks and disable the Menu, only if ``onclose`` is not
        None (or :py:mod:`pygame_menu.events.NONE`).

        :return: ``True`` if the Menu has executed the ``onclose`` callback
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
            elif is_callable(onclose):
                try:
                    onclose(self)
                except TypeError:
                    onclose()

        return True

    def close(self) -> bool:
        """
        Closes the **current** Menu firing ``onclose`` callback. If ``callback=None``
        this method does nothing.

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.menu.Menu.get_current`,
            for example, ``menu.get_current().reset(...)``.

        :return: ``True`` if the Menu has executed the ``onclose`` callback
        """
        if not self.is_enabled():
            self._current._runtime_errors.throw(
                self._current._runtime_errors.close, 'menu already closed'
            )
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
        if prev is not None:
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
        check_widget_mouseleave(force=True)
        self._top._enabled = False
        return self

    def set_relative_position(self, position_x: NumberType, position_y: NumberType) -> 'Menu':
        """
        Set the Menu position relative to the window.

        .. note::

            - Menu left position (x) must be between ``0`` and ``100``, if ``0``
              the margin is at the left of the window, if ``100`` the Menu is at
              the right of the window.

            - Menu top position (y) must be between ``0`` and ``100``, if ``0``
              the margin is at the top of the window, if ``100`` the margin is at
              the bottom of the window.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param position_x: Left position of the window
        :param position_y: Top position of the window
        :return: Self reference
        """
        assert isinstance(position_x, NumberInstance)
        assert isinstance(position_y, NumberInstance)
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
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

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

    def _get_scrollbar_thickness(self) -> Tuple2IntType:
        """
        Return the scrollbar thickness from x-axis and y-axis (horizontal and vertical).

        :return: Scrollbar thickness in px
        """
        return self._scrollarea.get_scrollbar_thickness(ORIENTATION_HORIZONTAL), \
               self._scrollarea.get_scrollbar_thickness(ORIENTATION_VERTICAL)

    def get_width(self, inner: bool = False, widget: bool = False) -> int:
        """
        Get the Menu width.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param inner: If ``True`` returns the available width (menu width minus scroll if visible)
        :param widget: If ``True`` returns the total width used by the widgets
        :return: Width in px
        """
        if widget:
            return int(self._widget_max_position[0] - self._widget_min_position[0])
        if not inner:
            return int(self._width)
        return int(self._width - self._get_scrollbar_thickness()[1])

    def get_height(self, inner: bool = False, widget: bool = False) -> int:
        """
        Get the Menu height.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param inner: If ``True`` returns the available height (menu height minus scroll and menubar)
        :param widget: If ``True`` returns the total height used by the widgets
        :return: Height in px
        """
        if widget:
            return int(self._widget_max_position[1] - self._widget_min_position[1])
        if not inner:
            return int(self._height)
        return int(self._height - self._menubar.get_height() - self._get_scrollbar_thickness()[0])

    def get_size(self, inner: bool = False, widget: bool = False) -> Vector2IntType:
        """
        Return the Menu size as a tuple of (width, height) in px.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param inner: If ``True`` returns the available (width, height) (menu height minus scroll and menubar)
        :param widget: If ``True`` returns the total (width, height) used by the widgets
        :return: Tuple of (width, height) in px
        """
        return self.get_width(inner=inner, widget=widget), self.get_height(inner=inner, widget=widget)

    def render(self) -> 'Menu':
        """
        Force the **current** Menu to render. Useful to force widget update.

        .. note::

            This method should not be called if the Menu is being drawn as this
            method is called by :py:meth:`pygame_menu.menu.Menu.draw`

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.menu.Menu.get_current`,
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

        :return: ``True`` if the surface has changed (if it was ``None``)
        """
        t0 = time.time()
        changed = False

        if self._widgets_surface_need_update:
            self._widgets_surface = None

        if self._widgets_surface is None:
            self._widgets_surface_need_update = False
            if self._auto_centering:
                self.center_content()
            self._build_widget_surface()
            self._stats.render_private += 1
            changed = True

        self._stats.total_rendering_time += time.time() - t0
        return changed

    def draw(self, surface: 'pygame.Surface', clear_surface: bool = False) -> 'Menu':
        """
        Draw the **current** Menu into the given surface.

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.menu.Menu.get_current`,
            for example, ``menu.get_current().draw(...)``

        :param surface: Pygame surface to draw the Menu
        :param clear_surface: Clear surface using theme default color
        :return: Self reference **(current)**
        """
        assert isinstance(surface, pygame.Surface)
        assert isinstance(clear_surface, bool)

        if not self.is_enabled():
            self._current._runtime_errors.throw(self._current._runtime_errors.draw, 'menu is not enabled')
            return self._current
        if self._current._disable_draw:
            return self._current

        # Render menu; if True, the surface widget has changed, thus cache should
        # change if enabled
        render = self._current._render()

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
            # surface. ScrollArea post decorator is drawn on _scroll.draw(surface) call
            scrollarea_decorator = self._current._scrollarea.get_decorator()
            scrollarea_decorator.force_cache_update()
            scrollarea_decorator.draw_prev(self._current._widgets_surface)

            # Iterate through widgets and draw them
            selected_widget = None
            for widget in self._current._widgets:
                # Widgets within frames are not drawn as it's frame draw these widgets
                if widget.get_frame() is not None:
                    continue
                if widget.is_selected():
                    selected_widget = widget
                widget.draw(self._current._widgets_surface)
            if selected_widget is not None:
                selected_widget.draw_after_if_selected(self._current._widgets_surface)

            self._current._stats.draw_update_cached += 1

        self._current._scrollarea.draw(surface)
        self._current._menubar.draw(surface)

        # Draw focus on selected if the widget is active
        self._current._draw_focus_widget(surface, self._current.get_selected_widget())
        self._current._decorator.draw_post(surface)
        self._current._stats.draw += 1

        # Update cursor if not mainloop
        if self._current._mainloop:
            check_widget_mouseleave()

        return self._current

    def _draw_focus_widget(
            self,
            surface: 'pygame.Surface',
            widget: Optional['Widget'],
            force: bool = False
    ) -> Optional[Dict[int, Tuple4Tuple2IntType]]:
        """
        Draw the focus background from a given widget. Widget must be selectable,
        active, selected. Not all widgets requests the active status, then focus
        may not be drawn.

        :param surface: Pygame surface to draw the Menu
        :param widget: Focused widget
        :param force: If ``True`` forces focus without any checks
        :return: Returns the focus region, ``None`` if the focus could not be possible
        """
        assert isinstance(surface, pygame.Surface)
        assert isinstance(widget, (Widget, type(None)))

        force = force or (widget is not None and widget.active and widget.force_menu_draw_focus)
        if not force and (widget is None
                          or not widget.active
                          or not widget.is_selectable
                          or not widget.is_selected()
                          or not (self._mouse_motion_selection or self._touchscreen_motion_selection)
                          or not widget.is_visible()):
            return
        window_width, window_height = self._window_size

        self._render()  # Surface may be none, then update the positioning
        rect = widget.get_focus_rect()

        # Apply selection effect
        rect = widget.get_selection_effect().inflate(rect)
        if rect.width == 0 or rect.height == 0:
            return

        x1, y1, x2, y2 = rect.topleft + rect.bottomright
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
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :return: Self reference
        """
        self._top._enabled = True
        return self

    def toggle(self) -> 'Menu':
        """
        Switch between enable/disable Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

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
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :return: Menu enabled status
        """
        return self._top._enabled

    def _sort_update_frames(self) -> None:
        """
        Sort the update frames (frames which receive updates).

        :return: None
        """
        if len(self._update_frames) <= 1:
            return

        # Sort frames by depth
        widgets: List[Tuple[int, 'Frame']] = []
        for w in self._update_frames:
            assert isinstance(w, Frame)
            widgets.append((-w.get_frame_depth(), w))
        widgets.sort(key=lambda x: x[0])

        # Sort frames with same depth by index
        frame_depths: Dict[int, List[Tuple[int, 'Frame']]] = {}
        for w in widgets:
            w_depth = w[0]
            if w_depth not in frame_depths.keys():
                frame_depths[w_depth] = []
            if w[1] in self._widgets:
                frame_depths[w_depth].append((self._widgets.index(w[1]), w[1]))
            else:
                frame_depths[w_depth].append((0, w[1]))

        self._update_frames = []
        for d in frame_depths.keys():
            frame_depths[d].sort(key=lambda x: x[0])
            for w in frame_depths[d]:
                self._update_frames.append(w[1])

    def _move_selected_left_right(self, pos: int, apply_sound: bool = False) -> bool:
        """
        Move the selected widget index to left/right position (column support).

        :param pos: If ``+1`` selects right column, ``-1`` left column
        :param apply_sound: Apply sound on widget selection
        :return: ``True`` if the widget changed
        """
        if not (pos == 1 or pos == -1):
            raise ValueError('pos must be +1 or -1')

        def _default() -> bool:
            if pos == -1:
                return self._select(0, 1, SELECT_KEY, apply_sound)
            return self._select(-1, -1, SELECT_KEY, apply_sound)

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

            # Get the first similar row in that column, if no widget is found
            # then select the first widget
            for widget in self._widget_columns[col]:
                c, r, i = widget.get_col_row_index()
                if r == row:
                    return self._select(i, pos, SELECT_KEY, apply_sound)

            # If no widget is in that column
            if len(self._widget_columns[col]) == 0:
                return _default()

            # If the number of rows in that column is less than current,
            # select the first one
            first_widget = self._widget_columns[col][0]
            _, _, i = first_widget.get_col_row_index()
            return self._select(i, pos, SELECT_KEY, apply_sound)

        else:
            return _default()

    def _handle_joy_event(self, apply_sound: bool = False) -> bool:
        """
        Handle joy events.

        :param apply_sound: Apply sound on widget selection
        :return: ``True`` if widget changed
        """
        if self._joy_event & JOY_EVENT_UP:
            return self._select(self._index - 1, -1, SELECT_KEY, apply_sound)
        if self._joy_event & JOY_EVENT_DOWN:
            return self._select(self._index + 1, 1, SELECT_KEY, apply_sound)
        if self._joy_event & JOY_EVENT_LEFT:
            return self._move_selected_left_right(-1, apply_sound)
        if self._joy_event & JOY_EVENT_RIGHT:
            return self._move_selected_left_right(1, apply_sound)

    def _up(self, apply_sound: bool = False) -> bool:
        """
        Process up key event.

        :param apply_sound: Apply selection sound
        :return: ``True`` if widget selected
        """
        if not apply_sound:
            self._sound.play_key_add()
        return self._select(self._index + 1, 1, SELECT_KEY, apply_sound)

    def _down(self, apply_sound: bool = False) -> bool:
        """
        Process down key event.

        :param apply_sound: Apply selection sound
        :return: ``True`` if widget selected
        """
        if not apply_sound:
            self._sound.play_key_add()
        return self._select(self._index - 1, -1, SELECT_KEY, apply_sound)

    def _left(self, apply_sound: bool = False) -> bool:
        """
        Process left key event.

        :param apply_sound: Apply selection sound
        :return: ``True`` if widget selected
        """
        if not apply_sound:
            self._sound.play_key_add()

        # Get frame properties
        selected_widget = self.get_selected_widget()
        selected_widget_in_frame_horizontal = selected_widget is not None and \
                                              selected_widget.get_frame() is not None and \
                                              selected_widget.get_frame().horizontal
        selected_widget_first_in_frame = selected_widget_in_frame_horizontal and \
                                         selected_widget.get_frame().first_index == self._index

        # If current selected in within a horizontal frame
        if selected_widget_in_frame_horizontal and not selected_widget_first_in_frame:
            return self._current._select(self._current._index - 1, -1, SELECT_KEY, False)
        elif self._current._used_columns > 1:
            return self._current._move_selected_left_right(-1)
        return False

    def _right(self, apply_sound: bool = False) -> bool:
        """
        Process left key event.

        :param apply_sound: Apply selection sound
        :return: ``True`` if widget selected
        """
        if not apply_sound:
            self._sound.play_key_add()

        # Get frame properties
        selected_widget = self.get_selected_widget()
        selected_widget_in_frame_horizontal = selected_widget is not None and \
                                              selected_widget.get_frame() is not None and \
                                              selected_widget.get_frame().horizontal
        selected_widget_last_in_frame = selected_widget_in_frame_horizontal and \
                                        selected_widget.get_frame().last_index == self._current._index

        # If current selected in within a horizontal frame
        if selected_widget_in_frame_horizontal and not selected_widget_last_in_frame:
            return self._current._select(self._current._index + 1, 1, SELECT_KEY, False)
        elif self._current._used_columns > 1:
            return self._current._move_selected_left_right(1)
        return False

    def update(self, events: EventVectorType) -> bool:
        """
        Update the status of the Menu using external events. The update event is
        applied only on the **current** Menu.

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.menu.Menu.get_current`,
            for example, ``menu.get_current().update(...)``.

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
        if self._current._disable_update:
            return False

        # If any widget status changes, set the status as True
        updated = False

        # Update mouse
        pygame.mouse.set_visible(self._current._mouse_visible)
        mouse_motion_event = None

        selected_widget = self._current.get_selected_widget()
        selected_widget_active_disable_scroll = (False if selected_widget is None else selected_widget.active) and \
                                                self._current._mouse_motion_selection or \
                                                selected_widget is not None and selected_widget.active and \
                                                selected_widget.force_menu_draw_focus
        selected_widget_scrollarea = None if selected_widget is None else selected_widget.get_scrollarea()

        # First, check scrollable widgets (if any)
        scrollable_frames_update = False
        if not selected_widget_active_disable_scroll:
            for scrollable_frame in self._current._update_frames:
                scrollable_frames_update = scrollable_frames_update or scrollable_frame.update(events)

        # Update widgets on update list
        for widget in self._current._update_widgets:
            widget.update(events)

        # Scrollable frames have changed
        if scrollable_frames_update:
            updated = True

        # Update scroll bars
        elif not selected_widget_active_disable_scroll and self._current._scrollarea.update(events):
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
            if self._current._mouse and self._current._mouse_motion_selection:
                events.append(mouse_motion_current_mouse_position())

            for event in events:

                # User closes window
                if event.type == _events.PYGAME_QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and (
                        event.mod == pygame.KMOD_LALT or event.mod == pygame.KMOD_RALT)) or \
                        event.type == _events.PYGAME_WINDOWCLOSE:
                    self._current._exit()
                    return True

                # User press key
                elif event.type == pygame.KEYDOWN and self._current._keyboard:

                    # Check key event is valid
                    if not check_key_pressed_valid(event):
                        continue

                    if event.key == KEY_MOVE_DOWN:
                        if self._current._down():
                            updated = True
                            break

                    elif event.key == KEY_MOVE_UP:
                        if self._current._up():
                            updated = True
                            break

                    elif event.key == KEY_LEFT:
                        if self._current._left():
                            updated = True
                            break

                    elif event.key == KEY_RIGHT:
                        if self._current._right():
                            updated = True
                            break

                    elif event.key == KEY_BACK and self._top._prev is not None:
                        self._current._sound.play_close_menu()
                        self.reset(1)  # public, do not use _current

                    elif event.key == KEY_CLOSE_MENU:
                        self._current._sound.play_close_menu()
                        if self._current._close():
                            updated = True

                # User moves hat joystick
                elif event.type == pygame.JOYHATMOTION and self._current._joystick:
                    if event.value == JOY_UP:
                        if self._current._down(apply_sound=True):
                            updated = True
                            break

                    elif event.value == JOY_DOWN:
                        if self._current._up(apply_sound=True):
                            updated = True
                            break

                    elif event.value == JOY_LEFT:
                        if self._current._left(apply_sound=True):
                            updated = True
                            break

                    elif event.value == JOY_RIGHT:
                        if self._current._right(apply_sound=True):
                            updated = True
                            break

                # User moves joy axis motion
                elif event.type == pygame.JOYAXISMOTION and self._current._joystick:
                    prev = self._current._joy_event
                    self._current._joy_event = 0

                    if event.axis == JOY_AXIS_Y and event.value < -JOY_DEADZONE:
                        self._current._joy_event |= JOY_EVENT_UP

                    elif event.axis == JOY_AXIS_Y and event.value > JOY_DEADZONE:
                        self._current._joy_event |= JOY_EVENT_DOWN

                    elif event.axis == JOY_AXIS_X and event.value < -JOY_DEADZONE and \
                            self._current._used_columns > 1:
                        self._current._joy_event |= JOY_EVENT_LEFT

                    elif event.axis == JOY_AXIS_X and event.value > JOY_DEADZONE and \
                            self._current._used_columns > 1:
                        self._current._joy_event |= JOY_EVENT_RIGHT

                    if self._current._joy_event:
                        sel = self._current._handle_joy_event(True)
                        if self._current._joy_event == prev:
                            pygame.time.set_timer(self._current._joy_event_repeat, JOY_REPEAT)
                        else:
                            pygame.time.set_timer(self._current._joy_event_repeat, JOY_DELAY)
                        if sel:
                            updated = True
                            break
                    else:
                        pygame.time.set_timer(self._current._joy_event_repeat, 0)

                # User repeats previous joy event input
                elif event.type == self._current._joy_event_repeat:
                    if self._current._joy_event:
                        sel = self._current._handle_joy_event(True)
                        pygame.time.set_timer(self._current._joy_event_repeat, JOY_REPEAT)
                        if sel:
                            updated = True
                            break
                    else:
                        pygame.time.set_timer(self._current._joy_event_repeat, 0)

                # Select widget by clicking
                elif event.type == pygame.MOUSEBUTTONDOWN and self._current._mouse and \
                        event.button in (1, 2, 3):  # Don't consider the mouse wheel (button 4 & 5)

                    # If the mouse motion selection is disabled then select a widget by clicking
                    if not self._current._mouse_motion_selection:
                        sel = False
                        for index in range(len(self._current._widgets)):
                            widget = self._current._widgets[index]
                            if isinstance(widget, Frame):  # Frame does not accept click
                                continue
                            if widget.is_selectable and widget.is_visible() and \
                                    widget.get_scrollarea().collide(widget, event):
                                sel = self._current._select(index, 1, SELECT_MOUSE_BUTTON_DOWN, True)
                                break

                        if sel:
                            updated = True
                            break

                    # If mouse motion selection, clicking will disable the active state
                    # only if the user clicked outside the widget
                    else:
                        if selected_widget is not None:
                            if not selected_widget_scrollarea.collide(selected_widget.get_focus_rect(), event):
                                selected_widget.active = False
                                selected_widget.render()  # Some widgets need to be rendered
                                updated = True
                                break

                # Mouse enters or leaves the window
                elif event.type == pygame.ACTIVEEVENT:
                    if event.gain == 1:  # Enter
                        if self._current._onwindowmouseover is not None:
                            self._current._onwindowmouseover(self._current)
                            check_widget_mouseleave()
                    else:  # Leave
                        if self._current._onwindowmouseleave is not None:
                            self._current._onwindowmouseleave(self._current)
                        if self._current._mouseover:
                            self._current._mouseover = False
                            if self._current._onmouseleave is not None:
                                self._current._onmouseleave(self._current, event)
                            check_widget_mouseleave(force=True)

                # Mouse motion. It changes the cursor of the mouse if enabled
                elif event.type == pygame.MOUSEMOTION and self._current._mouse:
                    mouse_motion_event = event

                    # Check if mouse over menu
                    if not self._current._mouseover:
                        if self._current.collide(event):
                            self._current._mouseover = True
                            if self._current._onmouseover is not None:
                                self._current._onmouseover(self._current, event)
                    else:
                        if not self._current.collide(event):
                            self._current._mouseover = False
                            if self._current._onmouseleave is not None:
                                self._current._onmouseleave(self._current, event)
                            mouse_motion_event = None
                            check_widget_mouseleave(force=True)

                    # If selected widget is active then motion should not select
                    # or change mouseover widget
                    if self._current._mouse_motion_selection and \
                            selected_widget is not None and selected_widget.active:
                        continue

                    # Check if "rel" exists within the event
                    if not hasattr(event, 'rel'):
                        continue

                    sel = False  # Widget has been selected
                    for index in range(len(self._current._widgets)):
                        widget = self._current._widgets[index]
                        if widget.is_visible() and widget.get_scrollarea().collide(widget, event):
                            if self._current._mouse_motion_selection and \
                                    widget.is_selectable and \
                                    not isinstance(widget, Frame):
                                sel = self._current._select(index, 1, SELECT_MOUSE_MOTION, True)
                        # noinspection PyProtectedMember
                        widget._check_mouseover(event)
                        if sel:
                            break
                    if sel:
                        updated = True
                        break

                # Mouse events in selected widget; don't consider the mouse wheel (button 4 & 5)
                elif event.type == pygame.MOUSEBUTTONUP and self._current._mouse and \
                        selected_widget is not None and event.button in (1, 2, 3):
                    self._current._sound.play_click_mouse()
                    if selected_widget_scrollarea.collide(selected_widget, event):
                        updated = selected_widget.update([event])
                        if updated:
                            break

                # Touchscreen event:
                elif event.type == FINGERDOWN and self._current._touchscreen:

                    # If the touchscreen motion selection is disabled then select
                    # a widget by clicking
                    if not self._current._touchscreen_motion_selection:
                        sel = False
                        for index in range(len(self._current._widgets)):
                            widget = self._current._widgets[index]
                            if isinstance(widget, Frame):  # Frame does not accept touch
                                continue
                            if widget.is_selectable and widget.is_visible() and \
                                    widget.get_scrollarea().collide(widget, event):
                                sel = self._current._select(index, 1, SELECT_TOUCH, True)
                                if not isinstance(widget, Frame):
                                    break
                        if sel:
                            updated = True
                            break

                    # If touchscreen motion selection, clicking will disable the
                    # active state only if the user clicked outside the widget
                    else:
                        if selected_widget is not None:
                            if not selected_widget_scrollarea.collide(selected_widget, event):
                                selected_widget.active = False
                                selected_widget.render()  # Some widgets need to be rendered
                                updated = True
                                break

                # Select widgets by touchscreen motion, this is valid only if the
                # current selected widget is not active and the pointed widget is
                # selectable
                elif event.type == FINGERMOTION and self._current._touchscreen_motion_selection:

                    # If selected widget is active then motion should not select
                    # any widget
                    if selected_widget is not None and selected_widget.active:
                        continue

                    sel = False
                    for index in range(len(self._current._widgets)):
                        widget = self._current._widgets[index]
                        if isinstance(widget, Frame):  # Frame does not accept touch
                            continue
                        if widget.is_selectable and widget.is_visible() and \
                                widget.get_scrollarea().collide(widget, event):
                            sel = self._current._select(index, 1, SELECT_TOUCH, True)
                            if not isinstance(widget, Frame):
                                break
                    if sel:
                        updated = True
                        break

                # Touchscreen events in selected widget
                elif event.type == FINGERUP and self._current._touchscreen and selected_widget is not None:
                    self._current._sound.play_click_mouse()
                    if selected_widget_scrollarea.collide(selected_widget, event):
                        updated = selected_widget.update([event])
                        if updated:
                            break

        if mouse_motion_event is not None:
            check_widget_mouseleave(event=mouse_motion_event)

        # If cache is enabled, always force a rendering (user may have have
        # changed any status)
        if self._current._widget_surface_cache_enabled and updated:
            self._current._widget_surface_cache_need_update = True

        # A widget has closed the Menu
        if not self.is_enabled():
            updated = True

        return updated

    def collide(self, event: EventType) -> bool:
        """
        Check if user event collides the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param event: Pygame event
        :return: ``True`` if collide
        """
        return bool(self.get_rect().collidepoint(*get_finger_pos(self, event)))

    def mainloop(
            self,
            surface: 'pygame.Surface',
            bgfun: Optional[Union[Callable[['Menu'], Any], Callable[[], Any]]] = None,
            **kwargs
    ) -> 'Menu':
        """
        Main loop of the **current** Menu. In this function, the Menu handle
        exceptions and draw. The Menu pauses the application and checks :py:mod:`pygame`
        events itself.

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
            - ``clear_surface``     (bool) – If ``True`` surface is cleared using ``theme.surface_clear_color``
            - ``disable_loop``      (bool) – If ``True`` the mainloop only runs once. Use for running draw and update in a single call
            - ``fps_limit``         (int) – Maximum FPS of the loop. Default equals to ``theme.fps``. If ``0`` there's no limit

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.menu.Menu.get_current`,
            for example, ``menu.get_current().mainloop(...)``.

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
        assert isinstance(fps_limit, NumberInstance)
        assert isinstance(surface, pygame.Surface)

        assert fps_limit >= 0, 'fps limit cannot be negative'

        # NOTE: For Menu accessor, use only _current, as the Menu pointer can
        # change through the execution
        if not self.is_enabled():
            self._current._runtime_errors.throw(
                self._current._runtime_errors.mainloop, 'menu is not enabled'
            )
            return self._current

        # Check background function
        bgfun_accept_menu = False
        if bgfun:
            assert is_callable(bgfun), \
                'background function must be callable (function-type) object'
            try:
                bgfun(self._current)
                bgfun_accept_menu = True
            except TypeError:
                pass
        self._current._background_function = (bgfun_accept_menu, bgfun)

        # Change state
        self._current._mainloop = True

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
                self._current._mainloop = False
                check_widget_mouseleave(force=True)
                return self._current

    def get_input_data(self, recursive: bool = False) -> Dict[str, Any]:
        """
        Return input data from a Menu. The results are given as a dict object.
        The keys are the ID of each element.

        With ``recursive=True`` it collect also data inside the all sub-menus.

        .. note::

            This is applied only to the base Menu (not the currently displayed),
            for such behaviour apply to :py:meth:`pygame_menu.menu.Menu.get_current` object.

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
                sub_data_keys = data_submenu.keys()
                for key in sub_data_keys:
                    if key in data_keys:
                        raise ValueError('collision between widget data ID="{0}" at depth={1}'.format(key, depth))

                # Update data
                data.update(data_submenu)
        return data

    def get_rect(self) -> 'pygame.Rect':
        """
        Return the :py:class:`pygame.Rect` object of the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :return: Rect
        """
        x, y = self.get_position()
        return pygame.Rect(x, y, int(self._width), int(self._height))

    def set_sound(self, sound: Optional['Sound'], recursive: bool = False) -> 'Menu':
        """
        Add a sound engine to the Menu. If ``recursive=True``, the sound is
        applied to all submenus.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

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
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :return: Menu title
        """
        return self._menubar.get_title()

    def set_title(self, title: Any, offset: Optional[Vector2NumberType] = None) -> 'Menu':
        """
        Set the title of the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param title: New menu title
        :param offset: If ``None`` uses theme offset, else it defines the title offset on x-axis and y-axis (x, y)
        :return: Self reference
        """
        if offset is None:
            offset = self._theme.title_offset
        else:
            assert_vector(offset, 2)
        self._menubar.set_title(title, offsetx=offset[0], offsety=offset[1])
        return self

    def full_reset(self) -> 'Menu':
        """
        Reset the Menu back to the first opened Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

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
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

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

            This method should not be used along :py:meth:`pygame_menu.menu.Menu.get_current`,
            for example, ``menu.get_current().reset(...)``.

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
        self._current._select(0, 1, SELECT_OPEN, False, update_mouse_position=False)

        # Re-render menu
        check_widget_mouseleave(force=True)
        self._render()

    def reset(self, total: int) -> 'Menu':
        """
        Go back in Menu history a certain number of times from the **current** Menu.
        This method operates through the **current** Menu pointer.

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.menu.Menu.get_current`,
            for example, ``menu.get_current().reset(...)``.

        :param total: How many menus to go back
        :return: Self reference **(current)**
        """
        assert isinstance(total, int)
        assert total > 0, 'total must be greater than zero'

        i = 0
        if self._top._prev is not None:
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

        self._current._widgets_surface = None
        check_widget_mouseleave(force=True)
        self._current._select(self._top._current._index, 1, SELECT_RESET, False,
                              update_mouse_position=False)
        self._current._stats.reset += 1
        return self._current

    def _select(
            self,
            new_index: int,
            dwidget: int,
            select_type: str,
            apply_sound: bool,
            **kwargs
    ) -> bool:
        """
        Select the widget at the given index and unselect others. Selection forces
        rendering of the widget. Also play widget selection sound. This is applied
        to the base Menu pointer.

        kwargs (Optional)
            - ``last_index``                (int) – Last index in recursive call on Frames
            - ``update_mouse_position``     (bool) – Update mouse position

        :param new_index: Widget index
        :param dwidget: Direction to search if ``new_index`` widget is non selectable
        :param select_type: Select type identifier
        :param apply_sound: Apply widget sound if selected
        :param kwargs: Optional keyword arguments
        :return: ``True`` if the widget changed
        """
        self._stats.select += 1
        self._last_selected_type = select_type

        if len(self._widgets) == 0:
            return False

        # This stores +/-1 if the index increases or decreases
        # Used by non-selectable selection
        if dwidget == 0:
            if new_index < self._index:
                dwidget = -1
            else:
                dwidget = 1

        # Limit the index to the length
        new_index %= len(self._widgets)

        # Get both widgets
        if self._index >= len(self._widgets):  # Menu length changed during execution time
            for i in range(len(self._widgets)):  # Unselect all possible candidates
                self._widgets[i].select(False)
            self._index = 0

        old_widget = self._widgets[self._index]
        new_widget = self._widgets[new_index]
        if old_widget == new_widget and self._index != -1 and old_widget.is_selected():
            return False

        # If new widget is not selectable or visible
        if not new_widget.is_selectable or not new_widget.is_visible():

            # If frame, select the first selectable object
            if isinstance(new_widget, Frame):
                if dwidget == 1:
                    min_index = new_widget.first_index
                else:
                    min_index = new_widget.last_index
                current_frame = self._widgets[self._index].get_frame()
                same_frame = current_frame is not None and current_frame == new_widget  # Ignore cycles

                # Check if recursive but same index as before
                last_index = kwargs.get('last_index', -1)
                if select_type == SELECT_RECURSIVE and last_index == min_index:
                    min_index += 2 * dwidget

                # A selectable widget has been found within frame
                if min_index != -1 and not same_frame and min_index != self._index:
                    kwargs['last_index'] = new_index
                    return self._select(min_index, dwidget, SELECT_RECURSIVE,
                                        apply_sound, **kwargs)

            # There's at least 1 selectable option
            if self._index >= 0:
                kwargs['last_index'] = new_index
                return self._select(new_index + dwidget, dwidget, SELECT_RECURSIVE,
                                    apply_sound, **kwargs)

            # No selectable options, quit
            else:
                return False

        # Selecting widgets forces rendering
        old_widget.select(False)
        self._index = new_index  # Update selected index
        new_widget.select()
        self.scroll_to_widget(new_widget)

        # Play widget selection sound
        if old_widget != new_widget and apply_sound:
            self._sound.play_widget_selection()

        # Update mouse position if selected using keys
        if select_type in (SELECT_KEY, SELECT_RECURSIVE) and \
                self._mouse_motion_selection and \
                not self._disable_widget_update_mousepos_mouseselection and \
                not new_widget.is_floating() and \
                self._mouseover and \
                kwargs.get('update_mouse_position', True):
            pygame.mouse.set_pos(new_widget.get_rect(to_real_position=True).center)

        return True

    def scroll_to_widget(
            self,
            widget: Optional['Widget'],
            scroll_parent: bool = True
    ) -> 'Menu':
        """
        Scroll the Menu to the given widget.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param widget: Widget to request scroll. If ``None`` scrolls to the selected widget
        :param scroll_parent: If ``True`` parent scroll also scrolls to rect
        :return: Self reference
        """
        if widget is None:
            widget = self.get_selected_widget()
            if widget is None:  # No widget is selected, scroll to top
                self.get_scrollarea().scroll_to(ORIENTATION_VERTICAL, 0)
                self.get_scrollarea().scroll_to(ORIENTATION_HORIZONTAL, 0)
                return self
        assert isinstance(widget, Widget), \
            'widget to scroll from must be a Widget class, not None'

        widget_scroll = widget.get_scrollarea()
        if widget_scroll is None:
            warn(
                '{0} scrollarea is None, thus, scroll to widget cannot be performed'
                ''.format(widget.get_class_id())
            )
            return self

        # Scroll to rect
        rect = widget.get_rect()
        widget_frame = widget.get_frame()
        widget_border = widget.get_border()[1]

        # Compute margin depending of widget position
        _, ry = widget_scroll.get_widget_position_relative_to_view_rect(widget)
        mx = 0
        my = 0

        if ry < 0.15 and self._menubar.fixed:
            my = -self._menubar.get_height() - widget_border

        # Call scroll parent container
        if widget_frame is not None and widget_frame.is_scrollable:
            widget_frame.scroll_to_widget((mx, my), scroll_parent)

        # The first set the scrolls
        widget_scroll.scroll_to_rect(rect, (mx, my), scroll_parent)

        # The later updates to active object
        widget_scroll.scroll_to_rect(rect, (mx, my), scroll_parent)

        return self

    def get_window_size(self) -> Tuple2IntType:
        """
        Return the window size as a tuple of (width, height).

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :return: Window size in px
        """
        return self._window_size

    def get_widgets(self) -> Tuple['Widget', ...]:
        """
        Return the Menu widgets as a tuple.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :return: Widgets tuple
        """
        return tuple(self._widgets)

    def get_menubar(self) -> 'MenuBar':
        """
        Return menubar widget.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :return: MenuBar widget
        """
        return self._menubar

    def get_scrollarea(self) -> 'ScrollArea':
        """
        Return the Menu ScrollArea.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :return: ScrollArea object
        """
        return self._scrollarea

    def get_widget(self, widget_id: str, recursive: bool = False) -> Optional['Widget']:
        """
        Return a widget by a given ID from the Menu.

        With ``recursive=True`` it looks for a widget in the Menu and all sub-menus.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

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
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

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
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

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

    def get_theme(self) -> 'Theme':
        """
        Return the Menu theme.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        .. warning::

            Use with caution, changing the theme may affect other menus or
            widgets if not properly copied.

        :return: Menu theme
        """
        return self._theme

    def get_clock(self) -> 'pygame.time.Clock':
        """
        Return the pygame Menu timer.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :return: Pygame clock object
        """
        return self._clock

    def get_index(self) -> int:
        """
        Get selected widget index from the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :return: Selected widget index
        """
        return self._index

    def get_mouseover_widget(self, filter_appended: bool = True) -> Optional['Widget']:
        """
        Return the mouseover widget on the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param filter_appended: If ``True`` return the widget only if it's appended to the base Menu
        :return: Widget object, ``None`` if no widget is mouseover
        """
        widget = WIDGET_MOUSEOVER[0]
        if widget is None or filter_appended and widget.get_menu() != self:
            return
        return widget

    def get_selected_widget(self) -> Optional['Widget']:
        """
        Return the selected widget on the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

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

    def get_decorator(self) -> 'Decorator':
        """
        Return the Menu decorator API.

        .. note::

            ``prev`` menu decorator may not draw because :py:class:`pygame_menu.widgets.MenuBar`
            and :py:class:`pygame_menu._scrollarea.ScrollArea` objects draw over
            it. If it's desired to draw a decorator behind widgets, use the ScrollArea
            decorator, for example: :py:data:`menu.get_scrollarea().get_decorator()`.

            The menu drawing order is:

            1. Menu background color/image
            2. Menu ``prev`` decorator
            3. Menu ScrollArea ``prev`` decorator
            4. Menu ScrollArea widgets
            5. Menu ScrollArea ``post`` decorator
            6. Menu title
            7. Menu ``post`` decorator

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :return: Decorator API
        """
        return self._decorator

    def _test_widgets_status(self) -> Tuple[Tuple[Any, ...], ...]:
        """
        Get the status of each widget as a tuple (position, indices, values, etc).

        :return: Widget status
        """
        self.render()
        data = []
        for w in self._widgets:
            # noinspection PyProtectedMember
            data.append(w._get_status())
        return tuple(data)

    def move_widget_index(
            self,
            widget: Optional['Widget'],
            index: Optional[Union['Widget', int]] = None,
            render: bool = True,
            **kwargs
    ) -> Optional[Tuple2IntType]:
        """
        Move a given widget to a certain index. ``index`` can be another widget,
        a numerical position, or ``None``; if ``None`` the widget is pushed to
        the last widget list position.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param widget: Widget to move. If ``None`` the widgets are flipped or reversed and returns ``None``
        :param index: Target index. It can be a widget, a numerical index, or ``None``; if ``None`` the widget is pushed to the last position
        :param render: Force menu rendering after update
        :param kwargs: Optional keyword arguments
        :return: The new indices of the widget and the previous index element
        """
        depth = kwargs.get('depth', 0)

        # Update only selected index
        if kwargs.get('update_selected_index', False):
            self._index = -1
            has_selected = False
            invalid_w: List[str] = []
            selected = None
            for w in self._widgets:
                if w.is_selected():
                    if not has_selected:
                        self._select(self._widgets.index(w), 1, SELECT_MOVE, False)
                        has_selected = True
                        selected = w.get_class_id()
                    else:
                        w.select(False)
                        invalid_w.append(w.get_class_id())
            if len(invalid_w) > 0:
                raise _MenuMultipleSelectedWidgetsException(
                    'several widgets are selected at the same time, current selected '
                    '(sorted by index): {0}, but the following are also selected: {1}'
                    ''.format(selected, ','.join(invalid_w))
                )
            return

        selected_widget = self.get_selected_widget()

        # Reverse widgets
        if widget is None:
            new_widgets = []
            lw = len(self._widgets)
            j_limit = -1  # Last position containing non frame
            for i in range(lw):
                j = lw - 1 - i
                if self._widgets[j].get_frame() is None:
                    new_widgets.append(self._widgets[j])
                    if j_limit != -1:
                        for k in range(j + 1, j_limit + 1):
                            new_widgets.append(self._widgets[k])
                    j_limit = -1
                else:
                    if j_limit == -1:
                        j_limit = j
            if j_limit != -1:
                for k in range(j_limit):
                    new_widgets.append(self._widgets[k])

            self._widgets = new_widgets
            if selected_widget is not None:
                selected_widget.select(False)
                self._select(self._widgets.index(selected_widget), 1, SELECT_MOVE, False)

            if len(self._update_frames) > 0:
                self._update_frames[0].sort_menu_update_frames()

            if render:
                self._widgets_surface = None
                self._render()

            check_widget_mouseleave()
            return

        # Asserts
        assert len(self._widgets) >= 2, \
            'menu must contain at least 2 widgets to perform this task'
        try:
            widget_index = self._widgets.index(widget)
        except ValueError:
            raise ValueError('{0} widget is not on widgets list'
                             ''.format(widget.get_class_id()))
        assert widget in self._widgets, \
            '{0} does not exist on current menu widgets list' \
            ''.format(widget.get_class_id())
        assert isinstance(index, (Widget, int, type(None)))
        if isinstance(index, Widget):
            assert index in self._widgets, \
                '{0} does not exist on current menu widgets list' \
                ''.format(index.get_class_id())
            index = self._widgets.index(index)
        elif isinstance(index, int):
            assert 0 <= index < len(self._widgets), \
                'index {0} must be between 0 and the number of widgets ({1})' \
                ''.format(index, len(self._widgets))
        elif index is None:
            index = len(self._widgets) - 1
        else:
            raise ValueError('index must be a widget, int, or None')
        assert widget_index != index, \
            'target index must be different than the current widget index ({0})' \
            ''.format(index)

        target_index = index
        target_widget = self._widgets[target_index]

        # If target widget is frame, find the latest index
        both_frames = isinstance(target_widget, Frame) and isinstance(widget, Frame)
        check_if_last = both_frames and self._validate_frame_widgetmove and target_index != 0
        if check_if_last:
            w_last = target_widget
            while True:
                target_index = w_last.last_index
                w_last = self._widgets[w_last.last_index]
                target_widget = w_last
                if not (isinstance(w_last, Frame) and w_last.get_indices() != (-1, -1)) or \
                        w_last.get_menu() is None:
                    break
        to_last_position = target_index == len(self._widgets) - 1

        if not to_last_position and check_if_last:
            target_index = index
            target_widget = self._widgets[target_index]
            if both_frames and self._validate_frame_widgetmove and \
                    not kwargs.get('swap_search', False):
                return self.move_widget_index(
                    target_widget, widget, render=render, swap_search=True, depth=depth + 1
                )

        # Check both widgets are within frame if widget to move is frame
        if self._validate_frame_widgetmove and not to_last_position and not both_frames:
            assert widget.get_frame() == target_widget.get_frame(), \
                'both widgets must be within same frame'

        self._widgets.pop(widget_index)
        self._widgets.insert(target_index, widget)

        new_widget_index = self._widgets.index(widget)
        assert new_widget_index != widget_index, 'widget index has not changed'
        assert widget != target_widget, 'widget must be different than target'

        # If frame is moved, move all sub-elements
        if self._validate_frame_widgetmove:
            if isinstance(widget, Frame):
                self._validate_frame_widgetmove = False
                for w in widget.get_widgets(unpack_subframes_include_frame=True,
                                            reverse=not to_last_position):
                    if w.get_menu() is None:
                        continue
                    if not to_last_position:
                        self.move_widget_index(
                            w, self._widgets.index(widget) + 1, render=False, depth=depth + 1
                        )
                    else:
                        self.move_widget_index(w, render=False, depth=depth + 1)
                self._validate_frame_widgetmove = True

            # Sort frame widget list
            if widget.get_frame() is not None:
                prev_frame_widgs = widget.get_frame().get_widgets(unpack_subframes=False)

                # Get none-menu widgets for ordering
                none_menu_widgs: Dict[Optional['Widget'], List['Widget']] = {}
                prev_wig: Optional['Widget'] = None
                for i in range(len(prev_frame_widgs)):
                    if prev_frame_widgs[i].get_menu() is None:
                        if prev_wig not in none_menu_widgs.keys():
                            none_menu_widgs[prev_wig] = []
                        none_menu_widgs[prev_wig].append(prev_frame_widgs[i])
                    else:
                        prev_wig = prev_frame_widgs[i]
                for i in none_menu_widgs.keys():
                    none_menu_widgs[i].reverse()

                # Get all widgets within given frame
                new_list = []
                for w in self._widgets:
                    if w.get_frame() == widget.get_frame():
                        new_list.append(w)

                # Create new list considering non-menu widgets
                new_list_non_menu = []
                if None in none_menu_widgs.keys():
                    for w in none_menu_widgs[None]:
                        new_list_non_menu.append(w)
                for w in new_list:
                    new_list_non_menu.append(w)
                    if w in none_menu_widgs.keys():
                        for ww in none_menu_widgs[w]:
                            new_list_non_menu.append(ww)

                # Make dict and update frame widgets dict
                new_dict = {}
                for w in new_list_non_menu:
                    new_dict[w.get_id()] = w
                widget.get_frame()._widgets = new_dict

        # Update selected widget
        if selected_widget is not None and selected_widget.is_selectable and \
                self._validate_frame_widgetmove:
            self._index = -1
            selected_widget.select(False)
            self._select(self._widgets.index(selected_widget), 1, SELECT_MOVE, False)

        if render:
            self._widgets_surface = None
            self._render()

        if self._validate_frame_widgetmove:
            if isinstance(widget, Frame) or isinstance(target_widget, Frame):
                if isinstance(widget, Frame):
                    widget.sort_menu_update_frames()
                else:
                    target_widget.sort_menu_update_frames()
            check_widget_mouseleave()

        return new_widget_index, target_index

    def _test_print_widgets(self) -> None:
        """
        Test printing widgets order.

        .. note::

            - Φ       Floating status
            - ⇇      Selected
            - !▲      Widget is not appended to current menu
            - ╳      Widget is hidden
            - ∑       Scrollable frame sizing
            - β       Widget is not selectable
            - {x,y}   Widget *column, row* position
            - <x,y>   Frame indices (min, max)

        :return: None
        """
        indx = 0
        current_depth = 0
        depth_widths = {}
        c = TerminalColors

        def close_frames(depth: int) -> None:
            """
            Close frames up to current depth.

            :param depth: Depth to close
            :return: None
            """
            d = current_depth - depth
            for i in range(d):
                j = depth + d - (i + 1)  # Current depth
                line = '·   {0}└{1}'.format('│   ' * j, '┄' * 3)  # * depth_widths[j]
                print(c.BRIGHT_WHITE + line.ljust(0, '━') + c.ENDC)  # 80 also work

        non_menu_frame_widgets: Dict[int, List['Widget']] = {}

        def process_non_menu_frame(w_indx: int) -> None:
            """
            Print non-menu frames list.

            :param w_indx: Current iteration index to print widgets
            :return: None
            """
            for nmi in list(non_menu_frame_widgets.keys()):
                if nmi == w_indx:
                    v = non_menu_frame_widgets[nmi]
                    for v_wid in v:
                        print(c.BRIGHT_WHITE + '·   ' + '│   ' * v_wid.get_frame_depth()
                              + c.ENDC + widget_terminal_title(v_wid))
                    del non_menu_frame_widgets[nmi]

        for w in self._widgets:
            w_depth = w.get_frame_depth()
            close_frames(w.get_frame_depth())
            title = widget_terminal_title(w, indx, self._index)
            print('{0}{1}{2}'.format(
                str(indx).ljust(3),
                ' ' + c.BRIGHT_WHITE + '│   ' * w_depth + c.ENDC,
                title
            ))
            if w_depth not in depth_widths.keys():
                depth_widths[w_depth] = 0
            # depth_widths[w_depth] = max(int(len(title) * 1.2) + 3, depth_widths[w_depth])
            depth_widths[w_depth] = len(title) - 2
            current_depth = w.get_frame_depth()
            process_non_menu_frame(indx)
            jw = self._widgets[0]
            try:
                if isinstance(w, Frame):  # Print ordered non-menu widgets
                    current_depth += 1
                    prev_indx = indx
                    for jw in w.get_widgets(unpack_subframes=False):
                        if jw.get_menu() is None or jw not in self._widgets:
                            if prev_indx not in non_menu_frame_widgets.keys():
                                non_menu_frame_widgets[prev_indx] = []
                            non_menu_frame_widgets[prev_indx].append(jw)
                        else:
                            prev_indx = self._widgets.index(jw)
            except ValueError as e:
                print('[ERROR] while requesting widget {0}'.format(jw.get_class_id()))
                warn(str(e))
            indx += 1
        process_non_menu_frame(indx)
        close_frames(0)


class _MenuStats(object):
    """
    Menu stats.
    """

    def __init__(self) -> None:
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
        warn(msg)


class _MenuSizingException(Exception):
    """
    Exception thrown if widget exceeds maximum size of column/row layout.
    """
    pass


class _MenuWidgetOverflow(Exception):
    """
    Exception thrown if adding more widgets than menu can contain on row/column layout.
    """
    pass


class _MenuMultipleSelectedWidgetsException(Exception):
    """
    Exception thrown if multiple widgets are selected at the same time.
    """
    pass
