"""
pygame-menu
https://github.com/ppizarror/pygame-menu

RANGE SLIDER
Slider bar between one/two numeric ranges.

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

__all__ = ['RangeSlider']

import pygame
import pygame_menu
import pygame_menu.controls as ctrl

from pygame_menu.locals import POSITION_NORTH, POSITION_SOUTH
from pygame_menu.font import FontType, assert_font
from pygame_menu.locals import FINGERUP
from pygame_menu.utils import check_key_pressed_valid, assert_color, assert_vector, \
    make_surface, get_finger_pos, assert_position, parse_padding
from pygame_menu.widgets.core.widget import Widget, WidgetTransformationNotImplemented

from pygame_menu._types import Any, CallbackType, Union, List, Tuple, Optional, \
    ColorType, NumberType, Tuple2NumberType, Tuple2IntType, NumberInstance, \
    ColorInputType, EventVectorType, Vector2NumberType, VectorType, PaddingType, \
    PaddingInstance, Tuple4IntType

RangeValuesType = Union[Vector2NumberType, VectorType]


# noinspection PyMissingOrEmptyDocstring
class RangeSlider(Widget):
    """
    Range slider widget. Offers 1 or 2 sliders for defining a unique value or
    a range of numeric ones.

    If the state of the widget changes the ``onchange`` callback is called. The
    state can change by pressing LEFT/RIGHT, or by mouse/touch events.

    .. code-block:: python

        onchange(state_value, **kwargs)

    .. note::

        RangeSlider only accepts translation transformation.

    :param title: Range slider title
    :param rangeslider_id: RangeSlider ID
    :param range_values: Tuple/list of 2 elements of min/max values of the range slider. Also range can accept a list of numbers, in which case the values of the range slider will be discrete. List must be sorted
    :param range_width: Width of the range in pixels
    :param default_value: Default range value, can accept a number or a tuple/list of 2 elements (min, max). If a single number is provided the rangeslider only accepts 1 value, if 2 are provided, the range is enabled (2 values)
    :param increment: Increment of the value if using lef/right keys
    :param onchange: Callback when changing the state of the switch
    :param onselect: Function when selecting the widget
    :param range_box_color: Color of the range box between the sliders
    :param range_box_color_readonly: Color of the range box if widget in readonly state
    :param range_box_enabled: Enables a range box between two sliders
    :param range_box_height_factor: Height of the range box (factor of the range title height)
    :param range_text_value_color: Color of the range values text
    :param range_text_value_enabled: Enables the range values text
    :param range_text_value_font: Font of the ranges value. If ``None`` the same font as the widget is used
    :param range_text_value_font_height: Height factor of the range value font (factor of the range title height)
    :param range_text_value_margin_factor: Margin of the range text values (factor of the range title height)
    :param range_text_value_position: Position of the range text values, can be NORTH or SOUTH. See :py:mod:`pygame_menu.locals`
    :param slider_color: Slider color
    :param slider_color_selected: Selected slider color
    :param slider_height_factor: Height of the slider (factor of the range title height)
    :param slider_text_value_bgcolor: Background color of the value text on each slider
    :param slider_text_value_color: Color of value text on each slider
    :param slider_text_value_enabled: Enables a value text on each slider
    :param slider_text_value_font: Font of the slider value. If ``None`` the same font as the widget is used
    :param slider_text_value_font_height: Height factor of the slider font (factor of the range title height)
    :param slider_text_value_margin_factor: Margin of the slider text values (factor of the range title height)
    :param slider_text_value_padding: Padding of the slider text values
    :param slider_text_value_position: Position of the slider text values, can be NORTH or SOUTH. See :py:mod:`pygame_menu.locals`
    :param slider_thickness: Slider thickness in px
    :param slider_vmargin: Vertical margin of the slider (factor of the range title height)
    :param args: Optional arguments for callbacks
    :param kwargs: Optional keyword arguments
    """
    _range_values: RangeValuesType
    _range_width: int
    _default_value: Union[NumberType, Vector2NumberType]
    _increment: NumberType
    _range_box_color: ColorType
    _range_box_color_readonly: ColorType
    _range_box_enabled: bool
    _range_box_height_factor: NumberType
    _range_text_value_color: ColorType
    _range_text_value_enabled: bool
    _range_text_value_font: Optional[FontType]
    _range_text_value_font_height: NumberType
    _range_text_value_margin_factor: NumberType
    _range_text_value_position: str
    _slider_color: ColorType
    _slider_color_selected: bool
    _slider_height_factor: NumberType
    _slider_text_value_bgcolor: ColorType
    _slider_text_value_color: ColorType
    _slider_text_value_enabled: bool
    _slider_text_value_font: Optional[FontType]
    _slider_text_value_font_height: NumberType
    _slider_text_value_margin_factor: NumberType
    _slider_text_value_padding: Tuple4IntType
    _slider_text_value_position: str
    _slider_thickness: int
    _slider_vmargin: NumberType

    def __init__(
            self,
            title: Any,
            rangeslider_id: str = '',
            range_values: RangeValuesType = (0, 1),
            range_width: int = 150,
            default_value: Union[NumberType, Vector2NumberType] = 0.5,
            increment: NumberType = 0.1,
            onchange: CallbackType = None,
            onselect: CallbackType = None,
            range_box_color: ColorInputType = (150, 150, 150),
            range_box_color_readonly: ColorInputType = (220, 220, 220),
            range_box_enabled: bool = True,
            range_box_height_factor: NumberType = 0.4,
            range_text_value_color: ColorInputType = (30, 30, 30),
            range_text_value_enabled: bool = True,
            range_text_value_font: Optional[FontType] = None,
            range_text_value_font_height: NumberType = 0.5,
            range_text_value_margin_factor: NumberType = 0.8,
            range_text_value_position: str = POSITION_SOUTH,
            slider_color: ColorInputType = (255, 255, 255),
            slider_color_selected: bool = True,
            slider_height_factor: NumberType = 0.6,
            slider_text_value_bgcolor: ColorInputType = (200, 200, 200),
            slider_text_value_color: ColorInputType = (0, 0, 0),
            slider_text_value_enabled: bool = True,
            slider_text_value_font: Optional[FontType] = None,
            slider_text_value_font_height: NumberType = 0.4,
            slider_text_value_margin_factor: NumberType = 0.2,
            slider_text_value_padding: PaddingType = 2,
            slider_text_value_position: str = POSITION_NORTH,
            slider_thickness: int = 25,
            slider_vmargin: NumberType = 0,
            *args,
            **kwargs
    ) -> None:
        super(RangeSlider, self).__init__(
            args=args,
            kwargs=kwargs,
            onchange=onchange,
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
                'minimum default value ({0}) must be equal or greater than ' \
                'minimum value of the range ({1})' \
                ''.format(default_value[0], range_values[0])
            assert default_value[1] <= range_values[-1], \
                'maximum default value ({0}) must be lower or equal than ' \
                'maximum value of the range ({1})' \
                ''.format(default_value[1], range_values[-1])
        else:
            assert range_values[0] <= default_value <= range_values[-1], \
                'default value ({0}) must be between minimum and maximum of the ' \
                'range values ({1}, {2}), that is, it must satisfy {0}<={1}<={2}' \
                ''.format(default_value, range_values[0], range_values[-1])

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
        range_text_value_color = assert_color(range_text_value_color)
        slider_color = assert_color(slider_color)
        slider_text_value_bgcolor = assert_color(slider_text_value_bgcolor)
        slider_text_value_color = assert_color(slider_text_value_color)

        # Check dimensions and sizes
        assert isinstance(range_box_height_factor, NumberInstance)
        assert 0 < range_box_height_factor, 'height factor must be greater than zero'
        assert isinstance(range_text_value_margin_factor, NumberInstance)
        assert 0 < range_text_value_margin_factor, 'height factor must be greater than zero'
        assert isinstance(slider_text_value_margin_factor, NumberInstance)
        assert 0 < slider_text_value_margin_factor, 'height factor must be greater than zero'
        assert isinstance(slider_height_factor, NumberInstance)
        assert 0 < slider_height_factor, 'height factor must be greater than zero'
        assert isinstance(slider_vmargin, NumberInstance)
        slider_text_value_padding = parse_padding(slider_text_value_padding)
        assert isinstance(slider_thickness, int)
        assert slider_thickness > 0, 'slider thickness must be greater than zero'

        # Check positions
        assert_position(range_text_value_position)
        assert range_text_value_position in (POSITION_NORTH, POSITION_SOUTH), \
            'range text value position must be north or south'
        assert_position(slider_text_value_position)
        assert slider_text_value_position in (POSITION_NORTH, POSITION_SOUTH), \
            'slider text value position must be north or south'

        # Check boolean
        assert isinstance(range_box_enabled, bool)
        assert isinstance(range_text_value_enabled, bool)
        assert isinstance(slider_color_selected, bool)
        assert isinstance(slider_text_value_enabled, bool)

        # Store properties
        self._range_values = range_values
        self._range_width = range_width
        self._default_value = default_value
        self._increment = increment
        self._range_box_color = range_box_color
        self._range_box_color_readonly = range_box_color_readonly
        self._range_box_enabled = range_box_enabled
        self._range_box_height_factor = range_box_height_factor
        self._range_text_value_color = range_text_value_color
        self._range_text_value_enabled = range_text_value_enabled
        self._range_text_value_font = range_text_value_font
        self._range_text_value_font_height = range_text_value_font_height
        self._range_text_value_margin_factor = range_text_value_margin_factor
        self._range_text_value_position = range_text_value_position
        self._slider_color = slider_color
        self._slider_color_selected = slider_color_selected
        self._slider_height_factor = slider_height_factor
        self._slider_text_value_bgcolor = slider_text_value_bgcolor
        self._slider_text_value_color = slider_text_value_color
        self._slider_text_value_enabled = slider_text_value_enabled
        self._slider_text_value_font = slider_text_value_font
        self._slider_text_value_font_height = slider_text_value_font_height
        self._slider_text_value_margin_factor = slider_text_value_margin_factor
        self._slider_text_value_padding = slider_text_value_padding
        self._slider_text_value_position = slider_text_value_position
        self._slider_thickness = slider_thickness
        self._slider_vmargin = slider_vmargin

    def set_value(self, state: int) -> None:
        assert isinstance(state, int), 'state value can only be an integer'
        assert 0 <= state < self._total_states, 'state value exceeds the total states'
        self._state = state

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

    def get_value(self) -> Any:
        return self._state_values[self._state]

    def _apply_font(self) -> None:
        if self._state_text_font is None:
            self._state_text_font = self._font_name
        if self._state_text_font_size is None:
            self._state_text_font_size = self._font_size
        self._state_font = pygame_menu.font.get_font(
            self._state_text_font, self._state_text_font_size
        )

        # Compute the height
        height = self._font_render_string('TEST').get_height()
        self._switch_height = int(height * self._switch_height_factor)
        self._slider_height = int(self._switch_height * self._slider_height_factor) \
                              - 2 * self._switch_border_width

        # Render the state texts
        for t in range(self._total_states):
            f_render = self._state_font.render(
                self._state_text[t], True, self._state_text_font_color[t]
            )
            self._switch_font_rendered.append(f_render)

    def _draw(self, surface: 'pygame.Surface') -> None:
        # Draw title
        surface.blit(self._surface, (self._rect.x, self._rect.y + self._switch_pos[1] - 1))

        # Draw switch
        switch_x = self._rect.x + self._switch_margin[0] + self._switch_pos[0]
        switch_y = self._rect.y + self._switch_margin[1]
        surface.blit(self._switch, (switch_x, switch_y))

        # Draw switch border
        if self._switch_border_width > 0:
            switch_rect = self._switch.get_rect()
            switch_rect.x += switch_x
            switch_rect.y += switch_y
            pygame.draw.rect(
                surface,
                self._switch_border_color,
                switch_rect,
                self._switch_border_width
            )

        # Draw switch font render
        if self._state_text[self._state] != '':
            text = self._switch_font_rendered[self._state]
            surface.blit(text, (
                int(switch_x
                    + (self._switch_width - text.get_width()) * self._state_text_position[0]),
                int(switch_y
                    + (self._switch_height - text.get_height()) * self._state_text_position[1])
            ))

        # Draw slider
        slider_x = switch_x + self._slider_pos[0] + self._switch_border_width
        slider_y = switch_y + self._slider_pos[1] + self._switch_border_width
        surface.blit(self._slider, (slider_x, slider_y))

    def _render(self) -> Optional[bool]:
        if not self._render_hash_changed(
                self._selected, self._title, self._visible, self.readonly,
                self._state):
            return True

        # Create basic title
        self._surface = self._render_string(self._title, self.get_font_color_status())
        self._rect.width, self._rect.height = self._surface.get_size()

        # Create slider
        self._slider = make_surface(self._slider_thickness, self._slider_height,
                                    fill_color=self._slider_color)
        self._slider_pos = (self._state_width_accum[self._state],
                            self._slider_vmargin * self._switch_height)

        # Create the switch surface
        self._switch = make_surface(self._switch_width, self._switch_height,
                                    fill_color=self._state_color[self._state])
        self._switch_pos = (self._rect.width,
                            int((self._switch_height - self._rect.height) / 2))

        # Update maximum rect height
        self._rect.height = max(self._rect.height, self._switch_height,
                                self._slider_height)
        self._rect.width += self._switch_margin[0] + self._switch_width

        # Finals
        self.force_menu_surface_update()

    def update(self, events: EventVectorType) -> bool:
        self.apply_update_callbacks(events)

        if self.readonly or not self.is_visible():
            return False

        for event in events:

            if event.type == pygame.KEYDOWN:  # Check key is valid
                if not check_key_pressed_valid(event):
                    continue

            # Check mouse over
            self._check_mouseover(event)

            # Events
            keydown = self._keyboard_enabled and event.type == pygame.KEYDOWN
            joy_hatmotion = self._joystick_enabled and event.type == pygame.JOYHATMOTION
            joy_axismotion = self._joystick_enabled and event.type == pygame.JOYAXISMOTION

            # Left button
            if keydown and event.key == ctrl.KEY_LEFT or \
                    joy_hatmotion and event.value == ctrl.JOY_LEFT or \
                    joy_axismotion and event.axis == ctrl.JOY_AXIS_X and event.value < ctrl.JOY_DEADZONE:
                self._left()
                return True

            # Right button
            elif keydown and event.key == ctrl.KEY_RIGHT or \
                    joy_hatmotion and event.value == ctrl.JOY_RIGHT or \
                    joy_axismotion and event.axis == ctrl.JOY_AXIS_X and event.value > -ctrl.JOY_DEADZONE:
                self._right()
                return True

            # Press enter
            elif keydown and event.key == ctrl.KEY_APPLY and self._total_states == 2 or \
                    event.type == pygame.JOYBUTTONDOWN and self._joystick_enabled and \
                    event.button == ctrl.JOY_BUTTON_SELECT and self._total_states == 2:
                self._sound.play_key_add()
                self._state = int(not self._state)
                self.change()
                self.active = not self.active
                return True

            # Click on switch; don't consider the mouse wheel (button 4 & 5)
            elif event.type == pygame.MOUSEBUTTONUP and self._mouse_enabled and \
                    event.button in (1, 2, 3) or \
                    event.type == FINGERUP and self._touchscreen_enabled and \
                    self._menu is not None:
                event_pos = get_finger_pos(self._menu, event)

                # If collides
                rect = self.get_rect(to_real_position=True, apply_padding=False)
                if rect.collidepoint(*event_pos):
                    # Check if mouse collides left or right as percentage, use
                    # only X coordinate
                    mouse_x, _ = event_pos
                    topleft, _ = rect.topleft
                    topright, _ = rect.topright
                    # Distance from title
                    dist = mouse_x - (topleft + self._switch_margin[0] + self._switch_pos[0])

                    if dist > 0:  # User clicked the options, not title
                        # Toggle with only 1 click
                        if self._single_click:
                            if self._single_click_dir:
                                self._left()
                            else:
                                self._right()
                            return True

                        else:
                            target_index = 0
                            best = 1e6
                            # Find the closest position
                            for i in range(self._total_states):
                                dx = abs(self._state_width_accum[i] - dist)
                                if dx < best:
                                    target_index = i
                                    best = dx
                            if target_index != self._state:
                                self._sound.play_key_add()
                                self._state = target_index
                                self.change()
                                return True

        return False
