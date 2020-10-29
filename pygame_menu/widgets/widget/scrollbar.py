# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SCROLLBAR
ScrollBar class, manage the selection in a range of values.

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

import pygame
import pygame_menu.locals as _locals
from pygame_menu.utils import make_surface, assert_orientation, assert_color
from pygame_menu.widgets.core import Widget


class ScrollBar(Widget):
    """
    A scroll bar include 3 separate controls: a slider, scroll arrows, and a page control:

        a. The slider provides a way to quickly go to any part of the document
        b. The scroll arrows are push buttons which can be used to accurately navigate
           to a particular place in a document.
        c. The page control is the area over which the slider is dragged (the scroll bar's
           background). Clicking here moves the scroll bar towards the click by one "page".

    .. warning:: Arrows are not yet implemented

    :param length: Length of the page control
    :type length: int
    :param values_range: Min and max values
    :type values_range: tuple, list
    :param scrollbar_id: Bar identifier
    :type scrollbar_id: str
    :param orientation: Bar orientation ORIENTATION_HORIZONTAL/ORIENTATION_VERTICAL
    :type orientation: str
    :param slider_pad: Space between slider and page control
    :type slider_pad: int, float
    :param slider_color: Color of the slider
    :type slider_color: tuple, list
    :param page_ctrl_thick: Page control thickness
    :type page_ctrl_thick: int, float
    :param page_ctrl_color: Page control color
    :type page_ctrl_color: tuple, list
    :param onchange: Callback when changing the selector
    :type onchange: callable, None
    :param onreturn: Callback when pressing return button
    :type onreturn: callable, None
    """

    def __init__(self,
                 length,
                 values_range,
                 scrollbar_id='',
                 orientation=_locals.ORIENTATION_HORIZONTAL,
                 slider_pad=0,
                 slider_color=(200, 200, 200),
                 page_ctrl_thick=20,
                 page_ctrl_color=(235, 235, 235),
                 onchange=None,
                 onreturn=None,
                 *args,
                 **kwargs):
        assert isinstance(length, (int, float))
        assert isinstance(values_range, (tuple, list))
        assert values_range[1] > values_range[0], 'minimum value first is expected'
        assert isinstance(slider_pad, (int, float))
        assert isinstance(page_ctrl_thick, (int, float))
        assert page_ctrl_thick - 2 * slider_pad >= 2, 'slider shall be visible'

        assert_color(slider_color)
        assert_color(page_ctrl_color)

        super(ScrollBar, self).__init__(
            widget_id=scrollbar_id,
            onchange=onchange,
            onreturn=onreturn,
            args=args,
            kwargs=kwargs
        )

        self._values_range = list(values_range)
        self.scrolling = False  # type: bool
        self._orientation = 0  # type: int
        self._opp_orientation = int(not self._orientation)  # type: int

        self._page_ctrl_length = length
        self._page_ctrl_thick = page_ctrl_thick
        self._page_ctrl_color = page_ctrl_color

        self._slider_rect = None  # type: (pygame.Rect,None)
        self._slider_pad = slider_pad
        self._slider_color = slider_color
        self._slider_position = 0  # type: int

        self._single_step = 20  # type: int
        self._page_step = None  # type: (int,None)

        if values_range[1] - values_range[0] > length:
            self.set_page_step(length)
        else:
            self.set_page_step((values_range[1] - values_range[0]) / 5.0)  # Arbitrary
        self.set_orientation(orientation)

    def _apply_font(self):
        pass

    def _apply_size_changes(self):
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

    # noinspection PyMissingOrEmptyDocstring
    def draw(self, surface):
        self._render()
        self._fill_background_color(surface)
        surface.blit(self._surface, self._rect.topleft)

    def get_maximum(self):
        """
        Return the greatest acceptable value.

        :return: Greatest acceptable value
        :rtype: int
        """
        return self._values_range[1]

    def get_minimum(self):
        """
        Return the smallest acceptable value.

        :return: Smallest acceptable value
        :rtype: int
        """
        return self._values_range[0]

    def get_orientation(self):
        """
        Return the scrollbar orientation (pygame-menu locals).

        :return: Scrollbar orientation
        :rtype: str
        """
        if self._orientation == 0:
            return _locals.ORIENTATION_HORIZONTAL
        else:
            return _locals.ORIENTATION_VERTICAL

    def get_page_step(self):
        """
        Return amount that the value changes by when the user
        click on the page control surface.

        :return: Page step
        :rtype: int
        """
        return self._page_step * (self._values_range[1] - self._values_range[0]) / \
               self._page_ctrl_length

    def get_value(self):
        """
        Return the value according to the slider position.

        :return: Position in pixels
        :rtype: int
        """
        value = self._values_range[0] + self._slider_position * \
                (self._values_range[1] - self._values_range[0]) / (self._page_ctrl_length - self._page_step)

        # Correction due to value scaling
        value = max(self._values_range[0], value)
        value = min(self._values_range[1], value)
        return value

    def _render(self):
        if not self._render_hash_changed(self._rect.size, self._slider_rect.x, self._slider_rect.y,
                                         self._slider_rect.width, self._slider_rect.height):
            return

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

    def _scroll(self, pixels):
        """
        Moves the slider based on mouse events relative to change along axis.
        The slider travel is limited to page control length.

        :param pixels: Number of pixels to scroll
        :type pixels: int, float
        :return: True is scroll position has changed
        :rtype: bool
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

    def set_length(self, value):
        """
        Set the length of the page control area.

        :param value: Length of the area
        :type value: int, float
        :return: None
        """
        assert isinstance(value, (int, float))
        assert 0 < value
        self._page_ctrl_length = value
        self._slider_position = min(self._slider_position, self._page_ctrl_length - self._page_step)
        self._apply_size_changes()

    def set_maximum(self, value):
        """
        Set the greatest acceptable value.

        :param value: Maximum value
        :type value: int, float
        :return: None
        """
        assert isinstance(value, (int, float))
        assert value > self._values_range[0], 'maximum value shall greater than {}'.format(self._values_range[0])
        self._values_range[1] = value

    def set_minimum(self, value):
        """
        Set the smallest acceptable value.

        :param value: Minimum value
        :type value: int, float
        :return: None
        """
        assert isinstance(value, (int, float))
        assert 0 <= value < self._values_range[1], 'minimum value shall lower than {}'.format(self._values_range[1])
        self._values_range[0] = value

    def set_orientation(self, orientation):
        """
        Set the scroll bar orientation to vertical or horizontal.

        :param orientation: Widget orientation, could be `ORIENTATION_HORIZONTAL / ORIENTATION_VERTICAL`
        :type orientation: str
        :return: None
        """
        assert_orientation(orientation)
        if orientation == _locals.ORIENTATION_HORIZONTAL:
            self._orientation = 0
        elif orientation == _locals.ORIENTATION_VERTICAL:
            self._orientation = 1
        self._opp_orientation = int(not self._orientation)
        self._apply_size_changes()

    def set_page_step(self, value):
        """
        Set the amount that the value changes by when the user click on the
        page control surface.
        The length of the slider is related to this value, and typically
        represents the proportion of the document area shown in a scrolling
        view.

        :param value: Page step
        :type value: int, float
        :return: None
        """
        assert isinstance(value, (int, float))
        assert 0 < value, 'page step shall be > 0'

        # Slider length shall represent the same ratio
        self._page_step = round(1.0 * self._page_ctrl_length * value /
                                (self._values_range[1] - self._values_range[0]))

        if self._single_step >= self._page_step:
            self._single_step = self._page_step // 2  # Arbitrary to be lower than page step

        self._apply_size_changes()

    def set_value(self, value):
        """
        Set the position of the scrollbar.

        :param value: Position
        :type value: int, float
        :return: None
        """
        assert isinstance(value, (int, float))
        assert self._values_range[0] <= value <= self._values_range[1], \
            '{} < {} < {}'.format(self._values_range[0], value, self._values_range[1])

        pixels = 1.0 * (value - self._values_range[0]) * (self._page_ctrl_length - self._page_step) / \
                 (self._values_range[1] - self._values_range[0])

        # Correction due to value scaling
        pixels = max(0, pixels)
        pixels = min(self._page_ctrl_length - self._page_step, pixels)

        self._scroll(pixels - self._slider_position)

    # noinspection PyMissingOrEmptyDocstring
    def update(self, events):
        updated = False
        for event in events:  # type: pygame.event.Event

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

            elif self.mouse_enabled and event.type == pygame.MOUSEMOTION and self.scrolling:
                if self._scroll(event.rel[self._orientation]):
                    self.change()
                    updated = True

            elif self.mouse_enabled and event.type == pygame.MOUSEBUTTONDOWN:
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

            elif self.mouse_enabled and event.type == pygame.MOUSEBUTTONUP:
                if self.scrolling:
                    self.scrolling = False
                    updated = True

        return updated
