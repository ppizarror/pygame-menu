"""
pygame-menu
https://github.com/ppizarror/pygame-menu

THEMES
Theme class and predefined themes.
"""

__all__ = [

    # Main class
    'Theme',

    # Custom themes
    'THEME_BLUE',
    'THEME_DARK',
    'THEME_DEFAULT',
    'THEME_GREEN',
    'THEME_ORANGE',
    'THEME_SOLARIZED',

    # Colors
    'TRANSPARENT_COLOR'

]

import copy

from pygame_menu.baseimage import BaseImage
from pygame_menu.font import FontType, FONT_OPEN_SANS, assert_font
from pygame_menu.locals import POSITION_NORTHWEST, POSITION_SOUTHEAST, ALIGN_CENTER, \
    CURSOR_ARROW
from pygame_menu._scrollarea import get_scrollbars_from_position
from pygame_menu.utils import assert_alignment, assert_cursor, assert_vector, \
    assert_position, assert_color, format_color, assert_position_vector
from pygame_menu.widgets import HighlightSelection, NoneSelection, MENUBAR_STYLE_ADAPTIVE, \
    MENUBAR_STYLE_SIMPLE, MENUBAR_STYLE_TITLE_ONLY, MENUBAR_STYLE_TITLE_ONLY_DIAGONAL, \
    MENUBAR_STYLE_NONE, MENUBAR_STYLE_UNDERLINE, MENUBAR_STYLE_UNDERLINE_TITLE
from pygame_menu.widgets.core import Selection
from pygame_menu.widgets.core.widget import WidgetBorderPositionType, WIDGET_FULL_BORDER, \
    WIDGET_SHADOW_TYPE_ELLIPSE, WIDGET_SHADOW_TYPE_RECTANGULAR

from pygame_menu._types import ColorType, ColorInputType, Tuple, List, Union, Dict, \
    Any, Tuple2IntType, VectorInstance, Tuple2NumberType, NumberType, PaddingType, \
    Optional, Type, NumberInstance, PaddingInstance, Tuple3IntType, CursorType

TRANSPARENT_COLOR: ColorType = (0, 0, 0, 0)


def _check_menubar_style(style: int) -> bool:
    """
    Check menubar style.

    :param style: Style
    :return: ``True`` if correct
    """
    return style in (MENUBAR_STYLE_ADAPTIVE, MENUBAR_STYLE_SIMPLE, MENUBAR_STYLE_TITLE_ONLY,
                     MENUBAR_STYLE_TITLE_ONLY_DIAGONAL, MENUBAR_STYLE_NONE,
                     MENUBAR_STYLE_UNDERLINE, MENUBAR_STYLE_UNDERLINE_TITLE)


class Theme(object):
    """
    Class defining the visual rendering of menus and widgets.

    .. note::

        All colors must be defined with a tuple of 3 or 4 numbers in the formats:

            - (R, G, B)
            - (R, G, B, A)

        Red (R), Green (G), and Blue (B) must be numbers between ``0`` and ``255``.
        A means the alpha channel (opacity), if ``0`` the color is transparent, ``100`` means opaque.

    .. note::

        Themes only modify visual behaviour of the Menu. For other options
        like rows/columns, enabling or disabling overflow, position, or Menu
        width/height see Menu parameters.

    :param background_color: Menu background color
    :type background_color: tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`
    :param border_color: Menu border color. If border is an image, it will be split in 9 tiles to use top, left, bottom, right, and the corners
    :type border_color: tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`, None
    :param border_width: Border width in px. Used only if ``border_color`` is not an image
    :type border_width: int
    :param cursor_color: Cursor color (used in some text-gathering widgets like ``TextInput``)
    :type cursor_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param cursor_selection_color: Color of the text selection if the cursor is enabled on certain widgets
    :type cursor_selection_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param cursor_switch_ms: Interval of cursor switch between off and on status
    :type cursor_switch_ms: int, float
    :param focus_background_color: Color of the widget focus, this must be a tuple of 4 elements (R, G, B, A)
    :type focus_background_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param fps: Menu max fps (frames per second). If ``0`` there's no limit
    :type fps: int, float
    :param readonly_color: Color of the widget in readonly mode
    :type readonly_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param readonly_selected_color: Color of the selected widget in readonly mode
    :type readonly_selected_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param scrollarea_outer_margin: Outer ScrollArea margin in px; the tuple is added to computed ScrollArea width/height, it can add a margin to bottom/right scrolls after widgets. If value less than ``1`` use percentage of width/height. It cannot be a negative value
    :type scrollarea_outer_margin: tuple, list
    :param scrollarea_position: Position of ScrollArea scrollbars. See :py:mod:`pygame_menu.locals`
    :type scrollarea_position: str
    :param scrollbar_color: Scrollbars color
    :type scrollbar_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param scrollbar_cursor: Scrollbar cursor if mouse is placed over. If ``None`` the scrollbar don't change the cursor
    :type scrollbar_cursor: int, :py:class:`pygame.cursors.Cursor`, None
    :param scrollbar_shadow: Indicate if a shadow is drawn on each scrollbar
    :type scrollbar_shadow: bool
    :param scrollbar_shadow_color: Color of the scrollbar shadow
    :type scrollbar_shadow_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param scrollbar_shadow_offset: Offset of the scrollbar shadow
    :type scrollbar_shadow_offset: int
    :param scrollbar_shadow_position: Position of the scrollbar shadow. See :py:mod:`pygame_menu.locals`
    :type scrollbar_shadow_position: str
    :param scrollbar_slider_color: Color of the sliders
    :type scrollbar_slider_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param scrollbar_slider_hover_color: Color of the slider if hovered or clicked
    :type scrollbar_slider_hover_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param scrollbar_slider_pad: Space between slider and scrollbars borders
    :type scrollbar_slider_pad: int, float
    :param scrollbar_thick: Scrollbar thickness in px
    :type scrollbar_thick: int
    :param selection_color: Color of the selected widget. It updates both selected font and ``widget_selection_effect`` color
    :type selection_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param surface_clear_color: Surface clear color before applying background function
    :type surface_clear_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param title: Title is enabled/disabled. If disabled the object is ``hidden``
    :type title: bool
    :param title_background_color: Title background color
    :type title_background_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param title_bar_modify_scrollarea: If ``True`` title bar modifies the scrollbars of the scrollarea depending on the style
    :type title_bar_modify_scrollarea: bool
    :param title_bar_style: Style of the title, use :py:class:`pygame_menu.widgets.MenuBar` widget styles
    :type title_bar_style: int
    :param title_close_button: Draw a back-box button on header to close the Menu. If user moves through nested submenus this buttons turns to a back-arrow
    :type title_close_button: bool
    :param title_close_button_background_color: Title back-box background color
    :type title_close_button_background_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param title_close_button_cursor: Cursor applied over title close button
    :type title_close_button_cursor: int, :py:class:`pygame.cursors.Cursor`, None
    :param title_fixed: If ``True`` title is drawn over the scrollarea, forcing widget surface area to be drawn behind the title
    :type title_fixed: bool
    :param title_floating: If ``True`` title don't contribute height to the Menu. Thus, scroll uses full menu width/height
    :type title_floating: bool
    :param title_font: Title font
    :type title_font: str, :py:class:`pygame.font.Font`, :py:class:`pathlib.Path`
    :param title_font_antialias: Title font renders with antialiasing
    :type title_font_antialias: bool
    :param title_font_color: Title font color
    :type title_font_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param title_font_shadow: Enable title font shadow
    :type title_font_shadow: bool
    :param title_font_shadow_color: Title font shadow color
    :type title_font_shadow_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param title_font_shadow_offset: Offset of title font shadow in px
    :type title_font_shadow_offset: int
    :param title_font_shadow_position: Position of the title font shadow. See :py:mod:`pygame_menu.locals`
    :type title_font_shadow_position: str
    :param title_font_size: Font size of the title
    :type title_font_size: int
    :param title_offset: Offset (x-position, y-position) of title in px
    :type title_offset: tuple, list
    :param title_updates_pygame_display: If ``True`` the menu title updates See :py:mod:`pygame.display.caption` automatically on draw
    :type title_updates_pygame_display: bool
    :param widget_alignment: Widget default `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_. See :py:mod:`pygame_menu.locals`
    :type widget_alignment: str
    :param widget_background_color: Background color of a widget, it can be a color, ``None`` (transparent), or a BaseImage object. Background fills the entire widget + the padding
    :type widget_background_color: tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`, None
    :param widget_background_inflate: Inflate background on x-axis and y-axis (x, y) in px. By default, it uses the highlight margin. This parameter is visual only. For modifying widget size use padding instead
    :type widget_background_inflate: tuple, list
    :param widget_background_inflate_to_selection: If ``True`` widget will inflate to match selection effect margin and overrides ``widget_background_inflate``
    :type widget_background_inflate_to_selection: bool
    :param widget_border_color: Widget border color
    :type widget_border_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param widget_border_inflate: Widget inflate size on x-axis and y-axis (x, y) in px. These values cannot be negative
    :type widget_border_inflate: tuple, list
    :param widget_border_position: Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
    :type widget_border_position: str, tuple, list
    :param widget_border_width: Widget border width in px. If ``0`` the border is disabled. Border width don't contribute to the widget width/height, it's visual-only
    :type widget_border_width: int
    :param widget_box_arrow_color: Widget box arrow color, used by some widgets such as DropSelect, Fancy Selector, etc.
    :type widget_box_arrow_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param widget_box_arrow_margin: Widget box arrow margin (left, right, vertical) in px, used by some widgets such as DropSelect, Fancy Selector, etc.
    :type widget_box_arrow_margin: tuple
    :param widget_box_background_color: Widget box background color, used by some widgets such as DropSelect, Fancy Selector, etc.
    :type widget_box_background_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param widget_box_border_color: Widget box border color, used by some widgets such as DropSelect, Fancy Selector, etc.
    :type widget_box_border_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param widget_box_border_width: Widget box border width in px, used by some widgets such as DropSelect, Fancy Selector, etc.
    :type widget_box_border_width: int
    :param widget_box_inflate: Widget box inflate on x-axis and y-axis (x, y) in px, used by some widgets such as DropSelect, Fancy Selector, etc.
    :type widget_box_inflate: tuple, list
    :param widget_box_margin: Box margin on x-axis and y-axis (x, y) in px
    :type widget_box_margin: tuple, list
    :param widget_cursor: Widget cursor if mouse is placed over. If ``None`` the widget don't change the cursor
    :type widget_cursor: int, :py:class:`pygame.cursors.Cursor`, None
    :param widget_font: Widget font path or name
    :type widget_font: str, :py:class:`pygame.font.Font`, :py:class:`pathlib.Path`
    :param widget_font_antialias: Widget font renders with antialiasing
    :type widget_font_antialias: bool
    :param widget_font_background_color: Widget font background color. If ``None`` the value will be the same as ``background_color`` if it is a color object and if ``widget_font_background_color_from_menu`` is ``True`` and ``widget_background_color`` is ``None``
    :type widget_font_background_color: tuple, list, str, int, :py:class:`pygame.Color`, None
    :param widget_font_background_color_from_menu: Use Menu background color as font background color. Disabled by default
    :type widget_font_background_color_from_menu: bool
    :param widget_font_color: Color of the font
    :type widget_font_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param widget_font_shadow: Indicate if the widget font shadow is enabled
    :type widget_font_shadow: bool
    :param widget_font_shadow_color: Color of the widget font shadow
    :type widget_font_shadow_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param widget_font_shadow_offset: Offset of the widget font shadow in px
    :type widget_font_shadow_offset: int
    :param widget_font_shadow_position: Position of the widget font shadow. See :py:mod:`pygame_menu.locals`
    :type widget_font_shadow_position: str
    :param widget_font_size: Font size
    :type widget_font_size: int
    :param widget_margin: Horizontal and vertical margin of each element in Menu in px
    :type widget_margin: tuple, list
    :param widget_padding: Padding of the widget according to CSS rules. It can be a single digit, or a tuple of 2, 3, or 4 elements. Padding modifies widget width/height
    :type widget_padding: int, float, tuple, list
    :param widget_offset: x-axis and y-axis (x, y) offset of widgets within Menu in px respect to top-left corner. If value less than ``1`` use percentage of width/height. It cannot be a negative value
    :type widget_offset: tuple, list
    :param widget_selection_effect: Widget selection effect object. This is visual-only, the selection properties does not affect widget height/width
    :type widget_selection_effect: :py:class:`pygame_menu.widgets.core.Selection`, None
    :param widget_shadow_aa: Widget shadow antialiasing factor, default is x4
    :type widget_shadow_aa: int
    :param widget_shadow_color: The color of the widget shadow
    :type widget_shadow_color: tuple, list, str, int, :py:class:`pygame.Color`
    :param widget_shadow_radius: The border radius of the widget shadow
    :type widget_shadow_radius: int
    :param widget_shadow_type: The shadow type, it can be 'rectangular' or 'ellipse'
    :type widget_shadow_type: str
    :param widget_shadow_width: The width of the shadow in px
    :type widget_shadow_width: int
    :param widget_tab_size: Widget tab size
    :type widget_tab_size: int
    :param widget_url_color: Color of url text links
    :type widget_url_color: tuple, list, str, int, :py:class:`pygame.Color`
    """
    _disable_validation: bool
    background_color: Union[ColorType, 'BaseImage']
    border_color: Union[ColorType, 'BaseImage']
    cursor_color: ColorType
    cursor_selection_color: ColorType
    cursor_switch_ms: NumberType
    focus_background_color: ColorType
    fps: NumberType
    readonly_color: ColorType
    readonly_selected_color: ColorType
    scrollarea_outer_margin: Tuple2NumberType
    scrollarea_position: str
    scrollbar_color: ColorType
    scrollbar_cursor: CursorType
    scrollbar_shadow: bool
    scrollbar_shadow_color: ColorType
    scrollbar_shadow_offset: int
    scrollbar_shadow_position: str
    scrollbar_slider_color: ColorType
    scrollbar_slider_hover_color: ColorType
    scrollbar_slider_pad: NumberType
    scrollbar_thick: int
    selection_color: ColorType
    surface_clear_color: ColorType
    title: bool
    title_background_color: ColorType
    title_bar_modify_scrollarea: bool
    title_bar_style: int
    title_close_button: bool
    title_close_button_background_color: ColorType
    title_close_button_cursor: CursorType
    title_fixed: bool
    title_floating: bool
    title_font: FontType
    title_font_antialias: bool
    title_font_color: ColorType
    title_font_shadow: bool
    title_font_shadow_color: ColorType
    title_font_shadow_offset: int
    title_font_shadow_position: str
    title_font_size: int
    title_offset: Tuple2NumberType
    title_updates_pygame_display: bool
    widget_alignment: str
    widget_background_color: Optional[Union[ColorType, 'BaseImage']]
    widget_background_inflate: Tuple2IntType
    widget_background_inflate_to_selection: bool
    widget_border_color: ColorType
    widget_border_inflate: Tuple2IntType
    widget_border_position: WidgetBorderPositionType
    widget_border_width: int
    widget_box_arrow_color: ColorType
    widget_box_arrow_margin: Tuple3IntType
    widget_box_background_color: ColorType
    widget_box_border_color: ColorType
    widget_box_border_width: int
    widget_box_inflate: Tuple2IntType
    widget_box_margin: Tuple2NumberType
    widget_cursor: CursorType
    widget_font: FontType
    widget_font_antialias: str
    widget_font_background_color: Optional[ColorType]
    widget_font_background_color_from_menu: bool
    widget_font_color: ColorType
    widget_font_shadow: bool
    widget_font_shadow_color: ColorType
    widget_font_shadow_offset: NumberType
    widget_font_shadow_position: str
    widget_font_size: int
    widget_margin: Tuple2NumberType
    widget_offset: Tuple2NumberType
    widget_padding: PaddingType
    widget_selection_effect: 'pygame_menu.widgets.core.Selection'
    widget_shadow_aa: int
    widget_shadow_color: ColorType
    widget_shadow_radius: int
    widget_shadow_type: str
    widget_shadow_width: int
    widget_tab_size: int
    widget_url_color: ColorType

    def __init__(self, **kwargs) -> None:

        # Menu general
        self.background_color = self._get(kwargs, 'background_color', 'color_image', (220, 220, 220))
        self.border_color = self._get(kwargs, 'border_color', 'color_image_none')
        self.border_width = self._get(kwargs, 'border_width', int, 0)
        self.focus_background_color = self._get(kwargs, 'focus_background_color', 'color', (0, 0, 0, 180))
        self.fps = self._get(kwargs, 'fps', NumberInstance, 30)
        self.readonly_color = self._get(kwargs, 'readonly_color', 'color', (120, 120, 120))
        self.readonly_selected_color = self._get(kwargs, 'readonly_selected_color', 'color', (190, 190, 190))
        self.selection_color = self._get(kwargs, 'selection_color', 'color', (255, 255, 255))
        self.surface_clear_color = self._get(kwargs, 'surface_clear_color', 'color', (0, 0, 0))

        # Cursor/Text gathering
        self.cursor_color = self._get(kwargs, 'cursor_color', 'color', (0, 0, 0))
        self.cursor_selection_color = self._get(kwargs, 'cursor_selection_color', 'color', (30, 30, 30, 120))
        self.cursor_switch_ms = self._get(kwargs, 'cursor_switch_ms', NumberInstance, 750)

        # Menubar/Title
        self.title = self._get(kwargs, 'title', bool, True)
        self.title_background_color = self._get(kwargs, 'title_background_color', 'color', (70, 70, 70))
        self.title_bar_modify_scrollarea = self._get(kwargs, 'title_bar_modify_scrollarea', bool, True)
        self.title_bar_style = self._get(kwargs, 'title_bar_style', int, MENUBAR_STYLE_ADAPTIVE)
        self.title_close_button = self._get(kwargs, 'title_close_button', bool, True)
        self.title_close_button_background_color = self._get(kwargs, 'title_close_button_background_color', 'color', (255, 255, 255))
        self.title_close_button_cursor = self._get(kwargs, 'title_close_button_cursor', 'cursor')
        self.title_fixed = self._get(kwargs, 'title_fixed', bool, True)
        self.title_floating = self._get(kwargs, 'title_floating', bool, False)
        self.title_font = self._get(kwargs, 'title_font', 'font', FONT_OPEN_SANS)
        self.title_font_antialias = self._get(kwargs, 'title_font_antialias', bool, True)
        self.title_font_color = self._get(kwargs, 'title_font_color', 'color', (220, 220, 220))
        self.title_font_shadow = self._get(kwargs, 'title_font_shadow', bool, False)
        self.title_font_shadow_color = self._get(kwargs, 'title_font_shadow_color', 'color', (0, 0, 0))
        self.title_font_shadow_offset = self._get(kwargs, 'title_font_shadow_offset', int, 2)
        self.title_font_shadow_position = self._get(kwargs, 'title_font_shadow_position', 'position', POSITION_NORTHWEST)
        self.title_font_size = self._get(kwargs, 'title_font_size', int, 40)
        self.title_offset = self._get(kwargs, 'title_offset', 'tuple2', (5, -1))
        self.title_updates_pygame_display = self._get(kwargs, 'title_updates_pygame_display', bool, False)

        # ScrollArea
        self.scrollarea_outer_margin = self._get(kwargs, 'scrollarea_outer_margin', 'tuple2', (0, 0))
        self.scrollarea_position = self._get(kwargs, 'scrollarea_position', str, POSITION_SOUTHEAST)

        # ScrollBar
        self.scrollbar_color = self._get(kwargs, 'scrollbar_color', 'color', (235, 235, 235))
        self.scrollbar_cursor = self._get(kwargs, 'scrollbar_cursor', 'cursor')
        self.scrollbar_shadow = self._get(kwargs, 'scrollbar_shadow', bool, False)
        self.scrollbar_shadow_color = self._get(kwargs, 'scrollbar_shadow_color', 'color', (0, 0, 0))
        self.scrollbar_shadow_offset = self._get(kwargs, 'scrollbar_shadow_offset', int, 2)
        self.scrollbar_shadow_position = self._get(kwargs, 'scrollbar_shadow_position', 'position', POSITION_NORTHWEST)
        self.scrollbar_slider_color = self._get(kwargs, 'scrollbar_slider_color', 'color', (200, 200, 200))
        self.scrollbar_slider_hover_color = self._get(kwargs, 'scrollbar_slider_hover_color', 'color', (170, 170, 170))
        self.scrollbar_slider_pad = self._get(kwargs, 'scrollbar_slider_pad', NumberInstance, 0)
        self.scrollbar_thick = self._get(kwargs, 'scrollbar_thick', int, 20)

        # Generic widget themes
        self.widget_alignment = self._get(kwargs, 'widget_alignment', 'alignment', ALIGN_CENTER)
        self.widget_background_color = self._get(kwargs, 'widget_background_color', 'color_image_none')
        self.widget_background_inflate = self._get(kwargs, 'background_inflate', 'tuple2int', (0, 0))
        self.widget_background_inflate_to_selection = self._get(kwargs, 'widget_background_inflate_to_selection', bool,
                                                                False)
        self.widget_border_color = self._get(kwargs, 'widget_border_color', 'color', (0, 0, 0))
        self.widget_border_inflate = self._get(kwargs, 'widget_border_inflate', 'tuple2int', (0, 0))
        self.widget_border_position = self._get(kwargs, 'widget_border_position', 'position_vector', WIDGET_FULL_BORDER)
        self.widget_border_width = self._get(kwargs, 'widget_border_width', int, 0)
        self.widget_box_arrow_color = self._get(kwargs, 'widget_box_arrow_color', 'color', (150, 150, 150))
        self.widget_box_arrow_margin = self._get(kwargs, 'widget_box_arrow_margin', 'tuple3int', (5, 5, 0))
        self.widget_box_background_color = self._get(kwargs, 'widget_box_background_color', 'color', (255, 255, 255))
        self.widget_box_border_color = self._get(kwargs, 'widget_box_border_color', 'color', (0, 0, 0))
        self.widget_box_border_width = self._get(kwargs, 'widget_box_border_width', int, 1)
        self.widget_box_inflate = self._get(kwargs, 'widget_box_inflate', 'tuple2int', (0, 0))
        self.widget_box_margin = self._get(kwargs, 'widget_box_margin', 'tuple2', (25, 0))
        self.widget_cursor = self._get(kwargs, 'widget_cursor', 'cursor', CURSOR_ARROW)
        self.widget_font = self._get(kwargs, 'widget_font', 'font', FONT_OPEN_SANS)
        self.widget_font_antialias = self._get(kwargs, 'widget_font_antialias', bool, True)
        self.widget_font_background_color = self._get(kwargs, 'widget_font_background_color', 'color_none', )
        self.widget_font_background_color_from_menu = self._get(kwargs, 'widget_font_background_color_from_menu', bool, False)
        self.widget_font_color = self._get(kwargs, 'widget_font_color', 'color', (70, 70, 70))
        self.widget_font_shadow = self._get(kwargs, 'widget_font_shadow', bool, False)
        self.widget_font_shadow_color = self._get(kwargs, 'widget_font_shadow_color', 'color', (0, 0, 0))
        self.widget_font_shadow_offset = self._get(kwargs, 'widget_font_shadow_offset', int, 2)
        self.widget_font_shadow_position = self._get(kwargs, 'widget_font_shadow_position', 'position', POSITION_NORTHWEST)
        self.widget_font_size = self._get(kwargs, 'widget_font_size', int, 30)
        self.widget_margin = self._get(kwargs, 'widget_margin', 'tuple2', (0, 0))
        self.widget_offset = self._get(kwargs, 'widget_offset', 'tuple2', (0, 0))
        self.widget_padding = self._get(kwargs, 'widget_padding', PaddingInstance, (4, 8))
        self.widget_selection_effect = self._get(kwargs, 'widget_selection_effect', Selection, HighlightSelection(margin_x=0, margin_y=0))
        self.widget_shadow_aa = self._get(kwargs, 'widget_shadow_aa', int, 4)
        self.widget_shadow_color = self._get(kwargs, 'widget_shadow_color', 'color', (0, 0, 0))
        self.widget_shadow_radius = self._get(kwargs, 'widget_shadow_radius', int, 0)
        self.widget_shadow_type = self._get(kwargs, 'widget_shadow_type', str, WIDGET_SHADOW_TYPE_RECTANGULAR)
        self.widget_shadow_width = self._get(kwargs, 'widget_shadow_width', int, 0)
        self.widget_tab_size = self._get(kwargs, 'widget_tab_size', int, 4)
        self.widget_url_color = self._get(kwargs, 'widget_url_color', 'color', (6, 69, 173))

        # Upon this, no more kwargs should exist, raise exception if there's more
        for invalid_keyword in kwargs.keys():
            raise ValueError(f'parameter Theme.{invalid_keyword} does not exist')

        # Test purpose only, if True disables any validation
        self._disable_validation = False

    def validate(self) -> 'Theme':
        """
        Validate the values of the theme. If there's an invalid parameter throws an
        ``AssertionError``.

        This function also converts all lists to tuples. This is done because lists
        are mutable.

        :return: Self reference
        """
        if self._disable_validation:
            return self

        # Boolean asserts
        assert isinstance(self.scrollbar_shadow, bool)
        assert isinstance(self.title_bar_modify_scrollarea, bool)
        assert isinstance(self.title_close_button, bool)
        assert isinstance(self.title_font_antialias, bool)
        assert isinstance(self.title_font_shadow, bool)
        assert isinstance(self.widget_font_antialias, bool)
        assert isinstance(self.widget_font_background_color_from_menu, bool)
        assert isinstance(self.widget_font_shadow, bool)

        # Value type checks
        assert_alignment(self.widget_alignment)
        assert_cursor(self.scrollbar_cursor)
        assert_cursor(self.title_close_button_cursor)
        assert_cursor(self.widget_cursor)
        assert_font(self.title_font)
        assert_font(self.widget_font)
        assert_position(self.scrollbar_shadow_position)
        assert_position(self.title_font_shadow_position)
        assert_position(self.widget_font_shadow_position)
        assert_position_vector(self.widget_border_position)

        assert _check_menubar_style(self.title_bar_style)
        assert get_scrollbars_from_position(self.scrollarea_position) is not None

        # Check selection effect if None
        if self.widget_selection_effect is None:
            self.widget_selection_effect = NoneSelection()

        assert isinstance(self.border_width, int)
        assert isinstance(self.cursor_switch_ms, NumberInstance)
        assert isinstance(self.fps, NumberInstance)
        assert isinstance(self.scrollbar_shadow_offset, int)
        assert isinstance(self.scrollbar_slider_pad, NumberInstance)
        assert isinstance(self.scrollbar_thick, int)
        assert isinstance(self.title, bool)
        assert isinstance(self.title_fixed, bool)
        assert isinstance(self.title_floating, bool)
        assert isinstance(self.title_font_shadow_offset, int)
        assert isinstance(self.title_font_size, int)
        assert isinstance(self.title_updates_pygame_display, bool)
        assert isinstance(self.widget_background_inflate_to_selection, bool)
        assert isinstance(self.widget_border_width, int)
        assert isinstance(self.widget_box_border_width, int)
        assert isinstance(self.widget_font_shadow_offset, int)
        assert isinstance(self.widget_font_size, int)
        assert isinstance(self.widget_padding, PaddingInstance)
        assert isinstance(self.widget_selection_effect, Selection)
        assert isinstance(self.widget_shadow_aa, int)
        assert isinstance(self.widget_shadow_radius, int)
        assert isinstance(self.widget_shadow_width, int)
        assert isinstance(self.widget_tab_size, int)

        # Format colors, this converts all color lists to tuples automatically,
        # if it is an image, return the same object
        self.background_color = self._format_color_opacity(self.background_color)
        self.border_color = self._format_color_opacity(self.border_color, none=True)
        self.cursor_color = self._format_color_opacity(self.cursor_color)
        self.cursor_selection_color = self._format_color_opacity(self.cursor_selection_color)
        self.focus_background_color = self._format_color_opacity(self.focus_background_color)
        self.readonly_color = self._format_color_opacity(self.readonly_color)
        self.readonly_selected_color = self._format_color_opacity(self.readonly_selected_color)
        self.scrollbar_color = self._format_color_opacity(self.scrollbar_color)
        self.scrollbar_shadow_color = self._format_color_opacity(self.scrollbar_shadow_color)
        self.scrollbar_slider_color = self._format_color_opacity(self.scrollbar_slider_color)
        self.scrollbar_slider_hover_color = self._format_color_opacity(self.scrollbar_slider_hover_color)
        self.selection_color = self._format_color_opacity(self.selection_color)
        self.surface_clear_color = self._format_color_opacity(self.surface_clear_color)
        self.title_background_color = self._format_color_opacity(self.title_background_color)
        self.title_close_button_background_color = self._format_color_opacity(self.title_close_button_background_color)
        self.title_font_color = self._format_color_opacity(self.title_font_color)
        self.title_font_shadow_color = self._format_color_opacity(self.title_font_shadow_color)
        self.widget_background_color = self._format_color_opacity(self.widget_background_color, none=True)
        self.widget_border_color = self._format_color_opacity(self.widget_border_color)
        self.widget_box_arrow_color = self._format_color_opacity(self.widget_box_arrow_color)
        self.widget_box_background_color = self._format_color_opacity(self.widget_box_background_color)
        self.widget_box_border_color = self._format_color_opacity(self.widget_box_border_color)
        self.widget_font_background_color = self._format_color_opacity(self.widget_font_background_color, none=True)
        self.widget_font_color = self._format_color_opacity(self.widget_font_color)
        self.widget_font_shadow_color = self._format_color_opacity(self.widget_font_shadow_color)
        self.widget_shadow_color = self._format_color_opacity(self.widget_shadow_color)
        self.widget_url_color = self._format_color_opacity(self.widget_url_color)

        # List to tuple
        self.scrollarea_outer_margin = self._vec_to_tuple(self.scrollarea_outer_margin, 2, NumberInstance)
        self.title_offset = self._vec_to_tuple(self.title_offset, 2, NumberInstance)
        self.widget_background_inflate = self._vec_to_tuple(self.widget_background_inflate, 2, int)
        self.widget_border_inflate = self._vec_to_tuple(self.widget_border_inflate, 2, int)
        self.widget_box_arrow_margin = self._vec_to_tuple(self.widget_box_arrow_margin, 3, int)
        self.widget_box_inflate = self._vec_to_tuple(self.widget_box_inflate, 2, int)
        self.widget_box_margin = self._vec_to_tuple(self.widget_box_margin, 2, NumberInstance)
        self.widget_margin = self._vec_to_tuple(self.widget_margin, 2, NumberInstance)
        if isinstance(self.widget_padding, VectorInstance):
            self.widget_padding = self._vec_to_tuple(self.widget_padding)
            assert 2 <= len(self.widget_padding) <= 4, \
                'widget padding tuple length must be 2, 3 or 4'
            for p in self.widget_padding:
                assert isinstance(p, NumberInstance), \
                    'each padding element must be numeric (integer or float)'
                assert p >= 0, \
                    'all padding elements must be equal or greater than zero'
        else:
            assert self.widget_padding >= 0, 'padding cannot be a negative number'
        self.widget_offset = self._vec_to_tuple(self.widget_offset, 2, NumberInstance)

        # Check sizes
        assert self.border_width >= 0, 'border width must be equal or greater than zero'
        assert self.scrollarea_outer_margin[0] >= 0 and self.scrollarea_outer_margin[1] >= 0, \
            'scroll area outer margin must be equal or greater than zero on both axis'
        assert self.widget_offset[0] >= 0 and self.widget_offset[1] >= 0, \
            'widget offset must be equal or greater than zero'
        assert self.widget_background_inflate[0] >= 0 and self.widget_background_inflate[1] >= 0, \
            'widget background inflate must be equal or greater than zero on both axis'
        assert self.widget_border_inflate[0] >= 0 and self.widget_border_inflate[1] >= 0, \
            'widget border inflate must be equal or greater than zero on both axis'
        assert self.widget_box_inflate[0] >= 0 and self.widget_box_inflate[1] >= 0, \
            'widget box inflate inflate must be equal or greater than zero on both axis'
        assert self.widget_shadow_width >= 0 and self.widget_shadow_radius >= 0, \
            'widget shadow width and radius must be equal or greater than zero'

        # Check shadow type
        assert self.widget_shadow_type in (WIDGET_SHADOW_TYPE_ELLIPSE, WIDGET_SHADOW_TYPE_RECTANGULAR), \
            'widget shadow type must be ellipse or rectangular'

        assert self.cursor_switch_ms > 0, 'cursor switch ms must be greater than zero'
        assert self.fps >= 0, 'fps must be equal or greater than zero'
        assert self.scrollbar_shadow_offset > 0, 'scrollbar shadow offset must be greater than zero'
        assert self.scrollbar_slider_pad >= 0, 'slider pad must be equal or greater than zero'
        assert self.scrollbar_thick > 0, 'scrollbar thickness must be greater than zero'
        assert self.title_font_size > 0, 'title font size must be greater than zero'
        assert self.widget_border_width >= 0, 'widget border width must be equal or greater than zero'
        assert self.widget_box_border_width >= 0, 'widget border box width must be equal or greater than zero'
        assert self.widget_font_shadow_offset > 0, 'widget font shadow offset must be greater than zero'
        assert self.widget_font_size > 0, 'widget font size must be greater than zero'
        assert self.widget_shadow_aa >= 1, 'widget shadow antialiasing must be equal or greater than one'
        assert self.widget_tab_size >= 0, 'widget tab size must be equal or greater than zero'

        # Color asserts
        assert self.focus_background_color[3] != 0, \
            'focus background color cannot be fully transparent, suggested opacity between 1 and 255'

        return self

    def set_background_color_opacity(self, opacity: float) -> 'Theme':
        """
        Modify the Menu background color with given opacity.

        :param opacity: Opacity value, from ``0`` (transparent) to ``1`` (opaque)
        :return: Self reference
        """
        self.background_color = assert_color(self.background_color)
        assert isinstance(opacity, NumberInstance)
        assert 0 <= opacity <= 1, 'opacity must be a number between 0 (transparent) and 1 (opaque)'
        self.background_color = (self.background_color[0], self.background_color[1], self.background_color[2], int(float(opacity) * 255))
        return self

    @staticmethod
    def _vec_to_tuple(obj: Union[Tuple, List], check_length: int = 0, check_instance: Type = Any) -> Tuple:
        """
        Return a tuple from a list or tuple object.

        :param obj: Object
        :param check_length: Check length if not zero
        :return: Tuple
        """
        if isinstance(obj, tuple):
            v = obj
        elif isinstance(obj, list):
            v = tuple(obj)
        else:
            if check_length == 0:
                raise ValueError('object is not a vector')
            raise ValueError(f'object is not a vector of length {check_length}')
        if check_length > 0:
            if len(v) != check_length:
                raise ValueError(f'object is not a vector of length {check_length}')
        if check_instance is not Any:
            for i in v:
                assert isinstance(i, check_instance), \
                    f'{i} element of tuple {v} is not {check_instance} instance'
        return v

    def copy(self) -> 'Theme':
        """
        Creates a deep copy of the object.

        :return: Copied theme
        """
        self.validate()
        return copy.deepcopy(self)

    def __copy__(self) -> 'Theme':
        """
        Copy method.

        :return: Copied theme
        """
        return self.copy()

    @staticmethod
    def _format_color_opacity(
            color: Optional[Union[ColorInputType, 'BaseImage']],
            none: bool = False
    ) -> Optional[Union[ColorType, 'BaseImage']]:
        """
        Adds opacity to a 3 channel color. (R,G,B) -> (R,G,B,A) if the color
        has not an alpha channel. Also updates the opacity to a number between
        ``0`` (transparent) and ``255`` (opaque).

        Color may be an Image, so if this is the case return the same object.

        - If the color is a list, return a tuple.
        - If the color is ``None``, return ``None`` if ``None`` is True.

        :param color: Color object
        :param none: If ``True`` Color can be ``None``
        :return: Color in the same format
        """
        if isinstance(color, BaseImage):
            return color
        if color is None and none:
            return color
        color = format_color(color)
        if isinstance(color, VectorInstance):
            assert_color(color)
            if len(color) == 4:
                if isinstance(color, tuple):
                    return color
                return tuple(color)
            elif len(color) == 3:
                color = color[0], color[1], color[2], 255
        else:
            raise ValueError(f'invalid color type {color}, only tuple or list are valid')
        return color

    # noinspection PyTypeChecker
    @staticmethod
    def _get(params: Dict[str, Any], key: str,
             allowed_types: Optional[Union[Type, str, List[Type], Tuple[Type, ...]]] = None,
             default: Any = None) -> Any:
        """
        Return a value from a dictionary.

        Custom types (str)
            -   alignment           – pygame-menu alignment (locals)
            -   callable            – Is callable type, same as ``"function"``
            -   color               – Check color
            -   color_image         – Color or :py:class:`pygame_menu.baseimage.BaseImage`
            -   color_image_none    – Color, :py:class:`pygame_menu.baseimage.BaseImage`, or None
            -   color_none          – Color or None
            -   cursor              – Cursor object (pygame)
            -   font                – Font type
            -   image               – Value must be ``BaseImage``
            -   none                – None only
            -   position            – pygame-menu position (locals)
            -   position_vector     – pygame-menu position (str or vector)
            -   tuple2              – Only valid numeric tuples ``(x, y)`` or ``[x, y]``
            -   tuple2int           – Only valid integer tuples ``(x, y)`` or ``[x, y]``
            -   tuple3              – Only valid numeric tuples ``(x, y, z)`` or ``[x, y, z]``
            -   tuple3int           – Only valid integer tuples ``(x, y, z)`` or ``[x, y, z]``
            -   type                – Type-class (bool, str, etc...)

        :param params: Parameters dictionary
        :param key: Key to look for
        :param allowed_types: List of allowed types
        :param default: Default value to return
        :return: The value associated to the key
        """
        value = params.pop(key, default)
        if allowed_types is not None:
            other_types = []  # Contain other types to check from
            if not isinstance(allowed_types, VectorInstance):
                allowed_types = (allowed_types,)
            for val_type in allowed_types:

                if val_type == 'alignment':
                    assert_alignment(value)

                elif val_type == callable or val_type == 'function' or val_type == 'callable':
                    assert callable(value), \
                        'value must be callable type'

                elif val_type == 'color':
                    value = assert_color(value)

                elif val_type == 'color_image':
                    if not isinstance(value, BaseImage):
                        value = assert_color(value)

                elif val_type == 'color_image_none':
                    if not (value is None or isinstance(value, BaseImage)):
                        value = assert_color(value)

                elif val_type == 'color_none':
                    if value is not None:
                        value = assert_color(value)

                elif val_type == 'cursor':
                    assert_cursor(value)

                elif val_type == 'font':
                    assert_font(value)

                elif val_type == 'image':
                    assert isinstance(value, BaseImage), \
                        'value must be BaseImage type'

                elif val_type == 'none':
                    assert value is None

                elif val_type == 'position':
                    assert_position(value)

                elif val_type == 'position_vector':
                    assert_position_vector(value)

                elif val_type == 'type':
                    assert isinstance(value, type), \
                        'value is not type-class'

                elif val_type == 'tuple2':
                    assert_vector(value, 2)

                elif val_type == 'tuple2int':
                    assert_vector(value, 2, int)

                elif val_type == 'tuple3':
                    assert_vector(value, 3)

                elif val_type == 'tuple3int':
                    assert_vector(value, 3, int)

                else:  # Unknown type
                    assert isinstance(val_type, type), \
                        f'allowed type "{val_type}" is not a type-class'
                    other_types.append(val_type)

            # Check other types
            if len(other_types) > 0:
                others = tuple(other_types)
                assert isinstance(value, others), \
                    f'Theme.{key} type shall be in {others} types (got {type(value)})'

        return value


THEME_DEFAULT = Theme()

THEME_DARK = Theme(
    background_color=(40, 41, 35),
    cursor_color=(255, 255, 255),
    cursor_selection_color=(80, 80, 80, 120),
    scrollbar_color=(39, 41, 42),
    scrollbar_slider_color=(65, 66, 67),
    scrollbar_slider_hover_color=(90, 89, 88),
    selection_color=(255, 255, 255),
    title_background_color=(47, 48, 51),
    title_font_color=(215, 215, 215),
    widget_font_color=(200, 200, 200)
)

THEME_BLUE = Theme(
    background_color=(228, 230, 246),
    scrollbar_shadow=True,
    scrollbar_slider_color=(150, 200, 230),
    scrollbar_slider_hover_color=(123, 173, 202),
    scrollbar_slider_pad=2,
    selection_color=(100, 62, 132),
    title_background_color=(62, 149, 195),
    title_font_color=(228, 230, 246),
    title_font_shadow=True,
    widget_font_color=(61, 170, 220)
)

THEME_GREEN = Theme(
    background_color=(186, 214, 177),
    scrollbar_slider_color=(125, 121, 114),
    scrollbar_slider_hover_color=(100, 96, 90),
    scrollbar_slider_pad=2,
    selection_color=(125, 121, 114),
    title_background_color=(125, 121, 114),
    title_font_color=(228, 230, 246),
    widget_font_color=(255, 255, 255)
)

THEME_ORANGE = Theme(
    background_color=(228, 100, 36),
    selection_color=(255, 255, 255),
    title_background_color=(170, 65, 50),
    widget_font_color=(0, 0, 0),
    widget_font_size=30
)

THEME_SOLARIZED = Theme(
    background_color=(239, 231, 211),
    cursor_color=(0, 0, 0),
    cursor_selection_color=(146, 160, 160, 120),
    selection_color=(207, 62, 132),
    title_background_color=(4, 47, 58),
    title_font_color=(38, 158, 151),
    widget_font_color=(102, 122, 130)
)
