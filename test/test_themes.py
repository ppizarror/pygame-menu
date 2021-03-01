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

    def test_validation(self):
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

    def test_copy(self):
        """
        Test theme copy.
        """
        image = pygame_menu.baseimage.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

        # Create theme
        theme = pygame_menu.themes.THEME_DEFAULT.copy()
        theme.background_color = image

        # Copy the theme
        theme_copy = theme.copy()
        self.assertNotEqual(theme.background_color, theme_copy.background_color)
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

    def test_get(self):
        """
        Test custom types get.
        """
        t = pygame_menu.themes.THEME_DEFAULT
        img = pygame_menu.baseimage.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

        class Test(object):
            """
            Class to test.
            """
            pass

        def dummy():
            """
            Callable.
            """
            return True

        # Test correct
        t._get({}, '', 'tuple2', (1, 1))
        t._get({}, '', str, 'hi')
        t._get({}, '', int, 4)
        t._get({}, '', bool, True)
        t._get({}, '', 'color', (1, 1, 1))
        t._get({}, '', 'color', [11, 1, 0])
        t._get({}, '', 'color', [11, 1, 0, 55])
        t._get({}, '', 'color_none', (1, 1, 1))
        t._get({}, '', 'color_none', [11, 1, 0])
        t._get({}, '', 'color_none', [11, 1, 0, 55])
        t._get({}, '', 'color_none', None)
        t._get({}, '', Test, Test())
        t._get({}, '', callable, dummy)
        t._get({}, '', 'callable', dummy)
        t._get({}, '', 'callable', dummy)
        t._get({}, '', 'image', img)
        t._get({}, '', 'tuple2', (1, -1))
        t._get({}, '', 'tuple2', [1, -1])
        t._get({}, '', 'color_image', (1, 1, 1))
        t._get({}, '', 'color_image', [11, 1, 0])
        t._get({}, '', 'color_image', [11, 1, 0, 55])
        t._get({}, '', 'color_image', img)
        t._get({}, '', 'alignment', pygame_menu.locals.ALIGN_LEFT)
        t._get({}, '', 'position', pygame_menu.locals.POSITION_SOUTHWEST)
        t._get({}, '', 'none', None)
        t._get({}, '', 'color_image_none', [11, 1, 0, 55])
        t._get({}, '', 'color_image_none', None)
        t._get({}, '', 'color_image_none', img)

        self.assertTrue(t._get({}, '', 'callable', dummy)())

        # Test raises
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'none', 1))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'none', bool))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'image', bool))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'callable', bool))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'unknown', Test()))
        self.assertRaises(AssertionError, lambda: t._get({}, '', callable, Test()))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'color', None))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'color', [11, 1, -1]))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'color', [11, 1, -1]))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'color', [11, 1]))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'color', [1, 1, 1, 256]))
        self.assertRaises(AssertionError, lambda: t._get({}, '', int, 4.4))
        self.assertRaises(AssertionError, lambda: t._get({}, '', bool, 4.4))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'tuple2.1', (1, 1)))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'tuple2', (1, 1, 1)))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'cursor', 'hi'))
