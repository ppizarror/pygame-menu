# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

MENU
Menu class.

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
# File constants no. 0

from uuid import uuid4
import sys
import textwrap
import types

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
    :param title: Title of the Menu (main title)
    :type title: str
    :param center_content: Auto centers the menu on the vertical position after a widget is added/deleted
    :type center_content: bool
    :param column_force_fit_text: Force text fitting of widgets if the width exceeds the column max width
    :type column_force_fit_text: bool
    :param column_max_width: List/Tuple representing the max width of each column in px, None equals no limit
    :type column_max_width: tuple, None
    :param columns: Number of columns, by default it's 1
    :type columns: int
    :param enabled: Menu is enabled by default or not
    :type enabled: bool
    :param joystick_enabled: Enable/disable joystick on the Menu
    :type joystick_enabled: bool
    :param menu_id: ID of the Menu
    :type menu_id: str
    :param menu_position: Position in x,y axis (%). Default *(50, 50)*, vertically and horizontally centered
    :type menu_position: tuple, list
    :param mouse_enabled: Enable/disable mouse click inside the Menu
    :type mouse_enabled: bool
    :param mouse_motion_selection: Select widgets using mouse motion
    :type mouse_motion_selection: bool
    :param mouse_visible: Set mouse visible on Menu
    :type mouse_visible: bool
    :param onclose: Function applied when closing the Menu
    :type onclose: callable, None
    :param rows: Number of rows of each column, None if there's only 1 column
    :type rows: int, None
    :param screen_dimension: List/Tuple representing the dimensions the menu should reference for sizing/positioning, if None pygame is queried for the display mode
    :type screen_dimension: tuple, list, None
    :param theme: Menu theme object, if None use the default theme
    :type theme: :py:class:`pygame_menu.themes.Theme`
    :param touchscreen_enabled: Enable/disable touch action inside the Menu
    :type touchscreen_enabled: bool
    :param touchscreen_motion_selection: Select widgets using touchscreen motion
    :type touchscreen_motion_selection: bool
    :param kwargs: Optional keyword arguments
    :type kwargs: dict
    """

    def __init__(self,
                 height,
                 width,
                 title,
                 center_content=True,
                 column_force_fit_text=False,
                 column_max_width=None,
                 columns=1,
                 enabled=True,
                 joystick_enabled=True,
                 menu_id='',
                 menu_position=(50, 50),
                 mouse_enabled=True,
                 mouse_motion_selection=False,
                 mouse_visible=True,
                 onclose=None,
                 rows=None,
                 screen_dimension=None,
                 theme=_themes.THEME_DEFAULT,
                 touchscreen_enabled=False,
                 touchscreen_motion_selection=False,
                 **kwargs
                 ):
        assert isinstance(height, (int, float))
        assert isinstance(width, (int, float))
        # assert isinstance(title, str)

        assert isinstance(center_content, bool)
        assert isinstance(column_force_fit_text, bool)
        assert isinstance(column_max_width, (tuple, type(None), (int, float), list))
        assert isinstance(columns, int)
        assert isinstance(enabled, bool)
        assert isinstance(joystick_enabled, bool)
        assert isinstance(menu_id, str)
        assert isinstance(menu_position, (tuple, list))
        assert isinstance(mouse_enabled, bool)
        assert isinstance(mouse_motion_selection, bool)
        assert isinstance(mouse_visible, bool)
        assert isinstance(rows, (int, type(None)))
        assert isinstance(screen_dimension, (tuple, list, type(None)))
        assert isinstance(theme, _themes.Theme), 'theme bust be an pygame_menu.themes.Theme object instance'
        assert isinstance(touchscreen_enabled, bool)
        assert isinstance(touchscreen_motion_selection, bool)

        # Assert theme
        theme.validate()

        # Assert pygame was initialized
        assert pygame.get_init(), 'pygame is not initialized'

        # Column/row asserts
        assert columns >= 1, 'number of columns must be greater or equal than 1'
        if columns > 1:
            assert rows is not None and rows >= 1, \
                'if columns greater than 1 then rows must be equal or greater than 1'
        else:
            if columns == 1:
                if rows is None:
                    rows = 1e6  # Set rows as a big number
                else:
                    assert rows > 0, \
                        'number of rows must be greater than 1'
        if column_max_width is not None:
            if isinstance(column_max_width, (int, float)):
                assert columns == 1, \
                    'column_max_width can be a single number if there is only 1 column'
                column_max_width = [column_max_width]
            assert len(column_max_width) == columns, \
                'column_max_width length must be the same as the number of columns'
            for i in column_max_width:
                assert isinstance(i, type(None)) or isinstance(i, (int, float)), \
                    'each column max width can be None (no limit) or an integer/float'
                assert i > 0 or i is None, 'each column max width must be greater than zero or None'
        else:
            column_max_width = [None for _ in range(columns)]

        # Element size and position asserts
        _utils.assert_vector2(menu_position)
        assert width > 0 and height > 0, \
            'menu width and height must be greater than zero'

        # Get window size if not given explicitly
        if screen_dimension is not None:
            _utils.assert_vector2(screen_dimension)
            assert screen_dimension[0] > 0, 'screen width has to be higher than zero'
            assert screen_dimension[1] > 0, 'screen height has to be higher than zero'
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

        # Generate ID if empty
        if len(menu_id) == 0:
            menu_id = str(uuid4())

        # General properties of the Menu
        self._auto_center_content = center_content
        self._background_function = None  # type: (None,callable)
        self._clock = pygame.time.Clock()  # Inner clock
        self._height = float(height)
        self._id = menu_id
        self._index = -1  # Selected index, if -1 the widget does not have been selected yet
        self._onclose = onclose  # Function that calls after closing Menu
        self._sounds = Sound()  # type: Sound
        self._submenus = []  # type: list
        self._theme = theme
        self._width = float(width)

        # Menu links (pointer to previous and next menus in nested submenus), for public methods
        # accessing self should be through "_current", because user can move through submenus
        # and self pointer should target the current Menu object. Private methods access
        # through self (not _current) because these methods are called by public (_current) or
        # by themselves. _top is only used when moving through menus (open,reset)
        self._current = self  # Current Menu

        # Prev stores a list of Menu pointers, when accessing a submenu, prev grows as
        # prev = [prev, new_pointer]
        self._prev = None  # type: (list,None)

        # Top is the same for the menus and submenus if the user moves through them
        self._top = self  # type: Menu

        # Enabled and closed belongs to top, closing a submenu is equal as closing the root
        # Menu
        self._enabled = enabled  # Menu is enabled or not

        # Position of Menu
        self._pos_x = 0  # type: int
        self._pos_y = 0  # type: int
        self.set_relative_position(menu_position[0], menu_position[1])

        # Menu widgets
        self._widgets = []  # type: list
        self._widget_offset = [theme.widget_offset[0], theme.widget_offset[1]]  # type: list

        if abs(self._widget_offset[0]) < 1:
            self._widget_offset[0] *= self._width
        if abs(self._widget_offset[1]) < 1:
            self._widget_offset[1] *= self._height

        # Columns and rows
        self._column_max_width = column_max_width
        self._column_pos_x = []
        self._column_widths = None  # type: (list,None)
        self._columns = columns
        self._force_fit_text = column_force_fit_text
        self._rows = rows

        # Init joystick
        self._joystick = joystick_enabled
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
        if touchscreen_enabled:
            version_major, _, _ = pygame.version.vernum
            assert version_major >= 2, 'touchscreen is only supported in pygame v2+'
        self._touchscreen = touchscreen_enabled
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
        self._scroll = ScrollArea(
            area_width=self._width,
            area_color=self._theme.background_color,
            area_height=self._height - self._menubar.get_rect().height,
            extend_y=self._menubar.get_rect().height,
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

        # Upon this, no more kwargs should exist, raise exception if there's more
        for invalid_keyword in kwargs.keys():
            msg = 'menu constructor parameter {} does not exist'.format(invalid_keyword)
            raise ValueError(msg)

    def get_current(self):
        """
        Get current active Menu. If the user has not opened any submenu
        the pointer object must be the same as the base. If not, this
        will return the opened menu pointer.

        :return: Menu object
        :rtype: :py:class:`pygame_menu.Menu`
        """
        return self._current

    def add_button(self,
                   title,
                   action,
                   *args,
                   **kwargs):
        """
        Adds a button to the Menu.

        The arguments and unknown keyword arguments are passed to
        the action::

            action(*args, **kwargs)

        kwargs (Optional):
            - ``align``                 Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_ (str)
            - ``background_color``      Color of the background (tuple, list, :py:class:`pygame_menu.baseimage.BaseImage`)
            - ``background_inflate``    Inflate background color if enabled (bool)
            - ``button_id``             Widget ID (str)
            - ``font_color``            Widget font color (tuple, list)
            - ``font_name``             Widget font (str)
            - ``font_size``             Font size of the widget (int)
            - ``margin``                (x,y) margin in px (tuple, list)
            - ``selection_color``       Widget selection color (tuple, list)
            - ``selection_effect``      Widget selection effect (:py:class:`pygame_menu.widgets.core.Selection`)
            - ``shadow``                Shadow is enabled or disabled (bool)
            - ``shadow_color``          Text shadow color (tuple, list)
            - ``shadow_position``       Text shadow position, see locals for position (str)
            - ``shadow_offset``         Text shadow offset (int, float, None)

        :param title: Title of the button
        :type title: str
        :param action: Action of the button, can be a Menu, an event or a function
        :type action: :py:class:`pygame_menu.Menu`, :py:class:`pygame_menu.events.MenuAction`, callable, None
        :param args: Additional arguments used by a function
        :type args: any
        :param kwargs: Optional keyword arguments
        :type kwargs: dict
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Button`
        """

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        # Get ID
        button_id = kwargs.pop('button_id', '')
        assert isinstance(button_id, str), 'ID must be a string'

        if action is None:
            action = _events.NONE

        # If element is a Menu
        onchange = None
        if isinstance(action, Menu):
            self._submenus.append(action)
            widget = _widgets.Button(title, button_id, onchange, self._open, action)
        # If element is a PyMenuAction
        elif action == _events.BACK:  # Back to Menu
            widget = _widgets.Button(title, button_id, onchange, self.reset, 1)  # reset is public, so no _current
        elif action == _events.RESET:  # Back to Top Menu
            widget = _widgets.Button(title, button_id, onchange, self.full_reset)  # no _current
        elif action == _events.CLOSE:  # Close Menu
            widget = _widgets.Button(title, button_id, onchange, self._close)
        elif action == _events.EXIT:  # Exit program
            widget = _widgets.Button(title, button_id, onchange, self._exit)
        elif action == _events.NONE:  # None action
            widget = _widgets.Button(title, button_id)
        # If element is a function
        elif isinstance(action, (types.FunctionType, types.MethodType)) or callable(action):
            widget = _widgets.Button(title, button_id, onchange, action, *args)
        else:
            raise ValueError('element must be a Menu, a PymenuAction or a function')

        # Configure and add the button
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget

    def add_color_input(self,
                        title,
                        color_type,
                        color_id='',
                        default='',
                        input_separator=',',
                        input_underline='_',
                        onchange=None,
                        onreturn=None,
                        previsualization_width=3,
                        **kwargs):
        """
        Add a color widget with RGB or Hex format to the Menu.
        Includes a preview box that renders the given color.

        The callbacks receive the current value and all unknown keyword
        arguments::

            onchange(current_color, **kwargs)
            onreturn(current_color, **kwargs)

        kwargs (Optional):
            - ``align``                 Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_ (str)
            - ``background_color``      Color of the background (tuple, list, :py:class:`pygame_menu.baseimage.BaseImage`)
            - ``background_inflate``    Inflate background color if enabled (bool)
            - ``font_color``            Widget font color (tuple, list)
            - ``font_name``             Widget font (str)
            - ``font_size``             Font size of the widget (int)
            - ``margin``                (x,y) margin in px (tuple, list)
            - ``selection_color``       Widget selection color (tuple, list)
            - ``selection_effect``      Widget selection effect (:py:class:`pygame_menu.widgets.core.Selection`)
            - ``shadow``                Shadow is enabled or disabled (bool)
            - ``shadow_color``          Text shadow color (tuple, list)
            - ``shadow_position``       Text shadow position, see locals for position (str)
            - ``shadow_offset``         Text shadow offset (int, float, None)

        :param title: Title of the color input
        :type title: str
        :param color_type: Type of the color input, can be "rgb" or "hex"
        :type color_type: str
        :param color_id: ID of the color input
        :type color_id: str
        :param default: Default value to display, if RGB must be a tuple (r,g,b), if HEX must be a string "#XXXXXX"
        :type default: str, tuple
        :param input_separator: Divisor between RGB channels, not valid in HEX format
        :type input_separator: str
        :param input_underline: Underline character
        :type input_underline: str
        :param onchange: Function when changing the selector
        :type onchange: callable, None
        :param onreturn: Function when pressing return button
        :type onreturn: callable, None
        :param previsualization_width: Previsualization width as a factor of the height
        :type previsualization_width: int, float
        :param kwargs: Optional keyword arguments
        :type kwargs: dict
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
            input_separator=input_separator,
            input_underline=input_underline,
            onchange=onchange,
            onreturn=onreturn,
            prev_size=previsualization_width,
            title=title,
            **kwargs
        )

        self._configure_widget(widget=widget, **attributes)
        widget.set_value(default)
        self._append_widget(widget)

        return widget

    def add_image(self,
                  image_path,
                  angle=0,
                  image_id='',
                  scale=(1, 1),
                  scale_smooth=False,
                  selectable=False,
                  **kwargs):
        """
        Add a simple image to the Menu.

        kwargs (Optional):
            - ``align``                 Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_ (str)
            - ``background_color``      Color of the background (tuple, list, :py:class:`pygame_menu.baseimage.BaseImage`)
            - ``background_inflate``    Inflate background color if enabled (bool)
            - ``margin``                (x,y) margin in px (tuple, list)
            - ``selection_color``       Widget selection color (tuple, list)
            - ``selection_effect``      Widget selection effect (:py:class:`pygame_menu.widgets.core.Selection`)

        :param image_path: Path of the image of the widget
        :type image_path: str
        :param angle: Angle of the image in degrees (clockwise)
        :type angle: int, float
        :param image_id: ID of the label
        :type image_id: str
        :param scale: Scale of the image (x,y), float or int
        :type scale: tuple, list
        :param scale_smooth: Scale is smoothed
        :type scale_smooth: bool
        :param selectable: Image accepts user selection
        :type selectable: bool
        :param kwargs: Optional keyword arguments
        :type kwargs: dict
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Image`
        """
        assert isinstance(selectable, bool)

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        widget = _widgets.Image(
            angle=angle,
            image_id=image_id,
            image_path=image_path,
            scale=scale,
            scale_smooth=scale_smooth,
        )

        widget.is_selectable = selectable
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)
        return widget

    def add_label(self,
                  title,
                  label_id='',
                  max_char=0,
                  selectable=False,
                  **kwargs):
        """
        Add a simple text to the Menu.

        kwargs (Optional):
            - ``align``                 Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_ (str)
            - ``background_color``      Color of the background (tuple, list, :py:class:`pygame_menu.baseimage.BaseImage`)
            - ``background_inflate``    Inflate background color if enabled (bool)
            - ``font_color``            Widget font color (tuple, list)
            - ``font_name``             Widget font (str)
            - ``font_size``             Font size of the widget (int)
            - ``margin``                (x,y) margin in px (tuple, list)
            - ``shadow``                Shadow is enabled or disabled (bool)
            - ``shadow_color``          Text shadow color (tuple, list)
            - ``shadow_position``       Text shadow position, see locals for position (str)
            - ``shadow_offset``         Text shadow offset (int, float, None)

        :param title: Text to be displayed
        :type title: str
        :param label_id: ID of the label
        :type label_id: str
        :param max_char: Split the title in several labels if length exceeds. (0: don't split, -1: split to menu width)
        :type max_char: int
        :param selectable: Label accepts user selection, if not selectable long paragraphs cannot be scrolled through keyboard
        :type selectable: bool
        :param kwargs: Optional keyword arguments
        :type kwargs: dict
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

        # Wrap text to menu width (imply additional calls to render functions)
        if max_char < 0:
            dummy_attrs = self._filter_widget_attributes(kwargs.copy())
            dummy = _widgets.Label(title=title)
            self._configure_widget(dummy, **dummy_attrs)
            max_char = int(1.0 * self._width * len(title) / dummy.get_rect().width)

        # If no overflow
        if len(title) <= max_char or max_char == 0:
            attributes = self._filter_widget_attributes(kwargs)
            widget = _widgets.Label(title=title, label_id=label_id)
            widget.is_selectable = selectable
            self._configure_widget(widget=widget, **attributes)
            self._append_widget(widget)
        else:
            self._check_id_duplicated(label_id)  # Before adding + LEN
            widget = []
            for line in textwrap.wrap(title, max_char):
                widget.append(
                    self.add_label(
                        title=line,
                        label_id=label_id + '+' + str(len(widget) + 1),
                        max_char=max_char,
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
                     selector_id='',
                     **kwargs):
        """
        Add a selector to the Menu: several items with values and
        two functions that are executed when changing the selector (left/right)
        and pressing return button on the selected item.

        The values of the selector are like::

            values = [('Item1', a, b, c...), ('Item2', d, e, f..)]

        The callbacks receive the current text, its index in the list,
        the associated arguments and all unknown keyword arguments::

            onchange((current_text, index), a, b, c..., **kwargs)
            onreturn((current_text, index), a, b, c..., **kwargs)

        kwargs (Optional):
            - ``align``                 Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_ (str)
            - ``background_color``      Color of the background (tuple, list, :py:class:`pygame_menu.baseimage.BaseImage`)
            - ``background_inflate``    Inflate background color if enabled (bool)
            - ``font_color``            Widget font color (tuple, list)
            - ``font_name``             Widget font (str)
            - ``font_size``             Font size of the widget (int)
            - ``margin``                (x,y) margin in px (tuple, list)
            - ``selection_color``       Widget selection color (tuple, list)
            - ``selection_effect``      Widget selection effect (:py:class:`pygame_menu.widgets.core.Selection`)
            - ``shadow``                Shadow is enabled or disabled (bool)
            - ``shadow_color``          Text shadow color (tuple, list)
            - ``shadow_position``       Text shadow position, see locals for position (str)
            - ``shadow_offset``         Text shadow offset (int, float, None)

        :param title: Title of the selector
        :type title: str
        :param items: Elements of the selector [('Item1', var1..), ('Item2'...)]
        :type items: list
        :param default: Index of default value to display
        :type default: int
        :param onchange: Function when changing the selector
        :type onchange: callable, None
        :param onreturn: Function when pressing return button
        :type onreturn: callable, None
        :param selector_id: ID of the selector
        :type selector_id: str
        :param kwargs: Optional keyword arguments
        :type kwargs: dict
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
            selector_id=selector_id,
            title=title,
            **kwargs
        )

        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget

    def add_text_input(self,
                       title,
                       default='',
                       copy_paste_enable=True,
                       cursor_selection_enable=True,
                       input_type=_locals.INPUT_TEXT,
                       input_underline='',
                       maxchar=0,
                       maxwidth=0,
                       onchange=None,
                       onreturn=None,
                       password=False,
                       tab_size=4,
                       textinput_id='',
                       valid_chars=None,
                       **kwargs):
        """
        Add a text input to the Menu: free text area and two functions
        that execute when changing the text and pressing return button
        on the element.

        The callbacks receive the current value and all unknown keyword
        arguments::

            onchange(current_text, **kwargs)
            onreturn(current_text, **kwargs)

        kwargs (Optional):
            - ``align``                 Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_ (str)
            - ``background_color``      Color of the background (tuple, list, :py:class:`pygame_menu.baseimage.BaseImage`)
            - ``background_inflate``    Inflate background color if enabled (bool)
            - ``font_color``            Widget font color (tuple, list)
            - ``font_name``             Widget font (str)
            - ``font_size``             Font size of the widget (int)
            - ``margin``                (x,y) margin in px (tuple, list)
            - ``selection_color``       Widget selection color (tuple, list)
            - ``selection_effect``      Widget selection effect (:py:class:`pygame_menu.widgets.core.Selection`)
            - ``shadow``                Shadow is enabled or disabled (bool)
            - ``shadow_color``          Text shadow color (tuple, list)
            - ``shadow_position``       Text shadow position, see locals for position (str)
            - ``shadow_offset``         Text shadow offset (int, float, None)

        :param title: Title of the text input
        :type title: str
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
        :param maxchar: Maximum length of string, if 0 there's no limit
        :type maxchar: int
        :param maxwidth: Maximum size of the text widget, if 0 there's no limit
        :type maxwidth: int
        :param onchange: Function when changing the selector
        :type onchange: callable, None
        :param onreturn: Function when pressing return button
        :type onreturn: callable, None
        :param password: Text input is a password
        :type password: bool
        :param tab_size: Size of tab key
        :type tab_size: int
        :param textinput_id: ID of the text input
        :type textinput_id: str
        :param valid_chars: List of authorized chars, None if all chars are valid
        :type valid_chars: list
        :param kwargs: Optional keyword arguments
        :type kwargs: dict
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
            maxchar=maxchar,
            maxwidth=maxwidth,
            onchange=onchange,
            onreturn=onreturn,
            password=password,
            tab_size=tab_size,
            textinput_id=textinput_id,
            title=title,
            valid_chars=valid_chars,
            **kwargs
        )

        self._configure_widget(widget=widget, **attributes)
        widget.set_value(default)
        self._append_widget(widget)

        return widget

    def add_vertical_margin(self, margin):
        """
        Adds a vertical margin to the current Menu.

        :param margin: Vertical margin in px
        :type margin: int, float
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.VMargin`
        """
        assert isinstance(margin, (int, float))

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes({'margin': (0, margin)})

        widget = _widgets.VMargin()

        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget

    def _filter_widget_attributes(self, kwargs):
        """
        Return the valid widgets attributes from a dictionary.
        The valid (key, value) are removed from the initial
        dictionary.

        :param kwargs: Optional keyword arguments (input attributes)
        :type kwargs: dict
        :return: Dictionary of valid attributes
        :rtype: dict
        """
        attributes = {}
        align = kwargs.pop('align', self._theme.widget_alignment)
        assert isinstance(align, str)
        attributes['align'] = align

        background_color = kwargs.pop('background_color', self._theme.widget_background_color)
        if background_color is not None:
            if isinstance(background_color, _baseimage.BaseImage):
                pass
            else:
                _utils.assert_color(background_color)
        attributes['background_color'] = background_color

        background_inflate = kwargs.pop('background_inflate', self._theme.widget_background_inflate)
        _utils.assert_vector2(background_inflate)
        attributes['background_inflate'] = background_inflate

        attributes['font_antialias'] = self._theme.widget_font_antialias

        font_background_color = None
        if self._theme.widget_font_background_color_from_menu:
            if isinstance(self._theme.background_color, tuple):
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
        assert isinstance(margin, (tuple, list))
        assert len(margin) == 2, 'margin must be a tuple or list of 2 numbers'
        attributes['margin'] = margin

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
        assert isinstance(shadow_offset, (int, float, type(None)))
        attributes['shadow_offset'] = shadow_offset

        return attributes

    def _configure_widget(self, widget, **kwargs):
        """
        Update the given widget with the parameters defined at
        the Menu level.

        kwargs (Optional):
            - ``align``                 Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_ (str)
            - ``background_color``      Color of the background (tuple, list, :py:class:`pygame_menu.baseimage.BaseImage`)
            - ``background_inflate``    Inflate background color if enabled (bool)
            - ``font_color``            Widget font color (tuple, list)
            - ``font_name``             Widget font (str)
            - ``font_size``             Font size of the widget (int)
            - ``margin``                (x,y) margin in px (tuple, list)
            - ``selection_color``       Widget selection color (tuple, list)
            - ``selection_effect``      Widget selection effect (:py:class:`pygame_menu.widgets.core.Selection`)
            - ``shadow``                Shadow is enabled or disabled (bool)
            - ``shadow_color``          Text shadow color (tuple, list)
            - ``shadow_position``       Text shadow position, see locals for position (str)
            - ``shadow_offset``         Text shadow offset (int, float, None)

        :param widget: Widget object
        :type widget: :py:class:`pygame_menu.widgets.core.widget.Widget`
        :param kwargs: Optional keywords arguments
        :type kwargs: dict
        :return: None
        """
        assert isinstance(widget, _widgets.core.Widget)
        assert widget.get_menu() is None, 'widget cannot have an instance of menu'

        _col = int((len(self._widgets) - 1) // self._rows)  # Column position
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

        selection_effect = kwargs['selection_effect']  # type: _widgets.core.Selection

        if self._force_fit_text and self._column_max_width[_col] is not None:
            widget.set_max_width(self._column_max_width[_col] - selection_effect.get_width())

        widget.set_shadow(
            enabled=kwargs['shadow'],
            color=kwargs['shadow_color'],
            position=kwargs['shadow_position'],
            offset=kwargs['shadow_offset']
        )
        widget.set_controls(self._joystick, self._mouse, self._touchscreen)
        widget.set_alignment(kwargs['align'])
        widget.set_margin(*kwargs['margin'])
        widget.set_selection_effect(selection_effect)
        widget.set_background_color(kwargs['background_color'], kwargs['background_inflate'])

    def _append_widget(self, widget):
        """
        Add a widget to the list of widgets.

        :param widget: Widget object
        :type widget: :py:class:`pygame_menu.widgets.core.widget.Widget`
        :return: None
        """
        assert isinstance(widget, _widgets.core.Widget)
        assert widget.get_menu() == self, 'widget cannot have a different instance of menu'
        if self._columns > 1:
            max_elements = self._columns * self._rows
            assert len(self._widgets) + 1 <= max_elements, \
                'total widgets cannot be greater than columns*rows ({0} elements)'.format(max_elements)
        self._widgets.append(widget)
        if self._index < 0 and widget.is_selectable:
            widget.set_selected()
            self._index = len(self._widgets) - 1
        if self._auto_center_content:
            self.center_content()
        self._widgets_surface = None  # If added on execution time forces the update of the surface

    def remove_widget(self, widget):
        """
        Remove a widget from the Menu.

        :param widget: Widget object
        :type widget: :py:class:`pygame_menu.widgets.core.widget.Widget`
        :return: None
        """
        assert widget is not None, 'widget cannot be None'
        assert isinstance(widget, _widgets.core.Widget)
        try:
            indx = self._widgets.index(widget)  # If not exists this raises ValueError
        except ValueError:
            raise ValueError('widget is not in Menu, check if exists on the current '
                             'with menu.get_current().remove_widget(widget)')
        self._widgets.pop(indx)

        # Check if there's more selectable widgets
        nselect = 0
        last_selectable = 0
        for indx in range(len(self._widgets)):
            wid = self._widgets[indx]  # type: _widgets.core.Widget
            if wid.is_selectable:
                nselect += 1
                last_selectable = indx

        if nselect == 0:
            self._index = -1  # Any widget is selected
        elif nselect == 1:
            self._select(last_selectable)  # Select the unique selectable option
        elif nselect > 1:
            if self._index > indx:  # If the selected widget was after this
                self._select(self._index - 1)
            else:
                self._select(self._index)
        if self._auto_center_content:
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

    def _update_column_width(self):
        """
        Update the width of each column (self._column_widths). If the max column width is not set
        the width of the column will be the maximum widget in the column.

        :return: Total width of the columns
        :rtype: int
        """
        # Compute the available width, that is the surface width minus the max width columns
        self._column_widths = [0 for _ in range(self._columns)]
        for i in range(self._columns):
            if self._column_max_width[i] is not None:
                self._column_widths[i] = self._column_max_width[i]

        # Update None columns (max width not set)
        for index in range(len(self._widgets)):
            widget = self._widgets[index]
            rect = widget.get_rect()  # type: pygame.Rect
            col_index = int(index // self._rows)
            selection = widget.get_selection_effect()  # type: _widgets.core.Selection
            if self._column_max_width[col_index] is None:  # No limit
                self._column_widths[col_index] = max(self._column_widths[col_index],
                                                     rect.width + selection.get_width())

        # If the total weight is less than the window width (so there's no horizontal scroll), scale the columns
        if 0 < sum(self._column_widths) < self._width:
            scale = float(self._width) / sum(self._column_widths)
            for index in range(self._columns):
                self._column_widths[index] *= scale

        # Final column width
        total_col_width = float(sum(self._column_widths))

        if self._columns > 1:

            # Calculate column width scale (weights)
            column_weights = tuple(
                float(self._column_widths[i]) / max(total_col_width, 1) for i in range(self._columns))

            # Calculate the position of each column
            self._column_pos_x = []
            cumulative = 0
            for i in range(self._columns):
                w = column_weights[i]
                self._column_pos_x.append(total_col_width * (cumulative + 0.5 * w))
                cumulative += w

        else:
            self._column_pos_x = [total_col_width * 0.5]
            self._column_widths = [total_col_width]

        return total_col_width

    def _update_widget_position(self):
        """
        Update the position dict for each widget.

        :return: None
        """
        self._update_column_width()

        # Update title position
        self._menubar.set_position(self._pos_x, self._pos_y)

        # Store widget rects
        widget_rects = {}
        for widget in self._widgets:  # type: _widgets.core.Widget
            widget_rects[widget.get_id()] = widget.get_rect()

        # Update appended widgets
        for index in range(len(self._widgets)):
            widget = self._widgets[index]  # type: _widgets.core.Widget
            rect = widget_rects[widget.get_id()]  # type: pygame.Rect
            selection = widget.get_selection_effect()

            # Get column and row position
            col = int(index // self._rows)
            row = int(index % self._rows)

            # Calculate X position
            column_width = self._column_widths[col]
            _, sel_left, sel_bottom, sel_right = selection.get_margin()
            selection_margin = 0
            align = widget.get_alignment()
            if align == _locals.ALIGN_CENTER:
                dx = -float(rect.width) / 2
            elif align == _locals.ALIGN_LEFT:
                selection_margin = sel_left
                dx = -column_width / 2 + selection_margin
            elif align == _locals.ALIGN_RIGHT:
                selection_margin = sel_right
                dx = column_width / 2 - rect.width - selection_margin
            else:
                dx = 0
            x_coord = self._column_pos_x[col] + dx + widget.get_margin()[0]
            x_coord = max(selection_margin, x_coord)
            x_coord += self._widget_offset[0]

            # Calculate Y position
            ysum = 0  # Compute the total height from the current row position to the top of the column
            for r in range(row):
                rwidget = self._widgets[int(self._rows * col + r)]  # type: _widgets.core.Widget
                ysum += widget_rects[rwidget.get_id()].height + rwidget.get_margin()[1]
            y_coord = max(1, self._widget_offset[1]) + ysum + sel_bottom

            # Update the position of the widget
            widget.set_position(x_coord, y_coord)

    def _get_widget_max_position(self):
        """
        Return the lower rightmost position of each widgets in Menu.

        :return: Rightmost position
        :rtype: tuple
        """
        max_x = -1e6
        max_y = -1e6
        for widget in self._widgets:  # type: _widgets.core.Widget
            x, y = widget.get_rect().bottomright
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        return max_x, max_y

    def _build_widget_surface(self):
        """
        Create the surface used to draw widgets according the
        required width and height.

        :return: None
        """
        self._update_widget_position()

        menubar_height = self._menubar.get_rect().height
        max_x, max_y = self._get_widget_max_position()

        if max_x > self._width and max_y > self._height - menubar_height:
            width, height = max_x + 20, max_y + 20
            if not self._mouse_visible:
                self._mouse_visible = True
        elif max_x > self._width:
            # Remove the thick of the scrollbar
            # to avoid displaying an vertical one
            width, height = max_x + 20, self._height - menubar_height - 20
            self._mouse_visible = self._mouse_visible_default
        elif max_y > self._height - menubar_height:
            # Remove the thick of the scrollbar
            # to avoid displaying an horizontal one
            width, height = self._width - 20, max_y + 20
            if not self._mouse_visible:
                self._mouse_visible = True
        else:
            width, height = self._width, self._height - menubar_height
            self._mouse_visible = self._mouse_visible_default

        self._widgets_surface = _utils.make_surface(width, height)
        self._scroll.set_world(self._widgets_surface)
        self._scroll.set_position(self._pos_x, self._pos_y + menubar_height)

    def _check_id_duplicated(self, widget_id):
        """
        Check if widget ID is duplicated.

        :param widget_id: New widget ID
        :type widget_id: str
        :return: None
        """
        assert isinstance(widget_id, str)
        for widget in self._widgets:  # type: _widgets.core.Widget
            if widget.get_id() == widget_id:
                raise ValueError('widget ID="{0}" is duplicated'.format(widget_id))

    def _close(self):
        """
        Execute close callbacks and disable the Menu.

        :return: True if Menu has been disabled
        :rtype: bool
        """
        onclose = self._onclose
        if onclose is None:
            close = False
        else:
            close = True
            a = isinstance(onclose, _events.MenuAction)
            b = str(type(onclose)) == "<class 'pygame_menu.events.PymenuAction'>"  # python compatibility
            if a or b:
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

            elif isinstance(onclose, (types.FunctionType, types.MethodType)):
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
        Disables the Menu (doesn't check events and draw on the surface).

        :return: None
        """
        self._top._enabled = False

    def set_relative_position(self, position_x, position_y):
        """
        Set the menu position relative to the window.

        - Menu left position (x) must be between 0 and 100, if 0 the margin
          is at the left of the window, if 100 the menu is at the right
          of the window.

        - Menu top position (y) must be between 0 and 100, if 0 the margin is
          at the top of the window, if 100 the margin is at the bottom of
          the window.

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
        Update draw_region_y based on the current widgets, centering the content
        of the window.

        If the height of the widgets is greater than the height of the Menu,
        the drawing region will start at zero, using all the height for the scrollbar.

        :return: None
        """
        if len(self._widgets) == 0:  # If this happen, get_widget_max returns an immense value
            self._widget_offset[1] = 0
            return
        self._build_widget_surface()  # For position
        horizontal_scroll = self._scroll.get_scrollbar_thickness(_locals.ORIENTATION_HORIZONTAL)
        _, max_y = self._get_widget_max_position()
        max_y -= self._widget_offset[1]  # Only use total height
        available = self._height - self._menubar.get_rect().height - horizontal_scroll
        new_pos = max((available - max_y) / (2.0 * self._height), 0)  # Percentage of height
        self._widget_offset[1] = self._height * new_pos
        self._current._widgets_surface = None  # Rebuild on the next draw

    def draw(self, surface, clear_surface=False):
        """
        Draw the current Menu into the given surface.

        .. note:: This method should not be used along :py:meth:`pygame_menu.Menu.get_current()`

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

        # The surface may has been erased because the number
        # of widgets has changed and thus size shall be calculated.
        if not self._current._widgets_surface:
            self._current._build_widget_surface()

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
            widget.draw(self._current._widgets_surface)
            if widget.selected:
                widget.draw_selection(self._current._widgets_surface)
                selected_widget = widget

        self._current._scroll.draw(surface)
        self._current._menubar.draw(surface)

        # Focus on selected if the widget is active
        self._draw_focus_widget(surface, selected_widget)

    def _draw_focus_widget(self, surface, widget):
        """
        Draw the focus background from a given widget.

        :param surface: Pygame surface to draw the Menu
        :type surface: :py:class:`pygame.Surface`
        :param widget: Focused widget
        :type widget: :py:class:`pygame_menu.widgets.core.widget.Widget`, None
        :return: None
        """
        assert isinstance(surface, pygame.Surface)
        assert isinstance(widget, (_widgets.core.Widget, type(None)))

        if widget is None or not widget.active or not self._mouse_motion_selection:
            return
        window_width, window_height = self._window_size

        rect = widget.get_rect()
        if widget.selected and widget.get_selection_effect():
            rect = widget.get_selection_effect().inflate(rect)
        rect = self._current._scroll.to_real_position(rect, visible=True)

        x1, y1, x2, y2 = rect.topleft + rect.bottomright

        # Convert to integer
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        # Draw 4 areas:
        # .------------------.
        # |________1_________|
        # |  2  |XXXXXX|  3  |
        # |_____|XXXXXX|_____|
        # |        4         |
        # .------------------.

        if abs(y1 - y2) <= 4 or abs(x1 - x2) <= 4:
            gfxdraw.filled_polygon(surface,
                                   [(0, 0), (window_width, 0), (window_width, window_height), (0, window_height)],
                                   self._theme.focus_background_color)
            return

        gfxdraw.filled_polygon(surface,
                               [(0, 0), (window_width, 0), (window_width, y1 + 1), (0, y1 + 1)],
                               self._theme.focus_background_color)  # 1
        gfxdraw.filled_polygon(surface,
                               [(0, y1 + 2), (x1 + 1, y1 + 2), (x1 + 1, y2 - 2), (0, y2 - 2)],
                               self._theme.focus_background_color)  # 2
        gfxdraw.filled_polygon(surface,
                               [(x2 - 1, y1 + 2), (window_width, y1 + 2), (window_width, y2 - 2), (x2 - 1, y2 - 2)],
                               self._theme.focus_background_color)  # 3
        gfxdraw.filled_polygon(surface,
                               [(0, y2 - 1), (window_width, y2 - 1), (window_width, window_height), (0, window_height)],
                               self._theme.focus_background_color)  # 4

    def enable(self):
        """
        Enables Menu (can check events and draw).

        :return: None
        """
        self._top._enabled = True

    def toggle(self):
        """
        Switch between enable and disable.

        :return: None
        """
        self._top._enabled = not self._top._enabled

    @staticmethod
    def _exit():
        """
        Internal exit function.

        :return: None
        """
        pygame.quit()
        sys.exit()

    def is_enabled(self):
        """
        Return True if the menu is enabled.

        :return: Menu enabled status
        :rtype: bool
        """
        return self._top._enabled

    def _left(self):
        """
        Left event (column support).

        :return: None
        """
        if self._index >= self._rows:
            self._select(self._index - self._rows)
        else:
            self._select(0, 1)

    def _right(self):
        """
        Right event (column support).

        :return: None
        """
        if self._index + self._rows < len(self._widgets):
            self._select(self._index + self._rows)
        else:
            self._select(len(self._widgets) - 1)

    def _handle_joy_event(self):
        """
        Handle joy events.

        :return: None
        """
        if self._joy_event & self._joy_event_up:
            self._select(self._index - 1)
        if self._joy_event & self._joy_event_down:
            self._select(self._index + 1)
        if self._joy_event & self._joy_event_left:
            self._left()
        if self._joy_event & self._joy_event_right:
            self._right()

    def update(self, events):
        """
        Update the status of the Menu using external events.
        The update event is applied only on the current Menu.

        .. note:: This method should not be used along :py:meth:`pygame_menu.Menu.get_current()`

        :param events: Pygame events as a list
        :type events: list[:py:class:`pygame.event.Event`]
        :return: True if mainloop must be stopped
        :rtype: bool
        """
        assert isinstance(events, list)

        # If any widget status changes, set the status as True
        updated = False

        # Update mouse
        pygame.mouse.set_visible(self._current._mouse_visible)

        selected_widget = None  # type: _widgets.core.Widget
        if len(self._current._widgets) >= 1:
            selected_widget = self._current._widgets[self._current._index % len(self._current._widgets)]

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
                    elif event.key == _controls.KEY_LEFT and self._current._columns > 1:
                        self._current._left()
                        self._current._sounds.play_key_add()
                    elif event.key == _controls.KEY_RIGHT and self._current._columns > 1:
                        self._current._right()
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
                    elif event.value == _controls.JOY_LEFT and self._columns > 1:
                        self._current._select(self._current._index - 1)
                    elif event.value == _controls.JOY_RIGHT and self._columns > 1:
                        self._current._select(self._current._index + 1)

                elif self._current._joystick and event.type == pygame.JOYAXISMOTION:
                    prev = self._current._joy_event
                    self._current._joy_event = 0
                    if event.axis == _controls.JOY_AXIS_Y and event.value < -_controls.JOY_DEADZONE:
                        self._current._joy_event |= self._current._joy_event_up
                    if event.axis == _controls.JOY_AXIS_Y and event.value > _controls.JOY_DEADZONE:
                        self._current._joy_event |= self._current._joy_event_down
                    if event.axis == _controls.JOY_AXIS_X and event.value < -_controls.JOY_DEADZONE and self._columns > 1:
                        self._current._joy_event |= self._current._joy_event_left
                    if event.axis == _controls.JOY_AXIS_X and event.value > _controls.JOY_DEADZONE and self._columns > 1:
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
                                    widget.is_selectable:
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
                        if self._current._scroll.collide(widget, event) and widget.is_selectable:
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
                                    widget.is_selectable:
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

        # Check if the menu widgets size changed, if True, updates the surface
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

        return updated

    def mainloop(self, surface, bgfun=None, disable_loop=False, fps_limit=30):
        """
        Main loop of Menu. In this function, the Menu handle exceptions and draw.
        The Menu pauses the application and checks :py:mod:`pygame` events itself.
        This method returns until the menu is updated (a widget status has changed).

        The execution of the mainloop is at the current Menu level.

        .. code-block:: python

            menu = pygame_menu.Menu(...)

            menu.mainloop(surface)

        .. note:: This method should not be used along :py:meth:`pygame_menu.Menu.get_current()`

        :param surface: Pygame surface to draw the Menu
        :type surface: :py:class:`pygame.Surface`
        :param bgfun: Background function called on each loop iteration before drawing the Menu
        :type bgfun: callable, None
        :param disable_loop: If true run this method for only 1 loop
        :type disable_loop: bool
        :param fps_limit: Limit frame per second of the loop, if 0 there's no limit
        :type fps_limit: int, float
        :return: None
        """
        assert isinstance(surface, pygame.Surface)
        if bgfun:
            assert callable(bgfun), 'background function must be callable (a function)'
        assert isinstance(disable_loop, bool)
        assert isinstance(fps_limit, (int, float))
        assert fps_limit >= 0, 'fps limit cannot be negative'

        # NOTE: For Menu accessor, use only _current, as the Menu pointer can change through the execution
        if not self.is_enabled():
            return

        self._background_function = bgfun

        while True:
            self._current._clock.tick(fps_limit)

            self.draw(surface=surface, clear_surface=True)

            # If loop, gather events by Menu and draw the background function, if this method
            # returns true then the mainloop will break
            self.update(pygame.event.get())

            if not self.is_enabled() or disable_loop:
                self._background_function = None
                return

            # Flip contents to screen
            pygame.display.flip()

    def get_input_data(self, recursive=False):
        """
        Return input data from a Menu. The results are given as a dict object.
        The keys are the ID of each element.

        With ``recursive=True``: it collect also data inside the all sub-menus.

        :param recursive: Look in Menu and sub-menus
        :type recursive: bool
        :return: Input dict e.g.: {'id1': value, 'id2': value, ...}
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
        :return: Input dict e.g.: {'id1': value, 'id2': value, ...}
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

        The sound is applied only to the base Menu (not the currently displayed,
        stored in _current pointer).

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

        :return: Menu title
        :rtype: str
        """
        return self._menubar.get_title()

    def full_reset(self):
        """
        Reset the Menu back to the first opened Menu.

        :return: None
        """
        depth = self._get_depth()
        if depth > 0:
            self.reset(depth)

    def clear(self):
        """
        Full reset Menu and clear all widgets.

        :return: None
        """
        self.full_reset()
        del self._widgets[:]
        del self._submenus[:]
        self._index = 0

    def _open(self, menu):
        """
        Open the given Menu.

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
        Go back in Menu history a certain number of times from the current Menu.
        This method operates through the current menu pointer.

        .. note:: This method should not be used along :py:meth:`pygame_menu.Menu.get_current()`

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

    def _select(self, new_index, dwidget=0):
        """
        Select the widget at the given index and unselect others.
        Selection forces rendering of the widget.
        Also play widget selection sound

        :param new_index: Widget index
        :type new_index: int
        :param dwidget: Direction to search if the *new_index* widget is non selectable
        :type dwidget: int
        :return: None
        """
        current = self._top._current
        if len(current._widgets) == 0:
            return

        # This stores +/-1 if the index increases or decreases
        # Used by non-selectable selection
        if dwidget == 0:
            if new_index < current._index:
                dwidget = -1
            else:
                dwidget = 1

        # Limit the index to the length
        total_current = len(current._widgets)
        new_index %= total_current
        if new_index == current._index:  # Index has not changed
            return

        # Get both widgets
        if current._index >= total_current:  # The length of the menu changed during execution time
            for i in range(total_current):  # Unselect all posible candidates
                current._widgets[i].set_selected(False)
            current._index = 0

        old_widget = current._widgets[current._index]  # type: _widgets.core.Widget
        new_widget = current._widgets[new_index]  # type:_widgets.core.Widget

        # If new widget is not selectable
        if not new_widget.is_selectable:
            if current._index >= 0:  # There's at least 1 selectable option (if only text this would be false)
                current._select(new_index + dwidget)
                return
            else:  # No selectable options, quit
                return

        # Selecting widgets forces rendering
        old_widget.set_selected(False)
        current._index = new_index  # Update selected index
        new_widget.set_selected()

        # Scroll to rect
        rect = new_widget.get_rect()
        if current._index == 0:  # Scroll to the top of the Menu
            rect = pygame.Rect(int(rect.x), 0, int(rect.width), int(rect.height))
        current._scroll.scroll_to_rect(rect)

        # Play widget selection sound
        self._current._sounds.play_widget_selection()

    def get_id(self):
        """
        Return the ID of the current/base Menu.

        :return: Menu ID
        :rtype: str
        """
        return self._id

    def get_window_size(self):
        """
        Return the window size (px) as a tuple of (width, height).

        :return: Window size in px
        :rtype: tuple
        """
        w, h = self._window_size
        return w, h

    def get_size(self):
        """
        Return the Menu size (px) as a tuple of (width, height).

        :return: Menu size in px
        :rtype: tuple
        """
        return self._width, self._height

    def get_widget(self, widget_id, recursive=False):
        """
        Return a widget by a given ID from the Menu.

        With ``recursive=True``: it looks for a widget in the Menu
        and all sub-menus. Use ``current`` for getting from current and
        base Menu.

        None is returned if no widget found.

        :param widget_id: Widget ID
        :type widget_id: str
        :param recursive: Look in Menu and submenus
        :type recursive: bool
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.core.widget.Widget`
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

    def get_index(self):
        """
        Get selected widget from the Menu.

        :return: Selected widget index
        :rtype: int
        """
        return self._index

    def get_selected_widget(self):
        """
        Return the selected widget on the Menu.

        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.core.widget.Widget`
        """
        return self._widgets[self._index]
