"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST FONT
Test font management.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2021 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

__all__ = ['FontTest']

from pathlib import Path
from test._utils import MenuUtils
import unittest

import pygame_menu


class FontTest(unittest.TestCase):

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
