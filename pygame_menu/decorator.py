"""
pygame-menu
https://github.com/ppizarror/pygame-menu

DECORATOR
Generic decorator, adds additional images, polygons or text to the object

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
# File constants no. 2000

__all__ = ['Decorator']

import pygame
import pygame_menu.baseimage as _baseimage
from pygame.font import Font
import pygame_menu.font as _fonts
import pygame.draw as pydraw
import pygame.gfxdraw as gfxdraw

import warnings
from math import pi
from pathlib import Path
from uuid import uuid4

from pygame_menu.custom_types import TYPE_CHECKING, List, Tuple2NumberType, ColorType, Tuple, \
    Any, Dict, Union, NumberType, Tuple2IntType, Optional, Callable
from pygame_menu.utils import assert_list_vector, assert_color, make_surface, is_callable, assert_vector

if TYPE_CHECKING:
    from pygame_menu.menu import Menu
    from pygame_menu.scrollarea import ScrollArea
    from pygame_menu.widgets import Widget

# Decoration constants
DECORATION_ARC = 2000
DECORATION_BASEIMAGE = 2001
DECORATION_BEZIER = 2002
DECORATION_CALLABLE = 2003
DECORATION_CIRCLE = 2004
DECORATION_ELLIPSE = 2005
DECORATION_LINE = 2006
DECORATION_NONE = 2007
DECORATION_PIE = 2008
DECORATION_PIXEL = 209
DECORATION_POLYGON = 2010
DECORATION_RECT = 2011
DECORATION_SURFACE = 2012
DECORATION_TEXT = 2013
DECORATION_TEXTURE_POLYGON = 2014

DECOR_TYPE_PREV = 'prev'
DECOR_TYPE_POST = 'post'


class Decorator(object):
    """
    Decorator class.
    """
    _coord_cache: Dict[
        str, Tuple[int, int, Union[Tuple[Tuple2NumberType, ...], Tuple2NumberType]]]  # centerx, centery, coords
    _cache_last_status: Dict[str, Tuple[int, int, int, int, int, int]]
    _cache_needs_update: Dict[str, bool]
    _cache_surface: Dict[str, Optional['pygame.Surface']]
    _decor: Dict[str, List[Tuple[int, str, Any]]]  # type, id, data
    _obj: Union['Widget', 'ScrollArea', 'Menu']
    _post_enabled: bool
    _prev_enabled: bool
    cache: bool

    def __init__(self, obj: Union['Widget', 'ScrollArea', 'Menu']) -> None:
        """
        Constructor.

        :param obj: Object
        :type obj: :py:class:`pygame_menu.widgets.core.Widget`, :py:class:`pygame_menu.Menu`, :py:class:`pygame_menu.scrollarea.ScrollArea`
        """
        self._coord_cache = {}
        self._decor = {DECOR_TYPE_PREV: [], DECOR_TYPE_POST: []}
        self._obj = obj

        self._prev_enabled = True
        self._post_enabled = True

        # If True, enables surface cache. This is intended to be used if there's many
        # decorations in the object (for example, 400). This is an expensive method anyway
        # because surface is called many times. See the following rendering times to guess
        # how much does a decoration takes time to render 1000 times (object: button)
        # 100 decoration, no cache:     0.214
        # 100 decoration, with cache:   0.646
        # 300 decoration, no cache:     0.581
        # 300 decoration, with cache:   0.606
        # 1000 decoration, no cache:    2.228
        # 1000 decoration, with cache:  0.615
        # 10000 decoration, no cache:   20.430
        # 10000 decoration, with cache: 0.599
        self.cache = False

        # Previous (surf.width, surf.height, rect.x, rect.y, rect.centerx, rect.centery
        self._cache_last_status = {DECOR_TYPE_PREV: (0, 0, 0, 0, 0, 0), DECOR_TYPE_POST: (0, 0, 0, 0, 0, 0)}
        self._cache_needs_update = {DECOR_TYPE_PREV: False, DECOR_TYPE_POST: False}
        self._cache_surface = {DECOR_TYPE_PREV: None, DECOR_TYPE_POST: None}

    def __copy__(self) -> 'Decorator':
        """
        Copy method.

        :return: Raises copy exception
        """
        raise _DecoratorCopyException('Decorator class cannot be copied')

    def __deepcopy__(self, memodict: Dict) -> 'Decorator':
        """
        Deepcopy method.

        :param memodict: Memo dict
        :return: Raises copy exception
        """
        raise _DecoratorCopyException('Decorator class cannot be deep-copied')

    def _add_decor(self, decortype: int, prev: bool, data: Any) -> str:
        """
        Add decoration.

        :param decortype: Decoration type
        :param prev: To prev or post
        :param data: Data of the decoration
        :return: ID of the decoration
        """
        decor_id = str(uuid4())

        if prev:
            assert self._prev_enabled, 'prev decorators are not enabled'
            self._decor[DECOR_TYPE_PREV].append((decortype, decor_id, data))
        else:
            assert self._post_enabled, 'post decorators are not enabled'
            self._decor[DECOR_TYPE_POST].append((decortype, decor_id, data))

        # Force surface cache update
        if hasattr(self._obj, 'force_menu_surface_cache_update'):
            self._obj.force_menu_surface_cache_update()

        # Forces cache update
        self._cache_needs_update[DECOR_TYPE_PREV if prev else DECOR_TYPE_POST] = True

        # Check sizes
        if self._total_decor() >= 300 and not self.cache:
            warnings.warn('cache is recommended if the total number of decorations exceeds 300')

        return decor_id

    def _add_none(self, prev: bool = True) -> str:
        """
        Add none decorator.

        :param prev: If ``True`` draw previous the object, else draws post
        :return: ID of the decoration
        """
        return self._add_decor(DECORATION_NONE, prev, None)

    def _total_decor(self) -> int:
        """
        Return total number of decorations.

        :return: None
        """
        return len(self._decor[DECOR_TYPE_PREV]) + len(self._decor[DECOR_TYPE_POST])

    def force_cache_update(self, prev: Optional[bool] = None) -> None:
        """
        Forces cache update.

        :param prev: Update the previous or post surface cache. If ``None`` forces both caches to update
        :return: None
        """
        if prev is None:
            self.force_cache_update(True)
            self.force_cache_update(False)
            return
        self._cache_needs_update[DECOR_TYPE_PREV if prev else DECOR_TYPE_POST] = True

    def add_polygon(self, coords: Union[List[Tuple2NumberType], Tuple[Tuple2NumberType, ...]], color: ColorType,
                    filled: bool, width: int = 0, prev: bool = True, gfx: bool = True) -> str:
        """
        Add polygon.

        :param coords: Coordinate list, being ``(0, 0)`` the center of the object
        :param color: Color of the polygon
        :param filled: If ``True`` fills the polygon with the given color
        :param width: Line border width. Only valid if ``filled=False``
        :param prev: If ``True`` draw previous the object, else draws post
        :param gfx: If ``True```uses pygame gfxdraw instead of draw
        :return: ID of the decoration
        """
        assert_list_vector(coords, 2)
        assert_color(color)
        assert len(coords) >= 3
        assert isinstance(filled, bool)
        assert isinstance(width, int) and width >= 0
        if filled:
            assert width == 0, 'width must be 0 if the polygon is filled'
            assert gfx, 'only gfxdraw support filled polygon, then gfx should be True'
        else:
            if width != 0 and gfx:
                gfx = False  # gfx don't support width
        return self._add_decor(DECORATION_POLYGON, prev, (tuple(coords), color, filled, width, gfx))

    def add_bezier(self, coords: Union[List[Tuple2NumberType], Tuple[Tuple2NumberType, ...]],
                   color: ColorType, steps: int = 5, prev: bool = True) -> str:
        """
        Add bezier curve.

        :param coords: Coordinate list, being ``(0, 0)`` the center of the object
        :param color: Color of the polygon
        :param steps: Interpolation steps
        :param prev: If ``True`` draw previous the object, else draws post
        :return: ID of the decoration
        """
        assert_list_vector(coords, 2)
        assert_color(color)
        assert len(coords) >= 3
        assert isinstance(steps, int) and steps >= 1
        return self._add_decor(DECORATION_BEZIER, prev, (tuple(coords), color, steps))

    def add_circle(self, x: NumberType, y: NumberType, radius: NumberType, color: ColorType, filled: bool,
                   width: int = 0, prev: bool = True, gfx: bool = True) -> str:
        """
        Add circle.

        :param x: X position (px), being ``0`` the center of the object
        :param y: Y position (px), being ``0`` the center of the object
        :param radius: Circle radius (px)
        :param color: Color of the polygon
        :param filled: If ``True`` fills the polygon with the given color
        :param width: Line border width. Only valid if ``filled=False``
        :param prev: If ``True`` draw previous the object, else draws post
        :param gfx: If ``True```uses pygame gfxdraw instead of draw
        :return: ID of the decoration
        """
        coords = [(x, y)]
        assert_list_vector(coords, 2)
        assert_color(color)
        assert isinstance(radius, (int, float)) and radius > 0
        assert isinstance(filled, bool)
        assert isinstance(width, int) and width >= 0
        if filled:
            assert width == 0, 'width must be 0 if the circle is filled'
        else:
            if width != 0 and gfx:
                gfx = False  # gfx don't support width
        return self._add_decor(DECORATION_CIRCLE, prev, (tuple(coords), int(radius), color, filled, width, gfx))

    def add_arc(self, x: NumberType, y: NumberType, radius: NumberType,
                init_angle: NumberType, final_angle: NumberType, color: ColorType,
                width: int = 0, prev: bool = True, gfx: bool = True) -> str:
        """
        Add arc.

        :param x: X position (px), being ``0`` the center of the object
        :param y: Y position (px), being ``0`` the center of the object
        :param radius: Circle radius (px)
        :param init_angle: Initial angle in degrees ``(0-360)``
        :param final_angle: Final angle in degrees ``(0-360)``
        :param color: Color of the polygon
        :param width: Line border width. Only valid if ``filled=False``
        :param prev: If ``True`` draw previous the object, else draws post
        :param gfx: If ``True```uses pygame gfxdraw instead of draw
        :return: ID of the decoration
        """
        coords = [(x, y)]
        assert_list_vector(coords, 2)
        assert_color(color)
        assert isinstance(radius, (int, float)) and radius > 0
        assert isinstance(init_angle, (int, float))
        assert isinstance(final_angle, (int, float))
        assert isinstance(width, int) and width >= 0
        assert init_angle != final_angle
        return self._add_decor(DECORATION_ARC, prev, (tuple(coords), int(radius), init_angle, final_angle,
                                                      color, width, gfx))

    def add_pie(self, x: NumberType, y: NumberType, radius: NumberType,
                init_angle: NumberType, final_angle: NumberType, color: ColorType,
                prev: bool = True) -> str:
        """
        Add a unfilled pie.

        :param x: X position (px), being ``0`` the center of the object
        :param y: Y position (px), being ``0`` the center of the object
        :param radius: Circle radius (px)
        :param init_angle: Initial angle in degrees ``(0-360)``
        :param final_angle: Final angle in degrees ``(0-360)``
        :param color: Color of the polygon
        :param prev: If ``True`` draw previous the object, else draws post
        :return: ID of the decoration
        """
        coords = [(x, y)]
        assert_list_vector(coords, 2)
        assert_color(color)
        assert isinstance(radius, (int, float)) and radius > 0
        assert isinstance(init_angle, (int, float))
        assert isinstance(final_angle, (int, float))
        assert init_angle != final_angle
        return self._add_decor(DECORATION_PIE, prev, (tuple(coords), int(radius), init_angle, final_angle, color))

    def add_surface(self, x: NumberType, y: NumberType, surface: 'pygame.Surface',
                    prev: bool = True, centered: bool = False) -> str:
        """
        Adds a surface.

        :param x: X position (px), being ``0`` the center of the object
        :param y: Y position (px), being ``0`` the center of the object
        :param surface: Surface
        :param prev: If ``True`` draw previous the object, else draws post
        :param centered: If ``True`` the text is centered into the position
        :return: ID of the decoration
        """
        coords = [(x, y)]
        assert_list_vector(coords, 2)
        assert isinstance(surface, pygame.Surface)
        return self._add_decor(DECORATION_SURFACE, prev, (tuple(coords), surface, centered))

    def add_baseimage(self, x: NumberType, y: NumberType, image: '_baseimage.BaseImage',
                      prev: bool = True, centered: bool = False) -> str:
        """
        Adds a :py:class:`pygame_menu.baseimage.BaseImage` object.

        .. note::

            If your :py:class:`pygame_menu.baseimage.BaseImage` object changes over time
            set ``decorator.cache=False`` or force cache manually by calling
            :py:class:`pygame_menu.decorator.Decorator.force_cache_update`.

        :param x: X position (px), being ``0`` the center of the object
        :param y: Y position (px), being ``0`` the center of the object
        :param image: ``BaseImage`` object
        :param prev: If ``True`` draw previous the object, else draws post
        :param centered: If ``True`` the text is centered into the position
        :return: ID of the decoration
        """
        coords = [(x, y)]
        assert_list_vector(coords, 2)
        assert isinstance(image, _baseimage.BaseImage)
        return self._add_decor(DECORATION_BASEIMAGE, prev, (tuple(coords), image, centered))

    def add_rect(self, x: NumberType, y: NumberType, rect: 'pygame.Rect', color: ColorType, width: int = 0,
                 prev: bool = True) -> str:
        """
        Adds a BaseImage object.

        :param x: X position (px), being ``0`` the center of the object
        :param y: Y position (px), being ``0`` the center of the object
        :param rect: Rect to draw
        :param color: Color of the rect
        :param width: Width of the rect. If ``0`` draw a filled rectangle
        :param prev: If ``True`` draw previous the object, else draws post
        :return: ID of the decoration
        """
        coords = [(x, y)]
        assert_list_vector(coords, 2)
        assert isinstance(rect, pygame.Rect)
        return self._add_decor(DECORATION_RECT, prev, (tuple(coords), rect, color, width))

    def add_text(self, x: NumberType, y: NumberType, text: str, font: Union[str, 'Font', 'Path'], size: int,
                 color: ColorType, prev: bool = True, antialias=True, centered=False) -> str:
        """
        Adds a text.

        :param x: X position (px), being ``0`` the center of the object
        :param y: Y position (px), being ``0`` the center of the object
        :param text: Text to draw
        :param font: Font path or pygame object
        :param size: Size of the font to render
        :param color: Font color
        :param prev: If ``True`` draw previous the object, else draws post
        :param antialias: Font antialias enabled
        :param centered: If ``True`` the text is centered into the position
        :return: ID of the decoration
        """
        coords = [(x, y)]
        assert_list_vector(coords, 2)
        text = str(text)
        font_obj = _fonts.get_font(font, size)
        surface_font = font_obj.render(text, antialias, color)
        surface = make_surface(
            width=surface_font.get_width(),
            height=surface_font.get_height(),
            alpha=True
        )
        surface.blit(surface_font, (0, 0))
        return self._add_decor(DECORATION_TEXT, prev, (tuple(coords), surface, centered))

    def add_ellipse(self, x: NumberType, y: NumberType, rx: NumberType, ry: NumberType, color: ColorType,
                    filled: bool, prev: bool = True) -> str:
        """
        Add an ellipse.

        :param x: X position (px), being ``0`` the center of the object
        :param y: Y position (px), being ``0`` the center of the object
        :param rx: Horizontal radius of the ellipse
        :param ry: Vertical radius of the ellipse
        :param color: Color of the polygon
        :param filled: If ``True`` fills the polygon with the given color
        :param prev: If ``True`` draw previous the object, else draws post
        :return: ID of the decoration
        """
        coords = [(x, y)]
        assert_list_vector(coords, 2)
        assert_color(color)
        assert isinstance(rx, (int, float)) and rx > 0
        assert isinstance(ry, (int, float)) and ry > 0
        assert isinstance(filled, bool)
        return self._add_decor(DECORATION_ELLIPSE, prev, (tuple(coords), rx, ry, color, filled))

    def add_pixel(self, x: NumberType, y: NumberType, color: ColorType, prev: bool = True) -> str:
        """
        Add a pixel.

        :param x: X position (px), being ``0`` the center of the object
        :param y: Y position (px), being ``0`` the center of the object
        :param color: Color of the pixel
        :param prev: If ``True`` draw previous the object, else draws post
        :return: ID of the decoration
        """
        coords = [(x, y)]
        assert_list_vector(coords, 2)
        assert_color(color)
        return self._add_decor(DECORATION_PIXEL, prev, (tuple(coords), color))

    def add_callable(self, fun: Callable[['pygame.Surface', Any], Any], prev: bool = True) -> str:
        """
        Add a callable method. The function receives the surface and the object.

        .. note::

            If your callable function changes over time set ``decorator.cache=False``
            or force cache manually by calling Decorator method
            :py:class:`pygame_menu.decorator.Decorator.force_cache_update`.

        :param fun: Function
        :param prev: If ``True`` draw previous the object, else draws post
        :return: ID of the decoration
        """
        assert is_callable(fun), 'fun must be a callable type'
        return self._add_decor(DECORATION_CALLABLE, prev, fun)

    def add_textured_polygon(self, coords: Union[List[Tuple2NumberType], Tuple[Tuple2NumberType, ...]],
                             texture: Union['pygame.Surface', '_baseimage.BaseImage'],
                             tx: int = 0, ty: int = 0, prev: bool = True) -> str:
        """
        Add a textured polygon.

        .. note::

            If your :py:class:`pygame_menu.baseimage.BaseImage` object changes over time
            set ``decorator.cache=False`` or force cache manually by calling
            :py:class:`pygame_menu.decorator.Decorator.force_cache_update`.

        :param coords: Coordinate list, being ``(0, 0)`` the center of the object
        :param texture: Texture (Surface) or Baseimage object
        :param tx: X offset of the texture (px)
        :param ty: Y offset of the texture (px)
        :param prev: If ``True`` draw previous the object, else draws post
        :return: ID of the decoration
        """
        assert_list_vector(coords, 2)
        assert len(coords) >= 3
        assert isinstance(texture, (pygame.Surface, _baseimage.BaseImage))
        assert isinstance(tx, int) and isinstance(ty, int)
        return self._add_decor(DECORATION_TEXTURE_POLYGON, prev, (tuple(coords), texture, tx, ty))

    def add_line(self, pos1: Tuple2NumberType, pos2: Tuple2NumberType, color: ColorType, width: int = 1,
                 prev: bool = True) -> str:
        """
        Adds a line.

        :param pos1: Position 1 *(x1, y1)*
        :param pos2: Position 2 *(x2, y2)*
        :param color: Line color
        :param width: Line width in px
        :param prev: If ``True`` draw previous the object, else draws post
        :return: ID of the decoration
        """
        assert_vector(pos1, 2)
        assert_vector(pos2, 2)
        assert_color(color)
        assert isinstance(width, int) and width >= 1
        return self._add_decor(DECORATION_LINE, prev, ((tuple(pos1), tuple(pos2)), color, width))

    def add_hline(self, x1: NumberType, x2: NumberType, y: NumberType, color: ColorType, width: int = 1,
                  prev: bool = True) -> str:
        """
        Adds a horizontal line.

        :param x1: Horizontal position 1 in px
        :param x2: Horizontal position 2 in px
        :param y: Vertical position in px
        :param color: Line color
        :param width: Line width in px
        :param prev: If ``True`` draw previous the object, else draws post
        :return: ID of the decoration
        """
        assert x1 != x2
        return self.add_line((x1, y), (x2, y), color, width, prev)

    def add_vline(self, x: NumberType, y1: NumberType, y2: NumberType, color: ColorType, width: int = 1,
                  prev: bool = True) -> str:
        """
        Adds a vertical line.

        :param x: Horizontal position in px
        :param y1: Vertical position 1 in px
        :param y2: Vertical position 2 in px
        :param color: Line color
        :param width: Line width in px
        :param prev: If ``True`` draw previous the object, else draws post
        :return: ID of the decoration
        """
        assert y1 != y2
        return self.add_line((x, y1), (x, y2), color, width, prev)

    def remove(self, decorid: str) -> None:
        """
        Remove a decoration from a given ID. Raises ``IndexError`` if decoration was
        not found.

        :param decorid: Decoration ID
        :return: None
        """
        assert isinstance(decorid, str)
        if decorid in self._coord_cache.keys():
            del self._coord_cache[decorid]
        for p in (DECOR_TYPE_PREV, DECOR_TYPE_POST):
            for d in self._decor[p]:
                if d[1] == decorid:
                    self._decor[p].remove(d)
                    self._cache_needs_update[p] = True
                    return
        raise IndexError('decoration ID "{0}" was not found'.format(decorid))

    def remove_all(self, prev: Optional[bool] = None) -> None:
        """
        Remove all decorations.

        :param prev: Remove from ``prev`` or ``post``. If ``None`` both are removed
        :return: None
        """
        if prev is None:
            self.remove_all(True)
            self.remove_all(False)
            return
        p = DECOR_TYPE_PREV if prev else DECOR_TYPE_POST
        self._cache_needs_update[p] = False
        del self._decor[p]
        self._decor[p] = []

    def _draw_assemble_cache(self, prev: str, deco: List[Tuple[int, str, Any]], surface: 'pygame.Surface') -> None:
        """
        Draw cache, assemble if needed.

        :param prev: Mode
        :param deco: Decoration lists
        :param surface: Source surface to draw from
        :return: None
        """
        if len(deco) == 0:
            return

        w, h = surface.get_size()
        rect = self._obj.get_rect()

        # If needs update, or the surface size changed, or the rect position changed
        prev_surf_changed = self._cache_last_status[prev][0] != w or self._cache_last_status[prev][1] != h
        prev_rect_changed = self._cache_last_status[prev][2] != rect.x or \
                            self._cache_last_status[prev][3] != rect.y or \
                            self._cache_last_status[prev][4] != rect.width or \
                            self._cache_last_status[prev][5] != rect.height

        if self._cache_needs_update[prev] or prev_surf_changed or prev_rect_changed or \
                self._cache_surface[prev] is None:
            self._cache_last_status[prev] = (w, h, rect.x, rect.y, rect.width, rect.height)
            del self._cache_surface[prev]
            self._cache_surface[prev] = make_surface(surface.get_width(), surface.get_height())
            self._draw(deco, self._cache_surface[prev])
            self._cache_needs_update[prev] = False

        surface.blit(self._cache_surface[prev], (0, 0))

    def draw_prev(self, surface: 'pygame.Surface') -> None:
        """
        Draw prev.

        :param surface: Pygame surface
        :return: None
        """
        if not self.cache:
            self._draw(self._decor[DECOR_TYPE_PREV], surface)
        else:
            self._draw_assemble_cache(DECOR_TYPE_PREV, self._decor[DECOR_TYPE_PREV], surface)

    def draw_post(self, surface: 'pygame.Surface') -> None:
        """
        Draw post.

        :param surface: Pygame surface
        :return: None
        """
        if not self.cache:
            self._draw(self._decor[DECOR_TYPE_POST], surface)
        else:
            self._draw_assemble_cache(DECOR_TYPE_POST, self._decor[DECOR_TYPE_POST], surface)

    def _draw(self, deco: List[Tuple[int, str, Any]], surface: 'pygame.Surface') -> None:
        """
        Draw.

        :param deco: Decoration list
        :param surface: Pygame surface
        :return: None
        """
        if len(deco) == 0:
            return
        rect = self._obj.get_rect()
        for d in deco:
            dtype, decoid, data = d

            if dtype == DECORATION_POLYGON:
                points, color, filled, width, gfx = data
                points = self._update_pos_list(rect, decoid, points)
                if gfx:
                    if filled:
                        gfxdraw.filled_polygon(surface, points, color)
                    else:
                        gfxdraw.polygon(surface, points, color)
                else:
                    pydraw.polygon(surface, color, points, width)

            elif dtype == DECORATION_CIRCLE:
                points, r, color, filled, width, gfx = data
                points = self._update_pos_list(rect, decoid, points)
                x, y = points[0]
                if filled:
                    if gfx:
                        gfxdraw.filled_circle(surface, x, y, r, color)
                    else:
                        pydraw.circle(surface, color, (x, y), r)
                else:
                    pydraw.circle(surface, color, (x, y), r, width)

            elif dtype == DECORATION_SURFACE or dtype == DECORATION_BASEIMAGE or dtype == DECORATION_TEXT:
                pos, surf, centered = data
                if isinstance(surf, _baseimage.BaseImage):
                    surf = surf.get_surface(new=False)
                pos = self._update_pos_list(rect, decoid, pos)[0]
                surfrect = surf.get_rect()
                surfrect.x += pos[0]
                surfrect.y += pos[1]
                if centered:
                    surfrect.x -= surfrect.width / 2
                    surfrect.y -= surfrect.height / 2
                surface.blit(surf, surfrect)

            elif dtype == DECORATION_ELLIPSE:
                pos, rx, ry, color, filled = data
                pos = self._update_pos_list(rect, decoid, pos)[0]
                if filled:
                    gfxdraw.filled_ellipse(surface, pos[0], pos[1], rx, ry, color)
                else:
                    gfxdraw.ellipse(surface, pos[0], pos[1], rx, ry, color)

            elif dtype == DECORATION_CALLABLE:
                data(surface, self._obj)

            elif dtype == DECORATION_TEXTURE_POLYGON:
                pos, texture, tx, ty = data
                pos = self._update_pos_list(rect, decoid, pos)
                if isinstance(texture, _baseimage.BaseImage):
                    texture = texture.get_surface()
                gfxdraw.textured_polygon(surface, pos, texture, tx, ty)

            elif dtype == DECORATION_ARC:
                points, r, ia, fa, color, width, gfx = data
                points = self._update_pos_list(rect, decoid, points)
                x, y = points[0]
                rectarc = pygame.Rect(x - r, y - r, x + 2 * r, y + 2 * r)
                if gfx:
                    gfxdraw.arc(surface, x, y, r, ia, fa, color)
                else:
                    pydraw.arc(surface, color, rectarc, ia / (2 * pi), fa / (2 * pi), width)

            elif dtype == DECORATION_PIE:
                points, r, ia, fa, color = data
                points = self._update_pos_list(rect, decoid, points)
                x, y = points[0]
                gfxdraw.pie(surface, x, y, r, ia, fa, color)

            elif dtype == DECORATION_BEZIER:
                points, color, steps = data
                points = self._update_pos_list(rect, decoid, points)
                gfxdraw.bezier(surface, points, steps, color)

            elif dtype == DECORATION_RECT:
                drect: 'pygame.Rect'
                pos, drect, color, width = data
                pos = self._update_pos_list(rect, decoid, pos)[0]
                drect = drect.copy()
                drect.x += pos[0]
                drect.y += pos[1]
                pygame.draw.rect(surface, color, drect, width)

            elif dtype == DECORATION_PIXEL:
                pos, color = data
                pos = self._update_pos_list(rect, decoid, pos)[0]
                gfxdraw.pixel(surface, pos[0], pos[1], color)

            elif dtype == DECORATION_LINE:
                pos, color, width = data
                pos = self._update_pos_list(rect, decoid, pos)
                pydraw.line(surface, color, pos[0], pos[1], width)

            else:
                raise ValueError('unknown decoration type')

    def _update_pos_list(self,
                         rect: 'pygame.rect.Rect',
                         decoid: str,
                         pos: Union[Tuple2NumberType, Tuple[Tuple2NumberType, ...]]  # only (x, y) or ((x1,y1), ...
                         ) -> Union[Tuple[Tuple2IntType, ...], Tuple2IntType]:
        """
        Updates position list based on rect center. If position of the rect changes, update
        the coords.

        :param rect: Object precomputed rect
        :param decoid: Decoration id
        :param pos: Original position tuple of the decoration
        :return: Position list updated to
        """
        cx, cy = rect.centerx, rect.centery  # Center position

        # Position of the rect has not changed and exists
        decoid_exists = False
        try:
            decoid_exists = self._coord_cache[decoid] is not None
        except KeyError:
            pass
        if decoid_exists and self._coord_cache[decoid][0] == cx and self._coord_cache[decoid][1] == cy:
            return self._coord_cache[decoid][2]

        # Update the position
        new_pos = []
        for p in pos:
            new_pos.append((int(p[0] + cx), int(p[1] + cy)))
        new_pos = tuple(new_pos)
        self._coord_cache[decoid] = (cx, cy, new_pos)
        return new_pos


class _DecoratorCopyException(Exception):
    """
    If user tries to copy a Decorator.
    """
    pass
