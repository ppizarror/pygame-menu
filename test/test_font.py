"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST FONT
Test font management.
"""

__all__ = ['FontTest']

from pathlib import Path
from test._utils import MenuUtils, BaseTest

import pygame
import pygame_menu


class FontTest(BaseTest):

    def test_font_load(self) -> None:
        """
        Load a font from a file.
        """
        font = MenuUtils.get_font(pygame_menu.font.FONT_8BIT, 5)
        self.assertIsNotNone(font)

        self.assertEqual(font, pygame_menu.font.get_font(font, 5))

        with self.assertRaises(ValueError):
            MenuUtils.get_font('', 0)

        with self.assertRaises(ValueError):
            MenuUtils.get_font('sys', 0)

    def test_pathlib(self) -> None:
        """
        Test font load with pathlib.
        """
        path_font = Path(pygame_menu.font.FONT_8BIT)

        with self.assertRaises(ValueError):
            pygame_menu.font.get_font(path_font, 0)

        font = pygame_menu.font.get_font(path_font, 10)
        self.assertIsNotNone(font)

    def test_system_load(self) -> None:
        """
        Test fonts from system.
        """
        font_sys = MenuUtils.random_system_font()
        font = MenuUtils.get_font(font_sys, 5)
        self.assertIsNotNone(font)

        # Invalid system font name should raise ValueError
        with self.assertRaises(ValueError):
            MenuUtils.get_font('invalid font', 5)

    def test_font_argument(self) -> None:
        """
        Test font passed directly as pygame.Font instance.
        """
        menu = MenuUtils.generic_menu()
        f0 = pygame.font.SysFont(pygame.font.get_fonts()[0], 20)

        # Widget with custom font
        text = menu.add.text_input('First name: ', default='John', font_name=f0)
        self.assertEqual(text.get_font_info()['name'], f0)

        # Default font should match theme
        text2 = menu.add.text_input('First name: ', default='John')
        self.assertEqual(text2.get_font_info()['name'], menu.get_theme().widget_font)

    def test_cache_identity(self):
        font1 = pygame_menu.font.get_font(pygame_menu.font.FONT_8BIT, 12)
        font2 = pygame_menu.font.get_font(pygame_menu.font.FONT_8BIT, 12)
        self.assertIs(font1, font2)

    def test_cache_size_variation(self):
        f1 = pygame_menu.font.get_font(pygame_menu.font.FONT_8BIT, 10)
        f2 = pygame_menu.font.get_font(pygame_menu.font.FONT_8BIT, 11)
        self.assertIsNot(f1, f2)

    def test_path_normalization(self):
        p1 = Path(pygame_menu.font.FONT_8BIT)
        p2 = Path(str(p1))  # same path, different object

        f1 = pygame_menu.font.get_font(p1, 14)
        f2 = pygame_menu.font.get_font(p2, 14)

        self.assertIs(f1, f2)

    def test_direct_font_instance(self):
        f = pygame.font.SysFont(pygame.font.get_fonts()[0], 18)
        out = pygame_menu.font.get_font(f, 18)
        self.assertIs(out, f)

    def test_invalid_file_path(self):
        fake = Path('this_font_does_not_exist.ttf')
        with self.assertRaises(ValueError):
            pygame_menu.font.get_font(fake, 12)

    def test_invalid_system_font_suggestion(self):
        with self.assertRaises(ValueError) as ctx:
            pygame_menu.font.get_font('definitely_not_a_real_font_name', 12)

        msg = str(ctx.exception)
        self.assertIn('unknown', msg)
        self.assertIn('use "', msg)  # suggestion present

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            pygame_menu.font.get_font('', 12)

    def test_invalid_size(self):
        with self.assertRaises(ValueError):
            pygame_menu.font.get_font(pygame_menu.font.FONT_8BIT, 0)

    def test_system_font_size_variation(self):
        sys_font = MenuUtils.random_system_font()
        f1 = pygame_menu.font.get_font(sys_font, 10)
        f2 = pygame_menu.font.get_font(sys_font, 11)
        self.assertIsNot(f1, f2)

    def test_direct_font_not_cached(self):
        f = pygame.font.SysFont(pygame.font.get_fonts()[0], 20)
        pygame_menu.font.get_font(f, 20)

        # Ensure no cache entry contains the instance
        for key, value in pygame_menu.font._cache.items():
            self.assertIsNot(value, f)

    def test_load_system_font_success(self):
        sys_font = MenuUtils.random_system_font()
        font = pygame_menu.font.load_system_font(sys_font, 14)
        self.assertIsNotNone(font)

    def test_load_system_font_invalid(self):
        with self.assertRaises(ValueError):
            pygame_menu.font.load_system_font('not_a_real_font_name', 14)

    def test_load_system_font_invalid_size(self):
        sys_font = MenuUtils.random_system_font()
        with self.assertRaises(ValueError):
            pygame_menu.font.load_system_font(sys_font, 0)

    def test_load_font_file_success(self):
        font = pygame_menu.font.load_font_file(pygame_menu.font.FONT_8BIT, 16)
        self.assertIsNotNone(font)

    def test_load_font_file_missing(self):
        with self.assertRaises(IOError):
            pygame_menu.font.load_font_file('missing_font.ttf', 16)
