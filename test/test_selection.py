"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET SELECTION.
Test widget selection effects.

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

__all__ = ['SelectionTest']

from test._utils import MenuUtils, surface
import copy
import unittest

from pygame_menu.widgets import Button
from pygame_menu.widgets.selection import LeftArrowSelection, RightArrowSelection, HighlightSelection, NoneSelection


class SelectionTest(unittest.TestCase):

    def setUp(self) -> None:
        """
        Setup sound engine.
        """
        self.menu = MenuUtils.generic_menu()
        self.menu.enable()

    def test_copy(self) -> None:
        """
        Test copy.
        """
        s = LeftArrowSelection()
        s1 = copy.copy(s)
        s2 = copy.deepcopy(s)
        s3 = s.copy()
        self.assertNotEqual(s, s1)
        self.assertNotEqual(s, s2)
        self.assertNotEqual(s, s3)

    def test_arrow(self) -> None:
        """
        Test arrow selection.
        """
        w = Button('epic')
        w.set_selection_effect(LeftArrowSelection())
        self.menu.add.generic_widget(w)
        self.menu.draw(surface)
        w.set_selection_effect(RightArrowSelection())
        self.menu.draw(surface)

    def test_highlight(self) -> None:
        """
        Test highlight selection.
        """
        w = Button('epic')
        border_width = 1
        margin_x = 18
        margin_y = 10
        w.set_selection_effect(HighlightSelection(
            border_width=border_width,
            margin_x=margin_x,
            margin_y=margin_y
        ))
        self.menu.add.generic_widget(w)
        self.menu.draw(surface)

        sel = w.get_selection_effect()
        self.assertEqual(sel.get_height(), margin_y)
        self.assertEqual(sel.get_width(), margin_x)

        # Test inflate
        rect = w.get_rect()
        inflate_rect = sel.inflate(rect)
        self.assertEqual(-inflate_rect.x + rect.x, sel.get_width() / 2)
        self.assertEqual(-inflate_rect.y + rect.y, sel.get_height() / 2)

        # Test margin xy
        sel.margin_xy(10, 20)
        self.assertEqual(sel.margin_left, 10)
        self.assertEqual(sel.margin_right, 10)
        self.assertEqual(sel.margin_top, 20)
        self.assertEqual(sel.margin_bottom, 20)

    def test_none(self) -> None:
        """
        Test highlight selection.
        """
        w = Button('epic')
        w.set_selection_effect(NoneSelection())
        self.menu.add.generic_widget(w)
        self.menu.draw(surface)

        rect = w.get_rect()
        new_rect = w.get_selection_effect().inflate(rect)
        self.assertTrue(rect == new_rect)
