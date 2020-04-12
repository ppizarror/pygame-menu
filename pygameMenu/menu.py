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
import textwrap
import types
from uuid import uuid4

import pygame as _pygame
import pygameMenu.controls as _ctrl
import pygameMenu.events as _events
import pygameMenu.locals as _locals
import pygameMenu.widgets as _widgets

from pygameMenu.scrollarea import ScrollArea as _ScrollArea
from pygameMenu.sound import Sound as _Sound
from pygameMenu.utils import assert_color, assert_position, assert_alignment, make_surface, \
    check_key_pressed_valid

# Joy events
_JOY_EVENT_LEFT = 1
_JOY_EVENT_RIGHT = 2
_JOY_EVENT_UP = 4
_JOY_EVENT_DOWN = 8
_JOY_EVENT_REPEAT = _pygame.NUMEVENTS - 1


class Menu(object):
    """
    Menu object.

    :param menu_height: Height of the Menu (px)
    :type menu_height: int, float
    :param menu_width: Width of the Menu (px)
    :type menu_width: int, float
    :param font: Font file path
    :type font: basestring
    :param title: Title of the Menu (main title)
    :type title: basestring
    :param back_box: Draw a back-box button on header
    :type back_box: bool
    :param column_force_fit_text: Force text fitting of widgets if the width exceeds the column max width
    :type column_force_fit_text: bool
    :param column_max_width: List/Tuple representing the max width of each column in px, None equals no limit
    :type column_max_width: tuple, NoneType
    :param columns: Number of columns, by default it's 1
    :type columns: int
    :param enabled: Menu is enabled by default or not
    :type enabled: bool
    :param joystick_enabled: Enable/disable joystick on the Menu
    :type joystick_enabled: bool
    :param menu_background_color: Menu background color
    :type menu_background_color: tuple, list
    :param mouse_enabled: Enable/disable mouse click inside the Menu
    :type mouse_enabled: bool
    :param menu_id: ID of the Menu
    :type menu_id: basestring
    :param menu_opacity: Opacity of background (0=transparent, 100=opaque)
    :type menu_opacity: int, float
    :param menu_position_x: Left position of the Menu respect to the window (%), if 50 the Menu is horizontally centered
    :type menu_position_x: int, float
    :param menu_position_y: Top position of the Menu respect to the window (%), if 50 the Menu is vertically centered
    :type menu_position_y: int, float
    :param mouse_visible: Set mouse visible on Menu
    :type mouse_visible: bool
    :param onclose: Function applied when closing the Menu
    :type onclose: callable, NoneType
    :param rows: Number of rows of each column, None if there's only 1 column
    :type rows: int, NoneType
    :param scrollbar_color: Scrollbars color
    :type scrollbar_color: tuple, list
    :param scrollbar_shadow: Indicate if a shadow is drawn on each scrollbar
    :type scrollbar_shadow: bool
    :param scrollbar_shadow_color: Color of the shadow
    :type scrollbar_shadow_color: tuple, list
    :param scrollbar_shadow_offset: Offset of shadow
    :type scrollbar_shadow_offset: int, float
    :param scrollbar_shadow_position: Position of shadow
    :type scrollbar_shadow_position: basestring
    :param scrollbar_slider_color: Color of the sliders
    :type scrollbar_slider_color: tuple, list
    :param scrollbar_slider_pad: Space between slider and scrollbars borders
    :type scrollbar_slider_pad: int, float
    :param scrollbar_thick: Scrollbars thickness
    :type scrollbar_thick: int, float
    :param selection_color: Color of selected item
    :type selection_color: tuple, list
    :param selection_highlight: Enable drawing a rectangle around selected item
    :type selection_highlight: bool
    :param selection_highlight_border_width: Border width of the rectangle around selected item
    :type selection_highlight_border_width: int
    :param selection_highlight_margin_x: X margin of selected highlight box
    :type selection_highlight_margin_x: int, float
    :param selection_highlight_margin_y: Y margin of selected highlight box
    :type selection_highlight_margin_y: int, float
    :param title_background_color: Title background color
    :type title_background_color: tuple, list
    :param title_font: Optional title font, if None use the Menu default font
    :type title_font: basestring, NoneType
    :param title_font_color: Title font color, if None use the widget font color
    :type title_font_color: list, tuple, NoneType
    :param title_font_size: Font size of the title
    :type title_font_size: int
    :param title_offset_x: Offset x-position of title (px)
    :type title_offset_x: int, float
    :param title_offset_y: Offset y-position of title (px)
    :type title_offset_y: int, float
    :param title_shadow: Enable shadow on title
    :type title_shadow: bool
    :param title_shadow_color: Title shadow color
    :type title_shadow_color: list, tuple
    :param title_shadow_offset: Offset of shadow on title
    :type title_shadow_offset: int, float
    :param title_shadow_position: Position of the shadow on title
    :type title_shadow_position: basestring
    :param widget_alignment: Widget default alignment
    :type widget_alignment: basestring
    :param widget_font_color: Color of the font
    :type widget_font_color: tuple, list
    :param widget_font_size: Font size
    :type widget_font_size: int
    :param widget_margin_x: Horizontal margin of each element in Menu (px)
    :type widget_margin_x: int, float
    :param widget_margin_y: Vertical margin of each element in Menu (px)
    :type widget_margin_y: int, float
    :param widget_offset_x: X axis offset of widgets inside Menu (px). If value less than 1 use percentage of width
    :type widget_offset_x: int, float
    :param widget_offset_y: Y axis offset of widgets inside Menu (px). If value less than 1 use percentage of height
    :type widget_offset_y: int, float
    :param widget_shadow: Indicate if a shadow is drawn on each widget
    :type widget_shadow: bool
    :param widget_shadow_color: Color of the shadow
    :type widget_shadow_color: tuple, list
    :param widget_shadow_offset: Offset of shadow
    :type widget_shadow_offset: int, float
    :param widget_shadow_position: Position of shadow
    :type widget_shadow_position: basestring
    """

    def __init__(self,
                 menu_height,
                 menu_width,
                 font,
                 title,
                 back_box=True,
                 column_force_fit_text=False,
                 column_max_width=None,
                 columns=1,
                 enabled=True,
                 joystick_enabled=True,
                 menu_opacity=100,
                 menu_background_color=(0, 0, 0),
                 menu_id='',
                 menu_position_x=50,
                 menu_position_y=50,
                 mouse_enabled=True,
                 mouse_visible=True,
                 onclose=None,
                 rows=None,
                 scrollbar_color=(235, 235, 235),
                 scrollbar_shadow=False,
                 scrollbar_shadow_color=(0, 0, 0),
                 scrollbar_shadow_offset=2,
                 scrollbar_shadow_position=_locals.POSITION_SOUTHEAST,
                 scrollbar_slider_color=(200, 200, 200),
                 scrollbar_slider_pad=0,
                 scrollbar_thick=20,
                 selection_color=(180, 180, 180),
                 selection_highlight=True,
                 selection_highlight_border_width=1,
                 selection_highlight_margin_x=16,
                 selection_highlight_margin_y=4,
                 title_background_color=None,
                 title_font=None,
                 title_font_color=None,
                 title_font_size=45,
                 title_offset_x=0,
                 title_offset_y=0,
                 title_shadow=False,
                 title_shadow_color=(0, 0, 0),
                 title_shadow_offset=2,
                 title_shadow_position=_locals.POSITION_NORTHWEST,
                 widget_alignment=_locals.ALIGN_CENTER,
                 widget_font_color=(255, 255, 255),
                 widget_font_size=35,
                 widget_margin_x=0,
                 widget_margin_y=10,
                 widget_offset_x=0,
                 widget_offset_y=0,
                 widget_shadow=False,
                 widget_shadow_color=(0, 0, 0),
                 widget_shadow_offset=2,
                 widget_shadow_position=_locals.POSITION_NORTHWEST,
                 ):
        assert isinstance(menu_height, (int, float))
        assert isinstance(menu_width, (int, float))
        assert isinstance(font, str)
        assert isinstance(back_box, bool)
        assert isinstance(column_force_fit_text, bool)
        assert isinstance(column_max_width, (tuple, type(None), (int, float), list))
        assert isinstance(columns, int)
        assert isinstance(enabled, bool)
        assert isinstance(joystick_enabled, bool)
        assert isinstance(menu_opacity, (int, float))
        assert isinstance(menu_id, str)
        assert isinstance(mouse_enabled, bool)
        assert isinstance(mouse_visible, bool)
        assert isinstance(rows, (int, type(None)))
        assert isinstance(scrollbar_shadow, bool)
        assert isinstance(scrollbar_shadow_offset, (int, float))
        assert isinstance(scrollbar_slider_pad, (int, float))
        assert isinstance(scrollbar_thick, (int, float))
        assert isinstance(selection_highlight, bool)
        assert isinstance(selection_highlight_border_width, int)
        assert isinstance(selection_highlight_margin_x, (int, float))
        assert isinstance(selection_highlight_margin_y, (int, float))
        assert isinstance(title, str)
        assert isinstance(title_font, (str, type(None)))
        assert isinstance(title_font_size, int)
        assert isinstance(title_offset_x, (int, float))
        assert isinstance(title_offset_y, (int, float))
        assert isinstance(title_shadow, bool)
        assert isinstance(title_shadow_offset, (int, float))
        assert isinstance(widget_alignment, str)
        assert isinstance(widget_font_size, int)
        assert isinstance(widget_margin_x, (int, float))
        assert isinstance(widget_margin_y, (int, float))
        assert isinstance(widget_offset_x, (int, float))
        assert isinstance(widget_offset_y, (int, float))
        assert isinstance(widget_shadow, bool)
        assert isinstance(widget_shadow_offset, (int, float))

        # Assert colors
        if title_background_color is None:
            title_background_color = menu_background_color
        if title_font_color is None:
            title_font_color = widget_font_color
        assert_color(menu_background_color)
        assert_color(scrollbar_color)
        assert_color(scrollbar_shadow_color)
        assert_color(scrollbar_slider_color)
        assert_color(selection_color)
        assert_color(title_background_color)
        assert_color(title_font_color)
        assert_color(title_shadow_color)
        assert_color(widget_font_color)
        assert_color(widget_shadow_color)

        # Assert positions
        assert_position(scrollbar_shadow_position)
        assert_position(title_shadow_position)
        assert_position(widget_shadow_position)

        # Column/row asserts
        assert columns >= 1, 'number of columns must be greater or equal than 1'
        if columns > 1:
            assert rows is not None and rows >= 1, 'if columns greater than 1 then rows must be equal or greater than 1'
        else:
            if columns == 1:
                if rows is None:
                    rows = 1e6  # Set rows as a big number
                else:
                    assert rows > 0, 'number of rows must be greater than 1'
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

        # Element size and position asserts
        assert menu_width > 0 and menu_height > 0, \
            'menu width and height must be greater than zero'
        assert scrollbar_thick > 0, 'scrollbar thickness must be greater than zero'
        assert selection_highlight_border_width >= 0, \
            'selection lighlight border width must be greater or equal than zero'
        assert selection_highlight_margin_x >= 0 and selection_highlight_margin_y >= 0, \
            'selection highlight margin must be greater or equal than zero in both axis'
        assert widget_font_size > 0 and title_font_size > 0, \
            'widget font size and title font size must be greater than zero'
        assert widget_offset_x >= 0 and widget_offset_y >= 0, 'widget offset must be greater or equal than zero'

        # Other asserts
        assert 0 <= menu_opacity <= 100, \
            'menu opacity must be between 0 and 100 (both values included)'
        assert_alignment(widget_alignment)

        # Get window size
        window_width, window_height = _pygame.display.get_surface().get_size()
        assert menu_width <= window_width and menu_height <= window_height, \
            'menu size must be lower than the size of the window'

        # Generate ID if empty
        if len(menu_id) == 0:
            menu_id = str(uuid4())

        # Update background color
        menu_opacity = int(255.0 * (1.0 - (100.0 - menu_opacity) / 100.0))
        menu_background_color = (menu_background_color[0],
                                 menu_background_color[1],
                                 menu_background_color[2],
                                 menu_opacity)

        # General properties of the Menu
        self._background_function = None  # type: (None,callable)
        self._clock = _pygame.time.Clock()  # Inner clock
        self._height = float(menu_height)
        self._id = menu_id
        self._index = 0  # Selected index
        self._joy_event = 0  # type: int
        self._onclose = onclose  # Function that calls after closing Menu
        self._sounds = _Sound()  # type: _Sound
        self._submenus = []  # type: list
        self._width = float(menu_width)

        # Menu links (pointer to previous and next menus in nested submenus), for public methods
        # accesing self should be through "_current", because user can move through submenus
        # and self pointer should target the current Menu object. Private methods access
        # through self (not _current) because these methods are called by public (_current) or
        # by themselves. _top is only used when moving through menus (open,reset)
        self._current = self  # Current Menu

        # Prev stores a list of Menu pointers, when accesing a submenu, prev grows as
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
        self.set_relative_position(menu_position_x, menu_position_y, current=False)

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
        self._widget_margin = (widget_margin_x, widget_margin_y)
        self._widget_offset_x = widget_offset_x
        self._widget_offset_y = widget_offset_y
        self._widget_shadow = widget_shadow
        self._widget_shadow_color = widget_shadow_color
        self._widget_shadow_offset = widget_shadow_offset
        self._widget_shadow_position = widget_shadow_position
        self._widget_selected = False  # True if a widget has been selected

        # Selected widget
        self._selection_border_width = selection_highlight_border_width * selection_highlight
        self._selection_color = selection_color
        self._selection_highlight = selection_highlight  # Highlight box around selected item (bool)
        self._selection_highlight_margin_x = selection_highlight_margin_x * selection_highlight
        self._selection_highlight_margin_y = selection_highlight_margin_y * selection_highlight

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
            if not _pygame.joystick.get_init():
                _pygame.joystick.init()
            for i in range(_pygame.joystick.get_count()):
                _pygame.joystick.Joystick(i).init()

        # Init mouse
        self._mouse = mouse_enabled and mouse_visible
        self._mouse_visible = mouse_visible
        self._mouse_visible_default = mouse_visible

        # Create Menu bar (title)
        self._menubar = _widgets.MenuBar(label=title,
                                         width=self._width,
                                         back_box=back_box,
                                         bgcolor=menu_background_color,  # bg_color_title is only used behind text
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
                                      menu_opacity),
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
                                   area_color=menu_background_color,
                                   scrollbar_color=scrollbar_color,
                                   scrollbar_slider_color=scrollbar_slider_color,
                                   scrollbar_slider_pad=scrollbar_slider_pad,
                                   scrollbar_thick=scrollbar_thick,
                                   shadow=scrollbar_shadow,
                                   shadow_color=scrollbar_shadow_color,
                                   shadow_offset=scrollbar_shadow_offset,
                                   shadow_position=scrollbar_shadow_position)

    def add_button(self,
                   title,
                   action,
                   *args,
                   **kwargs):
        """
        Adds a button to the current Menu.

        kwargs (Optional):
            - align         Widget alignment (str)
            - button_id     Widget ID (str)
            - font_size     Font size of the widget (int)
            - margin        Tuple of (x,y) integers

        :param title: Title of the button
        :type title: basestring
        :param action: Action of the button, can be a Menu, an event or a function
        :type action: Menu, PymenuAction, function
        :param args: Additional arguments used by a function
        :param kwargs: Additional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygameMenu.widgets.Button`
        """
        assert isinstance(title, str)

        # Get ID
        button_id = kwargs.pop('button_id', '')
        assert isinstance(button_id, str), 'ID must be a string'

        # If element is a Menu
        onchange = None
        if isinstance(action, Menu):
            self._current._submenus.append(action)
            widget = _widgets.Button(title, button_id, onchange, self._current._open, action)
        # If element is a PyMenuAction
        elif action == _events.BACK:  # Back to Menu
            widget = _widgets.Button(title, button_id, onchange, self.reset,
                                     1)  # reset is public, so no _current
        elif action == _events.RESET:  # Back to Top Menu
            widget = _widgets.Button(title, button_id, onchange, self.full_reset)
        elif action == _events.CLOSE:  # Close Menu
            widget = _widgets.Button(title, button_id, onchange, self._current._close)
        elif action == _events.EXIT:  # Exit program
            widget = _widgets.Button(title, button_id, onchange, self._current._exit)
        elif action == _events.NONE:  # None action
            widget = _widgets.Button(title, button_id)
        # If element is a function
        elif isinstance(action, (types.FunctionType, types.MethodType)) or callable(action):
            widget = _widgets.Button(title, button_id, onchange, action, *args)
        else:
            raise ValueError('Element must be a Menu, a PymenuAction or a function')

        # Configure and add the button
        self._current._configure_widget(widget=widget,
                                        align=kwargs.pop('align', self._current._widget_alignment),
                                        font_size=kwargs.pop('font_size', self._current._widget_font_size),
                                        margin=kwargs.pop('margin', self._current._widget_margin),
                                        )
        self._current._append_widget(widget)
        return widget

    def add_color_input(self,
                        title,
                        color_type,
                        align=None,
                        color_id='',
                        default='',
                        font_size=None,
                        input_separator=',',
                        input_underline='_',
                        margin=None,
                        onchange=None,
                        onreturn=None,
                        previsualization_width=3,
                        **kwargs
                        ):
        """
        Add a color widget with RGB or Hex format to the current Menu.
        Includes a preview box that renders the given color.

        And functions onchange and onreturn does
            onchange(current_text, \*\*kwargs)
            onreturn(current_text, \*\*kwargs)

        :param title: Title of the color input
        :type title: basestring
        :param color_type: Type of the color input, can be "rgb" or "hex"
        :type color_type: basestring
        :param align: Widget alignment, if None use default Menu widget alignment
        :type align: basestring, NoneType
        :param color_id: ID of the color input
        :type color_id: basestring
        :param default: Default value to display, if RGB must be a tuple (r,g,b), if HEX must be a string "#XXXXXX"
        :type default: basestring, tuple
        :param font_size: Font size of the widget, if None use default Menu widget font size
        :type font_size: int, NoneType
        :param input_separator: Divisor between RGB channels, not valid in HEX format
        :type input_separator: basestring
        :param input_underline: Underline character
        :type input_underline: basestring
        :param margin: Margin of the widget, tuple of (x,y) of integers, if None use default widget margin
        :type margin: tuple, NoneType
        :param onchange: Function when changing the selector
        :type onchange: callable, NoneType
        :param onreturn: Function when pressing return button
        :type onreturn: callable, NoneType
        :param previsualization_width: Previsualization width as a factor of the height
        :type previsualization_width: int, float
        :param kwargs: Additional keyword-parameters
        :return: Widget object
        :rtype: :py:class:`pygameMenu.widgets.ColorInput`
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
        self._current._configure_widget(widget=widget, align=align, font_size=font_size, margin=margin)
        widget.set_value(default)
        self._current._append_widget(widget)
        return widget

    def add_label(self,
                  title,
                  align=None,
                  font_size=None,
                  label_id='',
                  max_char=0,
                  margin=None,
                  ):
        """
        Add a simple text to the current Menu.

        :param title: Text to be displayed
        :type title: basestring
        :param label_id: ID of the label
        :type label_id: basestring
        :param align: Widget alignment, if None use default Menu widget alignment
        :type align: basestring, NoneType
        :param font_size: Font size of the text, if None use default widget font size
        :type font_size: int, NoneType
        :param max_char: If text length exeeds this limit then split the text and add another label, if 0 there's no limit
        :type max_char: int
        :param margin: Margin of the widget, tuple of (x,y) of integers, if None use default widget margin
        :type margin: tuple, NoneType
        :return: Widget object or List of widgets if the text overflows
        :rtype: :py:class:`pygameMenu.widgets.Label`, list[:py:class:`pygameMenu.widgets.Label`]
        """
        assert isinstance(label_id, str)
        assert isinstance(max_char, int)
        assert max_char >= 0, 'max characters cannot be negative'
        if len(label_id) == 0:
            label_id = str(uuid4())  # If wrap

        # If no overflow
        if len(title) <= max_char or max_char == 0:
            widget = _widgets.Label(label=title, label_id=label_id)
            self._current._configure_widget(widget=widget, align=align, font_size=font_size, margin=margin)
            self._current._append_widget(widget)
        else:
            self._current._check_id_duplicated(label_id)  # Before adding + LEN
            widget = []
            for line in textwrap.wrap(title, max_char):
                widget.append(self.add_label(title=line,
                                             align=align,
                                             font_size=font_size,
                                             label_id=label_id + '+' + str(len(widget) + 1),
                                             max_char=max_char,
                                             margin=margin))
        return widget

    def add_selector(self,
                     title,
                     items,
                     align=None,
                     default=0,
                     font_size=None,
                     margin=None,
                     onchange=None,
                     onreturn=None,
                     selector_id='',
                     **kwargs
                     ):
        """
        Add a selector to the current Menu: several items with values and
        two functions that are executed when changing the selector (left/right)
        and pressing return button on the selected item.

        Values of the selector are like:
            values = [('Item1', a, b, c...), ('Item2', a, b, c..)]

        And functions onchange and onreturn does
            onchange(a, b, c..., \*\*kwargs)
            onreturn(a, b, c..., \*\*kwargs)

        :param title: Title of the selector
        :type title: basestring
        :param items: Elements of the selector [('Item1', var1..), ('Item2'...)]
        :type items: list
        :param align: Widget alignment, if None use default Menu widget alignment
        :type align: basestring, NoneType
        :param default: Index of default value to display
        :type default: int
        :param font_size: Font size of the widget, if None use the default Menu widget font size
        :type font_size: int, NoneType
        :param margin: Margin of the widget, tuple of (x,y) of integers, if None use default widget margin
        :type margin: tuple, NoneType
        :param onchange: Function when changing the selector
        :type onchange: callable, NoneType
        :param onreturn: Function when pressing return button
        :type onreturn: callable, NoneType
        :param selector_id: ID of the selector
        :type selector_id: basestring
        :param kwargs: Additional parameters
        :return: Widget object
        :rtype: :py:class:`pygameMenu.widgets.Selector`
        """
        widget = _widgets.Selector(label=title,
                                   elements=items,
                                   selector_id=selector_id,
                                   default=default,
                                   onchange=onchange,
                                   onreturn=onreturn,
                                   **kwargs)
        self._current._configure_widget(widget=widget, align=align, font_size=font_size, margin=margin)
        self._current._append_widget(widget)
        return widget

    def add_text_input(self,
                       title,
                       align=None,
                       default='',
                       enable_copy_paste=True,
                       enable_selection=True,
                       font_size=None,
                       input_type=_locals.INPUT_TEXT,
                       input_underline='',
                       margin=None,
                       maxchar=0,
                       maxwidth=0,
                       onchange=None,
                       onreturn=None,
                       password=False,
                       textinput_id='',
                       valid_chars=None,
                       **kwargs
                       ):
        """
        Add a text input to the current Menu: free text area and two functions
        that execute when changing the text and pressing return button
        on the element.

        And functions onchange and onreturn does
            onchange(current_text, \*\*kwargs)
            onreturn(current_text, \*\*kwargs)

        :param title: Title of the text input
        :type title: basestring
        :param align: Widget alignment, if None use default Menu widget alignment
        :type align: basestring, NoneType
        :param default: Default value to display
        :type default: basestring, int, float
        :param enable_copy_paste: Enable text copy, paste and cut
        :type enable_copy_paste: bool
        :param enable_selection: Enable text selection on input
        :type enable_selection: bool
        :param font_size: Font size of the widget, if None use the default Menu widget font size
        :type font_size: int
        :param input_type: Data type of the input
        :type input_type: basestring
        :param input_underline: Underline character
        :type input_underline: basestring
        :param margin: Margin of the widget, tuple of (x,y) of integers, if None use default widget margin
        :type margin: tuple, NoneType
        :param maxchar: Maximum length of string, if 0 there's no limit
        :type maxchar: int
        :param maxwidth: Maximum size of the text widget, if 0 there's no limit
        :type maxwidth: int
        :param onchange: Function when changing the selector
        :type onchange: callable, NoneType
        :param onreturn: Function when pressing return button
        :type onreturn: callable, NoneType
        :param password: Text input is a password
        :type password: bool
        :param textinput_id: ID of the text input
        :type textinput_id: basestring
        :param valid_chars: List of chars to be ignored, None if no chars are invalid
        :type valid_chars: list
        :param kwargs: Additional keyword-parameters
        :return: Widget object
        :rtype: :py:class:`pygameMenu.widgets.TextInput`
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
        self._current._configure_widget(widget=widget, align=align, font_size=font_size, margin=margin)
        widget.set_value(default)
        self._current._append_widget(widget)
        return widget

    def add_vertical_margin(self, margin):
        """
        Adds a vertical margin to the current Menu.

        :param margin: Margin in px
        :type margin: int, float
        :return: Widget object
        :rtype: :py:class:`pygameMenu.widgets.VMargin`
        """
        assert isinstance(margin, (int, float))
        widget = _widgets.VMargin()
        self._current._configure_widget(widget=widget, margin=(0, margin))
        self._current._append_widget(widget)
        return widget

    def _configure_widget(self, widget, align=None, font_size=None, margin=None):
        """
        Update the given widget with the parameters defined at
        the Menu level.

        :param widget: Widget object
        :type widget: :py:class:`pygameMenu.widgets.widget.Widget`
        :param align: Widget alignment, if None use default Menu widget alignment
        :type align: basestring, NoneType
        :param font_size: Widget font size, if None use the default Menu widget font size
        :type font_size: int, NoneType
        :param margin: Widget vertical margin, if None the default Menu widget vertical margin
        :type margin: tuple, NoneType
        """
        assert isinstance(widget, _widgets.WidgetType)
        assert isinstance(align, (str, type(None)))
        assert isinstance(font_size, (int, type(None)))
        assert isinstance(margin, (tuple, type(None)))

        if align is None or align == '':
            align = self._widget_alignment
        if font_size is None or font_size == 0:
            font_size = self._widget_font_size
        assert font_size > 0, 'font_size must be greater than zero'
        if margin is None:
            margin = self._widget_margin
        else:
            assert len(margin) == 2, 'margin must be a tuple of 2 elements'

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
        widget.set_margin(margin[0], margin[1])

    def _append_widget(self, widget):
        """
        Add a widget to the list.

        :param widget: Widget object
        :type widget: :py:class:`pygameMenu.widgets.widget.Widget`
        """
        assert isinstance(widget, _widgets.WidgetType)
        if self._columns > 1:
            _max_elements = self._columns * self._rows
            _msg = 'total widgets cannot be greater than columns*rows ({0} elements)'.format(_max_elements)
            assert len(self._widgets) + 1 <= _max_elements, _msg
        self._widgets.append(widget)
        if not self._widget_selected and widget.is_selectable:
            widget.set_selected()
            self._widget_selected = True
            self._index = len(self._widgets) - 1
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
            rect = self._widgets[index].get_rect()  # type: _pygame.Rect
            col_index = int(index // self._rows)
            if self._column_max_width[col_index] is None:  # No limit
                self._column_widths[col_index] = max(self._column_widths[col_index],
                                                     rect.width + self._selection_highlight_margin_x,
                                                     # Add selection box
                                                     )

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
        if self._column_widths is None:
            self._update_column_width()

        # Update title position
        self._menubar.set_position(self._pos_x, self._pos_y)

        # Update appended widgets
        for index in range(len(self._widgets)):
            widget = self._widgets[index]  # type: _widgets.WidgetType
            rect = widget.get_rect()  # type: _pygame.Rect

            # Get column and row position
            _col = int(index // self._rows)
            _row = int(index % self._rows)

            # Calculate X position
            _column_width = self._column_widths[_col]
            _highlist_margin = float(self._selection_highlight_margin_x + self._selection_border_width) / 2
            align = widget.get_alignment()
            if align == _locals.ALIGN_CENTER:
                dx = -float(rect.width) / 2
            elif align == _locals.ALIGN_LEFT:
                dx = -_column_width / 2 + _highlist_margin
            elif align == _locals.ALIGN_RIGHT:
                dx = _column_width / 2 - rect.width - _highlist_margin
            else:
                dx = 0
            x_coord = self._column_pos_x[_col] + dx + widget.get_margin()[0]
            x_coord = max(_highlist_margin, x_coord)
            x_coord += self._widget_offset_x

            # Calculate Y position
            ysum = 0  # Compute the total height from the current row position to the top of the column
            for r in range(_row):
                rwidget = self._widgets[int(self._rows * _col + r)]  # type: _widgets.WidgetType
                ysum += rwidget.get_rect().height + rwidget.get_margin()[1]
            dy = self._selection_highlight_margin_y + self._selection_border_width - self._selection_highlight
            y_coord = self._widget_offset_y + ysum + dy

            # Update the position of the widget
            widget.set_position(x_coord, y_coord)

    def _get_widget_max_position(self):
        """
        :return: Returns the lower rightmost position of each widgets in Menu.
        :rtype: tuple
        """
        max_x = -1e6
        max_y = -1e6
        for widget in self._widgets:  # type: _widgets.WidgetType
            _, _, x, y = widget.get_position()  # Use only bottom right position
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
        elif max_y > self._height:
            # Remove the thick of the scrollbar
            # to avoid displaying an horizontal one
            width, height = self._width - 20, max_y + 20
            if not self._mouse_visible:
                self._mouse_visible = True
        else:
            width, height = self._width, self._height - menubar_height
            self._mouse_visible = self._mouse_visible_default

        self._widgets_surface = make_surface(width, height)
        self._scroll.set_world(self._widgets_surface)
        self._scroll.set_position(self._pos_x, self._pos_y + menubar_height + 5)

    def _check_id_duplicated(self, widget_id):
        """
        Check if widget ID is duplicated.

        :param widget_id: New widget ID
        :type widget_id: basestring
        :return: None
        """
        for widget in self._widgets:  # type: _widgets.WidgetType
            if widget.get_id() == widget_id:
                raise ValueError('The widget ID="{0}" is duplicated'.format(widget_id))

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
            a = isinstance(onclose, _events.PymenuAction)
            b = str(type(onclose)) == "<class 'pygameMenu.events.PymenuAction'>"  # python compatibility
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
        Find Menu depth.

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

    def disable(self):
        """
        Disables the Menu (doesn't check events and draw on the surface).

        :return: None
        """
        self._top._enabled = False

    def set_relative_position(self, position_x, position_y, current=True):
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
        :param current: If true, centers the current active Menu, otherwise center the base Menu
        :type current: bool
        :return: None
        """
        assert isinstance(position_x, (int, float))
        assert isinstance(position_y, (int, float))
        assert 0 <= position_x <= 100
        assert 0 <= position_y <= 100
        isinstance(current, bool)

        position_x = float(position_x) / 100
        position_y = float(position_y) / 100
        window_width, window_height = _pygame.display.get_surface().get_size()
        if current:
            self._current._pos_x = (window_width - self._current._width) * position_x
            self._current._pos_y = (window_height - self._current._height) * position_y
        else:
            self._pos_x = (window_width - self._width) * position_x
            self._pos_y = (window_height - self._height) * position_y
        self._widgets_surface = None  # This forces an update of the widgets

    def center_content(self, current=True):
        """
        Update draw_region_y based on the current widgets, centering the content
        of the window.

        If the height of the widgets is greater than the height of the Menu,
        the drawing region will start at zero, using all the height for the scrollbar.

        :param current: If true, centers the current active Menu, otherwise center the base Menu
        :type current: bool
        :return: None
        """
        isinstance(current, bool)
        if current:
            self._current._center_content()
        else:
            self._center_content()

    def _center_content(self):
        """
        Update draw_region_y based on the current widgets.
        If the height of the widgets is greater than the height of the Menu,
        the drawing region will start at zero.

        :return: None
        """
        self._build_widget_surface()
        horizontal_scroll = self._scroll.get_scrollbar_thickness(_locals.ORIENTATION_HORIZONTAL)
        _, max_y = self._get_widget_max_position()
        max_y -= self._widget_offset_y  # Only use total height
        available = self._height - self._menubar.get_rect().height - horizontal_scroll
        new_pos = max((available - max_y) / (2.0 * self._height), 0)  # Percentage of height
        self._widget_offset_y = self._height * new_pos
        self._build_widget_surface()  # Rebuild

    def draw(self, surface):
        """
        Draw the current Menu into the given surface.

        :param surface: Pygame surface to draw the Menu
        :type surface: pygame.surface.SurfaceType
        :return: None
        """
        if not self.is_enabled():
            raise RuntimeError('Menu is not enabled, it cannot be drawn')

        # The surface may has been erased because the number
        # of widgets has changed and thus size shall be calculated.
        if not self._current._widgets_surface:
            self._current._build_widget_surface()

        # Fill the surface with background function (setted from mainloop)
        if self._top._background_function is not None:
            self._top._background_function()

        # Fill the scrolling surface
        self._current._widgets_surface.fill((255, 255, 255, 0))

        # Draw widgets
        for widget in self._current._widgets:  # type: _widgets.WidgetType
            widget.draw(self._current._widgets_surface)
            if self._current._selection_highlight and widget.selected:  # If selected draw a rectangle
                widget.draw_selected_rect(self._current._widgets_surface,
                                          self._current._selection_color,
                                          self._current._selection_highlight_margin_x,
                                          self._current._selection_highlight_margin_y,
                                          self._current._selection_border_width)

        self._current._scroll.draw(surface)
        self._current._menubar.draw(surface)

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
        _pygame.quit()
        sys.exit()

    def is_enabled(self):
        """
        Returns True if Menu is enabled else False is returned.

        :return: True if the Menu is enabled
        :rtype: bool
        """
        return self._top._enabled

    def _left(self):
        """
        Left event (column support).
        """
        if self._index >= self._rows:
            self._select(self._index - self._rows)
        else:
            self._select(0)

    def _right(self):
        """
        Right event (column support).
        """
        if self._index + self._rows < len(self._widgets):
            self._select(self._index + self._rows)
        else:
            self._select(len(self._widgets) - 1)

    def _handle_joy_event(self):
        """
        Handle joy events.
        """
        if self._joy_event & _JOY_EVENT_UP:
            self._select(self._index - 1)
        if self._joy_event & _JOY_EVENT_DOWN:
            self._select(self._index + 1)
        if self._joy_event & _JOY_EVENT_LEFT:
            self._left()
        if self._joy_event & _JOY_EVENT_RIGHT:
            self._right()

    def update(self, events):
        """
        Update the status of the Menu using external events.
        The update event is applied only on the current Menu.

        :param events: Pygame events as a list
        :type events: list
        :return: True if mainloop must be stopped
        :rtype: bool
        """
        assert isinstance(events, list)

        # If any widget status changes, set the status as True
        updated = False

        # Update mouse
        _pygame.mouse.set_visible(self._current._mouse_visible)

        # Surface needs an update
        menu_surface_needs_update = False

        # Update scroll bars
        was_scrolling = self._current._scroll.is_scrolling()
        if self._current._scroll.update(events):
            updated = True

        # If scrolling is ending, no action on any other elements
        if was_scrolling and not self._current._scroll.is_scrolling():
            return updated

        # Update the menubar, it may change the status of the widget because
        # of the button back/close
        if self._current._menubar.update(events):
            updated = True

        # Check selected widget
        elif len(self._current._widgets) > 0 and self._current._widgets[self._current._index].update(events):
            updated = True

        # Check others
        else:

            for event in events:  # type: _pygame.event.EventType

                # noinspection PyUnresolvedReferences
                if event.type == _pygame.locals.QUIT or (
                        event.type == _pygame.KEYDOWN and event.key == _pygame.K_F4 and (
                        event.mod == _pygame.KMOD_LALT or event.mod == _pygame.KMOD_RALT)):
                    self._current._exit()
                    updated = True

                elif event.type == _pygame.locals.KEYDOWN:

                    # Check key event is valid
                    if not check_key_pressed_valid(event):
                        continue

                    if event.key == _ctrl.KEY_MOVE_DOWN:
                        self._current._select(self._current._index - 1)
                        self._current._sounds.play_key_add()
                    elif event.key == _ctrl.KEY_MOVE_UP:
                        self._current._select(self._current._index + 1)
                        self._current._sounds.play_key_add()
                    elif event.key == _ctrl.KEY_LEFT and self._current._columns > 1:
                        self._current._left()
                        self._current._sounds.play_key_add()
                    elif event.key == _ctrl.KEY_RIGHT and self._current._columns > 1:
                        self._current._right()
                        self._current._sounds.play_key_add()
                    elif event.key == _ctrl.KEY_BACK and self._top._prev is not None:
                        self._current._sounds.play_close_menu()
                        self.reset(1)  # public, do not use _current
                    elif event.key == _ctrl.KEY_CLOSE_MENU:
                        self._current._sounds.play_close_menu()
                        if self._current._close():
                            updated = True

                elif self._current._joystick and event.type == _pygame.JOYHATMOTION:
                    if event.value == _ctrl.JOY_UP:
                        self._current._select(self._current._index - 1)
                    elif event.value == _ctrl.JOY_DOWN:
                        self._current._select(self._current._index + 1)
                    elif event.value == _ctrl.JOY_LEFT and self._columns > 1:
                        self._current._select(self._current._index - 1)
                    elif event.value == _ctrl.JOY_RIGHT and self._columns > 1:
                        self._current._select(self._current._index + 1)

                elif self._current._joystick and event.type == _pygame.JOYAXISMOTION:
                    prev = self._current._joy_event
                    self._current._joy_event = 0
                    if event.axis == _ctrl.JOY_AXIS_Y and event.value < -_ctrl.JOY_DEADZONE:
                        self._current._joy_event |= _JOY_EVENT_UP
                    if event.axis == _ctrl.JOY_AXIS_Y and event.value > _ctrl.JOY_DEADZONE:
                        self._current._joy_event |= _JOY_EVENT_DOWN
                    if event.axis == _ctrl.JOY_AXIS_X and event.value < -_ctrl.JOY_DEADZONE and self._columns > 1:
                        self._current._joy_event |= _JOY_EVENT_LEFT
                    if event.axis == _ctrl.JOY_AXIS_X and event.value > _ctrl.JOY_DEADZONE and self._columns > 1:
                        self._current._joy_event |= _JOY_EVENT_RIGHT
                    if self._current._joy_event:
                        self._current._handle_joy_event()
                        if self._current._joy_event == prev:
                            _pygame.time.set_timer(_JOY_EVENT_REPEAT, _ctrl.JOY_REPEAT)
                        else:
                            _pygame.time.set_timer(_JOY_EVENT_REPEAT, _ctrl.JOY_DELAY)
                    else:
                        _pygame.time.set_timer(_JOY_EVENT_REPEAT, 0)

                elif event.type == _JOY_EVENT_REPEAT:
                    if self._current._joy_event:
                        self._current._handle_joy_event()
                        _pygame.time.set_timer(_JOY_EVENT_REPEAT, _ctrl.JOY_REPEAT)
                    else:
                        _pygame.time.set_timer(_JOY_EVENT_REPEAT, 0)

                elif self._current._mouse and event.type == _pygame.MOUSEBUTTONDOWN:
                    for index in range(len(self._current._widgets)):
                        widget = self._current._widgets[index]
                        # Don't considere the mouse wheel (button 4 & 5)
                        if event.button in (1, 2, 3) and \
                                self._current._scroll.to_real_position(widget.get_rect()).collidepoint(*event.pos):
                            self._current._select(index)

                elif self._current._mouse and event.type == _pygame.MOUSEBUTTONUP:
                    self._current._sounds.play_click_mouse()
                    widget = self._current._widgets[self._current._index]
                    # Don't considere the mouse wheel (button 4 & 5)
                    if event.button in (1, 2, 3) and \
                            self._current._scroll.to_real_position(widget.get_rect()).collidepoint(*event.pos):
                        new_event = _pygame.event.Event(event.type, **event.dict)
                        new_event.dict['origin'] = self._current._scroll.to_real_position((0, 0))
                        new_event.pos = self._current._scroll.to_world_position(event.pos)
                        widget.update((new_event,))  # This widget can change the current Menu to a submenu
                        menu_surface_needs_update = menu_surface_needs_update or widget.surface_needs_update()
                        updated = True  # It is updated
                        break

        # Check if the position has changed
        if len(self._current._widgets) > 0:
            menu_surface_needs_update = menu_surface_needs_update or self._current._widgets[
                self._current._index].surface_needs_update()

        # This forces the rendering of all widgets
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

            menu = pygameMenu.Menu(...)

            menu.mainloop(surface)

        :param surface: Pygame surface to draw the Menu
        :type surface: pygame.surface.SurfaceType
        :param bgfun: Background function called on each loop iteration before drawing the Menu
        :type bgfun: callable
        :param disable_loop: If true run this method for only 1 loop
        :type disable_loop: bool
        :param fps_limit: Limit frame per second of the loop, if 0 there's no limit
        :type fps_limit: int, float
        :return: None
        """
        assert isinstance(surface, _pygame.Surface)
        if bgfun:
            assert callable(bgfun), 'background function must be callable (a function)'
        assert isinstance(disable_loop, bool)
        assert isinstance(fps_limit, (int, float))
        assert fps_limit >= 0, 'fps limit cannot be negative'

        # NOTE: For Menu accesor, use only _current, as the Menu pointer can change through the execution
        if not self.is_enabled():
            return

        self._background_function = bgfun

        while True:
            self._current._clock.tick(fps_limit)

            # If loop, gather events by Menu and draw the background function, if this method
            # returns true then the mainloop will break
            self.update(_pygame.event.get())

            # As event can change the status of the Menu, this has to be checked twice
            if self.is_enabled():
                self.draw(surface=surface)

            _pygame.display.flip()

            if not self.is_enabled() or disable_loop:
                self._background_function = None
                return

    def get_input_data(self, recursive=False, current=True):
        """
        Return input data from a Menu. The results are given as a dict object.
        The keys are the ID of each element.

        With ``recursive=True``: it collect also data inside the all sub-menus.

        :param recursive: Look in Menu and sub-menus
        :type recursive: bool
        :param current: If True, returns the value from the current active Menu, otherwise from the base Menu
        :type current: bool
        :return: Input dict e.g.: {'id1': value, 'id2': value, ...}
        :rtype: dict
        """
        assert isinstance(recursive, bool)
        assert isinstance(current, bool)
        if current:
            return self._current._get_input_data(recursive, depth=0)
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
        for widget in self._widgets:  # type: _widgets.WidgetType
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
                        msg = 'Collision between widget data ID="{0}" at depth={1}'.format(key, depth)
                        raise ValueError(msg)

                # Update data
                data.update(data_submenu)
        return data

    def get_rect(self, current=True):
        """
        Return Menu pygame Rect.

        :param current: If True, returns the value from the current active Menu, otherwise from the base Menu
        :type current: bool
        :return: Rect
        :rtype: pygame.rect.RectType
        """
        if current:
            return _pygame.Rect(self._current._pos_x, self._current._pos_y,
                                self._current._width, self._current._height)
        return _pygame.Rect(self._pos_x, self._pos_y, self._width, self._height)

    def set_sound(self, sound, recursive=False):
        """
        Add a sound engine to the Menu. If ``recursive=True``, the sound is
        applied to all submenus.

        The sound is applied only to the base Menu (not the currently displayed).

        :param sound: Sound object
        :type sound: :py:class:`pygameMenu.sound.Sound`, NoneType
        :param recursive: Set the sound engine to all submenus
        :type recursive: bool
        :return: None
        """
        assert isinstance(sound, (type(self._sounds), type(None)))
        if sound is None:
            sound = _Sound()
        self._sounds = sound
        for widget in self._widgets:  # type: _widgets.WidgetType
            widget.set_sound(sound)
        if recursive:
            for menu in self._submenus:  # type: Menu
                menu.set_sound(sound, recursive=True)

    def get_title(self, current=True):
        """
        Return title of the Menu.

        :param current: If True, return the title of currently displayed Menu
        :type current: bool
        :return: Title
        :rtype: basestring
        """
        if current:
            return self._current._menubar.get_title()
        return self._menubar.get_title()

    def full_reset(self, current=True):
        """
        Reset the Menu back to the first opened Menu.

        :param current: If True, reset from current Menu, otherwise reset from base Menu
        :type current: bool
        :return: None
        """
        if current:
            depth = self._current._get_depth()
        else:
            depth = self._get_depth()
        if depth > 0:
            self.reset(depth)  # public, do not use _current

    def clear(self, current=True):
        """
        Full reset Menu and clear all widgets.

        :param current: If True, clear from current active Menu, otherwise clears base Menu
        :type current: bool
        :return: None
        """
        assert isinstance(current, bool)
        self.full_reset(current=current)  # public, do not use _current
        if current:
            del self._current._widgets[:]
            del self._current._submenus[:]
        else:
            del self._widgets[:]
            del self._submenus[:]

    def _open(self, menu):
        """
        Open the given Menu.

        :param menu: Menu object
        :type menu: Menu
        :return: None
        """
        current = self

        # Update pointers
        menu._top = self._top
        self._top._current = menu._current
        self._top._prev = [self._top._prev, current]

        # Select the first widget
        self._select(0)

    def reset(self, total):
        """
        Go back in Menu history a certain number of times from the current Menu.

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

    def _select(self, new_index):
        """
        Select the widget at the given index and unselect others.
        Selection forces rendering of the widget.

        :param new_index: Widget index
        :type new_index: int
        :return: None
        """
        current = self._top._current
        if len(current._widgets) == 0:
            return

        # This stores +/-1 if the index increases or decreases
        # Used by non-selectable selection
        if new_index < current._index:
            dwidget = -1
        else:
            dwidget = 1

        # Limit the index to the length
        new_index %= len(current._widgets)
        if new_index == current._index:  # Index has not changed
            return

        # Get both widgets
        old_widget = current._widgets[current._index]  # type: _widgets.WidgetType
        new_widget = current._widgets[new_index]  # type:_widgets.WidgetType

        # If new widget is not selectable
        if not new_widget.is_selectable:
            if current._widget_selected:  # There's at least 1 selectable option (if only text this would be false)
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
            rect = _pygame.Rect(rect.x, 0, rect.width, rect.height)
        current._scroll.scroll_to_rect(rect)

    def get_id(self, current=True):
        """
        Returns the ID of the Menu.

        :param current: If True, returns the value from the current active Menu, otherwise returns from the base Menu
        :type current: bool
        :return: Menu ID
        :rtype: basestring
        """
        assert isinstance(current, bool)
        if current:
            return self._current._id
        return self._id

    def get_widget(self, widget_id, recursive=False, current=True):
        """
        Return a widget by a given ID.

        With ``recursive=True``: it looks for a widget in the Menu
        and all sub-menus. Use ``current`` for getting from current and
        base Menu.

        None is returned if no widget found.

        :param widget_id: Widget ID
        :type widget_id: basestring
        :param recursive: Look in Menu and submenus
        :type recursive: bool
        :param current: If True, returns the value from the current active Menu, otherwise from the base Menu
        :type current: bool
        :return: Widget object
        :rtype: :py:class:`pygameMenu.widgets.widget.Widget`
        """
        assert isinstance(widget_id, str)
        assert isinstance(recursive, bool)
        assert isinstance(current, bool)
        if current:
            return self._current._get_widget(widget_id, recursive)
        return self._get_widget(widget_id, recursive)

    def _get_widget(self, widget_id, recursive):
        """
        Return a widget by a given ID.

        With ``recursive=True``: it looks for a widget in the Menu
        and all sub-menus. Use ``current`` for getting from current and
        base Menu.

        None is returned if no widget found.

        :param widget_id: Widget ID
        :type widget_id: basestring
        :param recursive: Look in Menu and submenus
        :type recursive: bool
        :return: Widget object
        :rtype: :py:class:`pygameMenu.widgets.widget.Widget`
        """
        for widget in self._widgets:  # type: _widgets.WidgetType
            if widget.get_id() == widget_id:
                return widget
        if recursive:
            for menu in self._submenus:  # type: Menu
                widget = menu.get_widget(widget_id, recursive)
                if widget:
                    return widget
        return None

    def get_index(self, current=True):
        """
        Get selected widget from the current Menu.

        :param current: If True, returns the value from the current active Menu, otherwise returns from the base Menu
        :type current: bool
        :return: Selected widget index
        :rtype: int
        """
        assert isinstance(current, bool)
        if current:
            return self._current._index
        return self._index

    def get_selected_widget(self, current=True):
        """
        Return the currently selected widget.

        :param current: If True, returns the value from the current active Menu, otherwise from the base Menu
        :type current: bool
        :return: Widget object
        :rtype: :py:class:`pygameMenu.widgets.widget.Widget`
        """
        assert isinstance(current, bool)
        if current:
            return self._current._widgets[self._current._index]
        return self._widgets[self._index]
