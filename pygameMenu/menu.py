# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

MENU
Menu class.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2019 Pablo Pizarro R. @ppizarror

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

# Library imports
from sys import exit
import pygame as _pygame
import pygame.gfxdraw as _gfxdraw
import types

from pygameMenu.sound import Sound as _Sound
import pygameMenu.config as _cfg
import pygameMenu.controls as _ctrl
import pygameMenu.events as _events
import pygameMenu.font as _fonts
import pygameMenu.locals as _locals
import pygameMenu.widgets as _widgets


# noinspection PyArgumentEqualDefault,PyProtectedMember,PyTypeChecker,PyUnresolvedReferences
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
                 widget_alignment=_locals.ALIGN_CENTER
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

        # Other asserts
        if dopause:
            assert callable(bgfun), \
                'Bgfun must be a function (or None if menu does not pause ' \
                'execution of the application)'
        else:
            assert isinstance(bgfun, type(None)), \
                'Bgfun must be None if menu does not pause execution of the application'
        assert dopause and bgfun is not None or not dopause and bgfun is None, \
            'If pause main execution is enabled then bgfun (Background ' \
            'function drawing) must be defined (not None)'
        assert draw_region_y >= 0 and draw_region_x >= 0, \
            'Drawing regions must be greater or equal than zero'
        assert font_size > 0 and font_size_title > 0, \
            'Font sizes must be greater than zero'
        assert menu_width > 0 and menu_height > 0, \
            'Menu size must be greater than zero'
        assert 0 <= menu_alpha <= 100, \
            'menu_alpha must be between 0 and 100 (both values included)'
        assert option_margin >= 0, \
            'Option margin must be greater or equal than zero'
        assert rect_width >= 0, 'rect_width must be greater or equal than zero'
        assert window_height > 0 and window_width > 0, \
            'Window size must be greater than zero'

        # Store configuration
        self._bgfun = bgfun
        self._bgcolor = (menu_color[0], menu_color[1], menu_color[2],
                         int(255 * (1 - (100 - menu_alpha) / 100.0)))

        self._drawselrect = draw_select
        self._font_color = font_color
        self._fsize = font_size
        self._height = menu_height
        self._opt_dy = option_margin
        self._option_shadow = option_shadow
        self._option_shadow_offset = option_shadow_offset
        self._option_shadow_position = option_shadow_position
        self._rect_width = rect_width
        self._sel_color = color_selected
        self._surface = surface
        self._width = menu_width

        # Inner variables
        self._actual = self  # Actual menu
        self._clock = _pygame.time.Clock()  # Inner clock
        self._closelocked = False  # Lock close until next mainloop
        self._dopause = dopause  # Pause or not
        self._enabled = enabled  # Menu is enabled or not
        self._fps = 0
        self._frame = 0
        self._index = 0  # Selected index
        self._onclose = onclose  # Function that calls after closing menu
        self._size = 0  # Menu total elements
        self._sounds = _Sound()

        # Menu widgets
        self._option = []  # type: list[_widgets.WidgetType]

        # Previous menu
        self._prev = None  # type: list[Menu]

        # Top level menu
        self._top = None  # type: Menu

        # List of all linked menus
        self._submenus = []  # type: list[Menu]

        # Load fonts
        self._font = _fonts.get_font(font, self._fsize)

        # Position of menu
        self._posx = (window_width - self._width) / 2
        self._posy = (window_height - self._height) / 2
        self._bgrect = [(self._posx, self._posy),
                        (self._posx + self._width, self._posy),
                        (self._posx + self._width, self._posy + self._height),
                        (self._posx, self._posy + self._height)]
        self._draw_regionx = draw_region_x
        self._draw_regiony = draw_region_y

        # Option position
        self._opt_posx = int(self._width * (self._draw_regionx / 100.0)) + self._posx
        self._opt_posy = int(self._height * (self._draw_regiony / 100.0)) + self._posy
        self._widget_align = widget_alignment

        # Init joystick
        self._joystick = joystick_enabled
        if self._joystick and not _pygame.joystick.get_init():
            _pygame.joystick.init()
            for i in range(_pygame.joystick.get_count()):
                _pygame.joystick.Joystick(i).init()

        # Init mouse
        self._mouse = mouse_enabled and mouse_visible
        self._mouse_visible = mouse_visible

        # Create menu bar
        self._menubar = _widgets.MenuBar(title, self._width, back_box, None, self._back)
        self._menubar.set_title(title, title_offsetx, title_offsety)
        font_title = _fonts.get_font(font_title or font, font_size_title)
        bg_color_title = (menu_color_title[0], menu_color_title[1], menu_color_title[2],
                          int(255 * (1 - (100 - menu_alpha) / 100.0)))
        self._menubar.set_font(font_title, font_size_title,
                               bg_color_title, self._font_color)
        self._menubar.set_shadow(enabled=self._option_shadow,
                                 color=_cfg.MENU_SHADOW_COLOR,
                                 position=self._option_shadow_position,
                                 offset=self._option_shadow_offset)
        self._menubar.set_controls(self._joystick, self._mouse)

        # Selected option
        self._selected_inflate_x = 16
        self._selected_inflate_y = 6

        # FPS of the menu
        self.set_fps(fps)

    def add_option(self, element_name, element, *args, **kwargs):
        """
        Add option (button) to menu.

        kwargs:
            - align         Widget alignment
            - option_id     Option ID

        :param element_name: Name of the element
        :type element_name: basestring
        :param element: Object
        :type element: Menu, _PymenuAction, function
        :param args: Aditional arguments used by a function
        :param kwargs: Additional keyword arguments
        :return: Widget object
        :rtype: pygameMenu.widgets.button.Button
        """
        assert isinstance(element_name, str), 'element_name must be a string'

        # Get id
        option_id = kwargs.pop('option_id', '')
        assert isinstance(option_id, str), 'ID must be a string'

        self._size += 1
        if self._size > 1:
            dy = -self._fsize / 2 - self._opt_dy / 2
            self._opt_posy += dy

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
        self._check_id_duplicated(option_id)

        widget.set_font(self._font,
                        self._fsize,
                        self._font_color,
                        self._sel_color)
        widget.set_shadow(enabled=self._option_shadow,
                          color=_cfg.MENU_SHADOW_COLOR,
                          position=self._option_shadow_position,
                          offset=self._option_shadow_offset)
        widget.set_controls(self._joystick,
                            self._mouse)
        widget.set_alignment(kwargs.pop('align', self._widget_align))

        self._option.append(widget)
        if len(self._option) == 1:
            widget.set_selected()

        return widget

    def add_selector(self,
                     title,
                     values,
                     selector_id='',
                     default=0,
                     align='',
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
        :param onchange: Function when changing the selector
        :type onchange: function, NoneType
        :param onreturn: Function when pressing return button
        :type onreturn: function, NoneType
        :param kwargs: Aditional parameters
        :return: Widget object
        :rtype: pygameMenu.widgets.selector.Selector
        """
        # Check value list
        for vl in values:
            assert len(vl) >= 1, \
                'Length of each element in value list must be greater than 1'
            assert isinstance(vl[0], str), \
                'First element of value list component must be a string'
        assert default < len(values), 'default position should be lower than number of values'
        assert isinstance(selector_id, str), 'ID must be a string'
        assert isinstance(default, int), 'default must be integer'
        assert isinstance(align, str), 'align must be a string'
        if align == '':
            align = self._widget_align

        self._size += 1
        if self._size > 1:
            dy = -self._fsize / 2 - self._opt_dy / 2
            self._opt_posy += dy

        # Create widget
        widget = _widgets.Selector(title, values, selector_id, default,
                                   onchange, onreturn, **kwargs)
        self._check_id_duplicated(selector_id)

        # Configure widget
        widget.set_font(self._font,
                        self._fsize,
                        self._font_color,
                        self._sel_color)
        widget.set_shadow(enabled=self._option_shadow,
                          color=_cfg.MENU_SHADOW_COLOR,
                          position=self._option_shadow_position,
                          offset=self._option_shadow_offset)
        widget.set_controls(self._joystick,
                            self._mouse)
        widget.set_alignment(align)

        # Store widget
        self._option.append(widget)
        if len(self._option) == 1:
            widget.set_selected()

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
                       enable_selection=True,
                       password=False,
                       onchange=None,
                       onreturn=None,
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
        :param enable_selection: Enable text selection on input
        :type enable_selection: bool
        :param password: Text input is a password
        :type password: bool
        :param onchange: Function when changing the selector
        :type onchange: function, NoneType
        :param onreturn: Function when pressing return button
        :type onreturn: function, NoneType
        :param kwargs: Aditional keyword-parameters
        :return: Widget object
        :rtype: pygameMenu.widgets.textinput.TextInput
        """
        self._size += 1
        if self._size > 1:
            dy = -self._fsize / 2 - self._opt_dy / 2
            self._opt_posy += dy
        if align == '':
            align = self._widget_align

        # Check data
        assert isinstance(textinput_id, str), 'ID must be a string'
        assert isinstance(input_type, str), 'input_type must be a string'
        assert isinstance(input_underline, str), 'input_underline must be a string'
        assert isinstance(align, str), 'align must be a string'
        assert isinstance(enable_selection, bool), 'enable_selection must be a boolean'

        assert isinstance(maxchar, int), 'maxchar must be integer'
        assert maxchar >= 0, 'maxchar must be greater or equal than zero'
        assert isinstance(maxwidth, int), 'maxwidth must be an integer'
        assert maxwidth >= 0, 'maxwidth must be greater or equal than zero'

        # Create widget
        widget = _widgets.TextInput(title,
                                    default,
                                    textinput_id=textinput_id,
                                    maxchar=maxchar,
                                    maxwidth=maxwidth,
                                    input_type=input_type,
                                    input_underline=input_underline,
                                    enable_selection=enable_selection,
                                    password=password,
                                    onchange=onchange,
                                    onreturn=onreturn,
                                    **kwargs)
        widget.set_menu(self)
        self._check_id_duplicated(textinput_id)

        # Configure widget
        widget.set_font(self._font,
                        self._fsize,
                        self._font_color,
                        self._sel_color)
        widget.set_shadow(enabled=self._option_shadow,
                          color=_cfg.MENU_SHADOW_COLOR,
                          position=self._option_shadow_position,
                          offset=self._option_shadow_offset)
        widget.set_controls(self._joystick,
                            self._mouse)
        widget.set_alignment(align)

        # Store widget
        self._option.append(widget)
        if len(self._option) == 1:
            widget.set_selected()

        return widget

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

    def _get_depth(self):
        """
        Find menu depth.

        :return: Depth
        :rtype: int
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

    def disable(self, closelocked=True):
        """
        Disable the menu.

        :return: None
        """
        if self.is_enabled():
            self._enabled = False
            self._closelocked = closelocked

    def draw(self):
        """
        Draw menu to the active surface.

        :return: None
        """
        self._frame += 1

        # Draw background rectangle
        _gfxdraw.filled_polygon(self._surface, self._bgrect, self._bgcolor)

        # Update menu bar position
        self._menubar.set_position(self._posx, self._posy)
        self._menubar.draw(self._surface)

        # Draw options (widgets)
        for index in range(len(self._option)):
            widget = self._option[index]

            # Update widget position
            widget.set_position(*self._get_option_pos(index))

            # Draw widget
            widget.draw(self._surface)

            # If selected item then draw a rectangle
            if self._drawselrect and widget.selected:
                widget.draw_selected_rect(self._surface,
                                          self._sel_color,
                                          self._selected_inflate_x,
                                          self._selected_inflate_y,
                                          self._rect_width)

    def _get_option_pos(self, index):
        """
        Get option position from the option index.

        :param index: Option index
        :type index: int
        :return: Position (x,y)
        :rtype: tuple
        """
        rect = self._option[index].get_rect()
        align = self._option[index].get_alignment()

        # Calculate alignment
        if align == _locals.ALIGN_CENTER:
            option_dx = -int(rect.width / 2.0)
        elif align == _locals.ALIGN_LEFT:
            option_dx = -self._width / 2 + self._selected_inflate_x
        elif align == _locals.ALIGN_RIGHT:
            option_dx = self._width / 2 - rect.width - self._selected_inflate_x
        else:
            option_dx = 0
        t_dy = -int(rect.height / 2.0)

        xccord = self._opt_posx + option_dx
        ycoord = self._opt_posy + index * (self._fsize + self._opt_dy) + t_dy
        return xccord, ycoord

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
        exit()

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

    @staticmethod
    def _check_key_pressed_valid(event):
        """
        Checks if the pressed key is valid.

        :param event: Key press event
        :type event: pygame.event.EventType
        :return: True if a key is pressed
        :rtype: bool
        """
        # If the system detects that any key event has been pressed but
        # there's not any key pressed then this method raises a KEYUP
        # flag
        bad_event = not (True in _pygame.key.get_pressed())
        if bad_event:
            if 'test' in event.dict and event.dict['test']:
                return True
            ev = _pygame.event.Event(_pygame.KEYUP, {'key': event.key})
            _pygame.event.post(ev)
        return not bad_event

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
                    if not self._check_key_pressed_valid(event):
                        continue

                    if event.key == _ctrl.KEY_MOVE_DOWN:
                        self._select(self._actual._index - 1)
                        self._sounds.play_key_add()
                    elif event.key == _ctrl.KEY_MOVE_UP:
                        self._select(self._actual._index + 1)
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
                        self._select(self._actual._index + 1)
                    elif event.value == _ctrl.JOY_DOWN:
                        self._select(self._actual._index - 1)

                elif self._joystick and event.type == _pygame.JOYAXISMOTION:
                    if event.axis == _ctrl.JOY_AXIS_Y and event.value < -_ctrl.JOY_DEADZONE:
                        self._select(self._actual._index - 1)
                    if event.axis == _ctrl.JOY_AXIS_Y and event.value > _ctrl.JOY_DEADZONE:
                        self._select(self._actual._index + 1)

                elif self._mouse and event.type == _pygame.MOUSEBUTTONUP:
                    self._sounds.play_click_mouse()
                    for index in range(len(self._actual._option)):
                        widget = self._actual._option[index]
                        if widget.get_rect().collidepoint(*event.pos):
                            self._select(index)
                            widget.update(events)  # This option can change the current menu to a submenu
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

                # Check if there is a colission between keys
                data_keys = data.keys()
                subdata_keys = data_submenu.keys()
                for key in subdata_keys:  # type: str
                    if key in data_keys:
                        msg = 'Colission between widget data ID="{0}" at depth={1}'.format(key, depth)
                        raise ValueError(msg)

                # Update data
                data.update(data_submenu)
        return data

    def get_position(self):
        """
        Returns menu position as a tuple.

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
        if actual._size == 0:
            return
        actual._option[actual._index].set_selected(False)
        actual._index = index % actual._size
        actual._option[actual._index].set_selected()

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
