"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SCROLLAREA
ScrollArea class to manage scrolling in Menu.
"""

__all__ = [

    # Main class
    'ScrollArea',

    # Utils
    'get_scrollbars_from_position'

]

import pygame
import pygame_menu

from itertools import product
from pygame_menu._base import Base
from pygame_menu._decorator import Decorator
from pygame_menu.locals import POSITION_SOUTHEAST, POSITION_SOUTHWEST, POSITION_WEST, \
    POSITION_NORTHEAST, POSITION_NORTHWEST, POSITION_CENTER, POSITION_EAST, \
    POSITION_NORTH, ORIENTATION_HORIZONTAL, ORIENTATION_VERTICAL, \
    SCROLLAREA_POSITION_BOTH_HORIZONTAL, POSITION_SOUTH, SCROLLAREA_POSITION_FULL, \
    SCROLLAREA_POSITION_BOTH_VERTICAL, SCROLLAREA_POSITION_NONE
from pygame_menu.utils import make_surface, assert_color, assert_position, \
    assert_orientation, get_finger_pos
from pygame_menu.widgets import ScrollBar

from pygame_menu._types import Union, NumberType, Tuple, List, Dict, Tuple2NumberType, \
    CursorInputType, Optional, Tuple2IntType, NumberInstance, ColorInputType, \
    EventVectorType, EventType, VectorInstance, StringVector, Any


def get_scrollbars_from_position(
        position: str
) -> Union[str, Tuple[str, str], Tuple[str, str, str, str]]:
    """
    Return the scrollbars from the given position.

    Raises ``ValueError`` if invalid position.

    :param position: Position
    :return: Scrollbars
    """
    if position in (POSITION_EAST, POSITION_EAST, POSITION_WEST, POSITION_NORTH):
        return position
    elif position == POSITION_NORTHWEST:
        return POSITION_NORTH, POSITION_WEST
    elif position == POSITION_NORTHEAST:
        return POSITION_NORTH, POSITION_EAST
    elif position == POSITION_SOUTHWEST:
        return POSITION_SOUTH, POSITION_WEST
    elif position == POSITION_SOUTHEAST:
        return POSITION_SOUTH, POSITION_EAST
    elif position == SCROLLAREA_POSITION_FULL:
        return POSITION_SOUTH, POSITION_EAST, POSITION_WEST, POSITION_NORTH
    elif position == SCROLLAREA_POSITION_BOTH_HORIZONTAL:
        return POSITION_SOUTH, POSITION_NORTH
    elif position == SCROLLAREA_POSITION_BOTH_VERTICAL:
        return POSITION_EAST, POSITION_WEST
    elif position == SCROLLAREA_POSITION_NONE:
        return ''
    elif position == POSITION_CENTER:
        raise ValueError('cannot init scrollbars from center position')
    else:
        raise ValueError('unknown ScrollArea position')


DEFAULT_SCROLLBARS = get_scrollbars_from_position(POSITION_SOUTHEAST)


class ScrollArea(Base):
    """
    The ScrollArea class provides a scrolling view managing up to 4 scroll bars.

    A scroll area is used to display the contents of a child surface (``world``).
    If the surface exceeds the size of the drawing surface, the view provide
    scroll bars so that the entire area of the child surface can be viewed.

    .. note::

        See :py:mod:`pygame_menu.locals` for valid ``scrollbars`` and
        ``shadow_position`` values.

    .. note::

        ScrollArea cannot be copied or deep-copied.

    :param area_width: Width of scrollable area in px
    :param area_height: Height of scrollable area in px
    :param area_color: Background color, it can be a color or an image
    :param border_color: Border color
    :param border_width: Border width in px
    :param controls_joystick: Use joystick events
    :param controls_keyboard: Use keyboard events
    :param controls_mouse: Use mouse events
    :param controls_touchscreen: Use touchscreen events
    :param extend_x: Px to extend the surface on x-axis in px from left. Recommended use only within Menus
    :param extend_y: Px to extend the surface on y-axis in px from top. Recommended use only within Menus
    :param menubar: Menubar for style compatibility. ``None`` if ScrollArea is not used within a Menu (for example, in Frames)
    :param parent_scrollarea: Parent ScrollArea if the new one is added within another area
    :param scrollarea_id: Scrollarea ID
    :param scrollbar_color: Scrollbars color
    :param scrollbar_cursor: Scrollbar cursor
    :param scrollbar_slider_color: Color of the sliders
    :param scrollbar_slider_hover_color: Color of the slider if hovered or clicked
    :param scrollbar_slider_pad: Space between slider and scrollbars borders in px
    :param scrollbar_thick: Scrollbar thickness in px
    :param scrollbars: Positions of the scrollbars. See :py:mod:`pygame_menu.locals`
    :param shadow: Indicate if a shadow is drawn on each scrollbar
    :param shadow_color: Color of the shadow of each scrollbar
    :param shadow_offset: Offset of the scrollbar shadow in px
    :param shadow_position: Position of the scrollbar shadow. See :py:mod:`pygame_menu.locals`
    :param world: Surface to draw and scroll
    """
    _area_color: Optional[Union[ColorInputType, 'pygame_menu.BaseImage']]
    _border_color: Optional[Union[ColorInputType, 'pygame_menu.BaseImage']]
    _border_tiles: List['pygame.Surface']
    _border_tiles_size: Tuple2IntType
    _border_width: int
    _bg_surface: Optional['pygame.Surface']
    _decorator: 'Decorator'
    _extend_x: int
    _extend_y: int
    _menu: Optional['pygame_menu.Menu']
    _menubar: 'pygame_menu.widgets.MenuBar'
    _parent_scrollarea: 'ScrollArea'
    _rect: 'pygame.Rect'
    _scrollbar_positions: Tuple[str, ...]
    _scrollbars: List['ScrollBar']
    _scrollbars_props: Tuple[Any, ...]
    _translate: Tuple2IntType
    _view_rect: 'pygame.Rect'
    _world: 'pygame.Surface'

    def __init__(
            self,
            area_width: int,
            area_height: int,
            area_color: Optional[Union[ColorInputType, 'pygame_menu.BaseImage']] = None,
            border_color: Optional[Union[ColorInputType, 'pygame_menu.BaseImage']] = None,
            border_width: int = 0,
            controls_joystick: bool = True,
            controls_keyboard: bool = True,
            controls_mouse: bool = True,
            controls_touchscreen: bool = True,
            extend_x: int = 0,
            extend_y: int = 0,
            menubar: Optional['pygame_menu.widgets.MenuBar'] = None,
            parent_scrollarea: Optional['ScrollArea'] = None,
            scrollarea_id: str = '',
            scrollbar_color: ColorInputType = (235, 235, 235),
            scrollbar_cursor: CursorInputType = None,
            scrollbar_slider_color: ColorInputType = (200, 200, 200),
            scrollbar_slider_hover_color: ColorInputType = (180, 180, 180),
            scrollbar_slider_pad: NumberType = 0,
            scrollbar_thick: int = 20,
            scrollbars: StringVector = DEFAULT_SCROLLBARS,
            shadow: bool = False,
            shadow_color: ColorInputType = (0, 0, 0),
            shadow_offset: int = 2,
            shadow_position: str = POSITION_SOUTHEAST,
            world: Optional['pygame.Surface'] = None
    ) -> None:
        super(ScrollArea, self).__init__(object_id=scrollarea_id)

        assert isinstance(area_height, int)
        assert isinstance(area_width, int)
        assert isinstance(border_width, int)
        assert isinstance(controls_joystick, bool)
        assert isinstance(controls_keyboard, bool)
        assert isinstance(controls_mouse, bool)
        assert isinstance(controls_touchscreen, bool)
        assert isinstance(extend_x, int)
        assert isinstance(extend_y, int)
        assert isinstance(scrollbar_slider_pad, NumberInstance)
        assert isinstance(scrollbar_thick, int)
        assert isinstance(shadow, bool)
        assert isinstance(shadow_offset, int)
        assert isinstance(world, (pygame.Surface, type(None)))

        if area_color is not None and not isinstance(area_color, pygame_menu.BaseImage):
            area_color = assert_color(area_color)
        if border_color is not None and not isinstance(border_color, pygame_menu.BaseImage):
            border_color = assert_color(border_color)

        # Create tiles
        if isinstance(border_color, pygame_menu.BaseImage):
            iw, ih = border_color.get_size()
            tw, th = iw // 3, ih // 3
            self._border_tiles_size = tw, th
            self._border_tiles = [
                border_color.subsurface((x, y, tw, th))
                for x, y in product(range(0, iw, tw), range(0, ih, th))
            ]

        scrollbar_color = assert_color(scrollbar_color)
        scrollbar_slider_color = assert_color(scrollbar_slider_color)
        shadow_color = assert_color(shadow_color)

        assert_position(shadow_position)

        assert area_width > 0 and area_height > 0, \
            'area size must be greater than zero'

        assert isinstance(scrollbars, (str, VectorInstance))
        unique_scrolls = []
        if isinstance(scrollbars, str):
            unique_scrolls.append(scrollbars)
        else:
            for s in scrollbars:
                if s not in unique_scrolls:
                    unique_scrolls.append(s)

        # Remove none position
        if '' in unique_scrolls:
            unique_scrolls.pop(unique_scrolls.index(''))

        self._area_color = area_color
        self._border_color = border_color
        self._border_width = border_width
        self._bg_surface = None
        self._decorator = Decorator(self)
        self._scrollbar_positions = tuple(unique_scrolls)  # Ensure unique
        self._translate = (0, 0)
        self._world = world

        self._extend_x = extend_x
        self._extend_y = extend_y
        self._menubar = menubar

        self._scrollbars_props = (scrollbar_color, scrollbar_thick, scrollbar_slider_color,
                                  scrollbar_slider_hover_color, scrollbar_slider_pad,
                                  scrollbar_cursor, shadow, shadow_color, shadow_position,
                                  shadow_offset, controls_joystick, controls_mouse,
                                  controls_touchscreen, controls_keyboard)
        self.set_parent_scrollarea(parent_scrollarea)
        self.create_rect(area_width, area_height)

        # Menu reference
        self._menu = None

    def create_rect(self, width: int, height: int) -> None:
        """
        Create rect object.

        :param width: Area width
        :param height: Area height
        """
        assert isinstance(width, int)
        assert isinstance(height, int)
        self._rect = pygame.Rect(0, 0, int(width), int(height))
        self._scrollbars = []
        self._view_rect = self.get_view_rect()

        # Unpack properties
        (scrollbar_color, scrollbar_thick, scrollbar_slider_color,
         scrollbar_slider_hover_color, scrollbar_slider_pad,
         scrollbar_cursor, shadow, shadow_color, shadow_position,
         shadow_offset, controls_joystick, controls_mouse, controls_touchscreen,
         controls_keyboard) = self._scrollbars_props

        for pos in self._scrollbar_positions:
            assert_position(pos)

            if pos == POSITION_EAST or pos == POSITION_WEST:
                sbar = ScrollBar(
                    length=self._view_rect.height,
                    onchange=self._on_vertical_scroll,
                    orientation=ORIENTATION_VERTICAL,
                    page_ctrl_color=scrollbar_color,
                    page_ctrl_thick=scrollbar_thick,
                    slider_color=scrollbar_slider_color,
                    slider_hover_color=scrollbar_slider_hover_color,
                    slider_pad=scrollbar_slider_pad,
                    values_range=(0, max(1, self.get_hidden_height()))
                )

            else:
                sbar = ScrollBar(
                    length=self._view_rect.width,
                    onchange=self._on_horizontal_scroll,
                    page_ctrl_color=scrollbar_color,
                    page_ctrl_thick=scrollbar_thick,
                    slider_color=scrollbar_slider_color,
                    slider_hover_color=scrollbar_slider_hover_color,
                    slider_pad=scrollbar_slider_pad,
                    values_range=(0, max(1, self.get_hidden_width()))
                )

            sbar.set_shadow(
                enabled=shadow,
                color=shadow_color,
                position=shadow_position,
                offset=shadow_offset
            )
            sbar.set_controls(
                joystick=controls_joystick,
                mouse=controls_mouse,
                touchscreen=controls_touchscreen,
                keyboard=controls_keyboard
            )
            sbar.set_cursor(cursor=scrollbar_cursor)
            sbar.set_scrollarea(self)
            sbar.configured = True
            sbar.hide()

            self._scrollbars.append(sbar)

        self._apply_size_changes()

    def _make_background_surface(self) -> None:
        """
        Create background surface.
        """
        # If bg surface is created, and it's the same size
        if self._bg_surface is not None and \
                self._bg_surface.get_width() == self._rect.width and \
                self._bg_surface.get_height() == self._rect.height:
            return

        # Make surface
        self._bg_surface = make_surface(width=self._rect.width + self._extend_x, height=self._rect.height + self._extend_y)
        rect = self._bg_surface.get_rect()
        if self._area_color is not None:
            if isinstance(self._area_color, pygame_menu.BaseImage):
                self._area_color.draw(surface=self._bg_surface, area=rect)
            else:
                self._bg_surface.fill(assert_color(self._area_color))

    def update_area_color(
            self,
            color: Optional[Union[ColorInputType, 'pygame_menu.BaseImage']]
    ) -> 'ScrollArea':
        """
        Updates area color.

        :param color: Color
        :return: Self reference
        """
        self._area_color = color
        self._bg_surface = None
        self._make_background_surface()
        return self

    def set_parent_scrollarea(self, parent: Optional['ScrollArea']) -> 'ScrollArea':
        """
        Set parent ScrollArea.

        :param parent: Parent ScrollArea
        """
        assert isinstance(parent, (ScrollArea, type(None)))
        assert parent != self, 'parent scrollarea cannot be set as itself'
        self._parent_scrollarea = parent
        return self

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
        if parent is not None:
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
        Deep-copy method.

        :param memodict: Memo dict
        :return: Raises copy exception
        """
        raise _ScrollAreaCopyException('ScrollArea class cannot be copied')

    def force_menu_surface_update(self) -> 'ScrollArea':
        """
        Forces menu surface update after next rendering call.

        .. note::

            This method is expensive, as menu surface update forces re-rendering
            of all widgets (because them can change in size, position, etc...).

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
            of all Menu widgets as
            :py:meth:`pygame_menu.widgets.core.widget.Widget.force_menu_surface_update`
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
        """
        self._view_rect = self.get_view_rect()

        for sbar in self._scrollbars:
            pos = self._scrollbar_positions[self._scrollbars.index(sbar)]

            d_size, dx, dy = 0, 0, 0
            if self._menubar is not None:
                d_size, (dx, dy) = self._menubar.get_scrollbar_style_change(pos)

            if pos == POSITION_WEST:
                sbar.set_position(x=self._view_rect.left - sbar.get_thickness() + dx, y=self._view_rect.top + dy)
            elif pos == POSITION_EAST:
                sbar.set_position(x=self._view_rect.right + dx, y=self._view_rect.top + dy)
            elif pos == POSITION_NORTH:
                sbar.set_position(x=self._view_rect.left + dx, y=self._view_rect.top - sbar.get_thickness() + dy)
            elif pos == POSITION_SOUTH:  # South
                sbar.set_position(x=self._view_rect.left + dx, y=self._view_rect.bottom + dy)
            else:
                raise ValueError('unknown position, only west, east, north, and'
                                 'south are allowed')

            if pos in (POSITION_NORTH, POSITION_SOUTH):
                if self.get_hidden_width() != 0:
                    sbar.set_length(self._view_rect.width + d_size)
                    sbar.set_maximum(self.get_hidden_width())
                    sbar.set_page_step(self._view_rect.width * self.get_hidden_width() /
                                       (self._view_rect.width + self.get_hidden_width()))
                    sbar.show()
                else:
                    sbar.hide()

            elif pos in (POSITION_EAST, POSITION_WEST):
                if self.get_hidden_height() != 0:
                    sbar.set_length(self._view_rect.height + d_size)
                    sbar.set_maximum(self.get_hidden_height())
                    sbar.set_page_step(self._view_rect.height * self.get_hidden_height() /
                                       (self._view_rect.height + self.get_hidden_height()))
                    sbar.show()
                else:
                    sbar.hide()

    def draw(self, surface: 'pygame.Surface') -> 'ScrollArea':
        """
        Draw the ScrollArea.

        :param surface: Surface to render the area
        :return: Self reference
        """
        if not self._world:
            return self

        # Background surface already has previous decorators
        if self._area_color is not None:
            self._make_background_surface()
            surface.blit(self._bg_surface, (self._rect.x - self._extend_x, self._rect.y - self._extend_y))

        # Draw world surface
        # noinspection PyTypeChecker
        surface.blit(self._world, self._view_rect.topleft, (self.get_offsets(), self._view_rect.size))

        # Then draw scrollbars
        for sbar in self._scrollbars:
            if not sbar.is_visible():
                continue
            if sbar.get_orientation() == ORIENTATION_HORIZONTAL:
                if self.get_hidden_width():
                    sbar.draw(surface)
            else:
                if self.get_hidden_height():
                    sbar.draw(surface)

        # Draw post decorator
        self._decorator.draw_post(surface)

        # Create border
        if isinstance(self._border_color, pygame_menu.BaseImage):  # Image
            tw, th = self._border_tiles_size
            border_rect = pygame.Rect(
                int(self._rect.x - tw),
                int(self._rect.y - th),
                int(self._rect.width + 2 * tw),
                int(self._rect.height + 2 * th)
            )

            surface_blit = surface.blit
            (
                tile_nw,
                tile_w,
                tile_sw,
                tile_n,
                tile_c,
                tile_s,
                tile_ne,
                tile_e,
                tile_se,
            ) = self._border_tiles
            left, top = self._rect.topleft
            left -= tw
            top -= th

            # draw top and bottom tiles
            area: Optional[Tuple[int, int, int, int]]

            for x in range(border_rect.left, border_rect.right, tw):
                if x + tw >= border_rect.right:
                    area = 0, 0, tw - (x + border_rect.right), th
                else:
                    area = None
                surface_blit(tile_n, (x, top), area)
                surface_blit(tile_s, (x, border_rect.bottom - th), area)

            # draw left and right tiles
            for y in range(border_rect.top, border_rect.bottom, th):
                if y + th >= border_rect.bottom:
                    area = 0, 0, tw, th - (y + border_rect.bottom)
                else:
                    area = None
                surface_blit(tile_w, (left, y), area)
                surface_blit(tile_e, (border_rect.right - tw, y), area)

            # draw corners
            surface_blit(tile_nw, (left, top))
            surface_blit(tile_sw, (left, border_rect.bottom - th))
            surface_blit(tile_ne, (border_rect.right - tw, top))
            surface_blit(tile_se, (border_rect.right - tw, border_rect.bottom - th))

        else:  # Color
            if self._border_width == 0 or self._border_color is None:
                return self
            border_rect = pygame.Rect(
                int(self._rect.x - self._border_width),
                int(self._rect.y - self._border_width),
                int(self._rect.width + 2 * self._border_width),
                int(self._rect.height + 2 * self._border_width)
            )
            pygame.draw.rect(
                surface,
                self._border_color,
                border_rect,
                self._border_width
            )

        return self

    def get_border_size(self) -> Tuple2IntType:
        """
        Return the border size (width, height) in px.

        :return: Border width, height
        """
        if isinstance(self._border_color, pygame_menu.BaseImage):  # Image
            return self._border_tiles_size
        else:  # Color
            if self._border_color is None:
                return 0, 0
            return self._border_width, self._border_width

    def get_hidden_width(self) -> int:
        """
        Return the total width out of the bounds of the viewable area.
        Zero is returned if the world width is lower than the viewable area.

        :return: Hidden width in px
        """
        if not self._world:
            return 0
        return int(max(0, self._world.get_width() - self._view_rect.width))

    def get_hidden_height(self) -> int:
        """
        Return the total height out of the bounds of the viewable area.
        Zero is returned if the world height is lower than the viewable area.

        :return: Hidden height in px
        """
        if not self._world:
            return 0
        return int(max(0, self._world.get_height() - self._view_rect.height))

    def get_offsets(self) -> Tuple2IntType:
        """
        Return the offset introduced by the scrollbars in the world.

        :return: ScrollArea offset on x-axis and y-axis (x, y)
        """
        offsets = [0, 0]
        for sbar in self._scrollbars:
            if not sbar.is_visible():
                continue
            if sbar.get_orientation() == ORIENTATION_HORIZONTAL:
                if self.get_hidden_width():
                    offsets[0] = sbar.get_value()  # Cannot add as each scrollbar can only affect 1 axis only
            else:
                if self.get_hidden_height():
                    offsets[1] = sbar.get_value()
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

    def get_scrollbar_thickness(self, orientation: str, visible: bool = True) -> int:
        """
        Return the scroll thickness of the area. If it's hidden return zero.

        :param orientation: Orientation of the scroll. See :py:mod:`pygame_menu.locals`
        :param visible: If ``True`` returns the real thickness depending on if it is visible or not
        :return: Thickness in px
        """
        assert_orientation(orientation)
        assert isinstance(visible, bool)

        if visible:
            total = 0
            for sbar in self._scrollbars:
                if sbar.get_orientation() == orientation and sbar.is_visible():
                    total += sbar.get_thickness()
            return total

        if orientation == ORIENTATION_HORIZONTAL:
            return int(self._rect.height - self._view_rect.height)
        elif orientation == ORIENTATION_VERTICAL:
            return int(self._rect.width - self._view_rect.width)

    def get_world_rect(self, absolute: bool = False) -> 'pygame.Rect':
        """
        Return the world rect.

        :param absolute: To absolute position
        :return: World rect object
        """
        rect = self._world.get_rect()
        if absolute:
            rect = self.to_absolute_position(rect)
        return rect

    def get_view_rect(self) -> 'pygame.Rect':
        """
        Subtract width of scrollbars from area with the given size and return
        the viewable area.

        The viewable area depends on the world size, because scroll bars may or
        may not be displayed.

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
            for sbar in self._scrollbars:
                if not sbar.is_visible():
                    continue
                pos = self._scrollbar_positions[self._scrollbars.index(sbar)]
                thk = sbar.get_thickness()
                if pos == POSITION_WEST:
                    rect.left += thk
                    rect.width -= thk
                elif pos == POSITION_EAST:
                    rect.width -= thk
                elif pos == POSITION_NORTH:
                    rect.top += thk
                    rect.height -= thk
                elif pos == POSITION_SOUTH:
                    rect.height -= thk
            return rect

        # Calculate the maximum variations introduced by the scrollbars
        bars_total_width = 0
        bars_total_height = 0
        for sbar in self._scrollbars:
            if not sbar.is_visible():
                continue
            pos = self._scrollbar_positions[self._scrollbars.index(sbar)]
            thk = sbar.get_thickness()
            if pos in (POSITION_NORTH, POSITION_SOUTH):
                bars_total_height += thk
            elif pos in (POSITION_WEST, POSITION_EAST):
                bars_total_width += thk

        if self._world.get_height() > self._rect.height:
            for sbar in self._scrollbars:
                if not sbar.is_visible():
                    continue
                pos = self._scrollbar_positions[self._scrollbars.index(sbar)]
                thk = sbar.get_thickness()
                if pos == POSITION_WEST:
                    rect.left += thk
                    rect.width -= thk
                elif pos == POSITION_EAST:
                    rect.width -= thk
                if self._world.get_width() > self._rect.width - bars_total_width:
                    if pos == POSITION_NORTH:
                        rect.top += thk
                        rect.height -= thk
                    elif pos == POSITION_SOUTH:
                        rect.height -= thk

        if self._world.get_width() > self._rect.width:
            for sbar in self._scrollbars:
                if not sbar.is_visible():
                    continue
                pos = self._scrollbar_positions[self._scrollbars.index(sbar)]
                thk = sbar.get_thickness()
                if pos == POSITION_NORTH:
                    rect.top += thk
                    rect.height -= thk
                elif pos == POSITION_SOUTH:
                    rect.height -= thk
                if self._world.get_height() > self._rect.height - bars_total_height:
                    if pos == POSITION_WEST:
                        rect.left += thk
                        rect.width -= thk
                    elif pos == POSITION_EAST:
                        rect.width -= thk

        return rect

    def hide_scrollbars(self, orientation: str, force: bool = True) -> 'ScrollArea':
        """
        Hide scrollbar from given orientation.

        :param orientation: Orientation. See :py:mod:`pygame_menu.locals`
        :param force: Force hide
        :return: Self reference
        """
        assert_orientation(orientation)
        for sbar in self._scrollbars:
            if sbar.get_orientation() == orientation:
                sbar.hide(force=force)
                if not force:
                    sbar.disable_visibility_force()
        self._apply_size_changes()
        return self

    def show_scrollbars(self, orientation: str, force: bool = True) -> 'ScrollArea':
        """
        Hide scrollbar from given orientation.

        :param orientation: Orientation. See :py:mod:`pygame_menu.locals`
        :param force: Force show
        :return: Self reference
        """
        assert_orientation(orientation)
        for sbar in self._scrollbars:
            if sbar.get_orientation() == orientation:
                sbar.show(force=force)
                if not force:
                    sbar.disable_visibility_force()
        self._apply_size_changes()
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
        rect = self._view_rect if view else self._rect
        return bool(self.to_absolute_position(rect).collidepoint(*pygame.mouse.get_pos()))

    def _on_horizontal_scroll(self, value: NumberType) -> None:
        """
        Call when a horizontal scroll bar as changed to update the
        position of the opposite one if it exists.

        :param value: New position of the slider
        """
        for sbar in self._scrollbars:
            if sbar.get_orientation() == ORIENTATION_HORIZONTAL \
                    and self.get_hidden_width() != 0 \
                    and sbar.get_value() != value:
                sbar.set_value(value)

    def _on_vertical_scroll(self, value: NumberType) -> None:
        """
        Call when a vertical scroll bar as changed to update the
        position of the opposite one if it exists.

        :param value: New position of the slider
        """
        for sbar in self._scrollbars:
            if sbar.get_orientation() == ORIENTATION_VERTICAL \
                    and self.get_hidden_height() != 0 \
                    and sbar.get_value() != value:
                sbar.set_value(value)

    def get_parent_scroll_value_percentage(self, orientation: str) -> Tuple[float]:
        """
        Get percentage scroll values of scroll and parents; if ``0`` the scroll
        is at top/left, ``1`` bottom/right.

        :param orientation: Orientation. See :py:mod:`pygame_menu.locals`
        :return: Value from ``0`` to ``1`` as a tuple; first item is the current scrollarea
        """
        values = [self.get_scroll_value_percentage(orientation)]
        parent = self._parent_scrollarea
        if parent is not None:
            while True:  # Recursive
                if parent is None:
                    break
                values.append(parent.get_scroll_value_percentage(orientation))
                parent = parent._parent_scrollarea
        return tuple(values)

    def get_scroll_value_percentage(self, orientation: str) -> float:
        """
        Get the scroll value in percentage; if ``0`` the scroll is at top/left,
        ``1`` bottom/right.

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
                return sbar.get_value_percentage()
        return -1

    def scroll_to(self, orientation: str, value: NumberType) -> 'ScrollArea':
        """
        Scroll to position in terms of the percentage.

        :param orientation: Orientation. See :py:mod:`pygame_menu.locals`
        :param value: If ``0`` scrolls to top/left, ``1`` to bottom/right
        :return: Self reference
        """
        assert_orientation(orientation)
        assert isinstance(value, NumberInstance) and 0 <= value <= 1
        for sbar in self._scrollbars:
            if not sbar.is_visible():
                continue
            if sbar.get_orientation() == orientation:
                v_min, v_max = sbar.get_minmax()
                delta = v_max - v_min
                new_value = int(min(v_min + delta * float(value), v_max))
                sbar.set_value(new_value)
                break
        return self

    # noinspection PyTypeChecker
    def scroll_to_rect(
            self,
            rect: 'pygame.Rect',
            margin: Tuple2NumberType = (0, 0),
            scroll_parent: bool = True
    ) -> bool:
        """
        Ensure that the given rect is in the viewable area.

        :param rect: Rect in the world surface reference
        :param margin: Extra margin around the rect on x-axis and y-axis in px
        :param scroll_parent: If ``True`` parent scroll also scrolls to rect
        :return: Scrollarea scrolled to rect. If ``False`` the rect was already inside the visible area
        """
        # Check if visible
        if self.to_real_position(rect, visible=True).height == 0 and \
                self._parent_scrollarea is not None and scroll_parent:
            self._parent_scrollarea.scroll_to_rect(self._parent_scrollarea.get_rect(), margin, scroll_parent)
            self._parent_scrollarea.scroll_to_rect(self.get_rect(), margin, scroll_parent)

        real_rect = self.to_real_position(rect)

        # Add margin to rect
        real_rect.x += margin[0]
        real_rect.y += margin[1]

        # Check rect is in viewable area
        sx = self.get_scrollbar_thickness(ORIENTATION_VERTICAL)
        sy = self.get_scrollbar_thickness(ORIENTATION_HORIZONTAL)
        view_rect = self.get_absolute_view_rect()
        if view_rect.topleft[0] <= real_rect.topleft[0] + sx \
                and view_rect.topleft[1] <= real_rect.topleft[1] + sy \
                and view_rect.bottomright[0] + sx >= real_rect.bottomright[0] \
                and view_rect.bottomright[1] + sy >= real_rect.bottomright[1]:
            return False

        for sbar in self._scrollbars:
            if not sbar.is_visible():
                continue
            if sbar.get_orientation() == ORIENTATION_HORIZONTAL and self.get_hidden_width():
                shortest_move = min(real_rect.left - view_rect.left, real_rect.right - view_rect.right, key=abs)
                value = min(sbar.get_maximum(), sbar.get_value() + shortest_move)
                value = max(sbar.get_minimum(), value)
                sbar.set_value(value)
            if sbar.get_orientation() == ORIENTATION_VERTICAL and self.get_hidden_height():
                shortest_move = min(real_rect.bottom - view_rect.bottom, real_rect.top - view_rect.top, key=abs)
                value = min(sbar.get_maximum(), sbar.get_value() + shortest_move)
                value = max(sbar.get_minimum(), value)
                sbar.set_value(value)

        if self._parent_scrollarea is not None and scroll_parent:
            self._parent_scrollarea.scroll_to_rect(rect, margin, scroll_parent)

        return True

    def set_position(self, x: int, y: int) -> 'ScrollArea':
        """
        Set the position.

        :param x: X position
        :param y: Y position
        :return: Self reference
        """
        self._rect.x = x + self._extend_x + self._translate[0]
        self._rect.y = y + self._extend_y + self._translate[1]
        self._apply_size_changes()
        return self

    def get_position(self) -> Tuple2IntType:
        """
        Return the ScrollArea position.

        :return: X, Y position in px
        """
        return self._rect.x, self._rect.y

    def get_widget_position_relative_to_view_rect(
            self,
            widget: 'pygame_menu.widgets.Widget'
    ) -> Tuple2NumberType:
        """
        Get widget position relative to view rect on x-axis and y-axis. On each axis,
        the relative position goes from ``-inf`` to ``+inf``. If between (0, 1) the
        widget is inside the view rect.

        .. note::

            Only top-left widget position is checked.

        :param widget: Widget to check the position
        :return: Relative position to view rect on x-axis and y-axis
        """
        assert widget.get_scrollarea() == self, \
            '{0} scrollarea {1} is different than current {2}' \
                .format(widget, widget.get_scrollarea().get_class_id(), self.get_class_id())
        wx, wy = widget.get_position()
        view_rect = self.get_view_rect()
        vx, vy = view_rect.width, view_rect.height
        offx, offy = self.get_offsets()
        return (wx - offx) / vx, (wy - offy) / vy

    def translate(self, x: NumberType, y: NumberType) -> 'ScrollArea':
        """
        Translate on x-axis and y-axis (x, y) in px.

        :param x: X translation in px
        :param y: Y translation in px
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

        :return: Translation on x-axis and y-axis (x, y) in px
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

    def get_world(self) -> Optional['pygame.Surface']:
        """
        Return the world surface area.

        .. warning::

            Use with caution.

        :return: World surface. ``None`` if it has not been set yet
        """
        return self._world

    def get_parent_position(self) -> Tuple2IntType:
        """
        Return parent ScrollArea position.

        :return: Position on x, y-axis in px
        """
        if self._parent_scrollarea is not None:
            px, py = self._parent_scrollarea.get_position()
            ox, oy = self._parent_scrollarea.get_offsets()
            par_x, par_y = 0, 0
            if self._parent_scrollarea.get_parent() is not None:
                par_x, par_y = self._parent_scrollarea.get_parent_position()
            return px - ox + par_x, py - oy + par_y
        return 0, 0

    def to_absolute_position(self, virtual: 'pygame.Rect') -> 'pygame.Rect':
        """
        Return the absolute position of a rect within the ScrollArea. Absolute
        position is concerning the parent ScrollArea. If ``None``, the rect is
        not changed at all.

        .. note::

            Absolute position must be used if desired to get the widget position
            outside a scrolled area status, for example the view rect, or the
            scrollbars.

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
        its parent ScrollArea.

        :return: Clipped absolute view rect
        """
        view_rect_absolute = self.to_absolute_position(self._view_rect)
        if self._parent_scrollarea is not None:
            parent = self._parent_scrollarea
            if parent is not None:
                while True:  # Recursive
                    if parent is None:
                        break
                    view_rect_absolute = parent.get_absolute_view_rect().clip(view_rect_absolute)
                    parent = parent._parent_scrollarea
        return view_rect_absolute

    def to_real_position(
            self,
            virtual: Union['pygame.Rect', Tuple2NumberType],
            visible: bool = False
    ) -> Union['pygame.Rect', Tuple2IntType]:
        """
        Return the real position/Rect according to the ScrollArea origin of a
        position/Rect in the world surface reference.

        .. note::

            Real position must be used if desired to get the widget position within
            a scrolled area status.

        :param virtual: Position/Rect in the world surface reference
        :param visible: If a ``virtual`` is Rect object, return only the visible width/height
        :return: Real rect or real position
        """
        assert isinstance(virtual, (pygame.Rect, VectorInstance))
        offsets = self.get_offsets()
        parent_position = self.get_parent_position()

        if isinstance(virtual, pygame.Rect):
            rect = pygame.Rect(virtual)  # virtual.copy() should also work
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
        Return the position/Rect in the world surface reference of a real
        position/Rect according to the ScrollArea origin.

        .. note::

            Virtual position must be used if desired to get the widget position
            within a scrolled area status.

        :param real: Position/Rect according ScrollArea origin
        :return: Rect in world or position in world
        """
        assert isinstance(real, (pygame.Rect, VectorInstance))
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
        updated = [False, False]
        for sbar in self._scrollbars:
            if not sbar.is_visible():
                continue
            if self.get_hidden_width() and not updated[0] and \
                    sbar.get_orientation() == ORIENTATION_HORIZONTAL:
                updated[0] = sbar.update(events)
            elif self.get_hidden_height() and not updated[1] and \
                    sbar.get_orientation() == ORIENTATION_VERTICAL:
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
        If user event collides a widget within the ScrollArea respect to the
        relative position.

        :param widget: Widget or rect
        :param event: Pygame event
        :return: ``True`` if collide
        """
        if not isinstance(widget, pygame.Rect):
            widget_rect = widget.get_rect(to_real_position=True)
        else:
            widget_rect = widget
        return bool(widget_rect.collidepoint(*get_finger_pos(self._menu, event)))

    def get_decorator(self) -> 'Decorator':
        """
        Return the ScrollArea decorator API.

        .. note::

            Menu drawing order:

            1. Menu background color/image
            2. Menu ``prev`` decorator
            3. Menu **ScrollArea** ``prev`` decorator
            4. Menu **ScrollArea** widgets
            5. Menu **ScrollArea** ``post`` decorator
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
