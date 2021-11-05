"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SIMPLE
Simple selection effect.
"""

__all__ = ['SimpleSelection']

import pygame
import pygame_menu

from pygame_menu.widgets.core import Selection


class SimpleSelection(Selection):
    """
    This selection effect only tells widget to apply selection color to font if
    selected.
    """

    def __init__(self) -> None:
        super(SimpleSelection, self).__init__(
            margin_left=0, margin_right=0, margin_top=0, margin_bottom=0
        )

    # noinspection PyMissingOrEmptyDocstring
    def draw(self, surface: 'pygame.Surface', widget: 'pygame_menu.widgets.Widget') -> 'SimpleSelection':
        return self
