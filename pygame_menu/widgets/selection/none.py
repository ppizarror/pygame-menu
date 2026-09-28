"""
pygame-menu
https://github.com/ppizarror/pygame-menu

NONE
No selection effect.
"""

from __future__ import annotations

__all__ = ["NoneSelection"]

from typing import TYPE_CHECKING

from pygame_menu.widgets.selection.simple import SimpleSelection

if TYPE_CHECKING:
    import pygame

    import pygame_menu


class NoneSelection(SimpleSelection):
    """
    No selection effect.
    """

    def __init__(self) -> None:
        super().__init__(widget_apply_font_color=False)

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
    ) -> NoneSelection:
        return self
