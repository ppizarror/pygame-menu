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

import pygame as _pygame
import pygameMenu.controls as _ctrl
import pygameMenu.events as _events
import pygameMenu.locals as _locals
import pygameMenu.widgets as _widgets

from pygameMenu.scrollarea import ScrollArea as _ScrollArea
from pygameMenu.sound import Sound as _Sound
from pygameMenu.utils import *

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
                 menu_height,
                 menu_width,
                 font,
                 title,
                 back_box=True,
                 bgfun=None,
                 column_force_fit_text=False,
                 column_max_width=None,
                 columns=1,
                 dopause=True,
                 enabled=True,
                 fps=0,
                 joystick_enabled=True,
                 menu_alpha=100,
                 menu_background_color=(0, 0, 0),
                 mouse_enabled=True,
                 mouse_visible=True,
                 onclose=None,
                 rows=None,
                 selection_color=(180, 180, 180),
                 selection_highlight=True,
                 selection_highlight_border_width=1,
                 selection_highlight_margin_x=16,
                 selection_highlight_margin_y=4,
                 title_background_color=None,
                 title_font=None,
                 title_font_color=None,
                 title_font_size=40,
                 title_offset_x=0,
                 title_offset_y=0,
                 title_shadow=False,
                 title_shadow_color=(0, 0, 0),
                 title_shadow_offset=2,
                 title_shadow_position=_locals.POSITION_NORTHWEST,
                 widget_alignment=_locals.ALIGN_CENTER,
                 widget_font_color=(255, 255, 255),
                 widget_font_size=30,
                 widget_margin_y=15,
                 widget_offset_x=0,
                 widget_offset_y=0,
                 widget_shadow=False,
                 widget_shadow_color=(0, 0, 0),
                 widget_shadow_offset=2,
                 widget_shadow_position=_locals.POSITION_NORTHWEST,
                 ):
        """
        Menu constructor.

        :param surface: Pygame surface
        :type surface: pygame.surface.SurfaceType
        :param menu_height: Height of menu (px)
        :type menu_height: int,float
        :param menu_width: Width of menu (px)
        :type menu_width: int,float
        :param font: Font file path
        :type font: basestring
        :param title: Title of the menu (main title)
        :type title: basestring
        :param back_box: Draw a back-box button on header
        :type back_box: bool
        :param bgfun: Background drawing function (only if menu pause app)
        :type bgfun: function
        :param column_force_fit_text: Force text fitting of widgets if the width exceeds the column max width
        :type column_force_fit_text: bool
        :param column_max_width: List/Tuple representing the max width of each column in px, None equals no limit
        :type column_max_width: tuple, None
        :param columns: Number of columns, by default it's 1
        :type columns: int
        :param dopause: Pause game
        :type dopause: bool
        :param enabled: Menu is enabled by default or not
        :type enabled: bool
        :param fps: Maximum FPS (frames per second)
        :type fps: int, float
        :param joystick_enabled: Enable/disable joystick on menu
        :type joystick_enabled: bool
        :param menu_alpha: Alpha of background (0=transparent, 100=opaque)
        :type menu_alpha: int
        :param menu_background_color: Menu background color
        :type menu_background_color: tuple,list
        :param mouse_enabled: Enable/disable mouse click on menu
        :type mouse_enabled: bool
        :param mouse_visible: Set mouse visible on menu
        :type mouse_visible: bool
        :param onclose: Function applied when closing the menu
        :type onclose: function, NoneType
        :param rows: Number of rows of each column, None if there's only 1 column
        :type rows: int,None
        :param selection_color: Color of selected item
        :type selection_color: tuple,list
        :param selection_highlight: Enable drawing a rectangle around selected item
        :type selection_highlight: bool
        :param selection_highlight_border_width: Border with of rectangle around selected item
        :type selection_highlight_border_width: int
        :param selection_highlight_margin_x: X margin of selected highlight box
        :type selection_highlight_margin_x: int
        :param selection_highlight_margin_y: Y margin of selected highlight box
        :type selection_highlight_margin_y: int
        :param title_background_color: Title background color
        :type title_background_color: tuple,list
        :param title_font: Optional title font, if None use the menu default font
        :type title_font: basestring,None
        :param title_font_color: Title font color, if None use the widget font color
        :type title_font_color: list,tuple,None
        :param title_font_size: Font size of the title
        :type title_font_size: int
        :param title_offset_x: Offset x-position of title (px)
        :type title_offset_x: int
        :param title_offset_y: Offset y-position of title (px)
        :type title_offset_y: int
        :param title_offset_y: Title shadow color
        :type title_offset_y: tuple,list
        :param title_shadow: Enable shadow on title
        :type title_shadow: bool
        :param title_shadow_color: Title shadow color
        :type title_shadow_color: list,tuple
        :param title_shadow_offset: Offset of shadow on title
        :type title_shadow_offset: int
        :param title_shadow_position: Position of the shadow on title
        :type title_shadow_position: basestring
        :param widget_alignment: Widget default alignment
        :type widget_alignment: basestring
        :param widget_font_color: Color of the font
        :type widget_font_color: tuple,list
        :param widget_font_size: Font size
        :type widget_font_size: int
        :param widget_margin_y: Vertical margin of each element in menu (px)
        :type widget_margin_y: int
        :param widget_offset_x: X axis offset of widgets inside menu (px). If value less than 1 use percentage of width
        :type widget_offset_x: int,float
        :param widget_offset_y: Y axis offset of widgets inside menu (px). If value less than 1 use percentage of height
        :type widget_offset_y: int,float
        :param widget_shadow: Indicate if a shadow is drawn on each widget
        :type widget_shadow: bool
        :param widget_shadow_color: Color of the shadow
        :type widget_shadow_color: tuple,list
        :param widget_shadow_offset: Offset of shadow
        :type widget_shadow_offset: int
        :param widget_shadow_position: Position of shadow
        :type widget_shadow_position: basestring
        """
        assert isinstance(surface, _pygame.Surface)
        assert isinstance(menu_height, (int, float))
        assert isinstance(menu_width, (int, float))
        assert isinstance(font, str)
        assert isinstance(back_box, bool)
        assert isinstance(column_force_fit_text, bool)
        assert isinstance(column_max_width, (tuple, type(None), (int, float), list))
        assert isinstance(columns, int)
        assert isinstance(dopause, bool)
        assert isinstance(enabled, bool)
        assert isinstance(fps, (int, float))
        assert isinstance(joystick_enabled, bool)
        assert isinstance(menu_alpha, int)
        assert isinstance(mouse_enabled, bool)
        assert isinstance(mouse_visible, bool)
        assert isinstance(rows, (int, type(None)))
        assert isinstance(selection_highlight, bool)
        assert isinstance(selection_highlight_border_width, int)
        assert isinstance(selection_highlight_margin_x, int)
        assert isinstance(selection_highlight_margin_y, int)
        assert isinstance(title, str)
        assert isinstance(title_font, (str, type(None)))
        assert isinstance(title_font_size, int)
        assert isinstance(title_offset_x, int)
        assert isinstance(title_offset_y, int)
        assert isinstance(title_shadow, bool)
        assert isinstance(title_shadow_offset, int)
        assert isinstance(widget_alignment, str)
        assert isinstance(widget_font_size, int)
        assert isinstance(widget_margin_y, int)
        assert isinstance(widget_offset_x, (int, float))
        assert isinstance(widget_offset_y, (int, float))
        assert isinstance(widget_shadow, bool)
        assert isinstance(widget_shadow_offset, int)

        # Assert colors
        if title_background_color is None:
            title_background_color = menu_background_color
        if title_font_color is None:
            title_font_color = widget_font_color
        assert_color(menu_background_color, 'menu_background_color')
        assert_color(selection_color, 'selection_color')
        assert_color(title_background_color, 'title_background_color')
        assert_color(title_font_color, 'title_font_color')
        assert_color(title_shadow_color, 'title_shadow_color')
        assert_color(widget_font_color, 'widget_font_color')
        assert_color(widget_shadow_color, 'widget_shadow_color')

        # Assert positions
        assert_position(title_shadow_position)
        assert_position(widget_shadow_position)

        # Column/row asserts
        assert columns >= 1, 'number of columns must be greater or equal than 1'
        if columns > 1:
            assert rows is not None and rows >= 1, 'if columns greater than 1 then rows must be equal or greater than 1'
        else:
            if columns == 1:
                assert rows is None, 'rows must be None if there is only 1 column'
                rows = 1e6  # Set rows as a big number
        if column_max_width is not None:
            if isinstance(column_max_width, (int, float)):
                assert columns == 1, 'column_max_width can be a single number if there is only 1 column'
                column_max_width = [column_max_width]
            assert len(column_max_width) == columns, 'column_max_width length must be the same as the number of columns'
            for i in column_max_width:
                assert isinstance(i, type(None)) or isinstance(i, (int, float)), \
                    'each column max width can be None (no limit) or an integer/float'
                assert i > 0 or i is None, 'each column max width must be greater than zero or None'
        else:
            column_max_width = [None for _ in range(columns)]

        # Element size asserts
        assert menu_width > 0 and menu_height > 0, \
            'menu width and height must be greater than zero'
        assert selection_highlight_border_width >= 0, \
            'selection lighlight border width must be greater or equal than zero'
        assert selection_highlight_margin_x > 0 and selection_highlight_margin_y > 0, \
            'selection highlight margin must be greater than zero in both axis'
        assert widget_font_size > 0 and title_font_size > 0, \
            'widget font size and title font size must be greater than zero'
        assert widget_margin_y >= 0, \
            'widget margin must be greater or equal than zero'
        assert widget_offset_x >= 0 and widget_offset_y >= 0, 'widget offset must be greater or equal than zero'

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
        assert 0 <= menu_alpha <= 100, \
            'menu alpha must be between 0 and 100 (both values included)'
        assert_alignment(widget_alignment)

        # General properties of the menu
        self._bgcolor = (menu_background_color[0],
                         menu_background_color[1],
                         menu_background_color[2],
                         int(255 * (1 - (100 - menu_alpha) / 100.0))
                         )
        self._bgfun = bgfun
        self._clock = _pygame.time.Clock()  # Inner clock
        self._closelocked = False  # Lock close until next mainloop
        self._dopause = dopause  # Pause or not
        self._enabled = enabled  # Menu is enabled or not
        self._fps = 0  # Updated in set_fps()
        self._height = int(menu_height)
        self._index = 0  # Selected index
        self._joy_event = 0  # type: int
        self._onclose = onclose  # Function that calls after closing menu
        self._sounds = _Sound()  # type: _Sound
        self._surface = surface
        self._width = int(menu_width)

        # Menu links (pointer to previous and next menus in nested submenus)
        self._actual = self  # Actual menu
        self._prev = None  # type: list
        self._top = None  # type: Menu
        self._submenus = []  # type: list

        # Position of menu
        window_width, window_height = _pygame.display.get_surface().get_size()
        self._posx = int((window_width - self._width) / 2)  # type: int
        self._posy = int((window_height - self._height) / 2)  # type: int
        self._bgrect = [(self._posx, self._posy),
                        (self._posx + self._width, self._posy),
                        (self._posx + self._width, self._posy + self._height),
                        (self._posx, self._posy + self._height)
                        ]

        # Menu widgets
        if abs(widget_offset_x) < 1:
            widget_offset_x *= self._width
        if abs(widget_offset_y) < 1:
            widget_offset_y *= self._height
        self._widgets = []  # type: list
        self._widget_alignment = widget_alignment
        self._widget_font_color = widget_font_color
        self._widget_font_name = font
        self._widget_font_size = widget_font_size
        self._widget_margin = widget_margin_y
        self._widget_offset_x = int(widget_offset_x)
        self._widget_offset_y = int(widget_offset_y)
        self._widget_shadow = widget_shadow
        self._widget_shadow_color = widget_shadow_color
        self._widget_shadow_offset = widget_shadow_offset
        self._widget_shadow_position = widget_shadow_position

        # Selected widget
        self._selection_border_width = selection_highlight_border_width * selection_highlight
        self._selection_color = selection_color
        self._selection_highlight = selection_highlight  # Highlight box around selected item
        self._selection_highlight_margin_x = selection_highlight_margin_x * selection_highlight
        self._selection_highlight_margin_y = selection_highlight_margin_y * selection_highlight

        # Columns and rows
        self._columns = columns
        self._column_max_width = column_max_width
        self._column_widths = None  # type: list
        self._force_fit_text = column_force_fit_text
        self._rows = rows

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

        # Create menu bar (title)
        self._menubar = _widgets.MenuBar(label=title,
                                         width=self._width,
                                         back_box=back_box,
                                         bgcolor=self._bgcolor,  # bg_color_title is only used behind text
                                         onchange=None,
                                         onreturn=self._back)
        self._menubar.set_menu(self)
        self._menubar.set_title(title=title,
                                offsetx=title_offset_x,
                                offsety=title_offset_y)
        self._menubar.set_font(font=title_font or font,
                               font_size=title_font_size,
                               color=(title_background_color[0],
                                      title_background_color[1],
                                      title_background_color[2],
                                      int(255 * (1 - (100 - menu_alpha) / 100.0))),
                               selected_color=title_font_color)
        self._menubar.set_shadow(enabled=title_shadow,
                                 color=title_shadow_color,
                                 position=title_shadow_position,
                                 offset=title_shadow_offset)
        self._menubar.set_controls(self._joystick, self._mouse)

        # Scrolling area
        self._widgets_surface = None
        self._scroll = _ScrollArea(area_width=self._width,
                                   area_height=self._height - self._menubar.get_rect().height,
                                   area_color=self._bgcolor,
                                   shadow=self._widget_shadow,
                                   shadow_offset=self._widget_shadow_offset,
                                   shadow_position=self._widget_shadow_position)

        # Set fps
        self.set_fps(fps)

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
            rect = self._widgets[index].get_rect()  # type: _pygame.Rect
            col_index = int(index // self._rows)
            if self._column_max_width[col_index] is None:  # No limit
                self._column_widths[col_index] = max(self._column_widths[col_index],
                                                     rect.width + self._selection_highlight_margin_x,
                                                     # Add selection box
                                                     )

        # If the total weight is less than the window width (so there's no horizontal scroll), scale the columns
        if 0 < sum(self._column_widths) < self._width:
            scale = self._width / sum(self._column_widths)
            for index in range(self._columns):
                self._column_widths[index] *= scale

        # Final column width
        total_col_width = int(sum(self._column_widths))

        if self._columns > 1:

            # Calculate column width scale (weights)
            column_weights = tuple(
                float(self._column_widths[i]) / max(total_col_width, 1.0) for i in range(self._columns))

            # Calculate the position of each column
            self._column_posx = []
            cumulative = 0
            for i in range(self._columns):
                w = column_weights[i]
                self._column_posx.append(int(total_col_width * (cumulative + 0.5 * w)))
                cumulative += w

        else:
            self._column_posx = [int(total_col_width * 0.5)]
            self._column_widths = [total_col_width]

        return total_col_width

    def _get_widget_max_position(self):
        """
        :return: Returns the lower rightmost position of each widgets in menu.
        :rtype: tuple
        """
        max_x = -1e6
        max_y = -1e6
        for index in range(len(self._widgets)):
            x, y = self._get_widget_position(index)[2:]
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        return int(max_x), int(max_y)

    def add_button(self, element_name, element, *args, **kwargs):
        """
        Add button to menu.

        kwargs (Optional):
            - align         Widget alignment
            - button_id     Widget ID
            - font_size     Font size of the widget

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
        button_id = kwargs.pop('button_id', '')
        assert isinstance(button_id, str), 'ID must be a string'

        # If element is a Menu
        if isinstance(element, Menu):
            self._submenus.append(element)
            widget = _widgets.Button(element_name, button_id, None, self._open, element)
        # If element is a PyMenuAction
        elif element == _events.BACK:  # Back to menu
            widget = _widgets.Button(element_name, button_id, None, self.reset, 1)
        elif element == _events.CLOSE:  # Close menu
            widget = _widgets.Button(element_name, button_id, None, self._close, False)
        elif element == _events.EXIT:  # Exit program
            widget = _widgets.Button(element_name, button_id, None, self._exit)
        # If element is a function
        elif isinstance(element, (types.FunctionType, types.MethodType)) or callable(element):
            widget = _widgets.Button(element_name, button_id, None, element, *args)
        else:
            raise ValueError('Element must be a Menu, a PymenuAction or a function')

        # Configure and add the button
        self._configure_widget(widget, kwargs.pop('font_size', self._widget_font_size),
                               kwargs.pop('align', self._widget_alignment))
        self._append_widget(widget)
        return widget

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

    def add_label(self,
                  title,
                  label_id='',
                  align='',
                  font_size=0, ):
        """
        Add a simple text to display.

        :param title: Title of the label
        :type title: basestring
        :param label_id: ID of the label
        :type label_id: basestring
        :param align: Widget alignment
        :type align: basestring
        :param font_size: Font size of the widget
        :type font_size: int
        :return: Widget object
        :rtype: pygameMenu.widgets.label.Label
        """
        widget = _widgets.Label(label=title, label_id=label_id)
        self._configure_widget(widget, font_size, align)
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
        :type align: basestring
        """
        assert isinstance(widget, _widgets.WidgetType), 'widget must be a Widget instance'
        assert isinstance(font_size, int), 'font_size must be an integer'
        assert isinstance(align, str), 'align must be a string'

        if align == '':
            align = self._widget_alignment
        if font_size == 0:
            font_size = self._widget_font_size
        assert font_size > 0, 'font_size must be greater than zero'

        _col = int((len(self._widgets) - 1) // self._rows)  # Column position

        widget.set_menu(self)
        self._check_id_duplicated(widget.get_id())
        widget.set_font(font=self._widget_font_name,
                        font_size=font_size,
                        color=self._widget_font_color,
                        selected_color=self._selection_color)
        if self._force_fit_text and self._column_max_width[_col] is not None:
            selection_dx = self._selection_highlight_margin_x + self._selection_border_width
            widget.set_max_width(self._column_max_width[_col] - selection_dx)
        widget.set_shadow(enabled=self._widget_shadow,
                          color=self._widget_shadow_color,
                          position=self._widget_shadow_position,
                          offset=self._widget_shadow_offset)
        widget.set_controls(self._joystick, self._mouse)
        widget.set_alignment(align)

    def _append_widget(self, widget):
        """
        Add a widget to the list.

        :param widget: Widget object
        :type widget: pygameMenu.widgets.widget.Widget
        """
        assert isinstance(widget, _widgets.WidgetType)
        if self._columns > 1:
            _max_elements = self._columns * self._rows
            _msg = 'total elements cannot be greater than columns*rows ({0} elements)'.format(_max_elements)
            assert len(self._widgets) + 1 <= _max_elements, _msg
        self._widgets.append(widget)
        _totals = len(self._widgets)
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
        self._update_column_width()
        menubar_height = self._menubar.get_rect().height
        max_x, max_y = self._get_widget_max_position()

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
        for widget in self._widgets:
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

    def center_vertically(self):
        """
        Update draw_region_y based on the current widgets.
        If the height of the widgets is greater than the height of the menu, the drawing region will start at zero.
        """
        self._build_widget_surface()
        horizontal_scroll = self._scroll.get_scrollbar_thickness(_locals.ORIENTATION_HORIZONTAL)
        _, max_y = self._get_widget_max_position()
        max_y -= self._widget_offset_y  # Only use total height
        available = self._height - self._menubar.get_rect().height - horizontal_scroll
        new_pos = max((available - max_y) / (2.0 * self._height), 0)  # Percentage of height
        self._widget_offset_y = int(self._height * new_pos)

    def _get_widget_position(self, index, x=True, y=True):
        """
        Get widget position on the surface from a index position.

        :param index: Widget index on the list
        :type index: int
        :param x: Calculate x position
        :type x: bool
        :param y: Calculate y position
        :type y: bool
        :return: Top left, bottom right as a tuple (x1, y1, x2, y2)
        :rtype: tuple
        """
        assert len(self._widgets) > index >= 0, 'index not valid'
        assert isinstance(index, int), 'index must be an integer'
        assert isinstance(x, bool) and isinstance(y, bool), 'x and y must be boolean'

        x_coord = 0
        y_coord = 0
        rect = self._widgets[index].get_rect()  # type: _pygame.Rect

        # Calculate X position
        if x:
            _column_width = self._column_widths[int(index // self._rows)]
            align = self._widgets[index].get_alignment()
            if align == _locals.ALIGN_CENTER:
                dx = -int(rect.width / 2.0)
            elif align == _locals.ALIGN_LEFT:
                dx = -_column_width / 2 + self._selection_highlight_margin_x / 2
            elif align == _locals.ALIGN_RIGHT:
                dx = _column_width / 2 - rect.width - self._selection_highlight_margin_x / 2
            else:
                dx = 0
            x_coord = self._widget_offset_x + self._column_posx[int(index // self._rows)] + dx

        # Calculate Y position
        if y:
            dy = self._selection_highlight_margin_y + self._selection_border_width - self._selection_highlight
            y_coord = self._widget_offset_y + (index % self._rows) * (self._widget_font_size + self._widget_margin) + dy

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

        # Draw widgets
        self._widgets_surface.fill((255, 255, 255, 0))  # Transparent
        for index in range(len(self._widgets)):
            widget = self._widgets[index]

            # Update widget position
            widget.set_position(*self._get_widget_position(index)[:2])

            # Draw widget
            widget.draw(self._widgets_surface)

            # If selected item then draw a rectangle
            if self._selection_highlight and widget.selected:
                widget.draw_selected_rect(self._widgets_surface,
                                          self._selection_color,
                                          self._selection_highlight_margin_x,
                                          self._selection_highlight_margin_y,
                                          self._selection_border_width)

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
        if self._actual._index + self._actual._rows < len(self._actual._widgets):
            self._select(self._actual._index + self._actual._rows)
        else:
            self._select(len(self._actual._widgets) - 1)

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
        elif len(self._actual._widgets) > 0 and self._actual._widgets[self._actual._index].update(events):
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
                    for index in range(len(self._actual._widgets)):
                        widget = self._actual._widgets[index]
                        # Don't considere the mouse wheel (button 4 & 5)
                        if event.button in (1, 2, 3) and \
                                self._actual._scroll.to_real_position(widget.get_rect()).collidepoint(*event.pos):
                            self._select(index)

                elif self._mouse and event.type == _pygame.MOUSEBUTTONUP:
                    self._sounds.play_click_mouse()
                    widget = self._actual._widgets[self._actual._index]
                    # Don't considere the mouse wheel (button 4 & 5)
                    if event.button in (1, 2, 3) and \
                            self._actual._scroll.to_real_position(widget.get_rect()).collidepoint(*event.pos):
                        new_event = _pygame.event.Event(event.type, **event.dict)
                        new_event.dict['origin'] = self._actual._scroll.to_real_position((0, 0))
                        new_event.pos = self._actual._scroll.to_world_position(event.pos)
                        widget.update((new_event,))  # This widget can change the current menu to a submenu
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
        for widget in self._widgets:
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
        for widget in self._widgets:
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
        for widget in self._widgets:
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
        Get actual selected widget.

        :return: Selected widget index
        :rtype: int
        """
        return self._top._actual._index

    def clear(self):
        """
        Full reset menu and clear all widgets.

        :return: None
        """
        self.full_reset()
        del self._actual._widgets[:]
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
        if len(actual._widgets) == 0:
            return
        actual._widgets[actual._index].set_selected(False)
        actual._index = index % len(actual._widgets)
        actual._widgets[actual._index].set_selected()
        rect = actual._widgets[actual._index].get_rect()
        if actual._index == 0:
            # Scroll to the top of the menu
            rect = _pygame.Rect(rect.x, 0, rect.width, rect.height)
        actual._scroll.scroll_to_rect(rect)

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
        for widget in self._widgets:
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
        return self._top._actual._widgets[self._top._actual._index]
