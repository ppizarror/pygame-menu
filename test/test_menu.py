"""
Menu object tests.
"""
from test._utils import *


class MenuTest(unittest.TestCase):
    def setUp(self):
        """
        Test setup.
        """
        self.menu = create_generic_menu('mainmenu')
        self.menu.mainloop()

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
            menu = create_generic_menu('submenu {0}'.format(i))
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
        self.assertEqual(self.menu.get_title(True), 'submenu 1')
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
            menu = create_generic_menu()
            prev_menu.add_option('menu', menu)
            prev_menu = menu

        # Add a deep input
        deep_widget = prev_menu.add_text_input('title', 'deep_id')

        self.assertEqual(self.menu.get_widget('deep_id', recursive=False), None)
        self.assertEqual(self.menu.get_widget('deep_id', recursive=True), deep_widget)

    def test_events(self):
        """
        Test key events.
        """
        self.menu.clear()

        # Add a menu and a method that set a function
        def _assert():
            print('wena')

        # Add some options (5)
        for i in range(5):
            self.menu.add_option('button', _assert)

        # Create a event in pygame
        self.menu._main([pygame.event.Event(pygame.KEYDOWN, {"key": pygameMenu.controls.KEY_MOVE_UP})], test_event=True)  # Down
        self.assertEqual(self.menu._get_actual_index(), 1)

        # Press Up twice
        for i in range(2):
            self.menu._main([pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_UP})], test_event=True)  # Down


if __name__ == '__main__':
    unittest.main()
