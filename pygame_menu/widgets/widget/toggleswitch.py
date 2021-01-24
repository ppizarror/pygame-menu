"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TOGGLE SWITCH
Switch between several states.

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

__all__ = ['ToggleSwitch']

import pygame
from pygame_menu.widgets.core import Widget
import pygame_menu.controls as _controls
import pygame_menu.font as _fonts
from pygame_menu._types import Any, CallbackType, Union, List, Tuple, Optional, ColorType, NumberType, \
    Tuple2NumberType, Tuple2IntType
from pygame_menu.utils import check_key_pressed_valid, assert_color, assert_vector, make_surface


# noinspection PyMissingOrEmptyDocstring
class ToggleSwitch(Widget):
    """
    Toggle switch widget.

    If the state of the widget changes the ``onchange`` callback is called. The state can
    change pressing LEFT/RIGHT or RETURN if the widget only has two states. This class can
    handle more than 2 states.

    .. code-block:: python

        onchange(state_value, **kwargs)

    .. note::

        This widget only accepts translation transformation.

    :param title: Toggle switch title
    :param toggleswitch_id: ToggleSwitch ID
    :param default_state: Default state index of the switch
    :param infinite: The state can rotate
    :param onchange: Callback when changing the state of the switch
    :param slider_color: Slider color
    :param slider_height_factor: Height of the slider (factor of the switch height)
    :param slider_thickness: Slider thickness (px)
    :param slider_vmargin: Vertical margin of the slider (factor of the switch height)
    :param state_color: Background color of each state, it modifies the whole width of the switch
    :param state_text: Text of each state of the switch
    :param state_text_font: Font of the state text. If ``None`` uses the widget font
    :param state_text_font_color: Color of the font of each state text
    :param state_text_font_size: Font size of the state text. If ``None`` uses the widget font size
    :param state_text_position: Position of the state text respect to the switch rect
    :param state_values: Value of each state of the switch
    :param state_width: Width of each state. For example if there's 2 states, ``state_width`` only can have 1 value
    :param switch_border_color: Border color of the switch
    :param switch_border_width: Border width of the switch (px)
    :param switch_height: Height factor respect to the title font size height
    :param switch_margin: *(x, y)* margin respect to the title of the widget. X is in px, Y is relative to the height of the title
    :param args: Optional arguments for callbacks
    :param kwargs: Optional keyword arguments
    """
    _infinite: bool
    _slider: Optional['pygame.Surface']
    _slider_color: ColorType
    _slider_height: int
    _slider_height_factor: float
    _slider_pos: Tuple2IntType
    _slider_thickness: int
    _slider_vmargin: int
    _state: int
    _state_color: Tuple[ColorType, ...]
    _state_font: Optional['pygame.font.Font']
    _state_text: Tuple[str, ...]
    _state_text_font: Optional[str]
    _state_text_font_color: Tuple[ColorType, ...]
    _state_text_font_size: Optional[int]
    _state_text_position: Tuple2NumberType
    _state_values: Tuple[Any, ...]
    _state_width: List[int]
    _switch: Optional['pygame.Surface']
    _switch_border_color: ColorType
    _switch_border_width: int
    _switch_font_rendered: List['pygame.Surface']
    _switch_height: int
    _switch_height_factor: float
    _switch_margin: Tuple2NumberType
    _switch_pos: Tuple2IntType
    _switch_width: int
    _total_states: int

    def __init__(self,
                 title: Any,
                 toggleswitch_id: str = '',
                 default_state: int = 0,
                 infinite: bool = False,
                 onchange: CallbackType = None,
                 slider_color: ColorType = (255, 255, 255),
                 slider_height_factor: NumberType = 1,
                 slider_thickness: int = 25,
                 slider_vmargin: NumberType = 0,
                 state_color: Tuple[ColorType, ...] = ((178, 178, 178), (117, 185, 54)),
                 state_text: Tuple[str, ...] = ('Off', 'On'),
                 state_text_font: Optional[str] = None,
                 state_text_font_color: Tuple[ColorType, ...] = ((255, 255, 255), (255, 255, 255)),
                 state_text_font_size: Optional[int] = None,
                 state_text_position: Tuple2NumberType = (0.5, 0.5),
                 state_values: Tuple[Any, ...] = (False, True),
                 state_width: Union[Tuple[int, ...], int] = 150,
                 switch_border_color: ColorType = (40, 40, 40),
                 switch_border_width: int = 1,
                 switch_height: NumberType = 1.25,
                 switch_margin: Tuple2NumberType = (25, 0),
                 *args,
                 **kwargs
                 ) -> None:
        super(ToggleSwitch, self).__init__(
            args=args,
            kwargs=kwargs,
            onchange=onchange,
            title=title,
            widget_id=toggleswitch_id
        )

        # Asserts
        assert isinstance(default_state, int)
        assert isinstance(state_values, tuple)
        assert isinstance(infinite, bool)
        self._total_states = len(state_values)
        assert 2 <= self._total_states, 'the minimum number of states is 2'
        assert 0 <= default_state < self._total_states, 'invalid default state value'
        assert isinstance(state_text_font, (str, type(None)))
        assert isinstance(state_text_font_size, (int, type(None)))
        if state_text_font_size is not None:
            assert state_text_font_size > 0, 'state text font size must be equal or greater than zero'
        assert_vector(state_text_position, 2)
        assert_color(switch_border_color)
        assert isinstance(switch_border_width, int) and switch_border_width >= 0, \
            'border width must be equal or greater than zero'
        assert_color(slider_color)
        assert slider_height_factor > 0, 'slider height factor cannot be negative'
        assert slider_thickness >= 0, 'slider thickness cannot be negative'
        assert isinstance(slider_vmargin, (int, float))
        assert_vector(switch_margin, 2)
        assert isinstance(switch_height, (int, float)) and switch_height > 0, \
            'switch height factor cannot be zero or negative'

        assert isinstance(state_color, tuple) and len(state_color) == self._total_states
        for c in state_color:
            assert_color(c)
        assert isinstance(state_text, tuple) and len(state_text) == self._total_states
        for c in state_text:
            assert isinstance(c, str), 'all states text must be string-type'
        assert isinstance(state_text_font_color, tuple) and len(state_text_font_color) == self._total_states
        for c in state_text_font_color:
            assert_color(c)
        self._switch_width = 0
        if isinstance(state_width, (int, float)):
            state_width = [state_width]
        assert_vector(state_width, self._total_states - 1)
        for i in range(len(state_width)):
            assert isinstance(state_width[i], int), 'each state width must be an integer'
            assert state_width[i] > 0, 'each state width must be greater than zero'
            self._switch_width += state_width[i]

        # Store properties
        self._switch_border_color = switch_border_color
        self._switch_border_width = switch_border_width
        self._infinite = infinite
        self._slider_color = slider_color
        self._slider_height_factor = slider_height_factor
        self._slider_thickness = slider_thickness
        self._slider_vmargin = slider_vmargin
        self._state = default_state
        self._state_color = state_color
        self._state_text = state_text
        self._state_text_font = state_text_font
        self._state_text_font_color = state_text_font_color
        self._state_text_font_size = state_text_font_size
        self._state_text_position = state_text_position
        self._state_values = state_values
        self._state_width = state_width
        self._switch_height_factor = float(switch_height)
        self._switch_margin = switch_margin

        # Compute state width accum
        self._state_width_accum = [0]
        accum = 0
        for w in self._state_width:
            accum += w
            self._state_width_accum.append(accum - self._slider_thickness - 2 * self._switch_border_width)

        # Inner properties
        self._slider_height = 0
        self._slider_pos = (0, 0)  # to add to (rect.x, rect.y)
        self._state_font = None
        self._switch_font_rendered = []  # Stores font render for each state
        self._switch_height = 0
        self._switch_pos = (0, 0)  # horizontal pos, and delta to title

    def set_value(self, value: int) -> None:
        assert isinstance(value, int), 'value can only be an integer'
        assert 0 <= value < self._total_states, 'state value exceeds the total states'
        self._state = value

    def scale(self, width: NumberType, height: NumberType, smooth: bool = False) -> 'Widget':
        return self

    def resize(self, width: NumberType, height: NumberType, smooth: bool = False) -> 'Widget':
        return self

    def set_max_width(self, width: Optional[NumberType], scale_height: NumberType = False,
                      smooth: bool = True) -> 'Widget':
        return self

    def set_max_height(self, height: Optional[NumberType], scale_width: NumberType = False,
                       smooth: bool = True) -> 'Widget':
        return self

    def rotate(self, angle: NumberType) -> 'Widget':
        return self

    def flip(self, x: bool, y: bool) -> 'Widget':
        return self

    def get_value(self) -> Any:
        return self._state_values[self._state]

    def _apply_font(self) -> None:
        if self._state_text_font is None:
            self._state_text_font = self._font_name
        if self._state_text_font_size is None:
            self._state_text_font_size = self._font_size
        self._state_font = _fonts.get_font(self._state_text_font, self._state_text_font_size)

        # Compute the height
        height = self._font_render_string('TEST').get_height()
        self._switch_height = int(height * self._switch_height_factor)
        self._slider_height = int(self._switch_height * self._slider_height_factor) - 2 * self._switch_border_width

        # Render the state texts
        for t in range(self._total_states):
            f_render = self._state_font.render(self._state_text[t], True, self._state_text_font_color[t])
            self._switch_font_rendered.append(f_render)

    def _draw(self, surface: 'pygame.Surface') -> None:
        # Draw title
        surface.blit(self._surface, (self._rect.x, self._rect.y + self._switch_pos[1]))

        # Draw switch
        switchx = self._rect.x + self._switch_margin[0] + self._switch_pos[0]
        switchy = self._rect.y + self._switch_margin[1] * self._switch.get_height()
        surface.blit(self._switch, (switchx, switchy))

        # Draw switch border
        if self._switch_border_width > 0:
            switch_rect = self._switch.get_rect()
            switch_rect.x += switchx
            switch_rect.y += switchy
            pygame.draw.rect(
                surface,
                self._switch_border_color,
                switch_rect,
                self._switch_border_width
            )

        # Draw switch font render
        if self._state_text[self._state] != '':
            text = self._switch_font_rendered[self._state]
            stextx = switchx + (self._switch_width - text.get_width()) * self._state_text_position[0]
            stexty = switchy + (self._switch_height - text.get_height()) * self._state_text_position[1]
            surface.blit(text, (stextx, stexty))

        # Draw slider
        sliderx = switchx + self._slider_pos[0] + self._switch_border_width
        slidery = switchy + self._slider_pos[1] + self._switch_border_width
        surface.blit(self._slider, (sliderx, slidery))

    def _render(self) -> Optional[bool]:
        if not self._render_hash_changed(self._selected, self._title, self._visible, self.readonly,
                                         self._state):
            return True

        # Create basic title
        self._surface = self._render_string(self._title, self.get_font_color_status())
        self._rect.width, self._rect.height = self._surface.get_size()

        # Create slider
        self._slider = make_surface(self._slider_thickness, self._slider_height,
                                    fill_color=self._slider_color)
        self._slider_pos = (self._state_width_accum[self._state], self._slider_vmargin * self._switch_height)

        # Create the switch surface
        self._switch = make_surface(self._switch_width, self._switch_height,
                                    fill_color=self._state_color[self._state])
        self._switch_pos = (self._rect.width, int((self._switch_height - self._rect.height) / 2))

        # Update maximum rect height
        self._rect.height = max(self._rect.height, self._switch_height, self._slider_height)
        self._rect.width += self._switch_margin[0] + self._switch_width

        # Finals
        self.force_menu_surface_update()

    def _left(self) -> None:
        """
        State left.

        :return: None
        """
        if self.readonly:
            return
        previous = self._state
        if self._infinite:
            self._state = (self._state - 1) % self._total_states
        else:
            self._state = max(0, self._state - 1)
        if previous != self._state:
            self.change()

    def _right(self) -> None:
        """
        State right.

        :return: None
        """
        if self.readonly:
            return
        previous = self._state
        if self._infinite:
            self._state = (self._state + 1) % self._total_states
        else:
            self._state = min(self._state + 1, self._total_states - 1)
        if previous != self._state:
            self.change()

    def update(self, events: Union[List['pygame.event.Event'], Tuple['pygame.event.Event']]) -> bool:
        if self.readonly:
            return False
        updated = False

        for event in events:

            if event.type == pygame.KEYDOWN:  # Check key is valid
                if not check_key_pressed_valid(event):
                    continue

            # Events
            keydown = event.type == pygame.KEYDOWN
            joy_hatmotion = self._joystick_enabled and event.type == pygame.JOYHATMOTION
            joy_axismotion = self._joystick_enabled and event.type == pygame.JOYAXISMOTION

            # Left button
            if keydown and event.key == _controls.KEY_LEFT or \
                    joy_hatmotion and event.value == _controls.JOY_LEFT or \
                    joy_axismotion and event.axis == _controls.JOY_AXIS_X and event.value < _controls.JOY_DEADZONE:
                self._sound.play_key_add()
                self._left()
                updated = True

            # Right button
            elif keydown and event.key == _controls.KEY_RIGHT or \
                    joy_hatmotion and event.value == _controls.JOY_RIGHT or \
                    joy_axismotion and event.axis == _controls.JOY_AXIS_X and event.value > -_controls.JOY_DEADZONE:
                self._sound.play_key_add()
                self._right()
                updated = True

            # Press enter
            elif keydown and event.key == _controls.KEY_APPLY and self._total_states == 2:
                self._sound.play_key_add()
                self._state = int(not self._state)
                self.change()
                updated = True
                self.active = not self.active

            # Click on switch
            elif self._mouse_enabled and event.type == pygame.MOUSEBUTTONUP or \
                    self._touchscreen_enabled and event.type == pygame.FINGERUP:

                # Get event position based on input type
                if self._touchscreen_enabled and event.type == pygame.FINGERUP:
                    window_size = self.get_menu().get_window_size()
                    event_pos = (event.x * window_size[0], event.y * window_size[1])
                else:
                    event_pos = event.pos

                # If collides
                rect = self.get_rect()
                if rect.collidepoint(*event_pos):
                    # Check if mouse collides left or right as percentage, use only X coordinate
                    mousex, _ = event.pos
                    topleft, _ = rect.topleft
                    topright, _ = rect.topright
                    dist = mousex - (topleft + self._switch_margin[0] + self._switch_pos[0])  # Distance from title
                    if dist > 0:  # User clicked the options, not title
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

        if updated:
            self.apply_update_callbacks()

        return updated
