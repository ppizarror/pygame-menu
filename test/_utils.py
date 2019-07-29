"""
Test suite utils.
"""

# noinspection PyUnresolvedReferences
import unittest
import pygame
import pygameMenu

# Constants
FPS = 60  # Frames per second of the menu
H_SIZE = 600  # Window height
W_SIZE = 600  # Window width

# Init pygame
pygame.init()
surface = pygame.display.set_mode((W_SIZE, H_SIZE))


def create_generic_menu(title=''):
    """
    Generate a generic test menu.

    :param title: Menu title
    :type title: basestring
    :return: Menu
    :rtype: pygameMenu.Menu
    """
    return pygameMenu.Menu(surface,
                           dopause=False,
                           enabled=False,
                           font=pygameMenu.fonts.FONT_NEVIS,
                           fps=FPS,
                           menu_alpha=90,
                           title=title,
                           window_height=H_SIZE,
                           window_width=W_SIZE
                           )
