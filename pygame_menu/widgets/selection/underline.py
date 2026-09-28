"""
pygame-menu

UNDERLINE
Widget selection underline effect.
"""

from __future__ import annotations

__all__ = ["UnderlineSelection"]

from typing import TYPE_CHECKING

import pygame

from pygame_menu.widgets.core import Selection

if TYPE_CHECKING:
    import pygame_menu
    from pygame_menu._types import NumberType


class UnderlineSelection(Selection):
    """
    Widget selection underline effect.

    :param line_width: Underline thickness in px
    :param margin: Distance from widget bottom to underline
    :param line_length_offset: Additional underline length
    """

    _line_width: int
    _margin: int
    _line_length_offset: int

    def __init__(
        self,
        line_width: int = 2,
        margin: NumberType = 4,
        line_length_offset: NumberType = 0,
    ) -> None:
        assert isinstance(line_width, int)
        assert line_width > 0

        assert margin >= 0
        assert line_length_offset >= 0

        super().__init__(
            margin_left=0,
            margin_right=0,
            margin_top=0,
            margin_bottom=line_width + margin,
        )

        self._line_width = line_width
        self._margin = int(margin)
        self._line_length_offset = int(line_length_offset)

    def _repr_attrs(self) -> dict[str, object]:
        attrs = super()._repr_attrs()

        attrs.update(
            {
                "line_width": self._line_width,
                "margin": self._margin,
                "line_length_offset": self._line_length_offset,
            }
        )

        return attrs

    def draw(
        self,
        surface: pygame.Surface,
        widget: pygame_menu.widgets.Widget,
    ) -> UnderlineSelection:
        rect = widget.get_rect()

        start = (
            rect.left - self._line_length_offset,
            rect.bottom + self._margin,
        )

        end = (
            rect.right + self._line_length_offset,
            rect.bottom + self._margin,
        )

        pygame.draw.line(
            surface,
            self.color,
            start,
            end,
            self._line_width,
        )

        return self
