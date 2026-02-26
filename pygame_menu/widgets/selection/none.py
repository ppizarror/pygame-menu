"""
pygame-menu
https://github.com/ppizarror/pygame-menu

NONE
No selection effect.
"""

from __future__ import annotations

__all__ = ['NoneSelection']


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
        super().__init__()
        self.widget_apply_font_color = False

    # noinspection PyMissingOrEmptyDocstring
    def draw(self, surface: pygame.Surface, widget: pygame_menu.widgets.Widget) -> NoneSelection:
        return self
