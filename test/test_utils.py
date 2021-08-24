"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST UTILS
Library utils.

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

__all__ = ['UtilsTest']

from test._utils import BaseTest

from pygame_menu.locals import POSITION_NORTHWEST

import pygame_menu
import pygame_menu.utils as ut


class UtilsTest(BaseTest):

    def test_position_str(self) -> None:
        """
        Test position assert values as str.
        """
        self.assertIsNone(ut.assert_position_vector(POSITION_NORTHWEST))

    def test_padding(self) -> None:
        """
        Padding test.
        """
        self.assertEqual(ut.parse_padding(1.0), (1, 1, 1, 1))
        self.assertEqual(ut.parse_padding(1.05), (1, 1, 1, 1))
        self.assertEqual(ut.parse_padding([1.0]), (1, 1, 1, 1))
        self.assertEqual(ut.parse_padding((1.0,)), (1, 1, 1, 1))

    def test_terminal_widget_title(self) -> None:
        """
        Test terminal title.
        """
        w = pygame_menu.widgets.Button('epic')
        w.hide()
        s = ut.widget_terminal_title(w)
        self.assertIn('╳', s)
