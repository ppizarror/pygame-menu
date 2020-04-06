# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SCROLLAREA
ScrollArea class to manage scrolling in menu.

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
import pygameMenu.config as _cfg
import pygameMenu.locals as _locals
from pygameMenu.widgets import ScrollBar as _ScrollBar


class ScrollArea(object):
    """
    The ScrollArea class provides a scrolling view managing up to 4 scroll bars.

    A scroll area is used to display the contents of a child surface (``world``).
    If the surface exceeds the size of the drawing surface, the view provide
    scroll bars so that the entire area of the child surface can be viewed.
    """

    def __init__(self,
                 menu_width,
                 menu_height,
                 world=None,
                 scrollbars=(_locals.POSITION_SOUTH, _locals.POSITION_EAST),
                 scrollbar_thick=20,
                 scrollbar_color=(235, 235, 235),
                 scrollbar_slider_pad=0,
                 scrollbar_slider_color=(200, 200, 200),
                 shadow=_cfg.MENU_OPTION_SHADOW,
                 shadow_color=_cfg.MENU_SHADOW_COLOR,
                 shadow_offset=_cfg.MENU_SHADOW_OFFSET,
                 shadow_position=_locals.POSITION_SOUTHEAST):

        self._rect = _pygame.Rect(0, 0, menu_width, menu_height)
        self._world = world
        self._scrollbars = []
        self._scrollbar_positions = tuple(set(scrollbars))  # Ensure unique
        self._scrollbar_thick = scrollbar_thick
        self._view_rect = self.get_view_rect()

        for pos in self._scrollbar_positions:
            if pos == _locals.POSITION_EAST or pos == _locals.POSITION_WEST:
                sbar = _ScrollBar(self._view_rect.height, (0, max(1, self.get_hidden_height())),
                                  orientation=_locals.ORIENTATION_VERTICAL,
                                  slider_pad=scrollbar_slider_pad,
                                  slider_color=scrollbar_slider_color,
                                  page_ctrl_thick=scrollbar_thick,
                                  page_ctrl_color=scrollbar_color,
                                  onchange=self._on_vertical_scroll)
            else:
                sbar = _ScrollBar(self._view_rect.width, (0, max(1, self.get_hidden_width())),
                                  orientation=_locals.ORIENTATION_HORIZONTAL,
                                  slider_pad=scrollbar_slider_pad,
                                  slider_color=scrollbar_slider_color,
                                  page_ctrl_thick=scrollbar_thick,
                                  page_ctrl_color=scrollbar_color,
                                  onchange=self._on_horizontal_scroll)

            sbar.set_shadow(enabled=shadow,
                            color=shadow_color,
                            position=shadow_position,
                            offset=shadow_offset)
            sbar.set_controls(False, True)

            self._scrollbars.append(sbar)

        self._apply_size_changes()

    def _apply_size_changes(self):
        self._view_rect = self.get_view_rect()
        for sbar in self._scrollbars:
            pos = self._scrollbar_positions[self._scrollbars.index(sbar)]
            if pos == _locals.POSITION_WEST:
                sbar.set_position(self._view_rect.left - self._scrollbar_thick, self._view_rect.top)
            elif pos == _locals.POSITION_EAST:
                sbar.set_position(self._view_rect.right, self._view_rect.top)
            elif pos == _locals.POSITION_NORTH:
                sbar.set_position(self._view_rect.left, self._view_rect.top - self._scrollbar_thick)
            else:
                sbar.set_position(self._view_rect.left, self._view_rect.bottom)

            if pos in (_locals.POSITION_NORTH, _locals.POSITION_SOUTH)\
                    and self.get_hidden_width() != sbar.get_maximum()\
                    and self.get_hidden_width() != 0:
                sbar.set_length(self._view_rect.width)
                sbar.set_maximum(self.get_hidden_width())
                sbar.set_page_step(self._view_rect.width * self.get_hidden_width() /
                                   (self._view_rect.width + self.get_hidden_width()))

            elif pos in (_locals.POSITION_EAST, _locals.POSITION_WEST)\
                    and self.get_hidden_height() != sbar.get_maximum()\
                    and self.get_hidden_height() != 0:
                sbar.set_length(self._view_rect.height)
                sbar.set_maximum(self.get_hidden_height())
                sbar.set_page_step(self._view_rect.height * self.get_hidden_height() /
                                   (self._view_rect.height + self.get_hidden_height()))

    def draw(self, surface):
        """
        Called by end user to draw state to the surface.
        """
        if not self._world:
            return

        offsets = [0, 0]
        for sbar in self._scrollbars:
            if sbar.get_orientation() == _locals.ORIENTATION_HORIZONTAL:
                if self.get_hidden_width():
                    sbar.draw(surface)
                    offsets[0] = sbar.get_value()
            else:
                if self.get_hidden_height():
                    sbar.draw(surface)
                    offsets[1] = sbar.get_value()

        surface.blit(self._world, self._view_rect.topleft, (offsets, self._view_rect.size))

    def get_hidden_width(self):
        """
        Return the total width out of the bounds of the the viewable area.
        Zero is returned if the world width is lower than the viewable area.
        """
        if not self._world:
            return 0
        return max(0, self._world.get_width() - self._view_rect.width)

    def get_hidden_height(self):
        """
        Return the total height out of the bounds of the the viewable area.
        Zero is returned if the world height is lower than the viewable area.
        """
        if not self._world:
            return 0
        return max(0, self._world.get_height() - self._view_rect.height)

    def get_rect(self):
        """
        Return the Rect object.

        :return: pygame.Rect
        :rtype: pygame.rect.RectType
        """
        return self._rect

    def get_view_rect(self):
        """
        Subtract width of scrollbars from area with the given size and return
        the viewable area.

        The viewable area depends on the world size, because scroll bars may
        or may not be displayed.

        :param width: real width of the surface
        :param height: real height of the surface
        """
        rect = _pygame.Rect(self._rect)

        if not self._world or (self._world.get_width() <= self._rect.width
                               and self._world.get_height() <= self._rect.height):
            return rect  # Area is enought large to display world

        if self._world.get_width() - self._rect.width > 0:
            if _locals.POSITION_NORTH in self._scrollbar_positions:
                rect.top += self._scrollbar_thick
                rect.height -= self._scrollbar_thick
            if _locals.POSITION_SOUTH in self._scrollbar_positions:
                rect.height -= self._scrollbar_thick
        if self._world.get_height() - self._rect.height > 0:
            if _locals.POSITION_WEST in self._scrollbar_positions:
                rect.left += self._scrollbar_thick
                rect.width -= self._scrollbar_thick
            if _locals.POSITION_EAST in self._scrollbar_positions:
                rect.width -= self._scrollbar_thick

        return rect

    def _on_horizontal_scroll(self, value):
        """
        Call when a horizontal scroll bar as changed to update the
        position of the opposite one if it exists.

        :param value: new position of the slider
        :type value: float
        """
        for sbar in self._scrollbars:
            if sbar.get_orientation() == _locals.ORIENTATION_HORIZONTAL\
                    and self.get_hidden_width() != 0\
                    and sbar.get_value() != value:
                sbar.set_value(value)

    def _on_vertical_scroll(self, value):
        """
        Call when a vertical scroll bar as changed to update the
        position of the opposite one if it exists.

        :param value: new position of the slider
        :type value: float
        """
        for sbar in self._scrollbars:
            if sbar.get_orientation() == _locals.ORIENTATION_VERTICAL\
                    and self.get_hidden_height() != 0\
                    and sbar.get_value() != value:
                sbar.set_value(value)

    def set_position(self, posx, posy):
        """
        Set the position.

        :param posx: X position
        :type posx: int, float
        :param posy: Y position
        :type posy: int, float
        :return: None
        """
        self._rect.x = posx
        self._rect.y = posy
        self._apply_size_changes()

    def set_world(self, surface):
        """
        Update the scrolled surface.

        :param surface: new world surface
        :type surface: pygame.Surface
        """
        self._world = surface
        self._apply_size_changes()

    def update(self, events):
        """
        Called by end user to update scroll state.
        """
        for sbar in self._scrollbars:
            sbar.update(events)
