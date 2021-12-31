"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SCROLLBAR
ScrollBar class, manage the selection in a range of values.
"""

__all__ = ['ScrollBar']

import pygame

from pygame_menu.locals import ORIENTATION_VERTICAL, ORIENTATION_HORIZONTAL, \
    POSITION_NORTHWEST, FINGERMOTION, FINGERUP, FINGERDOWN
from pygame_menu.utils import make_surface, assert_orientation, \
    mouse_motion_current_mouse_position, assert_color, get_finger_pos
from pygame_menu.widgets.core.widget import Widget, WidgetTransformationNotImplemented

from pygame_menu._types import Optional, List, VectorIntType, ColorType, Literal, \
    Tuple2IntType, CallbackType, NumberInstance, ColorInputType, NumberType, \
    EventVectorType, VectorInstance


# noinspection PyMissingOrEmptyDocstring
class ScrollBar(Widget):
    """
    A scroll bar include 3 separate controls: a slider, scroll arrows, and a
    page control:

        a. The slider provides a way to quickly go to any part of the document.
        b. The scroll arrows are push buttons which can be used to accurately
           navigate to a particular place in a document.
        c. The page control is the area over which the slider is dragged (the
           scroll bar's background). Clicking here moves the scroll bar towards
           the click by one page.

    .. note::

        ScrollBar only accepts translation transformation.

    :param length: Length of the page control
    :param values_range: Min and max values
    :param scrollbar_id: Bar identifier
    :param orientation: Bar orientation (horizontal or vertical). See :py:mod:`pygame_menu.locals`
    :param slider_pad: Space between slider and page control (px)
    :param slider_color: Color of the slider
    :param page_ctrl_thick: Page control thickness
    :param page_ctrl_color: Page control color
    :param onchange: Callback when pressing and moving the scroll
    """
    _clicked: bool
    _last_mouse_pos: Tuple2IntType
    _orientation: Literal[0, 1]
    _page_ctrl_color: ColorType
    _page_ctrl_length: NumberType
    _page_ctrl_thick: int
    _page_step: NumberType
    _shadow_color: ColorType
    _shadow_enabled: bool
    _shadow_offset: NumberType
    _shadow_position: str
    _shadow_tuple: Tuple2IntType
    _single_step: NumberType
    _slider_color: ColorType
    _slider_hover_color: ColorType
    _slider_pad: int
    _slider_position: int
    _slider_rect: Optional['pygame.Rect']
    _values_range: List[NumberType]
    scrolling: bool

    def __init__(
            self,
            length: NumberType,
            values_range: VectorIntType,
            scrollbar_id: str = '',
            orientation: str = ORIENTATION_HORIZONTAL,
            slider_pad: NumberType = 0,
            slider_color: ColorInputType = (200, 200, 200),
            slider_hover_color: ColorInputType = (180, 180, 180),
            page_ctrl_thick: int = 20,
            page_ctrl_color: ColorInputType = (235, 235, 235),
            onchange: CallbackType = None,
            *args,
            **kwargs
    ) -> None:
        assert isinstance(length, NumberInstance)
        assert isinstance(values_range, VectorInstance)
        assert values_range[1] > values_range[0], 'minimum value first is expected'
        assert isinstance(slider_pad, NumberInstance)
        assert isinstance(page_ctrl_thick, int)
        assert page_ctrl_thick - 2 * slider_pad >= 2, 'slider shall be visible'

        page_ctrl_color = assert_color(page_ctrl_color)
        slider_color = assert_color(slider_color)
        slider_hover_color = assert_color(slider_hover_color)

        super(ScrollBar, self).__init__(
            widget_id=scrollbar_id,
            onchange=onchange,
            args=args,
            kwargs=kwargs
        )

        self._check_mouseleave_call_render = True
        self._clicked = False
        self._last_mouse_pos = (-1, -1)
        self._mouseover_check_rect = lambda: self.get_slider_rect()
        self._orientation = 0  # 0: horizontal, 1: vertical
        self._values_range = list(values_range)

        # Page control
        self._page_ctrl_color = page_ctrl_color
        self._page_ctrl_length = length
        self._page_ctrl_thick = page_ctrl_thick

        # Slider
        self._default_value = 0
        self._slider_color = slider_color
        self._slider_hover_color = slider_hover_color
        self._slider_pad = slider_pad
        self._slider_position = 0
        self._slider_rect = None

        # Shadow
        self._shadow_color = (0, 0, 0)
        self._shadow_enabled = False
        self._shadow_offset = 2.0
        self._shadow_position = POSITION_NORTHWEST
        self._shadow_tuple = (0, 0)  # (x px offset, y px offset)

        # Page step
        self._page_step = 0
        self._single_step = 20

        if values_range[1] - values_range[0] > length:
            self.set_page_step(length)
        else:
            self.set_page_step((values_range[1] - values_range[0]) / 5.0)  # Arbitrary

        self.set_orientation(orientation)

        # Configure public's
        self.is_scrollable = True
        self.is_selectable = False
        self.scrolling = False

    def scroll_to_widget(self, *args, **kwargs) -> 'ScrollBar':
        pass

    def _apply_font(self) -> None:
        pass

    def set_padding(self, *args, **kwargs) -> 'ScrollBar':
        return self

    def scale(self, *args, **kwargs) -> 'ScrollBar':
        raise WidgetTransformationNotImplemented()

    def resize(self, *args, **kwargs) -> 'ScrollBar':
        raise WidgetTransformationNotImplemented()

    def set_max_width(self, *args, **kwargs) -> 'ScrollBar':
        raise WidgetTransformationNotImplemented()

    def set_max_height(self, *args, **kwargs) -> 'ScrollBar':
        raise WidgetTransformationNotImplemented()

    def rotate(self, *args, **kwargs) -> 'ScrollBar':
        raise WidgetTransformationNotImplemented()

    def flip(self, *args, **kwargs) -> 'ScrollBar':
        raise WidgetTransformationNotImplemented()

    def _apply_size_changes(self) -> None:
        """
        Apply scrollbar changes.

        :return: None
        """
        opp_orientation = 1 if self._orientation == 0 else 0  # Opposite of orientation
        dims = ('width', 'height')
        setattr(self._rect, dims[self._orientation], int(self._page_ctrl_length))
        setattr(self._rect, dims[opp_orientation], self._page_ctrl_thick)
        self._slider_rect = pygame.Rect(0, 0, int(self._rect.width), int(self._rect.height))
        setattr(self._slider_rect, dims[self._orientation], int(self._page_step))
        setattr(self._slider_rect, dims[opp_orientation], self._page_ctrl_thick)

        # Update slider position according to the current one
        pos = ('x', 'y')
        setattr(self._slider_rect, pos[self._orientation], int(self._slider_position))
        self._slider_rect = self._slider_rect.inflate(-2 * self._slider_pad,
                                                      -2 * self._slider_pad)

    def set_shadow(
            self,
            enabled: bool = True,
            color: Optional[ColorInputType] = None,
            position: Optional[str] = None,
            offset: int = 2
    ) -> 'ScrollBar':
        """
        Set the scrollbars shadow.

        .. note::

            See :py:mod:`pygame_menu.locals` for valid ``position`` values.

        :param enabled: Shadow is enabled or not
        :param color: Shadow color
        :param position: Shadow position
        :param offset: Shadow offset
        :return: Self reference
        """
        super(ScrollBar, self).set_font_shadow(enabled, color, position, offset)

        # Store shadow from font
        self._shadow_color = self._font_shadow_color
        self._shadow_enabled = self._font_shadow
        self._shadow_offset = self._font_shadow_offset
        self._shadow_position = self._font_shadow_position
        self._shadow_tuple = self._font_shadow_tuple

        # Disable font
        self._font_shadow = False
        return self

    def _draw(self, surface: 'pygame.Surface') -> None:
        surface.blit(self._surface, self._rect.topleft)

    def get_minimum(self) -> int:
        """
        Return the smallest acceptable value.

        :return: Smallest acceptable value
        """
        return int(self._values_range[0])

    def get_maximum(self) -> int:
        """
        Return the greatest acceptable value.

        :return: Greatest acceptable value
        """
        return int(self._values_range[1])

    def get_minmax(self) -> Tuple2IntType:
        """
        Return the min and max acceptable tuple values.

        :return: Min, Max tuple
        """
        return self.get_minimum(), self.get_maximum()

    def get_orientation(self) -> str:
        """
        Return the scrollbar orientation (pygame-menu locals).

        :return: Scrollbar orientation
        """
        if self._orientation == 0:
            return ORIENTATION_HORIZONTAL
        else:
            return ORIENTATION_VERTICAL

    def get_page_step(self) -> int:
        """
        Return amount that the value changes by when the user
        click on the page control surface.

        :return: Page step
        """
        p_step = self._page_step * (self._values_range[1] -
                                    self._values_range[0]) / self._page_ctrl_length
        return int(p_step)

    def get_value_percentage(self) -> float:
        """
        Return the value but in percentage between ``0`` (minimum value) and ``1`` (maximum value).

        :return: Value as percentage
        """
        v_min, v_max = self.get_minmax()
        value = self.get_value()
        return round((value - v_min) / (v_max - v_min), 3)

    def get_value(self) -> int:
        """
        Return the value according to the slider position.

        :return: Position in px
        """
        value = self._values_range[0] + self._slider_position * \
                (self._values_range[1] -
                 self._values_range[0]) / (self._page_ctrl_length - self._page_step)

        # Correction due to value scaling
        value = max(self._values_range[0], value)
        value = min(self._values_range[1], value)
        return int(value)

    def _render(self) -> Optional[bool]:
        width, height = self._rect.width + self._rect_size_delta[0], \
                        self._rect.height + self._rect_size_delta[1]

        if not self._render_hash_changed(
                width, height, self._slider_rect.x, self._slider_rect.y,
                self.readonly, self._slider_rect.width, self._slider_rect.height,
                self.scrolling, self._mouseover, self._clicked):
            return True

        self._surface = make_surface(width, height)
        self._surface.fill(self._page_ctrl_color)

        # Render slider
        slider_color = self._slider_color if not self.readonly else self._font_readonly_color
        mouse_hover = (self.scrolling and self._clicked) or self._mouseover
        slider_color = self._slider_hover_color if mouse_hover else slider_color
        if self._shadow_enabled:
            lit_rect = pygame.Rect(self._slider_rect)
            slider_rect = lit_rect.inflate(-self._shadow_offset * 2, -self._shadow_offset * 2)
            shadow_rect = lit_rect.inflate(-self._shadow_offset, -self._shadow_offset)
            shadow_rect = shadow_rect.move(int(self._shadow_tuple[0] / 2),
                                           int(self._shadow_tuple[1] / 2))

            pygame.draw.rect(self._surface, self._font_selected_color, lit_rect)
            pygame.draw.rect(self._surface, self._shadow_color, shadow_rect)
            pygame.draw.rect(self._surface, slider_color, slider_rect)
        else:
            pygame.draw.rect(self._surface, slider_color, self._slider_rect)

    def _scroll(self, rect: 'pygame.Rect', pixels: NumberType) -> bool:
        """
        Moves the slider based on mouse events relative to change along axis.
        The slider travel is limited to page control length.

        :param rect: Precomputed rect
        :param pixels: Number of pixels to scroll
        :return: ``True`` is scroll position has changed
        """
        assert isinstance(pixels, NumberInstance)
        if not pixels:
            return False

        axis = self._orientation
        space_before = rect.topleft[axis] \
                       - self._slider_rect.move(*rect.topleft).topleft[axis] \
                       + self._slider_pad
        move = max(round(pixels), space_before)
        space_after = rect.bottomright[axis] \
                      - self._slider_rect.move(*rect.topleft).bottomright[axis] \
                      - self._slider_pad
        move = min(move, space_after)

        if not move:
            return False

        move_pos = [0, 0]
        move_pos[axis] = move
        self._slider_rect.move_ip(*move_pos)
        self._slider_position += move
        return True

    def set_length(self, value: NumberType) -> None:
        """
        Set the length of the page control area.

        :param value: Length of the area
        :return: None
        """
        assert isinstance(value, NumberInstance)
        assert 0 < value
        self._page_ctrl_length = value
        self._slider_position = min(self._slider_position,
                                    self._page_ctrl_length - self._page_step)
        self._apply_size_changes()

    def get_thickness(self) -> int:
        """
        Return the thickness of the bar.

        :return: Thickness in px
        """
        return self._page_ctrl_thick

    def show(self) -> 'ScrollBar':
        self._visible = True
        return self

    def hide(self) -> 'ScrollBar':
        if self._mouseover:
            self._mouseover = False
            self.mouseleave(mouse_motion_current_mouse_position())
        self._visible = False
        return self

    def set_maximum(self, value: NumberType) -> None:
        """
        Set the greatest acceptable value.

        :param value: Maximum value
        :return: None
        """
        assert isinstance(value, NumberInstance)
        assert value > self._values_range[0], \
            f'maximum value shall greater than {self._values_range[0]}'
        self._values_range[1] = value

    def set_minimum(self, value: NumberType) -> None:
        """
        Set the smallest acceptable value.

        :param value: Minimum value
        :return: None
        """
        assert isinstance(value, NumberInstance)
        assert 0 <= value < self._values_range[1], \
            f'minimum value shall lower than {self._values_range[1]}'
        self._values_range[0] = value

    def set_orientation(self, orientation: str) -> None:
        """
        Set the scroll bar orientation to vertical or horizontal.

        .. note::

            See :py:mod:`pygame_menu.locals` for valid ``orientation`` values.

        :param orientation: Widget orientation
        :return: None
        """
        assert_orientation(orientation)
        if orientation == ORIENTATION_HORIZONTAL:
            self._orientation = 0
        elif orientation == ORIENTATION_VERTICAL:
            self._orientation = 1
        self._apply_size_changes()

    def set_page_step(self, value: NumberType) -> None:
        """
        Set the amount that the value changes by when the user click on the
        page control surface.

        .. note::

            The length of the slider is related to this value, and typically
            represents the proportion of the document area shown in a scrolling view.

        :param value: Page step
        :return: None
        """
        assert isinstance(value, NumberInstance)
        assert 0 < value, 'page step shall be > 0'

        # Slider length shall represent the same ratio
        self._page_step = self._page_ctrl_length * value / \
                          (self._values_range[1] - self._values_range[0])

        if self._single_step >= self._page_step:
            self._single_step = self._page_step // 2  # Arbitrary to be lower than page step

        self._apply_size_changes()

    def set_value(self, position_value: NumberType) -> None:
        """
        Set the position of the scrollbar.

        :param position_value: Position
        :return: None
        """
        assert isinstance(position_value, NumberInstance)
        assert self._values_range[0] <= position_value <= self._values_range[1], \
            f'{self._values_range[0]} < {position_value} < {self._values_range[1]}'

        pixels = (position_value - self._values_range[0]) * \
                 (self._page_ctrl_length - self._page_step)
        pixels /= (self._values_range[1] - self._values_range[0])

        # Correction due to value scaling
        pixels = max(0, pixels)
        pixels = min(self._page_ctrl_length - self._page_step, pixels)

        self._scroll(self.get_rect(), pixels - self._slider_position)

    def get_slider_rect(self) -> 'pygame.Rect':
        """
        Get slider rect.

        :return: Slider rect
        """
        return self._slider_rect.move(*self.get_rect(to_absolute_position=True).topleft)

    def update(self, events: EventVectorType) -> bool:
        self.apply_update_callbacks(events)

        if self.readonly or not self.is_visible():
            self._readonly_check_mouseover(events)
            return False

        rect = self.get_rect(to_absolute_position=True)

        for event in events:

            # Check mouse over
            self._check_mouseover(event)

            # User press PAGEUP or PAGEDOWN
            if event.type == pygame.KEYDOWN and \
                    event.key in (pygame.K_PAGEUP, pygame.K_PAGEDOWN) and \
                    self._keyboard_enabled and self._orientation == 1 and \
                    not self.scrolling:
                direction = 1 if event.key == pygame.K_PAGEDOWN else -1
                keys_pressed = pygame.key.get_pressed()
                step = self._page_step
                if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]:
                    step *= 0.35
                pixels = direction * step
                if self._scroll(rect, pixels):
                    self.change()
                    return True

            # User moves mouse while scrolling
            elif (event.type == pygame.MOUSEMOTION and self._mouse_enabled and hasattr(event, 'rel') or
                  event.type == FINGERMOTION and self._touchscreen_enabled and self._menu is not None) and \
                    self.scrolling:
                # Get relative movement
                h = self.get_orientation() == ORIENTATION_HORIZONTAL
                rel = event.rel[self._orientation] if event.type == pygame.MOUSEMOTION else (
                    event.dx * 2 * self._menu.get_window_size()[0] if h else
                    event.dy * 2 * self._menu.get_window_size()[1]
                )

                # If mouse outside region and scroll is on limits, ignore
                mx, my = event.pos if event.type == pygame.MOUSEMOTION else \
                    get_finger_pos(self._menu, event)
                if self.get_value_percentage() in (0, 1) and \
                        self.get_scrollarea() is not None and \
                        self.get_scrollarea().get_parent() is not None:
                    if self._orientation == 1:  # Vertical
                        h = self._slider_rect.height / 2
                        if my > (rect.bottom - h) or my < (rect.top + h):
                            continue
                    elif self._orientation == 0:  # Horizontal
                        w = self._slider_rect.width / 2
                        if mx > (rect.right - w) or mx < (rect.left + w):
                            continue

                # Check scrolling
                if self._scroll(rect, rel):
                    self.change()
                    return True

            # Mouse enters or leaves the window
            elif event.type == pygame.ACTIVEEVENT and hasattr(event, 'gain'):
                mx, my = pygame.mouse.get_pos()
                if event.gain != 1:  # Leave
                    self._last_mouse_pos = (mx, my)
                else:
                    lmx, lmy = self._last_mouse_pos
                    self._last_mouse_pos = (-1, -1)
                    if lmx == -1 or lmy == -1:
                        continue
                    if self.scrolling:
                        if self._orientation == 0:  # Horizontal
                            self._scroll(rect, mx - lmx)
                        else:
                            self._scroll(rect, my - lmy)

            # User clicks the slider rect
            elif event.type == pygame.MOUSEBUTTONDOWN and self._mouse_enabled or \
                    event.type == FINGERDOWN and self._touchscreen_enabled and \
                    self._menu is not None:
                # Vertical bar: scroll down (4) or up (5). Mouse must be placed
                # over the area to enable this feature
                if not event.type == FINGERDOWN and \
                        event.button in (4, 5) and self._orientation == 1 and \
                        (self._scrollarea is not None and
                         self._scrollarea.mouse_is_over() or self._scrollarea is None):
                    direction = -1 if event.button == 4 else 1
                    if self._scroll(rect, direction * self._single_step):
                        self.change()
                        return True

                # Click button (left, middle, right)
                elif event.type == FINGERDOWN or event.button in (1, 2, 3):
                    event_pos = get_finger_pos(self._menu, event)

                    # The _slider_rect origin is related to the widget surface
                    if self.get_slider_rect().collidepoint(*event_pos):
                        # Initialize scrolling
                        self.scrolling = True
                        self._clicked = True
                        self._render()
                        return True

                    elif rect.collidepoint(*event_pos):
                        # Moves towards the click by one "page" (= slider length without pad)
                        s_rect = self.get_slider_rect()
                        pos = (s_rect.x, s_rect.y)
                        direction = 1 if event_pos[self._orientation] > pos[self._orientation] else -1
                        if self._scroll(rect, direction * self._page_step):
                            self.change()
                            return True

            # User releases mouse button if scrolling
            elif (event.type == pygame.MOUSEBUTTONUP and self._mouse_enabled or
                  event.type == FINGERUP and self._touchscreen_enabled) and self.scrolling:
                self._clicked = False
                self.scrolling = False
                self._render()
                return True

        return False
