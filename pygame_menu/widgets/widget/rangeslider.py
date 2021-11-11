"""
pygame-menu
https://github.com/ppizarror/pygame-menu

RANGE SLIDER
Slider bar between one/two numeric ranges.
"""

__all__ = [

    # Class
    'RangeSlider',
    'RangeSliderManager',

    # Input types
    'RangeSliderRangeValueType',
    'RangeSliderValueFormatType',
    'RangeSliderValueType'

]

import math
import pygame
import pygame_menu
import pygame_menu.controls as ctrl

from abc import ABC
from pygame_menu.locals import POSITION_NORTH, POSITION_SOUTH
from pygame_menu.font import FontType, assert_font
from pygame_menu.locals import FINGERUP, FINGERDOWN, FINGERMOTION
from pygame_menu.utils import check_key_pressed_valid, assert_color, assert_vector, \
    make_surface, get_finger_pos, assert_position, parse_padding, is_callable
from pygame_menu.widgets.core.widget import Widget, WidgetTransformationNotImplemented, \
    AbstractWidgetManager

from pygame_menu._types import Any, CallbackType, Union, List, Tuple, Optional, \
    ColorType, NumberType, Tuple2IntType, NumberInstance, ColorInputType, \
    EventVectorType, Vector2NumberType, VectorType, PaddingType, Tuple4IntType, \
    Callable, Dict

RangeSliderRangeValueType = Union[Vector2NumberType, VectorType]
RangeSliderValueFormatType = Callable[[NumberType], str]
RangeSliderValueType = Union[NumberType, Vector2NumberType]


# noinspection PyMissingOrEmptyDocstring
class RangeSlider(Widget):
    """
    Range slider widget. Offers 1 or 2 sliders for defining a unique value or
    a range of numeric ones.

    If the state of the widget changes the ``onchange`` callback is called. The
    state can change by pressing LEFT/RIGHT, or by mouse/touch events.

    .. code-block:: python

        onchange(range_value, **kwargs)

    If pressing return key on the widget:

    .. code-block:: python

        onreturn(range_value, **kwargs)

    .. note::

        RangeSlider only accepts translation transformation.

    :param title: Range slider title
    :param rangeslider_id: RangeSlider ID
    :param default_value: Default range value, can accept a number or a tuple/list of 2 elements (min, max). If a single number is provided the rangeslider only accepts 1 value, if 2 are provided, the range is enabled (2 values)
    :param range_values: Tuple/list of 2 elements of min/max values of the range slider. Also range can accept a list of numbers, in which case the values of the range slider will be discrete. List must be sorted
    :param range_width: Width of the range in px
    :param increment: Increment of the value if using left/right keys; used only if the range values are not discrete
    :param onchange: Callback when changing the value of the range slider
    :param onreturn: Callback when pressing return on the range slider
    :param onselect: Function when selecting the widget
    :param range_box_color: Color of the range box between the sliders
    :param range_box_color_readonly: Color of the range box if widget in readonly state
    :param range_box_enabled: Enables a range box between two sliders
    :param range_box_height_factor: Height of the range box (factor of the range title height)
    :param range_box_single_slider: Enables range box if there's only 1 slider instead of 2
    :param range_line_color: Color of the range line
    :param range_line_height: Height of the range line in px
    :param range_margin: Range margin on x-axis and y-axis (x, y) from title in px
    :param range_text_value_color: Color of the range values text
    :param range_text_value_enabled: Enables the range values text
    :param range_text_value_font: Font of the ranges value. If ``None`` the same font as the widget is used
    :param range_text_value_font_height: Height factor of the range value font (factor of the range title height)
    :param range_text_value_margin_f: Margin of the range text values (factor of the range title height)
    :param range_text_value_position: Position of the range text values, can be NORTH or SOUTH. See :py:mod:`pygame_menu.locals`
    :param range_text_value_tick_color: Color of the range text value tick
    :param range_text_value_tick_enabled: Range text value tick enabled
    :param range_text_value_tick_hfactor: Height factor of the range text value tick (factor of the range title height)
    :param range_text_value_tick_number: Number of range value text, the values are placed uniformly distributed
    :param range_text_value_tick_thick: Thickness of the range text value tick in px
    :param repeat_keys_initial_ms: Time in ms before keys are repeated when held in ms
    :param repeat_keys_interval_ms: Interval between key press repetition when held in ms
    :param slider_color: Slider color
    :param slider_height_factor: Height of the slider (factor of the range title height)
    :param slider_sel_highlight_color: Color of the selected slider highlight box effect
    :param slider_sel_highlight_enabled: Selected slider is highlighted
    :param slider_sel_highlight_thick: Thickness of the selected slider highlight
    :param slider_selected_color: Selected slider color
    :param slider_text_value_bgcolor: Background color of the value text on each slider
    :param slider_text_value_color: Color of value text on each slider
    :param slider_text_value_enabled: Enables a value text on each slider
    :param slider_text_value_font: Font of the slider value. If ``None`` the same font as the widget is used
    :param slider_text_value_font_height: Height factor of the slider font (factor of the range title height)
    :param slider_text_value_margin_f: Margin of the slider text values (factor of the range title height)
    :param slider_text_value_padding: Padding of the slider text values
    :param slider_text_value_position: Position of the slider text values, can be NORTH or SOUTH. See :py:mod:`pygame_menu.locals`
    :param slider_text_value_triangle: Draws a triangle between slider text value and slider
    :param slider_thickness: Slider thickness in px
    :param slider_vmargin: Vertical margin of the slider (factor of the range title height)
    :param value_format: Function that format the value and returns a string that is used in the range and slider text
    :param args: Optional arguments for callbacks
    :param kwargs: Optional keyword arguments
    """
    _font_range_value: Optional['pygame.font.Font']
    _font_slider_value: Optional['pygame.font.Font']
    _increment: NumberType
    _increment_shift_factor: float
    _keyrepeat_counters: Dict[int, int]
    _keyrepeat_initial_interval_ms: NumberType
    _keyrepeat_interval_ms: NumberType
    _range_box: 'pygame.Surface'
    _range_box_color: ColorType
    _range_box_color_readonly: ColorType
    _range_box_enabled: bool
    _range_box_height: int
    _range_box_height_factor: NumberType
    _range_box_pos: Tuple2IntType
    _range_box_single_slider: bool
    _range_line: 'pygame.Surface'
    _range_line_color: ColorType
    _range_line_height: int
    _range_line_pos: Tuple2IntType
    _range_margin: Tuple2IntType
    _range_pos: Tuple2IntType
    _range_text_value_color: ColorType
    _range_text_value_enabled: bool
    _range_text_value_font: Optional[FontType]
    _range_text_value_font_height: NumberType
    _range_text_value_margin: int
    _range_text_value_margin_factor: NumberType
    _range_text_value_position: str
    _range_text_value_surfaces: List['pygame.Surface']
    _range_text_value_surfaces_pos: List[Tuple2IntType]
    _range_text_value_tick_color: ColorType
    _range_text_value_tick_enabled: bool
    _range_text_value_tick_height: int
    _range_text_value_tick_height_factor: NumberType
    _range_text_value_tick_number: int
    _range_text_value_tick_surfaces: List['pygame.Surface']
    _range_text_value_tick_surfaces_pos: List[Tuple2IntType]
    _range_text_value_tick_thickness: int
    _range_values: RangeSliderRangeValueType
    _range_width: int
    _scrolling: bool  # Slider is scrolling
    _selected_mouse: bool
    _single: bool  # Range single or double
    _slider: List['pygame.Surface']
    _slider_color: ColorType
    _slider_height: int
    _slider_height_factor: NumberType
    _slider_pos: Tuple[Tuple2IntType, Tuple2IntType]
    _slider_selected: Tuple[bool, bool]
    _slider_selected_color: ColorType
    _slider_selected_highlight_color: ColorType
    _slider_selected_highlight_enabled: bool
    _slider_selected_highlight_thickness: int
    _slider_text_value_bgcolor: ColorType
    _slider_text_value_color: ColorType
    _slider_text_value_enabled: bool
    _slider_text_value_font: Optional[FontType]
    _slider_text_value_font_height: NumberType
    _slider_text_value_margin: int
    _slider_text_value_margin_factor: NumberType
    _slider_text_value_padding: Tuple4IntType
    _slider_text_value_position: str
    _slider_text_value_surfaces: List['pygame.Surface']
    _slider_text_value_surfaces_pos: List[Tuple2IntType]
    _slider_text_value_triangle: bool
    _slider_text_value_vmargin: int
    _slider_thickness: int
    _slider_vmargin: NumberType
    _value: List[NumberType]  # Public value of the slider, generated from the hidden
    _value_format: RangeSliderValueFormatType
    _value_hidden: List[NumberType]  # Hidden value of the slider, modified by events

    def __init__(
            self,
            title: Any,
            rangeslider_id: str = '',
            default_value: RangeSliderValueType = 0,
            range_values: RangeSliderRangeValueType = (0, 1),
            range_width: int = 150,
            increment: NumberType = 0.1,
            onchange: CallbackType = None,
            onreturn: CallbackType = None,
            onselect: CallbackType = None,
            range_box_color: ColorInputType = (6, 119, 206, 170),
            range_box_color_readonly: ColorInputType = (200, 200, 200, 170),
            range_box_enabled: bool = True,
            range_box_height_factor: NumberType = 0.45,
            range_box_single_slider: bool = False,
            range_line_color: ColorInputType = (100, 100, 100),
            range_line_height: int = 2,
            range_margin: Tuple2IntType = (25, 0),
            range_text_value_color: ColorInputType = (80, 80, 80),
            range_text_value_enabled: bool = True,
            range_text_value_font: Optional[FontType] = None,
            range_text_value_font_height: NumberType = 0.4,
            range_text_value_margin_f: NumberType = 0.8,
            range_text_value_position: str = POSITION_SOUTH,
            range_text_value_tick_color: ColorInputType = (60, 60, 60),
            range_text_value_tick_enabled: bool = True,
            range_text_value_tick_hfactor: NumberType = 0.35,
            range_text_value_tick_number: int = 2,
            range_text_value_tick_thick: int = 1,
            repeat_keys_initial_ms: NumberType = 400,
            repeat_keys_interval_ms: NumberType = 50,
            slider_color: ColorInputType = (120, 120, 120),
            slider_height_factor: NumberType = 0.7,
            slider_sel_highlight_color: ColorInputType = (0, 0, 0),
            slider_sel_highlight_enabled: bool = True,
            slider_sel_highlight_thick: int = 1,
            slider_selected_color: ColorInputType = (180, 180, 180),
            slider_text_value_bgcolor: ColorInputType = (140, 140, 140),
            slider_text_value_color: ColorInputType = (0, 0, 0),
            slider_text_value_enabled: bool = True,
            slider_text_value_font: Optional[FontType] = None,
            slider_text_value_font_height: NumberType = 0.4,
            slider_text_value_margin_f: NumberType = 1,
            slider_text_value_padding: PaddingType = (0, 4),
            slider_text_value_position: str = POSITION_NORTH,
            slider_text_value_triangle: bool = True,
            slider_thickness: int = 15,
            slider_vmargin: NumberType = 0,
            value_format: RangeSliderValueFormatType = lambda x: str(round(x, 3)),
            *args,
            **kwargs
    ) -> None:
        super(RangeSlider, self).__init__(
            args=args,
            kwargs=kwargs,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            title=title,
            widget_id=rangeslider_id
        )

        # Check ranges
        assert_vector(range_values, 0)
        assert len(range_values) >= 2, \
            'range values length must be equal or greater than 2'
        if len(range_values) == 2:
            assert range_values[1] > range_values[0], \
                'range values must be increasing and different numeric values'
        else:
            for i in range(len(range_values) - 1):
                assert range_values[i] < range_values[i + 1], \
                    'range values list must be ordered and different'
        assert isinstance(range_width, int)
        assert range_width > 0, 'range width must be greater than zero'

        # Check default value
        if not isinstance(default_value, NumberInstance):
            assert_vector(default_value, 2)
            assert default_value[0] < default_value[1], \
                'default value vector must be ordered and different (min,max)'
            assert default_value[0] >= range_values[0], \
                f'minimum default value ({default_value[0]}) must be equal or ' \
                f'greater than minimum value of the range ({range_values[0]})'
            assert default_value[1] <= range_values[-1], \
                f'maximum default value ({default_value[1]}) must be lower or ' \
                f'equal than maximum value of the range ({range_values[-1]})'
            default_value = tuple(default_value)

        else:
            assert range_values[0] <= default_value <= range_values[-1], \
                f'default value ({default_value}) must be between minimum and maximum' \
                f' of the range values ({range_values[0]}, {range_values[-1]}), that ' \
                f'is, it must satisfy {range_values[0]}<={default_value}<={range_values[-1]}'

        # If range is discrete, check default value within list
        if len(range_values) > 2:
            if not isinstance(default_value, NumberInstance):
                assert default_value[0] in range_values, \
                    f'min default value ({default_value[0]}) must be within range'
                assert default_value[1] in range_values, \
                    f'max default value ({default_value[1]}) must be within range'
            else:
                assert default_value in range_values, \
                    f'default value ({default_value}) must be within range values'

        # Check increment
        assert isinstance(increment, NumberInstance)
        assert increment >= 0, 'increment must be equal or greater than zero'

        # Check fonts
        if range_text_value_font is not None:
            assert_font(range_text_value_font)
        assert isinstance(range_text_value_font_height, NumberInstance)
        assert 0 < range_text_value_font_height, \
            'range text value font height must be greater than zero'
        if slider_text_value_font is not None:
            assert_font(slider_text_value_font)
        assert isinstance(slider_text_value_font_height, NumberInstance)
        assert 0 < slider_text_value_font_height, \
            'slider text value font height must be greater than zero'

        # Check colors
        range_box_color = assert_color(range_box_color)
        range_box_color_readonly = assert_color(range_box_color_readonly)
        range_line_color = assert_color(range_line_color)
        range_text_value_color = assert_color(range_text_value_color)
        range_text_value_tick_color = assert_color(range_text_value_tick_color)
        slider_color = assert_color(slider_color)
        slider_selected_color = assert_color(slider_selected_color)
        slider_sel_highlight_color = assert_color(slider_sel_highlight_color)
        slider_text_value_bgcolor = assert_color(slider_text_value_bgcolor)
        slider_text_value_color = assert_color(slider_text_value_color)

        # Check dimensions and sizes
        assert isinstance(range_box_height_factor, NumberInstance)
        assert 0 < range_box_height_factor, \
            'height factor must be greater than zero'
        assert isinstance(range_text_value_margin_f, NumberInstance)
        assert 0 < range_text_value_margin_f, \
            'height factor must be greater than zero'
        assert isinstance(slider_text_value_margin_f, NumberInstance)
        assert 0 < slider_text_value_margin_f, \
            'height factor must be greater than zero'
        assert isinstance(slider_height_factor, NumberInstance)
        assert 0 < slider_height_factor, \
            'height factor must be greater than zero'
        assert isinstance(slider_vmargin, NumberInstance)
        slider_text_value_padding = parse_padding(slider_text_value_padding)
        assert isinstance(slider_thickness, int)
        assert slider_thickness > 0, \
            'slider thickness must be greater than zero'
        assert isinstance(range_line_height, int)
        assert range_line_height >= 0, \
            'range line height must be equal or greater than zero'
        assert_vector(range_margin, 2, int)
        assert isinstance(range_text_value_tick_number, int)
        if range_text_value_enabled:
            assert range_text_value_tick_number >= 2, \
                'number of range value must be equal or greater than 2'
        assert isinstance(range_text_value_tick_thick, int)
        assert range_text_value_tick_thick >= 1, \
            'range text tick thickness must be equal or greater than 1 px'
        assert isinstance(slider_sel_highlight_thick, int)
        assert slider_sel_highlight_thick >= 1, \
            'selected highlight thickness must be equal or greater than 1 px'

        # Check positions
        assert_position(range_text_value_position)
        assert range_text_value_position in (POSITION_NORTH, POSITION_SOUTH), \
            'range text value position must be north or south'
        assert_position(slider_text_value_position)
        assert slider_text_value_position in (POSITION_NORTH, POSITION_SOUTH), \
            'slider text value position must be north or south'

        # Check boolean
        assert isinstance(range_box_enabled, bool)
        assert isinstance(range_box_single_slider, bool)
        assert isinstance(range_text_value_enabled, bool)
        assert isinstance(range_text_value_enabled, bool)
        assert isinstance(slider_sel_highlight_enabled, bool)
        assert isinstance(slider_text_value_enabled, bool)
        assert isinstance(slider_text_value_triangle, bool)

        # Check the value format function
        assert is_callable(value_format)
        assert isinstance(value_format(0), str), \
            'value_format must be a function that accepts only 1 argument ' \
            '(value) and must return a string'

        # Single value
        single = isinstance(default_value, NumberInstance)

        # Convert default value to list
        if isinstance(default_value, NumberInstance):
            default_value = [default_value, 0]
        else:
            default_value = [default_value[0], default_value[1]]

        # Store properties
        self._clock = pygame.time.Clock()
        self._default_value = tuple(default_value)
        self._increment = increment
        self._increment_shift_factor = 0.5
        self._keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self._keyrepeat_initial_interval_ms = repeat_keys_initial_ms
        self._keyrepeat_interval_ms = repeat_keys_interval_ms
        self._range_box_color = range_box_color
        self._range_box_color_readonly = range_box_color_readonly
        self._range_box_enabled = range_box_enabled
        self._range_box_height_factor = range_box_height_factor
        self._range_box_single_slider = range_box_single_slider
        self._range_line_color = range_line_color
        self._range_line_height = range_line_height
        self._range_margin = range_margin
        self._range_pos = (0, 0)
        self._range_text_value_color = range_text_value_color
        self._range_text_value_enabled = range_text_value_enabled
        self._range_text_value_font = range_text_value_font
        self._range_text_value_font_height = range_text_value_font_height
        self._range_text_value_margin = 0
        self._range_text_value_margin_factor = range_text_value_margin_f
        self._range_text_value_position = range_text_value_position
        self._range_text_value_tick_color = range_text_value_tick_color
        self._range_text_value_tick_enabled = range_text_value_tick_enabled
        self._range_text_value_tick_height = 0
        self._range_text_value_tick_height_factor = range_text_value_tick_hfactor
        self._range_text_value_tick_number = range_text_value_tick_number
        self._range_text_value_tick_thickness = range_text_value_tick_thick
        self._range_values = tuple(range_values)
        self._range_width = range_width
        self._scrolling = False
        self._selected_mouse = False
        self._single = single
        self._slider_color = slider_color
        self._slider_height = 0
        self._slider_height_factor = slider_height_factor
        self._slider_selected = (True, False)
        self._slider_selected_color = slider_selected_color
        self._slider_selected_highlight_color = slider_sel_highlight_color
        self._slider_selected_highlight_enabled = slider_sel_highlight_enabled
        self._slider_selected_highlight_thickness = slider_sel_highlight_thick
        self._slider_text_value_bgcolor = slider_text_value_bgcolor
        self._slider_text_value_color = slider_text_value_color
        self._slider_text_value_enabled = slider_text_value_enabled
        self._slider_text_value_font = slider_text_value_font
        self._slider_text_value_font_height = slider_text_value_font_height
        self._slider_text_value_margin_factor = slider_text_value_margin_f
        self._slider_text_value_padding = slider_text_value_padding
        self._slider_text_value_position = slider_text_value_position
        self._slider_text_value_triangle = slider_text_value_triangle
        self._slider_text_value_vmargin = 0
        self._slider_thickness = slider_thickness
        self._slider_vmargin = slider_vmargin
        self._value = default_value
        self._value_format = value_format
        self._value_hidden = default_value.copy()  # Used when dragging mouse on discrete range

    def value_changed(self) -> bool:
        if self._single:
            return self.get_value() != self._default_value[0]
        return self.get_value() != self._default_value

    def reset_value(self) -> 'Widget':
        if self._single:
            self.set_value(self._default_value[0])
        else:
            self.set_value(self._default_value)
        return self

    def set_value(self, value: RangeSliderValueType) -> None:
        if self._single:
            assert isinstance(value, NumberInstance)
            # noinspection PyTypeChecker
            assert self._range_values[0] <= value <= self._range_values[-1], \
                f'value ({value}) must be within range {self._range_values[0]} <=' \
                f' {value} <= {self._range_values[1]}'
            if len(self._range_values) > 2:
                assert value in self._range_values, \
                    'value must be between range values discrete list'
            value = [value, 0]

        else:
            assert_vector(value, 2)
            assert self._range_values[0] <= value[0], \
                'value must be equal or greater than minimum range value'
            assert value[1] <= self._range_values[-1], \
                'value must be lower or equal than maximum range value'
            assert value[0] < value[1], 'value vector must be ordered'
            if len(self._range_values) > 2:
                assert value[0] in self._range_values
                assert value[1] in self._range_values
            value = [value[0], value[1]]

        self._value = value
        self._value_hidden = self._value.copy()
        self._render()

    def scale(self, *args, **kwargs) -> 'RangeSlider':
        raise WidgetTransformationNotImplemented()

    def resize(self, *args, **kwargs) -> 'RangeSlider':
        raise WidgetTransformationNotImplemented()

    def set_max_width(self, *args, **kwargs) -> 'RangeSlider':
        raise WidgetTransformationNotImplemented()

    def set_max_height(self, *args, **kwargs) -> 'RangeSlider':
        raise WidgetTransformationNotImplemented()

    def rotate(self, *args, **kwargs) -> 'RangeSlider':
        raise WidgetTransformationNotImplemented()

    def flip(self, *args, **kwargs) -> 'RangeSlider':
        raise WidgetTransformationNotImplemented()

    def get_value(self) -> Union[NumberType, Tuple[NumberType, NumberType]]:
        if self._single:
            return self._value[0]
        return self._value[0], self._value[1]

    def _apply_font(self) -> None:
        if self._range_text_value_font is None:
            self._range_text_value_font = self._font_name
        if self._slider_text_value_font is None:
            self._slider_text_value_font = self._font_name

        self._font_range_value = pygame_menu.font.get_font(
            self._range_text_value_font,
            int(self._range_text_value_font_height * self._font_size)
        )
        self._font_slider_value = pygame_menu.font.get_font(
            self._slider_text_value_font,
            int(self._slider_text_value_font_height * self._font_size)
        )

        # Compute the height
        height = self._font_render_string('TEST').get_height()
        self._range_box_height = int(height * self._range_box_height_factor)
        self._slider_height = int(height * self._slider_height_factor)
        self._range_text_value_margin = int(height * self._range_text_value_margin_factor)
        self._range_text_value_tick_height = int(height * self._range_text_value_tick_height_factor)
        self._slider_text_value_margin = int(height * self._slider_text_value_margin_factor)

    def _draw(self, surface: 'pygame.Surface') -> None:
        # Draw title
        surface.blit(self._surface, self._rect.topleft)

        # Draw range line
        surface.blit(self._range_line, (self._range_line_pos[0] + self._rect.x,
                                        self._range_line_pos[1] + self._rect.y))

        # Draw range values and ticks
        for i in range(len(self._range_text_value_surfaces)):
            if self._range_text_value_enabled:
                surface.blit(self._range_text_value_surfaces[i],
                             (self._rect.x + self._range_text_value_surfaces_pos[i][0],
                              self._rect.y + self._range_text_value_surfaces_pos[i][1]))
            if self._range_text_value_tick_enabled:
                tick_i = self._range_text_value_tick_surfaces[i]
                surface.blit(tick_i,
                             (self._rect.x + self._range_text_value_tick_surfaces_pos[i][0],
                              self._rect.y + self._range_text_value_tick_surfaces_pos[i][1]))

        # Draw range box
        if self._range_box_enabled and (not self._single or self._range_box_single_slider):
            surface.blit(self._range_box, (self._range_box_pos[0] + self._rect.x,
                                           self._range_box_pos[1] + self._rect.y))

        # Draw sliders
        surface.blit(self._slider[0], (self._slider_pos[0][0] + self._rect.x,
                                       self._slider_pos[0][1] + self._rect.y))
        if not self._single:
            surface.blit(self._slider[1], (self._slider_pos[1][0] + self._rect.x,
                                           self._slider_pos[1][1] + self._rect.y))

        # Draw slider highlighted
        if self._slider_selected[0] and not self.readonly and self.is_selected():
            pygame.draw.rect(
                surface, self._slider_selected_highlight_color,
                self._get_slider_inflate_rect(0), self._slider_selected_highlight_thickness
            )
        if self._slider_selected[1] and not self.readonly and self.is_selected():
            pygame.draw.rect(
                surface, self._slider_selected_highlight_color,
                self._get_slider_inflate_rect(1), self._slider_selected_highlight_thickness
            )

    def draw_after_if_selected(self, surface: Optional['pygame.Surface']) -> 'RangeSlider':
        super(RangeSlider, self).draw_after_if_selected(surface)
        self.last_surface = surface

        # Draw slider value
        if self._slider_text_value_enabled and not self.readonly:
            surface.blit(
                self._slider_text_value_surfaces[0],
                (self._slider_text_value_surfaces_pos[0][0] + self._rect.x,
                 self._slider_text_value_surfaces_pos[0][1] + self._rect.y)
            )
            if not self._single:
                surface.blit(
                    self._slider_text_value_surfaces[1],
                    (self._slider_text_value_surfaces_pos[1][0] + self._rect.x,
                     self._slider_text_value_surfaces_pos[1][1] + self._rect.y)
                )

        return self

    def _get_slider_inflate_rect(
            self,
            pos: int,
            inflate: Optional[Tuple2IntType] = None,
            to_real_position: bool = False,
            to_absolute_position: bool = False,
            real_position_visible: bool = True
    ) -> 'pygame.Rect':
        """
        Return the slider inflate rect.

        :param pos: Which slider 0/1
        :param inflate: Inflate in x, y
        :param to_real_position: Transform the widget rect to real coordinates. Used by events
        :param to_absolute_position: Transform the widget rect to absolute coordinates. Used by events
        :param real_position_visible: Return only the visible width/height if ``to_real_position=True``
        :return: Slider inflated rect
        """
        if inflate is None:
            inflate = (0, 0)
        s = self._slider[pos]
        rect = s.get_rect()

        rect.x += self._slider_pos[pos][0] + self._rect.x
        rect.y += self._slider_pos[pos][1] + self._rect.y
        rect = pygame.Rect(
            int(rect.x - inflate[0] / 2),
            int(rect.y - inflate[1] / 2),
            int(rect.width + inflate[0]),
            int(rect.height + inflate[1])
        )

        if self._scrollarea is not None:
            assert not (to_real_position and to_absolute_position), \
                'real and absolute positions cannot be True at the same time'
            if to_real_position:
                rect = self._scrollarea.to_real_position(rect, visible=real_position_visible)
            elif to_absolute_position:
                rect = self._scrollarea.to_absolute_position(rect)

        return rect

    def _render(self) -> Optional[bool]:
        if not hasattr(self, '_font_range_value'):
            return False

        if not self._render_hash_changed(
                self._selected, self._title, self._visible, self.readonly,
                self._range_values, self._slider_selected, self._value[0],
                self._value[1], self._scrolling, self._selected_mouse):
            return True

        # Create basic title
        self._surface = self._render_string(self._title, self.get_font_color_status())
        self._rect.width, self._rect.height = self._surface.get_size()
        self._range_pos = (self._rect.width + self._range_margin[0],
                           int(self._rect.height / 2) + self._range_margin[1])

        # Create slider
        sel_s = self._slider_selected[0] and self._selected and not self.readonly, \
                self._slider_selected[1] and self._selected and not self.readonly
        self._slider = [
            make_surface(self._slider_thickness, self._slider_height,
                         fill_color=(self._slider_color if not self.readonly else self._font_readonly_color)
                         if not sel_s[0] else self._slider_selected_color),
            make_surface(self._slider_thickness, self._slider_height,
                         fill_color=(self._slider_color if not self.readonly else self._font_readonly_color)
                         if not sel_s[1] else self._slider_selected_color)
        ]
        slider_vm = int(self._slider_vmargin * self._rect.height)  # Vertical margin
        if self._single:
            self._slider_pos = (
                (self._range_pos[0] + self._get_pos_range(self._value[0], self._slider[0]),
                 self._range_pos[1] + slider_vm - int(self._slider_height / 2)),
                (0, 0)
            )
        else:
            self._slider_pos = (
                (self._range_pos[0] + self._get_pos_range(self._value[0], self._slider[0]),
                 self._range_pos[1] + slider_vm - int(self._slider_height / 2)),
                (self._range_pos[0] + self._get_pos_range(self._value[1], self._slider[1]),
                 self._range_pos[1] + slider_vm - int(self._slider_height / 2))
            )

        # Create the range line
        self._range_line = make_surface(self._range_width, self._range_line_height,
                                        fill_color=self._range_line_color)
        self._range_line_pos = (self._range_pos[0],
                                int(self._range_pos[1] - self._range_line_height / 2))

        # Create the range font surfaces
        range_values: List[NumberType] = []
        if len(self._range_values) == 2:
            d_val = (self._range_values[1] - self._range_values[0]) \
                    / (self._range_text_value_tick_number - 1)
            v_i = self._range_values[0]
            for i in range(self._range_text_value_tick_number):
                range_values.append(v_i)
                v_i += d_val
        else:
            for i in self._range_values:
                range_values.append(i)

        # Create surfaces for each range value text & position + ticks
        self._range_text_value_surfaces = []
        self._range_text_value_surfaces_pos = []
        self._range_text_value_tick_surfaces = []
        self._range_text_value_tick_surfaces_pos = []
        range_value_pos = 1 if self._range_text_value_position == POSITION_SOUTH else -1
        for i in range_values:
            s = self._font_range_value.render(
                self._value_format(i), self._font_antialias,
                self._range_text_value_color if not self.readonly else self._font_readonly_color)
            self._range_text_value_surfaces.append(s)
            s_x = self._range_pos[0] + self._get_pos_range(i, s)
            s_y = self._range_pos[1] + self._range_text_value_margin / 2 * range_value_pos
            self._range_text_value_surfaces_pos.append((int(s_x), int(s_y)))

            # Create the tick
            s_tick = make_surface(self._range_text_value_tick_thickness,
                                  self._range_text_value_tick_height,
                                  fill_color=self._range_text_value_tick_color)
            self._range_text_value_tick_surfaces.append(s_tick)
            t_x = self._range_pos[0] + self._get_pos_range(i)
            t_y = self._range_pos[1] - s_tick.get_height() / 2
            self._range_text_value_tick_surfaces_pos.append((int(t_x), int(t_y)))

        # Computes the height of the ranges value text for modifying the rect box sizing
        range_values_size = 0, 0  # Stores sizing
        if self._range_text_value_enabled:
            s = self._range_text_value_surfaces[0]
            range_values_size = (int(s.get_width() * 0.7),
                                 int(self._range_text_value_surfaces_pos[0][1] + s.get_height() * 0.9))

        # Create the range box surface
        if not self._single or self._range_box_single_slider:
            r_pos = 0 if self._single else self._get_pos_range(self._value[0])
            r_width = self._get_distance_between_sliders()
            self._range_box = make_surface(
                max(0, r_width), self._range_box_height,
                fill_color=self._range_box_color if not self.readonly else self._range_box_color_readonly)
            self._range_box_pos = (self._range_pos[0] + r_pos,
                                   self._range_pos[1] - int(self._range_box.get_height() / 2))

        # Create the slider values
        self._slider_text_value_surfaces = []
        self._slider_text_value_surfaces_pos = []
        for v in self._value:
            t = self._font_slider_value.render(self._value_format(v), self._font_antialias,
                                               self._slider_text_value_color)  # Value text
            st = make_surface(
                t.get_width() + self._slider_text_value_padding[1] + self._slider_text_value_padding[3],
                t.get_height() + self._slider_text_value_padding[0] + self._slider_text_value_padding[2],
                fill_color=self._slider_text_value_bgcolor)
            st.blit(t, (self._slider_text_value_padding[1],
                        self._slider_text_value_padding[0] + self._slider_text_value_vmargin))

            # Create surface that considers st and the triangle
            tri_height = int(self._slider_text_value_margin / 2) - int(self._slider_height / 2)
            if tri_height and self._slider_text_value_triangle:
                st_root = make_surface(st.get_width(), st.get_height() + tri_height)
                st_root.blit(st, (0, 0))
                mid = st.get_width() / 2
                hig = st.get_height()
                w = tri_height / math.sqrt(3)
                tri_poly = ((mid - w, hig), (mid + w, hig), (mid, hig + tri_height))
                pygame.draw.polygon(st_root, self._slider_text_value_bgcolor, tri_poly)
            else:
                st_root = st

            self._slider_text_value_surfaces.append(st_root)
            st_x = self._range_pos[0] + self._get_pos_range(v, st)
            st_y = self._range_pos[1] - int(self._slider_text_value_margin / 2) - st.get_height()
            self._slider_text_value_surfaces_pos.append((st_x, st_y))

        # Update maximum rect height
        self._rect.height = max(self._rect.height, self._slider_height,
                                self._range_line_height, range_values_size[1])
        self._rect.height += self._range_margin[1]
        self._rect.width += self._range_width + self._range_margin[0] + range_values_size[0]

        # Finals
        self.force_menu_surface_update()

    def _get_pos_range(self, value: NumberType, surface: Optional['pygame.Surface'] = None) -> int:
        """
        Return the position of the surface within range slider.

        :param value: Value
        :param surface: Surface or None
        :return: Position in px
        """
        sw = surface.get_width() / 2 if surface is not None else 0
        if len(self._range_values) == 2:
            d = float(value - self._range_values[0]) / (self._range_values[1] - self._range_values[0])
            return int(d * self._range_width - sw)

        # Find nearest position
        n, t = self._find_nearest_discrete_range(value), len(self._range_values)
        return int((float(n) / (t - 1)) * self._range_width - sw)

    def _get_distance_between_sliders(self) -> int:
        """
        Returns the distance between both sliders.

        :return: Distance in px
        """
        if not self._single:
            return self._get_pos_range(self._value[1]) - self._get_pos_range(self._value[0])
        return self._get_pos_range(self._value[0])

    def _find_nearest_discrete_range(self, value: NumberType) -> int:
        """
        Return the nearest position of value from range discrete list.

        :param value: Value to find
        :return: Position of the list
        """
        n = 0  # Position of the nearest value
        m = math.inf  # Maximum distance
        t = len(self._range_values)  # Number of values
        for j in range(t):
            k = abs(self._range_values[j] - value)
            if k < m:
                m = k  # Update max
                n = j
        return n

    def _update_value(self, delta: NumberType) -> bool:
        """
        Updates the value of the active slider by delta.

        :param delta: Delta value
        :return: True if value changed
        """
        if self.readonly:
            return False

        old_value = self._value.copy()
        old_value_hidden = self._value_hidden.copy()
        slider_idx = 0 if self._slider_selected[0] else 1

        self._value_hidden[slider_idx] += delta
        if self._value_hidden[0] >= self._value_hidden[1] and not self._single:
            self._value_hidden = old_value_hidden
        else:
            self._value_hidden[slider_idx] = max(
                self._range_values[0], min(self._range_values[-1], self._value_hidden[slider_idx]))

        # Update real value
        if len(self._range_values) == 2:
            self._value = self._value_hidden
        else:
            # Find nearest
            val_index_nearest = self._find_nearest_discrete_range(self._value_hidden[slider_idx])
            self._value[slider_idx] = self._range_values[val_index_nearest]
            if self._value[0] >= self._value[1] and not self._single:
                self._value = old_value

        changed = old_value_hidden != self._value_hidden
        if changed:
            self.change()

        return changed

    def _blur(self) -> None:
        self._selected_mouse = False

    def _focus(self) -> None:
        self._selected_mouse = False

    def _left_right(self, event, left: bool) -> bool:
        """
        Process left and right event keys.

        :param event: Event
        :param left: ``True`` if left, right otherwise
        :return: ``True`` if updated
        """
        self._value_hidden = self._value.copy()  # Update hidden to real value
        if event.key not in self._keyrepeat_counters:
            self._keyrepeat_counters[event.key] = 0
        keys_pressed = pygame.key.get_pressed()

        # If not discrete, apply delta as increment
        if len(self._range_values) == 2:
            mod = 1 if not (keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]) \
                else self._increment_shift_factor
            if left:
                mod *= -1
            delta = self._increment * mod

        # If discrete, find the current index and subtract +-1, then find the delta
        # as the difference between two states
        else:
            if not self._single:
                slider_idx = 0 if self._slider_selected[0] else 1
            else:
                slider_idx = 0
            current_val_idx = self._find_nearest_discrete_range(self._value[slider_idx])
            new_val_idx = current_val_idx
            if left:
                new_val_idx = max(0, new_val_idx - 1)
            else:
                new_val_idx = min(len(self._range_values) - 1, new_val_idx + 1)
            delta = self._range_values[new_val_idx] - self._range_values[current_val_idx]

        if self._update_value(delta):
            self._sound.play_key_add()
            return True
        return False

    def _test_get_pos_value(self, value: NumberType, dx: int = 0, dy: int = 0) -> Tuple2IntType:
        """
        Return the position of the value in real coordinates, used for testing.

        :param value: Value to get position
        :param dx: Delta for x position in px
        :param dy: Delta for y position in px
        :return: (x, y) position
        """
        rect = self.get_rect(to_real_position=True, apply_padding=False)
        rect.x += self._range_pos[0] + self._get_pos_range(value)
        rect.y += self._range_pos[1]
        return rect.x + dx, rect.y + dy

    def update(self, events: EventVectorType) -> bool:
        self.apply_update_callbacks(events)

        self._clock.tick(60)

        if self.readonly or not self.is_visible():
            self._readonly_check_mouseover(events)
            return False

        # Get time clock
        time_clock = self._clock.get_time()

        updated = False
        events = self._merge_events(events)  # Extend events with custom events

        for event in events:

            if event.type == pygame.KEYDOWN:  # Check key is valid
                if self._ignores_keyboard_nonphysical() and not check_key_pressed_valid(event):
                    continue

            # Check mouse over
            self._check_mouseover(event)

            # Events
            keydown = self._keyboard_enabled and event.type == pygame.KEYDOWN
            joy_hatmotion = self._joystick_enabled and event.type == pygame.JOYHATMOTION
            joy_axismotion = self._joystick_enabled and event.type == pygame.JOYAXISMOTION
            joy_button_down = self._joystick_enabled and event.type == pygame.JOYBUTTONDOWN

            # Left button
            if keydown and event.key == ctrl.KEY_LEFT or \
                    joy_hatmotion and event.value == ctrl.JOY_LEFT or \
                    joy_axismotion and event.axis == ctrl.JOY_AXIS_X and event.value < ctrl.JOY_DEADZONE:
                if self._left_right(event, True):
                    return True

            # Right button
            elif keydown and event.key == ctrl.KEY_RIGHT or \
                    joy_hatmotion and event.value == ctrl.JOY_RIGHT or \
                    joy_axismotion and event.axis == ctrl.JOY_AXIS_X and event.value > -ctrl.JOY_DEADZONE:
                if self._left_right(event, False):
                    return True

            # Press enter
            elif keydown and event.key == ctrl.KEY_APPLY or \
                    joy_button_down and event.button == ctrl.JOY_BUTTON_SELECT:
                self.apply()
                return True

            # Tab, switch active slider
            elif keydown and event.key == ctrl.KEY_TAB:
                if self._single:
                    continue
                self._slider_selected = (False, True) if self._slider_selected[0] else (True, False)
                return True

            # Releases key
            elif event.type == pygame.KEYUP and self._keyboard_enabled:
                if event.key in self._keyrepeat_counters:
                    del self._keyrepeat_counters[event.key]

            # User clicks the slider rect
            elif event.type == pygame.MOUSEBUTTONDOWN and self._mouse_enabled or \
                    event.type == FINGERDOWN and self._touchscreen_enabled and \
                    self._menu is not None:
                event_pos = get_finger_pos(self._menu, event)

                # Check which slider is clicked
                rect_slider_0 = self._get_slider_inflate_rect(0, to_real_position=True)
                rect_slider_1 = self._get_slider_inflate_rect(1, to_real_position=True)

                rc_1 = rect_slider_0.collidepoint(*event_pos)
                rc_2 = rect_slider_1.collidepoint(*event_pos)

                old_slider_selected = self._slider_selected
                if not self._single:
                    # Check sliders does not collide each other
                    dist_sliders = self._get_distance_between_sliders()
                    sliders_intersect = dist_sliders <= (self._slider_thickness - 1)

                    if rc_1 and not sliders_intersect:
                        self._slider_selected = (True, False)
                    elif rc_2 and not sliders_intersect:
                        self._slider_selected = (False, True)

                if old_slider_selected != self._slider_selected:
                    updated = True
                    self._render()

                # Check if slider is clicked
                self._scrolling = bool(rc_1 or rc_2)
                self._selected_mouse = True

            # User releases the mouse
            elif event.type == pygame.MOUSEBUTTONUP and self._mouse_enabled and \
                    event.button in (1, 2, 3) or \
                    event.type == FINGERUP and self._touchscreen_enabled and \
                    self._menu is not None:
                event_pos = get_finger_pos(self._menu, event)

                # If collides and not scroll, update the value to the clicked position
                rect = self.get_rect(to_real_position=True, apply_padding=False)
                if rect.collidepoint(*event_pos) and not self._scrolling and self._selected_mouse:
                    mouse_x, _ = event_pos
                    topleft, _ = rect.topleft
                    topright, _ = rect.topright

                    # Distance from title
                    dist = mouse_x - (topleft + self._range_pos[0])

                    # Current slider active value
                    val = self._value[0] if self._single else self._value[0 if self._slider_selected[0] else 1]
                    val_px = self._get_pos_range(val)

                    delta = (self._range_values[-1] - self._range_values[0]) * (dist - val_px) / self._range_width

                    if delta != 0 and dist >= 0:  # If clicked true value
                        if self._update_value(delta):
                            updated = True

                self._selected_mouse = False

                # Disables scrolling
                if self._scrolling:
                    self._scrolling = False
                    self._value_hidden = self._value.copy()
                    updated = True

            # User scrolls clicked slider
            elif (event.type == pygame.MOUSEMOTION and self._mouse_enabled and hasattr(event, 'rel') or
                  event.type == FINGERMOTION and self._touchscreen_enabled and self._menu is not None) and \
                    self._scrolling and self._selected_mouse:
                rel = event.rel[0] if event.type == pygame.MOUSEMOTION else \
                    event.dx * 2 * self._menu.get_window_size()[0]
                delta = (self._range_values[-1] - self._range_values[0]) * rel / self._range_width

                # Check mouse position
                mx, my = event.pos if event.type == pygame.MOUSEMOTION else \
                    get_finger_pos(self._menu, event)
                rect = self.get_rect(to_real_position=True, apply_padding=False)

                # Compute position of mouse within valid range
                dist_x = mx - (rect.x + self._range_pos[0])
                dist_y = my - rect.y

                # Get current slider pos if not single
                x_max_min = 0, self._range_width
                if not self._single:
                    slider_idx = 0 if self._slider_selected[0] else 1
                    slider_pos = self._get_pos_range(self._value[slider_idx])
                    x_max_min = slider_pos - 1, slider_pos

                # Check slider within rect
                if delta < 0:
                    in_x = -self._slider_height <= dist_x <= x_max_min[1]
                else:
                    in_x = x_max_min[0] <= dist_x <= self._range_width + self._slider_height
                in_y = 0 <= dist_y <= rect.height

                # Checks mouse changed position and within rect position
                if delta != 0 and in_x and in_y:
                    if self._update_value(delta):
                        updated = True

        # Update key counters:
        for key in self._keyrepeat_counters:
            self._keyrepeat_counters[key] += time_clock  # Update clock

            # Generate new key events if enough time has passed:
            if self._keyrepeat_counters[key] >= self._keyrepeat_initial_interval_ms:
                self._keyrepeat_counters[key] = self._keyrepeat_initial_interval_ms - self._keyrepeat_interval_ms
                self._add_event(pygame.event.Event(pygame.KEYDOWN, key=key))

        return updated


class RangeSliderManager(AbstractWidgetManager, ABC):
    """
    RangeSlider manager.
    """

    def range_slider(
            self,
            title: str,
            default: RangeSliderValueType,
            range_values: RangeSliderRangeValueType,
            increment: Optional[NumberType] = None,
            onchange: CallbackType = None,
            onreturn: CallbackType = None,
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            rangeslider_id: str = '',
            value_format: RangeSliderValueFormatType = lambda x: str(round(x, 3)),
            width: int = 150,
            **kwargs
    ) -> 'pygame_menu.widgets.RangeSlider':
        """
        Add a range slider to the Menu: Offers 1 or 2 sliders for defining a unique
        value or a range of numeric ones.

        If the state of the widget changes the ``onchange`` callback is called. The
        state can change by pressing LEFT/RIGHT, or by mouse/touch events.

        .. code-block:: python

            onchange(range_value, **kwargs)

        If pressing return key on the widget:

        .. code-block:: python

            onreturn(range_value, **kwargs)

        If ``onselect`` is defined, the callback is executed as follows, where
        ``selected`` is a boolean representing the selected status:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over
            - ``float``                         (bool) - If ``True`` the widget don't contributes width/height to the Menu widget positioning computation, and don't add one unit to the rows
            - ``float_origin_position``         (bool) - If ``True`` the widget position is set to the top-left position of the Menu if the widget is floating
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``range_box_color_readonly``      (tuple, list, str, int, :py:class:`pygame.Color`) - Color of the range box if widget in readonly state
            - ``range_box_color``               (tuple, list, str, int, :py:class:`pygame.Color`) - Color of the range box between the sliders
            - ``range_box_enabled``             (bool) - Enables a range box between two sliders
            - ``range_box_height_factor``       (int, float) - Height of the range box (factor of the range title height)
            - ``range_box_single_slider``       (bool) - Enables range box if there's only 1 slider instead of 2
            - ``range_line_color``              (tuple, list, str, int, :py:class:`pygame.Color`) - Color of the range line
            - ``range_line_height``             (int) - Height of the range line in px
            - ``range_margin``                  (tuple, list) - Range margin on x-axis and y-axis (x, y) from title in px
            - ``range_text_value_color``        (tuple, list, str, int, :py:class:`pygame.Color`) - Color of the range values text
            - ``range_text_value_enabled``      (bool) - Enables the range values text
            - ``range_text_value_font_height``  (int, float) - Height factor of the range value font (factor of the range title height)
            - ``range_text_value_font``         (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) - Font of the ranges value. If ``None`` the same font as the widget is used
            - ``range_text_value_margin_f``     (int, float) - Margin of the range text values (factor of the range title height)
            - ``range_text_value_position``     (str) - Position of the range text values, can be NORTH or SOUTH. See :py:mod:`pygame_menu.locals`
            - ``range_text_value_tick_color``   (tuple, list, str, int, :py:class:`pygame.Color`) - Color of the range text value tick
            - ``range_text_value_tick_enabled`` (bool) - Range text value tick enabled
            - ``range_text_value_tick_hfactor`` (bool) Height factor of the range text value tick (factor of the range title height)
            - ``range_text_value_tick_number``  (int) - Number of range value text, the values are placed uniformly distributed
            - ``range_text_value_tick_thick``   (int) - Thickness of the range text value tick in px
            - ``readonly_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode
            - ``readonly_selected_color``       (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode and is selected
            - ``repeat_keys_initial_ms``        (int) - Time in ms before keys are repeated when held in ms. ``400`` by default
            - ``repeat_keys_interval_ms``       (int) - Interval between key press repetition when held in ms. ``50`` by default
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect
            - ``shadow_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget shadow
            - ``shadow_radius``                 (int) - Border radius of the shadow
            - ``shadow_type``                   (str) - Shadow type, it can be ``'rectangular'`` or ``'ellipse'``
            - ``shadow_width``                  (int) - Width of the shadow. If ``0`` the shadow is disabled
            - ``slider_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) - Slider color
            - ``slider_height_factor``          (int, float) - Height of the slider (factor of the range title height)
            - ``slider_sel_highlight_color``    (tuple, list, str, int, :py:class:`pygame.Color`) - Color of the selected slider highlight box effect
            - ``slider_sel_highlight_enabled``  (bool) - Selected slider is highlighted
            - ``slider_sel_highlight_thick``    (int) - Thickness of the selected slider highlight
            - ``slider_selected_color``         (tuple, list, str, int, :py:class:`pygame.Color`) - Selected slider color
            - ``slider_text_value_bgcolor``     (tuple, list, str, int, :py:class:`pygame.Color`) - Background color of the value text on each slider
            - ``slider_text_value_color``       (tuple, list, str, int, :py:class:`pygame.Color`) - Color of value text on each slider
            - ``slider_text_value_enabled``     (bool) - Enables a value text on each slider
            - ``slider_text_value_font_height`` (int, float) - Height factor of the slider font (factor of the range title height)
            - ``slider_text_value_font``        (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) - Font of the slider value. If ``None`` the same font as the widget is used
            - ``slider_text_value_margin_f``    (int, float) - Margin of the slider text values (factor of the range title height)
            - ``slider_text_value_padding``     (int, float, tuple, list) – Padding of the slider text values
            - ``slider_text_value_position``    (str) - Position of the slider text values, can be NORTH or SOUTH. See :py:mod:`pygame_menu.locals`
            - ``slider_text_value_triangle``    (bool) - Draws a triangle between slider text value and slider
            - ``slider_thickness``              (int) - Slider thickness in px
            - ``slider_vmargin``                (int, float) - Vertical margin of the slider (factor of the range title height)
            - ``tab_size``                      (int) – Width of a tab character

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Title of the range slider
        :param default: Default range value, can accept a number or a tuple/list of 2 elements (min, max). If a single number is provided the rangeslider only accepts 1 value, if 2 are provided, the range is enabled (2 values)
        :param range_values: Tuple/list of 2 elements of min/max values of the range slider. Also range can accept a list of numbers, in which case the values of the range slider will be discrete. List must be sorted
        :param increment: Increment of the value if using left/right keys; used only if the range values are not discrete
        :param onchange: Callback executed when when changing the value of the range slider
        :param onreturn: Callback executed when pressing return on the range slider
        :param onselect: Callback executed when selecting the widget
        :param rangeslider_id: ID of the range slider
        :param value_format: Function that format the value and returns a string that is used in the range and slider text
        :param width: Width of the range in px
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.RangeSlider`
        """
        assert_vector(range_values, 0)
        if len(range_values) == 2:
            assert isinstance(increment, NumberInstance), \
                'increment must be defined if the range values are not discrete'
        else:
            if increment is None:
                increment = 1

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        range_margin = kwargs.pop('range_margin', self._theme.widget_box_margin)
        range_line_color = kwargs.pop('range_line_color', self._theme.widget_font_color)
        range_text_value_color = kwargs.pop('range_text_value_color',
                                            self._theme.widget_font_color)
        range_text_value_font_height = kwargs.pop('range_text_value_font_height', 0.6)
        range_text_value_tick_hfactor = kwargs.pop('range_text_value_tick_hfactor', 0.5)
        slider_text_value_font_height = kwargs.pop('slider_text_value_font_height', 0.6)

        widget = RangeSlider(
            title=title,
            rangeslider_id=rangeslider_id,
            default_value=default,
            range_values=range_values,
            range_width=width,
            increment=increment,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            range_line_color=range_line_color,
            range_margin=range_margin,
            range_text_value_color=range_text_value_color,
            range_text_value_font_height=range_text_value_font_height,
            range_text_value_tick_hfactor=range_text_value_tick_hfactor,
            slider_text_value_font_height=slider_text_value_font_height,
            value_format=value_format,
            **kwargs
        )
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget
