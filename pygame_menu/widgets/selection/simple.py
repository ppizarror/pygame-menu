"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SIMPLE
Simple selection effect.
"""

from __future__ import annotations

__all__ = ["SimpleSelection"]

from typing import TYPE_CHECKING

from pygame_menu.widgets.core import Selection

if TYPE_CHECKING:
    import pygame

    import pygame_menu


class SimpleSelection(Selection):
    """
    This selection effect only tells widget to apply selection color to font if
    selected.
    """

    def __init__(self, widget_apply_font_color: bool = True) -> None:
        super().__init__(
            margin_left=0,
            margin_right=0,
            margin_top=0,
            margin_bottom=0,
            widget_apply_font_color=widget_apply_font_color,
        )

    def _repr_attrs(self) -> dict[str, object]:
        """
        Return dictionary of attributes for string representation.

        :return: Dictionary of attributes
        """
        return super()._repr_attrs()

    def __repr__(self) -> str:
        """
        Return string representation.

        :return: String representation
        """
        attrs = ", ".join(f"{k}={v!r}" for k, v in self._repr_attrs().items())
        return f"{self.__class__.__name__}({attrs})"

    def draw(
        self, surface: pygame.Surface, widget: pygame_menu.widgets.Widget
    ) -> SimpleSelection:
        return self
