# coding=utf-8
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

from test._utils import *
from pygame_menu.widgets import Button
from pygame_menu.widgets.selection import *


class WidgetSelectionTest(unittest.TestCase):

    def setUp(self):
        """
        Setup sound engine.
        """
        self.menu = MenuUtils.generic_menu()
        self.menu.enable()

    def test_arrow(self):
        """
        Test arrow selection.
        """
        w = Button('epic')
        w.set_selection_effect(LeftArrowSelection())
        self.menu.add_generic_widget(w)
        self.menu.draw(surface)
        w.set_selection_effect(RightArrowSelection())
        self.menu.draw(surface)

    def test_highlight(self):
        """
        Test highlight selection.
        """
        w = Button('epic')
        w.set_selection_effect(HighlightSelection())
        self.menu.add_generic_widget(w)
        self.menu.draw(surface)

    def test_none(self):
        """
        Test highlight selection.
        """
        w = Button('epic')
        w.set_selection_effect(NoneSelection())
        self.menu.add_generic_widget(w)
        self.menu.draw(surface)
