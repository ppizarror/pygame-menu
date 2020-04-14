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

import copy

import pygameMenu
import pygameMenu.font
import pygameMenu.utils
import pygameMenu.widgets as _widgets


class Theme(object):
    """
    Class defining the visual rendering of menus and widgets.

    .. note:: All colors must be defined with a tuple of 3 or 4 numbers in the formats:

                  - (R,G,B)
                  - (R,G,B,A)
                  
              Red (R), Green (G) and Blue (B) must be numbers between 0 and 255.
              A means the alpha channel (opacity), if 0 the color is transparent, 100 means opaque.

    :param background_color: Menu background color
    :type background_color: tuple, list
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
    :param selection_color: Color of the selecter widget
    :type selection_color: tuple
    :param title_background_color: Title background color
    :type title_background_color: tuple, list
    :param title_bar_mode: Mode of drawing the title, use menubar widget modes
    :type title_bar_mode: int
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
    :param widget_font: Widget font path or name
    :type widget_font: basestring
    :param widget_font_color: Color of the font
    :type widget_font_color: tuple, list
    :param widget_font_size: Font size
    :type widget_font_size: int
    :param widget_selection_effect: Widget selection effect object
    :type widget_selection_effect: pygameMenu.widgets.core.selection.Selection
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
                                          'color', (220, 220, 220))  # type: (tuple, list)
        self.scrollbar_color = self._get(kwargs, 'scrollbar_color',
                                         'color', (235, 235, 235))  # type: (tuple, list)
        self.scrollbar_shadow = self._get(kwargs, 'scrollbar_shadow',
                                          bool, False)  # type: bool
        self.scrollbar_shadow_color = self._get(kwargs, 'scrollbar_shadow_color',
                                                'color', (0, 0, 0))  # type: bool
        self.scrollbar_shadow_offset = self._get(kwargs, 'scrollbar_shadow_offset',
                                                 (int, float), 2)  # type: (int, float)
        self.scrollbar_shadow_position = self._get(kwargs, 'scrollbar_shadow_position',
                                                   'position', pygameMenu.locals.POSITION_NORTHWEST)  # type: str
        self.scrollbar_slider_color = self._get(kwargs, 'scrollbar_slider_color',
                                                'color', (200, 200, 200))  # type: (tuple, list)
        self.scrollbar_slider_pad = self._get(kwargs, 'scrollbar_slider_pad',
                                              (int, float), 0)  # type: (int,float)
        self.scrollbar_thick = self._get(kwargs, 'scrollbar_thick',
                                         (int, float), 20)  # type: (int,float)
        self.selection_color = self._get(kwargs, 'selection_color',
                                         'color', (255, 255, 255))  # type: (tuple, list)
        self.title_background_color = self._get(kwargs, 'title_background_color',
                                                'color', (70, 70, 70))  # type: (tuple, list)
        self.title_bar_mode = self._get(kwargs, 'title_bar_mode',
                                        int, _widgets.MENUBAR_MODE_ADAPTATIVE)
        self.title_font = self._get(kwargs, 'title_font',
                                    str, pygameMenu.font.FONT_OPEN_SANS)  # type: str
        self.title_font_color = self._get(kwargs, 'title_font_color',
                                          'color', (220, 220, 220))  # type: (tuple, list)
        self.title_font_size = self._get(kwargs, 'title_font_size',
                                         int, 40)  # type: int
        self.title_shadow = self._get(kwargs, 'title_shadow',
                                      bool, False)  # type: bool
        self.title_shadow_color = self._get(kwargs, 'title_shadow_color',
                                            'color', (0, 0, 0))  # type: (tuple, list)
        self.title_shadow_offset = self._get(kwargs, 'title_shadow_offset',
                                             (int, float), 2)  # type: (int,float)
        self.title_shadow_position = self._get(kwargs, 'title_shadow_position',
                                               'position', pygameMenu.locals.POSITION_NORTHWEST)  # type: str
        self.widget_font = self._get(kwargs, 'widget_font',
                                     str, pygameMenu.font.FONT_OPEN_SANS)  # type: str
        self.widget_alignment = self._get(kwargs, 'widget_alignment',
                                          'alignment', pygameMenu.locals.ALIGN_CENTER)
        self.widget_font_color = self._get(kwargs, 'widget_font_color',
                                           'color', (70, 70, 70))  # type: (tuple, list)
        self.widget_font_size = self._get(kwargs, 'widget_font_size',
                                          int, 30)  # type: int
        self.widget_selection_effect = self._get(kwargs, 'widget_selectiom_effect',
                                                 _widgets.Selection,
                                                 _widgets.HighlightSelection())  # type: _widgets.Selection
        self.widget_shadow = self._get(kwargs, 'widget_shadow',
                                       bool, False)  # type: bool
        self.widget_shadow_color = self._get(kwargs, 'widget_shadow_color',
                                             'color', (0, 0, 0))  # type: (tuple, list)
        self.widget_shadow_offset = self._get(kwargs, 'widget_shadow_offset',
                                              (int, float), 2)  # type: (int,float)
        self.widget_shadow_position = self._get(kwargs, 'widget_shadow_position',
                                                'position', pygameMenu.locals.POSITION_NORTHWEST)  # type: str

        # Upon this, no more kwargs should exist, raise exception if there's more
        for invalid_keyword in kwargs.keys():
            raise ValueError('parameter Theme.{} does not exist'.format(invalid_keyword))

        # Assert values
        assert self.scrollbar_thick > 0, 'scrollbar thickness must be greater than zero'
        assert self.scrollbar_shadow_offset > 0, 'scrollbar shadow offset must be greater than zero'
        assert self.title_font_size > 0, 'title font size must be greater than zero'
        assert self.widget_font_size > 0, 'widget font size must be greater than zero'
        assert self.widget_shadow_offset > 0, 'widget shadow offset must be greater than zero'

        # Format colors
        self.background_color = self._format_opacity(self.background_color)
        self.scrollbar_color = self._format_opacity(self.scrollbar_color)
        self.scrollbar_shadow_color = self._format_opacity(self.scrollbar_shadow_color)
        self.scrollbar_slider_color = self._format_opacity(self.scrollbar_slider_color)
        self.selection_color = self._format_opacity(self.selection_color)
        self.title_background_color = self._format_opacity(self.title_background_color)
        self.title_font_color = self._format_opacity(self.title_font_color)
        self.title_shadow_color = self._format_opacity(self.title_shadow_color)

        # Configs
        self.widget_selection_effect.set_color(self.selection_color)

    def copy(self):
        """
        Creates a deep copy of the object.

        :return: Copied theme
        :rtype: Theme
        """
        return copy.deepcopy(self)

    @staticmethod
    def _format_opacity(color):
        """
        Adds opacity to a 3 channel color. (R,G,B) -> (R,G,B,A) if the color
        has not an alpha channel. Also updates the opacity to a number between
        0 and 255.

        :param color: Color tuple
        :type color: list, tuple
        :return: Color in the same format
        :rtype: list, tuple
        """
        if len(color) == 4:
            return color
        opacity = 255
        if isinstance(color, tuple):
            color = color[0], color[1], color[2], opacity
        elif isinstance(color, list):
            color = [color[0], color[1], color[2], opacity]
        else:
            raise ValueError('Invalid color {0}'.format(color))
        return color

    @staticmethod
    def _get(params, key, allowed_types=None, default=None):
        """
        Return a value from a dictionary.

        :param params: parameters dictionnary
        :type params: dict
        :param key: key to look for
        :type key: basestring
        :param allowed_types: list of allowed types
        :type allowed_types: any
        :param default: default value to return
        :type default: any
        :return: The value associated to the key
        :rtype: any
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
                for t in others:
                    msg = 'Theme.{} type shall be {} (got {})'.format(key, t, type(value))
                    assert isinstance(value, t), msg
        return value


THEME_DEFAULT = Theme()

THEME_BLACK = Theme(
    background_color=(0, 0, 0),
    selection_color=(255, 255, 255),
    title_background_color=(0, 0, 0),
    title_font_color=(255, 255, 255),
    widget_font_color=(150, 150, 150),
)

THEME_BLUE = Theme(
    background_color=(228, 230, 246),
    selection_color=(100, 62, 132),
    title_background_color=(62, 149, 195),
    title_font_color=(228, 230, 246),
    widget_font_color=(61, 170, 220),
)

THEME_GREEN = Theme(
    background_color=(186, 214, 177),
    selection_color=(125, 121, 114),
    title_background_color=(125, 121, 114),
    title_font_color=(228, 230, 246),
    widget_font_color=(255, 255, 255),
)

THEME_ORANGE = Theme(
    background_color=(228, 100, 36),
    selection_color=(255, 255, 255),
    title_background_color=(170, 65, 50),
    widget_font_color=(0, 0, 0),
    widget_font_size=30,
)

THEME_SOLARIZED = Theme(
    background_color=(239, 231, 211),
    selection_color=(207, 62, 132),
    title_background_color=(4, 47, 58),
    title_font_color=(38, 158, 151),
    widget_font_color=(102, 122, 130),
)
