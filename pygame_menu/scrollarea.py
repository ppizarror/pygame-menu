"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SCROLLAREA
ScrollArea class to manage scrolling in Menu.

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

__all__ = ['ScrollArea', 'get_scrollbars_from_position']

import pygame
import pygame_menu
import pygame_menu.locals as _locals
from pygame_menu._decorator import Decorator
from pygame_menu.utils import make_surface, assert_color, assert_position
from pygame_menu.widgets import ScrollBar, MenuBar

from pygame_menu._types import ColorType, Union, NumberType, Tuple, List, Dict, \
    Tuple2NumberType, Optional, Tuple2IntType


def get_scrollbars_from_position(position: str) -> Union[str, Tuple[str, str], Tuple[str, str, str, str]]:
    """
    Return the scrollbars from the given position.
    Raises ``ValueError`` if invalid position.

    :param position: Position
    :return: Scrollbars
    """
    if position in (_locals.POSITION_EAST, _locals.POSITION_EAST, _locals.POSITION_WEST, _locals.POSITION_NORTH):
        return position
    elif position == _locals.POSITION_NORTHWEST:
        return _locals.POSITION_NORTH, _locals.POSITION_WEST
    elif position == _locals.POSITION_NORTHEAST:
        return _locals.POSITION_NORTH, _locals.POSITION_EAST
    elif position == _locals.POSITION_SOUTHWEST:
        return _locals.POSITION_SOUTH, _locals.POSITION_WEST
    elif position == _locals.POSITION_SOUTHEAST:
        return _locals.POSITION_SOUTH, _locals.POSITION_EAST
    elif position == _locals.SCROLLAREA_POSITION_FULL:
        return _locals.POSITION_SOUTH, _locals.POSITION_EAST, _locals.POSITION_WEST, _locals.POSITION_NORTH
    elif position == _locals.SCROLLAREA_POSITION_BOTH_HORIZONTAL:
        return _locals.POSITION_SOUTH, _locals.POSITION_NORTH
    elif position == _locals.SCROLLAREA_POSITION_BOTH_VERTICAL:
        return _locals.POSITION_EAST, _locals.POSITION_WEST
    elif position == _locals.POSITION_CENTER:
        raise ValueError('cannot init strollbars from center position')
    else:
        raise ValueError('unknown ScrollArea position')


SCROLL_VERTICAL = _locals.ORIENTATION_VERTICAL
SCROLL_HORIZONTAL = _locals.ORIENTATION_HORIZONTAL


class ScrollArea(object):
    """
    The ScrollArea class provides a scrolling view managing up to 4 scroll bars.

    A scroll area is used to display the contents of a child surface (``world``).
    If the surface exceeds the size of the drawing surface, the view provide
    scroll bars so that the entire area of the child surface can be viewed.

    .. note::

        See :py:mod:`pygame_menu.locals` for valid ``scrollbars`` and
        ``shadow_position`` values.

    .. note::

        ScrollArea cannot be copied or deepcopied.

    :param area_width: Width of scrollable area (px)
    :param area_height: Height of scrollable area (px)
    :param area_color: Background color, it can be a color or an image
    :param cursor: Scrollbar cursors
    :param menubar: Menubar for style compatibility
    :param extend_x: Px to extend the surface in x axis (px) from left
    :param extend_y: Px to extend the surface in y axis (px) from top
    :param scrollbar_color: Scrollbars color
    :param scrollbar_slider_color: Color of the sliders
    :param scrollbar_slider_pad: Space between slider and scrollbars borders
    :param scrollbar_thick: Scrollbars thickness
    :param scrollbars: Positions of the scrollbars
    :param shadow: Indicate if a shadow is drawn on each scrollbar
    :param shadow_color: Color of the shadow
    :param shadow_offset: Offset of shadow
    :param shadow_position: Position of shadow
    :param world: Surface to draw and scroll
    """
    _bg_surface: Optional['pygame.Surface']
    _decorator: 'Decorator'
    _extend_x: int
    _extend_y: int
    _menu: Optional['pygame_menu.Menu']
    _menubar: 'pygame_menu.widgets.MenuBar'
    _rect: 'pygame.Rect'
    _scrollbar_positions: Tuple[str, ...]
    _scrollbar_thick: NumberType
    _scrollbars: List['ScrollBar']
    _view_rect: 'pygame.Rect'
    _world: 'pygame.Surface'

    def __init__(self,
                 area_width: int,
                 area_height: int,
                 area_color: Optional[Union[ColorType, 'pygame_menu.BaseImage']] = None,
                 cursor: Optional[Union[int, 'pygame.cursors.Cursor']] = None,
                 extend_x: int = 0,
                 extend_y: int = 0,
                 menubar: Optional['MenuBar'] = None,
                 scrollbar_color: ColorType = (235, 235, 235),
                 scrollbar_slider_color: ColorType = (200, 200, 200),
                 scrollbar_slider_pad: NumberType = 0,
                 scrollbar_thick: NumberType = 20,
                 scrollbars: Union[str, Tuple[str, ...]] = get_scrollbars_from_position(_locals.POSITION_SOUTHEAST),
                 shadow: bool = False,
                 shadow_color: ColorType = (0, 0, 0),
                 shadow_offset: NumberType = 2,
                 shadow_position: str = _locals.POSITION_SOUTHEAST,
                 world: Optional['pygame.Surface'] = None
                 ) -> None:
        assert isinstance(area_width, int)
        assert isinstance(area_height, int)
        assert isinstance(scrollbar_slider_pad, (int, float))
        assert isinstance(scrollbar_thick, (int, float))
        assert isinstance(shadow, bool)
        assert isinstance(shadow_offset, (int, float))
        assert isinstance(world, (pygame.Surface, type(None)))

        assert_color(scrollbar_color)
        assert_color(scrollbar_slider_color)
        assert_color(shadow_color)
        assert_position(shadow_position)

        assert area_width > 0 and area_height > 0, \
            'area size must be greater than zero'

        self._bg_surface = None
        self._decorator = Decorator(self)
        self._rect = pygame.Rect(0, 0, int(area_width), int(area_height))
        self._scrollbar_positions = tuple(set(scrollbars))  # Ensure unique
        self._scrollbar_thick = scrollbar_thick
        self._scrollbars = []
        self._world = world

        self._extend_x = extend_x
        self._extend_y = extend_y
        self._menubar = menubar

        if area_color:
            self._bg_surface = make_surface(width=area_width + extend_x,
                                            height=area_height + self._extend_y)
            if isinstance(area_color, pygame_menu.BaseImage):
                area_color.draw(surface=self._bg_surface, area=self._bg_surface.get_rect())
            else:
                self._bg_surface.fill(area_color)

        self._view_rect = self.get_view_rect()

        for pos in self._scrollbar_positions:
            assert_position(pos)

            if pos == _locals.POSITION_EAST or pos == _locals.POSITION_WEST:
                sbar = ScrollBar(
                    length=self._view_rect.height,
                    values_range=(0, max(1, self.get_hidden_height())),
                    orientation=SCROLL_VERTICAL,
                    slider_pad=scrollbar_slider_pad,
                    slider_color=scrollbar_slider_color,
                    page_ctrl_thick=scrollbar_thick,
                    page_ctrl_color=scrollbar_color,
                    onchange=self._on_vertical_scroll
                )
            else:
                sbar = ScrollBar(
                    length=self._view_rect.width,
                    values_range=(0, max(1, self.get_hidden_width())),
                    slider_pad=scrollbar_slider_pad,
                    slider_color=scrollbar_slider_color,
                    page_ctrl_thick=scrollbar_thick,
                    page_ctrl_color=scrollbar_color,
                    onchange=self._on_horizontal_scroll
                )
            sbar.set_shadow(
                enabled=shadow,
                color=shadow_color,
                position=shadow_position,
                offset=shadow_offset
            )
            sbar.set_controls(joystick=False)
            sbar.set_cursor(cursor=cursor)

            self._scrollbars.append(sbar)

        self._apply_size_changes()

        # Menu reference
        self._menu = None

    def __copy__(self) -> 'ScrollArea':
        """
        Copy method.

        :return: Raises copy exception
        """
        raise _ScrollAreaCopyException('ScrollArea class cannot be copied')

    def __deepcopy__(self, memodict: Dict) -> 'ScrollArea':
        """
        Deepcopy method.

        :param memodict: Memo dict
        :return: Raises copy exception
        """
        raise _ScrollAreaCopyException('ScrollArea class cannot be copied')

    def force_menu_surface_update(self) -> 'ScrollArea':
        """
        Forces menu surface update after next rendering call.

        .. note ::

            This method is expensive, as menu surface update forces re-rendering of
            all widgets (because them can change in size, position, etc...).

        :return: Self reference
        """
        if self._menu is not None:
            self._menu._widgets_surface_need_update = True
        return self

    def force_menu_surface_cache_update(self) -> 'ScrollArea':
        """
        Forces menu surface cache to update after next drawing call.
        This also updates widget decoration.

        .. note::

            This method only updates the surface cache, without forcing re-rendering
            of all Menu widgets as :py:meth:`pygame_menu.widgets.core.widget.Widget.force_menu_surface_update`
            does.

        :return: Self reference
        """
        if self._menu is not None:
            self._menu._widget_surface_cache_need_update = True
            self._decorator.force_cache_update()
        return self

    def _apply_size_changes(self) -> None:
        """
        Apply size changes to scrollbar.

        :return: None
        """
        self._view_rect = self.get_view_rect()
        for sbar in self._scrollbars:
            pos = self._scrollbar_positions[self._scrollbars.index(sbar)]

            dsize, dx, dy = 0, 0, 0
            if self._menubar is not None:
                dsize, (dx, dy) = self._menubar.get_scrollbar_style_change(pos)

            if pos == _locals.POSITION_WEST:
                sbar.set_position(self._view_rect.left - self._scrollbar_thick + dx, self._view_rect.top + dy)
            elif pos == _locals.POSITION_EAST:
                sbar.set_position(self._view_rect.right + dx, self._view_rect.top + dy)
            elif pos == _locals.POSITION_NORTH:
                sbar.set_position(self._view_rect.left + dx, self._view_rect.top - self._scrollbar_thick + dy)
            elif pos == _locals.POSITION_SOUTH:  # South
                sbar.set_position(self._view_rect.left + dx, self._view_rect.bottom + dy)
            elif pos == _locals.POSITION_CENTER:
                raise ValueError('center position cannot be applied to scrollbar')
            else:
                raise ValueError('unknown position')

            if pos in (_locals.POSITION_NORTH, _locals.POSITION_SOUTH) \
                    and self.get_hidden_width() != sbar.get_maximum() \
                    and self.get_hidden_width() != 0:
                sbar.set_length(self._view_rect.width + dsize)
                sbar.set_maximum(self.get_hidden_width())
                sbar.set_page_step(self._view_rect.width * self.get_hidden_width() /
                                   (self._view_rect.width + self.get_hidden_width()))

            elif pos in (_locals.POSITION_EAST, _locals.POSITION_WEST) \
                    and self.get_hidden_height() != sbar.get_maximum() \
                    and self.get_hidden_height() != 0:
                sbar.set_length(self._view_rect.height + dsize)
                sbar.set_maximum(self.get_hidden_height())
                sbar.set_page_step(self._view_rect.height * self.get_hidden_height() /
                                   (self._view_rect.height + self.get_hidden_height()))

    def draw(self, surface: 'pygame.Surface') -> 'ScrollArea':
        """
        Draw the scrollarea.

        :param surface: Surface to render the area
        :return: Self reference
        """
        if not self._world:
            return self

        # Background surface already has previous decorators
        if self._bg_surface:
            surface.blit(self._bg_surface, (self._rect.x - self._extend_x, self._rect.y - self._extend_y))

        for sbar in self._scrollbars:
            if sbar.get_orientation() == SCROLL_HORIZONTAL:
                if self.get_hidden_width():
                    sbar.draw(surface)
            else:
                if self.get_hidden_height():
                    sbar.draw(surface)

        # noinspection PyTypeChecker
        surface.blit(self._world, self._view_rect.topleft, (self.get_offsets(), self._view_rect.size))
        self._decorator.draw_post(surface)
        return self

    def get_hidden_width(self) -> int:
        """
        Return the total width out of the bounds of the viewable area.
        Zero is returned if the world width is lower than the viewable area.

        :return: Hidden width (px)
        """
        if not self._world:
            return 0
        return int(max(0, self._world.get_width() - self._view_rect.width))

    def get_hidden_height(self) -> int:
        """
        Return the total height out of the bounds of the viewable area.
        Zero is returned if the world height is lower than the viewable area.

        :return: Hidden height (px)
        """
        if not self._world:
            return 0
        return int(max(0, self._world.get_height() - self._view_rect.height))

    def get_offsets(self) -> Tuple2IntType:
        """
        Return the offset introduced by the scrollbars in the world.

        :return: ScrollArea offset *(x, y)*
        """
        offsets = [0, 0]
        for sbar in self._scrollbars:
            if sbar.get_orientation() == SCROLL_HORIZONTAL:
                if self.get_hidden_width():
                    offsets[0] = sbar.get_value()
            else:
                if self.get_hidden_height():
                    offsets[1] = sbar.get_value()
        return offsets[0], offsets[1]

    def get_rect(self) -> 'pygame.Rect':
        """
        Return the :py:class:`pygame.Rect` object of the ScrollArea.

        :return: Pygame.Rect object
        """
        return self._rect.copy()

    def get_scrollbar_thickness(self, orientation: str, real: bool = False) -> int:
        """
        Return the scroll thickness of the area. If it's hidden return zero.

        :param orientation: Orientation of the scroll
        :param real: If ``True`` returns the real thickness depending if it is shown or not
        :return: Thickness (px)
        """
        assert isinstance(real, bool)
        if real:
            for sbar in self._scrollbars:
                if sbar.get_orientation() == orientation:
                    return sbar.get_thickness()
        if orientation == SCROLL_HORIZONTAL:
            return int(self._rect.height - self._view_rect.height)
        elif orientation == SCROLL_VERTICAL:
            return int(self._rect.width - self._view_rect.width)
        return 0

    def get_view_rect(self) -> 'pygame.Rect':
        """
        Subtract width of scrollbars from area with the given size and return
        the viewable area.

        The viewable area depends on the world size, because scroll bars may
        or may not be displayed.

        :return: View rect object
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

    def get_world_size(self) -> Tuple2IntType:
        """
        Return the world size.

        :return: Width, height in pixels
        """
        if self._world is None:
            return 0, 0
        return self._world.get_width(), self._world.get_height()

    def _on_horizontal_scroll(self, value: NumberType) -> None:
        """
        Call when a horizontal scroll bar as changed to update the
        position of the opposite one if it exists.

        :param value: New position of the slider
        :return: None
        """
        for sbar in self._scrollbars:
            if sbar.get_orientation() == SCROLL_HORIZONTAL \
                    and self.get_hidden_width() != 0 \
                    and sbar.get_value() != value:
                sbar.set_value(value)

    def _on_vertical_scroll(self, value: NumberType) -> None:
        """
        Call when a vertical scroll bar as changed to update the
        position of the opposite one if it exists.

        :param value: New position of the slider
        :return: None
        """
        for sbar in self._scrollbars:
            if sbar.get_orientation() == SCROLL_VERTICAL \
                    and self.get_hidden_height() != 0 \
                    and sbar.get_value() != value:
                sbar.set_value(value)

    # noinspection PyTypeChecker
    def scroll_to_rect(self, rect: 'pygame.Rect', margin: NumberType = 10) -> bool:
        """
        Ensure that the given rect is in the viewable area.

        :param rect: Rect in the world surface reference
        :param margin: Extra margin around the rect (px)
        :return: Scrollarea scrolled to rect. If ``False`` the rect was already inside the visible area
        """
        assert isinstance(margin, (int, float))
        real_rect = self.to_real_position(rect)

        # Check rect is in viewable area
        sx = self.get_scrollbar_thickness(SCROLL_VERTICAL)
        sy = self.get_scrollbar_thickness(SCROLL_HORIZONTAL)
        if self._view_rect.topleft[0] <= real_rect.topleft[0] + sx \
                and self._view_rect.topleft[1] <= real_rect.topleft[1] + sy \
                and self._view_rect.bottomright[0] + sx >= real_rect.bottomright[0] \
                and self._view_rect.bottomright[1] + sy >= real_rect.bottomright[1]:
            return False

        for sbar in self._scrollbars:
            if sbar.get_orientation() == SCROLL_HORIZONTAL and self.get_hidden_width():
                shortest_move = min(real_rect.left - margin - self._view_rect.left,
                                    real_rect.right + margin - self._view_rect.right, key=abs)
                value = min(sbar.get_maximum(), sbar.get_value() + shortest_move)
                value = max(sbar.get_minimum(), value)
                sbar.set_value(value)
            if sbar.get_orientation() == SCROLL_VERTICAL and self.get_hidden_height():
                shortest_move = min(real_rect.bottom + margin - self._view_rect.bottom,
                                    real_rect.top - margin - self._view_rect.top, key=abs)
                value = min(sbar.get_maximum(), sbar.get_value() + shortest_move)
                value = max(sbar.get_minimum(), value)
                sbar.set_value(value)
        return True

    def set_position(self, posx: int, posy: int) -> 'ScrollArea':
        """
        Set the position.

        :param posx: X position
        :param posy: Y position
        :return: Self reference
        """
        self._rect.x = posx
        self._rect.y = posy
        self._apply_size_changes()
        return self

    def set_world(self, surface: 'pygame.Surface') -> 'ScrollArea':
        """
        Update the scrolled surface.

        :param surface: New world surface
        :return: Self reference
        """
        self._world = surface
        self._apply_size_changes()
        return self

    def to_real_position(self, virtual: Union['pygame.Rect', Tuple2NumberType], visible: bool = False
                         ) -> Union['pygame.Rect', Tuple2IntType]:
        """
        Return the real position/Rect according to the scroll area origin
        of a position/Rect in the world surface reference.

        :param virtual: Position/Rect in the world surface reference
        :param visible: If a ``virtual`` is Rect object, return only the visible width/height
        :return: Real rect or real position
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
        return int(x_coord), int(y_coord)

    def to_world_position(self, real: Union['pygame.Rect', Tuple2NumberType]
                          ) -> Union['pygame.Rect', Tuple2IntType]:
        """
        Return the position/Rect in the world surface reference
        of a real position/Rect according to the scroll area origin.

        :param real: Position/Rect according scroll area origin
        :return: Rect in world or position in world
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
        return int(x_coord), int(y_coord)

    def is_scrolling(self) -> bool:
        """
        Return ``True`` if the user is scrolling.

        :return: ``True`` if user scrolls
        """
        scroll = False
        for sbar in self._scrollbars:
            scroll = scroll or sbar.scrolling
        return scroll

    def update(self, events: List['pygame.event.Event']) -> bool:
        """
        Called by end user to update scroll state.

        :param events: List of pygame events
        :return: ``True`` if updated
        """
        updated = [0, 0]
        for sbar in self._scrollbars:
            if self.get_hidden_width() and sbar.get_orientation() == SCROLL_HORIZONTAL and not updated[0]:
                updated[0] = sbar.update(events)
            elif self.get_hidden_height() and sbar.get_orientation() == SCROLL_VERTICAL and not updated[1]:
                updated[1] = sbar.update(events)
        return updated[0] or updated[1]

    def set_menu(self, menu: 'pygame_menu.Menu') -> 'ScrollArea':
        """
        Set the Menu reference.

        :param menu: Menu object
        :return: Self reference
        """
        self._menu = menu
        for sbar in self._scrollbars:
            sbar.set_menu(menu)
        return self

    def get_menu(self) -> Optional['pygame_menu.Menu']:
        """
        Return the Menu reference (if exists).

        :return: Menu reference
        """
        return self._menu

    def collide(self, widget: 'pygame_menu.widgets.Widget', event: 'pygame.event.Event') -> bool:
        """
        If user event collides a widget within the scroll area respect to the relative position.

        :param widget: Widget
        :param event: Pygame event
        :return: ``True`` if collide
        """
        widget_rect = widget.get_rect()
        if hasattr(pygame, 'FINGERDOWN') and (
                event.type == pygame.FINGERDOWN or event.type == pygame.FINGERUP or
                event.type == pygame.FINGERMOTION):
            display_size = self._menu.get_window_size()
            finger_pos = (event.x * display_size[0], event.y * display_size[1])
            return bool(self.to_real_position(widget_rect).collidepoint(*finger_pos))
        else:
            return bool(self.to_real_position(widget_rect).collidepoint(*event.pos))

    def get_decorator(self) -> 'Decorator':
        """
        Return the ScrollArea decorator API.

        .. note:: Menu drawing order:

            1. Menu background color/image
            2. Menu ``prev`` decorator
            3. **Menu ScrollArea ``prev`` decorator**
            4. **Menu ScrollArea widgets**
            5. **Menu ScrollArea ``post`` decorator**
            6. Menu title
            7. Menu ``post`` decorator

        :return: Decorator API
        """
        return self._decorator


class _ScrollAreaCopyException(Exception):
    """
    If user tries to copy a ScrollArea.
    """
    pass
