# coding=utf-8
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

from uuid import uuid4
import os
import sys
import textwrap
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
from pygame_menu.scrollarea import ScrollArea
from pygame_menu.sound import Sound


class Menu(object):
    """
    Menu object.

    :param height: Height of the Menu (px)
    :type height: int, float
    :param width: Width of the Menu (px)
    :type width: int, float
    :param title: Title of the Menu
    :type title: str
    :param center_content: Auto centers the Menu on the vertical position after a widget is added/deleted
    :type center_content: bool
    :param column_max_width: List/Tuple representing the maximum width of each column in px, ``None`` equals no limit. For example ``column_max_width=500`` (each column width can be 500px max), or ``column_max_width=(400,500)`` (first column 400px, second 500). If ``0`` uses the Menu width. This method does not resize the widgets, only determines the dynamic width of the column layout
    :type column_max_width: int, float, tuple, list, None
    :param column_min_width: List/Tuple representing the minimum width of each column in px. For example ``column_min_width=500`` (each column width is 500px min), or ``column_max_width=(400,500)`` (first column 400px, second 500). Negative values are not accepted
    :type column_min_width: int, float, tuple, list
    :param columns: Number of columns
    :type columns: int
    :param enabled: Menu is enabled
    :type enabled: bool
    :param joystick_enabled: Enable/disable joystick on the Menu
    :type joystick_enabled: bool
    :param menu_id: ID of the Menu
    :type menu_id: str
    :param menu_position: Position in *(x, y)* axis (%) respect to the window size
    :type menu_position: tuple, list
    :param mouse_enabled: Enable/disable mouse click inside the Menu
    :type mouse_enabled: bool
    :param mouse_motion_selection: Select widgets using mouse motion. If ``True`` menu draws a ``focus`` on the selected widget
    :type mouse_motion_selection: bool
    :param mouse_visible: Set mouse visible on Menu
    :type mouse_visible: bool
    :param onclose: Event or function applied when closing the Menu
    :type onclose: :py:class:`pygame_menu.events.MenuAction`, callable, None
    :param overflow: Enables overflow in x/y axes. If ``False`` then scrollbars will not work and the maximum width/height of the scrollarea is the same as the Menu container. Style: *(overflow_x, overflow_y)*
    :type overflow: tuple, list
    :param rows: Number of rows of each column, if there's only 1 column ``None`` can be used for no-limit. Also a tuple can be provided for defining different number of rows for each column, for example ``rows=10`` (each column can have a maximum 10 widgets), or ``rows=[2, 3, 5]`` (first column has 2 widgets, second 3, and third 5)
    :type rows: int, tuple, list, None
    :param screen_dimension: List/Tuple representing the dimensions the Menu should reference for sizing/positioning, if ``None`` pygame is queried for the display mode. This value defines the ``window_size`` of the Menu
    :type screen_dimension: tuple, list, None
    :param theme: Menu theme
    :type theme: :py:class:`pygame_menu.themes.Theme`
    :param touchscreen: Enable/disable touch action inside the Menu. Only available on pygame 2
    :type touchscreen: bool
    :param touchscreen_motion_selection: Select widgets using touchscreen motion. If ``True`` menu draws a ``focus`` on the selected widget
    :type touchscreen_motion_selection: bool
    """

    def __init__(self,
                 height,
                 width,
                 title,
                 center_content=True,
                 column_max_width=None,
                 column_min_width=0,
                 columns=1,
                 enabled=True,
                 joystick_enabled=True,
                 menu_id='',
                 menu_position=(50, 50),
                 mouse_enabled=True,
                 mouse_motion_selection=False,
                 mouse_visible=True,
                 onclose=None,
                 overflow=(True, True),
                 rows=None,
                 screen_dimension=None,
                 theme=_themes.THEME_DEFAULT.copy(),
                 touchscreen=False,
                 touchscreen_motion_selection=False
                 ):
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
        _utils.assert_vector2(menu_position)
        assert width > 0 and height > 0, \
            'menu width and height must be greater than zero'

        # Get window size if not given explicitly
        if screen_dimension is not None:
            _utils.assert_vector2(screen_dimension)
            assert screen_dimension[0] > 0, 'screen width must be higher than zero'
            assert screen_dimension[1] > 0, 'screen height must be higher than zero'
            self._window_size = screen_dimension
        else:
            surface = pygame.display.get_surface()
            if surface is None:
                raise RuntimeError('pygame surface could not be retrieved, check '
                                   'if pygame.display.set_mode() was called')
            self._window_size = surface.get_size()
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
        self._background_function = None  # type: (None, callable)
        self._center_content = center_content
        self._clock = pygame.time.Clock()  # Inner clock
        self._height = float(height)
        self._id = menu_id
        self._index = -1  # Selected index, if -1 the widget does not have been selected yet
        self._onclose = None  # Function or event called on Menu close
        self._sounds = Sound()  # type: Sound
        self._stats = _MenuStats()
        self._submenus = []  # type: list
        self._theme = theme
        self._width = float(width)

        # Set onclose
        self.set_onclose(onclose)

        # Menu links (pointer to previous and next menus in nested submenus), for public methods
        # accessing self should be through "_current", because user can move through submenus
        # and self pointer should target the current Menu object. Private methods access
        # through self (not _current) because these methods are called by public (_current) or
        # by themselves. _top is only used when moving through menus (open,reset)
        self._current = self  # Current Menu

        # Prev stores a list of Menu pointers, when accessing a submenu, prev grows as
        # prev = [prev, new_pointer]
        self._prev = None  # type: (list, None)

        # Top is the same for the menus and submenus if the user moves through them
        self._top = self  # type: Menu

        # Enabled and closed belongs to top, closing a submenu is equal as closing the root
        # Menu
        self._enabled = enabled  # Menu is enabled or not

        # Position of Menu
        self._pos_x = 0  # type: int
        self._pos_y = 0  # type: int
        self.set_relative_position(menu_position[0], menu_position[1])

        # Menu widgets, it should not be accessed outside the object as strange issues can occur
        self._widgets = []  # type: list
        self._widget_offset = [theme.widget_offset[0], theme.widget_offset[1]]  # type: list

        if abs(self._widget_offset[0]) < 1:
            self._widget_offset[0] *= self._width
        if abs(self._widget_offset[1]) < 1:
            self._widget_offset[1] *= self._height

        # Cast to int offset
        self._widget_offset[0] = int(self._widget_offset[0])
        self._widget_offset[1] = int(self._widget_offset[1])

        # If centering is enabled, but widget offset in the vertical is different than zero a warning is raised
        if self._center_content and self._widget_offset[1] != 0:
            msg = 'menu (title "{0}") is vertically centered (center_content=True), but widget offset (from theme) is different than zero ({1}px). Auto-centering has been disabled'
            msg = msg.format(title, self._widget_offset[1])
            warnings.warn(msg)
            self._center_content = False

        # Scrollarea outer margin
        self._scrollarea_margin = [theme.scrollarea_outer_margin[0], theme.scrollarea_outer_margin[1]]
        if abs(self._scrollarea_margin[0]) < 1:
            self._scrollarea_margin[0] *= self._width
        if abs(self._scrollarea_margin[1]) < 1:
            self._scrollarea_margin[1] *= self._height

        # If centering is enabled, but scrollarea margin in the vertical is different than zero a warning is raised
        if self._center_content and self._scrollarea_margin[1] != 0:
            msg = 'menu (title "{0}") is vertically centered (center_content=True), but scrollarea outer margin (from theme) is different than zero ({1}px). Auto-centering has been disabled'
            msg = msg.format(title, round(self._scrollarea_margin[1], 3))
            warnings.warn(msg)
            self._center_content = False

        # Columns and rows
        for i in range(len(column_max_width)):
            if column_max_width[i] == 0:
                column_max_width[i] = width

        self._column_max_width = column_max_width  # type: (tuple, list)
        self._column_min_width = column_min_width  # type: (tuple, list)
        self._column_pos_x = []  # Stores the center x position of each column
        self._column_widths = None  # type: (list, None)
        self._columns = columns  # type: int
        self._max_row_column_elements = 0
        self._rows = rows  # type: (tuple, list)
        self._used_columns = 0  # Total columns used in widget positioning
        self._widget_columns = {}
        self._widget_max_position = (0, 0)
        self._widget_min_position = (0, 0)

        for r in self._rows:
            self._max_row_column_elements += r

        # Init joystick
        self._joystick = joystick_enabled  # type: bool
        if self._joystick:
            if not pygame.joystick.get_init():
                pygame.joystick.init()
            for i in range(pygame.joystick.get_count()):
                pygame.joystick.Joystick(i).init()
        self._joy_event = 0  # type: int
        self._joy_event_down = 8
        self._joy_event_left = 1
        self._joy_event_repeat = pygame.NUMEVENTS - 1
        self._joy_event_right = 2
        self._joy_event_up = 4

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
            back_box=theme.menubar_close_button,
            background_color=self._theme.title_background_color,
            mode=self._theme.title_bar_style,
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
            selected_color=self._theme.title_font_color
        )
        self._menubar.set_shadow(
            color=self._theme.title_shadow_color,
            enabled=self._theme.title_shadow,
            offset=self._theme.title_shadow_offset,
            position=self._theme.title_shadow_position
        )
        self._menubar.set_controls(self._joystick, self._mouse, self._touchscreen)

        # Scrolling area
        self._widgets_surface = None
        menubar_rect = self._menubar.get_rect()
        if self._height - menubar_rect.height <= 0:
            raise ValueError('menubar is higher than menu height. Try increasing the later value')

        self._scroll = ScrollArea(
            area_width=self._width,
            area_color=self._theme.background_color,
            area_height=self._height - menubar_rect.height,
            extend_y=menubar_rect.height,
            scrollbar_color=self._theme.scrollbar_color,
            scrollbar_slider_color=self._theme.scrollbar_slider_color,
            scrollbar_slider_pad=self._theme.scrollbar_slider_pad,
            scrollbar_thick=self._theme.scrollbar_thick,
            shadow=self._theme.scrollbar_shadow,
            shadow_color=self._theme.scrollbar_shadow_color,
            shadow_offset=self._theme.scrollbar_shadow_offset,
            shadow_position=self._theme.scrollbar_shadow_position
        )
        self._scroll.set_menu(self)
        self._overflow = tuple(overflow)

    def set_onclose(self, onclose):
        """
        Set ``onclose`` callback.

        :param onclose: Onclose callback, it can be a function, an event or None
        :type onclose: :py:class:`pygame_menu.events.MenuAction`, callable, None
        :return: None
        """
        assert _utils.is_callable(onclose) or _events.is_event(onclose) or onclose is None, \
            'onclose must be a MenuAction, callable (function-type) or None'
        self._onclose = onclose

    def get_current(self):
        """
        Get **current** active Menu. If the user has not opened any submenu
        the pointer object must be the same as the base. If not, this
        will return the opened Menu pointer.

        :return: Menu object
        :rtype: :py:class:`pygame_menu.Menu`
        """
        return self._current

    @staticmethod
    def _check_kwargs(kwargs):
        """
        Check kwargs after widget addition. It should be empty. Raises ``ValueError``.

        :param kwargs: Kwargs dict
        :type kwargs: dict, any
        :return: None
        """
        for invalid_keyword in kwargs.keys():
            msg = 'widget addition optional parameter kwargs.{} is not valid'.format(invalid_keyword)
            raise ValueError(msg)

    def add_button(self,
                   title,
                   action,
                   *args,
                   **kwargs
                   ):
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
            - ``accept_kwargs``         *(bool)* – Button action accepts ``**kwargs`` if it's a callable object (function-type), ``False`` by default
            - ``align``                 *(str)* - Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_
            - ``back_count``            *(int)* - Number of menus to go back if action is :py:class:`pygame_menu.events.BACK` event, default is ``1``
            - ``background_color``      *(tuple, list,* :py:class:`pygame_menu.baseimage.BaseImage`) - Color of the background
            - ``background_inflate``    *(tuple, list)* - Inflate background in *(x, y)* in px
            - ``button_id``             *(str)* - Widget ID
            - ``font_background_color`` *(tuple, list, None)* - Widget font background color
            - ``font_color``            *(tuple, list)* - Widget font color
            - ``font_name``             *(str)* - Widget font
            - ``font_size``             *(int)* - Font size of the widget
            - ``margin``                *(tuple, list)* - *(left,bottom)* margin in px
            - ``onselect``              *(callable, None)* - Callback executed when selecting the widget
            - ``padding``               *(int, float, tuple, list)* - Widget padding according to CSS rules. General shape: *(top, right, bottom, left)*
            - ``selection_color``       *(tuple, list)* - Color of the selected widget; only affects the font color
            - ``selection_effect``      (:py:class:`pygame_menu.widgets.core.Selection`) - Widget selection effect
            - ``shadow``                *(bool)* - Text shadow is enabled or disabled
            - ``shadow_color``          *(tuple, list)* - Text shadow color
            - ``shadow_position``       *(str)* - Text shadow position, see locals for position
            - ``shadow_offset``         *(int, float)* - Text shadow offset

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
        :type title: str, any
        :param action: Action of the button, can be a Menu, an event, or a function
        :type action: :py:class:`pygame_menu.Menu`, :py:class:`pygame_menu.events.MenuAction`, callable, None
        :param args: Additional arguments used by a function
        :type args: any
        :param kwargs: Optional keyword arguments
        :type kwargs: dict, any
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

        elif action == _events.RESET:  # Back to Top Menu

            widget = _widgets.Button(title, button_id, self.full_reset)

        elif action == _events.CLOSE:  # Close Menu

            widget = _widgets.Button(title, button_id, self._close)

        elif action == _events.EXIT:  # Exit program

            widget = _widgets.Button(title, button_id, self._exit)

        elif action == _events.NONE:  # None action

            widget = _widgets.Button(title, button_id)

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
            self._check_kwargs(kwargs)
        self._configure_widget(widget=widget, **attributes)
        widget.set_selection_callback(onselect)
        self._append_widget(widget)
        self._stats.add_button += 1

        return widget

    def add_color_input(self,
                        title,
                        color_type,
                        color_id='',
                        default='',
                        hex_format='none',
                        input_separator=',',
                        input_underline='_',
                        onchange=None,
                        onreturn=None,
                        onselect=None,
                        previsualization_width=3,
                        **kwargs
                        ):
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
            - ``align``                 *(str)* - Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_
            - ``background_color``      *(tuple, list,* :py:class:`pygame_menu.baseimage.BaseImage`) - Color of the background
            - ``background_inflate``    *(tuple, list)* - Inflate background in *(x, y)* in px
            - ``font_background_color`` *(tuple, list, None)* - Widget font background color
            - ``font_color``            *(tuple, list)* - Widget font color
            - ``font_name``             *(str)* - Widget font
            - ``font_size``             *(int)* - Font size of the widget
            - ``margin``                *(tuple, list)* - *(left,bottom)* margin in px
            - ``padding``               *(int, float, tuple, list)* - Widget padding according to CSS rules. General shape: *(top, right, bottom, left)*
            - ``selection_color``       *(tuple, list)* - Color of the selected widget; only affects the font color
            - ``selection_effect``      (:py:class:`pygame_menu.widgets.core.Selection`) - Widget selection effect
            - ``shadow``                *(bool)* - Text shadow is enabled or disabled
            - ``shadow_color``          *(tuple, list)* - Text shadow color
            - ``shadow_position``       *(str)* - Text shadow position, see locals for position
            - ``shadow_offset``         *(int, float)* - Text shadow offset

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
        :type title: str, any
        :param color_type: Type of the color input, can be ``"rgb"`` or ``"hex"``
        :type color_type: str
        :param color_id: ID of the color input
        :type color_id: str
        :param default: Default value to display, if RGB type it must be a tuple ``(r,g,b)``, if HEX must be a string ``"#XXXXXX"``
        :type default: str, tuple
        :param hex_format: Hex format string mode (none, lower, upper)
        :type hex_format: str
        :param input_separator: Divisor between RGB channels, not valid in HEX format
        :type input_separator: str
        :param input_underline: Underline character
        :type input_underline: str
        :param onchange: Callback executed when changing the values of the color text
        :type onchange: callable, None
        :param onreturn: Callback executed when pressing return on the color text input
        :type onreturn: callable, None
        :param onselect: Callback executed when selecting the widget
        :type onselect: callable, None
        :param previsualization_width: Previsualization width as a factor of the height
        :type previsualization_width: int, float
        :param kwargs: Optional keyword arguments
        :type kwargs: dict, any
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.ColorInput`
        """
        assert isinstance(default, (str, tuple))

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        widget = _widgets.ColorInput(
            color_type=color_type,
            colorinput_id=color_id,
            cursor_color=self._theme.cursor_color,
            hex_format=hex_format,
            input_separator=input_separator,
            input_underline=input_underline,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            prev_size=previsualization_width,
            title=title,
            **kwargs
        )

        self._configure_widget(widget=widget, **attributes)
        widget.set_default_value(default)
        self._append_widget(widget)
        self._stats.add_color_input += 1

        return widget

    def add_image(self,
                  image_path,
                  angle=0,
                  image_id='',
                  onselect=None,
                  scale=(1, 1),
                  scale_smooth=False,
                  selectable=False,
                  **kwargs
                  ):
        """
        Add a simple image to the Menu.

        If ``onselect`` is defined, the callback is executed as follows:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                 *(str)* - Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_
            - ``background_color``      *(tuple, list,* :py:class:`pygame_menu.baseimage.BaseImage`) - Color of the background
            - ``background_inflate``    *(tuple, list)* - Inflate background in *(x, y)* in px
            - ``margin``                *(tuple, list)* - *(left,bottom)* margin in px
            - ``padding``               *(int, float, tuple, list)* - Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``selection_color``       *(tuple, list)* - Color of the selected widget; only affects the font color
            - ``selection_effect``      (:py:class:`pygame_menu.widgets.core.Selection`) - Widget selection effect

        .. note::

            All theme-related optional kwargs use the default Menu theme if not defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param image_path: Path of the image (file) or a BaseImage object. If BaseImage object is provided the angle and scale are ignored
        :type image_path: str, :py:class:`pygame_menu.baseimage.BaseImage`
        :param angle: Angle of the image in degrees (clockwise)
        :type angle: int, float
        :param image_id: ID of the label
        :type image_id: str
        :param onselect: Callback executed when selecting the widget
        :type onselect: callable, None
        :param scale: Scale of the image *(x, y)*
        :type scale: tuple, list
        :param scale_smooth: Scale is smoothed
        :type scale_smooth: bool
        :param selectable: Image accepts user selection
        :type selectable: bool
        :param kwargs: Optional keyword arguments
        :type kwargs: dict, any
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
                  title,
                  label_id='',
                  max_char=0,
                  onselect=None,
                  selectable=False,
                  **kwargs
                  ):
        """
        Add a simple text to the Menu.

        If ``onselect`` is defined, the callback is executed as follows:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                 *(str)* - Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_
            - ``background_color``      *(tuple, list,* :py:class:`pygame_menu.baseimage.BaseImage`) - Color of the background
            - ``background_inflate``    *(tuple, list)* - Inflate background in *(x, y)* in px
            - ``font_background_color`` *(tuple, list, None)* - Widget font background color
            - ``font_color``            *(tuple, list)* - Widget font color
            - ``font_name``             *(str)* - Widget font
            - ``font_size``             *(int)* - Font size of the widget
            - ``margin``                *(tuple, list)* - *(left,bottom)* margin in px
            - ``padding``               *(int, float, tuple, list)* - Widget padding according to CSS rules. General shape: *(top, right, bottom, left)*
            - ``selection_color``       *(tuple, list)* - Color of the selected widget; only affects the font color
            - ``selection_effect``      (:py:class:`pygame_menu.widgets.core.Selection`) - Widget selection effect
            - ``shadow``                *(bool)* - Text shadow is enabled or disabled
            - ``shadow_color``          *(tuple, list)* - Text shadow color
            - ``shadow_position``       *(str)* - Text shadow position, see locals for position
            - ``shadow_offset``         *(int, float)* - Text shadow offset

        .. note::

            All theme-related optional kwargs use the default Menu theme if not defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param title: Text to be displayed
        :type title: str, any
        :param label_id: ID of the label
        :type label_id: str
        :param max_char: Split the title in several labels if length exceeds; ``0``: don't split, ``-1``: split to Menu width
        :type max_char: int
        :param onselect: Callback executed when selecting the widget
        :type onselect: callable, None
        :param selectable: Label accepts user selection, if ``False`` long paragraphs cannot be scrolled through keyboard
        :type selectable: bool
        :param kwargs: Optional keyword arguments
        :type kwargs: dict, any
        :return: Widget object or List of widgets if the text overflows
        :rtype: :py:class:`pygame_menu.widgets.Label`, list[:py:class:`pygame_menu.widgets.Label`]
        """
        assert isinstance(label_id, str)
        assert isinstance(max_char, int)
        assert isinstance(selectable, bool)
        assert max_char >= -1

        title = _utils.to_string(title)
        if len(label_id) == 0:
            label_id = str(uuid4())

        # Wrap text to Menu width (imply additional calls to render functions)
        if max_char < 0:
            dummy_attrs = self._filter_widget_attributes(kwargs.copy())
            dummy = _widgets.Label(title=title)
            self._configure_widget(dummy, **dummy_attrs)
            max_char = int(1.0 * self._width * len(title) / dummy.get_width())

        # If no overflow
        if len(title) <= max_char or max_char == 0:

            attributes = self._filter_widget_attributes(kwargs)
            widget = _widgets.Label(
                title=title,
                label_id=label_id,
                onselect=onselect
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
                     title,
                     items,
                     default=0,
                     onchange=None,
                     onreturn=None,
                     onselect=None,
                     selector_id='',
                     **kwargs
                     ):
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
            - ``align``                 *(str)* - Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_
            - ``background_color``      *(tuple, list,* :py:class:`pygame_menu.baseimage.BaseImage`) - Color of the background
            - ``background_inflate``    *(tuple, list)* - Inflate background in *(x, y)* in px
            - ``font_background_color`` *(tuple, list, None)* - Widget font background color
            - ``font_color``            *(tuple, list)* - Widget font color
            - ``font_name``             *(str)* - Widget font
            - ``font_size``             *(int)* - Font size of the widget
            - ``margin``                *(tuple, list)* - *(left,bottom)* margin in px
            - ``padding``               *(int, float, tuple, list)* - Widget padding according to CSS rules. General shape: *(top, right, bottom, left)*
            - ``selection_color``       *(tuple, list)* - Color of the selected widget; only affects the font color
            - ``selection_effect``      (:py:class:`pygame_menu.widgets.core.Selection`) - Widget selection effect
            - ``shadow``                *(bool)* - Text shadow is enabled or disabled
            - ``shadow_color``          *(tuple, list)* - Text shadow color
            - ``shadow_position``       *(str)* - Text shadow position, see locals for position
            - ``shadow_offset``         *(int, float)* - Text shadow offset

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
        :type title: str, any
        :param items: Elements of the selector ``[('Item1', a, b, c...), ('Item2', d, e, f...)]``
        :type items: list
        :param default: Index of default value to display
        :type default: int
        :param onchange: Callback executed when when changing the selector
        :type onchange: callable, None
        :param onreturn: Callback executed when pressing return button
        :type onreturn: callable, None
        :param onselect: Callback executed when selecting the widget
        :type onselect: callable, None
        :param selector_id: ID of the selector
        :type selector_id: str
        :param kwargs: Optional keyword arguments
        :type kwargs: dict, any
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

    def add_text_input(self,
                       title,
                       default='',
                       copy_paste_enable=True,
                       cursor_selection_enable=True,
                       input_type=_locals.INPUT_TEXT,
                       input_underline='',
                       input_underline_len=0,
                       maxchar=0,
                       maxwidth=0,
                       onchange=None,
                       onreturn=None,
                       onselect=None,
                       password=False,
                       tab_size=4,
                       textinput_id='',
                       valid_chars=None,
                       **kwargs
                       ):
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
            - ``align``                 *(str)* - Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_
            - ``background_color``      *(tuple, list,* :py:class:`pygame_menu.baseimage.BaseImage`) - Color of the background
            - ``background_inflate``    *(tuple, list)* - Inflate background in *(x, y)* in px
            - ``font_background_color`` *(tuple, list, None)* - Widget font background color
            - ``font_color``            *(tuple, list)* - Widget font color
            - ``font_name``             *(str)* - Widget font
            - ``font_size``             *(int)* - Font size of the widget
            - ``margin``                *(tuple, list)* - *(left,bottom)* margin in px
            - ``padding``               *(int, float, tuple, list)* - Widget padding according to CSS rules. General shape: *(top, right, bottom, left)*
            - ``selection_color``       *(tuple, list)* - Color of the selected widget; only affects the font color
            - ``selection_effect``      (:py:class:`pygame_menu.widgets.core.Selection`) - Widget selection effect
            - ``shadow``                *(bool)* - Text shadow is enabled or disabled
            - ``shadow_color``          *(tuple, list)* - Text shadow color
            - ``shadow_position``       *(str)* - Text shadow position, see locals for position
            - ``shadow_offset``         *(int, float)* - Text shadow offset

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
        :type title: str, any
        :param default: Default value to display
        :type default: str, int, float
        :param copy_paste_enable: Enable text copy, paste and cut
        :type copy_paste_enable: bool
        :param cursor_selection_enable: Enable text selection on input
        :type cursor_selection_enable: bool
        :param input_type: Data type of the input
        :type input_type: str
        :param input_underline: Underline character
        :type input_underline: str
        :param input_underline_len: Total of characters to be drawn under the input. If ``0`` this number is computed automatically to fit the font
        :type input_underline_len: int
        :param maxchar: Maximum length of string, if 0 there's no limit
        :type maxchar: int
        :param maxwidth: Maximum size of the text widget (in number of chars), if ``0`` there's no limit
        :type maxwidth: int
        :param onchange: Callback executed when changing the text input
        :type onchange: callable, None
        :param onreturn: Callback executed when pressing return on the text input
        :type onreturn: callable, None
        :param onselect: Callback executed when selecting the widget
        :type onselect: callable, None
        :param password: Text input is a password
        :type password: bool
        :param tab_size: Size of tab key
        :type tab_size: int
        :param textinput_id: ID of the text input
        :type textinput_id: str
        :param valid_chars: List of authorized chars, ``None`` if all chars are valid
        :type valid_chars: list
        :param kwargs: Optional keyword arguments
        :type kwargs: dict, any
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.TextInput`
        """
        assert isinstance(default, (str, int, float))

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        # If password is active no default value should exist
        if password and default != '':
            raise ValueError('default value must be empty if the input is a password')

        widget = _widgets.TextInput(
            copy_paste_enable=copy_paste_enable,
            cursor_color=self._theme.cursor_color,
            cursor_selection_color=self._theme.cursor_selection_color,
            cursor_selection_enable=cursor_selection_enable,
            input_type=input_type,
            input_underline=input_underline,
            input_underline_len=input_underline_len,
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

    def add_vertical_margin(self, margin, margin_id=''):
        """
        Adds a vertical margin to the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param margin: Vertical margin in px
        :type margin: int, float
        :param margin_id: ID of the margin
        :type margin_id: str
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

    def add_none_widget(self, widget_id=''):
        """
        Add none widget to the Menu.

        .. note::

            This widget is usefull to fill column/rows layout without
            compromising any visuals. Also it can be used to store information
            or even to add a ``draw_callback`` function to it for being called
            on each Menu draw.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param widget_id: Widget ID
        :type widget_id: str
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.NoneWidget`
        """
        attributes = self._filter_widget_attributes({})

        widget = _widgets.NoneWidget(widget_id=widget_id)
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)
        self._stats.add_none_widget += 1

        return widget

    def add_generic_widget(self, widget, configure_defaults=False):
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
        :type widget: :py:class:`pygame_menu.widgets.core.widget.Widget`
        :param configure_defaults: Apply defaults widget configuration
        :type configure_defaults: bool
        :return: None
        """
        assert isinstance(widget, _widgets.core.Widget)
        if widget.get_menu() is not None:
            raise ValueError('widget to be added is already appended to another Menu')

        # Raise warning if adding button with Menu
        if isinstance(widget, _widgets.Button) and widget.to_menu:
            msg = 'prefer adding nested submenus using add_button method istead, unintended behaviours may occur'
            warnings.warn(msg)

        # Configure widget
        if configure_defaults:
            self._configure_widget(widget, **self._filter_widget_attributes({}))

        widget.set_menu(self)
        self._check_id_duplicated(widget.get_id())

        widget.set_controls(self._joystick, self._mouse, self._touchscreen)
        self._append_widget(widget)
        self._stats.add_generic_widget += 1

    def _filter_widget_attributes(self, kwargs):
        """
        Return the valid widgets attributes from a dictionary.
        The valid (key, value) are removed from the initial dictionary.

        :param kwargs: Optional keyword arguments (input attributes)
        :type kwargs: dict, any
        :return: Dictionary of valid attributes
        :rtype: dict
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
        _utils.assert_vector2(background_inflate)
        assert background_inflate[0] >= 0 and background_inflate[1] >= 0, \
            'both background inflate components must be equal or greater than zero'
        attributes['background_inflate'] = background_inflate

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
        assert isinstance(font_name, str)
        attributes['font_name'] = font_name

        font_size = kwargs.pop('font_size', self._theme.widget_font_size)
        assert isinstance(font_size, int)
        assert font_size > 0, 'font_size must be greater than zero'
        attributes['font_size'] = font_size

        margin = kwargs.pop('margin', self._theme.widget_margin)
        assert isinstance(margin, tuple)
        assert len(margin) == 2, 'margin must be a tuple or list of 2 numbers'
        attributes['margin'] = margin

        padding = kwargs.pop('padding', self._theme.widget_padding)
        assert isinstance(padding, (int, float, tuple))
        attributes['padding'] = padding

        selection_color = kwargs.pop('selection_color', self._theme.selection_color)
        _utils.assert_color(selection_color)
        attributes['selection_color'] = selection_color

        selection_effect = kwargs.pop('selection_effect', self._theme.widget_selection_effect)
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

    def _configure_widget(self, widget, **kwargs):
        """
        Update the given widget with the parameters defined at
        the Menu level.

        :param widget: Widget object
        :type widget: :py:class:`pygame_menu.widgets.core.widget.Widget`
        :param kwargs: Optional keywords arguments
        :type kwargs: dict, any
        :return: None
        """
        assert isinstance(widget, _widgets.core.Widget)
        assert widget.get_menu() is None, 'widget cannot have an instance of menu'

        widget.set_menu(self)
        self._check_id_duplicated(widget.get_id())

        widget.set_font(
            font=kwargs['font_name'],
            font_size=kwargs['font_size'],
            color=kwargs['font_color'],
            selected_color=kwargs['selection_color'],
            background_color=kwargs['font_background_color'],
            antialias=kwargs['font_antialias']
        )
        widget.set_shadow(
            enabled=kwargs['shadow'],
            color=kwargs['shadow_color'],
            position=kwargs['shadow_position'],
            offset=kwargs['shadow_offset']
        )
        widget.set_controls(
            joystick=self._joystick,
            mouse=self._mouse,
            touchscreen=self._touchscreen
        )
        widget.set_alignment(
            align=kwargs['align']
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
        widget.set_background_color(
            color=kwargs['background_color'],
            inflate=kwargs['background_inflate']
        )

    def _append_widget(self, widget):
        """
        Add a widget to the list of widgets.

        :param widget: Widget object
        :type widget: :py:class:`pygame_menu.widgets.core.widget.Widget`
        :return: None
        """
        assert isinstance(widget, _widgets.core.Widget)
        assert widget.get_menu() == self, 'widget cannot have a different instance of menu'
        self._widgets.append(widget)
        if self._index < 0 and widget.is_selectable:
            widget.set_selected()
            self._index = len(self._widgets) - 1
        self._stats.added_widgets += 1
        self._widgets_surface = None  # If added on execution time forces the update of the surface
        self._render()

    def select_widget(self, widget):
        """
        Select a widget from the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param widget: Widget to be selected
        :type widget: :py:class:`pygame_menu.widgets.core.widget.Widget`
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

    def remove_widget(self, widget):
        """
        Remove the ``widget`` from the Menu. If widget not exists on Menu this
        method raises a ``ValueError`` exception.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param widget: Widget object
        :type widget: :py:class:`pygame_menu.widgets.core.widget.Widget`
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

    def _update_after_remove_or_hidden(self, index, update_surface=True):
        """
        Update widgets after removal or hidden.

        :param index: Removed index, if ``-1`` then select next index, if equal to ``self._index`` select the same
        :type index: int
        :param update_surface: Updates Menu surface
        :type update_surface: bool
        :return: None
        """
        # Check if there's more selectable widgets
        nselect = 0
        last_selectable = 0
        for indx in range(len(self._widgets)):
            wid = self._widgets[indx]  # type: _widgets.core.Widget
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
        self._build_widget_surface()
        if update_surface:
            if self._center_content:
                self.center_content()
            self._widgets_surface = None  # If added on execution time forces the update of the surface

    def _back(self):
        """
        Go to previous Menu or close if top Menu is currently displayed.

        :return: None
        """
        if self._top._prev is not None:
            self.reset(1)
        else:
            self._close()

    def _update_selection_if_hidden(self):
        """
        Updates Menu widget selection if a widget was hidden.

        :return: None
        """
        if len(self._widgets) > 0:
            selected_widget = self._widgets[self._index % len(self._widgets)]  # type: _widgets.core.Widget
            if not selected_widget.visible:
                selected_widget.set_selected(False)  # Unselect
                self._update_after_remove_or_hidden(-1, update_surface=False)

    def _update_widget_position(self):
        """
        Update the position dict for each widget.
        Also sets the column/row of each widget.

        :return: None
        """
        # Store widget rects
        widget_rects = {}
        for widget in self._widgets:  # type: _widgets.core.Widget
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
                row -= self._rows[col]  # Substract the number of rows of such column

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
        self._menubar.set_position(self._pos_x, self._pos_y)

        # Widget max/min position
        max_x = -1e8
        max_y = -1e8
        min_x = 1e8
        min_y = 1e8

        # Update appended widgets
        for index in range(len(self._widgets)):
            widget = self._widgets[index]  # type: _widgets.core.Widget
            rect = widget_rects[widget.get_id()]  # type: pygame.Rect
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
            ysum = 0  # Compute the total height from the current row position to the top of the column
            for rwidget in self._widget_columns[col]:  # type: _widgets.core.Widget
                _, r, _ = rwidget.get_col_row_index()
                if r >= row:
                    break
                if rwidget.visible and not rwidget.floating:
                    ysum += widget_rects[rwidget.get_id()].height  # Height
                    ysum += rwidget.get_margin()[1]  # Vertical margin (bottom)
            y_coord = max(0, self._widget_offset[1]) + ysum + widget.get_padding()[0]

            # If the widget offset is zero, then add the selection effect to the height
            # of the widget to avoid visual glitches
            if self._widget_offset[1] == 0:
                y_coord += selection_effect.get_margin()[0] + 1  # add 1px of linewidth

            # Update the position of the widget
            widget.set_position(int(x_coord), int(y_coord))

            # Update max/min position
            widget_rect = widget.get_rect()
            x, y = widget_rect.bottomright
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            x, y = widget_rect.topleft
            min_x = min(min_x, x)
            min_y = min(min_y, y)

        # Save max/min position
        self._widget_max_position = (max_x, max_y)
        self._widget_min_position = (min_x, min_y)

        self._stats.position_update += 1

    def _build_widget_surface(self):
        """
        Create the surface used to draw widgets according the required width and height.

        :return: None
        """
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
            width, height = self._width - sy, max_y + sy * 0.25
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

        # Adds scrollarea margin
        width += self._scrollarea_margin[0]
        height += self._scrollarea_margin[1]

        self._widgets_surface = _utils.make_surface(width, height)
        self._scroll.set_world(self._widgets_surface)
        self._scroll.set_position(self._pos_x, self._pos_y + menubar_height)
        self._stats.build_surface += 1

    def _check_id_duplicated(self, widget_id):
        """
        Check if widget ID is duplicated. Throws ``IndexError`` if the index is duplicated.

        :param widget_id: New widget ID
        :type widget_id: str
        :return: None
        """
        assert isinstance(widget_id, str)
        for widget in self._widgets:  # type: _widgets.core.Widget
            if widget.get_id() == widget_id:
                raise IndexError('widget ID="{0}" already exists on the menu'.format(widget_id))

    def _close(self):
        """
        Execute close callbacks and disable the Menu.

        :return: ``True`` if Menu has been disabled
        :rtype: bool
        """
        onclose = self._onclose

        # Apply action
        if onclose is None:
            close = False
        else:
            close = True

            # If action is an event
            if _events.is_event(onclose):

                if onclose == _events.DISABLE_CLOSE:
                    close = False
                else:
                    self.disable()  # Closing disables the Menu

                    # Sort through events
                    if onclose == _events.RESET:
                        self.full_reset()
                    elif onclose == _events.BACK:
                        self.reset(1)
                    elif onclose == _events.EXIT:
                        self._exit()

            # If action is callable (function)
            elif _utils.is_callable(onclose):
                onclose()

        return close

    def _get_depth(self):
        """
        Return the Menu depth.

        :return: Menu depth
        :rtype: int
        """
        if self._top is None:
            return 0
        prev = self._top._prev  # type: list
        depth = 0
        while True:
            if prev is not None:
                prev = prev[0]
                depth += 1
            else:
                break
        return depth

    def disable(self):
        """
        Disables the Menu *(doesn't check events and draw on the surface)*.

        :return: None
        """
        self._top._enabled = False

    def set_relative_position(self, position_x, position_y):
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
        :type position_x: int, float
        :param position_y: Top position of the window
        :type position_y: int, float
        :return: None
        """
        assert isinstance(position_x, (int, float))
        assert isinstance(position_y, (int, float))
        assert 0 <= position_x <= 100
        assert 0 <= position_y <= 100

        position_x = float(position_x) / 100
        position_y = float(position_y) / 100
        window_width, window_height = self._window_size
        self._pos_x = (window_width - self._width) * position_x
        self._pos_y = (window_height - self._height) * position_y
        self._widgets_surface = None  # This forces an update of the widgets

    def center_content(self):
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
        if len(self._widgets) == 0:  # If this happen, get_widget_max returns an immense value
            self._widget_offset[1] = 0
            return
        if self._widgets_surface is None:
            self._build_widget_surface()  # For position (max/min)
        available = self.get_height(inner=True)
        widget_height = self.get_height(widget=True)
        new_offset = max(float(available - widget_height) / 2, 0)
        if abs(new_offset - self._widget_offset[1]) > 1:
            self._widget_offset[1] = new_offset
            self._widgets_surface = None  # Rebuild on the next draw
        self._stats.center_content += 1

    def get_height(self, inner=False, widget=False):
        """
        Get menu height.

        :param inner: If ``True`` returns the available height (menu height minus scroll and menubar)
        :type inner: bool
        :param widget: If ``True`` returns the height of the drawn widgets
        :type widget: bool
        :return: Height in px
        :rtype: int, float
        """
        if widget:
            return self._widget_max_position[1] - self._widget_min_position[1]
        if not inner:
            return self._height
        horizontal_scroll = self._scroll.get_scrollbar_thickness(_locals.ORIENTATION_HORIZONTAL)
        return self._height - self._menubar.get_height() - horizontal_scroll

    def render(self):
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

    def _render(self):
        """
        Menu rendering.

        :return: None
        """
        if self._widgets_surface is None:
            if self._center_content:
                self.center_content()
            self._build_widget_surface()
            self._stats.render_private += 1

    def draw(self, surface, clear_surface=False):
        """
        Draw the **current** Menu into the given surface.

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.Menu.get_current`,
            for example, ``menu.get_current().draw(...)``

        :param surface: Pygame surface to draw the Menu
        :type surface: :py:class:`pygame.Surface`
        :param clear_surface: Clear surface using theme default color
        :type clear_surface: bool
        :return: None
        """
        assert isinstance(surface, pygame.Surface)
        assert isinstance(clear_surface, bool)

        if not self.is_enabled():
            raise RuntimeError('menu is not enabled, it cannot be drawn')

        # Render menu
        # print('draw', self._stats.draw)
        self._current._render()

        # Clear surface
        if clear_surface:
            surface.fill(self._theme.surface_clear_color)

        # Call background function (set from mainloop)
        if self._top._background_function is not None:
            self._top._background_function()

        # Fill the scrolling surface
        self._current._widgets_surface.fill((255, 255, 255, 0))

        # Draw widgets
        selected_widget = None
        for widget in self._current._widgets:  # type: _widgets.core.Widget
            if not widget.visible:
                continue
            widget.draw(self._current._widgets_surface)
            if widget.selected:
                widget.draw_selection(self._current._widgets_surface)
                selected_widget = widget

        self._current._scroll.draw(surface)
        self._current._menubar.draw(surface)

        # Draw focus on selected if the widget is active
        self._current._draw_focus_widget(surface, selected_widget)

        self._current._stats.draw += 1

    def _draw_focus_widget(self, surface, widget):
        """
        Draw the focus background from a given widget. Widget must be selectable,
        active, selected. Not all widgets requests the active status, then focus may not
        be drawn.

        :param surface: Pygame surface to draw the Menu
        :type surface: :py:class:`pygame.Surface`
        :param widget: Focused widget
        :type widget: :py:class:`pygame_menu.widgets.core.widget.Widget`, None
        :return: Returns the focus region, None if the focus could not be possible
        :rtype: dict, None
        """
        assert isinstance(surface, pygame.Surface)
        assert isinstance(widget, (_widgets.core.Widget, type(None)))

        if widget is None or not widget.active or not widget.is_selectable or not widget.selected or \
                not (self._mouse_motion_selection or self._touchscreen_motion_selection):
            return
        window_width, window_height = self._window_size

        rect = widget.get_rect()  # type: pygame.Rect

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
            # |  2  |XXXXXX|  3  |
            # |_____|XXXXXX|_____|
            # |        4         |
            # .------------------.
            coords[1] = (0, 0), (window_width, 0), (window_width, y1 - 1), (0, y1 - 1)
            coords[2] = (0, y1), (x1 - 1, y1), (x1 - 1, y2 - 1), (0, y2 - 1)
            coords[3] = (x2, y1), (window_width, y1), (window_width, y2 - 1), (x2, y2 - 1)
            coords[4] = (0, y2), (window_width, y2), (window_width, window_height), (0, window_height)

        for area in coords:
            gfxdraw.filled_polygon(surface, coords[area], self._theme.focus_background_color)
        return coords

    def enable(self):
        """
        Enables Menu (can check events and draw).

        :return: None
        """
        self._top._enabled = True

    def toggle(self):
        """
        Switch between enable/disable Menu.

        :return: None
        """
        self._top._enabled = not self._top._enabled

    def _exit(self):
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
        # This should be unrecheable
        exit(0)

    def is_enabled(self):
        """
        Return ``True`` if the Menu is enabled.

        :return: Menu enabled status
        :rtype: bool
        """
        return self._top._enabled

    def _move_selected_left_right(self, pos):
        """
        Move selected to left/right position (column support).

        :param pos: If ``+1`` selects right column, ``-1`` left column
        :type pos: int
        :return: None
        """
        if not (pos == 1 or pos == -1):
            raise ValueError('pos must be +1 or -1')

        def _default():
            if pos == -1:
                self._select(0, 1)
            else:
                self._select(-1, -1)

        if self._used_columns > 1:

            # Get current widget
            sel_widget = self.get_selected_widget()  # type: _widgets.core.Widget

            # No widget is selected
            if sel_widget is None:
                return _default()

            # Get column row position
            col, row, _ = sel_widget.get_col_row_index()

            # Move column to position
            col = (col + pos) % self._used_columns

            # Get the first similar row in that column, if no widget is found then select the first widget
            for widget in self._widget_columns[col]:  # type: _widgets.core.Widget
                c, r, i = widget.get_col_row_index()
                if r == row:
                    return self._select(i, 1)

            # If no widget is in that column
            if len(self._widget_columns[col]) == 0:
                return _default()

            # If the number of rows in that column is less than current, select the first one
            first_widget = self._widget_columns[col][0]  # type: _widgets.core.Widget
            _, _, i = first_widget.get_col_row_index()
            self._select(i, 1)

        else:
            _default()

    def _handle_joy_event(self):
        """
        Handle joy events.

        :return: None
        """
        if self._joy_event & self._joy_event_up:
            self._select(self._index - 1)
        if self._joy_event & self._joy_event_down:
            self._select(self._index + 1)
        if self._used_columns > 1:
            if self._joy_event & self._joy_event_left:
                self._move_selected_left_right(-1)
            if self._joy_event & self._joy_event_right:
                self._move_selected_left_right(1)

    def update(self, events):
        """
        Update the status of the Menu using external events.
        The update event is applied only on the **current** Menu.

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.Menu.get_current`,
            for example, ``menu.get_current().update(...)``

        :param events: Pygame events as a list
        :type events: list[:py:class:`pygame.event.Event`]
        :return: ``True`` if mainloop must be stopped
        :rtype: bool
        """
        assert isinstance(events, list)

        # If any widget status changes, set the status as True
        updated = False

        # Update mouse
        pygame.mouse.set_visible(self._current._mouse_visible)

        selected_widget = None  # type: (_widgets.core.Widget, None)
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

            for event in events:  # type: pygame.event.Event

                if event.type == _events.PYGAME_QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and (
                        event.mod == pygame.KMOD_LALT or event.mod == pygame.KMOD_RALT)):
                    self._current._exit()
                    updated = True

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
                    elif event.key == _controls.KEY_LEFT:
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
                    elif event.value == _controls.JOY_LEFT and self._used_columns > 1:
                        self._current._select(self._current._index - 1)
                    elif event.value == _controls.JOY_RIGHT and self._used_columns > 1:
                        self._current._select(self._current._index + 1)

                elif self._current._joystick and event.type == pygame.JOYAXISMOTION:
                    prev = self._current._joy_event
                    self._current._joy_event = 0
                    if event.axis == _controls.JOY_AXIS_Y and event.value < -_controls.JOY_DEADZONE:
                        self._current._joy_event |= self._current._joy_event_up
                    if event.axis == _controls.JOY_AXIS_Y and event.value > _controls.JOY_DEADZONE:
                        self._current._joy_event |= self._current._joy_event_down
                    if event.axis == _controls.JOY_AXIS_X and event.value < -_controls.JOY_DEADZONE and self._used_columns > 1:
                        self._current._joy_event |= self._current._joy_event_left
                    if event.axis == _controls.JOY_AXIS_X and event.value > _controls.JOY_DEADZONE and self._used_columns > 1:
                        self._current._joy_event |= self._current._joy_event_right
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
                elif self._current._mouse and event.type == pygame.MOUSEBUTTONDOWN:

                    # If the mouse motion selection is disabled then select a widget by clicking
                    if not self._current._mouse_motion_selection:
                        for index in range(len(self._current._widgets)):
                            widget = self._current._widgets[index]
                            # Don't consider the mouse wheel (button 4 & 5)
                            if event.button in (1, 2, 3) and self._current._scroll.collide(widget, event) and \
                                    widget.is_selectable and widget.visible:
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
                        widget = self._current._widgets[index]  # type: _widgets.core.Widget
                        if self._current._scroll.collide(widget, event) and widget.is_selectable and widget.visible:
                            self._current._select(index)

                # Mouse events in selected widget
                elif self._current._mouse and event.type == pygame.MOUSEBUTTONUP and selected_widget is not None:
                    self._current._sounds.play_click_mouse()
                    # Don't consider the mouse wheel (button 4 & 5)
                    if event.button in (1, 2, 3) and self._current._scroll.collide(selected_widget, event):
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
                            # Don't consider the mouse wheel (button 4 & 5)
                            if self._current._scroll.collide(widget, event) and \
                                    widget.is_selectable and widget.visible:
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
                        widget = self._current._widgets[index]  # type: _widgets.core.Widget
                        if self._current._scroll.collide(widget, event) and widget.is_selectable:
                            self._current._select(index)

                # Touchscreen events in selected widget
                elif self._current._touchscreen and event.type == pygame.FINGERUP and selected_widget is not None:
                    self._current._sounds.play_click_mouse()

                    if self._current._scroll.collide(selected_widget, event):
                        new_event = pygame.event.Event(pygame.MOUSEBUTTONUP, **event.dict)
                        new_event.dict['origin'] = self._current._scroll.to_real_position((0, 0))
                        finger_pos = (event.x * self._window_size[0], event.y * self._window_size[1])
                        new_event.pos = self._current._scroll.to_world_position(finger_pos)
                        selected_widget.update((new_event,))  # This widget can change the current Menu to a submenu
                        updated = True  # It is updated
                        break

        # Check if the Menu widgets size changed, if True, updates the surface
        # forcing the rendering of all widgets
        menu_surface_needs_update = False
        if len(self._current._widgets) > 0:
            for widget in self._current._widgets:  # type: _widgets.core.Widget
                menu_surface_needs_update = menu_surface_needs_update or widget.surface_needs_update()
        if menu_surface_needs_update:
            self._current._widgets_surface = None

        # A widget has closed the Menu
        if not self.is_enabled():
            updated = True

        self._current._stats.update += 1

        return updated

    def mainloop(self, surface, bgfun=None, disable_loop=False, fps_limit=30):
        """
        Main loop of the **current** Menu. In this function, the Menu handle exceptions and draw.
        The Menu pauses the application and checks :py:mod:`pygame` events itself.
        This method returns until the Menu is updated (a widget status has changed).

        The execution of the mainloop is at the current Menu level.

        .. code-block:: python

            menu = pygame_menu.Menu(...)
            menu.mainloop(surface)

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.Menu.get_current`,
            for example, ``menu.get_current().mainloop(...)``

        :param surface: Pygame surface to draw the Menu
        :type surface: :py:class:`pygame.Surface`
        :param bgfun: Background function called on each loop iteration before drawing the Menu
        :type bgfun: callable, None
        :param disable_loop: If ``True`` run this method for only ``1`` loop
        :type disable_loop: bool
        :param fps_limit: Limit frames per second of the loop, if ``0`` there's no limit
        :type fps_limit: int, float
        :return: None
        """
        assert isinstance(surface, pygame.Surface)
        if bgfun:
            assert _utils.is_callable(bgfun), \
                'background function must be callable (function-type) object'
        assert isinstance(disable_loop, bool)
        assert isinstance(fps_limit, (int, float))
        assert fps_limit >= 0, 'fps limit cannot be negative'
        fps_limit = int(fps_limit)

        # NOTE: For Menu accessor, use only _current, as the Menu pointer can change through the execution
        if not self.is_enabled():
            warnings.warn('menu is not enabled, mainloop can\'t continue')
            return

        self._current._background_function = bgfun

        while True:
            self._current._stats.loop += 1
            self._current._clock.tick(fps_limit)

            self.draw(surface=surface, clear_surface=True)

            # If loop, gather events by Menu and draw the background function, if this method
            # returns true then the mainloop will break
            self.update(pygame.event.get())

            if not self.is_enabled() or disable_loop:
                self._current._background_function = None
                return

            # Flip contents to screen
            pygame.display.flip()

    def get_input_data(self, recursive=False):
        """
        Return input data from a Menu. The results are given as a dict object.
        The keys are the ID of each element.

        With ``recursive=True`` it collect also data inside the all sub-menus.

        .. note::

            This is applied only to the base Menu (not the currently displayed),
            for such behaviour apply to :py:meth:`pygame_menu.Menu.get_current` object.

        :param recursive: Look in Menu and sub-menus
        :type recursive: bool
        :return: Input dict e.g.: ``{'id1': value, 'id2': value, ...}``
        :rtype: dict
        """
        assert isinstance(recursive, bool)
        return self._get_input_data(recursive, depth=0)

    def _get_input_data(self, recursive, depth):
        """
        Return input data from a Menu. The results are given as a dict object.
        The keys are the ID of each element.

        With ``recursive=True``: it collect also data inside the all sub-menus.

        :param recursive: Look in Menu and sub-menus
        :type recursive: bool
        :param depth: Depth of the input data
        :type depth: int
        :return: Input dict e.g.: ``{'id1': value, 'id2': value, ...}``
        :rtype: dict
        """
        data = {}
        for widget in self._widgets:  # type: _widgets.core.Widget
            try:
                data[widget.get_id()] = widget.get_value()
            except ValueError:  # Widget does not return data
                pass
        if recursive:
            depth += 1
            for menu in self._submenus:  # type: Menu
                data_submenu = menu._get_input_data(recursive=recursive, depth=depth)

                # Check if there is a collision between keys
                data_keys = data.keys()
                subdata_keys = data_submenu.keys()
                for key in subdata_keys:  # type: str
                    if key in data_keys:
                        msg = 'collision between widget data ID="{0}" at depth={1}'.format(key, depth)
                        raise ValueError(msg)

                # Update data
                data.update(data_submenu)
        return data

    def get_rect(self):
        """
        Return the Menu rect.

        :return: Rect
        :rtype: :py:class:`pygame.Rect`
        """
        return pygame.Rect(int(self._pos_x), int(self._pos_y), int(self._width), int(self._height))

    def set_sound(self, sound, recursive=False):
        """
        Add a sound engine to the Menu. If ``recursive=True``, the sound is
        applied to all submenus.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param sound: Sound object
        :type sound: :py:class:`pygame_menu.sound.Sound`, None
        :param recursive: Set the sound engine to all submenus
        :type recursive: bool
        :return: None
        """
        assert isinstance(sound, (type(self._sounds), type(None))), \
            'sound must be pygame_menu.Sound type or None'
        if sound is None:
            sound = Sound()
        self._sounds = sound
        for widget in self._widgets:  # type: _widgets.core.Widget
            widget.set_sound(sound)
        if recursive:
            for menu in self._submenus:  # type: Menu
                menu.set_sound(sound, recursive=True)

    def get_title(self):
        """
        Return the title of the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: Menu title
        :rtype: str
        """
        return self._menubar.get_title()

    def set_title(self, title, offset=None):
        """
        Set the title of the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param title: New menu title
        :type title: str, any
        :param offset: If ``None`` uses theme offset, else it defines the title offset in *(x, y)*
        :type offset: None, tuple, list
        :return: None
        """
        if offset is None:
            offset = self._theme.title_offset
        else:
            _utils.assert_vector2(offset)
        self._menubar.set_title(title, offsetx=offset[0], offsety=offset[1])

    def full_reset(self):
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

    def clear(self):
        """
        Full reset and clears all widgets.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: None
        """
        self.full_reset()
        del self._widgets[:]
        del self._submenus[:]
        self._index = 0
        self._stats.clear += 1

    def _open(self, menu):
        """
        Open the given Menu.

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.Menu.get_current`,
            for example, ``menu.get_current().reset(...)``

        :param menu: Menu object
        :type menu: :py:class:`pygame_menu.Menu`
        :return: None
        """
        current = self

        # Update pointers
        menu._top = self._top
        self._top._current = menu._current
        self._top._prev = [self._top._prev, current]

        # Select the first widget
        self._select(0, 1)

    def reset(self, total):
        """
        Go back in Menu history a certain number of times from the **current** Menu.
        This method operates through the **current** Menu pointer.

        .. warning::

            This method should not be used along :py:meth:`pygame_menu.Menu.get_current`,
            for example, ``menu.get_current().reset(...)``

        :param total: How many menus to go back
        :type total: int
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

        self._current._select(self._top._current._index)
        self._current._stats.reset += 1

    def _select(self, new_index, dwidget=0):
        """
        Select the widget at the given index and unselect others. Selection forces
        rendering of the widget. Also play widget selection sound.

        :param new_index: Widget index
        :type new_index: int
        :param dwidget: Direction to search if ``new_index`` widget is non selectable
        :type dwidget: int
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
            for i in range(total_curr_widgets):  # Unselect all posible candidates
                curr_widget._widgets[i].set_selected(False)
            curr_widget._index = 0

        old_widget = curr_widget._widgets[curr_widget._index]  # type: _widgets.core.Widget
        new_widget = curr_widget._widgets[new_index]  # type:_widgets.core.Widget

        # If new widget is not selectable or visible
        if not new_widget.is_selectable or not new_widget.visible:
            if curr_widget._index >= 0:  # There's at least 1 selectable option (if only text this would be false)
                curr_widget._select(new_index + dwidget, dwidget)
                return
            else:  # No selectable options, quit
                return

        # Selecting widgets forces rendering
        old_widget.set_selected(False)
        curr_widget._index = new_index  # Update selected index
        new_widget.set_selected()

        # Scroll to rect
        rect = new_widget.get_rect()
        if curr_widget._index == 0:  # Scroll to the top of the Menu
            rect = pygame.Rect(int(rect.x), 0, int(rect.width), int(rect.height))

        # Get scroll thickness
        sx = self._scroll.get_scrollbar_thickness(_locals.ORIENTATION_HORIZONTAL)
        sy = self._scroll.get_scrollbar_thickness(_locals.ORIENTATION_VERTICAL)  # scroll
        col, _, _ = new_widget.get_col_row_index()
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

    def get_id(self):
        """
        Return the ID of the base Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: Menu ID
        :rtype: str
        """
        return self._id

    def get_window_size(self):
        """
        Return the window size (px) as a tuple of *(width, height)*.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: Window size in px
        :rtype: tuple
        """
        w, h = self._window_size
        return w, h

    def get_size(self):
        """
        Return the Menu size (px) as a tuple of *(width, height)*.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: Menu size in px
        :rtype: tuple
        """
        return self._width, self._height

    def get_widgets(self):
        """
        Return the Menu widgets as a tuple.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        .. warning::

            Use with caution.

        :return: Widgets tuple
        :rtype: tuple
        """
        return tuple(self._widgets)

    def get_menubar_widget(self):
        """
        Return menubar widget.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        .. warning::

            Use with caution.

        :return: MenuBar widget
        :rtype: :py:class:`pygame_menu.widgets.MenuBar`
        """
        return self._menubar

    def get_scrollarea(self):
        """
        Return the Menu scrollarea.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        .. warning::

            Use with caution.

        :return: Scrollarea object
        :rtype: :py:class:`pygame_menu.scrollarea.ScrollArea`
        """
        return self._scroll

    def get_widget(self, widget_id, recursive=False):
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
        :type widget_id: str
        :param recursive: Look in Menu and submenus
        :type recursive: bool
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.core.widget.Widget`, None
        """
        assert isinstance(widget_id, str)
        assert isinstance(recursive, bool)
        for widget in self._widgets:  # type: _widgets.core.Widget
            if widget.get_id() == widget_id:
                return widget
        if recursive:
            for menu in self._submenus:  # type: Menu
                widget = menu.get_widget(widget_id, recursive)
                if widget:
                    return widget
        return None

    def reset_value(self, recursive=False):
        """
        Reset all widget values to default.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param recursive: Set value recursively
        :type recursive: bool
        :return: None
        """
        for widget in self._widgets:  # type: _widgets.core.Widget
            widget.reset_value()
        if recursive:
            for sm in self._submenus:  # type: Menu
                sm.reset_value(recursive)

    def in_submenu(self, menu, recursive=False):
        """
        Return ``True`` if ``menu`` is a submenu of the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param menu: Menu to check
        :type menu: Menu
        :param recursive: Check recursively
        :type recursive: bool
        :return: ``True`` if ``menu`` is in the submenus
        :rtype: bool
        """
        if menu in self._submenus:
            return True
        if recursive:
            for sm in self._submenus:  # type: Menu
                if sm.in_submenu(menu, recursive):
                    return True
        return False

    def _remove_submenu(self, menu, recursive=False):
        """
        Removes Menu from submenu if ``menu`` is a submenu of the Menu.

        :param menu: Menu to remove
        :type menu: Menu
        :param recursive: Check recursively
        :type recursive: bool
        :return: ``True`` if ``menu`` was removed
        :rtype: bool
        """
        if menu in self._submenus:
            self._submenus.remove(menu)
            self._update_after_remove_or_hidden(self._index)
            return True
        if recursive:
            for sm in self._submenus:  # type: Menu
                if sm._remove_submenu(menu, recursive):
                    return True
        return False

    def get_theme(self):
        """
        Return the Menu theme.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        .. warning::

            Use with caution.

        :return: Menu theme
        :rtype: :py:class:`pygame_menu.themes.Theme`
        """
        return self._theme

    def get_clock(self):
        """
        Return the pygame Menu timer.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: Pygame clock object
        :rtype: :py:class:`pygame.time.Clock`
        """
        return self._clock

    def get_index(self):
        """
        Get selected widget index from the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: Selected widget index
        :rtype: int
        """
        return self._index

    def get_selected_widget(self):
        """
        Return the selected widget on the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :return: Widget object, None if no widget is selected
        :rtype: :py:class:`pygame_menu.widgets.core.widget.Widget`, None
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

    def set_attribute(self, key, value):
        """
        Set an attribute value.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param key: Key of the attribute
        :type key: str
        :param value: Value of the attribute
        :type value: any
        :return: None
        """
        assert isinstance(key, str)
        self._attributes[key] = value

    def get_attribute(self, key, default=None):
        """
        Get an attribute value.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param key: Key of the attribute
        :type key: str
        :param default: Value if does not exists
        :type default: any
        :return: Attribute data
        :rtype: any
        """
        assert isinstance(key, str)
        if not self.has_attribute(key):
            return default
        return self._attributes[key]

    def has_attribute(self, key):
        """
        Return ``True`` if the widget has the given attribute.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param key: Key of the attribute
        :type key: str
        :return: ``True`` if exists
        :rtype: bool
        """
        assert isinstance(key, str)
        return key in self._attributes.keys()

    def remove_attribute(self, key):
        """
        Removes the given attribute. Throws ``IndexError`` if given key does not exist.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply
            to :py:meth:`pygame_menu.Menu.get_current` object.

        :param key: Key of the attribute
        :type key: str
        :return: None
        """
        if not self.has_attribute(key):
            raise IndexError('attribute "{0}" does not exists on menu'.format(key))
        del self._attributes[key]


class _MenuStats(object):
    """
    Stores menu stats.
    """

    def __init__(self):
        """
        Constructor.
        """

        # Widget addition
        self.add_button = 0
        self.add_color_input = 0
        self.add_generic_widget = 0
        self.add_image = 0
        self.add_label = 0
        self.add_none_widget = 0
        self.add_selector = 0
        self.add_text_input = 0
        self.add_vertical_margin = 0

        # Widget update
        self.added_widgets = 0
        self.removed_widgets = 0

        # Widget position
        self.build_surface = 0
        self.position_update = 0
        self.center_content = 0

        # Render
        self.render_private = 0
        self.render_public = 0

        # Other
        self.clear = 0
        self.draw = 0
        self.loop = 0
        self.reset = 0
        self.select = 0
        self.update = 0
