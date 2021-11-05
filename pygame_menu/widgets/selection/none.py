"""
pygame-menu
https://github.com/ppizarror/pygame-menu

NONE
No selection effect.
"""

__all__ = ['NoneSelection']

import pygame
import pygame_menu

from pygame_menu.widgets.selection.simple import SimpleSelection


class NoneSelection(SimpleSelection):
    """
    No selection effect.
    """

    def __init__(self) -> None:
        super(NoneSelection, self).__init__()
        self.widget_apply_font_color = False

    # noinspection PyMissingOrEmptyDocstring
    def draw(self, surface: 'pygame.Surface', widget: 'pygame_menu.widgets.Widget') -> 'NoneSelection':
        return self
