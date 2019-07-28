"""
Menu object tests.
"""

# Imports
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
pygame.display.set_caption('PygameMenu Example 1')


class MenuTest(unittest.TestCase):
    def setUp(self):
        """
        Test setup.
        :return: None
        """
        self.menu_single = pygameMenu.Menu(surface,
                                           dopause=False,
                                           enabled=False,
                                           font=pygameMenu.fonts.FONT_NEVIS,
                                           fps=FPS,
                                           menu_alpha=90,
                                           onclose=pygameMenu.events.CLOSE,
                                           title='A menu',
                                           title_offsety=5,
                                           window_height=H_SIZE,
                                           window_width=W_SIZE
                                           )

    def test_depth(self):
        self.assertEqual(self.menu_single._get_depth(), 0)


if __name__ == '__main__':
    unittest.main()
