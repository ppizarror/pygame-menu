"""
pygame-menu
https://github.com/ppizarror/pygame-menu

UTILS
Utility functions.
"""

from __future__ import annotations

__all__ = ["ShadowGenerator"]

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from pygame_menu._types import Tuple3IntType


class ShadowGenerator:
    """
    A class to generate surfaces that work as a 'shadow' for rectangular and ellipse UI elements.
    Base shadows are generated procedurally, cached, and scaled for optimal performance.

    Source: https://github.com/MyreMylar/pygame_gui (with custom modifications for
    opacity, offsets, and robust caching).
    """

    _created_ellipse_shadows: dict[str, pygame.Surface]
    _preloaded_shadow_corners: dict[str, dict[str, pygame.Surface]]
    _short_term_rect_cache: dict[str, pygame.Surface]

    def __init__(self) -> None:
        self._created_ellipse_shadows = {}
        self._preloaded_shadow_corners = {}
        self._short_term_rect_cache = {}

    def clear_short_term_caches(self, force: bool = False) -> None:
        """
        Empties short term caches, so we aren't hanging on to so many surfaces.

        :param force: Force clear
        """
        t = (
            len(self._created_ellipse_shadows)
            + len(self._preloaded_shadow_corners)
            + len(self._short_term_rect_cache)
        )
        if t >= 100 or force:
            self._created_ellipse_shadows.clear()
            self._preloaded_shadow_corners.clear()
            self._short_term_rect_cache.clear()

    def _create_shadow_corners(
        self,
        shadow_width_param: int,
        corner_radius_param: int,
        color: Tuple3IntType,
        aa_amount: int = 4,
        opacity: float = 1.0,
    ) -> dict[str, pygame.Surface]:
        """
        Create corners for our rectangular shadows. These can be used across many
        sizes of shadow with the same shadow width and corner radius.

        :param shadow_width_param: Width of the shadow
        :param corner_radius_param: Corner radius of the shadow
        :param color: Shadow color
        :param aa_amount: Anti-aliasing amount. Defaults to 4x
        :param opacity: Shadow opacity multiplier
        :return: Dict that contain the shadows of each border
        """
        shadow_width_param = max(1, shadow_width_param)

        corner_rect = pygame.Rect(
            0, 0, corner_radius_param * aa_amount, corner_radius_param * aa_amount
        )

        corner_surface, edge_surface = self._create_single_corner_and_edge(
            aa_amount=aa_amount,
            corner_radius_param=corner_radius_param,
            corner_rect=corner_rect,
            shadow_width_param=shadow_width_param,
            color=color,
            opacity=opacity,
        )

        sub_radius = (corner_radius_param - shadow_width_param) * aa_amount
        top_edge = pygame.transform.smoothscale(
            edge_surface, (shadow_width_param, shadow_width_param)
        )
        left_edge = pygame.transform.rotate(top_edge, 90)

        tl_corner = pygame.transform.smoothscale(
            corner_surface, (corner_radius_param, corner_radius_param)
        )

        if sub_radius > 0:
            corner_sub_surface = pygame.surface.Surface(
                corner_rect.size, flags=pygame.SRCALPHA, depth=32
            )
            corner_sub_surface.fill(pygame.Color("#00000000"))

            pygame.draw.circle(
                corner_sub_surface,
                pygame.Color("#FFFFFFFF"),
                corner_rect.size,
                sub_radius,
            )

            corner_small_sub_surface = pygame.transform.smoothscale(
                corner_sub_surface, (corner_radius_param, corner_radius_param)
            )

            tl_corner.blit(
                corner_small_sub_surface, (0, 0), special_flags=pygame.BLEND_RGBA_SUB
            )

        corners_and_edges = {
            "bottom": pygame.transform.flip(top_edge, False, True),
            "bottom_left": pygame.transform.flip(tl_corner, False, True),
            "bottom_right": pygame.transform.flip(tl_corner, True, True),
            "left": left_edge,
            "right": pygame.transform.flip(left_edge, True, False),
            "top": top_edge,
            "top_left": tl_corner,
            "top_right": pygame.transform.flip(tl_corner, True, False),
        }

        r, g, b = color
        cache_key = f"{shadow_width_param}x{corner_radius_param}_{r}_{g}_{b}_{opacity}"
        self._preloaded_shadow_corners[cache_key] = corners_and_edges
        return corners_and_edges

    @staticmethod
    def _create_single_corner_and_edge(
        aa_amount: int,
        corner_radius_param: int,
        corner_rect: pygame.Rect,
        shadow_width_param: int,
        color: Tuple3IntType,
        opacity: float = 1.0,
    ) -> tuple[pygame.Surface, pygame.Surface]:
        """
        Creates a single corner surface and a single edge surface for a shadow.

        :param aa_amount: Amount of antialiasing
        :param corner_radius_param: Radius of a corner this shadow will go around
        :param corner_rect: Rectangular size of corner
        :param shadow_width_param: Width of shadow
        :param color: Shadow color
        :param opacity: Shadow opacity multiplier
        :return: A tuple of the corner surface and the edge surface
        """
        aa_amount = max(1, aa_amount)
        final_corner_surface = pygame.surface.Surface(
            (corner_radius_param * aa_amount, corner_radius_param * aa_amount),
            flags=pygame.SRCALPHA,
            depth=32,
        )
        final_corner_surface.fill(pygame.Color("#00000000"))
        final_edge_surface = pygame.surface.Surface(
            (shadow_width_param * aa_amount, shadow_width_param * aa_amount),
            flags=pygame.SRCALPHA,
            depth=32,
        )
        final_edge_surface.fill(pygame.Color("#00000000"))

        corner_radius = corner_radius_param * aa_amount
        corner_centre = (corner_radius, corner_radius)
        edge_rect = pygame.Rect(
            0, 0, shadow_width_param * aa_amount, shadow_width_param * aa_amount
        )
        edge_shadow_fade_height = edge_rect.width

        alpha_increment = (20.0 / (shadow_width_param**1.5)) * opacity
        shadow_alpha = alpha_increment
        r, g, b = color

        for _ in range(shadow_width_param):
            if corner_rect.width > 0 and corner_rect.height > 0 and corner_radius > 0:
                # Edge
                edge_shadow_surface = pygame.surface.Surface(
                    edge_rect.size, flags=pygame.SRCALPHA, depth=32
                )
                edge_shadow_surface.fill(pygame.Color("#00000000"))
                edge_shadow_surface.fill(
                    pygame.Color(r, g, b, int(min(255, max(0, shadow_alpha)))),
                    pygame.Rect(
                        0,
                        edge_rect.height - edge_shadow_fade_height,
                        edge_rect.width,
                        edge_shadow_fade_height,
                    ),
                )

                final_edge_surface.blit(
                    edge_shadow_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD
                )

                # Corner
                corner_shadow_surface = pygame.surface.Surface(
                    corner_rect.size, flags=pygame.SRCALPHA, depth=32
                )
                corner_shadow_surface.fill(pygame.Color("#00000000"))
                pygame.draw.circle(
                    corner_shadow_surface,
                    pygame.Color(r, g, b, int(min(255, max(0, shadow_alpha)))),
                    corner_centre,
                    corner_radius,
                )

                final_corner_surface.blit(
                    corner_shadow_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD
                )

                # increments/decrements
                shadow_alpha += alpha_increment
                corner_radius -= aa_amount
                edge_shadow_fade_height -= aa_amount

        return final_corner_surface, final_edge_surface

    def create_new_rectangle_shadow(
        self,
        width: int,
        height: int,
        shadow_width_param: int,
        corner_radius_param: int,
        aa_amount: int = 4,
        color: Tuple3IntType = (0, 0, 0),
        offset_x: int = 0,
        offset_y: int = 0,
        opacity: float = 1.0,
    ) -> pygame.Surface | None:
        """
        Creates a rectangular shadow surface at the specified size and stores it for later use.

        :param width: The width of the base shadow to create
        :param height: The height of the base shadow to create
        :param shadow_width_param: The width of the shadowed edge
        :param corner_radius_param: The radius of the rectangular shadow's corners
        :param aa_amount: Antialiasing
        :param color: Shadow color (r, g, b)
        :param offset_x: Horizontal shadow offset
        :param offset_y: Vertical shadow offset
        :param opacity: Shadow opacity multiplier
        :return: Shadow surface or None
        """
        assert isinstance(width, int)
        assert isinstance(height, int)
        shadow_width_param, corner_radius_param, aa_amount = (
            int(shadow_width_param),
            int(corner_radius_param),
            int(aa_amount),
        )
        if (
            width < corner_radius_param
            or height < corner_radius_param
            or shadow_width_param == 0
        ):
            return None

        r, g, b = color
        # Robust cache key including all state parameters
        params = [
            width,
            height,
            shadow_width_param,
            corner_radius_param,
            aa_amount,
            r,
            g,
            b,
            offset_x,
            offset_y,
            opacity,
        ]
        shadow_id = "_".join(str(param) for param in params)

        if shadow_id in self._short_term_rect_cache:
            return self._short_term_rect_cache[shadow_id]

        final_surface = pygame.surface.Surface(
            (width, height), flags=pygame.SRCALPHA, depth=32
        )
        final_surface.fill(pygame.Color("#00000000"))

        corner_index_id = (
            f"{shadow_width_param}x{corner_radius_param}_{r}_{g}_{b}_{opacity}"
        )
        if corner_index_id in self._preloaded_shadow_corners:
            edges_and_corners = self._preloaded_shadow_corners[corner_index_id]
        else:
            edges_and_corners = self._create_shadow_corners(
                shadow_width_param=shadow_width_param,
                corner_radius_param=corner_radius_param,
                color=color,
                aa_amount=aa_amount,
                opacity=opacity,
            )

        # Apply drawing with directional offsets
        blit_x = max(0, offset_x)
        blit_y = max(0, offset_y)

        final_surface.blit(edges_and_corners["top_left"], (blit_x, blit_y))
        final_surface.blit(
            edges_and_corners["top_right"],
            (width - corner_radius_param + blit_x, blit_y),
        )
        final_surface.blit(
            edges_and_corners["bottom_left"],
            (blit_x, height - corner_radius_param + blit_y),
        )
        final_surface.blit(
            edges_and_corners["bottom_right"],
            (
                width - corner_radius_param + blit_x,
                height - corner_radius_param + blit_y,
            ),
        )

        if width - (2 * corner_radius_param) > 0:
            top_edge = pygame.transform.scale(
                edges_and_corners["top"],
                (width - (2 * corner_radius_param), shadow_width_param),
            )
            bottom_edge = pygame.transform.scale(
                edges_and_corners["bottom"],
                (width - (2 * corner_radius_param), shadow_width_param),
            )
            final_surface.blit(top_edge, (corner_radius_param + blit_x, blit_y))
            final_surface.blit(
                bottom_edge,
                (corner_radius_param + blit_x, height - shadow_width_param + blit_y),
            )

        if height - (2 * corner_radius_param) > 0:
            left_edge = pygame.transform.scale(
                edges_and_corners["left"],
                (shadow_width_param, height - (2 * corner_radius_param)),
            )
            right_edge = pygame.transform.scale(
                edges_and_corners["right"],
                (shadow_width_param, height - (2 * corner_radius_param)),
            )
            final_surface.blit(left_edge, (blit_x, corner_radius_param + blit_y))
            final_surface.blit(
                right_edge,
                (width - shadow_width_param + blit_x, corner_radius_param + blit_y),
            )

        self._short_term_rect_cache[shadow_id] = final_surface
        return final_surface

    def create_new_ellipse_shadow(
        self,
        width: int,
        height: int,
        shadow_width_param: int,
        aa_amount: int = 4,
        color: Tuple3IntType = (0, 0, 0),
        offset_x: int = 0,
        offset_y: int = 0,
        opacity: float = 1.0,
    ) -> pygame.Surface | None:
        """
        Creates an ellipse shaped shadow surface at the specified size and stores it for later use.

        :param width: The width of the shadow to create
        :param height: The height of the shadow to create
        :param shadow_width_param: The width of the shadowed edge
        :param aa_amount: The amount of antialiasing to use, defaults to 4
        :param color: Shadow color (r, g, b)
        :param offset_x: Horizontal shadow offset
        :param offset_y: Vertical shadow offset
        :param opacity: Shadow opacity multiplier
        :return: Surface with shadow or None
        """
        assert isinstance(width, int)
        assert isinstance(height, int)
        shadow_width_param, aa_amount = int(shadow_width_param), int(aa_amount)
        if shadow_width_param == 0:
            return None

        r, g, b = color
        ellipse_id = f"{width}x{height}x{shadow_width_param}_{aa_amount}_{r}_{g}_{b}_{offset_x}_{offset_y}_{opacity}"
        if ellipse_id in self._created_ellipse_shadows:
            return self._created_ellipse_shadows[ellipse_id]

        shadow_surface = pygame.surface.Surface(
            (width * aa_amount, height * aa_amount), flags=pygame.SRCALPHA, depth=32
        )
        shadow_surface.fill(pygame.Color("#00000000"))

        alpha_increment = max(1.0, (20.0 / shadow_width_param) * opacity)
        shadow_alpha = alpha_increment
        shadow_width = width * aa_amount
        shadow_height = height * aa_amount

        blit_x = max(0, offset_x) * aa_amount
        blit_y = max(0, offset_y) * aa_amount

        for i in range(shadow_width_param):
            if shadow_width > 0 and shadow_height > 0:
                shadow_rect = pygame.Rect(
                    (i * aa_amount) + blit_x,
                    (i * aa_amount) + blit_y,
                    shadow_width,
                    shadow_height,
                )
                pygame.draw.ellipse(
                    shadow_surface,
                    pygame.Color(r, g, b, int(min(255, max(0, shadow_alpha)))),
                    shadow_rect,
                )
                shadow_width -= 2 * aa_amount
                shadow_height -= 2 * aa_amount
                shadow_alpha += alpha_increment

        final_surface = pygame.transform.smoothscale(shadow_surface, (width, height))
        self._created_ellipse_shadows[ellipse_id] = final_surface
        return final_surface
