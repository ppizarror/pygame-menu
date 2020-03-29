# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

ScrollArea
ScrollArea and ScrollBar class to manage scrolling in menu.

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

import pygame as _pygame
from pygameMenu.widgets.widget import Widget
import pygameMenu.locals as _locals


class ScrollBar(Widget):
    """
    A scroll bar include 3 separate controls: a slider, scroll arrows, and a page control.

        a. The slider provides a way to quickly go to any part of the document

        b. The scroll arrows are push buttons which can be used to accurately navigate
           to a particular place in a document. TODO: arrows not yet implemented

        c. The page control is the area over which the slider is dragged (the scroll bar's
           background). Clicking here moves the scroll bar towards the click by one "page".
    """

    def __init__(self,
                 length,
                 values_range,
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
        assert isinstance(slider_pad, (int, float))
        assert isinstance(page_ctrl_thick, (int, float))
        assert page_ctrl_thick - 2 * slider_pad >= 2, "slider shall be visible"

        super(ScrollBar, self).__init__(onchange=onchange,
                                        onreturn=onreturn,
                                        args=args,
                                        kwargs=kwargs)
        self._values_range = values_range
        self._scrolling = False
        self._orientation = 0
        self._opp_orientation = int(not self._orientation)

        self._page_ctrl_length = length
        self._page_ctrl_thick = page_ctrl_thick
        self._page_ctrl_color = page_ctrl_color
        self._page_ctrl_step = None  # type: int

        self._slider_rect = None  # type: _pygame.rect.RectType
        self._slider_pad = slider_pad
        self._slider_color = slider_color
        self._slider_position = 0
        self._slider_length = None  # type: int

        self.set_page_step((values_range[1] - values_range[0]) / 5)  # Arbitrary
        self.set_orientation(orientation)

    def _apply_size_changes(self):
        dims = ('width', 'height')
        setattr(self._rect, dims[self._orientation], self._page_ctrl_length)
        setattr(self._rect, dims[self._opp_orientation], self._page_ctrl_thick)
        self._slider_rect = _pygame.Rect(0, 0, self._rect.width, self._rect.height)
        setattr(self._slider_rect, dims[self._orientation], self._slider_length)
        setattr(self._slider_rect, dims[self._opp_orientation], self._page_ctrl_thick)
        self._slider_rect = self._slider_rect.inflate(-2 * self._slider_pad, -2 * self._slider_pad)

    def _apply_font(self):
        """
        See upper class doc.
        """
        pass

    def draw(self, surface):
        """
        See upper class doc.
        """
        self._render()
        surface.blit(self._surface, self._rect.topleft)

    def get_maximum(self):
        """
        Return the greatest acceptable value.
        """
        return self._values_range[1]

    def get_minimum(self):
        """
        Return the smallest acceptable value.
        """
        return self._values_range[0]

    def get_orientation(self):
        """
        Return the scroll bar orentation.
        """
        if self._orientation == 0:
            return _locals.ORIENTATION_HORIZONTAL
        else:
            return _locals.ORIENTATION_VERTICAL

    def get_page_step(self):
        """
        Return amount that the value changes by when the user click on the
        page control surface.
        """
        return self._page_ctrl_step * (self._values_range[1] - self._values_range[0]) / \
            (self._page_ctrl_length - self._slider_length)

    def get_value(self):
        """
        Return the value according to the slider position.

        :return: position in pixels
        :rtype: int
        """
        value = self._values_range[0] + self._slider_position *\
            (self._values_range[1] - self._values_range[0]) / (self._page_ctrl_length - self._slider_length)

        # Correction due to value scaling
        value = max(self._values_range[0], value)
        value = min(self._values_range[1], value)
        return value

    def _render(self):
        """
        See upper class doc.
        """
        # Render page control
        self._surface = _pygame.Surface(self._rect.size)
        self._surface.fill(self._page_ctrl_color)

        # Render slider
        if self._shadow:
            lit_rect = _pygame.Rect(self._slider_rect)
            slider_rect = lit_rect.inflate(-self._shadow_offset * 2, -self._shadow_offset * 2)
            shadow_rect = lit_rect.inflate(-self._shadow_offset, -self._shadow_offset)
            shadow_rect = shadow_rect.move(self._shadow_tuple[0] / 2, self._shadow_tuple[1] / 2)

            _pygame.draw.rect(self._surface, self._font_color, lit_rect, 0)
            _pygame.draw.rect(self._surface, self._shadow_color, shadow_rect, 0)
            _pygame.draw.rect(self._surface, self._slider_color, slider_rect, 0)
        else:
            _pygame.draw.rect(self._surface, self._slider_color, self._slider_rect, 0)

    def _scroll(self, pixels):
        """Moves the slider based on mouse events relatif change along axis.
        The slider travel is limited to page control length.

        :param pixels: number of pixels to scroll
        :type pixels: int
        :return: True is scroll position has changed
        :rtype: bool
        """
        if not pixels:
            return False

        axis = self._orientation
        space_before = self._rect.topleft[axis] - self._slider_rect.topleft[axis] + self._slider_pad
        move = max(round(pixels), space_before)
        space_after = self._rect.bottomright[axis] - self._slider_rect.bottomright[axis] - self._slider_pad
        move = min(move, space_after)
        if not move:
            return False

        move_pos = [0, 0]
        move_pos[axis] = move
        self._slider_rect.move_ip(move_pos)
        self._slider_position += move
        return True

    def set_orientation(self, orientation):
        """
        Set the scroll bar orentation to vertical or horizontal.

        :param align: Widget orentation, could be ORIENTATION_HORIZONTAL/ORIENTATION_VERTICAL
        :type align: basestring
        :return: None
        """
        if orientation == _locals.ORIENTATION_HORIZONTAL:
            self._orientation = 0
        elif orientation == _locals.ORIENTATION_VERTICAL:
            self._orientation = 1
        else:
            raise ValueError('Incorrect orientation of the widget')
        self._opp_orientation = int(not self._orientation)
        self._apply_size_changes()

    def set_page_step(self, value):
        """
        Set the amount that the value changes by when the user click on the
        page control surface.

        The length of the slider is related to this value, and typically
        represents the proportion of the document area shown in a scrolling
        view.

        :param value: page step
        :type value: int
        :return: None
        """
        assert value > 0 and value < self._values_range[1] - self._values_range[0]

        # Slider lenght shall represent the same ratio
        self._slider_length = round(1.0 * self._page_ctrl_length * value /
                                    (self._values_range[1] - self._values_range[0]))

        self._page_ctrl_step = round(1.0 * (self._page_ctrl_length - self._slider_length) *
                                     value / (self._values_range[1] - self._values_range[0]))

        self._apply_size_changes()

    def set_value(self, value):
        """
        Set the value and update the position of the slider accordingly.

        :param value: value in the values_range
        :type value: int
        :return: None
        """
        assert value >= self._values_range[0] and value <= self._values_range[1]

        pixels = 1.0 * (value - self._values_range[0]) * (self._page_ctrl_length - self._slider_length) /\
            (self._values_range[1] - self._values_range[0])

        # Correction due to value scaling
        pixels = max(0, pixels)
        pixels = min(self._page_ctrl_length - self._slider_length, pixels)

        self._scroll(pixels - self._slider_position)

    def update(self, events):
        """
        See upper class doc.
        """
        updated = False
        for event in events:  # type: _pygame.event.EventType
            if self.mouse_enabled and event.type is _pygame.MOUSEMOTION and self._scrolling:
                if self._scroll(event.rel[self._orientation]):
                    self.change()
                    updated = True

            elif self.mouse_enabled and event.type is _pygame.MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                topleftx, toplefty = self._rect.topleft

                # The _slider_rect origin is related to the widget surface
                if self._slider_rect.collidepoint((mousex - topleftx, mousey - toplefty)):
                    # Initialize scrolling
                    self._scrolling = True

                elif self._rect.collidepoint(event.pos):
                    # Moves towards the click by one "page" (= slider length without pad)
                    pos = (self._slider_rect.x, self._slider_rect.y)
                    direction = 1 if event.pos[self._orientation] > pos[self._orientation] else -1
                    if self._scroll(direction * self._page_ctrl_step):
                        self.change()
                        updated = True

            elif self.mouse_enabled and event.type is _pygame.MOUSEBUTTONUP:
                self._scrolling = False

        return updated
