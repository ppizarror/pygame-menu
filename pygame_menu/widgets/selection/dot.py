"""
pygame-menu

DOT
Widget selection dot indicator.
"""

from __future__ import annotations

__all__ = ["DotSelection"]

from typing import TYPE_CHECKING

import pygame

from pygame_menu._types import NumberInstance, NumberType
from pygame_menu.widgets.core import Selection

if TYPE_CHECKING:
    import pygame_menu


class DotSelection(Selection):
    """
    Widget selection dot indicator.

    Draws a filled circle to the left of the selected widget.

    :param radius: Dot radius in px
    :param margin: Distance between widget and dot
    :param vertical_offset: Dot vertical offset
    """

    _radius: int
    _margin: int
    _vertical_offset: int

    def __init__(
        self,
        radius: int = 5,
        margin: NumberType = 6,
        vertical_offset: NumberType = 0,
    ) -> None:
        assert isinstance(radius, int)
        assert radius > 0

        assert isinstance(margin, NumberInstance)
        assert margin >= 0

        assert isinstance(vertical_offset, NumberInstance)

        super().__init__(
            margin_left=radius * 2 + margin,
            margin_right=0,
            margin_top=0,
            margin_bottom=0,
        )

        self._radius = radius
        self._margin = int(margin)
        self._vertical_offset = int(vertical_offset)

    def _repr_attrs(self) -> dict[str, object]:
        attrs = super()._repr_attrs()

        attrs.update(
            {
                "radius": self._radius,
                "margin": self._margin,
                "vertical_offset": self._vertical_offset,
            }
        )

        return attrs

    def draw(
        self,
        surface: pygame.Surface,
        widget: pygame_menu.widgets.Widget,
    ) -> DotSelection:
        rect = widget.get_rect()

        center = (
            rect.left - self._margin - self._radius,
            rect.centery + self._vertical_offset,
        )

        pygame.draw.circle(
            surface,
            self.color,
            center,
            self._radius,
        )

        return self
