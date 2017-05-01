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

# Import configuration constants
from config import *

# Library imports
from selector import Selector
import pygame
import pygame.gfxdraw
import types

# Constants
MENU_BACK = 0
MENU_EXIT = 1


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
        self.height = menu_height
        self.option_shadow = option_shadow
        self.opt_dy = option_margin
        self.rectwidth = rect_width
        self.selectedcolor = color_selected
        self.surface = surface
        self.width = menu_width

        # Inner variables
        self.actual = self  # Actual menu
        self.opciones = []  # Option menu
        self.index = 0  # Selected index
        self.prev = None  # Previous menu
        self.prevDraw = None
        self.size = 0  # Menu total elements

        # Load fonts
        self.font = pygame.font.Font(font, self._fsize)
        self.fonttitle = pygame.font.Font(font, self._fsize_title)

        # Position of menu
        self.posx = (window_width - self.width) / 2
        self.posy = (window_height - self.height) / 2
        self.bgRect = [(self.posx, self.posy),
                       (self.posx + self.width, self.posy),
                       (self.posx + self.width, self.posy + self.height),
                       (self.posx, self.posy + self.height)]
        self.drawRegionX = draw_region_x
        self.drawRegionY = draw_region_y

        # Option position
        self._opt_posx = int(
            self.width * (self.drawRegionX / 100.0)) + self.posx
        self._opt_posy = int(
            self.height * (self.drawRegionY / 100.0)) + self.posy

        # Title properties
        self.title = self.fonttitle.render(title, 1, self._font_color)
        title_width = self.title.get_size()[0]
        self.titleRect = [(self.posx, self.posy),
                          (self.posx + self.width, self.posy), (
                              self.posx + self.width,
                              self.posy + self._fsize_title / 2),
                          (self.posx + title_width + 25,
                           self.posy + self._fsize_title / 2), (
                              self.posx + title_width + 5,
                              self.posy + self._fsize_title + 5),
                          (self.posx, self.posy + self._fsize_title + 5)]
        self.titlePos = (self.posx + 5, self.posy - 3)

    def add_option(self, element_name, menu, *args):
        """
        Add option to menu
        
        :param element_name: Name of the element
        :param menu: Menu object
        :param args: Aditional arguments
        :return: 
        """
        self.actual.opciones.append([element_name, menu, args])
        self.actual.size += 1
        if self.actual.size > 1:
            dy = -self.actual._fsize / 2 - self.actual.opt_dy / 2
            self.actual._opt_posy += dy

    def add_selector(self, title, values, event, *args):
        """
        Add a selector to menu
        
        :param title: Title of the selector
        :param values: Values of the selector
        :param event: Event of the selector
        :param args: Aditional arguments
        :return: None
        """
        self.actual.opciones.append(
            [SELECTOR, Selector(title, values, event, *args)])
        self.actual.size += 1
        if self.actual.size > 1:
            dy = -self.actual._fsize / 2 - self.actual.opt_dy / 2
            self.actual._opt_posy += dy

    def down(self):
        """
        Move selection down
        
        :return: None
        """
        self.actual.index = (self.actual.index - 1) % self.actual.size

    def draw(self):
        """
        Draw menu to surface
        :return: 
        """
        # Draw background rectangle
        pygame.gfxdraw.filled_polygon(self.surface, self.actual.bgRect,
                                      self.actual._bgcolor)
        # Draw title
        pygame.gfxdraw.filled_polygon(self.surface, self.actual.titleRect,
                                      self._bg_color_title)
        self.surface.blit(self.actual.title, self.titlePos)

        # Draw options
        dy = 0
        for option in self.actual.opciones:
            # Si el tipo es un selector
            if option[0] == SELECTOR:
                # If selected index draw a rectangle
                if dy == self.actual.index:
                    text = self.actual.font.render(option[1].get(), 1,
                                                   self.actual.selectedcolor)
                    text_bg = self.actual.font.render(option[1].get(), 1,
                                                      SHADOW)
                else:
                    text = self.actual.font.render(option[1].get(), 1,
                                                   self.actual._font_color)
                    text_bg = self.actual.font.render(option[1].get(), 1,
                                                      SHADOW)
            else:
                # If selected index draw a rectangle
                if dy == self.actual.index:
                    text = self.actual.font.render(option[0], 1,
                                                   self.actual.selectedcolor)
                    text_bg = self.actual.font.render(option[0], 1, SHADOW)
                else:
                    text = self.actual.font.render(option[0], 1,
                                                   self.actual._font_color)
                    text_bg = self.actual.font.render(option[0], 1, SHADOW)
            # Text anchor
            text_width, text_height = text.get_size()
            text_dy = -int(text_height / 2.0)
            if self.actual._centered_option:
                text_dx = -int(text_width / 2.0)
            else:
                text_dx = 0
            # Draw fonts
            if self.actual.option_shadow:
                ycoords = self.actual._opt_posy + dy * (
                    self.actual._fsize + self.actual.opt_dy) + text_dy - 3
                self.surface.blit(text_bg,
                                  (self.actual._opt_posx + text_dx - 3,
                                   ycoords))
            ycoords = self.actual._opt_posy + dy * (
                self.actual._fsize + self.actual.opt_dy) + text_dy
            self.surface.blit(text, (self.actual._opt_posx + text_dx,
                                     ycoords))
            # Si se tiene la seleccionada se dibuja el rectangulo
            if self.actual._drawselrect and (dy == self.actual.index):
                if not self.actual._centered_option:
                    text_dx_tl = -text_width
                else:
                    text_dx_tl = text_dx
                ycoords = self.actual._opt_posy + dy * (
                    self.actual._fsize + self.actual.opt_dy) + text_dy - 2
                pygame.draw.line(self.surface, self.actual.selectedcolor, (
                    self.actual._opt_posx + text_dx - 10,
                    self.actual._opt_posy + dy * (
                        self.actual._fsize + self.actual.opt_dy) + text_dy - 2),
                                 ((self.actual._opt_posx - text_dx_tl + 10,
                                   ycoords)), self.actual.rectwidth)
                ycoords = self.actual._opt_posy + dy * (
                    self.actual._fsize + self.actual.opt_dy) - text_dy + 2
                pygame.draw.line(self.surface, self.actual.selectedcolor, (
                    self.actual._opt_posx + text_dx - 10,
                    self.actual._opt_posy + dy * (
                        self.actual._fsize + self.actual.opt_dy) - text_dy + 2),
                                 ((self.actual._opt_posx - text_dx_tl + 10,
                                   ycoords)), self.actual.rectwidth)
                ycoords = self.actual._opt_posy + dy * (
                    self.actual._fsize + self.opt_dy) - text_dy + 2
                pygame.draw.line(self.surface, self.actual.selectedcolor, (
                    self.actual._opt_posx + text_dx - 10,
                    self.actual._opt_posy + dy * (
                        self.actual._fsize + self.actual.opt_dy) + text_dy - 2),
                                 ((self.actual._opt_posx + text_dx - 10,
                                   ycoords)), self.actual.rectwidth)
                ycoords = self.actual._opt_posy + dy * (
                    self.actual._fsize + self.actual.opt_dy) - text_dy + 2
                pygame.draw.line(self.surface, self.actual.selectedcolor, (
                    self.actual._opt_posx - text_dx_tl + 10,
                    self.actual._opt_posy + dy * (
                        self.actual._fsize + self.actual.opt_dy) + text_dy - 2),
                                 ((self.actual._opt_posx - text_dx_tl + 10,
                                   ycoords)), self.actual.rectwidth)
            dy += 1

    def left(self):
        """
        Move selector left
        
        :return: None
        """
        opcion = self.actual.opciones[self.actual.index][1]
        if isinstance(opcion, Selector):
            opcion.left()

    # noinspection PyAttributeOutsideInit
    def reset(self, total=0):
        """
        Reset menu
        :param total: 
        :return: 
        """
        # Se devuelve al menu padre
        i = 0
        while True:
            if self.actual.prev is not None:
                prev = self.actual.prev
                prev_draw = self.actual.prevDraw
                self.draw = prev_draw
                self.actual.index = 0
                self.actual = prev
                self.actual.prev = None
                self.actual.prevDraw = None
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
        opcion = self.actual.opciones[self.actual.index][1]
        if isinstance(opcion, Selector):
            opcion.right()

    # noinspection PyAttributeOutsideInit
    def select(self):
        """
        Apply selected option
        :return: 
        """
        opcion = self.actual.opciones[self.actual.index][1]
        # If element is an Menu
        if isinstance(opcion, Menu):
            actual = self
            self.actual.actual = opcion.actual
            self.actual.prev = actual
            self.actual.prevDraw = self.draw
            self.draw = opcion.draw
        # If option is a number (internal functions)
        elif isinstance(opcion, types.IntType):
            # Back to menu
            if opcion == MENU_BACK:
                prev = self.actual.prev
                prev_draw = self.actual.prevDraw
                self.draw = prev_draw
                self.actual.index = 0
                self.actual = prev
                self.actual.prev = None
                self.actual.prevDraw = None
            # Exit program
            elif opcion == MENU_EXIT:
                exit()
        # If element is a function
        elif isinstance(opcion, types.FunctionType):
            if len(self.actual.opciones[self.actual.index][2]) > 0:
                opcion(self.actual.opciones[self.actual.index][2])
            else:
                opcion()
        # If null type
        elif isinstance(opcion, types.NoneType):
            pass
        # If element is a selector
        elif isinstance(opcion, Selector):
            opcion.apply()

    def up(self):
        """
        Option up
        
        :return: None
        """
        self.actual.index = (self.actual.index + 1) % self.actual.size
