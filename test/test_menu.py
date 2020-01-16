# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST MENU
Menu object tests.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2020 Pablo Pizarro R. @ppizarror

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


class MenuTest(unittest.TestCase):

    def setUp(self):
        """
        Test setup.
        """
        self.menu = PygameMenuUtils.generic_menu('mainmenu')
        self.menu.mainloop()

    def test_enabled(self):
        """
        Test menu enable/disable feature.
        """
        menu = PygameMenuUtils.generic_menu()
        self.assert_(menu.is_disabled())
        menu.enable()
        self.assert_(menu.is_enabled())
        self.assert_(not menu.is_disabled())

        # Intialize and close
        menu.mainloop()
        menu._close()

    def test_initialization(self):
        """
        Test initialization of the menu.
        """
        self.assert_(self.menu._check_menu_initialized())
        menu_not_initializated = PygameMenuUtils.generic_menu()
        self.assertRaises(Exception, lambda: menu_not_initializated._check_menu_initialized())

    def test_depth(self):
        """
        Test depth of a menu.
        """
        self.menu.clear()
        self.assertEqual(self.menu._get_depth(), 0)

        # Adds some menus
        menu_prev = self.menu
        menu = None
        for i in range(1, 11):
            menu = PygameMenuUtils.generic_menu('submenu {0}'.format(i))
            button = menu_prev.add_option('open', menu)
            button.apply()
            menu_prev = menu
        self.menu.draw()

        self.assert_(self.menu != menu)
        self.assertEqual(menu._get_depth(), 10)
        self.assertEqual(self.menu._get_depth(), 10)

        """
        menu_single when it was opened it changed to submenu 1, when submenu 1 was opened
        it changed to submenu 2, and so on...
        """
        self.assertEqual(self.menu.get_title(), 'mainmenu')
        self.assertEqual(self.menu.get_title(True), 'submenu 10')
        self.assertEqual(menu.get_title(), 'submenu 10')

        """
        Submenu 10 has not changed to any, so back will not affect it,
        but mainmenu will reset 1 unit
        """
        menu._back()
        self.assertEqual(menu.get_title(), 'submenu 10')

        """
        Mainmenu has changed, go back changes from submenu 10 to 9
        """
        self.assertEqual(self.menu._get_depth(), 9)
        self.menu._back()
        self.assertEqual(self.menu._get_depth(), 8)
        self.assertEqual(self.menu.get_title(), 'mainmenu')
        self.assertEqual(self.menu.get_title(True), 'submenu 8')

        """
        Full go back (reset)
        """
        self.menu.full_reset()
        self.assertEqual(self.menu._get_depth(), 0)
        self.assertEqual(self.menu.get_title(True), 'mainmenu')

    # noinspection PyArgumentEqualDefault
    def test_get_widget(self):
        """
        Tests widget status.
        """
        self.menu.clear()

        widget = self.menu.add_text_input('test', 'some_id')
        widget_found = self.menu.get_widget('some_id')
        self.assertEqual(widget, widget_found)

        # Add a widget to a deepest menu
        prev_menu = self.menu
        for i in range(11):
            menu = PygameMenuUtils.generic_menu()
            prev_menu.add_option('menu', menu)
            prev_menu = menu

        # Add a deep input
        deep_widget = prev_menu.add_text_input('title', 'deep_id')
        deep_selector = prev_menu.add_selector('selector', [('0', 0), ('1', 1)], 'deep_selector', default=1)

        self.assertEqual(self.menu.get_widget('deep_id', recursive=False), None)
        self.assertEqual(self.menu.get_widget('deep_id', recursive=True), deep_widget)
        self.assertEqual(self.menu.get_widget('deep_selector', recursive=True), deep_selector)

    # noinspection PyArgumentEqualDefault
    def test_get_selected_widget(self):
        """
        Tests get current widget.
        """
        self.menu.clear()

        widget = self.menu.add_text_input('test', 'some_id')
        self.assertEqual(widget, self.menu.get_selected_widget())

    def test_generic_events(self):
        """
        Test key events.
        """
        self.menu.clear()

        # Add a menu and a method that set a function
        def _some_event():
            return 'the value'

        # Add some options
        button = None
        first_button = None
        for i in range(5):
            button = self.menu.add_option('button', _some_event)
            if i == 0:
                first_button = button

        # Create a event in pygame
        self.menu._main(PygameUtils.key(pygameMenu.controls.KEY_MOVE_UP, keydown=True))
        self.assertEqual(self.menu._get_actual_index(), 1)

        # Move down twice
        for i in range(2):
            self.menu._main(PygameUtils.key(pygameMenu.controls.KEY_MOVE_DOWN, keydown=True))
        self.assertEqual(self.menu._get_actual_index(), 4)
        self.menu._main(PygameUtils.key(pygameMenu.controls.KEY_MOVE_UP, keydown=True))
        self.assertEqual(self.menu._get_actual_index(), 0)

        # Press enter, button should trigger and call function
        self.assertEqual(button.apply(), 'the value')
        self.menu._main(PygameUtils.key(pygameMenu.controls.KEY_APPLY, keydown=True))

        # Other
        self.menu._main(PygameUtils.key(pygameMenu.controls.KEY_CLOSE_MENU, keydown=True))
        self.menu._main(PygameUtils.key(pygameMenu.controls.KEY_BACK, keydown=True))

        # Check index is the same as before
        self.assertEqual(self.menu._get_actual_index(), 0)

        # Check joy
        self.menu._main(PygameUtils.joy_key(pygameMenu.controls.JOY_UP))
        self.assertEqual(self.menu._get_actual_index(), 4)
        self.menu._main(PygameUtils.joy_key(pygameMenu.controls.JOY_DOWN))
        self.assertEqual(self.menu._get_actual_index(), 0)
        self.menu._main(PygameUtils.joy_motion(1, 1))
        self.assertEqual(self.menu._get_actual_index(), 1)
        self.menu._main(PygameUtils.joy_motion(1, -1))
        self.assertEqual(self.menu._get_actual_index(), 0)
        self.menu._main(PygameUtils.joy_motion(1, -1))
        self.assertEqual(self.menu._get_actual_index(), 4)

        # Check mouse, get last widget
        click_pos = PygameUtils.get_middle_rect(button.get_rect())
        self.menu._main(PygameUtils.mouse_click(click_pos[0], click_pos[1]))
        click_pos = PygameUtils.get_middle_rect(first_button.get_rect())
        self.menu._main(PygameUtils.mouse_click(click_pos[0], click_pos[1]))

    def test_back_event(self):
        """
        Test back event.
        """
        self.menu.clear()
        self.assertEqual(self.menu._get_depth(), 0)
        menu = PygameMenuUtils.generic_menu('submenu')
        button = self.menu.add_option('open', menu)
        button.apply()
        self.assertEqual(self.menu._get_depth(), 1)
        self.menu._main(PygameUtils.key(pygameMenu.controls.KEY_BACK, keydown=True))  # go back
        self.assertEqual(self.menu._get_depth(), 0)

    def test_mouse_empty_submenu(self):
        """
        Test mouse event where the following submenu has less elements.
        """
        self.menu.clear()

        submenu = PygameMenuUtils.generic_menu()  # 1 option
        submenu.add_option('button', lambda: None)

        self.menu.add_option('button', lambda: None)
        self.menu.add_option('button', lambda: None)
        button = self.menu.add_option('button', submenu)
        self.menu.draw()

        click_pos = PygameUtils.get_middle_rect(button.get_rect())
        self.menu._main(PygameUtils.mouse_click(click_pos[0], click_pos[1]))

    def test_input_data(self):
        """
        Test input data gathering.
        """
        self.menu.clear()

        self.menu.add_text_input('text1', 'id1', 1)  # Force to string
        data = self.menu.get_input_data(True)
        self.assertEqual(data['id1'], '1')

        self.menu.add_text_input('text1', 'id2', 1.5, input_type=pygameMenu.locals.INPUT_INT)
        data = self.menu.get_input_data(True)
        self.assertEqual(data['id2'], 1)  # Cast to int
        self.assertRaises(ValueError, lambda: self.menu.add_text_input('text1', 'id1', 1))

        self.menu.add_text_input('text1', 'id3', 1.5, input_type=pygameMenu.locals.INPUT_FLOAT)
        data = self.menu.get_input_data(True)
        self.assertEqual(data['id3'], 1.5)  # Correct

        # Add input to a submenu
        submenu = PygameMenuUtils.generic_menu()
        submenu.add_text_input('text', 'id4', 'thewidget')
        self.menu.add_option('submenu', submenu)
        data = self.menu.get_input_data(True)
        self.assertEqual(data['id4'], 'thewidget')

        # Add a submenu within submenu with a repeated id, menu.get_input_data
        # should raise an exception
        subsubmenu = PygameMenuUtils.generic_menu()
        subsubmenu.add_text_input('text', 'id4', 'repeateddata')
        submenu.add_option('submenu', subsubmenu)
        self.assertRaises(ValueError, lambda: self.menu.get_input_data(True))

    @staticmethod
    def test_textmenu():
        """
        Test textual menus.
        """
        menu = pygameMenu.TextMenu(surface,
                                   font=PygameMenuUtils.random_font(),
                                   dopause=False,
                                   menu_color=(30, 50, 107),  # Background color
                                   menu_color_title=(120, 45, 30),
                                   onclose=pygameMenu.events.DISABLE_CLOSE,  # Pressing ESC button does nothing
                                   option_shadow=True,
                                   option_shadow_position=pygameMenu.locals.POSITION_SOUTHEAST,
                                   text_align=pygameMenu.locals.ALIGN_CENTER,
                                   title='Help',
                                   window_height=H_SIZE,
                                   window_width=W_SIZE
                                   )
        menu.mainloop()
        menu.add_option('Return to Menu', pygameMenu.events.BACK)
        for m in ['a', 'b', 'c', 'd', 'e']:
            menu.add_line(m)
        menu.draw()
