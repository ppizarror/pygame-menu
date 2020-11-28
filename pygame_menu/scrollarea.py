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

import pygame
import pygame_menu.baseimage as _baseimage
import pygame_menu.locals as _locals
from pygame_menu.utils import make_surface, assert_color, assert_position
from pygame_menu.widgets import ScrollBar


class ScrollArea(object):
    """
    The ScrollArea class provides a scrolling view managing up to 4 scroll bars.

    A scroll area is used to display the contents of a child surface (``world``).
    If the surface exceeds the size of the drawing surface, the view provide
    scroll bars so that the entire area of the child surface can be viewed.

    :param area_width: Width of scrollable area (px)
    :type area_width: int, float
    :param area_height: Height of scrollable area (px)
    :type area_height: int, float
    :param area_color: Background color, it can be a color or an image
    :type area_color: tuple, list, :py:class:`pygame_menu.baseimage.BaseImage`, None
    :param extend_x: Px to extend the surface in yxaxis (px) from left
    :type extend_x: int, float
    :param extend_y: Px to extend the surface in y axis (px) from top
    :type extend_y: int, float
    :param scrollbar_color: Scrollbars color
    :type scrollbar_color: tuple, list
    :param scrollbar_slider_color: Color of the sliders
    :type scrollbar_slider_color: tuple, list
    :param scrollbar_slider_pad: Space between slider and scrollbars borders
    :type scrollbar_slider_pad: int, float
    :param scrollbar_thick: Scrollbars thickness
    :type scrollbar_thick: int, float
    :param scrollbars: Positions of the scrollbars
    :type scrollbars: tuple, list
    :param shadow: Indicate if a shadow is drawn on each scrollbar
    :type shadow: bool
    :param shadow_color: Color of the shadow
    :type shadow_color: tuple, list
    :param shadow_offset: Offset of shadow
    :type shadow_offset: int, float
    :param shadow_position: Position of shadow
    :type shadow_position: str
    :param world: Surface to draw and scroll
    :type world: :py:class:`pygame.Surface`, None
    """

    def __init__(self,
                 area_width,
                 area_height,
                 area_color=None,
                 extend_x=0,
                 extend_y=0,
                 scrollbar_color=(235, 235, 235),
                 scrollbar_slider_color=(200, 200, 200),
                 scrollbar_slider_pad=0,
                 scrollbar_thick=20,
                 scrollbars=(_locals.POSITION_SOUTH, _locals.POSITION_EAST),
                 shadow=False,
                 shadow_color=(0, 0, 0),
                 shadow_offset=2,
                 shadow_position=_locals.POSITION_SOUTHEAST,
                 world=None,
                 ):
        assert isinstance(area_width, (int, float))
        assert isinstance(area_height, (int, float))
        assert isinstance(scrollbar_slider_pad, (int, float))
        assert isinstance(scrollbar_thick, (int, float))
        assert isinstance(shadow, bool)
        assert isinstance(shadow_offset, (int, float))

        assert_color(scrollbar_color)
        assert_color(scrollbar_slider_color)
        assert_color(shadow_color)
        assert_position(shadow_position)

        assert area_width > 0 and area_height > 0, \
            'area size must be greater than zero'

        self._rect = pygame.Rect(0, 0, int(area_width), int(area_height))
        self._world = world  # type: pygame.Surface
        self._scrollbars = []
        self._scrollbar_positions = tuple(set(scrollbars))  # Ensure unique
        self._scrollbar_thick = scrollbar_thick
        self._bg_surface = None

        self._extend_x = extend_x
        self._extend_y = extend_y

        if area_color:
            self._bg_surface = make_surface(width=area_width + extend_x,
                                            height=area_height + self._extend_y)
            if isinstance(area_color, _baseimage.BaseImage):
                area_color.draw(surface=self._bg_surface, area=self._bg_surface.get_rect())
            else:
                self._bg_surface.fill(area_color)

        self._view_rect = self.get_view_rect()

        for pos in self._scrollbar_positions:  # type:str
            assert_position(pos)
            if pos == _locals.POSITION_EAST or pos == _locals.POSITION_WEST:
                sbar = ScrollBar(self._view_rect.height, (0, max(1, self.get_hidden_height())),
                                 orientation=_locals.ORIENTATION_VERTICAL,
                                 slider_pad=scrollbar_slider_pad,
                                 slider_color=scrollbar_slider_color,
                                 page_ctrl_thick=scrollbar_thick,
                                 page_ctrl_color=scrollbar_color,
                                 onchange=self._on_vertical_scroll)
            else:
                sbar = ScrollBar(self._view_rect.width, (0, max(1, self.get_hidden_width())),
                                 slider_pad=scrollbar_slider_pad,
                                 slider_color=scrollbar_slider_color,
                                 page_ctrl_thick=scrollbar_thick,
                                 page_ctrl_color=scrollbar_color,
                                 onchange=self._on_horizontal_scroll)
            sbar.set_shadow(enabled=shadow,
                            color=shadow_color,
                            position=shadow_position,
                            offset=shadow_offset)
            sbar.set_controls(joystick=False)

            self._scrollbars.append(sbar)

        self._apply_size_changes()

        # Menu reference
        self._menu = None

    def _apply_size_changes(self):
        """
        Apply size changes to scrollbar.

        :return: None
        """
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

            if pos in (_locals.POSITION_NORTH, _locals.POSITION_SOUTH) \
                    and self.get_hidden_width() != sbar.get_maximum() \
                    and self.get_hidden_width() != 0:
                sbar.set_length(self._view_rect.width)
                sbar.set_maximum(self.get_hidden_width())
                sbar.set_page_step(self._view_rect.width * self.get_hidden_width() /
                                   (self._view_rect.width + self.get_hidden_width()))

            elif pos in (_locals.POSITION_EAST, _locals.POSITION_WEST) \
                    and self.get_hidden_height() != sbar.get_maximum() \
                    and self.get_hidden_height() != 0:
                sbar.set_length(self._view_rect.height)
                sbar.set_maximum(self.get_hidden_height())
                sbar.set_page_step(self._view_rect.height * self.get_hidden_height() /
                                   (self._view_rect.height + self.get_hidden_height()))

    def draw(self, surface):
        """
        Called by end user to draw state to the surface.

        :param surface: Surface to render the area
        :type surface: :py:class:`pygame.Surface`
        :return: None
        """
        if not self._world:
            return

        if self._bg_surface:
            surface.blit(self._bg_surface, (self._rect.x - self._extend_x, self._rect.y - self._extend_y))

        offsets = self.get_offsets()
        for sbar in self._scrollbars:  # type: ScrollBar
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

        :return: None
        """
        if not self._world:
            return 0
        return max(0, self._world.get_width() - self._view_rect.width)

    def get_hidden_height(self):
        """
        Return the total height out of the bounds of the the viewable area.
        Zero is returned if the world height is lower than the viewable area.

        :return: None
        """
        if not self._world:
            return 0
        return max(0, self._world.get_height() - self._view_rect.height)

    def get_offsets(self):
        """
        Return the offset introduced by the scrollbars in the world.

        :return: None
        """
        offsets = [0, 0]
        for sbar in self._scrollbars:  # type: ScrollBar
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

        :return: Pygame.Rect object
        :rtype: :py:class:`pygame.Rect`
        """
        return self._rect.copy()

    def get_scrollbar_thickness(self, orientation):
        """
        Return the scroll thickness of the area. If it's hidden return zero.

        :param orientation: Orientation of the scroll
        :type orientation: str
        :return: Thickness in px
        :rtype: int
        """
        if orientation == _locals.ORIENTATION_HORIZONTAL:
            return self._rect.height - self._view_rect.height
        elif orientation == _locals.ORIENTATION_VERTICAL:
            return self._rect.width - self._view_rect.width
        return 0

    def get_view_rect(self):
        """
        Subtract width of scrollbars from area with the given size and return
        the viewable area.

        The viewable area depends on the world size, because scroll bars may
        or may not be displayed.

        :return: None
        """
        rect = pygame.Rect(self._rect)

        # No scrollbar: area is large enough to display world
        if not self._world or (self._world.get_width() <= self._rect.width
                               and self._world.get_height() <= self._rect.height):
            return rect

        # All scrollbars: the world is too large
        if self._world.get_height() > self._rect.height \
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

    def get_world_size(self):
        """
        Return the world size.

        :return: Width, height in pixels
        :rtype: tuple
        """
        if self._world is None:
            return 0, 0
        return self._world.get_width(), self._world.get_height()

    def _on_horizontal_scroll(self, value):
        """
        Call when a horizontal scroll bar as changed to update the
        position of the opposite one if it exists.

        :param value: New position of the slider
        :type value: float
        :return: None
        """
        for sbar in self._scrollbars:  # type: ScrollBar
            if sbar.get_orientation() == _locals.ORIENTATION_HORIZONTAL \
                    and self.get_hidden_width() != 0 \
                    and sbar.get_value() != value:
                sbar.set_value(value)

    def _on_vertical_scroll(self, value):
        """
        Call when a vertical scroll bar as changed to update the
        position of the opposite one if it exists.

        :param value: New position of the slider
        :type value: float
        :return: None
        """
        for sbar in self._scrollbars:  # type: ScrollBar
            if sbar.get_orientation() == _locals.ORIENTATION_VERTICAL \
                    and self.get_hidden_height() != 0 \
                    and sbar.get_value() != value:
                sbar.set_value(value)

    def scroll_to_rect(self, rect, margin=10.0):
        """
        Ensure that the given rect is in the viewable area.

        :param rect: Rect in the world surface reference
        :type rect: :py:class:`pygame.Rect`
        :param margin: Extra margin around the rect
        :type margin: int, float
        :return: None
        """
        assert isinstance(margin, (int, float))
        real_rect = self.to_real_position(rect)
        if self._view_rect.topleft[0] < real_rect.topleft[0] \
                and self._view_rect.topleft[1] < real_rect.topleft[1] \
                and self._view_rect.bottomright[0] > real_rect.bottomright[0] \
                and self._view_rect.bottomright[1] > real_rect.bottomright[1]:
            return  # rect is in viewable area

        for sbar in self._scrollbars:  # type: ScrollBar
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

        :param surface: New world surface
        :type surface: :py:class:`pygame.Surface`
        :return: None
        """
        self._world = surface
        self._apply_size_changes()

    def to_real_position(self, virtual, visible=False):
        """
        Return the real position/Rect according to the scroll area origin
        of a position/Rect in the world surface reference.

        :param virtual: Position/Rect in the world surface reference
        :type virtual: :py:class:`pygame.Rect`, tuple, list
        :param visible: If a rect is given, return only the visible width/height
        :type visible: bool
        :return: Real rect or real position
        :rtype: :py:class:`pygame.Rect`, tuple
        """
        assert isinstance(virtual, (pygame.Rect, tuple, list))
        offsets = self.get_offsets()

        if isinstance(virtual, pygame.Rect):
            rect = pygame.Rect(virtual)
            rect.x = self._rect.x + virtual.x - offsets[0]
            rect.y = self._rect.y + virtual.y - offsets[1]
            if visible:
                return self._view_rect.clip(rect)  # Visible width and height
            return rect

        x_coord = self._rect.x + virtual[0] - offsets[0]
        y_coord = self._rect.y + virtual[1] - offsets[1]
        return x_coord, y_coord

    def to_world_position(self, real):
        """
        Return the position/Rect in the world surface reference
        of a real position/Rect according to the scroll area origin.

        :param real: Position/Rect according scroll area origin
        :type real: :py:class:`pygame.Rect`, tuple, list
        :return: Rect in world or position in world
        :rtype: :py:class:`pygame.Rect`, tuple
        """
        assert isinstance(real, (pygame.Rect, tuple, list))
        offsets = self.get_offsets()

        if isinstance(real, pygame.Rect):
            rect = pygame.Rect(real)
            rect.x = real.x - self._rect.x + offsets[0]
            rect.y = real.y - self._rect.y + offsets[1]
            return rect

        x_coord = real[0] - self._rect.x + offsets[0]
        y_coord = real[1] - self._rect.y + offsets[1]
        return x_coord, y_coord

    def is_scrolling(self):
        """
        Return true if the user is scrolling.

        :return: True if user scrolls
        :rtype: bool
        """
        scroll = False
        for sbar in self._scrollbars:  # type: ScrollBar
            scroll = scroll or sbar.scrolling
        return scroll

    def update(self, events):
        """
        Called by end user to update scroll state.

        :param events: List of pygame events
        :type events: list
        :return: True if updated
        :rtype: bool
        """
        updated = [0, 0]
        for sbar in self._scrollbars:  # type: ScrollBar
            if sbar.get_orientation() == _locals.ORIENTATION_HORIZONTAL and not updated[0]:
                updated[0] = sbar.update(events)
            elif sbar.get_orientation() == _locals.ORIENTATION_VERTICAL and not updated[1]:
                updated[1] = sbar.update(events)
        return updated[0] or updated[1]

    def set_menu(self, menu):
        """
        Set the menu reference.

        :param menu: Menu object
        :type menu: :py:class:`pygame_menu.Menu`
        :return: None
        """
        self._menu = menu
        for sbar in self._scrollbars:  # type: ScrollBar
            sbar.set_menu(menu)

    def get_menu(self):
        """
        Return the menu reference (if exists).

        :return: Menu reference
        :rtype: :py:class:`pygame_menu.Menu`, None
        """
        return self._menu

    def collide(self, widget, event):
        """
        If user event collides a widget within the scroll area respect to the relative position.

        :param widget: Widget
        :type widget: :py:class:`pygame_menu.widgets.core.widget.Widget`
        :param event: Pygame event
        :type event: :py:class:`pygame.event.Event`
        :return: True if collide
        :rtype: bool
        """
        if event.type == pygame.FINGERDOWN or event.type == pygame.FINGERUP or event.type == pygame.FINGERMOTION:
            display_size = self._menu.get_window_size()
            finger_pos = (event.x * display_size[0], event.y * display_size[1])
            return self.to_real_position(widget.get_rect()).collidepoint(finger_pos)
        else:
            return self.to_real_position(widget.get_rect()).collidepoint(*event.pos)
