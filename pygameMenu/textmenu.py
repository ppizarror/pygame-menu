# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEXT MENU
Menu with text and buttons.

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

import pygameMenu.config as _cfg
import pygameMenu.font as _fonts
import pygameMenu.locals as _locals

from pygameMenu.menu import Menu


# noinspection PyProtectedMember
class TextMenu(Menu):
    """
    Menu with text lines.
    """

    def __init__(self,
                 surface,
                 font,
                 title,
                 draw_text_region_x=_cfg.TEXT_DRAW_X,
                 text_align=_locals.ALIGN_LEFT,
                 text_color=_cfg.TEXT_FONT_COLOR,
                 text_fontsize=_cfg.MENU_FONT_TEXT_SIZE,
                 text_margin=_cfg.TEXT_MARGIN,
                 **kwargs
                 ):
        """
        TextMenu constructor. Columns and rows not supported.

        :param surface: Pygame surface object
        :type surface: pygame.surface.SurfaceType
        :param font: Font file direction
        :type font: str
        :param title: Title of the Menu
        :type title: str
        :param draw_text_region_x: X-Axis drawing region of the text
        :type draw_text_region_x: int, float
        :param text_align: Text default alignment
        :type text_align: basestring
        :param text_color: Text color
        :type text_color: tuple
        :param text_fontsize: Text font size
        :type text_fontsize: int
        :param text_margin: Line margin
        :type text_margin: int
        :param kwargs: Additional parameters
        """
        assert isinstance(draw_text_region_x, int) or \
               isinstance(draw_text_region_x, float)
        assert isinstance(text_align, str)
        assert isinstance(text_color, tuple)
        assert isinstance(text_fontsize, int)
        assert isinstance(text_margin, int)

        assert draw_text_region_x >= 0, 'draw_text_region_x of the text must be greater or equal than zero'
        assert text_fontsize > 0, 'text_fontsize must be greater than zero'
        assert text_margin >= 0, 'text_margin must be greater or equal than zero'

        # Columns and rows not supported in textmenu
        _kwkeys = kwargs.keys()
        assert not ('rows' in _kwkeys or 'columns' in _kwkeys or 'column_weights' in _kwkeys or
                    'force_fit_text' in _kwkeys), 'columns and rows not supported in TextMenu'

        # Super call
        super(TextMenu, self).__init__(surface,
                                       font,
                                       title,
                                       **kwargs)

        # Store configuration
        self._draw_text_region_x = draw_text_region_x
        self._font_textcolor = text_color
        self._font_textsize = text_fontsize
        self._text_align = text_align
        self._textdy = text_margin

        # Load font
        self._fonttext = _fonts.get_font(font, self._font_textsize)

        # Inner variables
        self._text = []
        self._text_render = {}

    def add_line(self, text):
        """
        Add line of text.

        :param text: Line text
        :type text: str
        :return: None
        """
        assert isinstance(text, str), 'line text must be a string'
        text = text.strip()
        self._text.append(text)

    def _get_text_render(self, line_number):
        """
        Return the rendered surface of a given line.

        :param line_number: Line number
        :type line_number: int
        :return: Line surface
        :rtype: pygame.surface.SurfaceType
        """
        assert isinstance(line_number, int)
        _line_hash = hash(self._text[line_number])
        if _line_hash not in self._text_render.keys():
            self._text_render[_line_hash] = self._fonttext.render(self._text[line_number], 1, self._font_textcolor)
        return self._text_render[_line_hash]

    def _get_text_width(self, line_number):
        """
        Return line rendered surface width.

        :param line_number: Line number
        :type line_number: int
        :return: Line surface width
        :rtype: int
        """
        return self._get_text_render(line_number).get_size()[0]

    def _get_text_pos(self, line_number):
        """
        Return line rendered surface width.

        :param line_number: Line number
        :type line_number: int
        :return: Text position (x,y)
        :rtype: tuple
        """
        assert isinstance(line_number, int)
        text_width = self._get_text_width(line_number)

        # Check text align
        if self._text_align == _locals.ALIGN_CENTER:
            text_dx = -int(self._width * (self._draw_text_region_x / 100.0)) + \
                      self._width / 2 - text_width / 2
        elif self._text_align == _locals.ALIGN_LEFT:
            text_dx = 0
        elif self._text_align == _locals.ALIGN_RIGHT:
            text_dx = -2 * int(self._width * (self._draw_text_region_x / 100.0)) \
                      - text_width + self._width
        else:
            text_dx = 0

        x_coord = int(self._width * (self._draw_text_region_x / 100.0)) + self._posx
        y_coord = self._posy + self._option_offsety + self._textdy + line_number * (
                self._font_textsize + self._textdy) - self._font_textsize / 2
        return x_coord + text_dx, y_coord

    def _get_option_pos(self, index, x=True, y=True):
        """
        See upper class doc.
        """
        dysum = len(self._text) * (self._font_textsize + self._textdy)
        dysum += 2 * self._textdy + self._font_textsize

        rect = self._option[index].get_rect()
        if self._widget_align == _locals.ALIGN_CENTER:
            option_dx = -int(rect.width / 2.0)
        elif self._widget_align == _locals.ALIGN_CENTER:
            option_dx = -self._width / 2 + self._selected_inflate_x
        elif self._widget_align == _locals.ALIGN_CENTER:
            option_dx = self._width / 2 - rect.width - self._selected_inflate_x
        else:
            option_dx = 0
        t_dy = - rect.height

        x_coord = self._column_posx[0] + option_dx
        y_coord = self._option_offsety + index * (self._fsize + self._opt_dy) + t_dy + dysum
        return x_coord, y_coord, x_coord + rect.width, y_coord + rect.height

    def draw(self):
        """
        See upper class doc.
        """
        super(TextMenu, self).draw()
        for line in range(len(self._text)):
            self._surface.blit(self._get_text_render(line), self._get_text_pos(line))
