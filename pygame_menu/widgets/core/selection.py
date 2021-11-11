"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SELECTION
Widget selection effect.
"""

__all__ = ['Selection']

import copy
import pygame
import pygame_menu

from pygame_menu.utils import assert_color

from pygame_menu._types import NumberType, ColorType, ColorInputType, Tuple2IntType, \
    Tuple4IntType, NumberInstance, Optional, Union


class Selection(object):
    """
    Widget selection effect class.

    .. note::

        All selection classes must be copyable.

    :param margin_left: Left margin
    :param margin_right: Right margin
    :param margin_top: Top margin
    :param margin_bottom: Bottom margin
    """
    color: ColorType
    color_bg: Optional[ColorType]
    margin_bottom: NumberType
    margin_left: NumberType
    margin_right: NumberType
    margin_top: NumberType
    widget_apply_font_color: bool

    def __init__(
            self,
            margin_left: NumberType,
            margin_right: NumberType,
            margin_top: NumberType,
            margin_bottom: NumberType
    ) -> None:
        assert isinstance(margin_left, NumberInstance)
        assert isinstance(margin_right, NumberInstance)
        assert isinstance(margin_top, NumberInstance)
        assert isinstance(margin_bottom, NumberInstance)
        assert margin_left >= 0, 'left margin of widget selection cannot be negative'
        assert margin_right >= 0, 'right margin of widget selection cannot be negative'
        assert margin_top >= 0, 'top margin of widget selection cannot be negative'
        assert margin_bottom >= 0, 'bottom margin of widget selection cannot be negative'

        self.color = (0, 0, 0)  # Main color of the selection effect
        self.color_bg = None
        self.margin_bottom = margin_bottom
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.margin_top = margin_top
        self.widget_apply_font_color = True  # Widgets apply "selected_color" if selected

    def margin_xy(self, x: NumberType, y: NumberType) -> 'Selection':
        """
        Set margins at left-right / top-bottom.

        :param x: Left-Right margin in px
        :param y: Top-Bottom margin in px
        :return: Self reference
        """
        assert isinstance(x, NumberInstance) and x >= 0
        assert isinstance(y, NumberInstance) and y >= 0
        self.margin_left = x
        self.margin_right = x
        self.margin_top = y
        self.margin_bottom = y
        return self

    def zero_margin(self) -> 'Selection':
        """
        Makes selection margin zero.

        :return: Self reference
        """
        self.margin_top = 0
        self.margin_left = 0
        self.margin_right = 0
        self.margin_bottom = 0
        return self

    def copy(self) -> 'Selection':
        """
        Creates a deep copy of the object.

        :return: Copied selection effect
        """
        return copy.deepcopy(self)

    def __copy__(self) -> 'Selection':
        """
        Copy method.

        :return: Copied selection
        """
        return self.copy()

    def set_color(self, color: ColorInputType) -> 'Selection':
        """
        Set the selection effect color.

        :param color: Selection color
        :return: Self reference
        """
        self.color = assert_color(color)
        return self

    def set_background_color(self, color: Union[ColorInputType, 'pygame_menu.BaseImage']) -> 'Selection':
        """
        Set the selection background color. It will replace the background color of the widget
        if selected.

        :param color: Background color
        :return: Self reference
        """
        self.color_bg = color
        if not isinstance(color, pygame_menu.BaseImage):
            self.color_bg = assert_color(self.color_bg)
        return self

    def get_background_color(self) -> Optional[Union[ColorType, 'pygame_menu.BaseImage']]:
        """
        Return the background color.

        :return: Background color or None
        """
        return self.color_bg

    def get_margin(self) -> Tuple4IntType:
        """
        Return the top, left, bottom and right margins of the selection.

        :return: Tuple of (top, left, bottom, right) margins in px
        """
        return int(self.margin_top), int(self.margin_left), \
               int(self.margin_bottom), int(self.margin_right)

    def get_xy_margin(self) -> Tuple2IntType:
        """
        Return the x/y margins of the selection.

        :return: Margin tuple on x-axis and y-axis (x, y) in px
        """
        return int(self.margin_left + self.margin_right), \
               int(self.margin_top + self.margin_bottom)

    def get_width(self) -> int:
        """
        Return the selection width as sum of left and right margins.

        :return: Width in px
        """
        _, l, _, r = self.get_margin()
        return l + r

    def get_height(self) -> int:
        """
        Return the selection height as sum of top and bottom margins.

        :return: Height in px
        """
        t, _, b, _ = self.get_margin()
        return t + b

    def inflate(
            self,
            rect: 'pygame.Rect', inflate: Optional[Tuple2IntType] = None
    ) -> 'pygame.Rect':
        """
        Grow or shrink the rectangle size according to margins.

        :param rect: Rect object
        :param inflate: Extra border inflate
        :return: Inflated rect
        """
        if inflate is None:
            inflate = (0, 0)
        assert isinstance(rect, pygame.Rect)
        return pygame.Rect(
            int(rect.x - self.margin_left - inflate[0] / 2),
            int(rect.y - self.margin_top - inflate[1] / 2),
            int(rect.width + self.margin_left + self.margin_right + inflate[0]),
            int(rect.height + self.margin_top + self.margin_bottom + inflate[1])
        )

    def draw(self, surface: 'pygame.Surface', widget: 'pygame_menu.widgets.Widget') -> 'Selection':
        """
        Draw the selection.

        :param surface: Surface to draw
        :param widget: Widget object
        :return: Self reference
        """
        raise NotImplementedError('override is mandatory')
