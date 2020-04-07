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
                 area_width,
                 area_height,
                 world=None,
                 area_color=None,
                 scrollbars=(_locals.POSITION_SOUTH, _locals.POSITION_EAST),
                 scrollbar_thick=20,
                 scrollbar_color=(235, 235, 235),
                 scrollbar_slider_pad=0,
                 scrollbar_slider_color=(200, 200, 200),
                 shadow=_cfg.MENU_OPTION_SHADOW,
                 shadow_color=_cfg.MENU_SHADOW_COLOR,
                 shadow_offset=_cfg.MENU_SHADOW_OFFSET,
                 shadow_position=_locals.POSITION_SOUTHEAST):
        """
        Description of the parameters:

        :param area_width: Width of scrollable area (px)
        :type area_width: int
        :param area_height: Height of scrollable area (px)
        :type area_height: int
        :param world: Surface to draw and scroll
        :type world: pygame.Surface, NoneType
        :param area_color: Background color
        :type area_color: tuple, list, NoneType
        :param scrollbars: Postions of the scrollbars
        :type scrollbars: tuple, list
        :param scrollbar_thick: Scrollbars thickness
        :type scrollbar_thick: int
        :param scrollbar_color: Scrollbars color
        :type scrollbar_color: tuple, list
        :param scrollbar_slider_pad: Space between slider and scrollbars borders
        :type scrollbar_slider_pad: int
        :param scrollbar_slider_color: Color of the sliders
        :type scrollbar_slider_color: tuple, list
        :param shadow: Indicate if a shadow is drawn on each scrollbar
        :type shadow: bool
        :param shadow_color: Color of the shadow
        :type shadow_color: tuple, list
        :param shadow_offset: Offset of shadow
        :type shadow_offset: int
        :param shadow_position: Position of shadow
        :type shadow_position: basestring
        """
        self._rect = _pygame.Rect(0, 0, area_width, area_height)
        self._world = world
        self._scrollbars = []
        self._scrollbar_positions = tuple(set(scrollbars))  # Ensure unique
        self._scrollbar_thick = scrollbar_thick
        self._bg_surface = None
        if area_color:
            self._bg_surface = _pygame.Surface((area_width, area_height),
                                               _pygame.SRCALPHA, 32)  # lgtm [py/call/wrong-arguments]
            self._bg_surface.fill(area_color)

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

        if self._bg_surface:
            surface.blit(self._bg_surface, (self._rect.x, self._rect.y))

        offsets = self.get_offsets()
        for sbar in self._scrollbars:
            if sbar.get_orientation() == _locals.ORIENTATION_HORIZONTAL:
                if self.get_hidden_width():
                    sbar.draw(surface)  # Display scrollbar
            else:
                if self.get_hidden_height():
                    sbar.draw(surface)  # Display scrollbar

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

    def get_offsets(self):
        """
        Return the offset introduced by the scrollbars in the world.
        """
        offsets = [0, 0]
        for sbar in self._scrollbars:
            if sbar.get_orientation() == _locals.ORIENTATION_HORIZONTAL:
                if self.get_hidden_width():
                    offsets[0] = sbar.get_value()
            else:
                if self.get_hidden_height():
                    offsets[1] = sbar.get_value()
        return offsets

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

        # No scrollbar: area is enought large to display world
        if not self._world or (self._world.get_width() <= self._rect.width
                               and self._world.get_height() <= self._rect.height):
            return rect

         # All scrollbars: the world is too large
        if self._world.get_height() > self._rect.height\
           and self._world.get_width() > self._rect.width:
            if _locals.POSITION_WEST in self._scrollbar_positions:
                rect.left += self._scrollbar_thick
                rect.width -= self._scrollbar_thick
            if _locals.POSITION_EAST in self._scrollbar_positions:
                rect.width -= self._scrollbar_thick
            if _locals.POSITION_NORTH in self._scrollbar_positions:
                rect.top += self._scrollbar_thick
                rect.height -= self._scrollbar_thick
            if _locals.POSITION_SOUTH in self._scrollbar_positions:
                rect.height -= self._scrollbar_thick
            return rect

        # Calculate the maximum variations introduces by the scrollbars
        bars_total_width = 0
        bars_total_height = 0
        if _locals.POSITION_NORTH in self._scrollbar_positions:
            bars_total_height += self._scrollbar_thick
        if _locals.POSITION_SOUTH in self._scrollbar_positions:
            bars_total_height += self._scrollbar_thick
        if _locals.POSITION_WEST in self._scrollbar_positions:
            bars_total_width += self._scrollbar_thick
        if _locals.POSITION_EAST in self._scrollbar_positions:
            bars_total_width += self._scrollbar_thick

        if self._world.get_height() > self._rect.height:
            if _locals.POSITION_WEST in self._scrollbar_positions:
                rect.left += self._scrollbar_thick
                rect.width -= self._scrollbar_thick
            if _locals.POSITION_EAST in self._scrollbar_positions:
                rect.width -= self._scrollbar_thick
            if self._world.get_width() > self._rect.width - bars_total_width:
                if _locals.POSITION_NORTH in self._scrollbar_positions:
                    rect.top += self._scrollbar_thick
                    rect.height -= self._scrollbar_thick
                if _locals.POSITION_SOUTH in self._scrollbar_positions:
                    rect.height -= self._scrollbar_thick

        if self._world.get_width() > self._rect.width:
            if _locals.POSITION_NORTH in self._scrollbar_positions:
                rect.top += self._scrollbar_thick
                rect.height -= self._scrollbar_thick
            if _locals.POSITION_SOUTH in self._scrollbar_positions:
                rect.height -= self._scrollbar_thick
            if self._world.get_height() > self._rect.height - bars_total_height:
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

    def scroll_to_rect(self, rect, margin=10):
        """
        Ensure that the given rect is in the viewable area.

        :param rect: Rect in the world surface reference
        :type rect: pygame.Rect
        :param margin: Extra margin around the rect
        :type margin: int
        """
        real_rect = self.to_real_position(rect)
        if self._view_rect.topleft[0] < real_rect.topleft[0]\
                and self._view_rect.topleft[1] < real_rect.topleft[1]\
                and self._view_rect.bottomright[0] > real_rect.bottomright[0]\
                and self._view_rect.bottomright[1] > real_rect.bottomright[1]:
            return  # rect is in viewable area

        for sbar in self._scrollbars:
            if sbar.get_orientation() == _locals.ORIENTATION_HORIZONTAL and self.get_hidden_width():
                shortest_move = min(real_rect.left - margin - self._view_rect.left,
                                    real_rect.right + margin - self._view_rect.right, key=abs)
                value = min(sbar.get_maximum(), sbar.get_value() + shortest_move)
                value = max(sbar.get_minimum(), value)
                sbar.set_value(value)
            if sbar.get_orientation() == _locals.ORIENTATION_VERTICAL and self.get_hidden_height():
                shortest_move = min(real_rect.bottom + margin - self._view_rect.bottom,
                                    real_rect.top - margin - self._view_rect.top, key=abs)
                value = min(sbar.get_maximum(), sbar.get_value() + shortest_move)
                value = max(sbar.get_minimum(), value)
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

    def to_real_position(self, virtual):
        """
        Return the real position/Rect according to the scroll area origin
        of a position/Rect in the world surface reference.

        :param virtual: position/Rect in the world surface reference
        :type virtual: pygame.Rect, tuple, list
        """
        assert isinstance(virtual, (_pygame.Rect, tuple, list))
        offsets = self.get_offsets()

        if isinstance(virtual, _pygame.Rect):
            rect = _pygame.Rect(virtual)
            rect.x = self._rect.x + virtual.x - offsets[0]
            rect.y = self._rect.y + virtual.y - offsets[1]
            return rect

        x_coord = self._rect.x + virtual[0] - offsets[0]
        y_coord = self._rect.y + virtual[1] - offsets[1]
        return x_coord, y_coord

    def to_world_position(self, real):
        """
        Return the position/Rect in the world surface reference
        of a real position/Rect according to the scroll area origin.

        :param real: position/Rect according scroll area origin
        :type real: pygame.Rect, tuple, list
        """
        assert isinstance(real, (_pygame.Rect, tuple, list))
        offsets = self.get_offsets()

        if isinstance(real, _pygame.Rect):
            rect = _pygame.Rect(real)
            rect.x = real.x - self._rect.x + offsets[0]
            rect.y = real.y - self._rect.y + offsets[1]
            return rect

        x_coord = real[0] - self._rect.x + offsets[0]
        y_coord = real[1] - self._rect.y + offsets[1]
        return x_coord, y_coord

    def update(self, events):
        """
        Called by end user to update scroll state.
        """
        for sbar in self._scrollbars:
            sbar.update(events)
