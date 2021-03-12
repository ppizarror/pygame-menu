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

from math import pi
import math

import pygame
import pygame_menu
import pygame_menu.menu
import pygame.draw as pydraw
import pygame.gfxdraw as gfxdraw

from pygame_menu._base import Base
from pygame_menu.font import FontType
from pygame_menu.utils import assert_list_vector, assert_color, make_surface, \
    is_callable, assert_vector, uuid4, warn

from pygame_menu._types import List, Tuple2NumberType, ColorInputType, Tuple, \
    Any, Dict, Union, NumberType, Tuple2IntType, Optional, Callable, NumberInstance

# Decoration constants
DECORATION_ARC = 2000
DECORATION_BASEIMAGE = 2001
DECORATION_BEZIER = 2002
DECORATION_CALLABLE = 2003
DECORATION_CALLABLE_NO_ARGS = 2015
DECORATION_CIRCLE = 2004
DECORATION_ELLIPSE = 2005
DECORATION_FILL = 2020
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


# noinspection PyProtectedMember
class Decorator(Base):
    """
    Decorator class.

    :param obj: Object to decorate
    :param decorator_id: ID of the decorator
    """
    _coord_cache: Dict[
        str, Tuple[int, int, Union[Tuple[Tuple2NumberType, ...], Tuple2NumberType]]]  # centerx, centery, coords
    _cache_last_status: Dict[str, Tuple[int, int, int, int, int, int]]
    _cache_needs_update: Dict[str, bool]
    _cache_surface: Dict[str, Optional['pygame.Surface']]
    _decor: Dict[str, List[Tuple[int, str, Any]]]  # type, id, data
    _decor_enabled: Dict[str, bool]
    _decor_prev_id: List[str]
    _obj: Union['pygame_menu.widgets.Widget', 'pygame_menu._scrollarea.ScrollArea', 'pygame_menu.Menu']
    _post_enabled: bool
    _prev_enabled: bool
    cache: bool

    def __init__(
            self,
            obj: Union['pygame_menu.widgets.Widget', 'pygame_menu._scrollarea.ScrollArea', 'pygame_menu.Menu'],
            decorator_id: str = ''
    ) -> None:
        super(Decorator, self).__init__(object_id=decorator_id)

        self._coord_cache = {}
        self._decor = {DECOR_TYPE_PREV: [], DECOR_TYPE_POST: []}
        self._decor_prev_id = []  # Stores all decoration prev ids
        self._obj = obj
        self._decor_enabled = {}

        self._prev_enabled = True
        self._post_enabled = True

        # If True, enables surface cache. This is intended to be used if there's
        # many decorations in the object (for example, 400). This is an expensive
        # method anyway because surface is called many times. See the following
        # rendering times to guess how much does a decoration takes time to
        # render 1000 times (object: button)
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
        self._cache_last_status = {DECOR_TYPE_PREV: (0, 0, 0, 0, 0, 0),
                                   DECOR_TYPE_POST: (0, 0, 0, 0, 0, 0)}
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
        Adds a decoration.

        :param decortype: Decoration type
        :param prev: To prev or post
        :param data: Data of the decoration
        :return: ID of the decoration
        """
        decor_id = uuid4()

        if prev:
            assert self._prev_enabled, 'prev decorators are not enabled'
            self._decor[DECOR_TYPE_PREV].append((decortype, decor_id, data))
            self._decor_prev_id.append(decor_id)
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
            warn('cache is recommended if the total number of decorations exceeds 300')

        # Set automatically as enabled
        self._decor_enabled[decor_id] = True

        return decor_id

    def _add_none(self, prev: bool = True) -> str:
        """
        Adds a none decorator.

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

    def force_cache_update(self, prev: Optional[bool] = None) -> 'Decorator':
        """
        Forces cache update.

        :param prev: Update the previous or post surface cache. If ``None`` forces both caches to update
        :return: Self reference
        """
        if prev is None:
            self.force_cache_update(True)
            self.force_cache_update(False)
            return self
        self._cache_needs_update[DECOR_TYPE_PREV if prev else DECOR_TYPE_POST] = True
        return self

    def add_polygon(
            self,
            coords: Union[List[Tuple2NumberType], Tuple[Tuple2NumberType, ...]],
            color: ColorInputType,
            filled: bool,
            width: int = 0,
            prev: bool = True,
            gfx: bool = True,
            **kwargs
    ) -> str:
        """
        Adds a polygon.

        kwargs (Optional)
            - ``use_center_positioning``    (bool) – Uses object center position as *(0, 0)*. ``True`` by default

        :param coords: Coordinate list, being ``(0, 0)`` the center of the object
        :param color: Color of the polygon
        :param filled: If ``True`` fills the polygon with the given color
        :param width: Line border width. Only valid if ``filled=False``
        :param prev: If ``True`` draw previous the object, else draws post
        :param gfx: If ``True`` uses pygame gfxdraw instead of draw
        :param kwargs: Optional keyword arguments
        :return: ID of the decoration
        """
        assert_list_vector(coords, 2)
        color = assert_color(color)
        assert len(coords) >= 3
        assert isinstance(filled, bool)
        assert isinstance(width, int) and width >= 0
        if filled:
            assert width == 0, 'width must be 0 if the polygon is filled'
            assert gfx, 'only gfxdraw support filled polygon, then gfx should be True'
        else:
            if width != 0 and gfx:
                gfx = False  # gfx don't support width
        return self._add_decor(
            DECORATION_POLYGON, prev, (tuple(coords), color, filled, width, gfx, kwargs)
        )

    def add_bezier(
            self,
            coords: Union[List[Tuple2NumberType], Tuple[Tuple2NumberType, ...]],
            color: ColorInputType,
            steps: int = 5,
            prev: bool = True,
            **kwargs
    ) -> str:
        """
        Adds a bezier curve.

        kwargs (Optional)
            - ``use_center_positioning``    (bool) – Uses object center position as *(0, 0)*. ``True`` by default

        :param coords: Coordinate list, being ``(0, 0)`` the center of the object
        :param color: Color of the polygon
        :param steps: Interpolation steps
        :param prev: If ``True`` draw previous the object, else draws post
        :param kwargs: Optional keyword arguments
        :return: ID of the decoration
        """
        assert_list_vector(coords, 2)
        color = assert_color(color)
        assert len(coords) >= 3
        assert isinstance(steps, int) and steps >= 1
        return self._add_decor(
            DECORATION_BEZIER, prev, (tuple(coords), color, steps, kwargs)
        )

    def add_circle(
            self,
            x: NumberType,
            y: NumberType,
            radius: NumberType,
            color: ColorInputType,
            filled: bool,
            width: int = 0,
            prev: bool = True,
            gfx: bool = True,
            **kwargs
    ) -> str:
        """
        Adds a circle.

        kwargs (Optional)
            - ``use_center_positioning``    (bool) – Uses object center position as *(0, 0)*. ``True`` by default

        :param x: X position in px, being ``0`` the center of the object
        :param y: Y position in px, being ``0`` the center of the object
        :param radius: Circle radius in px
        :param color: Color of the polygon
        :param filled: If ``True`` fills the polygon with the given color
        :param width: Line border width. Only valid if ``filled=False``
        :param prev: If ``True`` draw previous the object, else draws post
        :param gfx: If ``True`` uses pygame gfxdraw instead of draw
        :param kwargs: Optional keyword arguments
        :return: ID of the decoration
        """
        coords = [(x, y)]
        assert_list_vector(coords, 2)
        color = assert_color(color)
        assert isinstance(radius, NumberInstance) and radius > 0
        assert isinstance(filled, bool)
        assert isinstance(width, int) and width >= 0
        if filled:
            assert width == 0, 'width must be 0 if the circle is filled'
        else:
            if width != 0 and gfx:
                gfx = False  # gfx don't support width
        return self._add_decor(
            DECORATION_CIRCLE, prev,
            (tuple(coords), int(radius), color, filled, width, gfx, kwargs)
        )

    def add_arc(
            self,
            x: NumberType,
            y: NumberType,
            radius: NumberType,
            init_angle: NumberType,
            final_angle: NumberType,
            color: ColorInputType,
            width: int = 0,
            prev: bool = True,
            gfx: bool = True,
            **kwargs
    ) -> str:
        """
        Adds an arc.

        kwargs (Optional)
            - ``use_center_positioning``    (bool) – Uses object center position as *(0, 0)*. ``True`` by default

        :param x: X position in px, being ``0`` the center of the object
        :param y: Y position in px, being ``0`` the center of the object
        :param radius: Circle radius in px
        :param init_angle: Initial angle in degrees, from ``0`` to ``360``
        :param final_angle: Final angle in degrees, from ``0`` to ``360``
        :param color: Color of the polygon
        :param width: Line border width. Only valid if ``filled=False``
        :param prev: If ``True`` draw previous the object, else draws post
        :param gfx: If ``True`` uses pygame gfxdraw instead of draw
        :param kwargs: Optional keyword arguments
        :return: ID of the decoration
        """
        coords = [(x, y)]
        assert_list_vector(coords, 2)
        color = assert_color(color)
        assert isinstance(radius, NumberInstance) and radius > 0
        assert isinstance(init_angle, NumberInstance)
        assert isinstance(final_angle, NumberInstance)
        assert isinstance(width, int) and width >= 0
        assert init_angle != final_angle
        return self._add_decor(
            DECORATION_ARC, prev,
            (tuple(coords), int(radius), init_angle, final_angle, color, width,
             gfx, kwargs)
        )

    def add_pie(
            self,
            x: NumberType,
            y: NumberType,
            radius: NumberType,
            init_angle: NumberType,
            final_angle: NumberType,
            color: ColorInputType,
            prev: bool = True,
            **kwargs
    ) -> str:
        """
        Adds a unfilled pie.

        kwargs (Optional)
            - ``use_center_positioning``    (bool) – Uses object center position as *(0, 0)*. ``True`` by default

        :param x: X position in px, being ``0`` the center of the object
        :param y: Y position in px, being ``0`` the center of the object
        :param radius: Circle radius in px
        :param init_angle: Initial angle in degrees, from ``0`` to ``360``
        :param final_angle: Final angle in degrees, from ``0`` to ``360``
        :param color: Color of the polygon
        :param prev: If ``True`` draw previous the object, else draws post
        :param kwargs: Optional keyword arguments
        :return: ID of the decoration
        """
        coords = [(x, y)]
        assert_list_vector(coords, 2)
        color = assert_color(color)
        assert isinstance(radius, NumberInstance) and radius > 0
        assert isinstance(init_angle, NumberInstance)
        assert isinstance(final_angle, NumberInstance)
        assert init_angle != final_angle
        return self._add_decor(
            DECORATION_PIE, prev,
            (tuple(coords), int(radius), init_angle, final_angle, color, kwargs)
        )

    def add_surface(
            self,
            x: NumberType,
            y: NumberType,
            surface: 'pygame.Surface',
            prev: bool = True,
            centered: bool = False,
            **kwargs
    ) -> str:
        """
        Adds a surface.

        kwargs (Optional)
            - ``use_center_positioning``    (bool) – Uses object center position as *(0, 0)*. ``True`` by default

        :param x: X position in px, being ``0`` the center of the object
        :param y: Y position in px, being ``0`` the center of the object
        :param surface: Surface
        :param prev: If ``True`` draw previous the object, else draws post
        :param centered: If ``True`` the surface is centered
        :param kwargs: Optional keyword arguments
        :return: ID of the decoration
        """
        coords = [(x, y)]
        assert_list_vector(coords, 2)
        assert isinstance(surface, pygame.Surface)
        return self._add_decor(
            DECORATION_SURFACE, prev,
            (tuple(coords), surface, centered, kwargs)
        )

    def add_baseimage(
            self,
            x: NumberType,
            y: NumberType,
            image: 'pygame_menu.BaseImage',
            prev: bool = True,
            centered: bool = False,
            **kwargs
    ) -> str:
        """
        Adds a :py:class:`pygame_menu.baseimage.BaseImage` object.

        .. note::

            If your :py:class:`pygame_menu.baseimage.BaseImage` object changes over time
            set ``decorator.cache=False`` or force cache manually by calling
            :py:meth:`pygame_menu._decorator.Decorator.force_cache_update`.

        kwargs (Optional)
            - ``use_center_positioning``    (bool) – Uses object center position as *(0, 0)*. ``True`` by default

        :param x: X position in px, being ``0`` the center of the object
        :param y: Y position in px, being ``0`` the center of the object
        :param image: ``BaseImage`` object
        :param prev: If ``True`` draw previous the object, else draws post
        :param centered: If ``True`` the image is centered
        :param kwargs: Optional keyword arguments
        :return: ID of the decoration
        """
        coords = [(x, y)]
        assert_list_vector(coords, 2)
        assert isinstance(image, pygame_menu.BaseImage)
        return self._add_decor(
            DECORATION_BASEIMAGE, prev, (tuple(coords), image, centered, kwargs)
        )

    def add_rect(
            self,
            x: NumberType,
            y: NumberType,
            rect: 'pygame.Rect',
            color: ColorInputType,
            width: int = 0,
            prev: bool = True,
            **kwargs
    ) -> str:
        """
        Adds a BaseImage object.

        kwargs (Optional)
            - ``use_center_positioning``    (bool) – Uses object center position as *(0, 0)*. ``True`` by default

        :param x: X position in px, being ``0`` the center of the object
        :param y: Y position in px, being ``0`` the center of the object
        :param rect: Rect to draw
        :param color: Color of the rect
        :param width: Border width of the rect. If ``0`` draw a filled rectangle
        :param prev: If ``True`` draw previous the object, else draws post
        :param kwargs: Optional keyword arguments
        :return: ID of the decoration
        """
        assert isinstance(width, int) and width >= 0
        coords = [(x, y)]
        assert_list_vector(coords, 2)
        color = assert_color(color)
        assert isinstance(rect, pygame.Rect)
        return self._add_decor(
            DECORATION_RECT, prev, (tuple(coords), rect, color, width, kwargs)
        )

    def add_rectangle(
            self,
            x: NumberType,
            y: NumberType,
            width: NumberType,
            height: NumberType,
            color: ColorInputType,
            border: int = 0,
            prev: bool = True,
            **kwargs
    ) -> str:
        """
        Adds a BaseImage object.

        kwargs (Optional)
            - ``use_center_positioning``    (bool) – Uses object center position as *(0, 0)*. ``True`` by default

        :param x: X position in px, being ``0`` the center of the object
        :param y: Y position in px, being ``0`` the center of the object
        :param width: Rectangle width
        :param height: Rectangle height
        :param color: Color of the rectangle
        :param border: Border width of the rectangle. If ``0`` draw a filled rectangle
        :param prev: If ``True`` draw previous the object, else draws post
        :param kwargs: Optional keyword arguments
        :return: ID of the decoration
        """
        assert isinstance(width, NumberInstance) and width > 0
        assert isinstance(height, NumberInstance) and height > 0
        rect = pygame.Rect(0, 0, width, height)
        return self.add_rect(x, y, rect, color, border, prev, **kwargs)

    def add_text(
            self,
            x: NumberType,
            y: NumberType,
            text: str,
            font: FontType,
            size: int,
            color: ColorInputType,
            prev: bool = True,
            antialias=True,
            centered=False,
            **kwargs
    ) -> str:
        """
        Adds a text.

        kwargs (Optional)
            - ``use_center_positioning``    (bool) – Uses object center position as *(0, 0)*. ``True`` by default

        :param x: X position in px, being ``0`` the center of the object
        :param y: Y position in px, being ``0`` the center of the object
        :param text: Text to draw
        :param font: Font path or pygame object
        :param size: Size of the font to render
        :param color: Font color
        :param prev: If ``True`` draw previous the object, else draws post
        :param antialias: Font antialias enabled
        :param centered: If ``True`` the text is centered
        :param kwargs: Optional keyword arguments
        :return: ID of the decoration
        """
        coords = [(x, y)]
        assert_list_vector(coords, 2)
        text = str(text)
        font_obj = pygame_menu.font.get_font(font, size)
        color = assert_color(color)
        surface_font = font_obj.render(text, antialias, color)
        surface = make_surface(
            width=surface_font.get_width(),
            height=surface_font.get_height(),
            alpha=True
        )
        surface.blit(surface_font, (0, 0))
        return self._add_decor(
            DECORATION_TEXT, prev, (tuple(coords), surface, centered, kwargs)
        )

    def add_ellipse(
            self,
            x: NumberType,
            y: NumberType,
            rx: NumberType,
            ry: NumberType,
            color: ColorInputType,
            filled: bool,
            prev: bool = True,
            **kwargs
    ) -> str:
        """
        Adds an ellipse.

        kwargs (Optional)
            - ``use_center_positioning``    (bool) – Uses object center position as *(0, 0)*. ``True`` by default

        :param x: X position in px, being ``0`` the center of the object
        :param y: Y position in px, being ``0`` the center of the object
        :param rx: Horizontal radius of the ellipse
        :param ry: Vertical radius of the ellipse
        :param color: Color of the polygon
        :param filled: If ``True`` fills the polygon with the given color
        :param prev: If ``True`` draw previous the object, else draws post
        :param kwargs: Optional keyword arguments
        :return: ID of the decoration
        """
        coords = [(x, y)]
        assert_list_vector(coords, 2)
        color = assert_color(color)
        assert isinstance(rx, NumberInstance) and rx > 0
        assert isinstance(ry, NumberInstance) and ry > 0
        assert isinstance(filled, bool)
        return self._add_decor(
            DECORATION_ELLIPSE, prev, (tuple(coords), rx, ry, color, filled, kwargs)
        )

    def add_pixel(
            self,
            x: NumberType,
            y: NumberType,
            color: ColorInputType,
            prev: bool = True,
            **kwargs
    ) -> str:
        """
        Adds a pixel.

        kwargs (Optional)
            - ``use_center_positioning``    (bool) – Uses object center position as *(0, 0)*. ``True`` by default

        :param x: X position in px, being ``0`` the center of the object
        :param y: Y position in px, being ``0`` the center of the object
        :param color: Color of the pixel
        :param prev: If ``True`` draw previous the object, else draws post
        :param kwargs: Optional keyword arguments
        :return: ID of the decoration
        """
        coords = [(x, y)]
        assert_list_vector(coords, 2)
        color = assert_color(color)
        return self._add_decor(
            DECORATION_PIXEL, prev, (tuple(coords), color, kwargs)
        )

    def add_callable(
            self,
            fun: Union[Callable[['pygame.Surface', Any], Any], Callable[[], Any]],
            prev: bool = True,
            pass_args: bool = True
    ) -> str:
        """
        Adds a callable method. The function receives the surface and the object;
        for example, if adding to a widget:

        .. code-block:: python

            fun(surface, object)

        .. note::

            If your callable function changes over time set ``decorator.cache=False``
            or force cache manually by calling Decorator method
            :py:meth:`pygame_menu._decorator.Decorator.force_cache_update`. Also,
            the object should force the menu surface cache to update.

        :param fun: Function
        :param prev: If ``True`` draw previous the object, else draws post
        :param pass_args: If ``False`` function is called without (surface, object) as args
        :return: ID of the decoration
        """
        assert is_callable(fun), 'fun must be a callable type'
        assert isinstance(pass_args, bool)
        if pass_args:
            return self._add_decor(DECORATION_CALLABLE, prev, fun)
        else:
            return self._add_decor(DECORATION_CALLABLE_NO_ARGS, prev, fun)

    def add_textured_polygon(
            self,
            coords: Union[List[Tuple2NumberType], Tuple[Tuple2NumberType, ...]],
            texture: Union['pygame.Surface', 'pygame_menu.BaseImage'],
            tx: int = 0,
            ty: int = 0,
            prev: bool = True,
            **kwargs
    ) -> str:
        """
        Adds a textured polygon.

        .. note::

            If your :py:class:`pygame_menu.baseimage.BaseImage` object changes over
            time set ``decorator.cache=False`` or force cache manually by calling
            :py:class:`pygame_menu._decorator.Decorator.force_cache_update`.

        kwargs (Optional)
            - ``use_center_positioning``    (bool) – Uses object center position as *(0, 0)*. ``True`` by default

        :param coords: Coordinate list, being ``(0, 0)`` the center of the object
        :param texture: Texture (Surface) or Baseimage object
        :param tx: X offset of the texture in px
        :param ty: Y offset of the texture in px
        :param prev: If ``True`` draw previous the object, else draws post
        :param kwargs: Optional keyword arguments
        :return: ID of the decoration
        """
        assert_list_vector(coords, 2)
        assert len(coords) >= 3
        assert isinstance(texture, (pygame.Surface, pygame_menu.BaseImage))
        assert isinstance(tx, int) and isinstance(ty, int)
        return self._add_decor(
            DECORATION_TEXTURE_POLYGON, prev, (tuple(coords), texture, tx, ty, kwargs)
        )

    def add_line(
            self,
            pos1: Tuple2NumberType,
            pos2: Tuple2NumberType,
            color: ColorInputType,
            width: int = 1,
            prev: bool = True,
            **kwargs
    ) -> str:
        """
        Adds a line.

        kwargs (Optional)
            - ``use_center_positioning``    (bool) – Uses object center position as *(0, 0)*. ``True`` by default

        :param pos1: Position 1 (x1, y1)
        :param pos2: Position 2 (x2, y2)
        :param color: Line color
        :param width: Line width in px
        :param prev: If ``True`` draw previous the object, else draws post
        :param kwargs: Optional keyword arguments
        :return: ID of the decoration
        """
        assert_vector(pos1, 2)
        assert_vector(pos2, 2)
        color = assert_color(color)
        assert isinstance(width, int) and width >= 1
        length = math.sqrt(math.pow(pos1[0] - pos2[0], 2) + math.pow(pos1[1] - pos2[1], 2))
        assert length > 0, 'line cannot be zero-length'
        return self._add_decor(
            DECORATION_LINE, prev, ((tuple(pos1), tuple(pos2)), color, width, kwargs)
        )

    def add_fill(
            self,
            color: ColorInputType,
            prev: bool = True
    ) -> str:
        """
        Fills the decorator rect object.

        kwargs (Optional)
            - ``use_center_positioning``    (bool) – Uses object center position as *(0, 0)*. ``True`` by default

        :param color: Fill color
        :param prev: If ``True`` draw previous the object, else draws post
        :return: ID of the decoration
        """
        return self._add_decor(DECORATION_FILL, prev, assert_color(color))

    def add_hline(
            self,
            x1: NumberType,
            x2: NumberType,
            y: NumberType,
            color: ColorInputType,
            width: int = 1,
            prev: bool = True,
            **kwargs
    ) -> str:
        """
        Adds a horizontal line.

        kwargs (Optional)
            - ``use_center_positioning``    (bool) – Uses object center position as *(0, 0)*. ``True`` by default

        :param x1: Horizontal position 1 in px
        :param x2: Horizontal position 2 in px
        :param y: Vertical position in px
        :param color: Line color
        :param width: Line width in px
        :param prev: If ``True`` draw previous the object, else draws post
        :param kwargs: Optional keyword arguments
        :return: ID of the decoration
        """
        assert x1 != x2
        return self.add_line((x1, y), (x2, y), color, width, prev, **kwargs)

    def add_vline(
            self,
            x: NumberType,
            y1: NumberType,
            y2: NumberType,
            color: ColorInputType,
            width: int = 1,
            prev: bool = True,
            **kwargs
    ) -> str:
        """
        Adds a vertical line.

        kwargs (Optional)
            - ``use_center_positioning``    (bool) – Uses object center position as *(0, 0)*. ``True`` by default

        :param x: Horizontal position in px
        :param y1: Vertical position 1 in px
        :param y2: Vertical position 2 in px
        :param color: Line color
        :param width: Line width in px
        :param prev: If ``True`` draw previous the object, else draws post
        :param kwargs: Optional keyword arguments
        :return: ID of the decoration
        """
        assert y1 != y2
        return self.add_line((x, y1), (x, y2), color, width, prev, **kwargs)

    def disable(self, decorid: str) -> 'Decorator':
        """
        Disable a certain decoration from ID. Raises ``IndexError`` if decoration was
        not found.

        :param decorid: Decoration ID
        :return: Self reference
        """
        if decorid not in self._decor_enabled.keys():
            raise IndexError('decoration<"{0}"> was not found'.format(decorid))
        self._decor_enabled[decorid] = False
        self.force_cache_update(prev=decorid in self._decor_prev_id)
        return self

    def enable(self, decorid: str) -> 'Decorator':
        """
        Enable a certain decoration from ID. Raises ``IndexError`` if decoration
        was not found.

        :param decorid: Decoration ID
        :return: Self reference
        """
        if decorid not in self._decor_enabled.keys():
            raise IndexError('decoration<"{0}"> was not found'.format(decorid))
        self._decor_enabled[decorid] = True
        self.force_cache_update(prev=decorid in self._decor_prev_id)
        return self

    def remove(self, decorid: str) -> 'Decorator':
        """
        Remove a decoration from a given ID. Raises ``IndexError`` if decoration
        was not found.

        :param decorid: Decoration ID
        :return: Self reference
        """
        assert isinstance(decorid, str)
        if decorid in self._coord_cache.keys():
            del self._coord_cache[decorid]
        for p in (DECOR_TYPE_PREV, DECOR_TYPE_POST):
            for d in self._decor[p]:
                if d[1] == decorid:
                    self._decor[p].remove(d)
                    self._cache_needs_update[p] = True
                    if decorid in self._decor_prev_id:
                        self._decor_prev_id.remove(decorid)
                    del self._decor_enabled[decorid]
                    return self
        raise IndexError('decoration<"{0}"> was not found'.format(decorid))

    def remove_all(self, prev: Optional[bool] = None) -> 'Decorator':
        """
        Remove all decorations.

        :param prev: Remove from ``prev`` or ``post``. If ``None`` both are removed
        :return: Self reference
        """
        if prev is None:
            self.remove_all(True)
            self.remove_all(False)
            return self
        p = DECOR_TYPE_PREV if prev else DECOR_TYPE_POST
        self._cache_needs_update[p] = False
        del self._decor[p]
        self._decor[p] = []
        return self

    def _draw_assemble_cache(
            self,
            prev: str,
            deco: List[Tuple[int, str, Any]],
            surface: 'pygame.Surface'
    ) -> None:
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
        prev_surf_changed = self._cache_last_status[prev][0] != w or \
                            self._cache_last_status[prev][1] != h
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

    def draw_prev(self, surface: 'pygame.Surface') -> 'Decorator':
        """
        Draw prev.

        :param surface: Pygame surface
        :return: Self reference
        """
        if not self.cache:
            self._draw(self._decor[DECOR_TYPE_PREV], surface)
        else:
            self._draw_assemble_cache(DECOR_TYPE_PREV, self._decor[DECOR_TYPE_PREV], surface)
        return self

    def draw_post(self, surface: 'pygame.Surface') -> 'Decorator':
        """
        Draw post.

        :param surface: Pygame surface
        :return: Self reference
        """
        if not self.cache:
            self._draw(self._decor[DECOR_TYPE_POST], surface)
        else:
            self._draw_assemble_cache(DECOR_TYPE_POST, self._decor[DECOR_TYPE_POST], surface)
        return self

    # noinspection PyArgumentList
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
            if not self._decor_enabled[decoid]:
                continue

            if dtype == DECORATION_POLYGON:
                points, color, filled, width, gfx, kwargs = data
                points = self._update_pos_list(rect, decoid, points, **kwargs)
                if gfx:
                    if filled:
                        gfxdraw.filled_polygon(surface, points, color)
                    else:
                        gfxdraw.polygon(surface, points, color)
                else:
                    pydraw.polygon(surface, color, points, width)

            elif dtype == DECORATION_CIRCLE:
                points, r, color, filled, width, gfx, kwargs = data
                points = self._update_pos_list(rect, decoid, points, **kwargs)
                x, y = points[0]
                if filled:
                    if gfx:
                        gfxdraw.filled_circle(surface, x, y, r, color)
                    else:
                        pydraw.circle(surface, color, (x, y), r)
                else:
                    pydraw.circle(surface, color, (x, y), r, width)

            elif dtype == DECORATION_SURFACE or dtype == DECORATION_BASEIMAGE or dtype == DECORATION_TEXT:
                pos, surf, centered, kwargs = data
                if isinstance(surf, pygame_menu.BaseImage):
                    surf = surf.get_surface(new=False)
                pos = self._update_pos_list(rect, decoid, pos, **kwargs)[0]
                surfrect = surf.get_rect()
                surfrect.x += pos[0]
                surfrect.y += pos[1]
                if centered:
                    surfrect.x -= surfrect.width / 2
                    surfrect.y -= surfrect.height / 2
                surface.blit(surf, surfrect)

            elif dtype == DECORATION_ELLIPSE:
                pos, rx, ry, color, filled, kwargs = data
                pos = self._update_pos_list(rect, decoid, pos, **kwargs)[0]
                if filled:
                    gfxdraw.filled_ellipse(surface, pos[0], pos[1], rx, ry, color)
                else:
                    gfxdraw.ellipse(surface, pos[0], pos[1], rx, ry, color)

            elif dtype == DECORATION_CALLABLE:
                data(surface, self._obj)

            elif dtype == DECORATION_CALLABLE_NO_ARGS:
                data()

            elif dtype == DECORATION_TEXTURE_POLYGON:
                pos, texture, tx, ty, kwargs = data
                pos = self._update_pos_list(rect, decoid, pos, **kwargs)
                if isinstance(texture, pygame_menu.BaseImage):
                    texture = texture.get_surface()
                gfxdraw.textured_polygon(surface, pos, texture, tx, ty)

            elif dtype == DECORATION_ARC:
                points, r, ia, fa, color, width, gfx, kwargs = data
                points = self._update_pos_list(rect, decoid, points, **kwargs)
                x, y = points[0]
                rect_arc = pygame.Rect(x - r, y - r, x + 2 * r, y + 2 * r)
                if gfx:
                    gfxdraw.arc(surface, x, y, r, ia, fa, color)
                else:
                    pydraw.arc(surface, color, rect_arc, ia / (2 * pi), fa / (2 * pi), width)

            elif dtype == DECORATION_PIE:
                points, r, ia, fa, color, kwargs = data
                points = self._update_pos_list(rect, decoid, points, **kwargs)
                x, y = points[0]
                gfxdraw.pie(surface, x, y, r, ia, fa, color)

            elif dtype == DECORATION_BEZIER:
                points, color, steps, kwargs = data
                points = self._update_pos_list(rect, decoid, points, **kwargs)
                gfxdraw.bezier(surface, points, steps, color)

            elif dtype == DECORATION_FILL:
                surface.fill(data, rect)

            elif dtype == DECORATION_RECT:
                drect: 'pygame.Rect'
                pos, drect, color, width, kwargs = data
                pos = self._update_pos_list(rect, decoid, pos, **kwargs)[0]
                drect = drect.copy()
                drect.x += pos[0]
                drect.y += pos[1]
                pygame.draw.rect(surface, color, drect, width)

            elif dtype == DECORATION_PIXEL:
                pos, color, kwargs = data
                pos = self._update_pos_list(rect, decoid, pos, **kwargs)[0]
                gfxdraw.pixel(surface, pos[0], pos[1], color)

            elif dtype == DECORATION_LINE:
                pos, color, width, kwargs = data
                pos = self._update_pos_list(rect, decoid, pos, **kwargs)
                pydraw.line(surface, color, pos[0], pos[1], width)

            else:
                raise ValueError('unknown decoration type')

    def _update_pos_list(
            self,
            rect: 'pygame.Rect',
            decoid: str,
            pos: Union[Tuple2NumberType, Tuple[Tuple2NumberType, ...]],  # only (x, y) or ((x1,y1), ...
            use_center_positioning=True
    ) -> Union[Tuple[Tuple2IntType, ...], Tuple2IntType]:
        """
        Updates position list based on rect center. If position of the rect changes,
        update the coords.

        :param rect: Object precomputed rect
        :param decoid: Decoration id
        :param pos: Original position tuple of the decoration
        :param use_center_positioning: If ``True`` use *(0, 0)* as the object center
        :return: Position list updated to
        """
        if not use_center_positioning:
            return tuple(pos)
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
