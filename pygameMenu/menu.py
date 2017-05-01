# coding=utf-8
"""
MENU
Menu class

Copyright (C) 2017 Pablo Pizarro @ppizarror

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
from config_menu import *
from locals import *

# Library imports
from selector import Selector
import pygame
import pygame.gfxdraw
import types


# noinspection PyProtectedMember
class Menu(object):
    """
    Menu object
    """

    def __init__(self, surface, window_width, window_height, font, title,
                 bg_color=MENU_BGCOLOR,
                 bg_color_title=MENU_TITLE_BG_COLOR,
                 bgalpha=MENU_ALPHA,
                 color_selected=MENU_SELECTEDCOLOR,
                 draw_region_x=MENU_DRAW_X,
                 draw_region_y=MENU_DRAW_Y,
                 draw_select=MENU_SELECTED_DRAW,
                 font_color=MENU_FONT_COLOR,
                 font_size=MENU_FONT_SIZE,
                 font_size_title=MENU_FONT_SIZE_TITLE,
                 menu_centered=MENU_CENTERED_TEXT,
                 menu_height=MENU_HEIGHT,
                 menu_width=MENU_WIDTH,
                 option_margin=MENU_OPTION_MARGIN,
                 option_shadow=MENU_OPTION_SHADOW,
                 rect_width=MENU_SELECTED_WIDTH):
        """
        Menu constructor.
        
        :param surface: Pygame surface
        :param window_width: Window width size (px)
        :param window_height: Window height size (px)
        :param font: Font file direction
        :param title: Title of the menu (main title)
        :param bg_color: Background color
        :param bg_color_title: Background color of title
        :param bgalpha: Alpha of background (0=opaque, 1=transparent)
        :param color_selected: Color of selected item
        :param draw_region_x: Drawing position of element inside menu (x-axis)
        :param draw_region_y: Drawing position of element inside menu (y-axis)
        :param draw_select: Draw a rectangle around selected item (bool)
        :param font_color: Color of font
        :param font_size: Font size
        :param font_size_title: Font size of title
        :param menu_centered: Text centered menu
        :param menu_height: Height of menu (px)
        :param menu_width: Width of menu (px)
        :param option_margin: Margin of each element in menu (px)
        :param option_shadow: Indicate if a shadow is drawn on each option
        :param rect_width: Border with of rectangle around selected item
        
        :type window_width: int
        :type window_height: int
        :type font: basestring
        :type title: basestring
        :type bg_color: tuple
        :type bg_color_title: tuple
        :type bgalpha: int
        :type color_selected: tuple
        :type draw_region_x: int
        :type draw_region_y: int
        :type draw_select: bool
        :type font_color: tuple
        :type font_size: int
        :type font_size_title: int
        :type menu_centered: bool
        :type menu_height: int
        :type menu_width: int
        :type option_margin: int
        :type option_shadow: bool
        :type rect_width: int
        
        :return: Menu object
        """
        # Assert types
        assert isinstance(window_width, int)
        assert isinstance(window_height, int)
        assert isinstance(font, str)
        assert isinstance(title, str)
        assert isinstance(bg_color, tuple)
        assert isinstance(bg_color_title, tuple)
        assert isinstance(bgalpha, int)
        assert isinstance(color_selected, tuple)
        assert isinstance(draw_region_x, int)
        assert isinstance(draw_region_y, int)
        assert isinstance(draw_select, bool)
        assert isinstance(font_color, tuple)
        assert isinstance(font_size, int)
        assert isinstance(font_size_title, int)
        assert isinstance(menu_centered, bool)
        assert isinstance(menu_height, int)
        assert isinstance(menu_width, int)
        assert isinstance(option_margin, int)
        assert isinstance(option_shadow, bool)
        assert isinstance(rect_width, int)

        # Store configuration
        self._bgcolor = (bg_color[0], bg_color[1], bg_color[2],
                         int(255 * (1 - (100 - bgalpha) / 100.0)))
        self._bg_color_title = (
            bg_color_title[0], bg_color_title[1], bg_color_title[2],
            int(255 * (1 - (100 - bgalpha) / 100.0)))
        self._centered_option = menu_centered
        self._drawselrect = draw_select
        self._font_color = font_color
        self._fsize = font_size
        self._fsize_title = font_size_title
        self._height = menu_height
        self._option_shadow = option_shadow
        self._opt_dy = option_margin
        self._rect_width = rect_width
        self._sel_color = color_selected
        self._surface = surface
        self._width = menu_width

        # Inner variables
        self._actual = self  # Actual menu
        self._option = []  # Option menu
        self._index = 0  # Selected index
        self._prev = None  # Previous menu
        self._prev_draw = None
        self._size = 0  # Menu total elements

        # Load fonts
        self._font = pygame.font.Font(font, self._fsize)
        self._font_title = pygame.font.Font(font, self._fsize_title)

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
        self._title = self._font_title.render(title, 1, self._font_color)
        title_width = self._title.get_size()[0]
        self._title_rect = [(self._posy, self._posx),
                            (self._posy + self._width, self._posx), (
                                self._posy + self._width,
                                self._posx + self._fsize_title / 2),
                            (self._posy + title_width + 25,
                             self._posx + self._fsize_title / 2), (
                                self._posy + title_width + 5,
                                self._posx + self._fsize_title + 5),
                            (self._posy, self._posx + self._fsize_title + 5)]
        self._title_pos = (self._posy + 5, self._posx - 3)

    def add_option(self, element_name, menu, *args):
        """
        Add option to menu
        
        :param element_name: Name of the element
        :param menu: Menu object
        :param args: Aditional arguments
        :return: 
        """
        self._actual._option.append([element_name, menu, args])
        self._actual._size += 1
        if self._actual._size > 1:
            dy = -self._actual._fsize / 2 - self._actual._opt_dy / 2
            self._actual._opt_posy += dy

    def add_selector(self, title, values, event, *args):
        """
        Add a selector to menu
        
        :param title: Title of the selector
        :param values: Values of the selector
        :param event: Event of the selector
        :param args: Aditional arguments
        :return: None
        """
        self._actual._option.append(
            [SELECTOR, Selector(title, values, event, *args)])
        self._actual._size += 1
        if self._actual._size > 1:
            dy = -self._actual._fsize / 2 - self._actual._opt_dy / 2
            self._actual._opt_posy += dy

    def down(self):
        """
        Move selection down
        
        :return: None
        """
        self._actual._index = (self._actual._index - 1) % self._actual._size

    def draw(self):
        """
        Draw menu to surface
        :return: 
        """
        # Draw background rectangle
        pygame.gfxdraw.filled_polygon(self._surface, self._actual._bgrect,
                                      self._actual._bgcolor)
        # Draw title
        pygame.gfxdraw.filled_polygon(self._surface, self._actual._title_rect,
                                      self._bg_color_title)
        self._surface.blit(self._actual._title, self._title_pos)

        # Draw options
        dy = 0
        for option in self._actual._option:
            # Si el tipo es un selector
            if option[0] == SELECTOR:
                # If selected index draw a rectangle
                if dy == self._actual._index:
                    text = self._actual._font.render(option[1].get(), 1,
                                                     self._actual._sel_color)
                    text_bg = self._actual._font.render(option[1].get(), 1,
                                                        SHADOW_COLOR)
                else:
                    text = self._actual._font.render(option[1].get(), 1,
                                                     self._actual._font_color)
                    text_bg = self._actual._font.render(option[1].get(), 1,
                                                        SHADOW_COLOR)
            else:
                # If selected index draw a rectangle
                if dy == self._actual._index:
                    text = self._actual._font.render(option[0], 1,
                                                     self._actual._sel_color)
                    text_bg = self._actual._font.render(option[0], 1,
                                                        SHADOW_COLOR)
                else:
                    text = self._actual._font.render(option[0], 1,
                                                     self._actual._font_color)
                    text_bg = self._actual._font.render(option[0], 1,
                                                        SHADOW_COLOR)
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
            # Si se tiene la seleccionada se dibuja el rectangulo
            if self._actual._drawselrect and (dy == self._actual._index):
                if not self._actual._centered_option:
                    text_dx_tl = -text_width
                else:
                    text_dx_tl = text_dx
                ycoords = self._actual._opt_posy + dy * (
                    self._actual._fsize + self._actual._opt_dy) + t_dy - 2
                pygame.draw.line(self._surface, self._actual._sel_color, (
                    self._actual._opt_posx + text_dx - 10,
                    self._actual._opt_posy + dy * (
                        self._actual._fsize + self._actual._opt_dy) + t_dy - 2),
                                 ((self._actual._opt_posx - text_dx_tl + 10,
                                   ycoords)), self._actual._rect_width)
                ycoords = self._actual._opt_posy + dy * (
                    self._actual._fsize + self._actual._opt_dy) - t_dy + 2
                pygame.draw.line(self._surface, self._actual._sel_color, (
                    self._actual._opt_posx + text_dx - 10,
                    self._actual._opt_posy + dy * (
                        self._actual._fsize + self._actual._opt_dy) - t_dy + 2),
                                 ((self._actual._opt_posx - text_dx_tl + 10,
                                   ycoords)), self._actual._rect_width)
                ycoords = self._actual._opt_posy + dy * (
                    self._actual._fsize + self._opt_dy) - t_dy + 2
                pygame.draw.line(self._surface, self._actual._sel_color, (
                    self._actual._opt_posx + text_dx - 10,
                    self._actual._opt_posy + dy * (
                        self._actual._fsize + self._actual._opt_dy) + t_dy - 2),
                                 ((self._actual._opt_posx + text_dx - 10,
                                   ycoords)), self._actual._rect_width)
                ycoords = self._actual._opt_posy + dy * (
                    self._actual._fsize + self._actual._opt_dy) - t_dy + 2
                pygame.draw.line(self._surface, self._actual._sel_color, (
                    self._actual._opt_posx - text_dx_tl + 10,
                    self._actual._opt_posy + dy * (
                        self._actual._fsize + self._actual._opt_dy) + t_dy - 2),
                                 ((self._actual._opt_posx - text_dx_tl + 10,
                                   ycoords)), self._actual._rect_width)
            dy += 1

    def left(self):
        """
        Move selector left
        
        :return: None
        """
        opcion = self._actual._option[self._actual._index][1]
        if isinstance(opcion, Selector):
            opcion.left()

    # noinspection PyAttributeOutsideInit
    def reset(self, total=0):
        """
        Reset menu
        :param total: 
        :return: 
        """
        assert isinstance(self._actual, Menu)
        # Se devuelve al menu padre
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

    def right(self):
        """
        Move selector to right
        
        :return: None
        """
        opcion = self._actual._option[self._actual._index][1]
        if isinstance(opcion, Selector):
            opcion.right()

    # noinspection PyAttributeOutsideInit
    def select(self):
        """
        Apply selected option
        :return: 
        """
        assert isinstance(self._actual, Menu)
        option = self._actual._option[self._actual._index][1]
        # If element is an Menu
        if isinstance(option, Menu):
            actual = self
            self._actual._actual = option._actual
            self._actual._prev = actual
            self._actual._prev_draw = self.draw
            self.draw = option.draw
        # If option is a number (internal functions)
        elif isinstance(option, types.IntType):
            # Back to menu
            if option == MENU_BACK:
                prev = self._actual._prev
                prev_draw = self._actual._prev_draw
                self.draw = prev_draw
                self._actual.index = 0
                self._actual = prev
                self._actual._prev = None
                self._actual._prev_draw = None
            # Exit program
            elif option == MENU_EXIT:
                exit()
        # If element is a function
        elif isinstance(option, types.FunctionType) or callable(option):
            if len(self._actual._option[self._actual.index][2]) > 0:
                option(self._actual._option[self._actual.index][2])
            else:
                option()
        # If null type
        elif isinstance(option, types.NoneType):
            pass
        # If element is a selector
        elif isinstance(option, Selector):
            option.apply()

    def up(self):
        """
        Option up
        
        :return: None
        """
        self._actual._index = (self._actual._index + 1) % self._actual._size
