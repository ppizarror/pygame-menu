"""
pygame-menu

ROUNDED HIGHLIGHT
Widget selection rounded highlight effect.
"""

from __future__ import annotations

__all__ = ["RoundedHighlightSelection"]

from typing import TYPE_CHECKING

import pygame

from pygame_menu.widgets.selection.highlight import HighlightSelection

if TYPE_CHECKING:
    import pygame_menu
    from pygame_menu._types import NumberType


class RoundedHighlightSelection(HighlightSelection):
    _border_radius: int

    def __init__(
        self,
        border_width: int = 1,
        border_radius: int = 8,
        margin_x: NumberType = 16,
        margin_y: NumberType = 8,
    ) -> None:
        super().__init__(
            border_width=border_width,
            margin_x=margin_x,
            margin_y=margin_y,
        )

        assert isinstance(border_radius, int)
        assert border_radius >= 0

        self._border_radius = border_radius

    def _repr_attrs(self) -> dict[str, object]:
        attrs = super()._repr_attrs()
        attrs["border_radius"] = self._border_radius
        return attrs

    def draw(
        self,
        surface: pygame.Surface,
        widget: pygame_menu.widgets.Widget,
    ) -> RoundedHighlightSelection:

        if self._border_width == 0:
            return self

        pygame.draw.rect(
            surface,
            self.color,
            self.inflate(widget.get_rect()),
            width=self._border_width,
            border_radius=self._border_radius,
        )

        return self
