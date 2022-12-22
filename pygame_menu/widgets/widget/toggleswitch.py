"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TOGGLE SWITCH
Switch between several states.
"""

__all__ = [
    'ToggleSwitch',
    'ToggleSwitchManager'
]

import pygame
import pygame_menu

from abc import ABC
from pygame_menu.font import FontType, assert_font
from pygame_menu.locals import FINGERUP
from pygame_menu.utils import check_key_pressed_valid, assert_color, assert_vector, \
    make_surface, get_finger_pos
from pygame_menu.widgets.core.widget import Widget, WidgetTransformationNotImplemented, \
    AbstractWidgetManager

from pygame_menu._types import Any, CallbackType, Union, List, Tuple, Optional, \
    ColorType, NumberType, Tuple2NumberType, Tuple2IntType, NumberInstance, \
    ColorInputType, EventVectorType, Callable


# noinspection PyMissingOrEmptyDocstring
class ToggleSwitch(Widget):
    """
    Toggle switch widget.

    If the state of the widget changes the ``onchange`` callback is called. The
    state can change by pressing LEFT/RIGHT or RETURN if the widget only has two
    states. This widget can handle more than 2 states.

    .. code-block:: python

        onchange(state_value, **kwargs)

    .. note::

        ToggleSwitch only accepts translation transformation.

    :param title: Toggle switch title
    :param toggleswitch_id: ToggleSwitch ID
    :param default_state: Default state index of the switch
    :param infinite: The state can rotate
    :param onchange: Callback when changing the state of the switch
    :param onselect: Function when selecting the widget
    :param single_click: Changes the state of the switch with 1 click instead of finding the closest position (events). If ``True`` the parameter ``infinite`` will also be ``True``
    :param single_click_dir: Direction of the change if only 1 click is pressed. ``True`` for left direction, ``False`` for right
    :param slider_color: Slider color
    :param slider_height_factor: Height of the slider (factor of the switch height)
    :param slider_thickness: Slider thickness in px
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
    :param switch_border_width: Border width of the switch in px
    :param switch_height: Height factor respect to the title font size height
    :param switch_margin: Switch margin on x-axis and y-axis (x, y) respect to the title of the widget in px
    :param args: Optional arguments for callbacks
    :param kwargs: Optional keyword arguments
    """
    _infinite: bool
    _single_click: bool
    _single_click_dir: bool
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
    _state_text_font: Optional[FontType]
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
    _switch_margin: Tuple2IntType
    _switch_pos: Tuple2IntType
    _switch_width: int
    _total_states: int

    def __init__(
            self,
            title: Any,
            toggleswitch_id: str = '',
            default_state: int = 0,
            infinite: bool = False,
            onchange: CallbackType = None,
            onselect: CallbackType = None,
            single_click: bool = False,
            single_click_dir: bool = True,
            slider_color: ColorInputType = (255, 255, 255),
            slider_height_factor: NumberType = 1,
            slider_thickness: int = 25,
            slider_vmargin: NumberType = 0,
            state_color: Tuple[ColorInputType, ...] = ((178, 178, 178), (117, 185, 54)),
            state_text: Tuple[str, ...] = ('Off', 'On'),
            state_text_font: Optional[FontType] = None,
            state_text_font_color: Tuple[ColorInputType, ...] = ((255, 255, 255), (255, 255, 255)),
            state_text_font_size: Optional[int] = None,
            state_text_position: Tuple2NumberType = (0.5, 0.5),
            state_values: Tuple[Any, ...] = (False, True),
            state_width: Union[Tuple[int, ...], int] = 150,
            switch_border_color: ColorInputType = (40, 40, 40),
            switch_border_width: int = 1,
            switch_height: NumberType = 1.25,
            switch_margin: Tuple2IntType = (25, 0),
            *args,
            **kwargs
    ) -> None:
        super(ToggleSwitch, self).__init__(
            args=args,
            kwargs=kwargs,
            onchange=onchange,
            onselect=onselect,
            title=title,
            widget_id=toggleswitch_id
        )

        # Asserts
        assert isinstance(default_state, int)
        assert isinstance(infinite, bool)
        assert isinstance(single_click, bool)
        assert isinstance(single_click_dir, bool)
        assert isinstance(state_values, tuple)

        # Check the number of states
        self._total_states = len(state_values)
        assert 2 <= self._total_states, 'the minimum number of states is 2'
        assert 0 <= default_state < self._total_states, 'invalid default state value'

        # Check fonts
        if state_text_font is not None:
            assert_font(state_text_font)
        assert isinstance(state_text_font_size, (int, type(None)))
        if state_text_font_size is not None:
            assert state_text_font_size > 0, \
                'state text font size must be equal or greater than zero'

        # Check colors
        assert_vector(state_text_position, 2)
        switch_border_color = assert_color(switch_border_color)
        assert isinstance(switch_border_width, int) and switch_border_width >= 0, \
            'border width must be equal or greater than zero'
        slider_color = assert_color(slider_color)

        # Check dimensions and sizes
        assert slider_height_factor > 0, 'slider height factor cannot be negative'
        assert slider_thickness >= 0, 'slider thickness cannot be negative'
        assert isinstance(slider_vmargin, NumberInstance)
        assert_vector(switch_margin, 2, int)
        assert isinstance(switch_height, NumberInstance) and switch_height > 0, \
            'switch height factor cannot be zero or negative'
        assert isinstance(state_color, tuple) and len(state_color) == self._total_states

        # Create state color
        new_state_color = []
        for c in state_color:
            new_state_color.append(assert_color(c))
        state_color = tuple(new_state_color)

        # Create state texts
        assert isinstance(state_text, tuple) and len(state_text) == self._total_states
        for c in state_text:
            assert isinstance(c, str), 'all states text must be string-type'
        assert isinstance(state_text_font_color, tuple) and \
               len(state_text_font_color) == self._total_states

        new_state_text_font_color = []
        for c in state_text_font_color:
            new_state_text_font_color.append(assert_color(c))
        state_text_font_color = tuple(new_state_text_font_color)

        # Crete state widths
        self._switch_width = 0
        if isinstance(state_width, NumberInstance):
            state_width = [state_width]
        assert_vector(state_width, self._total_states - 1, int)

        for i in range(len(state_width)):
            assert isinstance(state_width[i], int), 'each state width must be an integer'
            assert state_width[i] > 0, 'each state width must be greater than zero'
            self._switch_width += state_width[i]

        # Finals
        if single_click:
            infinite = True

        # Store properties
        self._default_value = default_state
        self._switch_border_color = switch_border_color
        self._switch_border_width = switch_border_width
        self._infinite = infinite
        self._single_click = single_click
        self._single_click_dir = single_click_dir
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
            accum_width = accum - self._slider_thickness - 2 * self._switch_border_width
            self._state_width_accum.append(accum_width)

        # Inner properties
        self._accept_events = True
        self._slider_height = 0
        self._slider_pos = (0, 0)  # to add to (rect.x, rect.y)
        self._state_font = None
        self._switch_font_rendered = []  # Stores font render for each state
        self._switch_height = 0
        self._switch_pos = (0, 0)  # horizontal pos, and delta to title

    def set_value(self, state: int) -> None:
        assert isinstance(state, int), 'state value can only be an integer'
        assert 0 <= state < self._total_states, 'state value exceeds the total states'
        self._state = state
        self._render()

    def scale(self, *args, **kwargs) -> 'ToggleSwitch':
        raise WidgetTransformationNotImplemented()

    def resize(self, *args, **kwargs) -> 'ToggleSwitch':
        raise WidgetTransformationNotImplemented()

    def set_max_width(self, *args, **kwargs) -> 'ToggleSwitch':
        raise WidgetTransformationNotImplemented()

    def set_max_height(self, *args, **kwargs) -> 'ToggleSwitch':
        raise WidgetTransformationNotImplemented()

    def rotate(self, *args, **kwargs) -> 'ToggleSwitch':
        raise WidgetTransformationNotImplemented()

    def flip(self, *args, **kwargs) -> 'ToggleSwitch':
        raise WidgetTransformationNotImplemented()

    def get_value(self) -> Any:
        return self._state_values[self._state]

    def _apply_font(self) -> None:
        self._state_font = pygame_menu.font.get_font(
            self._font_name if self._state_text_font is None else self._state_text_font,
            self._font_size if self._state_text_font_size is None else self._state_text_font_size
        )

        # Compute the height
        height = self._font_render_string('TEST').get_height()
        self._switch_height = int(height * self._switch_height_factor)
        self._slider_height = int(self._switch_height * self._slider_height_factor) - 2 * self._switch_border_width

        # Render the state texts
        self._switch_font_rendered = []
        for t in range(self._total_states):
            f_render = self._state_font.render(self._state_text[t], True, self._state_text_font_color[t])
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
                int(switch_x + (self._switch_width - text.get_width()) * self._state_text_position[0]),
                int(switch_y + (self._switch_height - text.get_height()) * self._state_text_position[1])
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
        self._slider = make_surface(self._slider_thickness, self._slider_height, fill_color=self._slider_color)
        self._slider_pos = (self._state_width_accum[self._state],
                            self._slider_vmargin * self._switch_height)

        # Create the switch surface
        self._switch = make_surface(self._switch_width, self._switch_height, fill_color=self._state_color[self._state])
        self._switch_pos = (self._rect.width, int((self._switch_height - self._rect.height) / 2))

        # Update maximum rect height
        self._rect.height = max(self._rect.height, self._switch_height, self._slider_height)
        self._rect.width += self._switch_margin[0] + self._switch_width

        # Finals
        self.force_menu_surface_update()

    def _left(self) -> None:
        """
        State left.
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
            self._sound.play_key_add()

    def _right(self) -> None:
        """
        State right.
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
            self._sound.play_key_add()

    def update(self, events: EventVectorType) -> bool:
        self.apply_update_callbacks(events)

        if self.readonly or not self.is_visible():
            self._readonly_check_mouseover(events)
            return False

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

            # Left button
            if keydown and self._ctrl.left(event, self) or \
                    joy_hatmotion and self._ctrl.joy_left(event, self) or \
                    joy_axismotion and self._ctrl.joy_axis_x_left(event, self):
                self._left()
                return True

            # Right button
            elif keydown and self._ctrl.right(event, self) or \
                    joy_hatmotion and self._ctrl.joy_right(event, self) or \
                    joy_axismotion and self._ctrl.joy_axis_x_right(event, self):
                self._right()
                return True

            # Press enter
            elif keydown and self._ctrl.apply(event, self) and self._total_states == 2 or \
                    event.type == pygame.JOYBUTTONDOWN and self._joystick_enabled and \
                    self._ctrl.joy_select(event, self) and self._total_states == 2:
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


class ToggleSwitchManager(AbstractWidgetManager, ABC):
    """
    ToggleSwitch manager.
    """

    def toggle_switch(
            self,
            title: Any,
            default: Union[int, bool] = 0,
            onchange: CallbackType = None,
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            toggleswitch_id: str = '',
            single_click: bool = True,
            state_text: Tuple[str, ...] = ('Off', 'On'),
            state_values: Tuple[Any, ...] = (False, True),
            width: int = 150,
            **kwargs
    ) -> 'pygame_menu.widgets.ToggleSwitch':
        """
        Add a toggle switch to the Menu: It can switch between two states.

        If user changes the status of the callback, ``onchange`` is fired:

        .. code-block:: python

            onchange(current_state_value, **kwargs)

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
            - ``float``                         (bool) - If ``True`` the widget don't contribute width/height to the Menu widget positioning computation, and don't add one unit to the rows
            - ``float_origin_position``         (bool) - If ``True`` the widget position is set to the top-left position of the Menu if the widget is floating
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``infinite``                      (bool) – The state can rotate. ``False`` by default
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``readonly_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode
            - ``readonly_selected_color``       (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode and is selected
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect
            - ``shadow_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget shadow
            - ``shadow_radius``                 (int) - Border radius of the shadow
            - ``shadow_type``                   (str) - Shadow type, it can be ``'rectangular'`` or ``'ellipse'``
            - ``shadow_width``                  (int) - Width of the shadow. If ``0`` the shadow is disabled
            - ``single_click_dir``              (bool) - Direction of the change if only 1 click is pressed. ``True`` for left direction (default), ``False`` for right
            - ``slider_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the slider
            - ``slider_height_factor``          (int, float) - Height of the slider (factor of the switch height). ``1`` by default
            - ``slider_thickness``              (int) – Slider thickness in px. ``20`` px by default
            - ``slider_vmargin``                (int, float) - Vertical margin of the slider (factor of the switch height). ``0`` by default
            - ``state_color``                   (tuple) – 2-item color tuple for each state
            - ``state_text_font``               (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`, None) - Font of the state text. If ``None`` uses the widget font. ``None`` by default
            - ``state_text_font_color``         (tuple) – 2-item color tuple for each font state text color
            - ``state_text_font_size``          (str, None) – Font size of the state text. If ``None`` uses the widget font size
            - ``state_text_position``           (tuple) - Position of the state text respect to the switch rect. ``(0.5, 0.5)`` by default
            - ``switch_border_color``           (tuple, list, str, int, :py:class:`pygame.Color`) – Switch border color
            - ``switch_border_width``           (int) – Switch border width
            - ``switch_height``                 (int, float) – Height factor respect to the title font size height
            - ``switch_margin``                 (tuple, list) – Switch on x-axis and y-axis (x, y) margin respect to the title of the widget in px
            - ``tab_size``                      (int) – Width of a tab character

        .. note::

            This method only handles two states. If you need more states (for example
            3, or 4), prefer using :py:class:`pygame_menu.widgets.ToggleSwitch`
            and add it as a generic widget.

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

        :param title: Title of the toggle switch
        :param default: Default state index of the switch; it can be ``0 (False)`` or ``1 (True)``
        :param onchange: Callback executed when changing the state of the toggle switch
        :param onselect: Callback executed when selecting the widget
        :param toggleswitch_id: Widget ID
        :param single_click: Changes the state of the switch with 1 click instead of finding the closest position
        :param state_text: Text of each state
        :param state_values: Value of each state of the switch
        :param width: Width of the switch box in px
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.ToggleSwitch`
        """
        if isinstance(default, (int, bool)):
            assert 0 <= default <= 1, 'default value can be 0 or 1'
        else:
            raise ValueError(
                f'invalid value type, default can be 0, False, 1, or True, but'
                f'received "{default}"'
            )

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        infinite = kwargs.pop('infinite', False)
        slider_color = kwargs.pop('slider_color', self._theme.widget_box_background_color)
        slider_thickness = kwargs.pop('slider_thickness', self._theme.scrollbar_thick)
        state_color = kwargs.pop('state_color', ((178, 178, 178), (117, 185, 54)))
        state_text_font_color = kwargs.pop('state_text_font_color', (self._theme.widget_box_background_color, self._theme.widget_box_background_color))
        state_text_font_size = kwargs.pop('state_text_font_size', None)
        switch_border_color = kwargs.pop('switch_border_color', self._theme.widget_box_border_color)
        switch_border_width = kwargs.pop('switch_border_width', self._theme.widget_box_border_width)
        switch_height = kwargs.pop('switch_height', 1)
        switch_margin = kwargs.pop('switch_margin', self._theme.widget_box_margin)

        widget = ToggleSwitch(
            default_state=default,
            infinite=infinite,
            onchange=onchange,
            onselect=onselect,
            single_click=single_click,
            single_click_dir=kwargs.pop('single_click_dir', True),
            slider_color=slider_color,
            slider_thickness=slider_thickness,
            state_color=state_color,
            state_text=state_text,
            state_text_font_color=state_text_font_color,
            state_text_font_size=state_text_font_size,
            state_values=state_values,
            switch_border_color=switch_border_color,
            switch_border_width=switch_border_width,
            switch_height=switch_height,
            switch_margin=switch_margin,
            title=title,
            state_width=int(width),
            toggleswitch_id=toggleswitch_id,
            **kwargs
        )
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget
