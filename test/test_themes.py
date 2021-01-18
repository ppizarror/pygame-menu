# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST THEME
Test theme.

NOTE: pygame-menu v3 will not provide new widgets or functionalities, consider
upgrading to the latest version.

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

import unittest
import pygame_menu


class ThemeTest(unittest.TestCase):

    def test_validation(self) -> None:
        """
        Validate theme.
        """
        theme = pygame_menu.themes.THEME_ORANGE
        self.assertEqual(theme.validate(), None)

        # Modify property to invalid and assert error
        theme.widget_padding = 'Epic'
        self.assertRaises(AssertionError, lambda: theme.validate())
        theme.widget_padding = -1
        self.assertRaises(AssertionError, lambda: theme.validate())
        theme.widget_padding = (-1, -1)
        self.assertRaises(AssertionError, lambda: theme.validate())
        theme.widget_padding = (1, 1)
        self.assertEqual(theme.validate(), None)

        # Disable validation
        theme._disable_validation = True
        theme.widget_padding = 'Epic'
        self.assertEqual(theme.validate(), None)

    def test_copy(self) -> None:
        """
        Test theme copy.
        """
        image = pygame_menu.baseimage.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

        # Create theme
        theme = pygame_menu.themes.THEME_DEFAULT.copy()
        theme.background_color = image

        # Copy the theme
        themecopy = theme.copy()
        self.assertNotEqual(theme.background_color, themecopy.background_color)
        self.assertNotEqual(theme.background_color, pygame_menu.themes.THEME_DEFAULT.background_color)

    def test_methods(self):
        """
        Test theme method.
        """
        image = pygame_menu.baseimage.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

        # Create theme
        theme = pygame_menu.themes.THEME_DEFAULT.copy()
        theme.background_color = image

        self.assertRaises(AssertionError, lambda: theme.set_background_color_opacity(0.5))
