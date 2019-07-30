# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGETS
Test widgets.

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


class WidgetsTest(unittest.TestCase):

    def setUp(self):
        """
        Setup sound engine.
        """
        self.menu = PygameMenuUtils.generic_menu()

    def test_selector(self):
        """
        Test selector widget.
        """
        selector = self.menu.add_selector('selector',
                                          [('1 - Easy', 'EASY'),
                                           ('2 - Medium', 'MEDIUM'),
                                           ('3 - Hard', 'HARD')],
                                          default=1)
        selector.draw(surface)
        selector.selected = False
        selector.draw(surface)

        # Test events
        selector.update(PygameUtils.key(0, keydown=True, testmode=False))
        selector.update(PygameUtils.key(pygameMenu.controls.KEY_LEFT, keydown=True))
        selector.update(PygameUtils.key(pygameMenu.controls.KEY_RIGHT, keydown=True))
        selector.update(PygameUtils.key(pygameMenu.controls.KEY_APPLY, keydown=True))
        selector.update(PygameUtils.joy_key(pygameMenu.controls.JOY_LEFT))
        selector.update(PygameUtils.joy_key(pygameMenu.controls.JOY_RIGHT))
        selector.update(PygameUtils.joy_motion(1, 0))
        selector.update(PygameUtils.joy_motion(-1, 0))
        click_pos = PygameUtils.get_middle_rect(selector.get_rect())
        selector.update(PygameUtils.mouse_click(click_pos[0], click_pos[1]))

        # Update elements
        new_elements = [('4 - Easy', 'EASY'),
                        ('5 - Medium', 'MEDIUM'),
                        ('6 - Hard', 'HARD')]
        selector.update_elements(new_elements)
        selector.set_value('6 - Hard')
        self.assertRaises(ValueError, None)
