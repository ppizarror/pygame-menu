# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

THEMES
Theme class and predefined themes.

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

import pygame as _pygame
import pygameMenu


class Theme(object):
    """
    Class defining the visual rendering of menus and widgets.

    :param background_color: Menu background color
    :type background_color: tuple, list
    :param selection_border_width: Border width of the highlight box
    :type selection_border_width: int
    :param selection_margin_x: X margin of selected highlight box
    :type selection_margin_x: int, float
    :param selection_margin_y: X margin of selected highlight box
    :type selection_margin_y: int, float
    :param selection_color: Color of the selecter widget
    :type selection_color: tuple
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
    :param title_background_color: Title background color
    :type title_background_color: tuple, list
    :param title_font: Optional title font, if None use the Menu default font
    :type title_font: basestring, NoneType
    :param title_font_color: Title font color, if None use the widget font color
    :type title_font_color: list, tuple, NoneType
    :param title_font_size: Font size of the title
    :type title_font_size: int
    :param title_shadow: Enable shadow on title
    :type title_shadow: bool
    :param title_shadow_color: Title shadow color
    :type title_shadow_color: list, tuple
    :param title_shadow_offset: Offset of shadow on title
    :type title_shadow_offset: int, float
    :param title_shadow_position: Position of the shadow on title
    :type title_shadow_position: basestring
    :param widget_font: Menu font file path or name
    :type widget_font: basestring
    :param widget_alignment: Widget default alignment
    :type widget_alignment: basestring
    :param widget_font_color: Color of the font
    :type widget_font_color: tuple, list
    :param widget_font_size: Font size
    :type widget_font_size: int
    :param widget_shadow: Indicate if a shadow is drawn on each widget
    :type widget_shadow: bool
    :param widget_shadow_color: Color of the shadow
    :type widget_shadow_color: tuple, list
    :param widget_shadow_offset: Offset of shadow
    :type widget_shadow_offset: int, float
    :param widget_shadow_position: Position of shadow
    :type widget_shadow_position: basestring
    """

    def __init__(self, **kwargs):
        self.background_color = self._get(kwargs, 'background_color',
                                          'color', (220, 220, 220))
        self.selection_border_width = self._get(kwargs, 'selection_border_width',
                                                int, 1)
        self.selection_margin_x = self._get(kwargs, 'selection_margin_x',
                                            float, 16.0)
        self.selection_margin_y = self._get(kwargs, 'selection_margin_y',
                                            float, 8.0)
        self.selection_color = self._get(kwargs, 'selection_color',
                                         'color', (0, 0, 0))
        self.scrollbar_color = self._get(kwargs, 'scrollbar_color',
                                         'color', (235, 235, 235))
        self.scrollbar_shadow = self._get(kwargs, 'scrollbar_shadow',
                                          bool, False)
        self.scrollbar_shadow_color = self._get(kwargs, 'scrollbar_shadow_color',
                                                'color', False)
        self.scrollbar_shadow_offset = self._get(kwargs, 'scrollbar_shadow_offset',
                                                 (int, float), False)
        self.scrollbar_shadow_position = self._get(kwargs, 'scrollbar_shadow_position',
                                                   'position', pygameMenu.locals.POSITION_NORTHWEST)
        self.scrollbar_slider_color = self._get(kwargs, 'scrollbar_slider_color',
                                                'color', (200, 200, 200))
        self.scrollbar_slider_pad = self._get(kwargs, 'scrollbar_slider_pad',
                                              (int, float), 0)
        self.scrollbar_thick = self._get(kwargs, 'scrollbar_thick',
                                         (int, float), 20)
        self.title_background_color = self._get(kwargs, 'title_background_color',
                                                'color', (70, 70, 70))
        self.title_font = self._get(kwargs, 'title_font',
                                    (str, type(None)), None)
        self.title_font_color = self._get(kwargs, 'title_font_color',
                                          'color', (220, 220, 220))
        self.title_font_size = self._get(kwargs, 'title_font_size',
                                         int, 45)
        self.title_shadow = self._get(kwargs, 'title_shadow',
                                      bool, False)
        self.title_shadow_color = self._get(kwargs, 'title_shadow_color',
                                            'color', (0, 0, 0))
        self.title_shadow_offset = self._get(kwargs, 'title_shadow_offset',
                                             (int, float), 2)
        self.title_shadow_position = self._get(kwargs, 'title_shadow_position',
                                               'position', pygameMenu.locals.POSITION_NORTHWEST)
        self.widget_font = self._get(kwargs, 'widget_font',
                                     str, pygameMenu.font.FONT_BEBAS)
        self.widget_alignment = self._get(kwargs, 'widget_alignment',
                                          'alignment', pygameMenu.locals.ALIGN_CENTER)
        self.widget_font_color = self._get(kwargs, 'widget_font_color',
                                           'color', (70, 70, 70))
        self.widget_font_size = self._get(kwargs, 'widget_font_size',
                                          int, 35)
        self.widget_shadow = self._get(kwargs, 'widget_shadow',
                                       bool, False)
        self.widget_shadow_color = self._get(kwargs, 'widget_shadow_color',
                                             'color', (0, 0, 0))
        self.widget_shadow_offset = self._get(kwargs, 'widget_shadow_offset',
                                              (int, float), 2)
        self.widget_shadow_position = self._get(kwargs, 'widget_shadow_position',
                                                'position', pygameMenu.locals.POSITION_NORTHWEST)

    def _get(self, params, key, allowed_types=None, default=None):
        """
        Return a value from a dictionary.

        :param params: parameters dictionnary
        :type params: dict
        :param key: key to look for
        :type key: basestring
        :param allowed_types: list of allowed types
        :type allowed_types: tuple
        :param default: default value to return
        :type default: any
        :return: the value associated to the key
        """
        if key not in params:
            return default

        value = params.pop(key)
        if allowed_types:
            if not isinstance(allowed_types, (tuple, list)):
                allowed_types = (allowed_types,)
            for valtype in allowed_types:
                if valtype == 'color':
                    pygameMenu.utils.assert_color(value)
                elif valtype == 'position':
                    pygameMenu.utils.assert_position(value)
                elif valtype == 'alignment':
                    pygameMenu.utils.assert_alignment(value)

            others = [t for t in allowed_types if t not in ('color', 'position', 'alignment')]
            if others:
                msg = "Theme.{} type shall be {} (got {})".format(key, others, type(value))
                assert isinstance(value, others), msg
        return value

    def apply_selected(self, surface, widget):
        """
        Draw the selection.

        :param surface: Surface to draw
        :type surface: pygame.surface.SurfaceType
        :param widget: Widget object
        :type widget: pygameMenu.widgets.core.widget.Widget
        :return: None
        """
        # noinspection PyProtectedMember
        rect = widget._rect.copy().inflate(self.selection_margin_x,
                                           self.selection_margin_y).move(0, -1)
        _pygame.draw.rect(surface, self.selection_color, rect, self.selection_border_width)


THEME_DEFAULT = Theme()

THEME_BLUE = Theme(widget_font_color=(61, 170, 220),
                   selection_color=(100, 62, 132),
                   title_font_color=(228, 230, 246),
                   title_background_color=(62, 149, 195),
                   background_color=(228, 230, 246))

THEME_GREEN = Theme(widget_font_color=(255, 255, 255),
                    selection_color=(125, 121, 114),
                    title_font_color=(228, 230, 246),
                    title_background_color=(125, 121, 114),
                    background_color=(186, 214, 177))

THEME_SOLARIZED = Theme(widget_font_color=(102, 122, 130),
                        selection_color=(207, 62, 132),
                        title_font_color=(38, 158, 151),
                        title_background_color=(4, 47, 58),
                        background_color=(239, 231, 211))
