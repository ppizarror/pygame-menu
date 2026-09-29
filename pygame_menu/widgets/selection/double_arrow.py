"""
pygame-menu

DOUBLE ARROW
Widget selection double-arrow effect.
"""

from __future__ import annotations

__all__ = ["DoubleArrowSelection"]

from typing import TYPE_CHECKING

from pygame_menu._types import NumberInstance, NumberType, Tuple2IntType
from pygame_menu.widgets.selection.arrow_selection import ArrowSelection

if TYPE_CHECKING:
    import pygame

    import pygame_menu


class DoubleArrowSelection(ArrowSelection):
    _arrow_margin: int

    def __init__(
        self,
        arrow_size: Tuple2IntType = (10, 15),
        arrow_margin: int = 5,
        arrow_vertical_offset: int = 0,
        blink_ms: NumberType = 0,
    ) -> None:

        assert isinstance(arrow_margin, NumberInstance)
        assert arrow_margin >= 0

        super().__init__(
            margin_left=arrow_size[0] + arrow_margin,
            margin_right=arrow_size[0] + arrow_margin,
            margin_top=0,
            margin_bottom=0,
            arrow_size=arrow_size,
            arrow_vertical_offset=arrow_vertical_offset,
            blink_ms=blink_ms,
        )

        self._arrow_margin = arrow_margin

    def _repr_attrs(self) -> dict[str, object]:
        attrs = super()._repr_attrs()
        attrs["arrow_margin"] = self._arrow_margin
        return attrs

    def draw(
        self,
        surface: pygame.Surface,
        widget: pygame_menu.widgets.Widget,
    ) -> DoubleArrowSelection:

        rect = widget.get_rect()

        # LEFT
        la = (
            rect.left - self._arrow_size[0] - self._arrow_margin,
            rect.centery - self._arrow_size[1] // 2,
        )

        lb = (
            rect.left - self._arrow_margin,
            rect.centery,
        )

        lc = (
            rect.left - self._arrow_size[0] - self._arrow_margin,
            rect.centery + self._arrow_size[1] // 2,
        )

        # RIGHT
        ra = (
            rect.right + self._arrow_size[0] + self._arrow_margin,
            rect.centery - self._arrow_size[1] // 2,
        )

        rb = (
            rect.right + self._arrow_margin,
            rect.centery,
        )

        rc = (
            rect.right + self._arrow_size[0] + self._arrow_margin,
            rect.centery + self._arrow_size[1] // 2,
        )

        super()._draw_arrow(surface, widget, la, lb, lc)
        super()._draw_arrow(surface, widget, ra, rb, rc)

        return self
