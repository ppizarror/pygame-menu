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
from pygameMenu.widgets import ScrollBar


class ScrollArea(object):
    """
    The ScrollArea class provides a scrolling view managing up to 4 scroll bars.

    A scroll area is used to display the contents of a child surface (``world``).
    If the surface exceeds the size of the drawing surface, the view provide
    scroll bars so that the entire area of the child surface can be viewed.
    """

    def __init__(self,
                 world,
                 menu_width,
                 menu_height,
                 scrollbars=(_locals.POSITION_SOUTH, _locals.POSITION_EAST),
                 scrollbar_thick=20,
                 scrollbar_color=(235, 235, 235),
                 scrollbar_slider_pad=0,
                 scrollbar_slider_color=(200, 200, 200),
                 shadow=_cfg.MENU_OPTION_SHADOW,
                 shadow_color=_cfg.MENU_SHADOW_COLOR,
                 shadow_offset=_cfg.MENU_SHADOW_OFFSET):

        self._posx = 0
        self._posy = 0
        self._width = menu_width
        self._height = menu_height
        self._world = world
        self._scrollbars = []
        self._scrollbar_thick = scrollbar_thick
        self._scrollbar_positions = scrollbars
        self._view_rect = self.get_view_rect()

        for pos in set(self._scrollbar_positions):
            if pos == _locals.POSITION_EAST or pos == _locals.POSITION_WEST:
                sbar = ScrollBar(self._view_rect.height, (0, max(1, self.get_hidden_height())),
                                 orientation=_locals.ORIENTATION_VERTICAL,
                                 slider_pad=scrollbar_slider_pad,
                                 slider_color=scrollbar_slider_color,
                                 page_ctrl_thick=scrollbar_thick,
                                 page_ctrl_color=scrollbar_color,
                                 onchange=self._on_vertical_scroll)
                if pos == _locals.POSITION_WEST:
                    sbar.set_position(self._view_rect.left - scrollbar_thick, self._view_rect.top)
                else:
                    sbar.set_position(self._view_rect.right, self._view_rect.top)
            else:
                sbar = ScrollBar(self._view_rect.width, (0, max(1, self.get_hidden_width())),
                                 orientation=_locals.ORIENTATION_HORIZONTAL,
                                 slider_pad=scrollbar_slider_pad,
                                 slider_color=scrollbar_slider_color,
                                 page_ctrl_thick=scrollbar_thick,
                                 page_ctrl_color=scrollbar_color,
                                 onchange=self._on_horizontal_scroll)
                if pos == _locals.POSITION_NORTH:
                    sbar.set_position(self._view_rect.left, self._view_rect.top - scrollbar_thick)
                else:
                    sbar.set_position(self._view_rect.left, self._view_rect.bottom)

            sbar.set_shadow(enabled=shadow,
                            color=shadow_color,
                            position=_locals.POSITION_SOUTHEAST,
                            offset=shadow_offset)
            sbar.set_controls(False, True)

            self._scrollbars.append(sbar)

    def draw(self, surface):
        """
        Called by end user to draw state to the surface.
        """
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
        return max(0, self._world.get_width() - self._view_rect.width)

    def get_hidden_height(self):
        """
        Return the total height out of the bounds of the the viewable area.
        Zero is returned if the world height is lower than the viewable area.
        """
        return max(0, self._world.get_height() - self._view_rect.height)

    def get_view_rect(self):
        """
        Subtract width of scrollbars from area with the given size and return
        the viewable area.

        :param width: real width of the surface
        :param height: real height of the surface
        """
        rect = _pygame.Rect(self._posx, self._posy, self._width, self._height)

        if _locals.POSITION_NORTH in self._scrollbar_positions\
                and _locals.POSITION_SOUTH in self._scrollbar_positions:
            total_height_thick = 2 * self._scrollbar_thick
        else:
            total_height_thick = self._scrollbar_thick

        if _locals.POSITION_EAST in self._scrollbar_positions\
                and _locals.POSITION_WEST in self._scrollbar_positions:
            total_width_thick = 2 * self._scrollbar_thick
        else:
            total_width_thick = self._scrollbar_thick

        if _locals.POSITION_NORTH in self._scrollbar_positions\
                and self._world.get_width() > self._width - total_width_thick:
            rect.top = self._scrollbar_thick
            rect.height -= self._scrollbar_thick
        if _locals.POSITION_SOUTH in self._scrollbar_positions\
                and self._world.get_width() > self._width - total_width_thick:
            rect.height -= self._scrollbar_thick
        if _locals.POSITION_EAST in self._scrollbar_positions\
                and self._world.get_height() > self._height - total_height_thick:
            rect.width -= self._scrollbar_thick
        if _locals.POSITION_WEST in self._scrollbar_positions\
                and self._world.get_height() > self._height - total_height_thick:
            rect.left = self._scrollbar_thick
            rect.width -= self._scrollbar_thick
        return rect

    def _on_horizontal_scroll(self, value):
        """
        Call when a horizontal scroll bar as changed to update the
        position of the opposite one if it exists.
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
        self._posx = posx
        self._posy = posy

    def update(self, events):
        """
        Called by end user to update scroll state.
        """
        # Update viewable area if size of the world has changed
        self._view_rect = self.get_view_rect()

        for sbar in self._scrollbars:
            # Update value range if size of the world has changed
            if sbar.get_orientation() == _locals.ORIENTATION_HORIZONTAL\
                    and self.get_hidden_width() != sbar.get_maximum()\
                    and self.get_hidden_width() != 0:
                sbar.set_maximum(self.get_hidden_width())

            elif sbar.get_orientation() == _locals.ORIENTATION_VERTICAL\
                    and self.get_hidden_height() != sbar.get_maximum()\
                    and self.get_hidden_height() != 0:
                sbar.set_maximum(self.get_hidden_height())

            # Update scroll bar according to user events
            sbar.update(events)
