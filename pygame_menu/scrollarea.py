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
from pygame_menu.utils import make_surface, assert_color, assert_position, assert_orientation, uuid4
from pygame_menu.widgets import ScrollBar, MenuBar

from pygame_menu._types import Union, NumberType, Tuple, List, Dict, Tuple2NumberType, \
    Optional, Tuple2IntType, NumberInstance, ColorInputType, EventVectorType, EventType


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
    :param extend_x: Px to extend the surface on x axis (px) from left. Recommended use only within Menus
    :param extend_y: Px to extend the surface on y axis (px) from top. Recommended use only within Menus
    :param menubar: Menubar for style compatibility. ``None`` if ScrollArea is not used within a Menu (for example, in Frames)
    :param parent_scrollarea: Parent ScrollArea if the new one is added within another area
    :param scrollbar_color: Scrollbars color
    :param scrollbar_cursor: Scrollbar cursor
    :param scrollbar_slider_color: Color of the sliders
    :param scrollbar_slider_pad: Space between slider and scrollbars borders (px)
    :param scrollbar_thick: Scrollbar thickness (px)
    :param scrollbars: Positions of the scrollbars. See :py:mod:`pygame_menu.locals`
    :param shadow: Indicate if a shadow is drawn on each scrollbar
    :param shadow_color: Color of the shadow of each scrollbar
    :param shadow_offset: Offset of the scrollbar shadow (px)
    :param shadow_position: Position of the scrollbar shadow. See :py:mod:`pygame_menu.locals`
    :param world: Surface to draw and scroll
    """
    _bg_surface: Optional['pygame.Surface']
    _decorator: 'Decorator'
    _extend_x: int
    _extend_y: int
    _id: str
    _menu: Optional['pygame_menu.Menu']
    _menubar: 'pygame_menu.widgets.MenuBar'
    _parent_scrollarea: 'ScrollArea'
    _rect: 'pygame.Rect'
    _scrollbar_positions: Tuple[str, ...]
    _scrollbar_thick: int
    _scrollbars: List['ScrollBar']
    _translate: Tuple2IntType
    _view_rect: 'pygame.Rect'
    _world: 'pygame.Surface'

    def __init__(
            self,
            area_width: int,
            area_height: int,
            area_color: Optional[Union[ColorInputType, 'pygame_menu.BaseImage']] = None,
            extend_x: int = 0,
            extend_y: int = 0,
            menubar: Optional['MenuBar'] = None,
            parent_scrollarea: Optional['ScrollArea'] = None,
            scrollbar_color: ColorInputType = (235, 235, 235),
            scrollbar_cursor: Optional[Union[int, 'pygame.cursors.Cursor']] = None,
            scrollbar_slider_color: ColorInputType = (200, 200, 200),
            scrollbar_slider_pad: NumberType = 0,
            scrollbar_thick: int = 20,
            scrollbars: Union[str, Tuple[str, ...]] = get_scrollbars_from_position(_locals.POSITION_SOUTHEAST),
            shadow: bool = False,
            shadow_color: ColorInputType = (0, 0, 0),
            shadow_offset: int = 2,
            shadow_position: str = _locals.POSITION_SOUTHEAST,
            world: Optional['pygame.Surface'] = None
    ) -> None:
        assert isinstance(area_height, int)
        assert isinstance(area_width, int)
        assert isinstance(extend_x, int)
        assert isinstance(extend_y, int)
        assert isinstance(scrollbar_slider_pad, NumberInstance)
        assert isinstance(scrollbar_thick, int)
        assert isinstance(shadow, bool)
        assert isinstance(shadow_offset, int)
        assert isinstance(world, (pygame.Surface, type(None)))

        scrollbar_color = assert_color(scrollbar_color)
        scrollbar_slider_color = assert_color(scrollbar_slider_color)
        shadow_color = assert_color(shadow_color)

        assert_position(shadow_position)

        assert area_width > 0 and area_height > 0, \
            'area size must be greater than zero'

        self._bg_surface = None
        self._decorator = Decorator(self)
        self._id = uuid4()
        self._rect = pygame.Rect(0, 0, int(area_width), int(area_height))
        self._scrollbar_positions = tuple(set(scrollbars))  # Ensure unique
        self._scrollbar_thick = scrollbar_thick
        self._scrollbars = []
        self._translate = (0, 0)
        self._world = world

        self._extend_x = extend_x
        self._extend_y = extend_y
        self._menubar = menubar

        self.set_parent_scrollarea(parent_scrollarea)

        if area_color is not None:
            self._bg_surface = make_surface(width=area_width + self._extend_x,
                                            height=area_height + self._extend_y)
            if isinstance(area_color, pygame_menu.BaseImage):
                area_color.draw(surface=self._bg_surface, area=self._bg_surface.get_rect())
            else:
                self._bg_surface.fill(assert_color(area_color))

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
            sbar.set_cursor(cursor=scrollbar_cursor)
            sbar.set_scrollarea(self)
            sbar.configured = True

            self._scrollbars.append(sbar)

        self._apply_size_changes()

        # Menu reference
        self._menu = None

    def set_id(self, scrollarea_id: str) -> 'ScrollArea':
        """
        Set ScrollArea id.

        :param scrollarea_id: New area ID
        :return: Self reference
        """
        assert isinstance(scrollarea_id, str)
        self._id = scrollarea_id
        return self

    def get_id(self) -> str:
        """
        Return the ScrollArea id.

        :return: Self reference
        """
        return self._id

    def set_parent_scrollarea(self, parent: Optional['ScrollArea']) -> None:
        """
        Set parent ScrollArea.

        :param parent: Parent ScrollArea
        :return: None
        """
        assert isinstance(parent, (ScrollArea, type(None)))
        assert parent != self
        self._parent_scrollarea = parent

    def get_parent(self) -> Optional['ScrollArea']:
        """
        Return the parent ScrollArea.

        :return: Parent ScrollArea object
        """
        return self._parent_scrollarea

    def get_depth(self) -> int:
        """
        Return the depth of the ScrollArea (how many parents do it has recursively).

        :return: Depth's number
        """
        parent = self._parent_scrollarea
        count = 0
        while True:
            if parent is None:
                break
            count += 1
            parent = parent._parent_scrollarea
        return count

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
        Draw the ScrollArea.

        :param surface: Surface to render the area
        :return: Self reference
        """
        if not self._world:
            return self

        # Background surface already has previous decorators
        if self._bg_surface:
            surface.blit(self._bg_surface, (self._rect.x - self._extend_x, self._rect.y - self._extend_y))

        for sbar in self._scrollbars:
            if not sbar.is_visible():
                continue
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

        :return: ScrollArea offset on x-axis and y-axis
        """
        offsets = [0, 0]
        for sbar in self._scrollbars:
            if not sbar.is_visible():
                continue
            if sbar.get_orientation() == SCROLL_HORIZONTAL:
                if self.get_hidden_width():
                    offsets[0] += sbar.get_value()
            else:
                if self.get_hidden_height():
                    offsets[1] += sbar.get_value()
        return offsets[0], offsets[1]

    def get_rect(self, to_real_position: bool = False) -> 'pygame.Rect':
        """
        Return the :py:class:`pygame.Rect` object of the ScrollArea.

        :param to_real_position: Get real position fof the scroll area
        :return: Pygame.Rect object
        """
        rect = self._rect.copy()
        if to_real_position:
            rect = self.to_real_position(rect)
        return rect

    def get_scrollbar_thickness(self, orientation: str, real: bool = False) -> int:
        """
        Return the scroll thickness of the area. If it's hidden return zero.

        :param orientation: Orientation of the scroll. See :py:mod:`pygame_menu.locals`
        :param real: If ``True`` returns the real thickness depending if it is shown or not
        :return: Thickness (px)
        """
        assert_orientation(orientation)
        assert isinstance(real, bool)
        if real:
            total = 0
            for sbar in self._scrollbars:
                if sbar.get_orientation() == orientation and sbar.is_visible():
                    total += sbar.get_thickness()
            return total
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

    def hide_scrollbars(self, orientation: str) -> 'ScrollArea':
        """
        Hide scrollbar from given orientation.

        :param orientation: Orientation. See :py:mod:`pygame_menu.locals`
        :return: Self reference
        """
        assert_orientation(orientation)
        for sbar in self._scrollbars:
            if sbar.get_orientation() == orientation:
                sbar.hide()
        return self

    def show_scrollbars(self, orientation: str) -> 'ScrollArea':
        """
        Hide scrollbar from given orientation.

        :param orientation: Orientation. See :py:mod:`pygame_menu.locals`
        :return: Self reference
        """
        assert_orientation(orientation)
        for sbar in self._scrollbars:
            if sbar.get_orientation() == orientation:
                sbar.show()
        return self

    def get_world_size(self) -> Tuple2IntType:
        """
        Return the world size.

        :return: Width, height in pixels
        """
        if self._world is None:
            return 0, 0
        return self._world.get_width(), self._world.get_height()

    def get_size(self, inner: bool = False) -> Tuple2IntType:
        """
        Return the area size.

        :param inner: If ``True`` returns the rect view area
        :return: Width, height in pixels
        """
        if inner:
            return self._view_rect.width, self._view_rect.height
        return self._rect.width, self._rect.height

    def mouse_is_over(self, view: bool = False) -> bool:
        """
        Return ``True`` if the mouse is placed over the ScrollArea.

        :param view: If ``True`` uses "view rect" instead of "rect"
        :return: ``True`` if the mouse is over the object
        """
        mousex, mousey = pygame.mouse.get_pos()
        return bool(self.to_absolute_position(self._view_rect if view else self._rect).collidepoint(mousex, mousey))

    def _on_horizontal_scroll(self, value: NumberType) -> None:
        """
        Call when a horizontal scroll bar as changed to update the
        position of the opposite one if it exists.

        :param value: New position of the slider
        :return: None
        """
        for sbar in self._scrollbars:
            if not sbar.is_visible():
                continue
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
            if not sbar.is_visible():
                continue
            if sbar.get_orientation() == SCROLL_VERTICAL \
                    and self.get_hidden_height() != 0 \
                    and sbar.get_value() != value:
                sbar.set_value(value)

    def get_scroll_value_percentual(self, orientation: str) -> float:
        """
        Get the scroll value in percentage, if ``0`` the scroll is at top/left, ``1`` bottom/right.

        .. note::

            If ScrollArea does not contain such orientation scroll, ``-1`` is returned.

        :param orientation: Orientation. See :py:mod:`pygame_menu.locals`
        :return: Value from ``0`` to ``1``
        """
        assert_orientation(orientation)
        for sbar in self._scrollbars:
            if not sbar.is_visible():
                continue
            if sbar.get_orientation() == orientation:
                return sbar.get_value_percentual()
        return -1

    def scroll_to(self, orientation: str, value: NumberType) -> 'ScrollArea':
        """
        Scroll to position in terms of the percentage.

        :param orientation: Orientation. See :py:mod:`pygame_menu.locals`
        :param value: If ``0`` scrolls to top, ``1`` to bottom
        :return: Self reference
        """
        assert_orientation(orientation)
        assert isinstance(value, NumberInstance) and 0 <= value <= 1
        for sbar in self._scrollbars:
            if not sbar.is_visible():
                continue
            if sbar.get_orientation() == orientation:
                vmin, vmax = sbar.get_minmax()
                delta = vmax - vmin
                new_value = int(min(vmin + delta * float(value), vmax))
                sbar.set_value(new_value)
                break
        return self

    # noinspection PyTypeChecker
    def scroll_to_rect(self, rect: 'pygame.Rect', margin: NumberType = 10) -> bool:
        """
        Ensure that the given rect is in the viewable area.

        :param rect: Rect in the world surface reference
        :param margin: Extra margin around the rect (px)
        :return: Scrollarea scrolled to rect. If ``False`` the rect was already inside the visible area
        """
        assert isinstance(margin, NumberInstance) and margin >= 0

        # Check if visible
        if self.to_real_position(rect, visible=True).height == 0 and self._parent_scrollarea is not None:
            self._parent_scrollarea.scroll_to_rect(self._parent_scrollarea.get_rect())
            self._parent_scrollarea.scroll_to_rect(self.get_rect())

        assert isinstance(margin, NumberInstance)
        real_rect = self.to_real_position(rect)

        # Check rect is in viewable area
        sx = self.get_scrollbar_thickness(SCROLL_VERTICAL)
        sy = self.get_scrollbar_thickness(SCROLL_HORIZONTAL)
        view_rect = self.get_absolute_view_rect()
        if view_rect.topleft[0] <= real_rect.topleft[0] + sx \
                and view_rect.topleft[1] <= real_rect.topleft[1] + sy \
                and view_rect.bottomright[0] + sx >= real_rect.bottomright[0] \
                and view_rect.bottomright[1] + sy >= real_rect.bottomright[1]:
            return False

        for sbar in self._scrollbars:
            if not sbar.is_visible():
                continue
            if sbar.get_orientation() == SCROLL_HORIZONTAL and self.get_hidden_width():
                shortest_move = min(real_rect.left - margin - view_rect.left,
                                    real_rect.right + margin - view_rect.right, key=abs)
                value = min(sbar.get_maximum(), sbar.get_value() + shortest_move)
                value = max(sbar.get_minimum(), value)
                sbar.set_value(value)
            if sbar.get_orientation() == SCROLL_VERTICAL and self.get_hidden_height():
                shortest_move = min(real_rect.bottom + margin - view_rect.bottom,
                                    real_rect.top - margin - view_rect.top, key=abs)
                value = min(sbar.get_maximum(), sbar.get_value() + shortest_move)
                value = max(sbar.get_minimum(), value)
                sbar.set_value(value)

        if self._parent_scrollarea is not None:
            self._parent_scrollarea.scroll_to_rect(rect, margin=margin)

        # Adjust scrollbars, if value is similar to 0 or 1
        # for sbar in self._scrollbars:
        #     if not sbar.is_visible():
        #         continue
        #     if sbar.get_value_percentual() < 0.025:
        #         sbar.set_value(sbar.get_minimum())
        #     if sbar.get_value_percentual() > 0.975:
        #         sbar.set_value(sbar.get_maximum())

        return True

    def set_position(self, posx: int, posy: int) -> 'ScrollArea':
        """
        Set the position.

        :param posx: X position
        :param posy: Y position
        :return: Self reference
        """
        self._rect.x = posx + self._extend_x + self._translate[0]
        self._rect.y = posy + self._extend_y + self._translate[1]
        self._apply_size_changes()
        return self

    def get_position(self) -> Tuple2IntType:
        """
        Return the ScrollArea position.

        :return: X, Y position in px
        """
        return self._rect.x, self._rect.y

    def translate(self, x: NumberType, y: NumberType) -> 'ScrollArea':
        """
        Translate on x-axis and y-axis

        :param x: X translation (px)
        :param y: Y translation (px)
        :return: Self reference
        """
        assert isinstance(x, NumberInstance)
        assert isinstance(y, NumberInstance)
        self._rect.x -= self._translate[0]
        self._rect.y -= self._translate[1]
        self._translate = (x, y)
        self._rect.x += x
        self._rect.y += y
        self._apply_size_changes()
        return self

    def get_translate(self) -> Tuple2IntType:
        """
        Get object translation on both axis.

        :return: Translation on x-axis and y-axis (px)
        """
        return self._translate

    def set_world(self, surface: 'pygame.Surface') -> 'ScrollArea':
        """
        Update the scrolled surface.

        :param surface: New world surface
        :return: Self reference
        """
        self._world = surface
        self._apply_size_changes()
        return self

    def get_parent_position(self) -> Tuple2IntType:
        """
        Return parent ScrollArea position.

        :return: Position on x, y axis (px)
        """
        if self._parent_scrollarea is not None:
            px, py = self._parent_scrollarea.get_position()
            ox, oy = self._parent_scrollarea.get_offsets()
            parx, pary = 0, 0
            if self._parent_scrollarea.get_parent() is not None:
                parx, pary = self._parent_scrollarea.get_parent_position()
            return px - ox + parx, py - oy + pary
        return 0, 0

    def to_absolute_position(self, virtual: 'pygame.Rect') -> 'pygame.Rect':
        """
        Return the absolute position of a rect within the ScrollArea. Absolute position
        is concerning the parent ScrollArea. If ``None``, the rect is not changed at all.

        .. note::

            Absolute position must be used if desired to get the widget position outside a scrolled
            area status, for example the view rect, or the scrollbars.

        :param virtual: Rect in the world surface reference
        :return: Rect in absolute position
        """
        rect = pygame.Rect(virtual)
        parent_position = self.get_parent_position()
        rect.x += parent_position[0]
        rect.y += parent_position[1]
        return rect

    def get_absolute_view_rect(self) -> 'pygame.Rect':
        """
        Return the ScrollArea absolute view rect clipped if it is not visible by
        it's parent ScrollArea.

        :return: Clipped absolute view rect
        """
        view_rect_absolute = self.to_absolute_position(self._view_rect)
        if self._parent_scrollarea is not None:
            parent = self._parent_scrollarea
            while True:  # Recursive
                if parent is None:
                    break
                view_rect_absolute = parent.get_absolute_view_rect().clip(view_rect_absolute)
                parent = parent._parent_scrollarea
        return view_rect_absolute

    def to_real_position(self, virtual: Union['pygame.Rect', Tuple2NumberType], visible: bool = False
                         ) -> Union['pygame.Rect', Tuple2IntType]:
        """
        Return the real position/Rect according to the ScrollArea origin
        of a position/Rect in the world surface reference.

        .. note::

            Real position must be used if desired to get the widget position within a scrolled
            area status.

        :param virtual: Position/Rect in the world surface reference
        :param visible: If a ``virtual`` is Rect object, return only the visible width/height
        :return: Real rect or real position
        """
        assert isinstance(virtual, (pygame.Rect, tuple, list))
        offsets = self.get_offsets()
        parent_position = self.get_parent_position()

        if isinstance(virtual, pygame.Rect):
            rect = pygame.Rect(virtual)
            rect.x = virtual.x + self._rect.x - offsets[0] + parent_position[0]
            rect.y = virtual.y + self._rect.y - offsets[1] + parent_position[1]
            if visible:
                return self.get_absolute_view_rect().clip(rect)  # Visible width and height
            return rect

        x_coord = self._rect.x + virtual[0] - offsets[0] + parent_position[0]
        y_coord = self._rect.y + virtual[1] - offsets[1] + parent_position[1]
        return int(x_coord), int(y_coord)

    def to_world_position(
            self,
            real: Union['pygame.Rect', Tuple2NumberType]
    ) -> Union['pygame.Rect', Tuple2IntType]:
        """
        Return the position/Rect in the world surface reference
        of a real position/Rect according to the ScrollArea origin.

        .. note::

            Virtual position must be used if desired to get the widget position within a scrolled
            area status.

        :param real: Position/Rect according ScrollArea origin
        :return: Rect in world or position in world
        """
        assert isinstance(real, (pygame.Rect, tuple, list))
        offsets = self.get_offsets()
        parent_position = self.get_parent_position()

        if isinstance(real, pygame.Rect):
            rect = pygame.Rect(real)
            rect.x = real.x - self._rect.x + offsets[0] - parent_position[0]
            rect.y = real.y - self._rect.y + offsets[1] - parent_position[1]
            return rect

        x_coord = real[0] - self._rect.x + offsets[0] - parent_position[0]
        y_coord = real[1] - self._rect.y + offsets[1] - parent_position[1]
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

    def update(self, events: EventVectorType) -> bool:
        """
        Called by end user to update scroll state.

        :param events: List of pygame events
        :return: ``True`` if updated
        """
        updated = [0, 0]
        for sbar in self._scrollbars:
            if not sbar.is_visible():
                continue
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

    def collide(
            self,
            widget: Union['pygame_menu.widgets.Widget', 'pygame.Rect'],
            event: EventType
    ) -> bool:
        """
        If user event collides a widget within the ScrollArea respect to the relative position.

        :param widget: Widget or rect
        :param event: Pygame event
        :return: ``True`` if collide
        """
        if not isinstance(widget, pygame.Rect):
            widget_rect = widget.get_rect(to_real_position=True)
        else:
            widget_rect = widget
        if hasattr(pygame, 'FINGERDOWN') and (
                event.type == pygame.FINGERDOWN or event.type == pygame.FINGERUP or
                event.type == pygame.FINGERMOTION):
            display_size = self._menu.get_window_size()
            finger_pos = (event.x * display_size[0], event.y * display_size[1])
            return bool(widget_rect.collidepoint(*finger_pos))
        else:
            return bool(widget_rect.collidepoint(*event.pos))

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
