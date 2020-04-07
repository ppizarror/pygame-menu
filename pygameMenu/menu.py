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

import sys
import types
import warnings

import pygame as _pygame
import pygameMenu.config as _cfg
import pygameMenu.controls as _ctrl
import pygameMenu.events as _events
import pygameMenu.font as _fonts
import pygameMenu.locals as _locals
import pygameMenu.widgets as _widgets

from pygameMenu.scrollarea import ScrollArea as _ScrollArea
from pygameMenu.sound import Sound as _Sound
from pygameMenu.utils import check_key_pressed_valid, make_surface

# Joy events
_JOY_EVENT_LEFT = 1
_JOY_EVENT_RIGHT = 2
_JOY_EVENT_UP = 4
_JOY_EVENT_DOWN = 8
_JOY_EVENT_REPEAT = _pygame.NUMEVENTS - 1


# noinspection PyArgumentEqualDefault,PyProtectedMember,PyTypeChecker
class Menu(object):
    """
    Menu object.
    """

    def __init__(self,
                 surface,
                 window_width,
                 window_height,
                 font,
                 title,
                 back_box=True,
                 bgfun=None,
                 color_selected=_cfg.MENU_SELECTEDCOLOR,
                 dopause=True,
                 draw_region_x=_cfg.MENU_DRAW_X,
                 draw_region_y=_cfg.MENU_DRAW_Y,
                 draw_select=_cfg.MENU_SELECTED_DRAW,
                 enabled=True,
                 font_color=_cfg.MENU_FONT_COLOR,
                 font_size=_cfg.MENU_FONT_SIZE,
                 font_size_title=_cfg.MENU_FONT_SIZE_TITLE,
                 font_title=None,
                 fps=0,
                 joystick_enabled=True,
                 menu_alpha=_cfg.MENU_ALPHA,
                 menu_color=_cfg.MENU_BGCOLOR,
                 menu_color_title=_cfg.MENU_TITLE_BG_COLOR,
                 menu_height=_cfg.MENU_HEIGHT,
                 menu_width=_cfg.MENU_WIDTH,
                 mouse_enabled=True,
                 mouse_visible=True,
                 onclose=None,
                 option_margin=_cfg.MENU_OPTION_MARGIN,
                 option_shadow=_cfg.MENU_OPTION_SHADOW,
                 option_shadow_offset=_cfg.MENU_SHADOW_OFFSET,
                 option_shadow_position=_cfg.MENU_SHADOW_POSITION,
                 rect_width=_cfg.MENU_SELECTED_WIDTH,
                 title_offsetx=0,
                 title_offsety=0,
                 widget_alignment=_locals.ALIGN_CENTER,
                 columns=1,
                 rows=None,
                 column_weights=None,
                 force_fit_text=False,
                 ):
        """
        Menu constructor.

        :param surface: Pygame surface
        :type surface: pygame.surface.SurfaceType
        :param window_width: Window width size (px)
        :type window_width: int
        :param window_height: Window height size (px)
        :type window_height: int
        :param font: Font file path
        :type font: basestring
        :param title: Title of the menu (main title)
        :type title: basestring
        :param back_box: Draw a back-box button on header
        :type back_box: bool
        :param bgfun: Background drawing function (only if menu pause app)
        :type bgfun: function
        :param color_selected: Color of selected item
        :type color_selected: tuple
        :param dopause: Pause game
        :type dopause: bool
        :param draw_region_x: Drawing position of element inside menu (x-axis)
        :type draw_region_x: int
        :param draw_region_y: Drawing position of element inside menu (y-axis)
        :type draw_region_y: int
        :param draw_select: Draw a rectangle around selected item (bool)
        :type draw_select: bool
        :param enabled: Menu is enabled by default or not
        :type enabled: bool
        :param fps: FPS of the menu
        :type fps: int, float
        :param font_color: Color of font
        :type font_color: tuple
        :param font_size: Font size
        :type font_size: int
        :param font_size_title: Font size of the title
        :type font_size_title: int
        :param font_title: Alternative font of the title (file path)
        :type font_title: basestring
        :param joystick_enabled: Enable/disable joystick on menu
        :type joystick_enabled: bool
        :param menu_alpha: Alpha of background (0=transparent, 100=opaque)
        :type menu_alpha: int
        :param menu_color: Menu color
        :type menu_color: tuple
        :param menu_color_title: Background color of title
        :type menu_color_title: tuple
        :param menu_height: Height of menu (px)
        :type menu_height: int
        :param menu_width: Width of menu (px)
        :type menu_width: int
        :param mouse_enabled: Enable/disable mouse click on menu
        :type mouse_enabled: bool
        :param mouse_visible: Set mouse visible on menu
        :type mouse_visible: bool
        :param onclose: Function applied when closing the menu
        :type onclose: function, NoneType
        :param option_margin: Margin of each element in menu (px)
        :type option_margin: int
        :param option_shadow: Indicate if a shadow is drawn on each option
        :type option_shadow: bool
        :param option_shadow_offset: Offset of shadow
        :type option_shadow_offset: int
        :param option_shadow_position: Position of shadow
        :type option_shadow_position: basestring
        :param rect_width: Border with of rectangle around selected item
        :type rect_width: int
        :param title_offsetx: Offset x-position of title (px)
        :type title_offsetx: int
        :param title_offsety: Offset y-position of title (px)
        :type title_offsety: int
        :param widget_alignment: Default widget alignment
        :type widget_alignment: basestring
        :param columns: Number of columns, by default it's 1
        :type columns: int
        :param rows: Number of rows of each column, None if there's only 1 column
        :type rows: int,None
        :param column_weights: Tuple representing the width of each column, None if percentage is equal
        :type column_weights: tuple, None
        :param force_fit_text: Force text fitting on each menu option in multiple columns
        :type force_fit_text: bool
        """
        assert isinstance(window_width, int)
        assert isinstance(window_height, int)
        assert isinstance(font, str)
        assert isinstance(title, str)
        assert isinstance(back_box, bool)
        assert isinstance(color_selected, tuple)
        assert isinstance(dopause, bool)
        assert isinstance(draw_region_x, int)
        assert isinstance(draw_region_y, int)
        assert isinstance(draw_select, bool)
        assert isinstance(enabled, bool)
        assert isinstance(font_color, tuple)
        assert isinstance(font_size, int)
        assert isinstance(font_size_title, int)
        assert isinstance(font_title, (str, type(None)))
        assert isinstance(joystick_enabled, bool)
        assert isinstance(menu_alpha, int)
        assert isinstance(menu_color, tuple)
        assert isinstance(menu_color_title, tuple)
        assert isinstance(menu_height, int)
        assert isinstance(menu_width, int)
        assert isinstance(mouse_enabled, bool)
        assert isinstance(mouse_visible, bool)
        assert isinstance(option_margin, int)
        assert isinstance(option_shadow, bool)
        assert isinstance(option_shadow_offset, int)
        assert isinstance(option_shadow_position, str)
        assert isinstance(rect_width, int)
        assert isinstance(columns, int)
        assert isinstance(rows, (int, type(None)))
        assert isinstance(column_weights, (tuple, type(None)))
        assert isinstance(force_fit_text, bool)

        # Other asserts
        if dopause:
            assert callable(bgfun), \
                'bgfun must be a function (or None if menu does not pause ' \
                'execution of the application)'
        else:
            assert isinstance(bgfun, type(None)), \
                'bgfun must be None if menu does not pause execution of the application'
        assert dopause and bgfun is not None or not dopause and bgfun is None, \
            'if pause main execution is enabled then bgfun (Background ' \
            'function drawing) must be defined (not None)'
        assert draw_region_y >= 0 and draw_region_x >= 0, \
            'drawing regions must be greater or equal than zero'
        assert font_size > 0 and font_size_title > 0, \
            'font sizes must be greater than zero'
        assert menu_width > 0 and menu_height > 0, \
            'menu size must be greater than zero'
        assert 0 <= menu_alpha <= 100, \
            'menu_alpha must be between 0 and 100 (both values included)'
        assert option_margin >= 0, \
            'option margin must be greater or equal than zero'
        assert rect_width >= 0, 'rect_width must be greater or equal than zero'
        assert window_height > 0 and window_width > 0, \
            'window size must be greater than zero'
        assert columns >= 1, 'number of columns must be greater or equal than 1'
        if columns > 1:
            assert rows is not None and rows >= 1, 'if columns greater than 1 then rows must be equal or greater than 1'
        else:
            if columns == 1:
                assert rows is None, 'rows must be None if there is only 1 column'
                rows = 1e6  # Set rows as a big number

        self._actual = self  # Actual menu
        self._bgfun = bgfun
        self._bgcolor = (menu_color[0],
                         menu_color[1],
                         menu_color[2],
                         int(255 * (1 - (100 - menu_alpha) / 100.0))
                         )
        self._clock = _pygame.time.Clock()  # Inner clock
        self._closelocked = False  # Lock close until next mainloop
        self._dopause = dopause  # Pause or not
        self._drawselrect = draw_select
        self._enabled = enabled  # Menu is enabled or not
        self._font_color = font_color
        self._fps = 0  # type: int
        self._fsize = font_size
        self._height = menu_height
        self._index = 0  # Selected index
        self._joy_event = 0  # type: int
        self._onclose = onclose  # Function that calls after closing menu
        self._opt_dy = option_margin
        self._option_shadow = option_shadow
        self._option_shadow_offset = option_shadow_offset
        self._option_shadow_position = option_shadow_position
        self._rect_width = rect_width
        self._sel_color = color_selected
        self._sounds = _Sound()  # type: _Sound
        self._surface = surface
        self._width = menu_width

        # Menu widgets
        self._option = []  # type: list

        # Previous menu
        self._prev = None  # type: list

        # Top level menu
        self._top = None  # type: Menu

        # List of all linked menus
        self._submenus = []  # type: list

        # Load fonts
        self._font = _fonts.get_font(font, self._fsize)  # type: _pygame.font.Font
        self._font_name = font

        # Position of menu
        self._posx = int((window_width - self._width) / 2)  # type: int
        self._posy = int((window_height - self._height) / 2)  # type: int
        self._bgrect = [(self._posx, self._posy),
                        (self._posx + self._width, self._posy),
                        (self._posx + self._width, self._posy + self._height),
                        (self._posx, self._posy + self._height)
                        ]
        self._draw_regionx = draw_region_x
        self._draw_regiony = draw_region_y

        # Columns and rows
        self._option_offsety = int(self._height * (self._draw_regiony / 100.0))
        self._columns = columns
        if column_weights is None:
            column_weights = tuple(1 for _ in range(columns))
        else:
            for i in column_weights:
                assert i > 0, 'each column weight factor must be greater than zero'
        self._column_weights = column_weights
        self._force_fit_text = force_fit_text
        self._rows = rows
        self._widget_align = widget_alignment

        self._calculate_column_widths(self._width)  # At first, the width must be the same as the window

        # Init joystick
        self._joystick = joystick_enabled
        if self._joystick:
            if not _pygame.joystick.get_init():
                _pygame.joystick.init()
            for i in range(_pygame.joystick.get_count()):
                _pygame.joystick.Joystick(i).init()

        # Init mouse
        self._mouse = mouse_enabled and mouse_visible
        self._mouse_visible = mouse_visible

        # Create menu bar
        self._menubar = _widgets.MenuBar(title,
                                         self._width,
                                         back_box,
                                         self._bgcolor,
                                         None,
                                         self._back)
        self._menubar.set_menu(self)

        # Configure widget
        bg_color_title = (menu_color_title[0],
                          menu_color_title[1],
                          menu_color_title[2],
                          int(255 * (1 - (100 - menu_alpha) / 100.0)))
        self._menubar.set_title(title,
                                title_offsetx,
                                title_offsety)
        self._menubar.set_font(font_title or font,
                               font_size_title,
                               bg_color_title,
                               self._font_color)
        self._menubar.set_shadow(enabled=self._option_shadow,
                                 color=_cfg.MENU_SHADOW_COLOR,
                                 position=self._option_shadow_position,
                                 offset=self._option_shadow_offset)
        self._menubar.set_controls(self._joystick, self._mouse)

        # Selected option
        self._selected_inflate_x = 16  # type: int
        self._selected_inflate_y = 6  # type: int

        self._widgets_surface = None
        self._scroll = _ScrollArea(self._width,
                                   self._height - self._menubar.get_rect().height,
                                   area_color=self._bgcolor,
                                   shadow=self._option_shadow,
                                   shadow_offset=self._option_shadow_offset,
                                   shadow_position=self._option_shadow_position)

        # FPS of the menu
        self.set_fps(fps)

    def _calculate_column_widths(self, width):
        """
        Calculate the width of each column (self._column_widths). Each column
        will have a certain factor of the total width surface area (width param), that factor
        is stored in column_weigts. If there's only 1 column, then the factor
        is 100%. If there's multiple columns, for example, a column that has 25%, other
        50% and the other 25% then column_weigths can be (1, 2, 1) or (0.25, 0.5, 0.25).
        The sum of all column widths must be equal to the surface width.

        :param width: Surface width, can be the window (no scroll area) or the surface scroll area.
        :type width: int,float
        """
        assert isinstance(width, (int, float))
        assert width > 0, 'width must be greater than zero'
        if self._columns > 1:
            s = float(sum(self._column_weights[:self._columns]))
            cumulative = 0
            self._column_posx = []
            for i in range(self._columns):
                w = self._column_weights[i] / s
                self._column_posx.append(
                    int(width * (self._draw_regionx / 100.0 + (cumulative + 0.5 * w - 0.5))))
                cumulative += self._column_weights[i] / s
            self._column_widths = tuple(int(width * self._column_weights[i] / s) for i in range(self._columns))
        else:
            self._column_posx = [int(width * (self._draw_regionx / 100.0))]
            self._column_widths = [width]

    def add_button(self, element_name, element, *args, **kwargs):
        """
        Add button to menu.

        kwargs (Optional):
            - align         Widget alignment
            - font_size     Font size of the widget
            - option_id     Option ID

        :param element_name: Name of the element
        :type element_name: basestring
        :param element: Object
        :type element: Menu, _PymenuAction, function
        :param args: Additional arguments used by a function
        :param kwargs: Additional keyword arguments
        :return: Widget object
        :rtype: pygameMenu.widgets.button.Button
        """
        assert isinstance(element_name, str), 'element_name must be a string'
        option_id = kwargs.pop('option_id', '')
        assert isinstance(option_id, str), 'ID must be a string'

        # If element is a Menu
        if isinstance(element, Menu):
            self._submenus.append(element)
            widget = _widgets.Button(element_name, option_id, None, self._open, element)
        # If option is a PyMenuAction
        elif element == _events.BACK:  # Back to menu
            widget = _widgets.Button(element_name, option_id, None, self.reset, 1)
        elif element == _events.CLOSE:  # Close menu
            widget = _widgets.Button(element_name, option_id, None, self._close, False)
        elif element == _events.EXIT:  # Exit program
            widget = _widgets.Button(element_name, option_id, None, self._exit)
        # If element is a function
        elif isinstance(element, (types.FunctionType, types.MethodType)) or callable(element):
            widget = _widgets.Button(element_name, option_id, None, element, *args)
        else:
            raise ValueError('Element must be a Menu, a PymenuAction or a function')

        # Configure and add the button
        self._configure_widget(widget, kwargs.pop('font_size', self._fsize), kwargs.pop('align', self._widget_align))
        self._append_widget(widget)
        return widget

    def add_option(self, *args, **kwargs):
        """
        Add option to menu. Deprecated method.
        """
        _msg = 'Menu.add_option is deprecated, use Menu.add_button instead. This feature will be deleted in v3.0'
        warnings.warn(_msg, DeprecationWarning)
        return self.add_button(*args, **kwargs)

    def add_color_input(self,
                        title,
                        color_type,
                        color_id='',
                        default='',
                        input_separator=',',
                        input_underline='_',
                        align='',
                        font_size=0,
                        onchange=None,
                        onreturn=None,
                        previsualization_width=3,
                        **kwargs
                        ):
        """
        Add a color widget with RGB or Hex format. Includes a preview
        box that renders the given color.

        And functions onchange and onreturn does
            onchange(current_text, **kwargs)
            onreturn(current_text, **kwargs)

        :param title: Title of the color input
        :type title: basestring
        :param color_type: Type of the color input, can be "rgb" or "hex"
        :type color_type: basestring
        :param color_id: ID of the color input
        :type color_id: basestring
        :param default: Default value to display, if RGB must be a tuple (r,g,b), if HEX must be a string "#XXXXXX"
        :type default: basestring, tuple
        :param input_separator: Divisor between RGB channels, not valid in HEX format
        :type input_separator: basestring
        :param input_underline: Underline character
        :type input_underline: basestring
        :param align: Widget alignment
        :type align: basestring
        :param font_size: Font size of the widget
        :type font_size: int
        :param onchange: Function when changing the selector
        :type onchange: function, NoneType
        :param onreturn: Function when pressing return button
        :type onreturn: function, NoneType
        :param previsualization_width: Previsualization width as a factor of the height
        :type previsualization_width: float, int
        :param kwargs: Additional keyword-parameters
        :return: Widget object
        :rtype: pygameMenu.widgets.colorinput.ColorInput
        """
        assert isinstance(default, (str, tuple))
        widget = _widgets.ColorInput(label=title,
                                     colorinput_id=color_id,
                                     color_type=color_type,
                                     input_separator=input_separator,
                                     input_underline=input_underline,
                                     onchange=onchange,
                                     onreturn=onreturn,
                                     prev_size=previsualization_width,
                                     **kwargs)
        self._configure_widget(widget, font_size, align)
        widget.set_value(default)
        self._append_widget(widget)
        return widget

    def add_selector(self,
                     title,
                     values,
                     selector_id='',
                     default=0,
                     align='',
                     font_size=0,
                     onchange=None,
                     onreturn=None,
                     **kwargs
                     ):
        """
        Add a selector to menu: several options with values and two functions
        that execute when changing the selector (left/right) and pressing
        return button on the element.

        Values of the selector are like:
            values = [('Item1', a, b, c...), ('Item2', a, b, c..)]

        And functions onchange and onreturn does
            onchange(a, b, c..., **kwargs)
            onreturn(a, b, c..., **kwargs)

        :param title: Title of the selector
        :type title: basestring
        :param values: Values of the selector [('Item1', var1..), ('Item2'...)]
        :type values: list
        :param selector_id: ID of the selector
        :type selector_id: basestring
        :param default: Index of default value to display
        :type default: int
        :param align: Widget alignment
        :type align: basestring
        :param font_size: Font size of the widget
        :type font_size: int
        :param onchange: Function when changing the selector
        :type onchange: function, NoneType
        :param onreturn: Function when pressing return button
        :type onreturn: function, NoneType
        :param kwargs: Additional parameters
        :return: Widget object
        :rtype: pygameMenu.widgets.selector.Selector
        """
        widget = _widgets.Selector(label=title,
                                   elements=values,
                                   selector_id=selector_id,
                                   default=default,
                                   onchange=onchange,
                                   onreturn=onreturn,
                                   **kwargs)
        self._configure_widget(widget, font_size, align)
        self._append_widget(widget)
        return widget

    def add_text_input(self,
                       title,
                       textinput_id='',
                       default='',
                       input_type=_locals.INPUT_TEXT,
                       input_underline='',
                       maxchar=0,
                       maxwidth=0,
                       align='',
                       font_size=0,
                       enable_copy_paste=True,
                       enable_selection=True,
                       password=False,
                       onchange=None,
                       onreturn=None,
                       valid_chars=None,
                       **kwargs
                       ):
        """
        Add a text input to menu: free text area and two functions
        that execute when changing the text and pressing return button
        on the element.

        And functions onchange and onreturn does
            onchange(current_text, **kwargs)
            onreturn(current_text, **kwargs)

        :param title: Title of the text input
        :type title: basestring
        :param textinput_id: ID of the text input
        :type textinput_id: basestring
        :param default: Default value to display
        :type default: basestring, int, float
        :param input_type: Data type of the input
        :type input_type: basestring
        :param input_underline: Underline character
        :type input_underline: basestring
        :param maxchar: Maximum length of string, if 0 there's no limit
        :type maxchar: int
        :param maxwidth: Maximum size of the text widget, if 0 there's no limit
        :type maxwidth: int
        :param align: Widget alignment
        :type align: basestring
        :param font_size: Font size of the widget
        :type font_size: int
        :param enable_copy_paste: Enable text copy, paste and cut
        :type enable_copy_paste: bool
        :param enable_selection: Enable text selection on input
        :type enable_selection: bool
        :param password: Text input is a password
        :type password: bool
        :param onchange: Function when changing the selector
        :type onchange: function, NoneType
        :param onreturn: Function when pressing return button
        :type onreturn: function, NoneType
        :param valid_chars: List of chars to be ignored, None if no chars are invalid
        :type valid_chars: list
        :param kwargs: Additional keyword-parameters
        :return: Widget object
        :rtype: pygameMenu.widgets.textinput.TextInput
        """
        assert isinstance(default, (str, int, float))

        # If password is active no default value should exist
        if password and default != '':
            raise ValueError('default value must be empty if the input is a password')

        widget = _widgets.TextInput(label=title,
                                    textinput_id=textinput_id,
                                    maxchar=maxchar,
                                    maxwidth=maxwidth,
                                    input_type=input_type,
                                    input_underline=input_underline,
                                    enable_copy_paste=enable_copy_paste,
                                    enable_selection=enable_selection,
                                    valid_chars=valid_chars,
                                    password=password,
                                    onchange=onchange,
                                    onreturn=onreturn,
                                    **kwargs)
        self._configure_widget(widget, font_size, align)
        widget.set_value(default)
        self._append_widget(widget)
        return widget

    def _configure_widget(self, widget, font_size=0, align=''):
        """
        Update the given widget with the parameters defined at
        the menu level.

        :param widget: Widget object
        :type widget: pygameMenu.widgets.widget.Widget
        :param font_size: Widget font size
        :type font_size: int
        :param align: Widget alignment
        :type align: str
        """
        assert isinstance(widget, _widgets.WidgetType), 'widget must be a Widget instance'
        assert isinstance(font_size, int), 'font_size must be an integer'
        assert isinstance(align, str), 'align must be a string'

        if align == '':
            align = self._widget_align
        if font_size == 0:
            font_size = self._fsize
        assert font_size > 0, 'font_size must be greater than zero'

        widget.set_menu(self)
        self._check_id_duplicated(widget.get_id())
        widget.set_font(font=self._font_name,
                        font_size=font_size,
                        color=self._font_color,
                        selected_color=self._sel_color)
        if self._force_fit_text:
            widget.set_max_width(self._column_widths[(len(self._option) - 1) // self._rows])
        widget.set_shadow(enabled=self._option_shadow,
                          color=_cfg.MENU_SHADOW_COLOR,
                          position=self._option_shadow_position,
                          offset=self._option_shadow_offset)
        widget.set_controls(self._joystick, self._mouse)
        widget.set_alignment(align)

    def _append_widget(self, widget):
        """
        Append the widget to the option lists.

        :param widget: Widget object
        :type widget: pygameMenu.widgets.widget.Widget
        """
        assert isinstance(widget, _widgets.WidgetType)
        if self._columns > 1:
            _max_elements = self._columns * self._rows
            _msg = 'total elements cannot be greater than columns*rows ({0} elements)'.format(_max_elements)
            assert len(self._option) + 1 <= _max_elements, _msg
        self._option.append(widget)
        _totals = len(self._option)
        if _totals == 1:
            widget.set_selected()

    def _back(self):
        """
        Go to previous menu or close if top menu is currently displayed.

        :return: None
        """
        self._check_menu_initialized()
        if self._top._prev is not None:
            self.reset(1)
        else:
            self._close()

    def _build_widget_surface(self):
        """
        Create the surface used to draw widgets according the
        required width and height.
        """
        max_x = 0
        max_y = 0
        for index in range(len(self._option)):
            x, y = self._get_option_pos(index)[2:]
            max_x = max(max_x, x)
            max_y = max(max_y, y)

        menubar_height = self._menubar.get_rect().height
        if max_x > self._width and max_y > self._height - menubar_height:
            width, height = max_x + 20, max_y + 20
        elif max_x > self._width:
            # Remove the thick of the scrollbar
            # to avoid displaying an vertical one
            width, height = max_x + 20, self._height - menubar_height - 20
        elif max_y > self._height:
            # Remove the thick of the scrollbar
            # to avoid displaying an horizontal one
            width, height = self._width - 20, max_y + 20
        else:
            width, height = self._width, self._height - menubar_height

        self._calculate_column_widths(width)
        self._widgets_surface = make_surface(width, height)
        self._scroll.set_world(self._widgets_surface)
        self._scroll.set_position(self._posx, self._posy + menubar_height + 5)

    def _check_id_duplicated(self, widget_id):
        """
        Check if widget ID is duplicated.

        :param widget_id: New widget ID
        :type widget_id: basestring
        :return: Exception if ID is duplicated
        """
        for widget in self._option:
            if widget.get_id() == widget_id:
                raise ValueError('The widget ID="{0}" is duplicated'.format(widget_id))

    def _close(self, closelocked=True):
        """
        Execute close callbacks and disable the menu.

        :param closelocked: Lock close event
        :type closelocked: bool
        :return: True if menu has been disabled
        :rtype: bool
        """
        self._check_menu_initialized()
        onclose = self._top._actual._onclose
        if onclose is None:
            close = False
        else:
            close = True
            a = isinstance(onclose, _events._PymenuAction)
            b = str(type(onclose)) == _events._PYMENUACTION
            if a or b:
                if onclose == _events.DISABLE_CLOSE:
                    close = False
                else:
                    self._top.disable(closelocked)
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
        Find menu depth.

        :return: Depth
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

    def disable(self, closelocked=True):
        """
        Disable the menu.

        :return: None
        """
        if self.is_enabled():
            self._enabled = False
            self._closelocked = closelocked

    def _get_option_pos(self, index):
        """
        Get option position on the widgets surface from the option index.

        :param index: Option index
        :type index: int
        :return: Top left, bottom right as a tuple (x1, y1, x2, y2)
        :rtype: tuple
        """
        rect = self._option[index].get_rect()
        align = self._option[index].get_alignment()

        # Calculate alignment
        _column_width = self._column_widths[int(index // self._rows)]  # if column=1 then (column width)=(menu width)
        if align == _locals.ALIGN_CENTER:
            option_dx = -int(rect.width / 2.0)
        elif align == _locals.ALIGN_LEFT:
            option_dx = -_column_width / 2 + self._selected_inflate_x
        elif align == _locals.ALIGN_RIGHT:
            option_dx = _column_width / 2 - rect.width - self._selected_inflate_x
        else:
            option_dx = 0
        t_dy = -int(rect.height / 2.0)

        x_coord = self._column_posx[int(index // self._rows)] + option_dx
        y_coord = self._option_offsety + (index % self._rows) * (self._fsize + self._opt_dy) + t_dy
        return x_coord, y_coord, x_coord + rect.width, y_coord + rect.height

    def draw(self):
        """
        Draw menu to the active surface.

        :return: None
        """
        # The surface may has been erased because the number
        # of widgets has changed and thus size shall be calculated.
        if not self._widgets_surface:
            self._build_widget_surface()

        # Update menu bar position
        self._menubar.set_position(self._posx, self._posy)

        # Draw options (widgets)
        self._widgets_surface.fill((255, 255, 255, 0))  # Transparent
        for index in range(len(self._option)):
            widget = self._option[index]

            # Update widget position
            widget.set_position(*self._get_option_pos(index)[:2])

            # Draw widget
            widget.draw(self._widgets_surface)

            # If selected item then draw a rectangle
            if self._drawselrect and widget.selected:
                widget.draw_selected_rect(self._widgets_surface,
                                          self._sel_color,
                                          self._selected_inflate_x,
                                          self._selected_inflate_y,
                                          self._rect_width)

        self._scroll.draw(self._surface)
        self._menubar.draw(self._surface)

    def enable(self):
        """
        Enables the menu.

        :return: None
        """
        if self.is_disabled():
            self._enabled = True
            self._closelocked = True

    @staticmethod
    def _exit():
        """
        Internal exit function.

        :return: None
        """
        _pygame.quit()
        sys.exit()

    def is_disabled(self):
        """
        Returns false/true if menu is disabled or not.

        :return: True if the menu is disabled
        :rtype: bool
        """
        return not self.is_enabled()

    def is_enabled(self):
        """
        Returns true/false if menu is enabled or not.

        :return: True if the menu is enabled
        :rtype: bool
        """
        return self._enabled

    def _left(self):
        """
        Left event (column support).
        """
        if self._actual._index >= self._actual._rows:
            self._select(self._actual._index - self._actual._rows)
        else:
            self._select(0)

    def _right(self):
        """
        Right event (column support).
        """
        if self._actual._index + self._actual._rows < len(self._actual._option):
            self._select(self._actual._index + self._actual._rows)
        else:
            self._select(len(self._actual._option) - 1)

    def _handle_joy_event(self):
        """
        Handle joy events.
        """
        if self._joy_event & _JOY_EVENT_UP:
            self._select(self._actual._index - 1)
        if self._joy_event & _JOY_EVENT_DOWN:
            self._select(self._actual._index + 1)
        if self._joy_event & _JOY_EVENT_LEFT:
            self._left()
        if self._joy_event & _JOY_EVENT_RIGHT:
            self._right()

    def _main(self, events=None):
        """
        Main function of the loop.

        :param events: Pygame events
        :type events: list
        :return: True if mainloop must be stopped
        :rtype: bool
        """
        break_mainloop = False
        if events is None:
            events = _pygame.event.get()

        # Update mouse
        _pygame.mouse.set_visible(self._actual._mouse_visible)

        if self._actual._dopause:  # If menu pauses game then apply function
            self._bgfun()

        # Clock tick
        self._actual._clock.tick(self._fps)

        # Process events, check title
        if self._actual._menubar.update(events):
            if not self._actual._dopause:
                break_mainloop = True

        # Process events, check title
        if self._actual._scroll.update(events):
            if not self._actual._dopause:
                break_mainloop = True

        # Check selected widget
        elif len(self._actual._option) > 0 and self._actual._option[self._actual._index].update(events):
            if not self._actual._dopause:
                break_mainloop = True

        # Check others
        else:

            for event in events:  # type: _pygame.event.EventType

                # noinspection PyUnresolvedReferences
                if event.type == _pygame.locals.QUIT or (
                        event.type == _pygame.KEYDOWN and event.key == _pygame.K_F4 and (
                        event.mod == _pygame.KMOD_LALT or event.mod == _pygame.KMOD_RALT)):
                    self._exit()
                    break_mainloop = True

                elif event.type == _pygame.locals.KEYDOWN:

                    # Check key event is valid
                    if not check_key_pressed_valid(event):
                        continue

                    if event.key == _ctrl.KEY_MOVE_DOWN:
                        self._select(self._actual._index - 1)
                        self._sounds.play_key_add()
                    elif event.key == _ctrl.KEY_MOVE_UP:
                        self._select(self._actual._index + 1)
                        self._sounds.play_key_add()
                    elif event.key == _ctrl.KEY_LEFT and self._columns > 1:
                        self._left()
                        self._sounds.play_key_add()
                    elif event.key == _ctrl.KEY_RIGHT and self._columns > 1:
                        self._right()
                        self._sounds.play_key_add()
                    elif event.key == _ctrl.KEY_BACK and self._top._prev is not None:
                        self._sounds.play_close_menu()
                        self.reset(1)
                    elif event.key == _ctrl.KEY_CLOSE_MENU and not self._closelocked:
                        self._sounds.play_close_menu()
                        if self._close():
                            break_mainloop = True

                elif self._joystick and event.type == _pygame.JOYHATMOTION:
                    if event.value == _ctrl.JOY_UP:
                        self._select(self._actual._index - 1)
                    elif event.value == _ctrl.JOY_DOWN:
                        self._select(self._actual._index + 1)
                    elif event.value == _ctrl.JOY_LEFT and self._columns > 1:
                        self._select(self._actual._index - 1)
                    elif event.value == _ctrl.JOY_RIGHT and self._columns > 1:
                        self._select(self._actual._index + 1)

                elif self._joystick and event.type == _pygame.JOYAXISMOTION:
                    prev = self._joy_event
                    self._joy_event = 0
                    if event.axis == _ctrl.JOY_AXIS_Y and event.value < -_ctrl.JOY_DEADZONE:
                        self._joy_event |= _JOY_EVENT_UP
                    if event.axis == _ctrl.JOY_AXIS_Y and event.value > _ctrl.JOY_DEADZONE:
                        self._joy_event |= _JOY_EVENT_DOWN
                    if event.axis == _ctrl.JOY_AXIS_X and event.value < -_ctrl.JOY_DEADZONE and self._columns > 1:
                        self._joy_event |= _JOY_EVENT_LEFT
                    if event.axis == _ctrl.JOY_AXIS_X and event.value > _ctrl.JOY_DEADZONE and self._columns > 1:
                        self._joy_event |= _JOY_EVENT_RIGHT
                    if self._joy_event:
                        self._handle_joy_event()
                        if self._joy_event == prev:
                            _pygame.time.set_timer(_JOY_EVENT_REPEAT, _ctrl.JOY_REPEAT)
                        else:
                            _pygame.time.set_timer(_JOY_EVENT_REPEAT, _ctrl.JOY_DELAY)
                    else:
                        _pygame.time.set_timer(_JOY_EVENT_REPEAT, 0)

                elif event.type == _JOY_EVENT_REPEAT:
                    if self._joy_event:
                        self._handle_joy_event()
                        _pygame.time.set_timer(_JOY_EVENT_REPEAT, _ctrl.JOY_REPEAT)
                    else:
                        _pygame.time.set_timer(_JOY_EVENT_REPEAT, 0)

                elif self._mouse and event.type == _pygame.MOUSEBUTTONDOWN:
                    for index in range(len(self._actual._option)):
                        widget = self._actual._option[index]
                        # Don't considere the mouse wheel (button 4 & 5)
                        if event.button in (1, 2, 3) and \
                                self._actual._scroll.to_real_position(widget.get_rect()).collidepoint(*event.pos):
                            self._select(index)

                elif self._mouse and event.type == _pygame.MOUSEBUTTONUP:
                    self._sounds.play_click_mouse()
                    widget = self._actual._option[self._actual._index]
                    # Don't considere the mouse wheel (button 4 & 5)
                    if event.button in (1, 2, 3) and \
                            self._actual._scroll.to_real_position(widget.get_rect()).collidepoint(*event.pos):
                        new_event = _pygame.event.Event(event.type, **event.dict)
                        new_event.dict['origin'] = self._actual._scroll.to_real_position((0, 0))
                        new_event.pos = self._actual._scroll.to_world_position(event.pos)
                        widget.update((new_event,))  # This option can change the current menu to a submenu
                        break_mainloop = True  # It is updated
                        break

        # A widget has closed the menu
        if not self._top._enabled:
            break_mainloop = True

        # Draw content
        else:
            self._actual.draw()

        _pygame.display.flip()
        self._closelocked = False

        return break_mainloop

    def _check_menu_initialized(self):
        """
        Check menu initialization.

        :return: True if menu is initialized, raise Exception if not
        :rtype: bool
        """
        if self._top is None:
            raise Exception('The menu has not been initialized yet, try using mainloop function')
        return True

    def mainloop(self, events=None, disable_loop=False):
        """
        Main function of menu.

        :param events: Menu events
        :type events: list
        :param disable_loop: Disable infinite loop waiting for events
        :type disable_loop: bool
        :return: None
        """
        self._top = self

        if self.is_disabled():
            return
        if self._actual._dopause and not disable_loop:
            while True:
                if self._main():
                    return
        else:
            self._main(events)

    def get_input_data(self, recursive=False, depth=0):
        """
        Return input data as a dict.

        With ``recursive=True``: it looks for a widget inside the current menu
        and all sub-menus.

        :param recursive: Look in menu and sub-menus
        :type recursive: bool
        :param depth: Depth of the input data, by default it's zero
        :type depth: int
        :return: Input dict
        :rtype: dict
        """
        assert isinstance(recursive, bool), 'recursive must be a boolean'

        data = {}
        for widget in self._option:
            try:
                data[widget.get_id()] = widget.get_value()
            except ValueError:  # Widget does not return data
                pass
        if recursive:
            depth += 1
            for menu in self._submenus:
                data_submenu = menu.get_input_data(recursive=recursive, depth=depth)

                # Check if there is a collision between keys
                data_keys = data.keys()
                subdata_keys = data_submenu.keys()
                for key in subdata_keys:  # type: str
                    if key in data_keys:
                        msg = 'Collision between widget data ID="{0}" at depth={1}'.format(key, depth)
                        raise ValueError(msg)

                # Update data
                data.update(data_submenu)
        return data

    def get_position(self):
        """
        Return menu position as a tuple.

        :return: Top left, bottom right as a tuple (x1, y1, x2, y2)
        :rtype: tuple
        """
        return self._posx, self._posy, self._posx + self._width, self._posy + self._height

    def get_fps(self):
        """
        Return the frames per second of the menu.

        :return: FPS
        :rtype: float
        """
        return self._clock.get_fps()

    def set_fps(self, fps, recursive=True):
        """
        Set the frames per second limit of the menu.

        :param fps: FPS
        :type fps: float, int
        :param recursive: Set FPS to all the submenus
        :type recursive: bool
        :return: None
        """
        assert isinstance(fps, (float, int))
        assert isinstance(recursive, bool)
        assert fps >= 0, 'fps must be equal or greater than zero'
        self._fps = float(fps)
        for widget in self._option:
            widget.set_fps(fps)
        if recursive:
            for menu in self._submenus:
                menu.set_fps(fps, recursive=True)

    def set_sound(self, sound, recursive=False):
        """
        Set sound engine to a menu.

        :param sound: Sound object
        :type sound: pygameMenu.sound.Sound, NoneType
        :param recursive: Set the sound engine to all submenus
        :type recursive: bool
        :return: None
        """
        assert isinstance(sound, (type(self._sounds), type(None)))
        if sound is None:
            sound = _Sound()
        self._sounds = sound
        for widget in self._option:
            widget.set_sound(sound)
        if recursive:
            for menu in self._submenus:
                menu.set_sound(sound, recursive=True)

    def get_title(self, current=False):
        """
        Return title of the menu.

        :param current: Get the current title of the menu object (if a submenu has been opened)
        :type current: bool
        :return: Title
        :rtype: basestring
        """
        if current:
            return self._actual._menubar.get_title()
        else:
            return self._menubar.get_title()

    def full_reset(self):
        """
        Reset to the first menu.

        :return: None
        """
        depth = self._actual._get_depth()
        if depth > 0:
            self.reset(depth)

    def _get_actual_index(self):
        """
        Get actual selected option.

        :return: Selected option index
        :rtype: int
        """
        return self._top._actual._index

    def clear(self):
        """
        Full reset menu and clear all widgets.

        :return: None
        """
        self.full_reset()
        del self._actual._option[:]
        del self._actual._submenus[:]

    def _open(self, menu):
        """
        Open the given menu.

        :param menu: Menu object
        :type menu: Menu, TextMenu
        :return: None
        """
        self._check_menu_initialized()
        actual = self
        menu._top = self._top
        self._top._actual = menu._actual
        self._top._prev = [self._top._prev, actual]
        self._select(0)

    def reset(self, total):
        """
        Reset the menu.

        :param total: How many menus to reset (1: back)
        :type total: int
        :return: None
        """
        self._check_menu_initialized()
        assert isinstance(self._top._actual, Menu)
        assert isinstance(total, int), 'total must be an integer'
        assert total > 0, 'total must be greater than zero'

        i = 0
        while True:
            if self._top._prev is not None:
                prev = self._top._prev
                self._top._actual = prev[1]
                self._top._prev = prev[0]  # Eventually will reach None
                i += 1
                if i == total:
                    break
            else:
                break

        self._select(self._top._actual._index)

    def _select(self, index):
        """
        Select the widget at the given index and unselect others.

        :param index: Widget index
        :type index: int
        :return: None
        """
        self._check_menu_initialized()
        actual = self._top._actual
        if len(actual._option) == 0:
            return
        actual._option[actual._index].set_selected(False)
        actual._index = index % len(actual._option)
        actual._option[actual._index].set_selected()
        actual._scroll.scroll_to_rect(actual._option[actual._index].get_rect())

    def get_widget(self, widget_id, recursive=False):
        """
        Return the widget with the given ID.

        With ``recursive=True``: it looks for a widget inside the current menu
        and all sub-menus.

        None is returned if no widget found.

        :param widget_id: Widget ID
        :type widget_id: basestring
        :param recursive: Look in menu and submenus
        :type recursive: bool
        :return: Widget object
        :rtype: pygameMenu.widgets.widget.Widget
        """
        assert isinstance(widget_id, str), 'widget_id must be a string'
        assert isinstance(recursive, bool), 'recursive must be a boolean'
        for widget in self._option:
            if widget.get_id() == widget_id:
                return widget
        if recursive:
            for menu in self._submenus:
                widget = menu.get_widget(widget_id, recursive)
                if widget:
                    return widget
        return None

    def get_selected_widget(self):
        """
        Return the currently selected widget.

        :return: Widget object
        :rtype: pygameMenu.widgets.widget.Widget
        """
        return self._top._actual._option[self._top._actual._index]
