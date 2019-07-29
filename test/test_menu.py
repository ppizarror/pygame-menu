"""
Menu object tests.
"""

# Imports
import unittest
import pygame
import pygameMenu

# Constants
FPS = 60  # Frames per second of the menu
H_SIZE = 600  # Window height
W_SIZE = 600  # Window width

# Init pygame
pygame.init()
surface = pygame.display.set_mode((W_SIZE, H_SIZE))
pygame.display.set_caption('PygameMenu Example 1')


def create_generic_menu(title=''):
    """
    Generate a generic test menu.

    :param title: Menu title
    :type title: basestring
    :return: Menu
    :rtype: pygameMenu.Menu
    """
    return pygameMenu.Menu(surface,
                           dopause=False,
                           enabled=False,
                           font=pygameMenu.fonts.FONT_NEVIS,
                           fps=FPS,
                           menu_alpha=90,
                           title=title,
                           window_height=H_SIZE,
                           window_width=W_SIZE
                           )


class MenuTest(unittest.TestCase):
    def setUp(self):
        """
        Test setup.
        :return: None
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


if __name__ == '__main__':
    unittest.main()
