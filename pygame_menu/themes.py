# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

THEMES
Theme class and predefined themes.

NOTE: pygame-menu v3 will not provide new widgets or functionalities, consider
upgrading to the latest version.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2021 Pablo Pizarro R. @ppizarror

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

import pygame_menu.font
import pygame_menu.utils as _utils
import pygame_menu.widgets as _widgets
from pygame_menu.baseimage import BaseImage

import copy


class Theme(object):
    """
    Class defining the visual rendering of menus and widgets.

    .. note::

        All colors must be defined with a tuple of 3 or 4 numbers in the formats:

            - (R,G,B)
            - (R,G,B,A)

        Red (R), Green (G) and Blue (B) must be numbers between 0 and 255.
        A means the alpha channel (opacity), if 0 the color is transparent, 100 means opaque.

    .. note::

        Themes only modify visual behaviour of the Menu. For other options
        like rows/columns, enabling or disabling overflow, position or menu
        width/height see Menu parameters.

    :param background_color: Menu background color
    :type background_color: tuple, list, :py:class:`pygame_menu.baseimage.BaseImage`
    :param cursor_color: Color of cursor
    :type cursor_color: tuple, list
    :param cursor_selection_color: Selection box color
    :type cursor_selection_color: tuple, list
    :param focus_background_color: Color of the widget focus, this must be a tuple of 4 elements. Also must be transparent
    :type focus_background_color: tuple, list
    :param menubar_close_button: Draw a back-box button on header to close the menu, if user moves through nested submenus this buttons turns to a back-arrow
    :type menubar_close_button: bool
    :param scrollarea_outer_margin: Outer scroll area margin (px), the tuple is added to computed scroll area width/height, it can add a margin to bottom/right scrolls after widgets. If value less than 1 use percentage of width/height. Default *(0,0)*. It cannot be negative values
    :type scrollarea_outer_margin: tuple, list
    :param scrollbar_color: Scrollbars color
    :type scrollbar_color: tuple, list
    :param scrollbar_shadow: Indicate if a shadow is drawn on each scrollbar
    :type scrollbar_shadow: bool
    :param scrollbar_shadow_color: Color of the scrollbar shadow
    :type scrollbar_shadow_color: tuple, list
    :param scrollbar_shadow_offset: Offset of the scrollbar shadow
    :type scrollbar_shadow_offset: int, float
    :param scrollbar_shadow_position: Position of the scrollbar shadow. See :py:mod:`pygame_menu.locals`
    :type scrollbar_shadow_position: str
    :param scrollbar_slider_color: Color of the sliders
    :type scrollbar_slider_color: tuple, list
    :param scrollbar_slider_pad: Space between slider and scrollbars borders
    :type scrollbar_slider_pad: int, float
    :param scrollbar_thick: Scrollbar thickness
    :type scrollbar_thick: int, float
    :param selection_color: Color of the selected widget, it affects font color and the selection effect
    :type selection_color: tuple, list
    :param surface_clear_color: Surface clear color before applying background function
    :type surface_clear_color: tuple, list
    :param title_background_color: Title background color
    :type title_background_color: tuple, list
    :param title_bar_style: Style of the title, use menubar widget styles
    :type title_bar_style: int
    :param title_font: Title font path or name
    :type title_font: str
    :param title_font_antialias: Title font renders with antialiasing
    :type title_font_antialias: bool
    :param title_font_color: Title font color, if None use the widget font color
    :type title_font_color: tuple, list, None
    :param title_font_size: Font size of the title
    :type title_font_size: int
    :param title_offset: Offset (x-position,y-position) of title (px). Default *(0,0)*
    :type title_offset: tuple, list
    :param title_shadow: Enable shadow on title
    :type title_shadow: bool
    :param title_shadow_color: Title shadow color
    :type title_shadow_color: tuple, list
    :param title_shadow_offset: Offset of shadow on title
    :type title_shadow_offset: int, float
    :param title_shadow_position: Position of the shadow on title. See :py:mod:`pygame_menu.locals`
    :type title_shadow_position: str
    :param widget_alignment: Widget default `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html#widgets-alignment>`_
    :type widget_alignment: str
    :param widget_background_color: Background color of a widget, it can be a color or a BaseImage object. Background fills the entire widget + the padding
    :type widget_background_color: tuple, list, :py:class:`pygame_menu.baseimage.BaseImage`, None
    :param widget_background_inflate: Inflate background in *(x,y)* in px. By default it uses the highlight margin. This parameter is visual only. For modifying widget size use padding instead
    :type widget_background_inflate: tuple, list
    :param widget_font: Widget font path or name
    :type widget_font: str
    :param widget_font_antialias: Widget font renders with antialiasing
    :type widget_font_antialias: bool
    :param widget_font_background_color: Widget font background color. By default it is None. If None the value will be the same as ``background_color`` if it's is a color object and if ``widget_font_background_color_from_menu`` is True and ``widget_background_color`` is None
    :type widget_font_background_color: tuple, list, None
    :param widget_font_background_color_from_menu: Use menu background color as font background color. Disabled by default
    :type widget_font_background_color_from_menu: bool
    :param widget_font_color: Color of the font
    :type widget_font_color: tuple, list
    :param widget_font_size: Font size
    :type widget_font_size: int
    :param widget_margin: Horizontal and vertical margin of each element in Menu (px). Default *(0,10)*
    :type widget_margin: tuple, list
    :param widget_padding: Padding of the widget according to CSS rules. It can be a single digit, or a tuple of 2, 3, or 4 elements. Padding modifies widget width/height
    :type widget_padding: int, float, tuple, list
    :param widget_offset: *(x, y)* axis offset of widgets within Menu (px) respect to top-left corner. If value less than 1 use percentage of width/height. Default *(0,0)*. It cannot be negative values
    :type widget_offset: tuple, list
    :param widget_selection_effect: Widget selection effect object. This is visual-only, the selection properties does not affect widget height/width
    :type widget_selection_effect: :py:class:`pygame_menu.widgets.core.Selection`
    :param widget_shadow: Indicate if the widget text shadow is enabled
    :type widget_shadow: bool
    :param widget_shadow_color: Color of the widget shadow
    :type widget_shadow_color: tuple, list
    :param widget_shadow_offset: Offset of the widget shadow
    :type widget_shadow_offset: int, float
    :param widget_shadow_position: Position of shadow. See :py:mod:`pygame_menu.locals`
    :type widget_shadow_position: str
    """

    def __init__(self, **kwargs):

        self.background_color = self._get(kwargs, 'background_color', 'color_image',
                                          (220, 220, 220))  # type: (tuple, BaseImage)
        self.cursor_color = self._get(kwargs, 'cursor_color', 'color',
                                      (0, 0, 0))  # type: tuple
        self.cursor_selection_color = self._get(kwargs, 'cursor_selection_color', 'color',
                                                (30, 30, 30, 120))  # type: tuple
        self.focus_background_color = self._get(kwargs, 'focus_background_color', 'color',
                                                (0, 0, 0, 180))  # type: tuple
        self.menubar_close_button = self._get(kwargs, 'menubar_close_button', bool,
                                              True)  # type: bool
        self.scrollarea_outer_margin = self._get(kwargs, 'scrollarea_outer_margin', 'tuple2',
                                                 (0, 0))  # type: tuple
        self.scrollbar_color = self._get(kwargs, 'scrollbar_color', 'color',
                                         (220, 220, 220))  # type: tuple
        self.scrollbar_shadow = self._get(kwargs, 'scrollbar_shadow', bool,
                                          False)  # type: bool
        self.scrollbar_shadow_color = self._get(kwargs, 'scrollbar_shadow_color', 'color',
                                                (0, 0, 0))  # type: bool
        self.scrollbar_shadow_offset = self._get(kwargs, 'scrollbar_shadow_offset', (int, float),
                                                 2)  # type: (int, float)
        self.scrollbar_shadow_position = self._get(kwargs, 'scrollbar_shadow_position', 'position',
                                                   pygame_menu.locals.POSITION_NORTHWEST)  # type: str
        self.scrollbar_slider_color = self._get(kwargs, 'scrollbar_slider_color', 'color',
                                                (200, 200, 200))  # type: tuple
        self.scrollbar_slider_pad = self._get(kwargs, 'scrollbar_slider_pad', (int, float),
                                              0)  # type: (int,float)
        self.scrollbar_thick = self._get(kwargs, 'scrollbar_thick', (int, float),
                                         20)  # type: (int,float)
        self.selection_color = self._get(kwargs, 'selection_color', 'color',
                                         (255, 255, 255))  # type: tuple
        self.surface_clear_color = self._get(kwargs, 'surface_clear_color', 'color',
                                             (0, 0, 0))  # type: tuple
        self.title_background_color = self._get(kwargs, 'title_background_color', 'color',
                                                (70, 70, 70))  # type: tuple
        self.title_bar_style = self._get(kwargs, 'title_bar_style', int,
                                         _widgets.MENUBAR_STYLE_ADAPTIVE)  # type: int
        self.title_font = self._get(kwargs, 'title_font', str,
                                    pygame_menu.font.FONT_OPEN_SANS)  # type: str
        self.title_font_antialias = self._get(kwargs, 'title_font_antialias', bool,
                                              True)  # type: bool
        self.title_font_color = self._get(kwargs, 'title_font_color', 'color',
                                          (220, 220, 220))  # type: tuple
        self.title_font_size = self._get(kwargs, 'title_font_size', int,
                                         40)  # type: int
        self.title_offset = self._get(kwargs, 'title_offset', 'tuple2',
                                      (5, -1))  # type: tuple
        self.title_shadow = self._get(kwargs, 'title_shadow', bool,
                                      False)  # type: bool
        self.title_shadow_color = self._get(kwargs, 'title_shadow_color', 'color',
                                            (0, 0, 0))  # type: tuple
        self.title_shadow_offset = self._get(kwargs, 'title_shadow_offset', (int, float),
                                             2)  # type: (int,float)
        self.title_shadow_position = self._get(kwargs, 'title_shadow_position', 'position',
                                               pygame_menu.locals.POSITION_NORTHWEST)  # type: str
        self.widget_font = self._get(kwargs, 'widget_font', str,
                                     pygame_menu.font.FONT_OPEN_SANS)  # type: str
        self.widget_alignment = self._get(kwargs, 'widget_alignment', 'alignment',
                                          pygame_menu.locals.ALIGN_CENTER)  # type: str
        self.widget_background_color = self._get(kwargs, 'widget_background_color', 'color_image_none',
                                                 )  # type: (tuple, BaseImage, type(None))
        self.widget_background_inflate = self._get(kwargs, 'background_inflate', 'tuple2',
                                                   (0, 0))  # type: tuple
        self.widget_font_antialias = self._get(kwargs, 'widget_font_antialias', bool,
                                               True)  # type: bool
        self.widget_font_background_color = self._get(kwargs, 'widget_font_background_color', 'color_none',
                                                      )  # type: tuple
        self.widget_font_background_color_from_menu = self._get(kwargs, 'widget_font_background_color_from_menu',
                                                                bool, False)  # type: bool
        self.widget_font_color = self._get(kwargs, 'widget_font_color', 'color',
                                           (70, 70, 70))  # type: tuple
        self.widget_font_size = self._get(kwargs, 'widget_font_size', int,
                                          30)  # type: int
        self.widget_margin = self._get(kwargs, 'widget_margin', 'tuple2',
                                       (0, 10))  # type: tuple
        self.widget_padding = self._get(kwargs, 'widget_padding', (int, float, tuple, list),
                                        0)  # type: (int,float,tuple)
        self.widget_offset = self._get(kwargs, 'widget_offset', 'tuple2',
                                       (0, 0))  # type: tuple
        self.widget_selection_effect = self._get(kwargs, 'widget_selection_effect', _widgets.core.Selection,
                                                 _widgets.HighlightSelection())  # type: _widgets.core.Selection
        self.widget_shadow = self._get(kwargs, 'widget_shadow', bool,
                                       False)  # type: bool
        self.widget_shadow_color = self._get(kwargs, 'widget_shadow_color', 'color',
                                             (0, 0, 0))  # type: tuple
        self.widget_shadow_offset = self._get(kwargs, 'widget_shadow_offset', (int, float),
                                              2)  # type: (int,float)
        self.widget_shadow_position = self._get(kwargs, 'widget_shadow_position', 'position',
                                                pygame_menu.locals.POSITION_NORTHWEST)  # type: str

        # Upon this, no more kwargs should exist, raise exception if there's more
        for invalid_keyword in kwargs.keys():
            msg = 'parameter Theme.{} does not exist'.format(invalid_keyword)
            raise ValueError(msg)

        # Test purpose only, if True disables any validation
        self._disable_validation = False

    def validate(self):
        """
        Validate the values of the theme. If there's a invalid parameter throws an
        AssertionError.

        This function also converts all lists to tuples. This is done because lists
        are mutable.

        :return: None
        """
        if self._disable_validation:
            return

        # Size asserts
        assert self.scrollbar_shadow_offset > 0, 'scrollbar shadow offset must be greater than zero'
        assert self.scrollbar_slider_pad >= 0, 'slider pad must be equal or greater than zero'
        assert self.scrollbar_thick > 0, 'scrollbar thickness must be greater than zero'
        assert self.title_font_size > 0, 'title font size must be greater than zero'
        assert self.widget_font_size > 0, 'widget font size must be greater than zero'
        assert self.widget_shadow_offset > 0, 'widget shadow offset must be greater than zero'

        # Format colors, this converts all color lists to tuples automatically
        self.background_color = self._format_opacity(self.background_color)  # type: tuple
        self.cursor_color = self._format_opacity(self.cursor_color)  # type: tuple
        self.cursor_selection_color = self._format_opacity(self.cursor_selection_color)  # type: tuple
        self.focus_background_color = self._format_opacity(self.focus_background_color)  # type: tuple
        self.scrollbar_color = self._format_opacity(self.scrollbar_color)  # type: tuple
        self.scrollbar_shadow_color = self._format_opacity(self.scrollbar_shadow_color)  # type: tuple
        self.scrollbar_slider_color = self._format_opacity(self.scrollbar_slider_color)  # type: tuple
        self.selection_color = self._format_opacity(self.selection_color)  # type: tuple
        self.surface_clear_color = self._format_opacity(self.surface_clear_color)  # type: tuple
        self.title_background_color = self._format_opacity(self.title_background_color)  # type: tuple
        self.title_font_color = self._format_opacity(self.title_font_color)  # type: tuple
        self.title_shadow_color = self._format_opacity(self.title_shadow_color)  # type: tuple
        self.widget_background_color = self._format_opacity(self.widget_background_color)  # type: tuple
        self.widget_font_background_color = self._format_opacity(self.widget_font_background_color)  # type: tuple
        self.widget_font_color = self._format_opacity(self.widget_font_color)  # type: tuple

        # List to tuple
        self.scrollarea_outer_margin = self._vec_to_tuple(self.scrollarea_outer_margin, 2)  # type: tuple
        self.title_offset = self._vec_to_tuple(self.title_offset, 2)  # type: tuple
        self.widget_background_inflate = self._vec_to_tuple(self.widget_background_inflate, 2)  # type: tuple
        self.widget_margin = self._vec_to_tuple(self.widget_margin, 2)  # type: tuple
        if isinstance(self.widget_padding, (tuple, list)):
            self.widget_padding = self._vec_to_tuple(self.widget_padding)  # type: tuple
            assert 2 <= len(self.widget_padding) <= 4, 'widget padding tuple length must be 2, 3 or 4'
            for p in self.widget_padding:
                assert p >= 0, 'all padding elements must be equal or greater than zero'
        else:
            assert isinstance(self.widget_padding, (int, float))
            assert self.widget_padding >= 0, 'padding cant be a negative number'
        self.widget_offset = self._vec_to_tuple(self.widget_offset, 2)  # type: tuple

        # Check sizes
        assert self.scrollarea_outer_margin[0] >= 0 and self.scrollarea_outer_margin[1] >= 0, \
            'scroll area outer margin must be equal or greater than zero'
        assert self.widget_offset[0] >= 0 and self.widget_offset[1] >= 0, \
            'widget offset must be equal or greater than zero'

        # Configs
        self.widget_selection_effect.set_color(self.selection_color)

        # Color asserts
        assert self.focus_background_color[3] != 0, \
            'focus background color cannot be fully transparent, suggested opacity between 1 and 255'

    def set_background_color_opacity(self, opacity):
        """
        Modify menu background color with given opacity.

        :param opacity: Opacity value, from 0 (transparent) to 1 (transparent)
        :type opacity: int
        :return: None
        """
        _utils.assert_color(self.background_color)
        assert isinstance(opacity, float)
        assert 0 <= opacity <= 1, 'opacity must be a number between 0 (transparent) and 1 (opaque)'
        self.background_color = (self.background_color[0], self.background_color[1],
                                 self.background_color[2], int(opacity * 255))  # type: tuple

    @staticmethod
    def _vec_to_tuple(obj, check_length=0):
        """
        Return a tuple from a list or tuple object.

        :param obj: Object
        :type obj: list, tuple
        :param check_length: Check length if not zero
        :type check_length: int
        :return: Tuple
        :rtype: tuple
        """
        if isinstance(obj, tuple):
            v = obj
        elif isinstance(obj, list):
            v = tuple(obj)
        else:
            raise ValueError('object is not a vector')
        if check_length > 0:
            if len(v) != check_length:
                raise ValueError('object is not a {0}-length vector'.format(check_length))
        return v

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

        Color may be an Image, so if this is the case return the same object.
        If the color is a list, return a tuple.

        :param color: Color object
        :type color: tuple, list, :py:class:`pygame_menu.baseimage.BaseImage`, None
        :return: Color in the same format
        :rtype: tuple, :py:class:`pygame_menu.baseimage.BaseImage`, None
        """
        if isinstance(color, BaseImage):
            return color
        if color is None:
            return color
        if isinstance(color, (tuple, list)):
            _utils.assert_color(color)
            if len(color) == 4:
                if isinstance(color, tuple):
                    return color
                else:
                    return color[0], color[1], color[2], color[3]
            elif len(color) == 3:
                color = color[0], color[1], color[2], 255
        else:
            raise ValueError('invalid color type {0}, only tuple or list are valid'.format(color))
        return color

    @staticmethod
    def _get(params, key, allowed_types=None, default=None):
        """
        Return a value from a dictionary.

        Custom types (str)
            -   alignment           pygame-menu alignment (locals)
            -   callable            Is callable type, same as ``"function"``
            -   color               Check color
            -   color_image         Color or :py:class:`pygame_menu.baseimage.BaseImage`
            -   color_image_none    Color, :py:class:`pygame_menu.baseimage.BaseImage`, or None
            -   color_none          Color or None
            -   cursor              Cursor object (pygame)
            -   font                Font type
            -   image               Value must be ``BaseImage``
            -   none                None only
            -   position            pygame-menu position (locals)}
            -   tuple2              Only valid numeric tuples ``(x, y)`` or ``[x, y]``
            -   type                Type-class (bool, str, etc...)

        :param params: Parameters dictionary
        :type params: dict
        :param key: Key to look for
        :type key: str
        :param allowed_types: List of allowed types
        :type allowed_types: any
        :param default: Default value to return
        :type default: any
        :return: The value associated to the key
        :rtype: any
        """
        value = params.pop(key, default)
        if allowed_types is not None:
            other_types = []  # Contain other types to check from
            if not isinstance(allowed_types, (tuple, list)):
                allowed_types = (allowed_types,)
            for val_type in allowed_types:

                if val_type == 'alignment':
                    _utils.assert_alignment(value)

                elif val_type == callable or val_type == 'function' or val_type == 'callable':
                    assert _utils.is_callable(value), \
                        'value must be callable type'

                elif val_type == 'color':
                    _utils.assert_color(value)

                elif val_type == 'color_image':
                    if not isinstance(value, BaseImage):
                        _utils.assert_color(value)

                elif val_type == 'color_image_none':
                    if not (value is None or isinstance(value, BaseImage)):
                        _utils.assert_color(value)

                elif val_type == 'color_none':
                    if value is not None:
                        _utils.assert_color(value)

                elif val_type == 'image':
                    assert isinstance(value, BaseImage), \
                        'value must be BaseImage type'

                elif val_type == 'none':
                    assert value is None

                elif val_type == 'position':
                    _utils.assert_position(value)

                elif val_type == 'type':
                    assert isinstance(value, type), \
                        'value is not type-class'

                elif val_type == 'tuple2':
                    _utils.assert_vector2(value)

                else:  # Unknown type
                    assert isinstance(val_type, type), \
                        'allowed type "{0}" is not a type-class'.format(val_type)
                    other_types.append(val_type)

            # Check other types
            if len(other_types) > 0:
                others = tuple(other_types)
                msg = 'Theme.{} type shall be in {} types (got {})'.format(key, others, type(value))
                assert isinstance(value, others), msg

        return value


THEME_DEFAULT = Theme()

THEME_DARK = Theme(
    background_color=(40, 41, 35),
    cursor_color=(255, 255, 255),
    cursor_selection_color=(80, 80, 80, 120),
    scrollbar_color=(39, 41, 42),
    scrollbar_slider_color=(65, 66, 67),
    selection_color=(255, 255, 255),
    title_background_color=(47, 48, 51),
    title_font_color=(215, 215, 215),
    widget_font_color=(200, 200, 200),
)

THEME_BLUE = Theme(
    background_color=(228, 230, 246),
    scrollbar_shadow=True,
    scrollbar_slider_color=(150, 200, 230),
    scrollbar_slider_pad=2,
    selection_color=(100, 62, 132),
    title_background_color=(62, 149, 195),
    title_font_color=(228, 230, 246),
    title_shadow=True,
    widget_font_color=(61, 170, 220),
)

THEME_GREEN = Theme(
    background_color=(186, 214, 177),
    scrollbar_slider_color=(125, 121, 114),
    scrollbar_slider_pad=2,
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
    cursor_color=(0, 0, 0),
    cursor_selection_color=(146, 160, 160, 120),
    selection_color=(207, 62, 132),
    title_background_color=(4, 47, 58),
    title_font_color=(38, 158, 151),
    widget_font_color=(102, 122, 130),
)
