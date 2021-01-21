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

from pathlib import Path
from uuid import uuid4
import os
import sys
import textwrap
import time
import warnings

import pygame
import pygame.gfxdraw as gfxdraw
import pygame_menu.baseimage as _baseimage
import pygame_menu.controls as _controls
import pygame_menu.events as _events
import pygame_menu.locals as _locals
import pygame_menu.themes as _themes
import pygame_menu.utils as _utils
import pygame_menu.widgets as _widgets
from pygame_menu.decorator import Decorator
from pygame_menu.scrollarea import ScrollArea, get_scrollbars_from_position
from pygame_menu.sound import Sound

from pygame_menu.widgets.widget.colorinput import ColorInputColorType, ColorInputHexFormatType
from pygame_menu.widgets.widget.textinput import TextInputModeType
from pygame_menu.custom_types import Callable, Any, Dict, NumberType, VectorType, Vector2NumberType, \
    Union, Tuple, List, Vector2IntType, Vector2BoolType, Tuple4Tuple2IntType, Literal, \
    MenuColumnMaxWidthType, MenuColumnMinWidthType, MenuRowsType, CallbackType, Optional

# Joy events
JOY_EVENT_LEFT = 1
JOY_EVENT_RIGHT = 2
JOY_EVENT_UP = 4
JOY_EVENT_DOWN = 8


class Menu(object):
    """
    Menu object.

    If menu is closed or reset, the callbacks ``onclose`` and ``onreset`` are fired
    (if them are callable-type). They can only receive 1 argument maximum, if so,
    the Menu instance is provided

    .. code-block:: python

        onclose() <or> onclose(Menu)
        onreset() <or> onreset(Menu)

    .. note::

        Menu cannot be copied or deepcopied.

    :param height: Height of the Menu (px)
    :param width: Width of the Menu (px)
    :param title: Title of the Menu
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
    :param overflow: Enables overflow in x/y axes. If ``False`` then scrollbars will not work and the maximum width/height of the scrollarea is the same as the Menu container. Style: *(overflow_x, overflow_y)*
    :param rows: Number of rows of each column, if there's only 1 column ``None`` can be used for no-limit. Also a tuple can be provided for defining different number of rows for each column, for example ``rows=10`` (each column can have a maximum 10 widgets), or ``rows=[2, 3, 5]`` (first column has 2 widgets, second 3, and third 5)
    :param screen_dimension: List/Tuple representing the dimensions the Menu should reference for sizing/positioning, if ``None`` pygame is queried for the display mode. This value defines the ``window_size`` of the Menu
    :param theme: Menu theme
    :param touchscreen: Enable/disable touch action inside the Menu. Only available on pygame 2
    :param touchscreen_motion_selection: Select widgets using touchscreen motion. If ``True`` menu draws a ``focus`` on the selected widget
    """
    _attributes: Dict[str, Any]
    _auto_centering: bool
    _background_function: Optional[Union[Callable[['Menu'], Any], Callable[[], Any]]]
    _clock: 'pygame.time.Clock'
    _column_max_width: VectorType
    _column_min_width: VectorType
    _column_pos_x: List[NumberType]
    _column_widths: Optional[List[NumberType]]
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
    _onclose: Optional[Union['_events.MenuAction', Callable[[], Any], Callable[['Menu'], Any]]]
    _onreset: Optional[Union[Callable[[], Any], Callable[['Menu'], Any]]]
    _overflow: Tuple[bool, bool]
    _position: Tuple[int, int]
    _prev: Optional[List[Union['Menu', List['Menu']]]]
    _runtime_errors: '_MenuRuntimeErrorConfig'
    _scroll: 'ScrollArea'
    _scrollarea_margin: List[int]
    _sounds: 'Sound'
    _stats: '_MenuStats'
    _submenus: List['Menu']
    _theme: '_themes.Theme'
    _top: 'Menu'
    _touchscreen: bool
    _touchscreen_motion_selection: bool
    _used_columns: int
    _widget_columns: Dict[int, List['_widgets.core.Widget']]
    _widget_max_position: Tuple[int, int]
    _widget_min_position: Tuple[int, int]
    _widget_offset: List[int]
    _widget_surface_cache_enabled: bool
    _widget_surface_cache_need_update: bool
    _widgets: List['_widgets.core.Widget']
    _widgets_surface: Optional['pygame.Surface']
    _widgets_surface_last: Tuple[int, int, Optional['pygame.Surface']]
    _widgets_surface_need_update: bool
    _width: int
    _window_size: Tuple[int, int]

    def __init__(self,
                 height: NumberType,
                 width: NumberType,
                 title: str,
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
                 onclose: Optional[Union['_events.MenuAction', Callable[[], Any], Callable[['Menu'], Any]]] = None,
                 onreset: Optional[Union[Callable[[], Any], Callable[['Menu'], Any]]] = None,
                 overflow: Vector2BoolType = (True, True),
                 rows: MenuRowsType = None,
                 screen_dimension: Optional[Vector2IntType] = None,
                 theme: '_themes.Theme' = _themes.THEME_DEFAULT.copy(),
                 touchscreen: bool = False,
                 touchscreen_motion_selection: bool = False
                 ) -> None:
        assert isinstance(height, (int, float))
        assert isinstance(width, (int, float))
        # assert isinstance(title, str)

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
        self._background_function = None
        self._auto_centering = center_content
        self._clock = pygame.time.Clock()
        self._decorator = Decorator(self)
        self._height = int(height)
        self._id = menu_id
        self._index = -1  # Selected index, if -1 the widget does not have been selected yet
        self._onclose = None  # Function or event called on Menu close
        self._sounds = Sound()
        self._stats = _MenuStats()
        self._submenus = []
        self._theme = theme
        self._width = int(width)

        # Set callbacks
        self.set_onclose(onclose)
        self.set_onreset(onreset)

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

        # Enabled and closed belongs to top, closing a submenu is equal as closing the root
        # Menu. If the menu is disabled adding widgets don't trigger rendering
        self._enabled = enabled  # Menu is enabled or not

        # Position of Menu
        self._position = (0, 0)
        self.set_relative_position(menu_position[0], menu_position[1])

        # Menu widgets, it should not be accessed outside the object as strange issues can occur
        self._widgets = []
        self._widget_offset = [theme.widget_offset[0], theme.widget_offset[1]]

        if abs(self._widget_offset[0]) < 1:
            self._widget_offset[0] *= self._width
        if abs(self._widget_offset[1]) < 1:
            self._widget_offset[1] *= self._height

        # Cast to int offset
        self._widget_offset[0] = int(self._widget_offset[0])
        self._widget_offset[1] = int(self._widget_offset[1])

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
        self._column_widths = None
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
        self._mouse = mouse_enabled and mouse_visible
        self._mouse_motion_selection = mouse_motion_selection and mouse_visible
        self._mouse_visible = mouse_visible
        self._mouse_visible_default = mouse_visible

        # Init touchscreen
        if touchscreen:
            version_major, _, _ = pygame.version.vernum
            assert version_major >= 2, 'touchscreen is only supported in pygame v2+'
        if touchscreen_motion_selection:
            assert touchscreen, 'touchscreen_motion_selection cannot be enabled if touchscreen is disabled'
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

        # Widget surface
        self._widgets_surface = None
        self._widgets_surface_need_update = False
        self._widgets_surface_last = (0, 0, None)

        # Precache widgets surface draw
        self._widget_surface_cache_enabled = True
        self._widget_surface_cache_need_update = True

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

    def set_onclose(self,
                    onclose: Optional[Union['_events.MenuAction', Callable[[], Any], Callable[['Menu'], Any]]]
                    ) -> None:
        """
        Set ``onclose`` callback.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param onclose: Onclose callback, it can be a function, an event, or None
        :return: None
        """
        assert _utils.is_callable(onclose) or _events.is_event(onclose) or onclose is None, \
            'onclose must be a MenuAction, callable (function-type) or None'
        if onclose == _events.NONE:
            onclose = None
        self._onclose = onclose

    def set_onreset(self,
                    onreset: Optional[Union[Callable[[], Any], Callable[['Menu'], Any]]]
                    ) -> None:
        """
        Set ``onreset`` callback.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param onreset: Onreset callback, it can be a function or None
        :return: None
        """
        assert _utils.is_callable(onreset) or onreset is None, \
            'onreset must be a callable (function-type) or None'
        self._onreset = onreset

    def get_current(self) -> 'Menu':
        """
        Get **current** active Menu. If the user has not opened any submenu
        the pointer object must be the same as the base. If not, this
        will return the opened Menu pointer.

        :return: Menu object
        """
        return self._current

    @staticmethod
    def _check_kwargs(kwargs: Dict) -> None:
        """
        Check kwargs after widget addition. It should be empty. Raises ``ValueError``.

        :param kwargs: Kwargs dict
        :return: None
        """
        for invalid_keyword in kwargs.keys():
            msg = 'widget addition optional parameter kwargs.{} is not valid'.format(invalid_keyword)
            raise ValueError(msg)

    def add_button(self,
                   title: Any,
                   action: Optional[Union['Menu', '_events.MenuAction', Callable, int]],
                   *args,
                   **kwargs
                   ) -> '_widgets.Button':
        """
        Adds a button to the Menu.

        The arguments and unknown keyword arguments are passed to the action, if
        it's a callable object:

        .. code-block:: python

            action(*args)

        If ``accept_kwargs=True`` then the ``**kwargs`` are also unpacked on action call:

        .. code-block:: python

            action(*args, **kwargs)

        If ``onselect`` is defined, the callback is executed as follows:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``accept_kwargs``             *(bool)* – Button action accepts ``**kwargs`` if it's a callable object (function-type), ``False`` by default
            - ``align``                     *(str)* - Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_
            - ``back_count``                *(int)* - Number of menus to go back if action is :py:class:`pygame_menu.events.BACK` event, default is ``1``
            - ``background_color``          *(tuple, list,* :py:class:`pygame_menu.baseimage.BaseImage`) - Color of the background
            - ``background_inflate``        *(tuple, list)* - Inflate background in *(x, y)* in px
            - ``border_color``              *(tuple, list)* - Widget border color
            - ``border_inflate``            *(tuple, list)* - Widget border inflate in *(x, y)* in px
            - ``border_width``              *(int)* - Border width in px. If ``0`` disables the border
            - ``button_id``                 *(str)* - Widget ID
            - ``font_background_color``     *(tuple, list, None)* - Widget font background color
            - ``font_color``                *(tuple, list)* - Widget font color
            - ``font_name``                 *(str, Path)* - Widget font path
            - ``font_size``                 *(int)* - Font size of the widget
            - ``margin``                    *(tuple, list)* - Widget *(left, bottom)* margin in px
            - ``onselect``                  *(callable, None)* - Callback executed when selecting the widget
            - ``padding``                   *(int, float, tuple, list)* - Widget padding according to CSS rules. General shape: *(top, right, bottom, left)*
            - ``readonly_color``            *(tuple, list)* - Color of the widget if readonly mode
            - ``readonly_selected_color``   *(tuple, list)* - Color of the widget if readonly mode and is selected
            - ``selection_color``           *(tuple, list)* - Color of the selected widget; only affects the font color
            - ``selection_effect``          (:py:class:`pygame_menu.widgets.core.Selection`) - Widget selection effect
            - ``shadow``                    *(bool)* - Text shadow is enabled or disabled
            - ``shadow_color``              *(tuple, list)* - Text shadow color
            - ``shadow_position``           *(str)* - Text shadow position, see locals for position
            - ``shadow_offset``             *(int, float)* - Text shadow offset

        .. note::

            All theme-related optional kwargs use the default Menu theme if not defined.

        .. note::

            Using ``action=None`` is the same as using ``action=pygame_menu.events.NONE``.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Title of the button
        :param action: Action of the button, can be a Menu, an event, or a function
        :param args: Additional arguments used by a function
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Button`
        """
        total_back = kwargs.pop('back_count', 1)
        assert isinstance(total_back, int) and 1 <= total_back

        # Get ID
        button_id = kwargs.pop('button_id', '')
        assert isinstance(button_id, str), 'id must be a string'

        # Accept kwargs
        accept_kwargs = kwargs.pop('accept_kwargs', False)
        assert isinstance(accept_kwargs, bool)

        # Onselect callback
        onselect = kwargs.pop('onselect', None)

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        # Change action if certain events
        if action == _events.PYGAME_QUIT or action == _events.PYGAME_WINDOWCLOSE:
            action = _events.EXIT
        elif action is None:
            action = _events.NONE

        # If element is a Menu
        if isinstance(action, Menu):
            # Check for recursive
            if action == self or action.in_submenu(self, recursive=True):
                msg = 'Menu "{0}" is already on submenu structure, recursive menus lead ' \
                      'to unexpected behaviours. For returning to previous menu use ' \
                      'pygame_menu.events.BACK event defining an optional back_count ' \
                      'number of menus to return from, default is 1'.format(action.get_title())
                raise ValueError(msg)

            self._submenus.append(action)
            widget = _widgets.Button(title, button_id, self._open, action)
            widget.to_menu = True

        # If element is a MenuAction
        elif action == _events.BACK:  # Back to Menu
            widget = _widgets.Button(title, button_id, self.reset, total_back)

        elif action == _events.CLOSE:  # Close Menu
            widget = _widgets.Button(title, button_id, self._close)

        elif action == _events.EXIT:  # Exit program
            widget = _widgets.Button(title, button_id, self._exit)

        elif action == _events.NONE:  # None action
            widget = _widgets.Button(title, button_id)

        elif action == _events.RESET:  # Back to Top Menu
            widget = _widgets.Button(title, button_id, self.full_reset)

        # If element is a function or callable
        elif _utils.is_callable(action):
            if not accept_kwargs:
                widget = _widgets.Button(title, button_id, action, *args)
            else:
                widget = _widgets.Button(title, button_id, action, *args, **kwargs)

        else:
            raise ValueError('action must be a Menu, a MenuAction (event), a function (callable), or None')

        # Configure and add the button
        if not accept_kwargs:
            try:
                self._check_kwargs(kwargs)
            except ValueError:
                warnings.warn('button cannot accept kwargs. If you want to use kwargs options set accept_kwargs=True')
                raise
        self._configure_widget(widget=widget, **attributes)
        widget.set_selection_callback(onselect)
        self._append_widget(widget)
        self._stats.add_button += 1

        return widget

    def add_color_input(self,
                        title: Union[str, Any],
                        color_type: ColorInputColorType,
                        color_id: str = '',
                        default: Any = '',
                        hex_format: ColorInputHexFormatType = 'none',
                        input_separator: str = ',',
                        input_underline: str = '_',
                        onchange: CallbackType = None,
                        onreturn: CallbackType = None,
                        onselect: Optional[Callable[[bool, '_widgets.core.Widget', 'Menu'], Any]] = None,
                        **kwargs
                        ) -> '_widgets.ColorInput':
        """
        Add a color widget with RGB or Hex format to the Menu.
        Includes a preview box that renders the given color.

        The callbacks receive the current value and all unknown keyword
        arguments, where ``current_color=widget.get_value()``:

        .. code-block:: python

            onchange(current_color, **kwargs)
            onreturn(current_color, **kwargs)
            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                     *(str)* - Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_
            - ``background_color``          *(tuple, list,* :py:class:`pygame_menu.baseimage.BaseImage`) - Color of the background
            - ``background_inflate``        *(tuple, list)* - Inflate background in *(x, y)* in px
            - ``border_color``              *(tuple, list)* - Widget border color
            - ``border_inflate``            *(tuple, list)* - Widget border inflate in *(x, y)* in px
            - ``border_width``              *(int)* - Border width in px. If ``0`` disables the border
            - ``dynamic_width``             *(int, float)* - If ``True`` the widget width changes if the previsualization color box is active or not
            - ``font_background_color``     *(tuple, list, None)* - Widget font background color
            - ``font_color``                *(tuple, list)* - Widget font color
            - ``font_name``                 *(str, Path)* - Widget font path
            - ``font_size``                 *(int)* - Font size of the widget
            - ``input_underline_vmargin``   *(int)* - Vertical margin of underline (px)
            - ``margin``                    *(tuple, list)* - Widget *(left, bottom)* margin in px
            - ``padding``                   *(int, float, tuple, list)* - Widget padding according to CSS rules. General shape: *(top, right, bottom, left)*
            - ``previsualization_margin``   *(int)* - Previsualization left margin from text input in px. Default is ``0``
            - ``previsualization_width``    *(int, float)* - Previsualization width as a factor of the height. Default is ``3``
            - ``readonly_color``            *(tuple, list)* - Color of the widget if readonly mode
            - ``readonly_selected_color``   *(tuple, list)* - Color of the widget if readonly mode and is selected
            - ``selection_color``           *(tuple, list)* - Color of the selected widget; only affects the font color
            - ``selection_effect``          (:py:class:`pygame_menu.widgets.core.Selection`) - Widget selection effect
            - ``shadow``                    *(bool)* - Text shadow is enabled or disabled
            - ``shadow_color``              *(tuple, list)* - Text shadow color
            - ``shadow_position``           *(str)* - Text shadow position, see locals for position
            - ``shadow_offset``             *(int, float)* - Text shadow offset

        .. note::

            All theme-related optional kwargs use the default Menu theme if not defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Title of the color input
        :param color_type: Type of the color input
        :param color_id: ID of the color input
        :param default: Default value to display, if RGB type it must be a tuple ``(r,g,b)``, if HEX must be a string ``"#XXXXXX"``
        :param hex_format: Hex format string mode
        :param input_separator: Divisor between RGB channels, not valid in HEX format
        :param input_underline: Underline character
        :param onchange: Callback executed when changing the values of the color text
        :param onreturn: Callback executed when pressing return on the color text input
        :param onselect: Callback executed when selecting the widget
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.ColorInput`
        """
        assert isinstance(default, (str, tuple))

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        dynamic_width = kwargs.pop('dynamic_width', True)
        input_underline_vmargin = kwargs.pop('input_underline_vmargin', 0)
        prev_margin = kwargs.pop('previsualization_margin', 10)
        prev_width = kwargs.pop('previsualization_width', 3)

        widget = _widgets.ColorInput(
            color_type=color_type,
            colorinput_id=color_id,
            cursor_color=self._theme.cursor_color,
            cursor_switch_ms=self._theme.cursor_switch_ms,
            dynamic_width=dynamic_width,
            hex_format=hex_format,
            input_separator=input_separator,
            input_underline=input_underline,
            input_underline_vmargin=input_underline_vmargin,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            prev_margin=prev_margin,
            prev_width_factor=prev_width,
            title=title,
            **kwargs
        )

        self._configure_widget(widget=widget, **attributes)
        widget.set_default_value(default)
        self._append_widget(widget)
        self._stats.add_color_input += 1

        return widget

    def add_image(self,
                  image_path: Union[str, 'Path', '_baseimage.BaseImage'],
                  angle: NumberType = 0,
                  image_id: str = '',
                  onselect: Optional[Callable[[bool, '_widgets.core.Widget', 'Menu'], Any]] = None,
                  scale: Vector2NumberType = (1, 1),
                  scale_smooth: bool = True,
                  selectable: bool = False,
                  **kwargs
                  ) -> '_widgets.Image':
        """
        Add a simple image to the Menu.

        If ``onselect`` is defined, the callback is executed as follows:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                     *(str)* - Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_
            - ``background_color``          *(tuple, list,* :py:class:`pygame_menu.baseimage.BaseImage`) - Color of the background
            - ``background_inflate``        *(tuple, list)* - Inflate background in *(x, y)* in px
            - ``border_color``              *(tuple, list)* - Widget border color
            - ``border_inflate``            *(tuple, list)* - Widget border inflate in *(x, y)* in px
            - ``border_width``              *(int)* - Border width in px. If ``0`` disables the border
            - ``margin``                    *(tuple, list)* - Widget *(left, bottom)* margin in px
            - ``padding``                   *(int, float, tuple, list)* - Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``selection_color``           *(tuple, list)* - Color of the selected widget; only affects the font color
            - ``selection_effect``          (:py:class:`pygame_menu.widgets.core.Selection`) - Widget selection effect

        .. note::

            All theme-related optional kwargs use the default Menu theme if not defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param image_path: Path of the image (file) or a BaseImage object. If BaseImage object is provided the angle and scale are ignored
        :param angle: Angle of the image in degrees (clockwise)
        :param image_id: ID of the label
        :param onselect: Callback executed when selecting the widget
        :param scale: Scale of the image *(x, y)*
        :param scale_smooth: Scale is smoothed
        :param selectable: Image accepts user selection
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Image`
        """
        assert isinstance(selectable, bool)

        # Remove invalid keys from kwargs
        for key in ['font_background_color', 'font_color', 'font_name', 'font_size', 'shadow', 'shadow_color',
                    'shadow_position', 'shadow_offset']:
            kwargs.pop(key, None)

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        widget = _widgets.Image(
            angle=angle,
            image_id=image_id,
            image_path=image_path,
            onselect=onselect,
            scale=scale,
            scale_smooth=scale_smooth
        )
        widget.is_selectable = selectable

        self._check_kwargs(kwargs)
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)
        self._stats.add_image += 1

        return widget

    def add_label(self,
                  title: Any,
                  label_id: str = '',
                  max_char: int = 0,
                  onselect: Optional[Callable[[bool, '_widgets.core.Widget', 'Menu'], Any]] = None,
                  selectable: bool = False,
                  **kwargs
                  ) -> Union['_widgets.Label', List['_widgets.Label']]:
        """
        Add a simple text to the Menu.

        If ``onselect`` is defined, the callback is executed as follows:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                     *(str)* - Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_
            - ``background_color``          *(tuple, list,* :py:class:`pygame_menu.baseimage.BaseImage`) - Color of the background
            - ``background_inflate``        *(tuple, list)* - Inflate background in *(x, y)* in px
            - ``border_color``              *(tuple, list)* - Widget border color
            - ``border_inflate``            *(tuple, list)* - Widget border inflate in *(x, y)* in px
            - ``border_width``              *(int)* - Border width in px. If ``0`` disables the border
            - ``font_background_color``     *(tuple, list, None)* - Widget font background color
            - ``font_color``                *(tuple, list)* - Widget font color
            - ``font_name``                 *(str, Path)* - Widget font path
            - ``font_size``                 *(int)* - Font size of the widget
            - ``margin``                    *(tuple, list)* - Widget *(left, bottom)* margin in px
            - ``padding``                   *(int, float, tuple, list)* - Widget padding according to CSS rules. General shape: *(top, right, bottom, left)*
            - ``selection_color``           *(tuple, list)* - Color of the selected widget; only affects the font color
            - ``selection_effect``          (:py:class:`pygame_menu.widgets.core.Selection`) - Widget selection effect
            - ``shadow``                    *(bool)* - Text shadow is enabled or disabled
            - ``shadow_color``              *(tuple, list)* - Text shadow color
            - ``shadow_position``           *(str)* - Text shadow position, see locals for position
            - ``shadow_offset``             *(int, float)* - Text shadow offset

        .. note::

            All theme-related optional kwargs use the default Menu theme if not defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param title: Text to be displayed
        :param label_id: ID of the label
        :param max_char: Split the title in several labels if the string length exceeds ``max_char``; ``0``: don't split, ``-1``: split to Menu width
        :param onselect: Callback executed when selecting the widget
        :param selectable: Label accepts user selection, if ``False`` long paragraphs cannot be scrolled through keyboard
        :param kwargs: Optional keyword arguments
        :return: Widget object, or List of widgets if the text overflows
        :rtype: :py:class:`pygame_menu.widgets.Label`, list[:py:class:`pygame_menu.widgets.Label`]
        """
        assert isinstance(label_id, str)
        assert isinstance(max_char, int)
        assert isinstance(selectable, bool)
        assert max_char >= -1

        title = str(title)
        if len(label_id) == 0:
            label_id = str(uuid4())

        # If newline detected, split in two new lines
        if '\n' in title:
            title = title.split('\n')
            widgets = []
            for t in title:
                wig = self.add_label(
                    title=t,
                    label_id=label_id + '+' + str(len(widgets) + 1),
                    max_char=max_char,
                    onselect=onselect,
                    selectable=selectable,
                    **kwargs
                )
                if isinstance(wig, list):
                    for w in wig:
                        widgets.append(w)
                else:
                    widgets.append(wig)
            return widgets

        # Wrap text to Menu width (imply additional calls to render functions)
        if max_char < 0:
            dummy_attrs = self._filter_widget_attributes(kwargs.copy())
            dummy = _widgets.Label(title=title)
            self._configure_widget(dummy, **dummy_attrs)
            max_char = int(1.0 * self.get_width(inner=True) * len(title) / dummy.get_width())

        # If no overflow
        if len(title) <= max_char or max_char == 0:
            attributes = self._filter_widget_attributes(kwargs)
            widget = _widgets.Label(
                label_id=label_id,
                onselect=onselect,
                title=title
            )
            widget.is_selectable = selectable
            self._check_kwargs(kwargs)
            self._configure_widget(widget=widget, **attributes)
            self._append_widget(widget)
            self._stats.add_label += 1

        else:
            self._check_id_duplicated(label_id)  # Before adding + LEN
            widget = []
            for line in textwrap.wrap(title, max_char):
                widget.append(
                    self.add_label(
                        title=line,
                        label_id=label_id + '+' + str(len(widget) + 1),
                        max_char=max_char,
                        onselect=onselect,
                        selectable=selectable,
                        **kwargs
                    )
                )

        return widget

    def add_selector(self,
                     title: Any,
                     items: Union[List[Tuple[Any, ...]], List[str]],
                     default: int = 0,
                     onchange: CallbackType = None,
                     onreturn: CallbackType = None,
                     onselect: Optional[Callable[[bool, '_widgets.core.Widget', 'Menu'], Any]] = None,
                     selector_id: str = '',
                     **kwargs
                     ) -> '_widgets.Selector':
        """
        Add a selector to the Menu: several items with values and
        two functions that are executed when changing the selector (left/right)
        and pressing return button on the selected item.

        The values of the selector are like:

        .. code-block:: python

            values = [('Item1', a, b, c...), ('Item2', d, e, f...)]

        The callbacks receive the current text, its index in the list,
        the associated arguments, and all unknown keyword arguments, where
        ``selected_value=widget.get_value()`` and ``selected_index=widget.get_index()``:

        .. code-block:: python

            onchange((selected_value, selected_index), a, b, c..., **kwargs)
            onreturn((selected_value, selected_index), a, b, c..., **kwargs)
            onselect(selected, widget, menu)

        For example, if ``selected_index=0`` then ``selected_value=('Item1', a, b, c...)``.

        kwargs (Optional)
            - ``align``                     *(str)* - Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_
            - ``background_color``          *(tuple, list,* :py:class:`pygame_menu.baseimage.BaseImage`) - Color of the background
            - ``background_inflate``        *(tuple, list)* - Inflate background in *(x, y)* in px
            - ``border_color``              *(tuple, list)* - Widget border color
            - ``border_inflate``            *(tuple, list)* - Widget border inflate in *(x, y)* in px
            - ``border_width``              *(int)* - Border width in px. If ``0`` disables the border
            - ``font_background_color``     *(tuple, list, None)* - Widget font background color
            - ``font_color``                *(tuple, list)* - Widget font color
            - ``font_name``                 *(str, Path)* - Widget font path
            - ``font_size``                 *(int)* - Font size of the widget
            - ``margin``                    *(tuple, list)* - Widget *(left, bottom)* margin in px
            - ``padding``                   *(int, float, tuple, list)* - Widget padding according to CSS rules. General shape: *(top, right, bottom, left)*
            - ``readonly_color``            *(tuple, list)* - Color of the widget if readonly mode
            - ``readonly_selected_color``   *(tuple, list)* - Color of the widget if readonly mode and is selected
            - ``selection_color``           *(tuple, list)* - Color of the selected widget; only affects the font color
            - ``selection_effect``          (:py:class:`pygame_menu.widgets.core.Selection`) - Widget selection effect
            - ``shadow``                    *(bool)* - Text shadow is enabled or disabled
            - ``shadow_color``              *(tuple, list)* - Text shadow color
            - ``shadow_position``           *(str)* - Text shadow position, see locals for position
            - ``shadow_offset``             *(int, float)* - Text shadow offset

        .. note::

            All theme-related optional kwargs use the default Menu theme if not defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Title of the selector
        :param items: Elements of the selector ``[('Item1', a, b, c...), ('Item2', d, e, f...)]``
        :param default: Index of default value to display
        :param onchange: Callback executed when when changing the selector
        :param onreturn: Callback executed when pressing return button
        :param onselect: Callback executed when selecting the widget
        :param selector_id: ID of the selector
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Selector`
        """
        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        widget = _widgets.Selector(
            default=default,
            elements=items,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            selector_id=selector_id,
            title=title,
            **kwargs
        )

        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)
        self._stats.add_selector += 1

        return widget

    def add_toggle_switch(self,
                          title: Any,
                          default: Union[int, bool] = 0,
                          onchange: CallbackType = None,
                          toggleswitch_id: str = '',
                          state_text: Tuple[str, ...] = ('Off', 'On'),
                          state_values: Tuple[Any, ...] = (False, True),
                          **kwargs
                          ) -> '_widgets.ToggleSwitch':
        """
        Add a toggle switch to the Menu: It can switch between two states.

        If user changes the status of the callback, ``onchange`` is fired:

        .. code-block:: python

            onchange(current_state_value, **kwargs)

        kwargs (Optional)
            - ``align``                     *(str)* - Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_
            - ``background_color``          *(tuple, list,* :py:class:`pygame_menu.baseimage.BaseImage`) - Color of the background
            - ``background_inflate``        *(tuple, list)* - Inflate background in *(x, y)* in px
            - ``border_color``              *(tuple, list)* - Widget border color
            - ``border_inflate``            *(tuple, list)* - Widget border inflate in *(x, y)* in px
            - ``border_width``              *(int)* - Border width in px. If ``0`` disables the border
            - ``font_background_color``     *(tuple, list, None)* - Widget font background color
            - ``font_color``                *(tuple, list)* - Widget font color
            - ``font_name``                 *(str, Path)* - Widget font path
            - ``font_size``                 *(int)* - Font size of the widget
            - ``infinite``                  *(bool)* - The state can rotate. ``False`` by default
            - ``margin``                    *(tuple, list)* - Widget *(left, bottom)* margin in px
            - ``padding``                   *(int, float, tuple, list)* - Widget padding according to CSS rules. General shape: *(top, right, bottom, left)*
            - ``readonly_color``            *(tuple, list)* - Color of the widget if readonly mode
            - ``readonly_selected_color``   *(tuple, list)* - Color of the widget if readonly mode and is selected
            - ``selection_color``           *(tuple, list)* - Color of the selected widget; only affects the font color
            - ``selection_effect``          (:py:class:`pygame_menu.widgets.core.Selection`) - Widget selection effect
            - ``shadow``                    *(bool)* - Text shadow is enabled or disabled
            - ``shadow_color``              *(tuple, list)* - Text shadow color
            - ``shadow_position``           *(str)* - Text shadow position, see locals for position
            - ``shadow_offset``             *(int, float)* - Text shadow offset
            - ``slider_color``              *(tuple, list)* - Color of the slider
            - ``slider_thickness``          *(int)* - Slider thickness (px)
            - ``state_color``               *(tuple)* - 2-item color tuple for each state
            - ``state_text_font_size``      *(str, None)* - Font size of the state text. If ``None`` uses the widget font size
            - ``state_text_font_color``     *(tuple)* - 2-item color tuple for each font state text color
            - ``switch_border_color``       *(tuple, list)* - Switch border color
            - ``switch_border_width``       *(int)* - Switch border width
            - ``switch_height``             *(int, float)* - Height factor respect to the title font size height
            - ``switch_margin``             *(tuple, list)* - *(x, y)* margin respect to the title of the widget. X is in px, Y is relative to the height of the title
            - ``width``                     *(int, float)* - Width of the switch box (px)

        .. note::

            This method only handles two states. If you need more states (for example 3, or 4),
            prefer using :py:class:`pygame_menu.widgets.ToggleSwitch` and add it as a generic
            widget.

        .. note::

            All theme-related optional kwargs use the default Menu theme if not defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Title of the toggle switch
        :param default: Default state index of the switch; it can be ``0 (False)`` or ``1 (True)``
        :param onchange: Callback executed when when changing the STATE
        :param toggleswitch_id: Widget ID
        :param state_text: Text of each state
        :param state_values: Value of each state of the switch
        :return: :py:class:`pygame_menu.widgets.ToggleSwitch`
        """
        if isinstance(default, (int, bool)):
            assert 0 <= default <= 1, 'default value can be 0 or 1'
        else:
            raise ValueError('invalid value type, default can be 0, False, 1, or True')

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        infinite = kwargs.pop('infinite', False)
        slider_color = kwargs.pop('slider_color', (255, 255, 255))
        slider_thickness = kwargs.pop('slider_thickness', 20)
        state_color = kwargs.pop('state_color', ((178, 178, 178), (117, 185, 54)))
        state_text_font_color = kwargs.pop('state_text_font_color', ((255, 255, 255), (255, 255, 255)))
        state_text_font_size = kwargs.pop('state_text_font_size', None)
        switch_border_color = kwargs.pop('switch_border_color', (40, 40, 40))
        switch_border_width = kwargs.pop('switch_border_width', 1)
        switch_height = kwargs.pop('switch_height', 1.25)
        switch_margin = kwargs.pop('switch_margin', (25, 0))
        width = kwargs.pop('width', 150)

        widget = _widgets.ToggleSwitch(
            default_state=default,
            infinite=infinite,
            onchange=onchange,
            slider_color=slider_color,
            slider_thickness=slider_thickness,
            state_color=state_color,
            state_text=state_text,
            state_text_font_color=state_text_font_color,
            state_text_font_size=state_text_font_size,
            state_values=state_values,
            switch_border_color=switch_border_color,
            switch_border_width=switch_border_width,
            switch_height=switch_height,
            switch_margin=switch_margin,
            title=title,
            state_width=int(width),
            toggleswitch_id=toggleswitch_id,
            **kwargs
        )
        self._configure_widget(widget=widget, **attributes)
        widget.set_default_value(default)
        self._append_widget(widget)
        self._stats.add_toggle_switch += 1

        return widget

    def add_text_input(self,
                       title: Any,
                       default: Union[str, int, float] = '',
                       copy_paste_enable: bool = True,
                       cursor_selection_enable: bool = True,
                       input_type: TextInputModeType = _locals.INPUT_TEXT,
                       input_underline: str = '',
                       input_underline_len: int = 0,
                       maxchar: int = 0,
                       maxwidth: int = 0,
                       onchange: CallbackType = None,
                       onreturn: CallbackType = None,
                       onselect: Optional[Callable[[bool, '_widgets.core.Widget', 'Menu'], Any]] = None,
                       password: bool = False,
                       tab_size: int = 4,
                       textinput_id: str = '',
                       valid_chars: Optional[List[str]] = None,
                       **kwargs
                       ) -> '_widgets.TextInput':
        """
        Add a text input to the Menu: free text area and two functions
        that execute when changing the text and pressing return button
        on the element.

        The callbacks receive the current value and all unknown keyword
        arguments, where ``current_text=widget.get_value``:

        .. code-block:: python

            onchange(current_text, **kwargs)
            onreturn(current_text, **kwargs)
            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                     *(str)* - Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_
            - ``background_color``          *(tuple, list,* :py:class:`pygame_menu.baseimage.BaseImage`) - Color of the background
            - ``background_inflate``        *(tuple, list)* - Inflate background in *(x, y)* in px
            - ``border_color``              *(tuple, list)* - Widget border color
            - ``border_inflate``            *(tuple, list)* - Widget border inflate in *(x, y)* in px
            - ``border_width``              *(int)* - Border width in px. If ``0`` disables the border
            - ``font_background_color``     *(tuple, list, None)* - Widget font background color
            - ``font_color``                *(tuple, list)* - Widget font color
            - ``font_name``                 *(str, Path)* - Widget font path
            - ``font_size``                 *(int)* - Font size of the widget
            - ``input_underline_vmargin``   *(int)* - Vertical margin of underline (px)
            - ``margin``                    *(tuple, list)* - Widget *(left, bottom)* margin in px
            - ``padding``                   *(int, float, tuple, list)* - Widget padding according to CSS rules. General shape: *(top, right, bottom, left)*
            - ``readonly_color``            *(tuple, list)* - Color of the widget if readonly mode
            - ``readonly_selected_color``   *(tuple, list)* - Color of the widget if readonly mode and is selected
            - ``selection_color``           *(tuple, list)* - Color of the selected widget; only affects the font color
            - ``selection_effect``          (:py:class:`pygame_menu.widgets.core.Selection`) - Widget selection effect
            - ``shadow``                    *(bool)* - Text shadow is enabled or disabled
            - ``shadow_color``              *(tuple, list)* - Text shadow color
            - ``shadow_position``           *(str)* - Text shadow position, see locals for position
            - ``shadow_offset``             *(int, float)* - Text shadow offset

        .. note::

            All theme-related optional kwargs use the default Menu theme if not defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Title of the text input
        :param default: Default value to display
        :param copy_paste_enable: Enable text copy, paste and cut
        :param cursor_selection_enable: Enable text selection on input
        :param input_type: Data type of the input
        :param input_underline: Underline character
        :param input_underline_len: Total of characters to be drawn under the input. If ``0`` this number is computed automatically to fit the font
        :param maxchar: Maximum length of string, if 0 there's no limit
        :param maxwidth: Maximum size of the text widget (in number of chars), if ``0`` there's no limit
        :param onchange: Callback executed when changing the text input
        :param onreturn: Callback executed when pressing return on the text input
        :param onselect: Callback executed when selecting the widget
        :param password: Text input is a password
        :param tab_size: Size of tab key
        :param textinput_id: ID of the text input
        :param valid_chars: List of authorized chars. ``None`` if all chars are valid
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.TextInput`
        """
        assert isinstance(default, (str, int, float))

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)
        input_underline_vmargin = kwargs.pop('input_underline_vmargin', 0)

        # If password is active no default value should exist
        if password and default != '':
            raise ValueError('default value must be empty if the input is a password')

        widget = _widgets.TextInput(
            copy_paste_enable=copy_paste_enable,
            cursor_color=self._theme.cursor_color,
            cursor_selection_color=self._theme.cursor_selection_color,
            cursor_selection_enable=cursor_selection_enable,
            cursor_switch_ms=self._theme.cursor_switch_ms,
            input_type=input_type,
            input_underline=input_underline,
            input_underline_len=input_underline_len,
            input_underline_vmargin=input_underline_vmargin,
            maxchar=maxchar,
            maxwidth=maxwidth,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            password=password,
            tab_size=tab_size,
            textinput_id=textinput_id,
            title=title,
            valid_chars=valid_chars,
            **kwargs
        )

        self._configure_widget(widget=widget, **attributes)
        widget.set_default_value(default)
        self._append_widget(widget)
        self._stats.add_text_input += 1

        return widget

    def add_vertical_margin(self,
                            margin: NumberType,
                            margin_id: str = ''
                            ) -> '_widgets.VMargin':
        """
        Adds a vertical margin to the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param margin: Vertical margin in px
        :param margin_id: ID of the margin
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.VMargin`
        """
        assert isinstance(margin, (int, float))
        assert margin > 0, \
            'zero margin is not valid, prefer adding a NoneWidget menu.add_none_widget()'

        attributes = self._filter_widget_attributes({'margin': (0, margin)})
        widget = _widgets.VMargin(widget_id=margin_id)
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)
        self._stats.add_vertical_margin += 1

        return widget

    def add_none_widget(self, widget_id: str = '') -> '_widgets.NoneWidget':
        """
        Add none widget to the Menu.

        .. note::

            This widget is useful to fill column/rows layout without
            compromising any visuals. Also it can be used to store information
            or even to add a ``draw_callback`` function to it for being called
            on each Menu draw.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param widget_id: Widget ID
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.NoneWidget`
        """
        attributes = self._filter_widget_attributes({})

        widget = _widgets.NoneWidget(widget_id=widget_id)
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)
        self._stats.add_none_widget += 1

        return widget

    def add_generic_widget(self, widget: '_widgets.core.Widget', configure_defaults: bool = False) -> None:
        """
        Add generic widget to the Menu.

        .. note::

            The widget should be fully configured by the user: font, padding, etc.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        .. warning::

            Unintended behaviours may happen while using this method, use only with caution.
            Specially while creating nested submenus with buttons.

        :param widget: Widget to be added
        :param configure_defaults: Apply defaults widget configuration (for example, theme)
        :return: None
        """
        assert isinstance(widget, _widgets.core.Widget)
        if widget.get_menu() is not None:
            raise ValueError('widget to be added is already appended to another Menu')

        # Raise warning if adding button with Menu
        if isinstance(widget, _widgets.Button) and widget.to_menu:
            msg = 'prefer adding nested submenus using add_button method instead, unintended behaviours may occur'
            warnings.warn(msg)

        # Configure widget
        if configure_defaults:
            self._configure_widget(widget, **self._filter_widget_attributes({}))

        widget.set_menu(self)
        self._check_id_duplicated(widget.get_id())

        widget.set_controls(self._joystick, self._mouse, self._touchscreen)
        self._append_widget(widget)
        self._stats.add_generic_widget += 1

    def _filter_widget_attributes(self, kwargs: Dict) -> Dict[str, Any]:
        """
        Return the valid widgets attributes from a dictionary.
        The valid (key, value) are removed from the initial dictionary.

        :param kwargs: Optional keyword arguments (input attributes)
        :return: Dictionary of valid attributes
        """
        attributes = {}
        align = kwargs.pop('align', self._theme.widget_alignment)
        assert isinstance(align, str)
        attributes['align'] = align

        background_is_color = False
        background_color = kwargs.pop('background_color', self._theme.widget_background_color)
        if background_color is not None:
            if isinstance(background_color, _baseimage.BaseImage):
                pass
            else:
                _utils.assert_color(background_color)
                background_is_color = True
        attributes['background_color'] = background_color

        background_inflate = kwargs.pop('background_inflate', self._theme.widget_background_inflate)
        _utils.assert_vector(background_inflate, 2)
        assert background_inflate[0] >= 0 and background_inflate[1] >= 0, \
            'both background inflate components must be equal or greater than zero'
        attributes['background_inflate'] = background_inflate

        border_color = kwargs.pop('border_color', self._theme.widget_border_color)
        _utils.assert_color(border_color)
        attributes['border_color'] = border_color

        border_inflate = kwargs.pop('border_inflate', self._theme.widget_border_inflate)
        _utils.assert_vector(border_inflate, 2)
        assert isinstance(border_inflate[0], int) and border_inflate[0] >= 0
        assert isinstance(border_inflate[1], int) and border_inflate[1] >= 0
        attributes['border_inflate'] = border_inflate

        border_width = kwargs.pop('border_width', self._theme.widget_border_width)
        assert isinstance(border_width, int) and border_width >= 0
        attributes['border_width'] = border_width

        attributes['font_antialias'] = self._theme.widget_font_antialias

        font_background_color = kwargs.pop('font_background_color', self._theme.widget_font_background_color)
        if font_background_color is None and \
                self._theme.widget_font_background_color_from_menu and \
                not background_is_color:
            if isinstance(self._theme.background_color, tuple):  # Is color
                _utils.assert_color(self._theme.background_color)
                font_background_color = self._theme.background_color
        attributes['font_background_color'] = font_background_color

        font_color = kwargs.pop('font_color', self._theme.widget_font_color)
        _utils.assert_color(font_color)
        attributes['font_color'] = font_color

        font_name = kwargs.pop('font_name', self._theme.widget_font)
        assert isinstance(font_name, (str, Path))
        attributes['font_name'] = str(font_name)

        font_size = kwargs.pop('font_size', self._theme.widget_font_size)
        assert isinstance(font_size, int)
        assert font_size > 0, 'font size must be greater than zero'
        attributes['font_size'] = font_size

        margin = kwargs.pop('margin', self._theme.widget_margin)
        assert isinstance(margin, tuple)
        assert len(margin) == 2, 'margin must be a tuple or list of 2 numbers'
        attributes['margin'] = margin

        padding = kwargs.pop('padding', self._theme.widget_padding)
        assert isinstance(padding, (int, float, tuple))
        attributes['padding'] = padding

        readonly_color = kwargs.pop('readonly_color', self._theme.readonly_color)
        _utils.assert_color(readonly_color)
        attributes['readonly_color'] = readonly_color

        readonly_selected_color = kwargs.pop('readonly_selected_color', self._theme.readonly_selected_color)
        _utils.assert_color(readonly_selected_color)
        attributes['readonly_selected_color'] = readonly_selected_color

        selection_color = kwargs.pop('selection_color', self._theme.selection_color)
        _utils.assert_color(selection_color)
        attributes['selection_color'] = selection_color

        selection_effect = kwargs.pop('selection_effect', self._theme.widget_selection_effect)
        if selection_effect is None:
            selection_effect = _widgets.NoneSelection()
        assert isinstance(selection_effect, _widgets.core.Selection)
        attributes['selection_effect'] = selection_effect

        shadow = kwargs.pop('shadow', self._theme.widget_shadow)
        assert isinstance(shadow, bool)
        attributes['shadow'] = shadow

        shadow_color = kwargs.pop('shadow_color', self._theme.widget_shadow_color)
        _utils.assert_color(shadow_color)
        attributes['shadow_color'] = shadow_color

        shadow_position = kwargs.pop('shadow_position', self._theme.widget_shadow_position)
        assert isinstance(shadow_position, str)
        attributes['shadow_position'] = shadow_position

        shadow_offset = kwargs.pop('shadow_offset', self._theme.widget_shadow_offset)
        assert isinstance(shadow_offset, (int, float))
        attributes['shadow_offset'] = shadow_offset

        return attributes

    def _configure_widget(self, widget: '_widgets.core.Widget', **kwargs) -> None:
        """
        Update the given widget with the parameters defined at
        the Menu level.

        :param widget: Widget object
        :param kwargs: Optional keywords arguments
        :return: None
        """
        assert isinstance(widget, _widgets.core.Widget)
        assert widget.get_menu() is None, 'widget cannot have an instance of menu'

        widget.set_menu(self)
        self._check_id_duplicated(widget.get_id())

        widget.set_alignment(
            align=kwargs['align']
        )
        widget.set_background_color(
            color=kwargs['background_color'],
            inflate=kwargs['background_inflate']
        )
        widget.set_border(
            width=kwargs['border_width'],
            color=kwargs['border_color'],
            inflate=kwargs['border_inflate']
        )
        widget.set_controls(
            joystick=self._joystick,
            mouse=self._mouse,
            touchscreen=self._touchscreen
        )
        widget.set_font(
            antialias=kwargs['font_antialias'],
            background_color=kwargs['font_background_color'],
            color=kwargs['font_color'],
            font=kwargs['font_name'],
            font_size=kwargs['font_size'],
            readonly_color=kwargs['readonly_color'],
            readonly_selected_color=kwargs['readonly_selected_color'],
            selected_color=kwargs['selection_color']
        )
        widget.set_margin(
            x=kwargs['margin'][0],
            y=kwargs['margin'][1]
        )
        widget.set_padding(
            padding=kwargs['padding']
        )
        widget.set_selection_effect(
            selection=kwargs['selection_effect']
        )
        widget.set_shadow(
            color=kwargs['shadow_color'],
            enabled=kwargs['shadow'],
            offset=kwargs['shadow_offset'],
            position=kwargs['shadow_position']
        )

    def _append_widget(self, widget: '_widgets.core.Widget') -> None:
        """
        Add a widget to the list of widgets.

        :param widget: Widget object
        :return: None
        """
        assert isinstance(widget, _widgets.core.Widget)
        assert widget.get_menu() == self, 'widget cannot have a different instance of menu'
        self._widgets.append(widget)
        if self._index < 0 and widget.is_selectable:
            widget.select()
            self._index = len(self._widgets) - 1
        self._stats.added_widgets += 1
        self._widgets_surface = None  # If added on execution time forces the update of the surface
        self._render()

    def select_widget(self, widget: '_widgets.core.Widget') -> None:
        """
        Select a widget from the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param widget: Widget to be selected
        :return: None
        """
        assert isinstance(widget, _widgets.core.Widget)
        if not widget.is_selectable:
            raise ValueError('widget is not selectable')
        if not widget.visible:
            raise ValueError('widget is not visible')
        try:
            index = self._widgets.index(widget)  # If not exists this raises ValueError
        except ValueError:
            raise ValueError('widget is not in Menu, check if exists on the current '
                             'with menu.get_current().remove_widget(widget)')
        self._select(index)

    def remove_widget(self, widget: '_widgets.core.Widget') -> None:
        """
        Remove the ``widget`` from the Menu. If widget not exists on Menu this
        method raises a ``ValueError`` exception.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param widget: Widget object
        :return: None
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
            if wid.is_selectable and wid.visible:
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
                if not selected_widget.visible:
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
            if not widget.visible:
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

            # If widget is floating don't update the current index
            if not widget.floating:
                i_index += 1

            # If floating, don't contribute to the column width
            if widget.floating:
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
        if 0 < sum_width_columns < self._width:

            # First, scale columns to its maximum
            sum_contrib = []
            for col in range(self._used_columns):
                if self._column_max_width[col] is None:
                    sum_contrib.append(0)
                elif self._column_widths[col] < self._column_max_width[col]:
                    sum_contrib.append(self._column_max_width[col] - self._column_widths[col])
                else:
                    sum_contrib.append(0)

            delta = float(self._width) - sum(sum_contrib) - sum_width_columns
            if delta < 0:  # Scale contrib back
                scale = (float(self._width) - sum_width_columns) / sum(sum_contrib)
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

            delta = float(self._width) - sum_width_columns
            if delta > 0:
                for col in range(self._used_columns):
                    if sum_contrib[col] > 0:
                        self._column_widths[col] += delta * sum_contrib[col] / sum(sum_contrib)

        # Final column width
        total_col_width = float(sum(self._column_widths))
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

            if not widget.visible:
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
                if rwidget.visible and not rwidget.floating:
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

    def disable(self) -> None:
        """
        Disables the Menu *(doesn't check events and draw on the surface)*.

        .. note::

            This method does not fires ``onclose`` callback. Use ``Menu.close()``
            instead.

        :return: None
        """
        self._top._enabled = False

    def set_relative_position(self, position_x: NumberType, position_y: NumberType) -> None:
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
        :return: None
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

    def center_content(self) -> None:
        """
        Centers the content of the Menu vertically. This action rewrites ``widget_offset``.

        .. note::

            If the height of the widgets is greater than the height of the Menu,
            the drawing region will cover all Menu inner surface.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: None
        """
        self._stats.center_content += 1
        if len(self._widgets) == 0:  # If this happen, get_widget_max returns an immense value
            self._widget_offset[1] = 0
            return
        if self._widgets_surface is None:
            self._update_widget_position()  # For position (max/min)
        available = self.get_height(inner=True)
        widget_height = self.get_height(widget=True)
        if widget_height >= available:  # There's nothing to center
            if self._widget_offset[1] != 0:
                self._widgets_surface = None
                self._widget_offset[1] = 0
                return
        new_offset = int(max(float(available - widget_height) / 2, 0))
        if abs(new_offset - self._widget_offset[1]) > 1:
            self._widget_offset[1] = new_offset
            self._widgets_surface = None  # Rebuild on the next draw

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

    def render(self) -> None:
        """
        Force **current** Menu rendering. Useful to force widget update.

        .. note::

            This method should not be called if the Menu is being drawn as
            this method is called by :py:meth:`pygame_menu.Menu.draw`

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.Menu.get_current`,
            for example, ``menu.get_current().render(...)``

        :return: None
        """
        self._current._widgets_surface = None
        self._current._render()
        self._current._stats.render_public += 1

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

    def draw(self, surface: 'pygame.Surface', clear_surface: bool = False) -> None:
        """
        Draw the **current** Menu into the given surface.

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.Menu.get_current`,
            for example, ``menu.get_current().draw(...)``

        :param surface: Pygame surface to draw the Menu
        :param clear_surface: Clear surface using theme default color
        :return: None
        """
        assert isinstance(surface, pygame.Surface)
        assert isinstance(clear_surface, bool)

        if not self.is_enabled():
            return self._current._runtime_errors.throw(self._current._runtime_errors.draw, 'menu is not enabled')

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
        if self._top._background_function is not None:
            try:
                self._top._background_function(self._current)
            except TypeError:
                self._top._background_function()

        # Draw the prev decorator
        self._current._decorator.draw_prev(surface)

        # Draw widgets, update cache if enabled
        if not self._current._widget_surface_cache_enabled or \
                (render or self._current._widget_surface_cache_need_update):

            # Fill the scrolling surface (clear previous state)
            self._current._widgets_surface.fill((255, 255, 255, 0))

            # Iterate through widgets and draw them
            for widget in self._current._widgets:
                if not widget.visible:
                    continue
                widget.draw(self._current._widgets_surface)
                if widget.selected:
                    widget.draw_selection(self._current._widgets_surface)

            self._current._stats.draw_update_cached += 1
            self._current._widget_surface_cache_need_update = False

        self._current._scroll.draw(surface)
        self._current._menubar.draw(surface)

        # Draw focus on selected if the widget is active
        self._current._draw_focus_widget(surface, self._current.get_selected_widget())
        self._current._decorator.draw_post(surface)
        self._current._stats.draw += 1

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

        if widget is None or not widget.active or not widget.is_selectable or not widget.selected or \
                not (self._mouse_motion_selection or self._touchscreen_motion_selection) or not widget.visible:
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

    def enable(self) -> None:
        """
        Enables Menu (can check events and draw).

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: None
        """
        self._top._enabled = True

    def toggle(self) -> None:
        """
        Switch between enable/disable Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: None
        """
        self._top._enabled = not self._top._enabled

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
            if not selected_widget.visible or not selected_widget.is_selectable:
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

            for event in events:

                if event.type == pygame.KEYDOWN:
                    # Check key event is valid
                    if not _utils.check_key_pressed_valid(event):
                        continue

                    if event.key == _controls.KEY_MOVE_DOWN:
                        self._current._select(self._current._index - 1)
                        self._current._sounds.play_key_add()

                    elif event.key == _controls.KEY_MOVE_UP:
                        self._current._select(self._current._index + 1)
                        self._current._sounds.play_key_add()

                    elif event.key == _controls.KEY_LEFT and self._current._used_columns > 1:
                        self._current._move_selected_left_right(-1)
                        self._current._sounds.play_key_add()

                    elif event.key == _controls.KEY_RIGHT and self._current._used_columns > 1:
                        self._current._move_selected_left_right(1)
                        self._current._sounds.play_key_add()

                    elif event.key == _controls.KEY_BACK and self._top._prev is not None:
                        self._current._sounds.play_close_menu()
                        self.reset(1)  # public, do not use _current

                    elif event.key == _controls.KEY_CLOSE_MENU:
                        self._current._sounds.play_close_menu()
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
                            if widget.is_selectable and widget.visible and \
                                    self._current._scroll.collide(widget, event):
                                self._current._select(index)

                    # If mouse motion selection, clicking will disable the active state
                    # only if the user clicked outside the widget
                    else:
                        if not self._current._scroll.collide(selected_widget, event):
                            selected_widget.active = False

                # Select widgets by mouse motion, this is valid only if the current selected widget
                # is not active and the pointed widget is selectable
                elif self._current._mouse_motion_selection and event.type == pygame.MOUSEMOTION and \
                        not selected_widget.active:
                    for index in range(len(self._current._widgets)):
                        widget = self._current._widgets[index]
                        if widget.is_selectable and widget.visible and \
                                self._current._scroll.collide(widget, event):
                            self._current._select(index)

                # Mouse events in selected widget
                elif self._current._mouse and event.type == pygame.MOUSEBUTTONUP and selected_widget is not None and \
                        event.button in (1, 2, 3):  # Don't consider the mouse wheel (button 4 & 5)
                    self._current._sounds.play_click_mouse()

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
                            if widget.is_selectable and widget.visible and \
                                    self._current._scroll.collide(widget, event):
                                self._current._select(index)

                    # If touchscreen motion selection, clicking will disable the active state
                    # only if the user clicked outside the widget
                    else:
                        if not self._current._scroll.collide(selected_widget, event):
                            selected_widget.active = False

                # Select widgets by touchscreen motion, this is valid only if the current selected widget
                # is not active and the pointed widget is selectable
                elif self._current._touchscreen_motion_selection and event.type == pygame.FINGERMOTION and \
                        not selected_widget.active:
                    for index in range(len(self._current._widgets)):
                        widget = self._current._widgets[index]
                        if widget.is_selectable and self._current._scroll.collide(widget, event):
                            self._current._select(index)

                # Touchscreen events in selected widget
                elif self._current._touchscreen and event.type == pygame.FINGERUP and selected_widget is not None:
                    self._current._sounds.play_click_mouse()

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
                 disable_loop: bool = False,
                 fps_limit: int = 30
                 ) -> None:
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

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.Menu.get_current`,
            for example, ``menu.get_current().mainloop(...)``

        :param surface: Pygame surface to draw the Menu
        :param bgfun: Background function called on each loop iteration before drawing the Menu
        :param disable_loop: If ``True`` run this method for only ``1`` loop
        :param fps_limit: Limit frames per second of the loop, if ``0`` there's no limit
        :return: None
        """
        assert isinstance(surface, pygame.Surface)
        if bgfun:
            assert _utils.is_callable(bgfun), \
                'background function must be callable (function-type) object'
        assert isinstance(disable_loop, bool)
        assert isinstance(fps_limit, int)
        assert fps_limit >= 0, 'fps limit cannot be negative'
        fps_limit = int(fps_limit)

        # NOTE: For Menu accessor, use only _current, as the Menu pointer can change through the execution
        if not self.is_enabled():
            return self._current._runtime_errors.throw(self._current._runtime_errors.mainloop, 'menu is not enabled')

        # Store background function and force render
        self._current._background_function = bgfun
        self._current._widgets_surface = None

        while True:
            self._current._stats.loop += 1
            self._current._clock.tick(fps_limit)

            # Draw the menu
            self.draw(surface=surface, clear_surface=True)

            # If loop, gather events by Menu and draw the background function, if this method
            # returns true then the mainloop will break
            self.update(pygame.event.get())

            # Flip contents to screen
            pygame.display.flip()

            # Menu closed or disabled
            if not self.is_enabled() or disable_loop:
                self._current._background_function = None
                return

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

    def set_sound(self, sound: Optional['Sound'], recursive: bool = False) -> None:
        """
        Add a sound engine to the Menu. If ``recursive=True``, the sound is
        applied to all submenus.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param sound: Sound object
        :param recursive: Set the sound engine to all submenus
        :return: None
        """
        assert isinstance(sound, (type(self._sounds), type(None))), \
            'sound must be pygame_menu.Sound type or None'
        if sound is None:
            sound = Sound()
        self._sounds = sound
        for widget in self._widgets:
            widget.set_sound(sound)
        if recursive:
            for menu in self._submenus:
                menu.set_sound(sound, recursive=True)

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

    def set_title(self, title: Any, offset: Optional[Vector2NumberType] = None) -> None:
        """
        Set the title of the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param title: New menu title
        :param offset: If ``None`` uses theme offset, else it defines the title offset in *(x, y)*
        :return: None
        """
        if offset is None:
            offset = self._theme.title_offset
        else:
            _utils.assert_vector(offset, 2)
        self._menubar.set_title(title, offsetx=offset[0], offsety=offset[1])

    def full_reset(self) -> None:
        """
        Reset the Menu back to the first opened Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: None
        """
        depth = self._get_depth()
        if depth > 0:
            self.reset(depth)

    def clear(self, reset: bool = True) -> None:
        """
        Clears all widgets.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param reset: If ``True`` the menu full-resets
        :return: None
        """
        if reset:
            self.full_reset()
        del self._widgets[:]
        del self._submenus[:]
        self._index = -1
        self._stats.clear += 1
        self._render()

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

        # Select the first widget
        self._select(0, 1)

    def reset(self, total: int) -> None:
        """
        Go back in Menu history a certain number of times from the **current** Menu.
        This method operates through the **current** Menu pointer.

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.Menu.get_current`,
            for example, ``menu.get_current().reset(...)``

        :param total: How many menus to go back
        :return: None
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
        if not new_widget.is_selectable or not new_widget.visible:
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
        self._sounds.play_widget_selection()
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

    def get_window_size(self) -> Tuple[int, int]:
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

    def reset_value(self, recursive: bool = False) -> None:
        """
        Reset all widget values to default.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param recursive: Set value recursively
        :return: None
        """
        for widget in self._widgets:
            widget.reset_value()
        if recursive:
            for sm in self._submenus:
                sm.reset_value(recursive)

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

    def set_attribute(self, key: str, value: Any) -> None:
        """
        Set an attribute value.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param key: Key of the attribute
        :param value: Value of the attribute
        :return: None
        """
        assert isinstance(key, str)
        self._attributes[key] = value

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
        Return ``True`` if the widget has the given attribute.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param key: Key of the attribute
        :return: ``True`` if exists
        """
        assert isinstance(key, str)
        return key in self._attributes.keys()

    def remove_attribute(self, key: str) -> None:
        """
        Removes the given attribute. Throws ``IndexError`` if given key does not exist.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param key: Key of the attribute
        :return: None
        """
        if not self.has_attribute(key):
            raise IndexError('attribute "{0}" does not exists on menu'.format(key))
        del self._attributes[key]

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
