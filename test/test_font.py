"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST FONT
Test font management.
"""

__all__ = ['FontTest']

from pathlib import Path
from test._utils import MenuUtils, BaseTest

import pygame_menu


class FontTest(BaseTest):

    def test_font_load(self) -> None:
        """
        Load a font from a file.
        """
        font = MenuUtils.get_font(pygame_menu.font.FONT_8BIT, 5)
        self.assertTrue(font is not None)
        self.assertEqual(font, pygame_menu.font.get_font(font, 5))
        self.assertRaises(ValueError, lambda: MenuUtils.get_font('', 0))
        self.assertRaises(ValueError, lambda: MenuUtils.get_font('sys', 0))

    def test_pathlib(self) -> None:
        """
        Test font load with pathlib.
        """
        path_font = Path(pygame_menu.font.FONT_8BIT)
        self.assertRaises(ValueError, lambda: pygame_menu.font.get_font(path_font, 0))
        font = pygame_menu.font.get_font(path_font, 10)
        assert font is not None

    def test_system_load(self) -> None:
        """
        Test fonts from system.
        """
        font_sys = MenuUtils.random_system_font()
        font = MenuUtils.get_font(font_sys, 5)
        self.assertTrue(font is not None)

        # Modify the system font and load, this will raise an exception
        self.assertRaises(ValueError, lambda: MenuUtils.get_font('invalid font', 5))
