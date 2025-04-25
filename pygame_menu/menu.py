"""
pygame-menu
https://github.com/ppizarror/pygame-menu

MENU
Menu class.
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
from pygame_menu.controls import Controller
from pygame_menu.locals import ALIGN_CENTER, ALIGN_LEFT, ALIGN_RIGHT, \
    ORIENTATION_HORIZONTAL, ORIENTATION_VERTICAL, FINGERDOWN, FINGERUP, FINGERMOTION
from pygame_menu._scrollarea import ScrollArea, get_scrollbars_from_position
from pygame_menu.sound import Sound
from pygame_menu.themes import Theme, THEME_DEFAULT
from pygame_menu.utils import assert_vector, make_surface, warn, \
    check_key_pressed_valid, mouse_motion_current_mouse_position, get_finger_pos, \
    print_menu_widget_structure
from pygame_menu.widgets import Frame, Widget, MenuBar
from pygame_menu.widgets.core.widget import check_widget_mouseleave, WIDGET_MOUSEOVER

# Import types
from pygame_menu._types import Callable, Any, Dict, NumberType, VectorType, \
    Vector2NumberType, Union, Tuple, List, Vector2IntType, Vector2BoolType, \
    Tuple4Tuple2IntType, Tuple2IntType, MenuColumnMaxWidthType, MenuColumnMinWidthType, \
    MenuRowsType, Optional, Tuple2BoolType, NumberInstance, VectorInstance, EventType, \
    EventVectorType, EventListType, CallableNoArgsType

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
SELECT_REMOVE = 'remove'
SELECT_RESET = 'reset'
SELECT_TOUCH = 'touch'
SELECT_WIDGET = 'widget'


class Menu(Base):
    """
    Menu object.

    Menu can receive many callbacks; callbacks ``onclose`` and ``onreset`` are fired
    (if them are callable-type). They can only receive 1 argument maximum, if so,
    the Menu instance is provided.

    .. code-block:: python

        onclose(menu) <or> onclose()
        onreset(menu) <or> onreset()

    .. note::

        Menu cannot be copied or deep-copied.

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
    :param keyboard_ignore_nonphysical: Ignores non-physical keyboard buttons pressed
    :param menu_id: ID of the Menu
    :param mouse_enabled: Enable/disable mouse click inside the Menu
    :param mouse_motion_selection: Select widgets using mouse motion. If ``True`` menu draws a ``focus`` on the selected widget
    :param mouse_visible: Set mouse cursor visible on Menu. Auto-enables if the Menu has scrollbars. Also requires ``mouse_visible_update`` to be True for the Menu to update cursor visibility
    :param mouse_visible_update: Menu can update the cursor mouse visibility. If ``False``, the Menu does not update cursor visibility
    :param onclose: Event or function executed when closing the Menu. If not ``None`` the menu disables and executes the event or function it points to. If a function (callable) is provided it can be both non-argument or single argument (Menu instance)
    :param onreset: Function executed when resetting the Menu. The function must be non-argument or single argument (Menu instance)
    :param overflow: Enables overflow on x/y axes. If ``False`` then scrollbars will not work and the maximum width/height of the scrollarea is the same as the Menu container. Style: (overflow_x, overflow_y). If ``False`` or ``True`` the value will be set on both axis
    :param position: Position on x-axis and y-axis. If the value is only 2 elements, the position is relative to the window width (thus, values must be 0-100%); else, the third element defines if the position is relative or not. If ``(x, y, False)`` the values of ``(x, y)`` are in px
    :param remember_selection: Menu remembers selection when moving through submenus. By default it is false, so, when moving back the selected widget will be the first one of the Menu
    :param rows: Number of rows of each column, if there's only 1 column ``None`` can be used for no-limit. Also, a tuple can be provided for defining different number of rows for each column, for example ``rows=10`` (each column can have a maximum 10 widgets), or ``rows=[2, 3, 5]`` (first column has 2 widgets, second 3, and third 5)
    :param screen_dimension: List/Tuple representing the dimensions the Menu should reference for sizing/positioning (width, height), if ``None`` pygame is queried for the display mode. This value defines the ``window_size`` of the Menu
    :param surface: The surface that contains the Menu. By default the Menu always considers that it is drawn on a surface that uses all window width/height. However, if a sub-surface is used the ``surface`` value will be used instead to retrieve the offset. Also, if ``surface`` is provided the menu can be drawn without providing a surface object while calling ``Menu.draw()``
    :param theme: Menu theme
    :param touchscreen: Enable/disable touch action inside the Menu. Only available on pygame 2
    :param touchscreen_motion_selection: Select widgets using touchscreen motion. If ``True`` menu draws a ``focus`` on the selected widget
    :param verbose: Enable/disable verbose mode (warnings/errors). Propagates to all widgets
    """
    _auto_centering: bool
    _background_function: Tuple[bool, Optional[Union[Callable[['Menu'], Any], CallableNoArgsType]]]
    _clock: 'pygame.time.Clock'
    _column_max_width: Union[List[None], VectorType]
    _column_max_width_zero: List[bool]
    _column_min_width: VectorType
    _column_pos_x: List[NumberType]
    _column_widths: List[NumberType]
    _columns: int
    _ctrl: 'Controller'
    _current: 'Menu'
    _decorator: 'Decorator'
    _disable_draw: bool
    _disable_exit: bool
    _disable_update: bool
    _enabled: bool
    _height: int
    _index: int
    _joy_event: int
    _joy_event_repeat: int
    _joystick: bool
    _keyboard: bool
    _keyboard_ignore_nonphysical: bool
    _last_scroll_thickness: List[Union[Tuple2IntType, int]]
    _last_selected_type: str
    _last_update_mode: List[str]
    _mainloop: bool
    _max_row_column_elements: int
    _menubar: 'MenuBar'
    _mouse: bool
    _mouse_motion_selection: bool
    _mouse_visible: bool
    _mouse_visible_default: bool
    _mouse_visible_update: bool
    _mouseover: bool
    _onbeforeopen: Optional[Callable[['Menu', 'Menu'], Any]]
    _onclose: Optional[Union['_events.MenuAction', Callable[['Menu'], Any], CallableNoArgsType]]
    _onmouseleave: Optional[Union[Callable[['Menu', EventType], Any], CallableNoArgsType]]
    _onmouseover: Optional[Union[Callable[['Menu', EventType], Any], CallableNoArgsType]]
    _onreset: Optional[Union[Callable[['Menu'], Any], CallableNoArgsType]]
    _onupdate: Optional[Union[Callable[[EventListType, 'Menu'], Any], CallableNoArgsType]]
    _onwidgetchange: Optional[Callable[['Menu', 'Widget'], Any]]
    _onwindowmouseleave: Optional[Union[Callable[['Menu'], Any], CallableNoArgsType]]
    _onwindowmouseover: Optional[Union[Callable[['Menu'], Any], CallableNoArgsType]]
    _overflow: Tuple2BoolType
    _position: Tuple2IntType
    _position_default: Tuple2IntType
    _position_relative: bool
    _prev: Optional[List[Union['Menu', List['Menu']]]]
    _remember_selection: bool
    _runtime_errors: '_MenuRuntimeErrorConfig'
    _scrollarea: 'ScrollArea'
    _scrollarea_margin: List[int]
    _sound: 'Sound'
    _stats: '_MenuStats'
    _submenus: Dict['Menu', List['Widget']]
    _surface: Optional['pygame.Surface']  # The surface that contains the menu
    _surface_last: Optional['pygame.Surface']  # The last surface used to draw the menu
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
    _widget_selected_update: bool  # Selected widget receives updates
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
        keyboard_ignore_nonphysical: bool = True,
        menu_id: str = '',
        mouse_enabled: bool = True,
        mouse_motion_selection: bool = False,
        mouse_visible: bool = True,
        mouse_visible_update: bool = True,
        onclose: Optional[Union['_events.MenuAction', Callable[['Menu'], Any], CallableNoArgsType]] = None,
        onreset: Optional[Union[Callable[['Menu'], Any], CallableNoArgsType]] = None,
        overflow: Union[Vector2BoolType, bool] = (True, True),
        position: Union[Vector2NumberType, Tuple[NumberType, NumberType, bool]] = (50, 50, True),
        remember_selection: bool = False,
        rows: MenuRowsType = None,
        screen_dimension: Optional[Vector2IntType] = None,
        surface: Optional['pygame.Surface'] = None,
        theme: 'Theme' = THEME_DEFAULT.copy(),
        touchscreen: bool = False,
        touchscreen_motion_selection: bool = False,
        verbose: bool = True
    ) -> None:
        super(Menu, self).__init__(object_id=menu_id, verbose=verbose)

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
        assert isinstance(mouse_visible_update, bool)
        assert isinstance(overflow, (VectorInstance, bool))
        assert isinstance(remember_selection, bool)
        assert isinstance(rows, (int, type(None), VectorInstance))
        assert isinstance(surface, (pygame.Surface, type(None)))
        assert isinstance(theme, Theme), \
            'theme bust be a pygame_menu.themes.Theme object instance'
        assert isinstance(touchscreen, bool)
        assert isinstance(touchscreen_motion_selection, bool)

        # Assert theme
        theme.validate()

        # Assert pygame was initialized
        assert not hasattr(pygame, 'get_init') or pygame.get_init(), \
            'pygame is not initialized'

        # Assert python version is greater than 3.8
        assert sys.version_info >= (3, 8, 0), \
            'pygame-menu only supports python equal or greater than version 3.8.0'

        # Column/row asserts
        assert columns >= 1, \
            f'the number of columns must be equal or greater than 1 (current={columns})'
        if columns > 1:
            assert rows is not None, \
                'rows cannot be None if the number of columns is greater than 1'
            if isinstance(rows, int):
                assert rows >= 1, \
                    f'if number of columns is greater than 1 (current={columns}) then the ' \
                    f'number of rows must be equal or greater than 1 (current={rows})'
                rows = [rows for _ in range(columns)]
            assert isinstance(rows, VectorInstance), \
                'if rows is not an integer it must be a tuple/list'
            assert len(rows) == columns, \
                f'the length of the rows vector must be the same as the number of' \
                f' columns (current={rows}, expected={columns})'

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
                    if self._verbose:
                        warn(
                            f'column_min_width can be a single number if there is only '
                            f'1 column, but there is {columns} columns. Thus, column_min_width '
                            f'should be a vector of {columns} items. By default a vector has '
                            f'been created using the same value for each column'
                        )
                column_min_width = [column_min_width for _ in range(columns)]
            else:
                column_min_width = [column_min_width]

        assert len(column_min_width) == columns, \
            f'column_min_width length must be the same as the number of columns, ' \
            f'but size is different {len(column_min_width)}!={columns}'
        for i in column_min_width:
            assert isinstance(i, NumberInstance), \
                'each item of column_min_width must be an integer/float'
            assert i >= 0, \
                'each item of column_min_width must be equal or greater than zero'

        # Set column max width
        if column_max_width is not None:
            if isinstance(column_max_width, NumberInstance):
                assert column_max_width >= 0, \
                    'column_max_width must be equal or greater than zero'
                if columns != 1:
                    column_max_width = [column_max_width for _ in range(columns)]
                else:
                    column_max_width = [column_max_width]

            assert len(column_max_width) == columns, \
                f'column_max_width length must be the same as the number of columns, ' \
                f'but size is different {len(column_max_width)}!={columns}'

            for i in column_max_width:
                assert isinstance(i, type(None)) or isinstance(i, NumberInstance), \
                    'each item of column_max_width can be None (no limit) or an ' \
                    'integer/float'
                assert i is None or i >= 0, \
                    'each item of column_max_width must be equal or greater than' \
                    ' zero or None'

        else:
            column_max_width = [None for _ in range(columns)]

        # Check that every column max width is equal or greater than minimum width
        for i in range(len(column_max_width)):
            if column_max_width[i] is not None:
                # noinspection PyTypeChecker
                assert column_max_width[i] >= column_min_width[i], \
                    f'item {i} of column_max_width ({column_max_width[i]}) must be equal or greater ' \
                    f'than column_min_width ({column_min_width[i]})'

        # Element size and position asserts
        if len(position) == 3:
            # noinspection PyTypeChecker
            self._position_relative = position[2]
            position = position[0:2]
        else:
            self._position_relative = True
        assert_vector(position, 2)

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
        self._decorator = Decorator(self, verbose=verbose)
        self._enabled = enabled  # Menu is enabled or not. If disabled menu can't update or draw
        self._index = -1  # Selected index, if -1 the widget does not have been selected yet
        self._last_scroll_thickness = [(0, 0), 0]  # scroll and the number of recursive states
        self._last_selected_type = ''  # Last type selection, used for test purposes
        self._mainloop = False  # Menu is in mainloop state
        self._onclose = None  # Function or event called on Menu close
        self._remember_selection = remember_selection
        self._render_enabled = True
        self._sound = Sound(verbose=verbose)
        self._stats = _MenuStats()
        self._submenus = {}
        self._surface = surface
        self._surface_last = None
        self._theme = theme

        # Set callbacks
        self.set_onclose(onclose)
        self.set_onreset(onreset)

        self._onbeforeopen = None
        self._onmouseleave = None
        self._onmouseover = None
        self._onupdate = None
        self._onwidgetchange = None
        self._onwindowmouseleave = None
        self._onwindowmouseover = None

        # Menu links (pointer to previous and next menus in nested submenus),
        # for public methods accessing, self should be used through "_current",
        # because user can move through submenus and self pointer should target
        # the current Menu object. Private methods access through self
        # (not _current) because these methods are called by public (_current) or
        # by themselves. _top is only used when moving through menus (open, reset)
        self._current = self  # Current Menu

        # Prev stores a list of Menu pointers, when accessing a submenu, prev grows
        # as prev = [prev, new_pointer]
        self._prev = None

        # Top is the same for the menus and submenus if the user moves through them
        self._top = self

        # Menu widgets, it should not be accessed outside the object as strange
        # issues can occur
        self.add = WidgetManager(self, verbose=verbose)
        self._widget_selected_update = True  # If True, the selected widget receives the updates, if False, the events only are passed to the Menu
        self._widgets = []  # This list may change during execution (replaced by a new one)

        # Stores the frames which receive update events, updated and managed only
        # by the Frame class
        self._update_frames = []

        # Stores the widgets which receive update even if not selected or events
        # is empty
        self._update_widgets = []

        # Widget surface
        self._widgets_surface = None
        self._widgets_surface_need_update = False
        self._widgets_surface_last = (0, 0, None)

        # Precache widgets surface draw, this method dramatically increases the
        # performance of the menu rendering
        self._widget_surface_cache_enabled = True

        # This boolean variable, if True, forces the cache to be updated, after
        # updating, _widget_surface_cache_need_update goes back again to False,
        # thus, the state only is used once
        self._widget_surface_cache_need_update = True

        # Columns and rows
        self._column_max_width_zero = []
        for i in range(len(column_max_width)):
            if column_max_width[i] == 0:
                self._column_max_width_zero.append(True)
            else:
                self._column_max_width_zero.append(False)

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

        # Position of Menu
        self._position_default = position
        self._position = (0, 0)
        self._translate = (0, 0)

        # Set the size
        self.resize(
            width=width,
            height=height,
            screen_dimension=screen_dimension
        )

        # Setups controller
        self._ctrl = Controller()

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
        self._keyboard_ignore_nonphysical = keyboard_ignore_nonphysical

        # Init mouse
        if mouse_motion_selection:
            assert mouse_enabled, \
                'mouse motion selection cannot be enabled if mouse is disabled'
            assert mouse_visible, \
                'mouse motion cannot be enabled if mouse is not visible'
            assert hasattr(pygame, 'MOUSEMOTION'), \
                'pygame MOUSEMOTION does not exist, thus, mouse motion selection' \
                ' cannot be enabled'
        self._mouse = mouse_enabled
        self._mouseover = False
        self._mouse_motion_selection = mouse_motion_selection
        self._mouse_visible = mouse_visible
        self._mouse_visible_default = mouse_visible
        self._mouse_visible_update = mouse_visible_update

        # Init touchscreen
        if touchscreen_motion_selection:
            assert touchscreen, \
                'touchscreen motion selection cannot be enabled if touchscreen is disabled'
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
        self._menubar._verbose = verbose

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

        self._menubar.set_menu(self)

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
            raise ValueError(f'menubar is higher than menu height ({menubar_height} > {self._height})')

        extend_y = 0 if self._theme.title_fixed else menubar_height

        self._scrollarea = ScrollArea(
            area_color=self._theme.background_color,
            area_height=self._height - extend_y,
            area_width=self._width,
            border_color=self._theme.border_color,
            border_width=self._theme.border_width,
            controls_joystick=self._joystick,
            controls_keyboard=self._keyboard,
            controls_mouse=self._mouse,
            controls_touchscreen=self._touchscreen,
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
        self._scrollarea._verbose = verbose
        self._scrollarea.set_menu(self)
        self._scrollarea.set_position(*self.get_position())
        self._overflow = (overflow[0], overflow[1])

        # Controls the behaviour of runtime errors
        self._runtime_errors = _MenuRuntimeErrorConfig()

        # Stores the last update
        self._last_update_mode = []

        # These can be changed without any major problem
        self._disable_exit = False
        self._disable_draw = False
        self._disable_widget_update_mousepos_mouseselection = False
        self._disable_update = False
        self._validate_frame_widgetmove = True

    def resize(
        self,
        width: NumberType,
        height: NumberType,
        screen_dimension: Optional[Vector2IntType] = None,
        position: Optional[Union[Vector2NumberType, Tuple[NumberType, NumberType, bool]]] = None,
        recursive: bool = False
    ) -> 'Menu':
        """
        Resizes the menu to another width/height.

        :param width: Menu width (px)
        :param height: Menu height (px)
        :param screen_dimension: List/Tuple representing the dimensions the Menu should reference for sizing/positioning (width, height), if ``None`` pygame is queried for the display mode. This value defines the ``window_size`` of the Menu
        :param position: Position on x-axis and y-axis. If the value is only 2 elements, the position is relative to the window width (thus, values must be 0-100%); else, the third element defines if the position is relative or not. If ``(x, y, False)`` the values of ``(x, y)`` are in px. If ``None`` use the default from the menu constructor
        :param recursive: If true, resize all submenus in a recursive fashion
        :return: Self reference
        """
        assert isinstance(width, NumberInstance)
        assert isinstance(height, NumberInstance)
        assert width > 0 and height > 0, \
            'menu width and height must be greater than zero'
        assert isinstance(recursive, bool)

        # Resize recursively
        if recursive:
            for menu in self.get_submenus(True):
                menu.resize(width, height, screen_dimension, position)

        # Convert to int
        width, height = int(width), int(height)

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

        # Check menu sizing
        window_width, window_height = self._window_size
        assert width <= window_width and height <= window_height, \
            f'menu size ({width}x{height}) must be lower or equal than the size of the ' \
            f'window ({window_width}x{window_height})'

        # Store width and height
        self._height = height
        self._width = width

        # Compute widget offset
        self._widget_offset = [self._theme.widget_offset[0], self._theme.widget_offset[1]]
        if abs(self._widget_offset[0]) < 1:
            self._widget_offset[0] *= self._width
        if abs(self._widget_offset[1]) < 1:
            self._widget_offset[1] *= self._height

        # Cast to int offset
        self._widget_offset[0] = int(self._widget_offset[0])
        self._widget_offset[1] = int(self._widget_offset[1])

        # If centering is enabled, but widget offset in the vertical is different
        # from zero a warning is raised
        if self._auto_centering and self._widget_offset[1] != 0:
            if self._verbose:
                warn(
                    f'menu is vertically centered (center_content=True), but widget '
                    f'offset (from theme) is different than zero ({self._widget_offset[1]}px). '
                    f'Auto-centering has been disabled'
                )
            self._auto_centering = False

        # Scroll area outer margin
        self._scrollarea_margin = [self._theme.scrollarea_outer_margin[0], self._theme.scrollarea_outer_margin[1]]
        if abs(self._scrollarea_margin[0]) < 1:
            self._scrollarea_margin[0] *= self._width
        if abs(self._scrollarea_margin[1]) < 1:
            self._scrollarea_margin[1] *= self._height
        self._scrollarea_margin[0] = int(self._scrollarea_margin[0])
        self._scrollarea_margin[1] = int(self._scrollarea_margin[1])

        # If centering is enabled, but ScrollArea margin in the vertical is
        # different from zero a warning is raised
        if self._auto_centering and self._scrollarea_margin[1] != 0:
            if self._verbose:
                warn(
                    f'menu is vertically centered (center_content=True), but '
                    f'ScrollArea outer margin (from theme) is different than zero '
                    f'({round(self._scrollarea_margin[1], 3)}px). Auto-centering has been disabled'
                )
            self._auto_centering = False

        # Configure menubar
        extend_y = 0
        if hasattr(self, '_menubar'):
            self._menubar._width = self._width
            menubar_height = self._menubar.get_height()
            if self._height - menubar_height <= 0:
                raise ValueError(f'menubar is higher than menu height ({menubar_height} > {self._height})')
            extend_y = 0 if self._theme.title_fixed else menubar_height

        # Configure scrollbar
        if hasattr(self, '_scrollarea'):
            self._scrollarea.create_rect(self._width, self._height - extend_y)

        # Update column max width
        for i in range(len(self._column_max_width)):
            if self._column_max_width_zero[i]:
                # noinspection PyTypeChecker
                self._column_max_width[i] = self._width

        # Force the rendering
        if self._widgets_surface is not None:
            self._widgets_surface_need_update = True

        # Update the menu position
        if position is None:
            position = self._position_default
        else:
            if len(position) == 3:
                # noinspection PyTypeChecker
                self._position_relative = position[2]
            else:
                self._position_relative = True
        if self._position_relative:
            self.set_relative_position(position[0], position[1])
        else:
            self.set_absolute_position(position[0], position[1])
        return self

    def __copy__(self) -> 'Menu':
        """
        Copy method.

        :return: Raises copy exception
        """
        raise _MenuCopyException('Menu class cannot be copied')

    def __deepcopy__(self, memodict: Dict) -> 'Menu':
        """
        Deep-copy method.

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
        Menu, it receives the current Menu and the next Menu. This method is only
        executed programatically (by calling ``menu._open``) or by applying to
        certain widgets, like :py:class:`pygame_menu.widgets.Button`. Rendering, or
        drawing the current Menu does not trigger this event.

        .. code-block:: python

            onbeforeopen(current Menu <from>, next Menu <to>)

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param onbeforeopen: Onbeforeopen callback, it can be a function or None
        :return: Self reference
        """
        assert callable(onbeforeopen) or onbeforeopen is None, \
            'onbeforeopen must be callable (function-type) or None'
        self._onbeforeopen = onbeforeopen
        return self

    def set_onupdate(
        self,
        onupdate: Optional[Union[Callable[[EventListType, 'Menu'], Any], CallableNoArgsType]]
    ) -> 'Menu':
        """
        Set ``onupdate`` callback. Callback is executed before updating the Menu,
        it receives the event list and the Menu reference; also, ``onupdate`` can
        receive zero arguments:

        .. code-block:: python

            onupdate(event_list, menu) <or> onupdate()

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param onupdate: Onupdate callback, it can be a function or None
        :return: Self reference
        """
        assert callable(onupdate) or onupdate is None, \
            'onupdate must be a callable (function-type) or None'
        self._onupdate = onupdate
        return self

    def set_onclose(
        self,
        onclose: Optional[Union['_events.MenuAction', Callable[['Menu'], Any], CallableNoArgsType]]
    ) -> 'Menu':
        """
        Set ``onclose`` callback. Callback can only receive 1 argument maximum
        (if not ``None``), if so, the Menu instance is provided:

        .. code-block:: python

            onclose(menu) <or> onclose()

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param onclose: Onclose callback, it can be a function, a pygame-menu event, or None
        :return: Self reference
        """
        assert callable(onclose) or _events.is_event(onclose) or onclose is None, \
            'onclose must be a MenuAction (event), callable (function-type), or None'
        if onclose == _events.NONE:
            onclose = None
        self._onclose = onclose
        return self

    def set_onreset(
        self,
        onreset: Optional[Union[Callable[['Menu'], Any], CallableNoArgsType]]
    ) -> 'Menu':
        """
        Set ``onreset`` callback. Callback can only receive 1 argument maximum
        (if not ``None``), if so, the Menu instance is provided:

        .. code-block:: python

            onreset(menu) <or> onreset()

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param onreset: Onreset callback, it can be a function or None
        :return: Self reference
        """
        assert callable(onreset) or onreset is None, \
            'onreset must be a callable (function-type) or None'
        self._onreset = onreset
        return self

    def set_onwindowmouseover(
        self,
        onwindowmouseover: Optional[Union[Callable[['Menu'], Any], CallableNoArgsType]]
    ) -> 'Menu':
        """
        Set ``onwindowmouseover`` callback. This method is executed in
        :py:meth:`pygame_menu.menu.Menu.update` method. The callback function
        receives the following arguments:

        .. code-block:: python

            onwindowmouseover(menu) <or> onwindowmouseover()

        :param onwindowmouseover: Callback executed if user enters the window with the mouse; it can be a function or None
        :return: Self reference
        """
        if onwindowmouseover is not None:
            assert callable(onwindowmouseover), \
                'onwindowmouseover must be callable (function-type) or None'
        self._onwindowmouseover = onwindowmouseover
        return self

    def set_onwindowmouseleave(
        self,
        onwindowmouseleave: Optional[Union[Callable[['Menu'], Any], CallableNoArgsType]]
    ) -> 'Menu':
        """
        Set ``onwindowmouseleave`` callback. This method is executed in
        :py:meth:`pygame_menu.menu.Menu.update` method. The callback function
        receives the following arguments:

        .. code-block:: python

            onwindowmouseleave(menu) <or> onwindowmouseleave()

        :param onwindowmouseleave: Callback executed if user leaves the window with the mouse; it can be a function or None
        :return: Self reference
        """
        if onwindowmouseleave is not None:
            assert callable(onwindowmouseleave), \
                'onwindowmouseleave must be callable (function-type) or None'
        self._onwindowmouseleave = onwindowmouseleave
        return self

    def set_onwidgetchange(
        self,
        onwidgetchange: Optional[Callable[['Menu', 'Widget'], Any]]
    ) -> 'Menu':
        """
        Set ``onwidgetchange`` callback. This method is executed if any appended
        widget changes its value. The callback function receives the following
        arguments:

        .. code-block:: python

            onwidgetchange(menu, widget)

        :param onwidgetchange: Callback executed if an appended widget changes its value
        :return: Self reference
        """
        if onwidgetchange is not None:
            assert callable(onwidgetchange), \
                'onwidgetchange must be callable (function-type) or None'
        self._onwidgetchange = onwidgetchange
        return self

    def set_onmouseover(
        self,
        onmouseover: Optional[Union[Callable[['Menu', EventType], Any], CallableNoArgsType]]
    ) -> 'Menu':
        """
        Set ``onmouseover`` callback. This method is executed in
        :py:meth:`pygame_menu.menu.Menu.update` method. The callback function
        receives the following arguments:

        .. code-block:: python

            onmouseover(menu, event) <or> onmouseover()

        :param onmouseover: Callback executed if user enters the Menu with the mouse; it can be a function or None
        :return: Self reference
        """
        if onmouseover is not None:
            assert callable(onmouseover), \
                'onmouseover must be callable (function-type) or None'
        self._onmouseover = onmouseover
        return self

    def set_onmouseleave(
        self,
        onmouseleave: Optional[Union[Callable[['Menu', EventType], Any], CallableNoArgsType]]
    ) -> 'Menu':
        """
        Set ``onmouseleave`` callback. This method is executed in
        :py:meth:`pygame_menu.menu.Menu.update` method. The callback function
        receives the following arguments:

        .. code-block:: python

            onmouseleave(menu, event) <or> onmouseleave()

        :param onmouseleave: Callback executed if user leaves the Menu with the mouse; it can be a function or None
        :return: Self reference
        """
        if onmouseleave is not None:
            assert callable(onmouseleave), \
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
        elif isinstance(widget, str):
            widget = self.get_widget(widget)
        assert isinstance(widget, Widget)
        if not widget.is_selectable:
            raise ValueError(f'{widget.get_class_id()} is not selectable')
        elif not widget.is_visible():  # Considers frame
            raise ValueError(f'{widget.get_class_id()} is not visible')
        try:
            index = self._widgets.index(widget)  # If not exists this raises ValueError
        except ValueError:
            raise ValueError(f'{widget.get_class_id()} is not in Menu, check if exists on the current '
                             f'with menu.get_current().remove_widget(widget)')
        self._select(index, 1, SELECT_WIDGET, False)
        self.force_surface_cache_update()
        return self

    def unselect_widget(self) -> 'Menu':
        """
        Unselects the current widget.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :return: Self reference
        """
        return self.select_widget(None)

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
        self._update_after_remove_or_hidden(index)  # Forces surface update
        self._stats.removed_widgets += 1

        # If widget is within a frame, remove from frame
        frame = widget.get_frame()
        if frame is not None:
            frame.unpack(widget)

        # If widget points to a hook, remove the submenu
        # noinspection PyProtectedMember
        menu_hook = widget._menu_hook
        if menu_hook in self._submenus.keys():
            self._remove_submenu(menu_hook, widget)
            widget._menu_hook = None

        widget.on_remove_from_menu()
        # Removes Menu reference from widget. If Frame, it removes from _update_frames
        widget.set_menu(None)

        # Remove widget from update lists
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
            # If added on execution time forces the update of the surface
            self._widgets_surface = None

    def _back(self) -> None:
        """
        Go to previous Menu or close if the top Menu is currently displayed.
        """
        if self._top._prev is not None:
            self.reset(1)
        else:
            self._close()

    def _update_selection_if_hidden(self) -> None:
        """
        Updates the Menu widget selection if a widget was hidden.
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
        """
        # Column widgets
        self._widget_columns = {}
        for i in range(self._columns):
            self._widget_columns[i] = []

        # Set the column widths (minimum values), safe for certain widgets that
        # request the width on rendering
        self._column_widths = []
        column_widths = [self._column_min_width[i] for i in range(self._columns)]

        # Set column/row of each widget and compute maximum width of each column if None
        self._used_columns = 0
        max_elements_msg = \
            f'total visible/non-floating widgets ([widg]) cannot exceed columns*rows' \
            f'({self._max_row_column_elements} elements). Menu position update failed.' \
            f' If using frames, please pack before adding new widgets'
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
                    if self._verbose:
                        warn(f'{widget.get_class_id()} failed to update')
                    raise
                has_frame = True

            # If not visible, or within frame, continue to the next widget
            if not widget.is_visible() or widget.get_frame() is not None:
                widget.set_col_row_index(-1, -1, index)
                continue

            # Check if the maximum number of elements was reached, if so raise an exception
            # If menu has frames, this check is disabled
            elif not has_frame and not i_index < self._max_row_column_elements:
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

            # Get the next widget; if it doesn't exist, use the same
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
                f'several widgets are selected at the same time, current selected '
                f'(sorted by index): {selected_widget}, but the following are also'
                f' selected: {", ".join(invalid_selection_widgets)}. If widget is'
                f' selected outside the menu, use widget.select(update_menu=True)'
            )

        # Apply max width column limit
        for col in range(self._used_columns):
            if self._column_max_width[col] is not None:
                column_widths[col] = min(column_widths[col], self._column_max_width[col])

        # If some columns were not used, set these widths to zero
        for col in range(self._used_columns, self._columns):
            column_widths.pop()
            try:
                del self._widget_columns[col]
            except KeyError:
                pass

        # If the total weight is less than the window width (so there's no horizontal
        # scroll), scale the columns. Only None column_max_widths and columns less
        # than the maximum are scaled
        sum_width_columns = sum(column_widths)
        max_width = self.get_width(inner=True)
        if 0 <= sum_width_columns < max_width and len(self._widgets) > 0:

            # First, scale columns to its maximum
            sum_contrib: List[float] = []
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
            sum_contrib: List[float] = []
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
                mod_width = max_width  # Available left width for non-max columns
                non_max = self._used_columns

                # First fill all maximum width columns
                for col in range(self._used_columns):
                    if self._column_max_width[col] is not None:
                        column_widths[col] = min(self._column_max_width[col], max_width / self._used_columns)
                        mod_width -= column_widths[col]
                        non_max -= 1

                # Now, update the rest (non-maximum set)
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
            selection_effect_margin = widget.get_selection_effect().get_margin()
            width = get_rect(widget).width

            if not widget.is_visible():
                widget.set_position(0, 0)
                continue

            # If widget within frame update col/row position
            elif widget.get_frame() is not None:
                # noinspection PyProtectedMember
                widget._set_position_relative_to_frame(index)
                continue

            # Get column and row position
            col, row, _ = widget.get_col_row_index()

            # Calculate X position
            column_width = self._column_widths[col]
            selection_margin = 0
            dx = 0
            sm_left, sm_right = selection_effect_margin[1], selection_effect_margin[3]
            if align == ALIGN_CENTER:
                dx = -(width + sm_right - sm_left) / 2
            elif align == ALIGN_LEFT:
                selection_margin = sm_left
                dx = -column_width / 2 + selection_margin
            elif align == ALIGN_RIGHT:
                selection_margin = sm_right
                dx = column_width / 2 - width - selection_margin
            d_border = int(math.ceil(widget.get_border()[1] / 2))

            # self._column_pos_x points at the middle of each column
            x_coord = self._column_pos_x[col] + dx + margin[0] + padding[3]
            x_coord = max(selection_margin, x_coord)
            x_coord += max(0, self._widget_offset[0]) + d_border

            # Check if widget width exceeds column max width
            max_column_width = self._column_max_width[col]
            if max_column_width is not None and width > max_column_width:
                raise _MenuSizingException(
                    f'{widget.get_class_id()} widget width ({width}) exceeds column {col + 1} max width ({max_column_width})'
                )

            # Calculate Y position
            y_sum = 1  # Compute the total height from the current row position to the top of the column
            for r_widget in self._widget_columns[col]:
                _, r, _ = r_widget.get_col_row_index()
                if r >= row:
                    break
                elif (
                    r_widget.is_visible() and
                    not r_widget.is_floating() and
                    not r_widget.get_frame() is not None
                ):
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

            # If the widget is floating and has origin-position
            # noinspection PyProtectedMember
            if widget.is_floating() and widget._floating_origin_position:
                widget.set_position(
                    x=max(0, self._widget_offset[0]) + padding[3],
                    y=menubar_height + padding[0] + d_border)
                continue

            # Add the widget translation to the widget for computing the min/max position. This
            # feature does not work as intended as there's edge cases not covered, and centering makes
            # the translation more difficult
            # tx, ty = widget.get_translate()
            tx, ty = 0, 0

            # Update max/min position, minus padding
            min_max_updated = True
            max_x = max(max_x, x_coord + width - padding[1] + tx + sm_right)  # minus right padding
            max_y = max(max_y, y_coord + get_rect(widget).height - padding[2] + ty)  # minus bottom padding
            min_x = min(min_x, x_coord - padding[3] - sm_left)
            min_y = min(min_y, y_coord - padding[0])

            # Restore the discounted scrollbar thickness
            if self._theme.widget_alignment_ignore_scrollbar_thickness:
                x_coord += self._get_scrollbar_thickness()[1] / 2

            # Update the position of the widget
            widget.set_position(x_coord, y_coord)

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

        # Check if there is an overflow
        overflow_x = max_x - (self._width - sy) > 1
        overflow_y = max_y - (self._height - sx - menubar_height) > 1

        # Remove the thick of the scrollbar to avoid displaying a horizontal one
        # If overflow on both axis
        if overflow_x and overflow_y:
            width, height = max_x, max_y
            if not self._mouse_visible:
                self._mouse_visible = True

        # If horizontal overflow
        elif overflow_x:
            width, height = max_x, self._height - menubar_height - sx
            self._mouse_visible = self._mouse_visible_default

        # If vertical overflow
        elif overflow_y:
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
        if width == self._widgets_surface_last[0] and height == self._widgets_surface_last[1]:
            self._widgets_surface = self._widgets_surface_last[2]
        else:
            self._widgets_surface = make_surface(width, height)
            self._widgets_surface_last = (width, height, self._widgets_surface)

        # Set position
        self._scrollarea.set_world(self._widgets_surface)
        self._scrollarea.set_position(*self.get_position())

        # Check if the scrollbars changed
        sx, sy = self._get_scrollbar_thickness()
        if (sx, sy) != self._last_scroll_thickness[0] and self._last_scroll_thickness[1] == 0:
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
        """
        assert isinstance(widget_id, str)
        for widget in self._widgets:
            if widget.get_id() == widget_id:
                raise IndexError(
                    f'widget id "{widget_id}" already exists on the current menu ({widget.get_class_id()})'
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
        elif callable(onclose):
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
        prev = self._top._prev
        depth: int = 0
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

            This method does not fire ``onclose`` callback. Use ``Menu.close()``
            instead.

        :return: Self reference
        """
        check_widget_mouseleave(force=True)
        self._top._enabled = False
        return self

    def set_absolute_position(self, position_x: NumberType, position_y: NumberType) -> 'Menu':
        """
        Set the absolute Menu position.

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
        self._position = (position_x, position_y)
        self._widgets_surface = None  # This forces an update of the widgets
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
        if len(self._widgets) == 0:  # If this happens, get_widget_max returns an immense value
            self._widget_offset[1] = 0
            return self
        elif self._widgets_surface is None:
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

        :return: Scrollbar thickness in px (horizontal, vertical)
        """
        if not hasattr(self, '_scrollarea'):  # Prevent issues if computing
            return 0, 0
        return self._scrollarea.get_scrollbar_thickness(ORIENTATION_HORIZONTAL), \
            self._scrollarea.get_scrollbar_thickness(ORIENTATION_VERTICAL)

    def get_width(self, inner: bool = False, widget: bool = False, border: bool = False) -> int:
        """
        Get the Menu width.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param inner: If ``True`` returns the available width (menu width minus scroll if visible)
        :param widget: If ``True`` returns the total width used by the widgets
        :param border: If ``True`` add the mmenu border width. Only applied if both ``inner`` and ``widget`` are ``False``
        :return: Width in px
        """
        if widget:
            return int(self._widget_max_position[0] - self._widget_min_position[0])
        elif not inner:
            bw: int = 0 if not border else 2 * self._scrollarea.get_border_size()[0]
            return int(self._width) + bw
        return int(self._width - self._get_scrollbar_thickness()[1])

    def get_height(self, inner: bool = False, widget: bool = False, border: bool = False) -> int:
        """
        Get the Menu height.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param inner: If ``True`` returns the available height (menu height minus scroll and menubar)
        :param widget: If ``True`` returns the total height used by the widgets
        :param border: If ``True`` add the menu border height. Only applied if both ``inner`` and ``widget`` are ``False``
        :return: Height in px
        """
        if widget:
            return int(self._widget_max_position[1] - self._widget_min_position[1])
        elif not inner:
            bh = 0 if not border else 2 * self._scrollarea.get_border_size()[1]
            return int(self._height) + bh
        return int(self._height - self._menubar.get_height() - self._get_scrollbar_thickness()[0])

    def get_size(self, inner: bool = False, widget: bool = False, border: bool = False) -> Vector2IntType:
        """
        Return the Menu size as a tuple of (width, height) in px.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param inner: If ``True`` returns the available size (width, height) (menu height minus scroll and menubar)
        :param widget: If ``True`` returns the total (width, height) used by the widgets
        :param border: If ``True`` add the border size to the dimensions (width, height). Only applied if both ``inner`` and ``widget`` are ``False``
        :return: Tuple of (width, height) in px
        """
        return self.get_width(inner=inner, widget=widget, border=border), \
            self.get_height(inner=inner, widget=widget, border=border)

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
        if not self._render_enabled:
            return False  # Modify using Menu.disable_render() and Menu.enable_render()
        t0: float = time.time()
        changed: bool = False

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

    def disable_render(self) -> 'Menu':
        """
        Disable the render of the Menu. Useful to improve performance when
        adding many widgets. Must be turned on after finishing the build.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :return: Self reference
        """
        self._render_enabled = False
        return self

    def enable_render(self) -> 'Menu':
        """
        Enable the Menu rendering. Useful to improve performance when
        adding many widgets.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :return: Self reference
        """
        self._render_enabled = True
        self._render()
        return self

    def draw(self, surface: Optional['pygame.Surface'] = None, clear_surface: bool = False) -> 'Menu':
        """
        Draw the **current** Menu into the given surface.

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.menu.Menu.get_current`,
            for example, ``menu.get_current().draw(...)``

        :param surface: Pygame surface to draw the Menu. If None, the Menu will use the provided ``surface`` from the constructor
        :param clear_surface: Clear surface using theme ``surface_clear_color``
        :return: Self reference **(current)**
        """
        if surface is None:
            surface = self._surface
        assert isinstance(surface, pygame.Surface)
        assert isinstance(clear_surface, bool)

        # Update last surface
        self._surface_last = surface

        if not self.is_enabled():
            self._current._runtime_errors.throw(self._current._runtime_errors.draw, 'menu is not enabled')
            return self._current
        elif self._current._disable_draw:
            return self._current

        # Render menu; if True, the surface widget has changed, thus cache should
        # change if enabled
        render = self._current._render()

        # Updates title
        if (self._current._theme.title_updates_pygame_display and
            pygame.display.get_caption()[0] != self._current.get_title()):
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
        if (
            not self._current._widget_surface_cache_enabled or
            render or
            self._current._widget_surface_cache_need_update
        ):
            # This should be updated before drawing widgets. As widget
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
            selected_widget_draw: Tuple[Optional['Widget'], Optional['pygame.Surface']] = (None, None)

            for widget in self._current._widgets:
                # Widgets within frames are not drawn as it's frame draw these widgets
                if widget.get_frame() is not None:
                    continue
                elif widget.is_selected():
                    selected_widget_draw = widget, self._current._widgets_surface
                widget.draw(self._current._widgets_surface)

            if selected_widget_draw[0] is not None:
                selected_widget_draw[0].draw_after_if_selected(selected_widget_draw[1])

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
        :return: The focus region, ``None`` if the focus could not be possible
        """
        assert isinstance(surface, pygame.Surface)
        assert isinstance(widget, (Widget, type(None)))

        force = force or (widget is not None and widget.active and widget.force_menu_draw_focus)
        if not force and (
            widget is None
            or not widget.active
            or not widget.is_selectable
            or not widget.is_selected()
            or not (self._mouse_motion_selection or self._touchscreen_motion_selection)
            or not widget.is_visible()
        ):
            return None
        window_width, window_height = self._window_size

        self._render()  # Surface may be none, then update the positioning
        rect = widget.get_focus_rect()

        # Apply selection effect
        rect = widget.get_selection_effect().inflate(rect)
        if rect.width == 0 or rect.height == 0:
            return None

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

    def set_controller(self, controller: 'Controller', apply_to_widgets: bool = False) -> 'Menu':
        """
        Set a new controller object.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param controller: Controller
        :param apply_to_widgets: If ``True``, apply this controller to all menu widgets
        :return: Self reference
        """
        self._ctrl = controller
        if apply_to_widgets:
            for w in self._widgets:
                w.set_controller(controller)
        return self

    def get_controller(self) -> 'Controller':
        """
        Return the menu controller object.

        :return: Controller
        """
        return self._ctrl

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
        """
        if self._disable_exit:
            return
        self.disable()
        pygame.quit()
        try:
            sys.exit(0)
        except SystemExit:
            # noinspection PyUnresolvedReferences,PyProtectedMember
            os._exit(1)
        # This should be unreachable
        # noinspection PyUnreachableCode
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
                _, r, i = widget.get_col_row_index()
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

        return _default()

    def _handle_joy_event(self, apply_sound: bool = False) -> bool:
        """
        Handle joy events.

        :param apply_sound: Apply sound on widget selection
        :return: ``True`` if the widget changed
        """
        if self._joy_event & JOY_EVENT_UP:
            return self._select(self._index - 1, -1, SELECT_KEY, apply_sound)
        elif self._joy_event & JOY_EVENT_DOWN:
            return self._select(self._index + 1, 1, SELECT_KEY, apply_sound)
        elif self._joy_event & JOY_EVENT_LEFT:
            return self._move_selected_left_right(-1, apply_sound)
        elif self._joy_event & JOY_EVENT_RIGHT:
            return self._move_selected_left_right(1, apply_sound)
        return False

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
        selected_in_frame_horizontal = selected_widget is not None and \
                                       selected_widget.get_frame() is not None and \
                                       selected_widget.get_frame().horizontal
        selected_last_in_frame = selected_in_frame_horizontal and \
                                 selected_widget.get_frame().last_index == self._current._index

        # If current selected in within a horizontal frame
        if selected_in_frame_horizontal and not selected_last_in_frame:
            return self._current._select(self._current._index + 1, 1, SELECT_KEY, False)
        elif self._current._used_columns > 1:
            return self._current._move_selected_left_right(1)
        return False

    def get_last_surface_offset(self) -> Tuple2IntType:
        """
        Return the last menu surface offset.

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.menu.Menu.get_current`,
            for example, ``menu.get_current().update(...)``.

        :return: Return the offset of the last surface used. If ``surface`` param was provided within Menu constructor that offset will be used instead, else, the returned value will be the last surface used to draw the Menu. Else, ``(0, 0)`` will be returned
        """
        if self._surface is not None:
            return self._surface.get_offset()
        return self._surface_last.get_offset() if self._surface_last is not None else (0, 0)

    def get_last_update_mode(self) -> List[str]:
        """
        Return the update mode.

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.menu.Menu.get_current`,
            for example, ``menu.get_current().update(...)``.

        :return: Returns a string that represents the update status, see ``pygame_menu.events``. Some also indicate which widget updated in the format ``EVENT_NAME#widget_id``
        """
        if len(self._current._last_update_mode) == 0:
            return [_events.MENU_LAST_NONE]
        return self._current._last_update_mode

    def update(self, events: EventVectorType) -> bool:
        """
        Update the status of the Menu using external events. The update event is
        applied only on the **current** Menu.

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.menu.Menu.get_current`,
            for example, ``menu.get_current().update(...)``.

        :param events: List of pygame events
        :return: ``True`` if the menu updated (or a widget)
        """
        # Check events
        assert isinstance(events, list)
        self._current._last_update_mode = []

        # If menu is not enabled
        if not self.is_enabled():
            self._current._runtime_errors.throw(self._current._runtime_errors.update,
                                                'menu is not enabled')
        self._current._stats.update += 1

        # Call onupdate callback
        if self._current._onupdate is not None:
            try:
                self._current._onupdate(events, self._current)
            except TypeError:
                self._current._onupdate()
        if self._current._disable_update:
            self._current._last_update_mode.append(_events.MENU_LAST_DISABLE_UPDATE)
            return False

        # If any widget status changes, set the status as True
        updated = False

        # Update mouse
        if self._mouse_visible_update:
            pygame.mouse.set_visible(self._current._mouse_visible)
        mouse_motion_event = None

        selected_widget = self._current.get_selected_widget()
        selected_widget_disable_frame_update = (
            (False if selected_widget is None else selected_widget.active) and self._current._mouse_motion_selection or
            selected_widget is not None and selected_widget.active and selected_widget.force_menu_draw_focus
        )
        selected_widget_scrollarea = None if selected_widget is None else selected_widget.get_scrollarea()

        # First, check update frames
        frames_updated = False
        if not selected_widget_disable_frame_update:
            for frame in self._current._update_frames:
                frames_updated = frames_updated or frame.update_menu(events)

        # Update widgets on update list
        for widget in self._current._update_widgets:
            widget.update_menu(events)

        # Frames have updated
        if frames_updated:
            self._current._last_update_mode.append(_events.MENU_LAST_FRAMES)
            updated = True

        # Update scroll bars
        elif not selected_widget_disable_frame_update and self._current._scrollarea.update(events):
            self._current._last_update_mode.append(_events.MENU_LAST_SCROLL_AREA)
            updated = True

        # Update the menubar, it may change the status of the widget because
        # of the button back/close
        elif self._current._menubar.update_menu(events):
            self._current._last_update_mode.append(_events.MENU_LAST_MENUBAR)
            updated = True

        # Check selected widget
        elif (
            selected_widget is not None and
            self._current._widget_selected_update and
            selected_widget.update_menu(events)
        ):
            self._current._last_update_mode.append(
                f'{_events.MENU_LAST_SELECTED_WIDGET_EVENT}#{selected_widget.get_id()}'
            )
            updated = True

        # Check others
        else:

            # If mouse motion enabled, add the current mouse position to the events list
            if self._current._mouse and self._current._mouse_motion_selection:
                events.append(mouse_motion_current_mouse_position())

            for event in events:
                # User closes window
                close_altf4 = (
                    event.type == pygame.KEYDOWN and
                    event.key == pygame.K_F4 and
                    (event.mod == pygame.KMOD_LALT or event.mod == pygame.KMOD_RALT)
                )
                if event.type == _events.PYGAME_QUIT or close_altf4 or event.type == _events.PYGAME_WINDOWCLOSE:
                    self._current._last_update_mode.append(_events.MENU_LAST_QUIT)
                    self._current._exit()
                    return True

                # User press key
                elif event.type == pygame.KEYDOWN and self._current._keyboard:
                    # Check key event is valid
                    if self._keyboard_ignore_nonphysical and not check_key_pressed_valid(event):
                        continue

                    elif self._ctrl.move_down(event, self):
                        if self._current._down(apply_sound=True):
                            self._current._last_update_mode.append(_events.MENU_LAST_MOVE_DOWN)
                            updated = True
                            break

                    elif self._ctrl.move_up(event, self):
                        if self._current._up(apply_sound=True):
                            self._current._last_update_mode.append(_events.MENU_LAST_MOVE_UP)
                            updated = True
                            break

                    elif self._ctrl.left(event, self):
                        if self._current._left(apply_sound=True):
                            self._current._last_update_mode.append(_events.MENU_LAST_MOVE_LEFT)
                            updated = True
                            break

                    elif self._ctrl.right(event, self):
                        if self._current._right(apply_sound=True):
                            self._current._last_update_mode.append(_events.MENU_LAST_MOVE_RIGHT)
                            updated = True
                            break

                    elif self._ctrl.back(event, self) and self._top._prev is not None:
                        self._current._sound.play_close_menu()
                        self.reset(1)  # public, do not use _current
                        self._current._last_update_mode.append(_events.MENU_LAST_MENU_BACK)
                        updated = True

                    elif self._ctrl.close_menu(event, self):
                        self._current._sound.play_close_menu()
                        if self._current._close():
                            self._current._last_update_mode.append(_events.MENU_LAST_MENU_CLOSE)
                            updated = True

                # User moves hat joystick
                elif event.type == pygame.JOYHATMOTION and self._current._joystick:
                    if self._ctrl.joy_up(event, self):
                        if self._current._down(apply_sound=True):
                            self._current._last_update_mode.append(_events.MENU_LAST_MOVE_DOWN)
                            updated = True
                            break

                    elif self._ctrl.joy_down(event, self):
                        if self._current._up(apply_sound=True):
                            self._current._last_update_mode.append(_events.MENU_LAST_MOVE_UP)
                            updated = True
                            break

                    elif self._ctrl.joy_left(event, self):
                        if self._current._left(apply_sound=True):
                            self._current._last_update_mode.append(_events.MENU_LAST_MOVE_LEFT)
                            updated = True
                            break

                    elif self._ctrl.joy_right(event, self):
                        if self._current._right(apply_sound=True):
                            self._current._last_update_mode.append(_events.MENU_LAST_MOVE_RIGHT)
                            updated = True
                            break

                # User moves joy axis motion
                elif event.type == pygame.JOYAXISMOTION and self._current._joystick and hasattr(event, 'axis'):
                    prev = self._current._joy_event
                    self._current._joy_event = 0

                    if self._ctrl.joy_axis_y_up(event, self):
                        self._current._joy_event |= JOY_EVENT_UP

                    elif self._ctrl.joy_axis_y_down(event, self):
                        self._current._joy_event |= JOY_EVENT_DOWN

                    elif self._ctrl.joy_axis_x_left(event, self) and self._current._used_columns > 1:
                        self._current._joy_event |= JOY_EVENT_LEFT

                    elif self._ctrl.joy_axis_x_right(event, self) and self._current._used_columns > 1:
                        self._current._joy_event |= JOY_EVENT_RIGHT

                    if self._current._joy_event:
                        sel = self._current._handle_joy_event(True)
                        if self._current._joy_event == prev:
                            pygame.time.set_timer(self._current._joy_event_repeat, self._ctrl.joy_repeat)
                        else:
                            pygame.time.set_timer(self._current._joy_event_repeat, self._ctrl.joy_delay)
                        if sel:
                            self._current._last_update_mode.append(_events.MENU_LAST_JOY_REPEAT)
                            updated = True
                            break
                    else:
                        pygame.time.set_timer(self._current._joy_event_repeat, 0)

                # User repeats previous joy event input
                elif event.type == self._current._joy_event_repeat:
                    if self._current._joy_event:
                        sel = self._current._handle_joy_event(True)
                        pygame.time.set_timer(self._current._joy_event_repeat, self._ctrl.joy_repeat)
                        if sel:
                            self._current._last_update_mode.append(_events.MENU_LAST_JOY_REPEAT)
                            updated = True
                            break
                    else:
                        pygame.time.set_timer(self._current._joy_event_repeat, 0)

                # Select widget by clicking
                elif (event.type == pygame.MOUSEBUTTONDOWN and self._current._mouse and
                      event.button in (1, 2, 3)):  # Don't consider the mouse wheel (button 4 & 5)

                    # If the mouse motion selection is disabled then select a widget by clicking
                    if not self._current._mouse_motion_selection:
                        sel = False
                        for index in range(len(self._current._widgets)):
                            widget = self._current._widgets[index]
                            if isinstance(widget, Frame):  # Frame does not accept click
                                continue
                            elif (widget.is_selectable and widget.is_visible() and
                                  widget.get_scrollarea().collide(widget, event)):
                                sel = self._current._select(index, 1, SELECT_MOUSE_BUTTON_DOWN, True)
                                break

                        if sel:
                            self._current._last_update_mode.append(
                                f'{_events.MENU_LAST_WIDGET_SELECT}#{self._current.get_selected_widget().get_id()}'
                            )
                            updated = True
                            break

                    # If mouse motion selection, clicking will disable the active state
                    # only if the user clicked outside the widget
                    else:
                        if selected_widget is not None and selected_widget.active:
                            focus_rect = selected_widget.get_focus_rect()
                            if not selected_widget_scrollarea.collide(focus_rect, event):
                                selected_widget.active = False
                                selected_widget.render()  # Some widgets need to be rendered
                                self._current._last_update_mode.append(
                                    f'{_events.MENU_LAST_WIDGET_DISABLE_ACTIVE_STATE}#{selected_widget.get_id()}'
                                )
                                updated = True
                                break

                # Mouse enters or leaves the window
                elif event.type == pygame.ACTIVEEVENT and hasattr(event, 'gain'):
                    if event.gain == 1:  # Enter
                        if self._current._onwindowmouseover is not None:
                            try:
                                self._current._onwindowmouseover(self._current)
                            except TypeError:
                                self._current._onwindowmouseover()
                            check_widget_mouseleave()
                        self._current._last_update_mode.append(_events.MENU_LAST_MOUSE_ENTER_WINDOW)
                    else:  # Leave
                        if self._current._onwindowmouseleave is not None:
                            try:
                                self._current._onwindowmouseleave(self._current)
                            except TypeError:
                                self._current._onwindowmouseleave()
                        if self._current._mouseover:
                            self._current._mouseover = False
                            if self._current._onmouseleave is not None:
                                try:
                                    self._current._onmouseleave(self._current, event)
                                except TypeError:
                                    self._current._onmouseleave()
                            check_widget_mouseleave(force=True)
                        self._current._last_update_mode.append(_events.MENU_LAST_MOUSE_LEAVE_WINDOW)

                # Mouse motion. It changes the cursor of the mouse if enabled
                elif event.type == pygame.MOUSEMOTION and self._current._mouse:
                    mouse_motion_event = event

                    # Check if mouse over menu
                    if not self._current._mouseover:
                        if self._current.collide(event):
                            self._current._mouseover = True
                            if self._current._onmouseover is not None:
                                try:
                                    self._current._onmouseover(self._current, event)
                                except TypeError:
                                    self._current._onmouseover()
                            self._current._last_update_mode.append(_events.MENU_LAST_MOUSE_ENTER_MENU)

                    else:
                        if not self._current.collide(event):
                            self._current._mouseover = False
                            if self._current._onmouseleave is not None:
                                try:
                                    self._current._onmouseleave(self._current, event)
                                except TypeError:
                                    self._current._onmouseleave()
                            mouse_motion_event = None
                            check_widget_mouseleave(force=True)
                            self._current._last_update_mode.append(_events.MENU_LAST_MOUSE_LEAVE_MENU)

                    # If selected widget is active then motion should not select
                    # or change mouseover widget
                    if self._current._mouse_motion_selection and selected_widget is not None and selected_widget.active:
                        continue

                    # Check if "rel" exists within the event
                    elif not hasattr(event, 'rel'):
                        continue

                    # Select if mouse motion
                    sel = False  # Widget has been selected
                    for index in range(len(self._current._widgets)):
                        widget = self._current._widgets[index]
                        if widget.is_visible() and widget.get_scrollarea().collide(widget, event):
                            if (self._current._mouse_motion_selection and widget.is_selectable
                                and not isinstance(widget, Frame)):
                                sel = self._current._select(index, 1, SELECT_MOUSE_MOTION, True)
                        # noinspection PyProtectedMember
                        widget._check_mouseover(event)
                        if sel:
                            break
                    if sel:
                        self._current._last_update_mode.append(
                            f'{_events.MENU_LAST_WIDGET_SELECT_MOTION}#{self._current.get_selected_widget().get_id()}'
                        )
                        updated = True
                        break

                # Mouse events in selected widget; don't consider the mouse wheel (button 4 & 5)
                elif (event.type == pygame.MOUSEBUTTONUP and self._current._mouse and
                      selected_widget is not None and event.button in (1, 2, 3)):
                    self._current._sound.play_click_mouse()
                    if selected_widget_scrollarea.collide(selected_widget, event):
                        updated = selected_widget.update_menu([event])
                        if updated:
                            self._current._last_update_mode.append(
                                f'{_events.MENU_LAST_SELECTED_WIDGET_BUTTON_UP}#{selected_widget.get_id()}'
                            )
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
                            elif (widget.is_selectable and widget.is_visible() and
                                  widget.get_scrollarea().collide(widget, event)):
                                sel = self._current._select(index, 1, SELECT_TOUCH, True)
                                if not isinstance(widget, Frame):
                                    break
                        if sel:
                            self._current._last_update_mode.append(
                                f'{_events.MENU_LAST_WIDGET_SELECT}#{self._current.get_selected_widget().get_id()}'
                            )
                            updated = True
                            break

                    # If touchscreen motion selection, clicking will disable the
                    # active state only if the user clicked outside the widget
                    else:
                        if selected_widget is not None and selected_widget.active:
                            if not selected_widget_scrollarea.collide(selected_widget, event):
                                selected_widget.active = False
                                selected_widget.render()  # Some widgets need to be rendered
                                self._current._last_update_mode.append(
                                    f'{_events.MENU_LAST_WIDGET_DISABLE_ACTIVE_STATE}#{selected_widget.get_id()}'
                                )
                                updated = True
                                break

                # Touchscreen events in selected widget
                elif event.type == FINGERUP and self._current._touchscreen and selected_widget is not None:
                    self._current._sound.play_click_touch()
                    if selected_widget_scrollarea.collide(selected_widget, event):
                        updated = selected_widget.update_menu([event])
                        if updated:
                            self._current._last_update_mode.append(
                                f'{_events.MENU_LAST_SELECTED_WIDGET_FINGER_UP}#{selected_widget.get_id()}'
                            )
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
                        elif (widget.is_selectable and widget.is_visible() and
                              widget.get_scrollarea().collide(widget, event)):
                            sel = self._current._select(index, 1, SELECT_TOUCH, True)
                            if not isinstance(widget, Frame):
                                break
                    if sel:
                        self._current._last_update_mode.append(
                            f'{_events.MENU_LAST_WIDGET_SELECT_MOTION}#{self._current.get_selected_widget().get_id()}'
                        )
                        updated = True
                        break

        if mouse_motion_event is not None:
            check_widget_mouseleave(event=mouse_motion_event)

        # If cache is enabled, always force a rendering (user may have changed any status)
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
        surface: Optional['pygame.Surface'] = None,
        bgfun: Optional[Union[Callable[['Menu'], Any], CallableNoArgsType]] = None,
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
                bgfun(menu) <or> bgfun()

        Finally, mainloop can be disabled externally if menu.disable() is called.

        kwargs (Optional)
            - ``clear_surface``     (bool) – If ``True`` surface is cleared using ``theme.surface_clear_color``. Default equals to ``True``
            - ``disable_loop``      (bool) – If ``True`` the mainloop only runs once. Use for running draw and update in a single call
            - ``fps_limit``         (int) – Maximum FPS of the loop. Default equals to ``theme.fps``. If ``0`` there's no limit
            - ``wait_for_event``    (bool) – Holds the loop until an event is provided, useful to save CPU power

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.menu.Menu.get_current`,
            for example, ``menu.get_current().mainloop(...)``.

        :param surface: Pygame surface to draw the Menu. If None, the Menu will use the provided ``surface`` from the constructor
        :param bgfun: Background function called on each loop iteration before drawing the Menu
        :param kwargs: Optional keyword arguments
        :return: Self reference **(current)**
        """
        # Unpack kwargs
        clear_surface = kwargs.get('clear_surface', True)
        disable_loop = kwargs.get('disable_loop', False)
        fps_limit = kwargs.get('fps_limit', self._theme.fps)
        wait_for_event = kwargs.get('wait_for_event', False)

        if surface is None:
            surface = self._surface

        assert isinstance(clear_surface, bool)
        assert isinstance(disable_loop, bool)
        assert isinstance(fps_limit, NumberInstance)
        assert isinstance(surface, pygame.Surface)
        assert isinstance(wait_for_event, bool)

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
            assert callable(bgfun), \
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
            if wait_for_event:
                self.update([pygame.event.wait()])
            if (not wait_for_event or pygame.event.peek()) and self.is_enabled():
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

        With ``recursive=True`` it collects also data inside the all sub-menus.

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

        With ``recursive=True``: it collects also data inside the all sub-menus.

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
            for menu in self._submenus.keys():
                # noinspection PyProtectedMember
                data_submenu = menu._get_input_data(recursive=recursive, depth=depth)

                # Check if there is a collision between keys
                data_keys = data.keys()
                sub_data_keys = data_submenu.keys()
                for key in sub_data_keys:
                    if key in data_keys:
                        raise ValueError(f'collision between widget data ID="{key}" at depth={depth}')

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
        assert isinstance(sound, (Sound, type(self._sound), type(None))), \
            'sound must be pygame_menu.Sound type or None'
        if sound is None:
            sound = Sound()
        self._sound = sound
        self._sound._verbose = self._verbose
        for widget in self._widgets:
            widget.set_sound(sound)
        if recursive:
            for menu in self._submenus.keys():
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
        depth: int = self._get_depth()
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
        for w in self._widgets.copy():
            self.remove_widget(w)
        del self._widgets[:]
        del self._submenus
        self._submenus = {}
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
        """
        current = self

        # Update pointers
        menu._top = self._top
        self._top._current = menu._current
        self._top._prev = [self._top._prev, current]

        # Select the first widget (if not remember the selection)
        if not self._current._remember_selection:
            self._current._select(0, 1, SELECT_OPEN, False, update_mouse_position=False)

        # Call event
        if menu._onbeforeopen is not None:
            menu._onbeforeopen(current, menu)

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
                    # noinspection PyUnresolvedReferences
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
        :param dwidget: Direction to search if ``new_index`` widget is non-selectable
        :param select_type: Select type identifier
        :param apply_sound: Apply widget sound if selected
        :param kwargs: Optional keyword arguments
        :return: ``True`` if the widget changed
        """
        self._stats.select += 1
        self._last_selected_type = select_type

        if len(self._widgets) == 0:
            return False

        # This stores +/-1 if the index increases or decreases, used by non-selectable selection
        elif dwidget == 0:
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
        elif not new_widget.is_selectable or not new_widget.is_visible():

            # If it is a frame, select the first selectable object
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
        if (
            select_type in (SELECT_KEY, SELECT_RECURSIVE) and
            self._mouse_motion_selection and
            not self._disable_widget_update_mousepos_mouseselection and
            not new_widget.is_floating() and
            self._mouseover and
            kwargs.get('update_mouse_position', True)
        ):
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
            if self._verbose:
                warn(f'{widget.get_class_id()} scrollarea is None, thus, scroll to widget cannot be performed')
            return self

        # Scroll to rect
        rect = widget.get_rect()
        widget_frame = widget.get_frame()
        widget_border = widget.get_border()[1]

        # Compute margin depending on widget position
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

        # The latter updates to active object
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

    def get_col_rows(self) -> Tuple[int, List[int]]:
        """
        Return the number of columns and rows of the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :return: Tuple of (columns, rows for each column)
        """
        return self._columns, self._rows

    def get_submenus(self, recursive: bool = False) -> Tuple['Menu', ...]:
        """
        Return the Menu submenus as a tuple.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param recursive: If ``True`` return all submenus in a recursive fashion
        :return: Submenus tuple
        """
        assert isinstance(recursive, bool)
        if not recursive:
            return tuple(self._submenus.keys())
        sm = list(self._submenus.keys())
        for m in self._submenus:
            m_sm = m.get_submenus(recursive=recursive)
            for i in m_sm:
                if i not in sm:
                    sm.append(i)
        return tuple(sm)

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

    def get_widget(
        self,
        widget_id: str,
        recursive: bool = False
    ) -> Optional['Widget']:
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
            for menu in self._submenus.keys():
                widget = menu.get_widget(widget_id, recursive)
                if widget:
                    return widget
        return None

    def get_widgets_column(self, col: int) -> Tuple['Widget', ...]:
        """
        Return all the widgets within column which are visible.

        :param col: Column number (start from zero)
        :return: Widget list
        """
        return tuple(self._widget_columns[col])

    def get_widgets(self, ids: Optional[Union[List[str], Tuple[str, ...]]] = None) -> Tuple['Widget', ...]:
        """
        Return the Menu widgets as a tuple.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param ids: Widget id list. If ``None``, return all the widgets, otherwise, return the widgets from that list
        :return: Widgets tuple
        """
        if not ids:
            return tuple(self._widgets)
        widgets = []
        for i in ids:
            widgets.append(self.get_widget(i, recursive=True))
        return tuple(widgets)

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
            for sm in self._submenus.keys():
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
        if menu in self._submenus.keys():
            return True
        elif recursive:
            for sm in self._submenus.keys():
                if sm.in_submenu(menu, recursive):
                    return True
        return False

    def _remove_submenu(
        self,
        menu: 'Menu',
        hook: 'Widget',
        recursive: bool = False
    ) -> bool:
        """
        Removes Menu from submenu if ``menu`` is a submenu of the Menu.

        :param menu: Menu to remove
        :param hook: Widget associated with the menu
        :param recursive: Check recursively
        :return: ``True`` if ``menu`` was removed
        """
        assert isinstance(menu, Menu)
        assert isinstance(hook, Widget)
        if menu in self._submenus.keys():
            # Remove hook if in list
            if hook in self._submenus[menu]:
                self._submenus[menu].remove(hook)
            hook._menu_hook = None
            # If total hooks are empty, remove the menu
            if len(self._submenus[menu]) == 0:
                del self._submenus[menu]
            self._update_after_remove_or_hidden(self._index)
            return True
        elif recursive:
            for sm in self._submenus:
                if sm._remove_submenu(menu, hook, recursive):
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
            return None
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
        elif self._index < 0:
            return None
        try:
            return self._widgets[self._index % len(self._widgets)]
        except (IndexError, ZeroDivisionError):
            pass
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
        Get the status of each widget as a tuple (position, indices, values, etc.).

        :return: Widget status
        """
        self.render()
        data = []
        for w in self._widgets:
            # noinspection PyProtectedMember
            data.append(w._get_status())
        return tuple(data)

    # noinspection PyProtectedMember
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
        depth: int = kwargs.get('depth', 0)

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
                    f'several widgets are selected at the same time, current '
                    f'selected (sorted by index): {selected}, but the following '
                    f'are also selected: {", ".join(invalid_w)}'
                )
            return None

        selected_widget = self.get_selected_widget()

        # Reverse widgets
        if widget is None:
            new_widgets = []
            lw: int = len(self._widgets)
            j_limit: int = -1  # Last position containing non frame
            for i in range(lw):
                j: int = lw - 1 - i
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
                self._update_frames[0]._sort_menu_update_frames()

            if render:
                self._widgets_surface = None
                self._render()

            check_widget_mouseleave()
            return None

        # Asserts
        assert len(self._widgets) >= 2, \
            'menu must contain at least 2 widgets to perform this task'
        try:
            widget_index = self._widgets.index(widget)
        except ValueError:
            raise ValueError(f'{widget.get_class_id()} widget is not on widgets list')
        assert widget in self._widgets, \
            f'{widget.get_class_id()} does not exist on current menu widgets list'
        assert isinstance(index, (Widget, int, type(None)))
        if isinstance(index, Widget):
            assert index in self._widgets, \
                f'{index.get_class_id()} does not exist on current menu widgets list'
            index = self._widgets.index(index)
        elif isinstance(index, int):
            assert 0 <= index < len(self._widgets), \
                f'index {index} must be between 0 and the number of widgets ({len(self._widgets)})'
        elif index is None:
            index = len(self._widgets) - 1
        else:
            raise ValueError('index must be a widget, int, or None')
        assert widget_index != index, \
            f'target index must be different than the current widget index ({index})'

        target_index: int = index
        target_widget = self._widgets[target_index]

        # If target widget is frame, find the latest index
        both_frames: bool = isinstance(target_widget, Frame) and isinstance(widget, Frame)
        check_if_last: bool = both_frames and self._validate_frame_widgetmove and target_index != 0
        if check_if_last:
            w_last = target_widget
            while True:
                target_index = w_last.last_index
                w_last = self._widgets[w_last.last_index]
                target_widget = w_last
                if not (isinstance(w_last, Frame) and w_last.get_indices() != (-1, -1)) or w_last.get_menu() is None:
                    break
        to_last_position: bool = target_index == len(self._widgets) - 1

        if not to_last_position and check_if_last:
            target_index = index
            target_widget = self._widgets[target_index]
            if both_frames and self._validate_frame_widgetmove and not kwargs.get('swap_search', False):
                return self.move_widget_index(target_widget, widget, render=render, swap_search=True, depth=depth + 1)

        # Check both widgets are within frame if widget to move is frame
        if self._validate_frame_widgetmove and not to_last_position and not both_frames:
            assert widget.get_frame() == target_widget.get_frame(), 'both widgets must be within same frame'

        self._widgets.pop(widget_index)
        self._widgets.insert(target_index, widget)

        new_widget_index: int = self._widgets.index(widget)
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
                    elif not to_last_position:
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
        if selected_widget is not None and selected_widget.is_selectable and self._validate_frame_widgetmove:
            self._index = -1
            selected_widget.select(False)
            self._select(self._widgets.index(selected_widget), 1, SELECT_MOVE, False)

        if render:
            self._widgets_surface = None
            self._render()

        if self._validate_frame_widgetmove:
            if isinstance(widget, Frame) or isinstance(target_widget, Frame):
                if isinstance(widget, Frame):
                    widget._sort_menu_update_frames()
                else:
                    target_widget._sort_menu_update_frames()
            check_widget_mouseleave()

        return new_widget_index, target_index

    def _test_print_widgets(self) -> None:
        """
        Test printing widgets order.
        """
        print_menu_widget_structure(self._widgets, self._index)

    def _copy_theme(self) -> None:
        """
        Updates theme reference with a copied one.
        """
        self._theme = self._theme.copy()


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
        self.update = True  # It should be True, as non-active Menus SHOULD NOT receive updates

    @staticmethod
    def throw(throw_runtime: bool, msg: str) -> None:
        """
        Throws an error, if ``throw_runtime=True`` throws a ``RuntimeError``, otherwise
        only a warning.

        :param throw_runtime: If error is raised
        :param msg: Message
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
