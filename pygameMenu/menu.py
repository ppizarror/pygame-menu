# coding=utf-8
"""
MENU
Menu class.

Copyright (C) 2017-2018 Pablo Pizarro @ppizarror

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

# Import constants
import pygameMenu.config_controls as _ctrl
import pygameMenu.config_menu as _cfg
import pygameMenu.locals as _locals

# Library imports
from pygameMenu.selector import Selector as _Selector
import pygame as _pygame
import pygame.gfxdraw as _gfxdraw
import types


# noinspection PyBroadException
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
                 joystick_enabled=True,
                 menu_alpha=_cfg.MENU_ALPHA,
                 menu_centered=_cfg.MENU_CENTERED_TEXT,
                 menu_color=_cfg.MENU_BGCOLOR,
                 menu_color_title=_cfg.MENU_TITLE_BG_COLOR,
                 menu_height=_cfg.MENU_HEIGHT,
                 menu_width=_cfg.MENU_WIDTH,
                 onclose=None,
                 option_margin=_cfg.MENU_OPTION_MARGIN,
                 option_shadow=_cfg.MENU_OPTION_SHADOW,
                 rect_width=_cfg.MENU_SELECTED_WIDTH,
                 title_offsetx=0,
                 title_offsety=0
                 ):
        """
        Menu constructor.

        :param bgfun: Background drawing function (only if menu pause app)
        :param color_selected: Color of selected item
        :param dopause: Pause game
        :param draw_region_x: Drawing position of element inside menu (x-axis)
        :param draw_region_y: Drawing position of element inside menu (y-axis)
        :param draw_select: Draw a rectangle around selected item (bool)
        :param enabled: Menu is enabled by default or not
        :param font: Font file direction
        :param font_color: Color of font
        :param font_size: Font size
        :param font_size_title: Font size of the title
        :param font_title: Alternative font of the title (file direction)
        :param joystick_enabled: Enable/disable joystick on menu
        :param menu_alpha: Alpha of background (0=transparent, 100=opaque)
        :param menu_centered: Text centered menu
        :param menu_color: Menu color
        :param menu_color_title: Background color of title
        :param menu_height: Height of menu (px)
        :param menu_width: Width of menu (px)
        :param onclose: Function that applies when closing menu
        :param option_margin: Margin of each element in menu (px)
        :param option_shadow: Indicate if a shadow is drawn on each option
        :param rect_width: Border with of rectangle around selected item
        :param surface: Pygame surface
        :param title: Title of the menu (main title)
        :param title_offsetx: Offset x-position of title (px)
        :param title_offsety: Offset y-position of title (px)
        :param window_height: Window height size (px)
        :param window_width: Window width size (px)
        :type bgfun: function
        :type color_selected: tuple
        :type dopause: bool
        :type draw_region_x: int
        :type draw_region_y: int
        :type draw_select: bool
        :type font: basestring
        :type font_color: tuple
        :type font_size: int
        :type font_size_title: int
        :type font_title: basestring
        :type joystick_enabled: bool
        :type menu_alpha: int
        :type menu_centered: bool
        :type menu_color: tuple
        :type menu_color_title: tuple
        :type menu_height: int
        :type menu_width: int
        :type option_margin: int
        :type option_shadow: bool
        :type rect_width: int
        :type title: basestring
        :type window_height: int
        :type window_width: int
        """
        assert isinstance(color_selected, tuple)
        assert isinstance(dopause, bool)
        assert isinstance(draw_region_x, int)
        assert isinstance(draw_region_y, int)
        assert isinstance(draw_select, bool)
        assert isinstance(font, str)
        assert isinstance(font_color, tuple)
        assert isinstance(font_size, int)
        assert isinstance(font_size_title, int)
        assert isinstance(joystick_enabled, bool)
        assert isinstance(menu_alpha, int)
        assert isinstance(menu_centered, bool)
        assert isinstance(menu_color, tuple)
        assert isinstance(menu_color_title, tuple)
        assert isinstance(menu_height, int)
        assert isinstance(menu_width, int)
        assert isinstance(option_margin, int)
        assert isinstance(option_shadow, bool)
        assert isinstance(rect_width, int)
        assert isinstance(title, str)
        assert isinstance(window_height, int)
        assert isinstance(window_width, int)

        # Other asserts
        if dopause:
            assert isinstance(bgfun, types.FunctionType), \
                'Bgfun must be a function (or None if menu does not pause ' \
                'execution of the application)'
        else:
            assert isinstance(bgfun, type(None)), \
                'Bgfun must be None if menu does not pause execution of the ' \
                'application'
        assert window_height > 0 and window_width > 0, \
            'Window size must be greater than zero'
        assert rect_width >= 0, 'rect_width must be greater or equal than zero'
        assert option_margin >= 0, \
            'Option margin must be greater or equal than zero'
        assert menu_width > 0 and menu_height > 0, \
            'Menu size must be greater than zero'
        assert font_size > 0 and font_size_title > 0, \
            'Font sizes must be greater than zero'
        assert draw_region_y >= 0 and draw_region_x >= 0, \
            'Drawing regions must be greater or equal than zero'
        assert dopause and bgfun is not None or not dopause and bgfun is None, \
            'If pause main execution is enabled then bgfun (Background ' \
            'function drawing) must be defined (not None)'
        assert 0 <= menu_alpha <= 100, 'Menu_alpha must be between 0 and 100'

        # Store configuration
        self._bgfun = bgfun
        self._bgcolor = (menu_color[0], menu_color[1], menu_color[2],
                         int(255 * (1 - (100 - menu_alpha) / 100.0)))
        self._bg_color_title = (menu_color_title[0],
                                menu_color_title[1],
                                menu_color_title[2],
                                int(255 * (1 - (100 - menu_alpha) / 100.0)))
        self._centered_option = menu_centered
        self._drawselrect = draw_select
        self._font_color = font_color
        self._fsize = font_size
        self._fsize_title = font_size_title
        self._height = menu_height
        self._opt_dy = option_margin
        self._option_shadow = option_shadow
        self._rect_width = rect_width
        self._sel_color = color_selected
        self._surface = surface
        self._width = menu_width

        # Inner variables
        self._actual = self  # Actual menu
        self._closelocked = False  # Lock close until next mainloop
        self._dopause = dopause  # Pause or not
        self._enabled = enabled  # Menu is enabled or not
        self._index = 0  # Selected index
        self._onclose = onclose  # Function that calls after closing menu
        self._option = []  # Option menu
        self._prev = None  # Previous menu
        self._prev_draw = None  # Previous menu drawing function
        self._size = 0  # Menu total elements

        # Load fonts
        try:
            self._font = _pygame.font.Font(font, self._fsize)
        except Exception:
            raise Exception('Could not load {0} font file'.format(font))
        if font_title is None:
            font_title = font
        self._font_title = _pygame.font.Font(font_title, self._fsize_title)

        # Position of menu
        self._posy = (window_width - self._width) / 2
        self._posx = (window_height - self._height) / 2
        self._bgrect = [(self._posy, self._posx),
                        (self._posy + self._width, self._posx),
                        (self._posy + self._width, self._posx + self._height),
                        (self._posy, self._posx + self._height)]
        self._draw_regionx = draw_region_x
        self._draw_regiony = draw_region_y

        # Option position
        self._opt_posx = int(
            self._width * (self._draw_regionx / 100.0)) + self._posy
        self._opt_posy = int(
            self._height * (self._draw_regiony / 100.0)) + self._posx

        # Title properties
        self.set_title(title, title_offsetx, title_offsety)

        # Init joystick
        self._joystick = joystick_enabled
        if self._joystick and not _pygame.joystick.get_init():
            _pygame.joystick.init()
            for i in range(_pygame.joystick.get_count()):
                _pygame.joystick.Joystick(i).init()

    def add_option(self, element_name, element, *args):
        """
        Add option to menu.

        :param element_name: Name of the element
        :param element: Object
        :param args: Aditional arguments
        :type element_name: str
        :type element: Menu, _PymenuAction, function
        :return:
        """
        a = isinstance(element, Menu)
        b = str(type(element)) == _locals.PYGAMEMENU_PYMENUACTION
        c = isinstance(element, types.FunctionType)
        d = callable(element)
        e = isinstance(element, _locals.PymenuAction)
        assert a or b or c or d or e, \
            'Element must be a Menu, an PymenuAction or a function'
        assert isinstance(element_name, str), 'Element name must be a string'
        self._actual._option.append([element_name, element, args])
        self._actual._size += 1
        if self._actual._size > 1:
            dy = -self._actual._fsize / 2 - self._actual._opt_dy / 2
            self._actual._opt_posy += dy

    def add_selector(self, title, values, onchange, onreturn,
                     **kwargs):
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
        :param values: Values of the selector [('Item1', var1..), ('Item2'...)]
        :param onchange: Function when changing the selector
        :param onreturn: Function when pressing return button
        :param kwargs: Aditional parameters
        :type title: basestring
        :type values: list
        :type onchange: function, NoneType
        :type onreturn: function, NoneType
        :return: Selector ID
        :rtype: int
        """
        # Check value list
        for vl in values:
            assert len(vl) > 1, \
                'Length of each element in value list must be greater than 1'
            assert isinstance(vl[0], str), \
                'First element of value list component must be a string'

        self._actual._option.append(
            [_locals.PYGAMEMENU_TYPE_SELECTOR,
             _Selector(title, values, onchange=onchange, onreturn=onreturn,
                       **kwargs)])
        selector_id = self._actual._size
        self._actual._size += 1
        if self._actual._size > 1:
            dy = -self._actual._fsize / 2 - self._actual._opt_dy / 2
            self._actual._opt_posy += dy
        return selector_id

    def add_selector_change(self, title, values, fun, **kwargs):
        """
        Add a selector to the menu, apply function with values list and kwargs
        optional parameters when pressing left/right on the element.

        Values of the selector are like:
            values = [('Item1', a, b, c...), ('Item2', a, b, c..)]

        And when changing the value of the selector:
            fun(a, b, c,..., **kwargs)

        :param title: Title of the selector
        :param values: Values of the selector
        :param fun: Function to apply values when changing the selector
        :param kwargs: Optional parameters to function
        :type title: basestring
        :type values: list
        :type fun: function, NoneType
        :return: Selector ID
        :rtype: int
        """
        return self.add_selector(title=title, values=values, onchange=fun,
                                 onreturn=None, kwargs=kwargs)

    def add_selector_return(self, title, values, fun, **kwargs):
        """
        Add a selector to the menu, apply function with values list and kwargs
        optional parameters when pressing return on the element.

        Values of the selector are like:
            values = [('Item1', a, b, c...), ('Item2', a, b, c..)]

        And when pressing return on the selector:
            fun(a, b, c,..., **kwargs)

        :param title: Title of the selector
        :param values: Values of the selector
        :param fun: Function to apply values when pressing return on the element
        :param kwargs: Optional parameters to function
        :type title: str
        :type values: list
        :type fun: function, NoneType
        :return: Selector ID
        :rtype: int
        """
        return self.add_selector(title=title, values=values, onchange=None,
                                 onreturn=fun, kwargs=kwargs)

    def disable(self):
        """
        Disable menu.

        :return: None
        """
        if self.is_enabled():
            self._enabled = False
            self._closelocked = True

    def _down(self):
        """
        Move selection down.

        :return: None
        """
        if self._actual._size == 0:
            return
        self._actual._index = (self._actual._index - 1) % self._actual._size

    def draw(self):
        """
        Draw menu to surface.

        :return:
        """
        # Draw background rectangle
        _gfxdraw.filled_polygon(self._surface, self._actual._bgrect,
                                self._actual._bgcolor)
        # Draw title
        _gfxdraw.filled_polygon(self._surface, self._actual._title_rect,
                                self._bg_color_title)
        self._surface.blit(self._actual._title, self._title_pos)

        # Draw options
        dy = 0
        for option in self._actual._option:
            # Si el tipo es un selector
            if option[0] == _locals.PYGAMEMENU_TYPE_SELECTOR:
                # If selected index draw a rectangle
                if dy == self._actual._index:
                    text = self._actual._font.render(option[1].get(), 1,
                                                     self._actual._sel_color)
                    text_bg = self._actual._font.render(option[1].get(), 1,
                                                        _cfg.SHADOW_COLOR)
                else:
                    text = self._actual._font.render(option[1].get(), 1,
                                                     self._actual._font_color)
                    text_bg = self._actual._font.render(option[1].get(), 1,
                                                        _cfg.SHADOW_COLOR)
            else:
                # If selected index draw a rectangle
                if dy == self._actual._index:
                    text = self._actual._font.render(option[0], 1,
                                                     self._actual._sel_color)
                    text_bg = self._actual._font.render(option[0], 1,
                                                        _cfg.SHADOW_COLOR)
                else:
                    text = self._actual._font.render(option[0], 1,
                                                     self._actual._font_color)
                    text_bg = self._actual._font.render(option[0], 1,
                                                        _cfg.SHADOW_COLOR)
            # Text anchor
            text_width, text_height = text.get_size()
            t_dy = -int(text_height / 2.0)
            if self._actual._centered_option:
                text_dx = -int(text_width / 2.0)
            else:
                text_dx = 0
            # Draw fonts
            if self._actual._option_shadow:
                ycoords = self._actual._opt_posy + dy * (
                        self._actual._fsize + self._actual._opt_dy) + t_dy - 3
                self._surface.blit(text_bg,
                                   (self._actual._opt_posx + text_dx - 3,
                                    ycoords))
            ycoords = self._actual._opt_posy + dy * (
                    self._actual._fsize + self._actual._opt_dy) + t_dy
            self._surface.blit(text, (self._actual._opt_posx + text_dx,
                                      ycoords))
            # If selected item then draw a rectangle
            if self._actual._drawselrect and (dy == self._actual._index):
                if not self._actual._centered_option:
                    text_dx_tl = -text_width
                else:
                    text_dx_tl = text_dx
                ycoords = self._actual._opt_posy + dy * (
                        self._actual._fsize + self._actual._opt_dy) + t_dy - 2
                _pygame.draw.line(self._surface, self._actual._sel_color, (
                    self._actual._opt_posx + text_dx - 10,
                    self._actual._opt_posy + dy * (
                            self._actual._fsize + self._actual._opt_dy) + t_dy - 2),
                                  ((self._actual._opt_posx - text_dx_tl + 10,
                                    ycoords)), self._actual._rect_width)
                ycoords = self._actual._opt_posy + dy * (
                        self._actual._fsize + self._actual._opt_dy) - t_dy + 2
                _pygame.draw.line(self._surface, self._actual._sel_color, (
                    self._actual._opt_posx + text_dx - 10,
                    self._actual._opt_posy + dy * (
                            self._actual._fsize + self._actual._opt_dy) - t_dy + 2),
                                  ((self._actual._opt_posx - text_dx_tl + 10,
                                    ycoords)), self._actual._rect_width)
                ycoords = self._actual._opt_posy + dy * (
                        self._actual._fsize + self._opt_dy) - t_dy + 2
                _pygame.draw.line(self._surface, self._actual._sel_color, (
                    self._actual._opt_posx + text_dx - 10,
                    self._actual._opt_posy + dy * (
                            self._actual._fsize + self._actual._opt_dy) + t_dy - 2),
                                  ((self._actual._opt_posx + text_dx - 10,
                                    ycoords)), self._actual._rect_width)
                ycoords = self._actual._opt_posy + dy * (
                        self._actual._fsize + self._actual._opt_dy) - t_dy + 2
                _pygame.draw.line(self._surface, self._actual._sel_color, (
                    self._actual._opt_posx - text_dx_tl + 10,
                    self._actual._opt_posy + dy * (
                            self._actual._fsize + self._actual._opt_dy) + t_dy - 2),
                                  ((self._actual._opt_posx - text_dx_tl + 10,
                                    ycoords)), self._actual._rect_width)
            dy += 1

    def enable(self):
        """
        Enable menu.

        :return: None
        """
        if self.is_disabled():
            self._enabled = True
            self._closelocked = True

    def get_title(self):
        """
        Return title of the Menu

        :return: Title
        :rtype: str
        """
        return self._title_str

    def is_disabled(self):
        """
        Returns false/true if Menu is enabled or not

        :return: Boolean
        :rtype: bool
        """
        return not self.is_enabled()

    def is_enabled(self):
        """
        Returns true/false if Menu is enabled or not

        :return: Boolean
        :rtype: bool
        """
        return self._enabled

    def _main(self, events=None):
        """
        Main function of the loop.

        :param events: Pygame events
        :return: None
        """
        if self._actual._dopause:  # If menu pauses game then apply function
            self._bgfun()
        self.draw()
        if events is None:
            events = _pygame.event.get()
        for event in events:
            # noinspection PyUnresolvedReferences
            if event.type == _pygame.locals.QUIT:
                exit()
            elif event.type == _pygame.locals.KEYDOWN:
                if event.key == _ctrl.MENU_CTRL_DOWN:
                    self._down()
                elif event.key == _ctrl.MENU_CTRL_UP:
                    self._up()
                elif event.key == _ctrl.MENU_CTRL_ENTER:
                    self._select()
                    if not self._actual._dopause:
                        return True
                elif event.key == _ctrl.MENU_CTRL_LEFT:
                    self._left()
                elif event.key == _ctrl.MENU_CTRL_RIGHT:
                    self._right()
                elif event.key == _ctrl.MENU_CTRL_BACK:
                    self.reset(1)
                elif event.key == _ctrl.MENU_CTRL_CLOSE_MENU and \
                        not self._closelocked:
                    onclose = self._actual._onclose
                    close = True
                    if not isinstance(onclose, type(None)):
                        a = isinstance(onclose, _locals.PymenuAction)
                        b = str(type(onclose)) == _locals.PYGAMEMENU_PYMENUACTION
                        if a or b:
                            if onclose == _locals.PYGAME_MENU_RESET:
                                self.reset(100)
                            elif onclose == _locals.PYGAME_MENU_BACK:
                                self.reset(1)
                            elif onclose == _locals.PYGAME_MENU_EXIT:
                                exit()
                            elif onclose == _locals.PYGAME_MENU_DISABLE_CLOSE:
                                close = False
                        elif isinstance(onclose, types.FunctionType):
                            onclose()
                    else:
                        close = False
                    if close:
                        self.disable()
                        return True
            elif self._joystick and event.type == _pygame.JOYHATMOTION:
                if event.value == _locals.JOY_UP:
                    self._up()
                elif event.value == _locals.JOY_DOWN:
                    self._down()
                elif event.value == _locals.JOY_LEFT:
                    self._left()
                elif event.value == _locals.JOY_RIGHT:
                    self._right()
            elif self._joystick and event.type == _pygame.JOYAXISMOTION:
                if event.axis == _locals.JOY_AXIS_Y and event.value < -_locals.JOY_DEADZONE:
                    self._down()
                if event.axis == _locals.JOY_AXIS_Y and event.value > _locals.JOY_DEADZONE:
                    self._up()
                if event.axis == _locals.JOY_AXIS_X and event.value > _locals.JOY_DEADZONE:
                    self._right()
                if event.axis == _locals.JOY_AXIS_X and event.value < -_locals.JOY_DEADZONE:
                    self._left()
            elif self._joystick and event.type == _pygame.JOYBUTTONDOWN:
                if event.button == _locals.JOY_BUTTON_SELECT:
                    self._select()
                elif event.button == _locals.JOY_BUTTON_BACK:
                    self.reset(1)
        _pygame.display.flip()
        self._closelocked = False
        return False

    def mainloop(self, events):
        """
        Main function of Menu, draw, etc.

        :param events: Menu events
        :return: None
        """
        assert isinstance(self._actual, Menu)

        if self.is_disabled():
            return
        if self._actual._dopause:
            while True:
                if self._main():
                    return
        else:
            self._main(events)

    def _left(self):
        """
        Move selector left

        :return: None
        """
        try:
            option = self._actual._option[self._actual._index][1]
            if isinstance(option, _Selector):
                option.left()
        except Exception:
            pass

    # noinspection PyAttributeOutsideInit
    def reset(self, total):
        """
        Reset menu.

        :param total: How many menus to reset (1: back)
        :type total: int
        :return:
        """
        assert isinstance(self._actual, Menu)
        assert isinstance(total, int)
        assert total > 0, 'Total must be greater than zero'

        i = 0
        while True:
            if self._actual._prev is not None:
                prev = self._actual._prev
                prev_draw = self._actual._prev_draw
                self.draw = prev_draw
                self._actual.index = 0
                self._actual = prev
                self._actual._prev = None
                self._actual._prev_draw = None
                i += 1
                if total != 0 and i == total:
                    break
            else:
                break

    def _right(self):
        """
        Move selector to right.

        :return: None
        """
        try:
            option = self._actual._option[self._actual._index][1]
            if isinstance(option, _Selector):
                option.right()
        except Exception:
            pass

    def _select(self):
        """
        Apply selected option.

        :return:
        """
        assert isinstance(self._actual, Menu)
        try:
            option = self._actual._option[self._actual._index][1]
        except Exception:
            return
        a = isinstance(option, _locals.PymenuAction)
        b = str(type(option)) == _locals.PYGAMEMENU_PYMENUACTION

        # If element is a Menu
        if isinstance(option, Menu):
            actual = self
            self._actual._actual = option._actual
            self._actual._prev = actual
            self._actual._prev_draw = self.draw
            self.draw = option.draw
        # If option is a PyMenuAction
        elif a or b:
            # Back to menu
            if option == _locals.PYGAME_MENU_BACK:
                self.reset(1)
            # Close menu
            elif option == _locals.PYGAME_MENU_CLOSE:
                self.disable()
                self._closelocked = False
                closefun = self._actual._onclose
                if closefun is not None:
                    if closefun == _locals.PYGAME_MENU_RESET:
                        self.reset(100)
                    elif closefun == _locals.PYGAME_MENU_BACK:
                        self.reset(1)
                    elif closefun == _locals.PYGAME_MENU_EXIT:
                        exit()
                    elif isinstance(self._onclose, types.FunctionType):
                        closefun()
            # Exit program
            elif option == _locals.PYGAME_MENU_EXIT:
                exit()
        # If element is a function
        elif isinstance(option, types.FunctionType) or callable(option):
            if len(self._actual._option[self._actual._index][2]) > 0:
                if type(self._actual._option[self._actual._index][2]) is tuple:
                    option(*self._actual._option[self._actual._index][2])
                else:
                    option(self._actual._option[self._actual._index][2])
            else:
                option()
        # If null type
        elif isinstance(option, type(None)):
            pass
        # If element is a selector
        elif isinstance(option, _Selector):
            option.apply()

    # noinspection PyAttributeOutsideInit
    def set_title(self, title, offsetx=0, offsety=0):
        """
        Set menu title.

        :param title: Menu title
        :param offsetx: Offset x-position of title (px)
        :param offsety: Offset y-position of title (px)
        :type title: str
        :type offsetx: int
        :type offsety: int
        :return: None
        """
        assert isinstance(title, str)
        assert isinstance(offsetx, int)
        assert isinstance(offsety, int)

        self._title_offsety = offsety
        self._title_offsetx = offsetx
        self._title = self._font_title.render(title, 1, self._font_color)
        self._title_str = title
        title_width = self._title.get_size()[0]
        title_height = self._title.get_size()[1]
        self._fsize_title = title_height
        self._title_rect = [(self._posy, self._posx),
                            (self._posy + self._width, self._posx), (
                                self._posy + self._width,
                                self._posx + self._fsize_title / 2),
                            (self._posy + title_width + 25,
                             self._posx + self._fsize_title / 2), (
                                self._posy + title_width + 5,
                                self._posx + self._fsize_title + 5),
                            (self._posy, self._posx + self._fsize_title + 5)]
        self._title_pos = (
            self._posy + 5 + self._title_offsetx, self._posx + self._title_offsety)

    def _up(self):
        """
        Option up.

        :return: None
        """
        if self._actual._size == 0:
            return
        self._actual._index = (self._actual._index + 1) % self._actual._size

    def update_selector(self, selector_id, values):
        """
        Update selector given its ID.

        :param selector_id: ID of existing selector
        :param values: Values of the selector [('Item1', var1..), ('Item2'...)]
        :return:
        """
        assert self._actual._size > selector_id and self._actual._option[selector_id][
            0] == _locals.PYGAMEMENU_TYPE_SELECTOR, 'There is no selector with such ID'
        for vl in values:  # Check value list
            assert len(vl) > 1, \
                'Length of each element in value list must be greater than 1'
            assert isinstance(vl[0], str), \
                'First element of value list component must be a string'

        self._actual._option[selector_id][1].update_elements(values)
