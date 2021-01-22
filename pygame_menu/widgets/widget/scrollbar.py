"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SCROLLBAR
ScrollBar class, manage the selection in a range of values.

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

__all__ = ['ScrollBar']

import pygame
from pygame_menu.custom_types import NumberType
from pygame_menu.utils import make_surface, assert_orientation, assert_color
from pygame_menu.widgets.core import Widget
import pygame_menu.locals as _locals
from pygame_menu.custom_types import Optional, List, Tuple, PaddingType, VectorIntType, ColorType, \
    CallbackType, Union


# noinspection PyMissingOrEmptyDocstring
class ScrollBar(Widget):
    """
    A scroll bar include 3 separate controls: a slider, scroll arrows, and a page control:

        a. The slider provides a way to quickly go to any part of the document.
        b. The scroll arrows are push buttons which can be used to accurately navigate
           to a particular place in a document.
        c. The page control is the area over which the slider is dragged (the scroll bar's
           background). Clicking here moves the scroll bar towards the click by one page.

    .. note::

        This widget only accepts translation transformation.

    .. warning::

        Arrows are not yet implemented.

    :param length: Length of the page control
    :param values_range: Min and max values
    :param scrollbar_id: Bar identifier
    :param orientation: Bar orientation ``ORIENTATION_HORIZONTAL``/``ORIENTATION_VERTICAL``
    :param slider_pad: Space between slider and page control
    :param slider_color: Color of the slider
    :param page_ctrl_thick: Page control thickness
    :param page_ctrl_color: Page control color
    :param onchange: Callback when pressing and moving the scroll
    """
    _opp_orientation: int
    _orientation: int
    _page_ctrl_color: ColorType
    _page_ctrl_length: NumberType
    _page_ctrl_thick: int
    _page_step: NumberType
    _single_step: NumberType
    _slider_color: ColorType
    _slider_pad: int
    _slider_position: int
    _slider_rect: Optional['pygame.Rect']
    _values_range: List[NumberType]
    scrolling: bool

    def __init__(self,
                 length: NumberType,
                 values_range: VectorIntType,
                 scrollbar_id: str = '',
                 orientation: str = _locals.ORIENTATION_HORIZONTAL,
                 slider_pad: NumberType = 0,
                 slider_color: ColorType = (200, 200, 200),
                 page_ctrl_thick: int = 20,
                 page_ctrl_color: ColorType = (235, 235, 235),
                 onchange: CallbackType = None,
                 *args,
                 **kwargs
                 ) -> None:
        assert isinstance(length, (int, float))
        assert isinstance(values_range, (tuple, list))
        assert values_range[1] > values_range[0], 'minimum value first is expected'
        assert isinstance(slider_pad, (int, float))
        assert isinstance(page_ctrl_thick, int)
        assert page_ctrl_thick - 2 * slider_pad >= 2, 'slider shall be visible'

        assert_color(slider_color)
        assert_color(page_ctrl_color)

        super(ScrollBar, self).__init__(
            widget_id=scrollbar_id,
            onchange=onchange,
            args=args,
            kwargs=kwargs
        )

        self._values_range = list(values_range)
        self.scrolling = False
        self._orientation = 0
        self._opp_orientation = int(not self._orientation)

        self._page_ctrl_length = length
        self._page_ctrl_thick = page_ctrl_thick
        self._page_ctrl_color = page_ctrl_color

        self._slider_rect = None
        self._slider_pad = slider_pad
        self._slider_color = slider_color
        self._slider_position = 0

        self._single_step = 20
        self._page_step = 0

        if values_range[1] - values_range[0] > length:
            self.set_page_step(length)
        else:
            self.set_page_step((values_range[1] - values_range[0]) / 5.0)  # Arbitrary
        self.set_orientation(orientation)
        self.is_selectable = False

    def _apply_font(self) -> None:
        pass

    def set_padding(self, padding: PaddingType) -> None:
        pass

    def scale(self, width: NumberType, height: NumberType, smooth: bool = False) -> None:
        pass

    def resize(self, width: NumberType, height: NumberType, smooth: bool = False) -> None:
        pass

    def set_max_width(self, width: Optional[NumberType], scale_height: NumberType = False,
                      smooth: bool = True) -> None:
        pass

    def set_max_height(self, height: Optional[NumberType], scale_width: NumberType = False,
                       smooth: bool = True) -> None:
        pass

    def rotate(self, angle: NumberType) -> None:
        pass

    def flip(self, x: bool, y: bool) -> None:
        pass

    def _apply_size_changes(self) -> None:
        """
        Apply scrollbar changes.

        :return: None
        """
        dims = ('width', 'height')
        setattr(self._rect, dims[self._orientation], self._page_ctrl_length)
        setattr(self._rect, dims[self._opp_orientation], self._page_ctrl_thick)
        self._slider_rect = pygame.Rect(0, 0, int(self._rect.width), int(self._rect.height))
        setattr(self._slider_rect, dims[self._orientation], self._page_step)
        setattr(self._slider_rect, dims[self._opp_orientation], self._page_ctrl_thick)

        # Update slider position according to the current one
        pos = ('x', 'y')
        setattr(self._slider_rect, pos[self._orientation], self._slider_position)
        self._slider_rect = self._slider_rect.inflate(-2 * self._slider_pad, -2 * self._slider_pad)

    def _draw(self, surface: 'pygame.Surface') -> None:
        surface.blit(self._surface, self._rect.topleft)

    def get_maximum(self) -> int:
        """
        Return the greatest acceptable value.

        :return: Greatest acceptable value
        """
        return int(self._values_range[1])

    def get_minimum(self) -> int:
        """
        Return the smallest acceptable value.

        :return: Smallest acceptable value
        """
        return int(self._values_range[0])

    def get_orientation(self) -> str:
        """
        Return the scrollbar orientation (pygame-menu locals).

        :return: Scrollbar orientation
        """
        if self._orientation == 0:
            return _locals.ORIENTATION_HORIZONTAL
        else:
            return _locals.ORIENTATION_VERTICAL

    def get_page_step(self) -> int:
        """
        Return amount that the value changes by when the user
        click on the page control surface.

        :return: Page step
        """
        pstep = self._page_step * (self._values_range[1] - self._values_range[0]) / self._page_ctrl_length
        return int(pstep)

    def get_value(self) -> int:
        """
        Return the value according to the slider position.

        :return: Position in pixels (px)
        """
        value = self._values_range[0] + self._slider_position * \
                (self._values_range[1] - self._values_range[0]) / (self._page_ctrl_length - self._page_step)

        # Correction due to value scaling
        value = max(self._values_range[0], value)
        value = min(self._values_range[1], value)
        return int(value)

    def _render(self) -> Optional[bool]:
        if not self._render_hash_changed(self._rect.size, self._slider_rect.x, self._slider_rect.y,
                                         self._slider_rect.width, self._slider_rect.height, self._visible):
            return True

        self._surface = make_surface(*self._rect.size)
        self._surface.fill(self._page_ctrl_color)

        # Render slider
        if self._shadow:
            lit_rect = pygame.Rect(self._slider_rect)
            slider_rect = lit_rect.inflate(-self._shadow_offset * 2, -self._shadow_offset * 2)
            shadow_rect = lit_rect.inflate(-self._shadow_offset, -self._shadow_offset)
            shadow_rect = shadow_rect.move(self._shadow_tuple[0] / 2, self._shadow_tuple[1] / 2)

            pygame.draw.rect(self._surface, self._font_selected_color, lit_rect)
            pygame.draw.rect(self._surface, self._shadow_color, shadow_rect)
            pygame.draw.rect(self._surface, self._slider_color, slider_rect)
        else:
            pygame.draw.rect(self._surface, self._slider_color, self._slider_rect)

    def _scroll(self, pixels: NumberType) -> bool:
        """
        Moves the slider based on mouse events relative to change along axis.
        The slider travel is limited to page control length.

        :param pixels: Number of pixels to scroll
        :return: ``True`` is scroll position has changed
        """
        assert isinstance(pixels, (int, float))
        if not pixels:
            return False

        axis = self._orientation
        space_before = self._rect.topleft[axis] - \
                       self._slider_rect.move(*self._rect.topleft).topleft[axis] + self._slider_pad
        move = max(round(pixels), space_before)
        space_after = self._rect.bottomright[axis] - \
                      self._slider_rect.move(*self._rect.topleft).bottomright[axis] - self._slider_pad
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
        assert isinstance(value, (int, float))
        assert 0 < value
        self._page_ctrl_length = value
        self._slider_position = min(self._slider_position, self._page_ctrl_length - self._page_step)
        self._apply_size_changes()

    def get_thickness(self) -> int:
        """
        Return the thickness of the bar.

        :return: Thickness (px)
        """
        return self._page_ctrl_thick

    def set_maximum(self, value: NumberType) -> None:
        """
        Set the greatest acceptable value.

        :param value: Maximum value
        :return: None
        """
        assert isinstance(value, (int, float))
        assert value > self._values_range[0], 'maximum value shall greater than {}'.format(self._values_range[0])
        self._values_range[1] = value

    def set_minimum(self, value: NumberType) -> None:
        """
        Set the smallest acceptable value.

        :param value: Minimum value
        :return: None
        """
        assert isinstance(value, (int, float))
        assert 0 <= value < self._values_range[1], 'minimum value shall lower than {}'.format(self._values_range[1])
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
        if orientation == _locals.ORIENTATION_HORIZONTAL:
            self._orientation = 0
        elif orientation == _locals.ORIENTATION_VERTICAL:
            self._orientation = 1
        self._opp_orientation = int(not self._orientation)
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
        assert isinstance(value, (int, float))
        assert 0 < value, 'page step shall be > 0'

        # Slider length shall represent the same ratio
        self._page_step = self._page_ctrl_length * value / (self._values_range[1] - self._values_range[0])

        if self._single_step >= self._page_step:
            self._single_step = self._page_step // 2  # Arbitrary to be lower than page step

        self._apply_size_changes()

    def set_value(self, value: NumberType) -> None:
        """
        Set the position of the scrollbar.

        :param value: Position
        :return: None
        """
        assert isinstance(value, (int, float))
        assert self._values_range[0] <= value <= self._values_range[1], \
            '{} < {} < {}'.format(self._values_range[0], value, self._values_range[1])

        pixels = (value - self._values_range[0]) * (self._page_ctrl_length - self._page_step)
        pixels /= self._values_range[1] - self._values_range[0]

        # Correction due to value scaling
        pixels = max(0, pixels)
        pixels = min(self._page_ctrl_length - self._page_step, pixels)

        self._scroll(pixels - self._slider_position)

    def update(self, events: Union[List['pygame.event.Event'], Tuple['pygame.event.Event']]) -> bool:
        if self.readonly:
            return False
        updated = False

        for event in events:

            if event.type == pygame.KEYDOWN:

                if self._orientation == 1 and event.key in (pygame.K_PAGEUP, pygame.K_PAGEDOWN):
                    direction = 1 if event.key == pygame.K_PAGEDOWN else -1
                    keys_pressed = pygame.key.get_pressed()
                    step = self._page_step
                    if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]:
                        step *= 0.35
                    if self._scroll(direction * step):
                        self.change()
                        updated = True

            elif self._mouse_enabled and event.type == pygame.MOUSEMOTION and self.scrolling:
                if self._scroll(event.rel[self._orientation]):
                    self.change()
                    updated = True

            elif self._mouse_enabled and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (4, 5) and self._orientation == 1:
                    # Vertical bar: scroll down (4) or up (5)
                    direction = -1 if event.button == 4 else 1
                    if self._scroll(direction * self._single_step):
                        self.change()
                        updated = True
                else:
                    # The _slider_rect origin is related to the widget surface
                    if self._slider_rect.move(*self._rect.topleft).collidepoint(event.pos):
                        # Initialize scrolling
                        self.scrolling = True

                    elif self._rect.collidepoint(*event.pos):
                        # Moves towards the click by one "page" (= slider length without pad)
                        srect = self._slider_rect.move(*self._rect.topleft)
                        pos = (srect.x, srect.y)
                        direction = 1 if event.pos[self._orientation] > pos[self._orientation] else -1
                        if self._scroll(direction * self._page_step):
                            self.change()
                            updated = True

            elif self._mouse_enabled and event.type == pygame.MOUSEBUTTONUP:
                if self.scrolling:
                    self.scrolling = False
                    updated = True

        if updated:
            self.apply_update_callbacks()

        return updated
