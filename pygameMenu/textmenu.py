# coding=utf-8
"""
TEXT MENU
Menu with text and buttons.

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

# Library import
from pygameMenu.menu import Menu
import pygameMenu.config_textmenu as _cfg
import pygameMenu.config_menu as _cfg_menu
import pygameMenu.locals as _locals
import pygame as _pygame
import pygame.gfxdraw as _gfxdraw


# noinspection PyProtectedMember
class TextMenu(Menu):
    """
    Text menu object.
    """

    def __init__(self, surface, window_width, window_height, font, title,
                 text_centered=_cfg.TEXT_CENTERED,
                 text_color=_cfg.TEXT_FONT_COLOR,
                 text_fontsize=_cfg.MENU_FONT_TEXT_SIZE,
                 text_margin=_cfg.TEXT_MARGIN,
                 draw_text_region_x=_cfg.TEXT_DRAW_X,
                 **kwargs):
        """
        TextMenu constructor.

        :param surface: Pygame surface object
        :param window_width: Window width
        :param window_height: Window height
        :param font: Font file direction
        :param title: Title of the Menu
        :param text_centered: Indicate if text is centered
        :param text_color: Text color
        :param text_fontsize: Text font size
        :param text_margin: Line margin
        :param draw_text_region_x: X-Axis drawing region of the text
        :type window_width: int
        :type window_height: int
        :type font: str
        :type title: str
        :type text_centered: bool
        :type text_color: tuple
        :type text_fontsize: int
        :type text_margin: int
        :type draw_text_region_x: int
        """
        assert isinstance(draw_text_region_x, int)
        assert isinstance(text_centered, bool)
        assert isinstance(text_fontsize, int)
        assert isinstance(text_margin, int)

        # Other asserts
        assert draw_text_region_x >= 0, \
            'X-Axis drawing region of the text must be greather than zero'
        assert text_fontsize > 0, 'Text font size must be greather than zero'
        assert text_margin >= 0, \
            'Text margin must be greather or equal than zero'

        # Super call
        super(TextMenu, self).__init__(surface, window_width, window_height,
                                       font, title, **kwargs)

        # Store configuration
        self._centered_text = text_centered
        self._draw_text_region_x = draw_text_region_x
        self._font_textcolor = text_color
        self._font_textsize = text_fontsize
        self._textdy = text_margin

        # Load font
        self._fonttext = _pygame.font.Font(font, self._font_textsize)

        # Inner variables
        self._text = []

        # Position of text
        self._pos_text_x = int(
            self._width * (self._draw_text_region_x / 100.0)) + self._posy
        self._actual._opt_posy -= self._textdy / 2 + self._font_textsize / 2

    def add_line(self, text):
        """
        Add line of text.

        :param text: Line text
        :type text: str
        :return: None
        """
        assert isinstance(self._actual, TextMenu)
        assert isinstance(text, str)
        text = text.strip()
        self._actual._text.append(text)
        dy = -self._actual._font_textsize / 2 - self._actual._textdy / 2
        self._actual._opt_posy += dy

    def add_option(self, element_name, element, *args):
        """
        Add option to menu.

        :param element_name: Name of the element
        :param element: Menu object
        :param args: Aditional arguments
        :type element_name: basestring
        :type element: Menu, _locals._PymenuAction
        :return: None
        """
        a = isinstance(element, Menu)
        b = isinstance(element, _locals.PymenuAction)
        c = str(type(element)) == "<class 'pygameMenu.locals._PymenuAction'>"
        assert a or b or c, 'Element must be a Menu or PymenuAction'
        self._actual._option.append([element_name, element, args])
        self._actual._size += 1
        dy = -self._actual._fsize / 2 - self._actual._opt_dy / 2
        self._actual._opt_posy += dy

    def draw(self):
        """
        Draw menu on surface.

        :return: None
        """
        assert isinstance(self._actual, TextMenu)
        # Draw background rectangle
        _gfxdraw.filled_polygon(self._surface, self._actual._bgrect,
                                self._actual._bgcolor)
        # Draw title
        _gfxdraw.filled_polygon(self._surface, self._actual._title_rect,
                                self._bg_color_title)
        self._surface.blit(self._actual._title, self._title_pos)

        # Draw text
        dy = 0
        for linea in self._actual._text:
            text = self._actual._fonttext.render(linea, 1,
                                                 self._actual._font_textcolor)
            text_width = text.get_size()[0]
            if self._actual._centered_text:
                text_dx = -int(text_width / 2.0)
            else:
                text_dx = 0
            ycoords = self._actual._opt_posy + self._actual._textdy + dy * (
                    self._actual._font_textsize + self._actual._textdy)
            ycoords -= self._actual._font_textsize / 2
            self._surface.blit(text, (self._actual._pos_text_x + text_dx,
                                      ycoords))
            dy += 1
        dysum = dy * (self._actual._font_textsize + self._actual._textdy)
        dysum += 2 * self._actual._textdy + self._actual._font_textsize

        dy = 0
        dy_index = 0
        for option in self._actual._option:
            # If option is selector
            if option[0] == _locals._PYGAME_TYPE_SELECTOR:
                # If selected index then change color
                if dy == self._actual._index:
                    text = self._actual._font.render(option[1].get(), 1,
                                                     self._actual._sel_color)
                    text_bg = self._actual._font.render(option[1].get(), 1,
                                                        _cfg_menu.SHADOW_COLOR)
                else:
                    text = self._actual._font.render(option[1].get(), 1,
                                                     self._actual._font_color)
                    text_bg = self._actual._font.render(option[1].get(), 1,
                                                        _cfg_menu.SHADOW_COLOR)
            else:
                # If selected index then change color
                if dy == self._actual._index:
                    text = self._actual._font.render(option[0], 1,
                                                     self._actual._sel_color)
                    text_bg = self._actual._font.render(option[0], 1,
                                                        _cfg_menu.SHADOW_COLOR)
                else:
                    text = self._actual._font.render(option[0], 1,
                                                     self._actual._font_color)
                    text_bg = self._actual._font.render(option[0], 1,
                                                        _cfg_menu.SHADOW_COLOR)
            # Text font and size
            text_width, text_height = text.get_size()
            if self._actual._centered_option:
                text_dx = -int(text_width / 2.0)
                t_dy = -int(text_height / 2.0)
            else:
                text_dx = 0
                t_dy = 0
            # Draw fonts
            if self._actual._option_shadow:
                ycoords = self._actual._opt_posy + dy * (
                        self._actual._fsize + self._actual._opt_dy) + t_dy - 3
                self._surface.blit(text_bg,
                                   (self._actual._opt_posx + text_dx - 3,
                                    ycoords + dysum))
            ycoords = self._actual._opt_posy + dy * (
                    self._actual._fsize + self._actual._opt_dy) + t_dy
            self._surface.blit(text, (self._actual._opt_posx + text_dx,
                                      ycoords + dysum))
            # If selected option draw a rectangle
            if self._actual._drawselrect and (dy_index == self._actual._index):
                if not self._actual._centered_option:
                    text_dx_tl = -text_width
                else:
                    text_dx_tl = text_dx
                ycoords = self._actual._opt_posy + dy * (
                        self._actual._fsize + self._actual._opt_dy) + t_dy - 2
                _pygame.draw.line(self._surface, self._actual._sel_color, (
                    self._actual._opt_posx + text_dx - 10,
                    self._actual._opt_posy + dysum + dy * (
                            self._actual._fsize + self._actual._opt_dy) + t_dy - 2),
                                  ((self._actual._opt_posx - text_dx_tl + 10,
                                    ycoords + dysum)), self._actual._rect_width)
                ycoords = self._actual._opt_posy + dy * (
                        self._actual._fsize + self._actual._opt_dy) - t_dy + 2
                _pygame.draw.line(self._surface, self._actual._sel_color, (
                    self._actual._opt_posx + text_dx - 10,
                    self._actual._opt_posy + dysum + dy * (
                            self._actual._fsize + self._actual._opt_dy) - t_dy + 2),
                                  ((self._actual._opt_posx - text_dx_tl + 10,
                                    ycoords + dysum)), self._actual._rect_width)
                ycoords = self._actual._opt_posy + dy * (
                        self._actual._fsize + self._opt_dy) - t_dy + 2
                _pygame.draw.line(self._surface, self._actual._sel_color, (
                    self._actual._opt_posx + text_dx - 10,
                    self._actual._opt_posy + dysum + dy * (
                            self._actual._fsize + self._actual._opt_dy) + t_dy - 2),
                                  ((self._actual._opt_posx + text_dx - 10,
                                    ycoords + dysum)), self._actual._rect_width)
                ycoords = self._actual._opt_posy + dy * (
                        self._actual._fsize + self._actual._opt_dy) - t_dy + 2
                _pygame.draw.line(self._surface, self._actual._sel_color, (
                    self._actual._opt_posx - text_dx_tl + 10,
                    self._actual._opt_posy + dysum + dy * (
                            self._actual._fsize + self._actual._opt_dy) + t_dy - 2),
                                  ((self._actual._opt_posx - text_dx_tl + 10,
                                    ycoords + dysum)), self._actual._rect_width)
            dy += 1
            dy_index += 1
