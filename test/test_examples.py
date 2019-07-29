# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST EXAMPLES
Test example files.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2019 Pablo Pizarro R. @ppizarror

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
import pygame

# Imports
import pygameMenu.examples.timer_clock as example1
import pygameMenu.examples.game_difficulty_selector as example2
import pygameMenu.examples.multi_input as example3


class ExamplesTest(unittest.TestCase):

    @staticmethod
    def test_example_timer_clock():
        """
        Test timer clock example.
        """
        example1.main(True)
        example1.mainmenu_background()
        example1.reset_timer()

    def test_example_difficulty_selector(self):
        """
        Test multi-input example.
        """
        example2.main(True)
        font = PygameMenuUtils.load_font(PygameMenuUtils.random_font(), 5)
        example2.play_function(['EASY'], font, test=True)

        # Find
        menu_inputs = example2.play_menu.get_input_data(recursive=True)
        keys = menu_inputs.keys()
        self.assert_('select_difficulty' in keys)
        selector = example2.play_menu.get_widget('select_difficulty', True)
        selector.update([])
        selector.left()
        selector.apply()

    @staticmethod
    def test_example_multi_input():
        """
        Test multi-input example.
        """
        example3.main(True)
