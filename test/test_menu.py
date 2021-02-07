"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST MENU
Menu object tests.

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

__all__ = ['MenuTest']

import copy
import unittest
import timeit
from test._utils import surface, test_reset_surface, MenuUtils, PygameUtils
from typing import Any, Tuple

import pygame
import pygame_menu
from pygame_menu import events
from pygame_menu.widgets import Label, Button

# Configure the tests
TEST_TIME_DRAW = False


def dummy_function() -> None:
    """
    Dummy function, this can be achieved with lambda but it's against
    PEP-8.

    :return: None
    """
    return


class MenuTest(unittest.TestCase):

    def setUp(self) -> None:
        """
        Test setup.
        """
        test_reset_surface()
        self.menu = MenuUtils.generic_menu(title='mainmenu')
        self.menu.disable()
        self.assertRaises(RuntimeError, lambda: self.menu.mainloop(surface, bgfun=dummy_function, disable_loop=True))
        self.menu.enable()

    @staticmethod
    def test_time_draw() -> None:
        """
        This test the time that takes to menu to draw several times.
        """
        if not TEST_TIME_DRAW:
            return
        menu = MenuUtils.generic_menu(title='EPIC')
        menu.enable()

        # Add several widgets
        add_decorator = True
        for i in range(30):
            btn = menu.add.button(title='epic', action=events.BACK)
            btndeco = btn.get_decorator()
            if add_decorator:
                for j in range(10):
                    btndeco.add_pixel(j * 10, j * 20, (10, 10, 150))
            menu.add.vertical_margin(margin=10)
            menu.add.label(title='epic test')
            menu.add.color_input(title='color', color_type='rgb', default=(234, 33, 2))
            menu.add.selector(title='epic selector', items=[('1', '3'), ('2', '4')])
            menu.add.text_input(title='text', default='the default text')

        def draw_and_update() -> None:
            """
            Draw and updates the menu.
            """
            menu.draw(surface)
            menu.update(pygame.event.get())

        # (no decorator) no updates, 0.921
        # (no decorator) updates, 0.860
        # (no decorator) check len updates, 0.855
        # (no decorator) with surface cache, 0.10737799999999886
        # (decorator) with surface cache, 0.1033874000000008
        print(timeit.timeit(lambda: draw_and_update(), number=100))

    def test_copy(self) -> None:
        """
        Test menu copy.
        """
        menu = MenuUtils.generic_menu()
        self.assertRaises(pygame_menu.menu._MenuCopyException, lambda: copy.copy(menu))
        self.assertRaises(pygame_menu.menu._MenuCopyException, lambda: copy.deepcopy(menu))

    def test_size_constructor(self) -> None:
        """
        Test menu sizes.
        """
        inf_size = 1000000000
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(width=0, height=300))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(width=300, height=0))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(width=-200, height=300))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(width=inf_size, height=300))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(width=300, height=inf_size))

    def test_position(self) -> None:
        """
        Test position.
        """
        # Test centering
        menu = MenuUtils.generic_menu()
        btn = menu.add.button('button', None)
        menu.center_content()
        self.assertEqual(menu.get_height(), 400)
        self.assertEqual(menu.get_height(inner=True), 345)
        self.assertEqual(menu.get_menubar_widget().get_height(), 55)

        h = 41
        if pygame.version.vernum[0] < 2:
            h = 42

        self.assertEqual(btn.get_height(), h)
        self.assertEqual(btn.get_size()[1], h)
        self.assertEqual(menu.get_height(widget=True), h)

        vpos = int((345 - h) / 2)  # available_height - widget_height
        self.assertEqual(menu._widget_offset[1], vpos)
        self.assertEqual(btn.get_position()[1], vpos + 1)

        # If there's too many widgets, the centering should be disabled
        for i in range(20):
            menu.add.button('button', None)
        self.assertEqual(menu._widget_offset[1], 0)

        theme = menu.get_theme()

        # Anyway, as the widget is 0, the first button position should be the height of its selection effect
        btneff = btn.get_selection_effect().get_margin()[0]
        self.assertEqual(btn.get_position()[1], btneff + 1)

        self.assertEqual(h * 21 + theme.widget_margin[1] * 20, menu.get_height(widget=True))

        # Test menu not centered
        menu = MenuUtils.generic_menu(center_content=False)
        btn = menu.add.button('button', None)
        btneff = btn.get_selection_effect().get_margin()[0]
        self.assertEqual(btn.get_position()[1], btneff + 1)

        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(position_x=-1, position_y=0))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(position_x=0, position_y=-1))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(position_x=-1, position_y=-1))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(position_x=101, position_y=0))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(position_x=99, position_y=101))
        menu = MenuUtils.generic_menu(position_x=0, position_y=0)
        menu.set_relative_position(20, 40)

        theme = pygame_menu.themes.THEME_BLUE.copy()
        theme.widget_font_size = 20

        menu = pygame_menu.Menu(
            column_min_width=380,
            columns=2,
            height=300,
            rows=4,
            theme=theme,
            title='Welcome',
            width=400
        )

        quit1 = menu.add.button('Quit', pygame_menu.events.EXIT)
        name1 = menu.add.text_input('Name: ', default='John Doe', maxchar=10, padding=30)
        sel1 = menu.add.selector('Difficulty: ', [('Hard', 1), ('Easy', 2)])
        sel2 = menu.add.selector('Difficulty: ', [('Hard', 1), ('Easy', 2)])
        play1 = menu.add.button('Play', pygame_menu.events.NONE, align=pygame_menu.locals.ALIGN_LEFT)
        play2 = menu.add.button('Play 2', pygame_menu.events.NONE, align=pygame_menu.locals.ALIGN_RIGHT)
        play2.set_float()
        hidden = menu.add.button('Hidden', None, font_size=100)
        hidden.hide()
        quit2 = menu.add.button('Quit', pygame_menu.events.EXIT)
        label = menu.add.label('This label is really epic')
        label.rotate(90)

        menu.render()
        # menu.mainloop(surface)

        x, y = quit1.get_position()
        self.assertEqual(x, 170)
        self.assertEqual(y, 6)
        x, y = name1.get_position()
        self.assertEqual(x, 115)
        self.assertEqual(y, 74)
        x, y = sel1.get_position()
        self.assertEqual(x, 104)
        self.assertEqual(y, 142)
        x, y = sel2.get_position()
        self.assertEqual(x, 104)
        self.assertEqual(y, 180)
        x, y = play1.get_position()
        self.assertEqual(x, 389)
        self.assertEqual(y, 6)
        x, y = play2.get_position()
        self.assertEqual(x, 697)
        self.assertEqual(y, 6)
        x, y = hidden.get_position()
        self.assertEqual(x, 0)
        self.assertEqual(y, 0)
        x, y = quit2.get_position()
        self.assertEqual(x, 550)
        self.assertEqual(y, 44)
        x, y = label.get_position()
        self.assertEqual(x, 556)
        self.assertEqual(y, 82)

        # Test no selectable position
        menu = MenuUtils.generic_menu(center_content=False)
        btn = menu.add.button('button', None)
        btn.is_selectable = False
        menu.render()
        self.assertEqual(btn.get_position()[1], 1)

        # Test no selectable + widget
        menu = MenuUtils.generic_menu()
        img = menu.add.image(
            pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU,
            scale=(0.25, 0.25),
            align=pygame_menu.locals.ALIGN_CENTER
        )
        btn = menu.add.button('Nice', None)
        margin = menu.get_theme().widget_margin[1]
        menu.render()
        self.assertEqual(menu.get_height(widget=True), img.get_height() + btn.get_height() + margin)
        self.assertEqual(int((menu.get_height(inner=True) - menu.get_height(widget=True)) / 2), menu._widget_offset[1])

        # Test alternating float
        # b1,b2
        # b3
        # b4,b5,b6
        # b7
        menu = MenuUtils.generic_menu()
        b1 = menu.add.button('b1', None)
        b2 = menu.add.button('b2', None).set_float()
        b3 = menu.add.button('b3', None)
        b4 = menu.add.button('b4', None)
        b5 = menu.add.button('b5', None).set_float()
        b6 = menu.add.button('b6', None).set_float()
        b7 = menu.add.button('b37', None)
        self.assertEqual(b1.get_col_row_index(), (0, 0, 0))
        self.assertEqual(b2.get_col_row_index(), (0, 0, 1))
        self.assertEqual(b3.get_col_row_index(), (0, 1, 2))
        self.assertEqual(b4.get_col_row_index(), (0, 2, 3))
        self.assertEqual(b5.get_col_row_index(), (0, 2, 4))
        self.assertEqual(b6.get_col_row_index(), (0, 2, 5))
        self.assertEqual(b7.get_col_row_index(), (0, 3, 6))

        # b1,b2
        # b3,b5,b6
        # b7
        menu.remove_widget(b4)

        self.assertEqual(b1.get_col_row_index(), (0, 0, 0))
        self.assertEqual(b2.get_col_row_index(), (0, 0, 1))
        self.assertEqual(b3.get_col_row_index(), (0, 1, 2))
        self.assertEqual(b4.get_col_row_index(), (-1, -1, -1))
        self.assertEqual(b5.get_col_row_index(), (0, 1, 3))
        self.assertEqual(b6.get_col_row_index(), (0, 1, 4))
        self.assertEqual(b7.get_col_row_index(), (0, 2, 5))

        # b1,b2,b5,b6
        # b7
        menu.remove_widget(b3)

        self.assertEqual(b1.get_col_row_index(), (0, 0, 0))
        self.assertEqual(b2.get_col_row_index(), (0, 0, 1))
        self.assertEqual(b3.get_col_row_index(), (-1, -1, -1))
        self.assertEqual(b4.get_col_row_index(), (-1, -1, -1))
        self.assertEqual(b5.get_col_row_index(), (0, 0, 2))
        self.assertEqual(b6.get_col_row_index(), (0, 0, 3))
        self.assertEqual(b7.get_col_row_index(), (0, 1, 4))

    def test_attributes(self) -> None:
        """
        Test menu attributes.
        """
        menu = MenuUtils.generic_menu()
        self.assertFalse(menu.has_attribute('epic'))
        self.assertRaises(IndexError, lambda: menu.remove_attribute('epic'))
        menu.set_attribute('epic', True)
        self.assertTrue(menu.has_attribute('epic'))
        self.assertTrue(menu.get_attribute('epic'))
        menu.set_attribute('epic', False)
        self.assertFalse(menu.get_attribute('epic'))
        menu.remove_attribute('epic')
        self.assertFalse(menu.has_attribute('epic'))
        self.assertEqual(menu.get_attribute('epic', 420), 420)

    def test_close(self) -> None:
        """
        Test menu close.
        """
        menu = MenuUtils.generic_menu()
        menu.disable()
        menu.set_title('1')
        menu.set_attribute('epic', False)
        menu._back()

        def close() -> None:
            """
            Close callback.
            """
            menu.set_attribute('epic', True)

        menu.set_onclose(close)
        self.assertTrue(not menu.is_enabled())
        menu.enable()
        self.assertFalse(menu.get_attribute('epic'))
        menu._close()
        self.assertTrue(menu.get_attribute('epic'))

        test = [False, False]

        def closefun() -> None:
            """
            Close callback.
            """
            test[0] = True

        menu2 = MenuUtils.generic_menu(onclose=closefun)
        menu2.set_title(2)
        menu2.enable()

        self.assertTrue(menu2.close())
        self.assertTrue(test[0])

        # This method takes menu as input
        def closefun_menu(m: 'pygame_menu.Menu') -> None:
            """
            Test object is menu.
            """
            test[1] = True
            self.assertEqual(m, menu2)

        menu2.set_onclose(closefun_menu)
        menu2.enable()
        menu2.close()
        self.assertTrue(test[1])

        # Change onclose
        menu2.set_onclose(None)
        menu2.enable()
        self.assertFalse(menu2.close())  # None status don't changes enabled
        self.assertTrue(menu2.is_enabled())
        menu2.set_onclose(pygame_menu.events.NONE)
        self.assertFalse(menu2.close())  # NONE event don't changes enabled
        self.assertTrue(menu2.is_enabled())

        # Add button with submenu, and open it
        self.assertEqual(menu2.get_current().get_title(), '2')
        menu2.add.button('to1', menu).apply()
        self.assertEqual(menu2.get_current().get_title(), '1')
        self.assertEqual(menu2.get_current(), menu)

        # Set onclose 1 as reset, if close then menu should be disabled
        # and back to '2'
        menu.set_onclose(pygame_menu.events.RESET)
        menu.close()

        # Open again 1
        self.assertFalse(menu2.is_enabled())
        menu2.enable()
        menu2.get_selected_widget().apply()
        self.assertEqual(menu2.get_current().get_title(), '1')

        # Set new close callback, it receives the menu and fires reset,
        # the output should be the same, except it don't closes

        def new_close(m: 'pygame_menu.Menu') -> None:
            """
            Reset the current menu.
            """
            self.assertEqual(m, menu)
            m.reset(1)

        # Also, set first menu onreset to test this behaviour
        reset = [False]

        def onreset(m: 'pygame_menu.Menu') -> None:
            """
            Called in reset.
            """
            self.assertEqual(m, menu)
            reset[0] = True

        menu.set_onclose(new_close)
        menu.set_onreset(onreset)
        self.assertFalse(reset[0])
        menu.close()
        self.assertTrue(reset[0])
        self.assertEqual(menu2.get_current().get_title(), '2')
        self.assertFalse(menu2.is_enabled())

        # Test back event
        menu2.enable()
        menu2.get_selected_widget().apply()
        menu.set_onclose(pygame_menu.events.BACK)
        menu.set_onreset(None)
        self.assertEqual(menu2.get_current(), menu)
        menu2.close()
        self.assertEqual(menu2.get_current(), menu2)

        # Test close event, this should NOT change the pointer
        menu2.enable()
        menu2.get_selected_widget().apply()
        menu.set_onclose(pygame_menu.events.CLOSE)
        menu.set_onreset(None)
        self.assertEqual(menu2.get_current(), menu)
        menu.close()
        self.assertEqual(menu2.get_current(), menu)
        menu.reset(1)
        self.assertEqual(menu2.get_current(), menu2)

    def test_enabled(self) -> None:
        """
        Test menu enable/disable feature.
        """
        menu = MenuUtils.generic_menu(onclose=events.NONE, enabled=False)
        self.assertTrue(not menu.is_enabled())
        menu.enable()
        self.assertTrue(menu.is_enabled())
        self.assertFalse(not menu.is_enabled())

        # Initialize and close
        menu.mainloop(surface, bgfun=dummy_function, disable_loop=True)
        menu._close()

    # noinspection PyArgumentEqualDefault
    def test_depth(self) -> None:
        """
        Test depth of a menu.
        """
        self.menu.clear()
        self.assertEqual(self.menu._get_depth(), 0)

        # Adds some menus
        menu_prev = self.menu
        menu = None
        for i in range(1, 11):
            menu = MenuUtils.generic_menu(title='submenu {0}'.format(i))
            button = menu_prev.add.button('open', menu)
            button.apply()
            menu_prev = menu
        self.menu.enable()
        self.menu.draw(surface)

        self.assertNotEqual(self.menu.get_current().get_id(), self.menu.get_id())
        self.assertTrue(self.menu != menu)
        self.assertEqual(menu._get_depth(), 10)
        self.assertEqual(self.menu._get_depth(), 10)

        """
        menu when it was opened it changed to submenu 1, when submenu 1 was opened
        it changed to submenu 2, and so on...
        """
        self.assertEqual(self.menu.get_title(), 'mainmenu')
        self.assertEqual(self.menu.get_current().get_title(), 'submenu 10')
        self.assertEqual(menu.get_current().get_title(), 'submenu 10')

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
        self.assertEqual(self.menu.get_current().get_title(), 'submenu 8')

        """
        Full go back (reset)
        """
        self.menu.full_reset()
        self.assertEqual(self.menu._get_depth(), 0)
        self.assertEqual(self.menu.get_current().get_title(), 'mainmenu')

    # noinspection PyArgumentEqualDefault
    def test_get_widget(self) -> None:
        """
        Tests widget status.
        """
        self.menu.clear()

        widget = self.menu.add.text_input('test', textinput_id='some_id')
        widget_found = self.menu.get_widget('some_id')
        self.assertEqual(widget, widget_found)

        # Add a widget to a deepest menu
        prev_menu = self.menu
        for i in range(11):
            menu = MenuUtils.generic_menu()
            prev_menu.add.button('menu', menu)
            prev_menu = menu

        # Add a deep input
        deep_widget = prev_menu.add.text_input('title', textinput_id='deep_id')
        deep_selector = prev_menu.add.selector('selector', [('0', 0), ('1', 1)], selector_id='deep_selector', default=1)

        self.assertIsNone(self.menu.get_widget('deep_id', recursive=False))
        self.assertEqual(self.menu.get_widget('deep_id', recursive=True), deep_widget)
        self.assertEqual(self.menu.get_widget('deep_selector', recursive=True), deep_selector)

    def test_add_generic_widget(self) -> None:
        """
        Test generic widget.
        """
        self.menu.clear()
        menu = MenuUtils.generic_menu()
        btn = menu.add.button('nice', None)
        w = Button('title')
        self.menu.add.generic_widget(w)
        self.assertRaises(ValueError, lambda: menu.add.generic_widget(w))
        btn._menu = None
        self.menu.add.generic_widget(btn)

    # noinspection PyArgumentEqualDefault
    def test_get_selected_widget(self) -> None:
        """
        Tests get current widget.
        """
        self.menu.clear()

        # Test widget selection and removal
        widget = self.menu.add.text_input('test', default='some_id')
        self.assertEqual(widget, self.menu.get_selected_widget())
        self.menu.remove_widget(widget)
        self.assertIsNone(self.menu.get_selected_widget())
        self.assertEqual(self.menu.get_index(), -1)

        # Add two widgets, first widget will be selected first, but if removed the second should be selected
        widget1 = self.menu.add.text_input('test', default='some_id', textinput_id='epic')
        self.assertRaises(IndexError, lambda: self.menu.add.text_input('test', default='some_id', textinput_id='epic'))
        widget2 = self.menu.add.text_input('test', default='some_id')
        self.assertEqual(widget1.get_menu(), self.menu)
        self.assertEqual(widget1, self.menu.get_selected_widget())
        self.menu.remove_widget(widget1)
        self.assertIsNone(widget1.get_menu())
        self.assertEqual(widget2, self.menu.get_selected_widget())
        self.menu.remove_widget(widget2)
        self.assertIsNone(widget2.get_menu())
        self.assertEqual(len(self.menu.get_widgets()), 0)

        # Add 3 widgets, select the last one and remove it, then the selected widget must be the first
        w1 = self.menu.add.button('1', None)
        w2 = Label('2')
        self.menu.add.generic_widget(w2, configure_defaults=True)
        w3 = self.menu.add.button('3', None)
        self.assertEqual(self.menu.get_selected_widget(), w1)
        self.menu.select_widget(w3)
        self.assertEqual(self.menu.get_selected_widget(), w3)
        self.menu.remove_widget(w3)
        # 3 was deleted, so 1 should be selected
        self.assertEqual(self.menu.get_selected_widget(), w1)

        # Hides w1, then w2 should be selected
        w1.hide()
        self.assertEqual(self.menu.get_selected_widget(), w2)

        # Unhide w1, w2 should be keep selected
        w1.show()
        self.assertEqual(self.menu.get_selected_widget(), w2)

        # Mark w1 as unselectable and remove w2, then no widget should be selected
        w1.is_selectable = False
        self.menu.remove_widget(w2)
        self.assertIsNone(self.menu.get_selected_widget())
        self.assertRaises(ValueError, lambda: self.menu.select_widget(w1))

        # Mark w1 as selectable
        w1.is_selectable = True
        self.menu.add.generic_widget(w2)
        self.assertEqual(self.menu.get_selected_widget(), w2)

        # Add a new widget that cannot be selected
        self.menu.add.label('not selectable')
        self.menu.add.label('not selectable')
        wlast = self.menu.add.label('not selectable', selectable=True)

        # If w2 is removed, then menu will try to select labels, but as them are not selectable it should select the last one
        w2.hide()
        self.assertEqual(self.menu.get_selected_widget(), wlast)

        # Mark w1 as unselectable, then w1 is not selectable, nor w2, and labels are unselectable too
        # so the selected should be the same
        w1.is_selectable = False
        self.menu.update(PygameUtils.key(pygame_menu.controls.KEY_MOVE_DOWN, keydown=True))
        self.assertEqual(self.menu.get_selected_widget(), wlast)

        # Show w2, then if DOWN is pressed again, the selected status should be 2
        w2.show()
        self.menu.update(PygameUtils.key(pygame_menu.controls.KEY_MOVE_DOWN, keydown=True))
        self.assertEqual(self.menu.get_selected_widget(), w2)

        # Hide w2, pass again to wlast
        w2.hide()
        self.assertEqual(self.menu.get_selected_widget(), wlast)

        # Hide wlast, then nothing is selected
        wlast.hide()
        self.assertIsNone(self.menu.get_selected_widget())

        # Unhide w2, then it should be selected
        w2.show()
        self.assertEqual(self.menu.get_selected_widget(), w2)

        # Remove w2, then nothing should be selected
        self.menu.remove_widget(w2)
        self.assertIsNone(self.menu.get_selected_widget())

        # Clear all widgets and get index
        self.menu._widgets = []
        self._index = 100
        self.assertIsNone(self.menu.get_selected_widget())

        # Destroy index
        self.menu._index = '0'
        self.assertIsNone(self.menu.get_selected_widget())
        self.assertEqual(self.menu._index, 0)

    def test_submenu(self) -> None:
        """
        Test submenus.
        """
        menu = MenuUtils.generic_menu()
        menu2 = MenuUtils.generic_menu()
        btn = menu.add.button('btn', menu2)
        self.assertTrue(btn.to_menu)
        self.assertTrue(menu.in_submenu(menu2))
        self.assertFalse(menu2.in_submenu(menu))

        btn.update_callback(lambda: None)
        self.assertFalse(btn.to_menu)
        self.assertFalse(menu.in_submenu(menu2))

        # Test recursive
        menu.clear()
        menu2.clear()

        self.assertRaises(ValueError, lambda: menu.add.button('to self', menu))
        menu.add.button('to2', menu2)
        self.assertRaises(ValueError, lambda: menu2.add.button('to1', menu))

    def test_centering(self) -> None:
        """
        Test centering menu.
        """
        # Vertical offset disables centering
        theme = pygame_menu.themes.THEME_BLUE.copy()
        theme.widget_offset = (0, 100)
        menu = MenuUtils.generic_menu(theme=theme)
        self.assertEqual(menu.get_theme(), theme)
        self.assertFalse(menu._auto_centering)

        # Outer scrollarea margin disables centering
        theme = pygame_menu.themes.THEME_BLUE.copy()
        theme.scrollarea_outer_margin = (0, 100)
        menu = MenuUtils.generic_menu(theme=theme)
        self.assertFalse(menu._auto_centering)

        # Normal
        theme = pygame_menu.themes.THEME_BLUE.copy()
        menu = MenuUtils.generic_menu(theme=theme)
        self.assertTrue(menu._auto_centering)

        # Text offset
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.title_font_size = 35
        theme.widget_font_size = 25

        menu = pygame_menu.Menu(
            column_min_width=400,
            height=300,
            theme=theme,
            title='Images in v4',
            width=400
        )

        menu.add.label('Text #1')
        menu.add.vertical_margin(100)
        menu.add.label('Text #2')
        v = 36
        if pygame.version.vernum[0] < 2:
            v = 35

        self.assertEqual(menu._widget_offset[1], v)

    def test_getters(self) -> None:
        """
        Test other getters.
        """
        self.assertTrue(self.menu.get_menubar_widget() is not None)
        self.assertTrue(self.menu.get_scrollarea() is not None)

        w, h = self.menu.get_size()
        self.assertEqual(int(w), 600)
        self.assertEqual(int(h), 400)

        w, h = self.menu.get_window_size()
        self.assertEqual(int(w), 600)
        self.assertEqual(int(h), 600)

    def test_generic_events(self) -> None:
        """
        Test key events.
        """
        self.menu.clear()

        # Add a menu and a method that set a function
        event_val = [False]

        def _some_event() -> str:
            event_val[0] = True
            return 'the value'

        # Add some widgets
        button = None
        wid = []
        for i in range(5):
            button = self.menu.add.button('button', _some_event)
            wid.append(button.get_id())
        self.assertEqual(len(self.menu.get_widgets()), 5)

        # Create a event in pygame
        self.menu.update(PygameUtils.key(pygame_menu.controls.KEY_MOVE_UP, keydown=True))
        self.assertEqual(self.menu.get_index(), 1)

        # Move down twice
        for i in range(2):
            self.menu.update(PygameUtils.key(pygame_menu.controls.KEY_MOVE_DOWN, keydown=True))
        self.assertEqual(self.menu.get_index(), 4)
        self.menu.update(PygameUtils.key(pygame_menu.controls.KEY_MOVE_UP, keydown=True))
        self.assertEqual(self.menu.get_index(), 0)

        # Press enter, button should trigger and call function
        self.assertEqual(button.apply(), 'the value')
        self.menu.update(PygameUtils.key(pygame_menu.controls.KEY_APPLY, keydown=True))

        # Other
        self.menu.update(PygameUtils.key(pygame_menu.controls.KEY_CLOSE_MENU, keydown=True))
        self.menu.update(PygameUtils.key(pygame_menu.controls.KEY_BACK, keydown=True))

        # Check index is the same as before
        self.assertEqual(self.menu.get_index(), 0)

        # Check joy
        self.menu.update(PygameUtils.joy_key(pygame_menu.controls.JOY_UP))
        self.assertEqual(self.menu.get_index(), 4)
        self.menu.update(PygameUtils.joy_key(pygame_menu.controls.JOY_DOWN))
        self.assertEqual(self.menu.get_index(), 0)
        self.menu.update(PygameUtils.joy_motion(1, 1))
        self.assertEqual(self.menu.get_index(), 1)
        self.menu.update(PygameUtils.joy_motion(1, -1))
        self.assertEqual(self.menu.get_index(), 0)
        self.menu.update(PygameUtils.joy_motion(1, -1))
        self.assertEqual(self.menu.get_index(), 4)

        click_pos = button.get_rect(to_real_position=True).center
        self.menu.update(PygameUtils.mouse_click(click_pos[0], click_pos[1]))
        self.assertTrue(event_val[0])
        event_val[0] = False

    def test_back_event(self) -> None:
        """
        Test back event.
        """
        self.menu.clear()
        self.assertEqual(self.menu._get_depth(), 0)
        menu = MenuUtils.generic_menu(title='submenu')
        button = self.menu.add.button('open', menu)
        button.apply()
        self.assertEqual(self.menu._get_depth(), 1)
        self.menu.update(PygameUtils.key(pygame_menu.controls.KEY_BACK, keydown=True))  # go back
        self.assertEqual(self.menu._get_depth(), 0)

    def test_mouse_empty_submenu(self) -> None:
        """
        Test mouse event where the following submenu has less elements.
        """
        self.menu.clear()
        self.menu.enable()

        submenu = MenuUtils.generic_menu()  # 1 option
        submenu.add.button('button', lambda: None)

        self.menu.add.button('button', lambda: None)
        self.menu.add.button('button', lambda: None)
        button = self.menu.add.button('button', submenu)
        self.menu.disable()
        self.assertRaises(RuntimeError, lambda: self.menu.draw(surface))
        self.menu.enable()
        self.menu.draw(surface)

        click_pos = button.get_rect(to_real_position=True).center
        self.menu.update(PygameUtils.mouse_click(click_pos[0], click_pos[1]))

    def test_input_data(self) -> None:
        """
        Test input data gathering.
        """
        self.menu.clear()

        self.menu.add.text_input('text1', textinput_id='id1', default=1)  # Force to string
        data = self.menu.get_input_data(True)
        self.assertEqual(data['id1'], '1')

        self.menu.add.text_input('text1', textinput_id='id2', default=1.5, input_type=pygame_menu.locals.INPUT_INT)
        data = self.menu.get_input_data(True)
        self.assertEqual(data['id2'], 1)  # Cast to int
        self.assertRaises(IndexError, lambda: self.menu.add.text_input('text1', textinput_id='id1', default=1))

        self.menu.add.text_input('text1', textinput_id='id3', default=1.5, input_type=pygame_menu.locals.INPUT_FLOAT)
        data = self.menu.get_input_data(True)
        self.assertEqual(data['id3'], 1.5)  # Correct

        # Add input to a submenu
        submenu = MenuUtils.generic_menu()
        submenu.add.text_input('text', textinput_id='id4', default='thewidget')
        self.menu.add.button('submenu', submenu)
        data = self.menu.get_input_data(recursive=True)
        self.assertEqual(data['id4'], 'thewidget')

        # Add a submenu within submenu with a repeated id, menu.get_input_data
        # should raise an exception
        subsubmenu = MenuUtils.generic_menu()
        subsubmenu.add.text_input('text', textinput_id='id4', default='repeateddata')
        submenu.add.button('submenu', subsubmenu)
        self.assertRaises(ValueError, lambda: self.menu.get_input_data(recursive=True))

    # noinspection PyTypeChecker
    def test_columns_menu(self) -> None:
        """
        Test menu columns behaviour.
        """
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(columns=0))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(columns=-1))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(rows=0))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(rows=-10))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(columns=2, rows=0))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(columns=2))  # none rows

        # Assert append more widgets than number of rows*columns
        column_menu = MenuUtils.generic_menu(columns=2, rows=4, enabled=False)
        for _ in range(8):
            column_menu.add.button('test', pygame_menu.events.BACK)
        self.assertRaises(RuntimeError, lambda: column_menu.mainloop(surface, bgfun=dummy_function, disable_loop=True))
        column_menu._move_selected_left_right(-1)
        column_menu._move_selected_left_right(1)
        column_menu.disable()
        self.assertRaises(RuntimeError, lambda: column_menu.draw(surface))
        column_menu.enable()
        column_menu.draw(surface)
        column_menu.disable()
        self.assertEqual(len(column_menu._widgets), 8)
        self.assertRaises(RuntimeError, lambda: column_menu.draw(surface))
        self.assertRaises(pygame_menu.menu._MenuWidgetOverflow,
                          lambda: column_menu.add.button('test', pygame_menu.events.BACK))
        column_menu._update_widget_position()
        self.assertEqual(len(column_menu._widgets), 8)  # Widget not added

        # Test max width
        self.assertRaises(AssertionError,
                          lambda: MenuUtils.generic_menu(columns=3, rows=4, column_max_width=[500, 500, 500, 500]))
        column_menu = MenuUtils.generic_menu(columns=3, rows=4, column_max_width=0)  # max menu width
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(columns=3, rows=4, column_max_width=-1))
        column_menu = MenuUtils.generic_menu(columns=3, rows=4, column_max_width=500)  # max menu width
        self.assertEqual(len(column_menu._column_max_width), 3)
        for i in range(3):
            self.assertEqual(column_menu._column_max_width[i], 500)

        # Test min width
        self.assertRaises(AssertionError,
                          lambda: MenuUtils.generic_menu(columns=3, rows=4, column_min_width=[500, 500, 500, 500]))
        column_menu = MenuUtils.generic_menu(columns=3, rows=4, column_min_width=100)  # max menu width
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(columns=3, rows=4, column_min_width=-100))
        column_menu = MenuUtils.generic_menu(columns=3, rows=4, column_min_width=500)  # max menu width
        self.assertEqual(len(column_menu._column_min_width), 3)
        for i in range(3):
            self.assertEqual(column_menu._column_min_width[i], 500)
        self.assertRaises(AssertionError,
                          lambda: MenuUtils.generic_menu(columns=3, rows=4, column_min_width=None))

        # Test max width should be greater than min width
        self.assertRaises(AssertionError,
                          lambda: MenuUtils.generic_menu(columns=2, rows=4, column_min_width=[500, 500],
                                                         column_max_width=[100, 500]))
        self.assertRaises(AssertionError,
                          lambda: MenuUtils.generic_menu(columns=2, rows=4, column_min_width=[500, 500],
                                                         column_max_width=[500, 100]))
        self.assertRaises(AssertionError,
                          lambda: MenuUtils.generic_menu(rows=4, column_min_width=10, column_max_width=1))

        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(columns=-1, rows=4, column_max_width=500))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(rows=0, column_max_width=500))
        MenuUtils.generic_menu(column_max_width=[500])

        # Test different rows
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(columns=2, rows=[3, 3, 3]))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(columns=2, rows=[3, -3]))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(columns=2, rows=[3]))

        # Create widget positioning
        width = 600
        menu = MenuUtils.generic_menu(columns=3, rows=2, width=width)
        btn1 = menu.add.button('btn', None)
        btn2 = menu.add.button('btn', None)
        btn3 = menu.add.button('btn', None)
        btn4 = menu.add.button('btn', None)
        btn5 = menu.add.button('btn', None)
        btn6 = menu.add.button('btn', None)
        self.assertEqual(btn1.get_col_row_index(), (0, 0, 0))
        self.assertEqual(btn2.get_col_row_index(), (0, 1, 1))
        self.assertEqual(btn3.get_col_row_index(), (1, 0, 2))
        self.assertEqual(btn4.get_col_row_index(), (1, 1, 3))
        self.assertEqual(btn5.get_col_row_index(), (2, 0, 4))
        self.assertEqual(btn6.get_col_row_index(), (2, 1, 5))

        # Check size
        self.assertEqual(len(menu._column_widths), 3)
        for colw in menu._column_widths:
            self.assertEqual(colw, width / 3)

        # If removing widget, all column row should change
        menu.remove_widget(btn1)
        self.assertEqual(btn1.get_col_row_index(), (-1, -1, -1))
        self.assertEqual(btn2.get_col_row_index(), (0, 0, 0))
        self.assertEqual(btn3.get_col_row_index(), (0, 1, 1))
        self.assertEqual(btn4.get_col_row_index(), (1, 0, 2))
        self.assertEqual(btn5.get_col_row_index(), (1, 1, 3))
        self.assertEqual(btn6.get_col_row_index(), (2, 0, 4))

        # Hide widget, the column layout should change
        btn2.hide()
        menu.render()
        self.assertEqual(btn2.get_col_row_index(), (-1, -1, 0))
        self.assertEqual(btn3.get_col_row_index(), (0, 0, 1))
        self.assertEqual(btn4.get_col_row_index(), (0, 1, 2))
        self.assertEqual(btn5.get_col_row_index(), (1, 0, 3))
        self.assertEqual(btn6.get_col_row_index(), (1, 1, 4))

        # Show again
        btn2.show()
        menu.render()
        self.assertEqual(btn1.get_col_row_index(), (-1, -1, -1))
        self.assertEqual(btn2.get_col_row_index(), (0, 0, 0))
        self.assertEqual(btn3.get_col_row_index(), (0, 1, 1))
        self.assertEqual(btn4.get_col_row_index(), (1, 0, 2))
        self.assertEqual(btn5.get_col_row_index(), (1, 1, 3))
        self.assertEqual(btn6.get_col_row_index(), (2, 0, 4))

        # Remove button
        menu.remove_widget(btn2)
        self.assertEqual(btn3.get_col_row_index(), (0, 0, 0))
        self.assertEqual(btn4.get_col_row_index(), (0, 1, 1))
        self.assertEqual(btn5.get_col_row_index(), (1, 0, 2))
        self.assertEqual(btn6.get_col_row_index(), (1, 1, 3))

        self.assertEqual(len(menu._column_widths), 2)
        for colw in menu._column_widths:
            self.assertEqual(colw, width / 2)  # 600/2

        # Add a new button
        btn7 = menu.add.button('btn', None)

        # Layout:
        # btn3 | btn5 | btn7
        # btn4 | btn6 |

        # Select second button
        self.assertRaises(ValueError, lambda: menu.select_widget(btn2))
        menu.select_widget(btn4)
        self.assertTrue(btn4.is_selected())

        # Move to right, btn6 should be selected
        menu._move_selected_left_right(1)
        self.assertFalse(btn4.is_selected())
        self.assertTrue(btn6.is_selected())
        self.assertFalse(btn7.is_selected())

        # Move right, as third column only has 1 widget, that should be selected
        menu._move_selected_left_right(1)
        self.assertFalse(btn6.is_selected())
        self.assertTrue(btn7.is_selected())

        # Move right, moves from 3 to 1 column, then button 3 should be selected
        menu._move_selected_left_right(1)
        self.assertFalse(btn7.is_selected())
        self.assertTrue(btn3.is_selected())

        # Set btn4 as floating, then the layout should be
        # btn3,4 | btn6
        # btn5   | btn7
        btn4.set_float()
        menu.render()
        self.assertEqual(btn3.get_col_row_index(), (0, 0, 0))
        self.assertEqual(btn4.get_col_row_index(), (0, 0, 1))
        self.assertEqual(btn5.get_col_row_index(), (0, 1, 2))
        self.assertEqual(btn6.get_col_row_index(), (1, 0, 3))
        self.assertEqual(btn7.get_col_row_index(), (1, 1, 4))

        # Test sizing
        # btn3   | btn6
        # btn4,5 | btn7
        btn4.set_float(False)
        btn5.set_float()
        menu.render()

        self.assertEqual(btn3.get_width(apply_selection=True), 65)
        for colw in menu._column_widths:
            self.assertEqual(colw, width / 2)

        # Scale 4, this should not change menu column widths
        btn4.scale(5, 5)
        menu.render()
        for colw in menu._column_widths:
            self.assertEqual(colw, width / 2)

        # Scale 3, this should change menu column widths
        btn3.scale(5, 1)
        btn3_sz = btn3.get_width(apply_selection=True)
        btn6_sz = btn6.get_width(apply_selection=True)
        menu.render()
        col_width1 = width * btn3_sz / (btn3_sz + btn6_sz)
        col_width2 = width - col_width1
        self.assertAlmostEqual(menu._column_widths, [col_width1, col_width2])

        # Test different rows per column
        menu = MenuUtils.generic_menu(columns=3, rows=[2, 1, 2], width=width, column_max_width=[300, None, 100])
        btn1 = menu.add.button('btn', None)
        btn2 = menu.add.button('btn', None)
        btn3 = menu.add.button('btn', None)
        btn4 = menu.add.button('btn', None)
        btn5 = menu.add.button('btn', None)
        self.assertEqual(btn1.get_col_row_index(), (0, 0, 0))
        self.assertEqual(btn2.get_col_row_index(), (0, 1, 1))
        self.assertEqual(btn3.get_col_row_index(), (1, 0, 2))
        self.assertEqual(btn4.get_col_row_index(), (2, 0, 3))
        self.assertEqual(btn5.get_col_row_index(), (2, 1, 4))

        btn1.scale(10, 1)
        self.assertRaises(pygame_menu.menu._MenuSizingException, lambda: menu.render())

        btn1.resize(300, 10)
        menu.render()

        self.assertEqual(menu._column_widths, [300, 200, 100])
        self.assertEqual(menu._column_pos_x, [150, 400, 550])

        # btn1 | btn3 | btn4
        # btn2 |      | btn5

        # Change menu max column width, this should
        # fulfill third column to its maximum possible less than 300
        # col2 should keep its current width
        menu._column_max_width = [300, None, 300]
        menu.render()
        self.assertEqual(menu._column_widths, [300, 65, 235])
        self.assertEqual(menu._column_pos_x, [150, 332.5, 482.5])

        # Chance maximum width of third column and enlarge button 4, then
        # middle column 3 will take 600-300-100 = 200
        menu._column_max_width = [300, None, 100]
        btn5.resize(100, 10)
        menu.render()
        self.assertEqual(menu._column_widths, [300, 200, 100])

        # Test minimum width
        menu = MenuUtils.generic_menu(columns=3, rows=[2, 1, 2], width=width,
                                      column_max_width=[200, None, 150], column_min_width=[150, 150, 150])
        # btn1 | btn3 | btn4
        # btn2 |      | btn5
        btn1 = menu.add.button('btn', None)
        menu.add.button('btn', None)
        menu.add.button('btn', None)
        menu.add.button('btn', None)
        menu.add.button('btn', None)
        btn1.resize(200, 10)
        menu.render()  # This should scale 2 column
        self.assertEqual(menu._column_widths, [200, 250, 150])

        menu = MenuUtils.generic_menu(columns=3, rows=[2, 1, 2], width=width,
                                      column_max_width=[200, 150, 150], column_min_width=[150, 150, 150])
        btn1 = menu.add.button('btn', None)
        btn2 = menu.add.button('btn', None)
        btn3 = menu.add.button('btn', None)
        menu.add.button('btn', None)
        menu.add.button('btn', None)
        btn1.resize(200, 10)
        btn2.resize(150, 1)
        btn3.resize(150, 1)
        menu.render()
        self.assertEqual(menu._column_widths, [200, 150, 150])

    def test_screen_dimension(self) -> None:
        """
        Test screen dim.
        """
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(title='mainmenu', screen_dimension=1))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(title='mainmenu', screen_dimension=(-1, 1)))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(title='mainmenu', screen_dimension=(1, -1)))

        # The menu is 600x400, so using a lower screen throws an error
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(title='mainmenu', screen_dimension=(1, 1)))
        menu = MenuUtils.generic_menu(title='mainmenu', screen_dimension=(888, 999))
        self.assertEqual(menu.get_window_size()[0], 888)
        self.assertEqual(menu.get_window_size()[1], 999)

    def test_touchscreen(self) -> None:
        """
        Test menu touchscreen behaviour.
        """
        vmajor, _, _ = pygame.version.vernum
        if vmajor < 2:
            self.assertRaises(AssertionError,
                              lambda: MenuUtils.generic_menu(title='mainmenu', touchscreen=True))
            return

        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(title='mainmenu', touchscreen=False,
                                                                         touchscreen_motion_selection=True))
        menu = MenuUtils.generic_menu(title='mainmenu', touchscreen=True, enabled=False)
        self.assertRaises(RuntimeError, lambda: menu.mainloop(surface, bgfun=dummy_function))

        # Add a menu and a method that set a function
        event_val = [False]

        def _some_event() -> str:
            event_val[0] = True
            return 'the value'

        # Add some widgets
        button = menu.add.button('button', _some_event)

        # Check touch
        if hasattr(pygame, 'FINGERUP'):
            click_pos = button.get_rect(to_real_position=True).center
            menu.enable()
            menu.update(
                PygameUtils.touch_click(click_pos[0], click_pos[1], normalize=False))  # Event must be normalized
            self.assertFalse(event_val[0])

            menu.update(PygameUtils.touch_click(click_pos[0], click_pos[1], menu=menu))
            self.assertTrue(event_val[0])
            event_val[0] = False
            self.assertEqual(menu.get_selected_widget().get_id(), button.get_id())
            btn = menu.get_selected_widget()
            self.assertTrue(btn.get_selected_time() >= 0)

    def test_reset_value(self) -> None:
        """
        Test menu reset value.
        """
        menu = MenuUtils.generic_menu(title='mainmenu')
        menu2 = MenuUtils.generic_menu(title='other')

        color = menu.add.color_input('title', default='ff0000', color_type='hex')
        text = menu.add.text_input('title', default='epic')
        selector = menu.add.selector('title', items=[('a', 1), ('b', 2)], default=1)
        text2 = menu2.add.text_input('titlesub', default='not epic')
        menu.add.label('mylabel')
        menu.add.button('submenu', menu2)

        # Change values
        color.set_value('aaaaaa')
        text.set_value('changed')
        text2.set_value('changed2')
        selector.set_value(0)

        # Reset values
        color.reset_value()
        self.assertEqual(color.get_value(as_string=True), '#ff0000')
        color.set_value('aaaaaa')

        # Check values changed
        self.assertEqual(color.get_value(as_string=True), '#aaaaaa')
        self.assertEqual(text.get_value(), 'changed')
        self.assertEqual(selector.get_index(), 0)

        # Reset values
        menu.reset_value(recursive=True)
        self.assertEqual(color.get_value(as_string=True), '#ff0000')
        self.assertEqual(text.get_value(), 'epic')
        self.assertEqual(text2.get_value(), 'not epic')
        self.assertEqual(selector.get_index(), 1)

    def test_mainloop_kwargs(self) -> None:
        """
        Test menu mainloop kwargs.
        """
        test = [False, False]

        def test_accept_menu(m: 'pygame_menu.Menu') -> None:
            """
            This method accept menu as argument.
            """
            assert isinstance(m, pygame_menu.Menu)
            test[0] = True

        def test_not_accept_menu() -> None:
            """
            This method does not accept menu as argument.
            """
            test[1] = True

        menu = MenuUtils.generic_menu()
        self.assertFalse(test[0])
        menu.mainloop(surface, test_accept_menu, disable_loop=True)
        self.assertTrue(test[0])
        self.assertFalse(test[1])
        menu.mainloop(surface, test_not_accept_menu, disable_loop=True)
        self.assertTrue(test[0])
        self.assertTrue(test[1])

    # noinspection PyArgumentList
    def test_invalid_args(self) -> None:
        """
        Test menu invalid args.
        """
        self.assertRaises(TypeError, lambda: pygame_menu.Menu(height=100, width=100, title='nice', fake_option=True))

    def test_set_title(self) -> None:
        """
        Test menu title.
        """
        menu = MenuUtils.generic_menu(title='menu')
        theme = menu.get_theme()
        menubar = menu.get_menubar_widget()

        self.assertEqual(menu.get_title(), 'menu')
        self.assertEqual(menubar.get_title_offset()[0], theme.title_offset[0])
        self.assertEqual(menubar.get_title_offset()[1], theme.title_offset[1])

        menu.set_title('nice')
        self.assertEqual(menu.get_title(), 'nice')
        self.assertEqual(menubar.get_title_offset()[0], theme.title_offset[0])
        self.assertEqual(menubar.get_title_offset()[1], theme.title_offset[1])

        menu.set_title('nice', offset=(9, 10))
        self.assertEqual(menu.get_title(), 'nice')
        self.assertEqual(menubar.get_title_offset()[0], 9)
        self.assertEqual(menubar.get_title_offset()[1], 10)

        menu.set_title('nice2')
        self.assertEqual(menu.get_title(), 'nice2')
        self.assertEqual(menubar.get_title_offset()[0], theme.title_offset[0])
        self.assertEqual(menubar.get_title_offset()[1], theme.title_offset[1])

    def test_empty(self) -> None:
        """
        Test empty menu.
        """
        menu = MenuUtils.generic_menu(title='menu')
        menu.render()
        self.assertEqual(menu.get_height(widget=True), 0)

        # Adds a button, hide it, then the height should be 0 as well
        btn = menu.add.button('hidden', None)
        btn.hide()
        self.assertEqual(menu.get_height(widget=True), 0)

    def test_beforeopen(self) -> None:
        """
        Test beforeopen event.
        """
        menu = MenuUtils.generic_menu()
        menu2 = MenuUtils.generic_menu()
        test = [False]

        def onbeforeopen(menu_from: 'pygame_menu.Menu', menu_to: 'pygame_menu.Menu') -> None:
            """
            Before open callback.
            """
            self.assertEqual(menu_from, menu)
            self.assertEqual(menu_to, menu2)
            test[0] = True

        menu2.set_onbeforeopen(onbeforeopen)
        self.assertFalse(test[0])
        menu.add.button('to2', menu2).apply()
        self.assertTrue(test[0])

    def test_focus(self) -> None:
        """
        Test menu focus effect.
        """
        menu = MenuUtils.generic_menu(title='menu', mouse_motion_selection=True)
        btn = menu.add.button('nice', None)
        # menu.add.button('nice', None)

        # Test focus
        btn.active = True
        focus = menu._draw_focus_widget(surface, btn)
        # menu.mainloop(surface)
        self.assertEqual(len(focus), 4)
        if pygame.version.vernum[0] < 2:
            self.assertEqual(focus[1], ((0, 0), (600, 0), (600, 301), (0, 301)))
            self.assertEqual(focus[2], ((0, 302), (261, 302), (261, 353), (0, 353)))
            self.assertEqual(focus[3], ((337, 302), (600, 302), (600, 353), (337, 353)))
            self.assertEqual(focus[4], ((0, 354), (600, 354), (600, 600), (0, 600)))
        else:
            self.assertEqual(focus[1], ((0, 0), (600, 0), (600, 302), (0, 302)))
            self.assertEqual(focus[2], ((0, 303), (261, 303), (261, 353), (0, 353)))
            self.assertEqual(focus[3], ((337, 303), (600, 303), (600, 353), (337, 353)))
            self.assertEqual(focus[4], ((0, 354), (600, 354), (600, 600), (0, 600)))

        # Test cases where the focus must fail
        btn._selected = False
        self.assertEqual(None, menu._draw_focus_widget(surface, btn))
        btn._selected = True

        # Set active false
        btn.active = False
        self.assertEqual(None, menu._draw_focus_widget(surface, btn))
        btn.active = True

        btn.hide()
        self.assertEqual(None, menu._draw_focus_widget(surface, btn))
        btn.show()

        btn.is_selectable = False
        self.assertEqual(None, menu._draw_focus_widget(surface, btn))
        btn.is_selectable = True

        menu._mouse_motion_selection = False
        self.assertEqual(None, menu._draw_focus_widget(surface, btn))
        menu._mouse_motion_selection = True

        btn.active = True
        btn._selected = True
        self.assertNotEqual(None, menu._draw_focus_widget(surface, btn))

    def test_visible(self) -> None:
        """
        Test visible.
        """
        menu = MenuUtils.generic_menu(title='menu')
        btn1 = menu.add.button('nice', None)
        btn2 = menu.add.button('nice', None)
        self.assertTrue(btn1.is_selected())
        btn2.hide()
        menu.select_widget(btn1)

        # btn2 cannot be selected as it is hidden
        self.assertRaises(ValueError, lambda: menu.select_widget(btn2))
        btn2.show()
        menu.select_widget(btn2)

        # Hide buttons
        btn1.hide()
        btn2.hide()

        self.assertFalse(btn1.is_selected())
        self.assertFalse(btn2.is_selected())

        c1, r1, i1 = btn1.get_col_row_index()
        c2, r2, i2 = btn2.get_col_row_index()
        self.assertEqual(c1, -1)
        self.assertEqual(c2, -1)
        self.assertEqual(i1, 0)
        self.assertEqual(c2, -1)
        self.assertEqual(r2, -1)
        self.assertEqual(i2, 1)

        menu.remove_widget(btn1)
        c1, r1, i1 = btn1.get_col_row_index()
        c2, r2, i2 = btn2.get_col_row_index()
        self.assertEqual(c1, -1)
        self.assertEqual(c2, -1)
        self.assertEqual(i1, -1)
        self.assertEqual(c2, -1)
        self.assertEqual(r2, -1)
        self.assertEqual(i2, 0)

        menu.remove_widget(btn2)
        c1, r1, i1 = btn1.get_col_row_index()
        c2, r2, i2 = btn2.get_col_row_index()
        self.assertEqual(c1, -1)
        self.assertEqual(c2, -1)
        self.assertEqual(i1, -1)
        self.assertEqual(c2, -1)
        self.assertEqual(r2, -1)
        self.assertEqual(i2, -1)

        menu = MenuUtils.generic_menu(title='menu')
        btn = menu.add.button('button', None)
        self.assertTrue(btn.is_selected())
        btn.hide()

        # As theres no more visible widgets, index must be -1
        self.assertEqual(menu._index, -1)
        self.assertFalse(btn.is_selected())
        btn.show()

        # Widget should be selected, and index must be 0
        self.assertTrue(btn.is_selected())
        self.assertEqual(menu._index, 0)

        # Hide button, and set is as unselectable
        btn.hide()
        btn.is_selectable = False
        self.assertEqual(menu._index, -1)
        btn.show()

        # Now, as widget is not selectable, button should not
        # be selected and index still -1
        self.assertFalse(btn.is_selected())
        self.assertEqual(menu._index, -1)

        # Set selectable again
        btn.is_selectable = True
        btn.select()
        self.assertEqual(menu._index, -1)  # Menu still don't considers widget as selected
        self.assertIsNone(menu.get_selected_widget())
        btn.select(update_menu=True)
        self.assertEqual(menu.get_selected_widget(), btn)

    def test_decorator(self) -> None:
        """
        Test menu decorator.
        """
        menu = MenuUtils.generic_menu()
        dec = menu.get_decorator()
        self.assertEqual(menu, dec._obj)

    # noinspection PyArgumentEqualDefault
    def test_events(self) -> None:
        """
        Test events gather.
        """
        if pygame.vernum[0] < 2:
            return
        menu_top = MenuUtils.generic_menu()
        menu = MenuUtils.generic_menu(columns=4, rows=2, touchscreen=True,
                                      touchscreen_motion_selection=True, column_min_width=[400, 300, 400, 300],
                                      joystick_enabled=True)  # submenu
        menu_top.add.button('menu', menu).apply()
        widg = []
        for i in range(8):
            b = menu.add.button('test' + str(i), None)
            widg.append(b)
        # btn0 | btn2 | btn4 | btn6
        # btn1 | btn3 | btn5 | btn7

        self.assertEqual(menu_top.get_current(), menu)

        # Arrow keys
        self.assertEqual(menu.get_selected_widget(), widg[0])
        menu_top.update(PygameUtils.key(pygame_menu.controls.KEY_LEFT, keydown=True))
        self.assertEqual(menu.get_selected_widget(), widg[6])
        menu_top.update(PygameUtils.key(pygame_menu.controls.KEY_MOVE_UP, keydown=True))
        self.assertEqual(menu.get_selected_widget(), widg[7])
        menu_top.update(PygameUtils.key(pygame_menu.controls.KEY_RIGHT, keydown=True))
        self.assertEqual(menu.get_selected_widget(), widg[1])
        menu_top.update(PygameUtils.key(pygame_menu.controls.KEY_MOVE_DOWN, keydown=True))
        self.assertEqual(menu.get_selected_widget(), widg[0])

        # Joy key
        menu_top.update(PygameUtils.joy_key(pygame_menu.controls.JOY_LEFT))
        self.assertEqual(menu.get_selected_widget(), widg[6])
        menu_top.update(PygameUtils.joy_key(pygame_menu.controls.JOY_DOWN))
        self.assertEqual(menu.get_selected_widget(), widg[7])
        menu_top.update(PygameUtils.joy_key(pygame_menu.controls.JOY_RIGHT))
        self.assertEqual(menu.get_selected_widget(), widg[1])
        menu_top.update(PygameUtils.joy_key(pygame_menu.controls.JOY_UP))
        self.assertEqual(menu.get_selected_widget(), widg[0])

        # Joy hat
        menu_top.update(PygameUtils.joy_motion(-10, 0))
        self.assertEqual(menu_top.get_current()._joy_event, pygame_menu.menu.JOY_EVENT_LEFT)
        self.assertEqual(menu.get_selected_widget(), widg[6])
        menu_top.update(PygameUtils.joy_motion(0, 10))
        self.assertEqual(menu_top.get_current()._joy_event, pygame_menu.menu.JOY_EVENT_DOWN)
        self.assertEqual(menu.get_selected_widget(), widg[7])
        menu_top.update(PygameUtils.joy_motion(10, 0))
        self.assertEqual(menu_top.get_current()._joy_event, pygame_menu.menu.JOY_EVENT_RIGHT)
        self.assertEqual(menu.get_selected_widget(), widg[1])
        menu_top.update(PygameUtils.joy_motion(0, -10))
        self.assertEqual(menu_top.get_current()._joy_event, pygame_menu.menu.JOY_EVENT_UP)
        self.assertEqual(menu.get_selected_widget(), widg[0])

        # Menu should keep a recursive state of joy
        self.assertNotEqual(menu.get_current()._joy_event, 0)
        menu_top.update(PygameUtils.center_joy())  # center !!
        self.assertEqual(menu.get_current()._joy_event, 0)

        # Click widget
        menu_top.enable()
        menu_top.update([PygameUtils.middle_rect_click(widg[1], evtype=pygame.MOUSEBUTTONDOWN)])
        self.assertEqual(menu.get_selected_widget(), widg[1])
        menu_top.update([PygameUtils.middle_rect_click(widg[0], evtype=pygame.MOUSEBUTTONDOWN)])
        self.assertEqual(menu.get_selected_widget(), widg[0])
        menu_top.update([PygameUtils.middle_rect_click(widg[1], evtype=pygame.MOUSEBUTTONDOWN)])
        self.assertEqual(menu.get_selected_widget(), widg[1])

        # It should not change the menu selection (button up)
        self.assertTrue(
            menu_top.update([PygameUtils.middle_rect_click(widg[1], evtype=pygame.MOUSEBUTTONUP)]))
        self.assertEqual(menu.get_selected_widget(), widg[1])

        # Applying button up in a non-selected widget must return false
        self.assertFalse(
            menu.update([PygameUtils.middle_rect_click(widg[0], evtype=pygame.MOUSEBUTTONUP)]))

        # Fingerdown don't change selected widget if _touchscreen_motion_selection is enabled
        self.assertTrue(menu._touchscreen_motion_selection)
        menu.update([PygameUtils.middle_rect_click(widg[0], evtype=pygame.FINGERDOWN)])
        # self.assertNotEqual(menu.get_selected_widget(), widg[0])

        # If touchscreen motion is disabled, then fingerdown should select the widget
        menu._touchscreen_motion_selection = False
        menu.update([PygameUtils.middle_rect_click(widg[1], evtype=pygame.FINGERDOWN)])
        self.assertEqual(menu.get_selected_widget(), widg[1])
        menu._touchscreen_motion_selection = True

        # Fingermoution should select widgets as touchscreen is active
        menu.update([PygameUtils.middle_rect_click(widg[0], evtype=pygame.FINGERMOTION)])
        self.assertEqual(menu.get_selected_widget(), widg[0])

        # Infinite joy
        menu_top.update(PygameUtils.joy_motion(0, 10))
        menu.update([pygame.event.Event(menu._joy_event_repeat)])
        self.assertNotEqual(menu._joy_event, 0)

        # Now disable joy event, then event repeat should not continue
        menu._joy_event = 0
        menu.update([pygame.event.Event(menu._joy_event_repeat)])
        menu_top.update(PygameUtils.center_joy())  # center !!
        self.assertEqual(menu.get_current()._joy_event, 0)

        # Active widget, and click outside to disable it (only if motion selection enabled)
        widg = menu.get_selected_widget()
        widg.active = True

        # Clicking the same rect should not fire the callback
        menu_top.update([PygameUtils.middle_rect_click(widg, evtype=pygame.MOUSEBUTTONDOWN)])
        self.assertTrue(widg.active)
        self.assertTrue(widg.is_selected())

        widg._rect.x += 500
        menu._mouse_motion_selection = True
        menu_top.update([PygameUtils.middle_rect_click(widg, evtype=pygame.MOUSEBUTTONDOWN)])
        self.assertFalse(widg.active)

        # Test mouseover and mouseleave
        test: Any = [None]

        def onover(m: 'pygame_menu.Menu', e: 'pygame.event.Event') -> None:
            """
            Mouse over menu.
            """
            self.assertIsInstance(m, pygame_menu.Menu)
            self.assertEqual(e.type, pygame.MOUSEMOTION)
            test[0] = True

        def onleave(m: 'pygame_menu.Menu', e: 'pygame.event.Event') -> None:
            """
            Mouse leave menu.
            """
            self.assertIsInstance(m, pygame_menu.Menu)
            self.assertEqual(e.type, pygame.MOUSEMOTION)
            test[0] = False

        menu = MenuUtils.generic_menu(width=100, height=100)
        menu.set_onmouseover(onover)
        menu.set_onmouseleave(onleave)

        self.assertIsNone(test[0])
        ev = PygameUtils.mouse_click(50, 50, inlist=True, evtype=pygame.MOUSEMOTION)
        self.assertFalse(menu._mouseover)
        menu.update(ev)
        self.assertFalse(test[0])

        rect = menu.get_rect()
        ev = PygameUtils.mouse_click(rect.centerx, rect.centery, inlist=True, evtype=pygame.MOUSEMOTION)
        menu.update(ev)
        self.assertTrue(test[0])
        self.assertTrue(menu._mouseover)

        ev = PygameUtils.mouse_click(50, 50, inlist=True, evtype=pygame.MOUSEMOTION)
        menu.update(ev)
        self.assertFalse(menu._mouseover)
        self.assertFalse(test[0])

        # Test window mouseover and mouseleave
        test: Any = [None]

        def onover(m: 'pygame_menu.Menu') -> None:
            """
            Mouse over window.
            """
            self.assertIsInstance(m, pygame_menu.Menu)
            test[0] = True

        def onleave(m: 'pygame_menu.Menu') -> None:
            """
            Mouse leave window.
            """
            self.assertIsInstance(m, pygame_menu.Menu)
            test[0] = False

        menu.set_onwindowmouseover(onover)
        menu.set_onwindowmouseleave(onleave)

        self.assertIsNone(test[0])
        menu.update([pygame.event.Event(pygame.ACTIVEEVENT, {'gain': 1})])  # Enter
        self.assertTrue(test[0])
        menu.update([pygame.event.Event(pygame.ACTIVEEVENT, {'gain': 0})])  # Enter
        self.assertFalse(test[0])

    def test_frame(self) -> None:
        """
        Test frame menu support.
        """
        # Test frame movement
        theme = pygame_menu.themes.THEME_DEFAULT.copy()
        theme.widget_font_size = 20
        menu = MenuUtils.generic_menu(columns=3, rows=2, theme=theme)

        # btn0 | f1(btn2,btn3,btn4,btn5) | f2(btn7,
        #      |                         |    btn8,
        #      |                         |    f3(btn9,btn10))
        # btn1 |           btn6          | f4(btn11,btn12,btn13)
        btn0 = menu.add.button('btn0', None)
        btn1 = menu.add.button('btn1', None)
        f1 = menu.add.frame_h(200, 50, frame_id='f1')
        btn2 = menu.add.button('btn2 ', None)
        btn3 = menu.add.button('btn3 ', None)
        btn4 = menu.add.button('btn4 ', None)
        btn5 = menu.add.button('btn5 ', None)
        btn6 = menu.add.button('btn6', None)
        f2 = menu.add.frame_v(200, 132, background_color=(100, 0, 0), frame_id='f2')
        f3 = menu.add.frame_h(200, 50, background_color=(0, 0, 100), frame_id='f3')
        f4 = menu.add.frame_h(260, 50, frame_id='f4')
        btn7 = menu.add.button('btn7', None)
        btn8 = menu.add.button('btn8', None)
        btn9 = menu.add.button('btn9 ', None)
        btn10 = menu.add.button('btn10', None)
        btn11 = menu.add.button('btn11 ', None)
        btn12 = menu.add.button('btn12 ', None)
        btn13 = menu.add.button('btn13', None)
        f1.pack((btn2, btn3, btn4, btn5))
        f3.pack((btn9, btn10))
        f2.pack((btn7, btn8, f3), alignment=pygame_menu.locals.ALIGN_CENTER)
        f4.pack((btn11, btn12, btn13))

        # Test min max indices
        self.assertEqual(f1.get_indices(), (2, 5))
        self.assertEqual(f2.get_indices(), (8, 10))
        self.assertEqual(f3.get_indices(), (12, 13))
        self.assertEqual(f4.get_indices(), (14, 16))

        # Check positioning
        self.assertEqual(btn0.get_col_row_index(), (0, 0, 0))
        self.assertEqual(btn1.get_col_row_index(), (0, 1, 1))
        self.assertEqual(f1.get_col_row_index(), (1, 0, 6))
        self.assertEqual(btn6.get_col_row_index(), (1, 1, 7))
        self.assertEqual(f2.get_col_row_index(), (2, 0, 11))
        self.assertEqual(f4.get_col_row_index(), (2, 1, 17))

        self.assertFalse(f1.is_scrollable)
        self.assertFalse(f2.is_scrollable)
        self.assertFalse(f3.is_scrollable)
        self.assertEqual(menu._test_widgets_status(), (
            (('Button-btn0', (0, 0, 0), (13, 77), (1, 0, 1, 1, (42, 28))),
             ('Button-btn1', (0, 1, 1), (13, 115), (1, 0, 0, 1, (42, 28))),
             ('Button-btn2 ', (1, 0, 2), (84, 77), (1, 1, 0, 1, (47, 28))),
             ('Button-btn3 ', (1, 0, 3), (131, 77), (1, 1, 0, 1, (47, 28))),
             ('Button-btn4 ', (1, 0, 4), (178, 77), (1, 1, 0, 1, (47, 28))),
             ('Button-btn5 ', (1, 0, 5), (225, 77), (1, 1, 0, 1, (47, 28))),
             ('Frame',
              (1, 0, 6),
              (84, 77),
              ('Button-btn2 ', (1, 0, 2), (84, 77), (1, 1, 0, 1, (47, 28))),
              ('Button-btn3 ', (1, 0, 3), (131, 77), (1, 1, 0, 1, (47, 28))),
              ('Button-btn4 ', (1, 0, 4), (178, 77), (1, 1, 0, 1, (47, 28))),
              ('Button-btn5 ', (1, 0, 5), (225, 77), (1, 1, 0, 1, (47, 28))),
              (2, 5),
              (0, 0, 0, 1, (200, 50))),
             ('Button-btn6', (1, 1, 7), (163, 137), (1, 0, 0, 1, (42, 28))),
             ('Button-btn7', (2, 0, 8), (429, 77), (1, 1, 0, 1, (42, 28))),
             ('Button-btn8', (2, 0, 9), (429, 105), (1, 1, 0, 1, (42, 28))),
             ('Frame',
              (2, 0, 10),
              (350, 133),
              ('Button-btn9 ', (2, 0, 12), (350, 133), (1, 1, 0, 1, (47, 28))),
              ('Button-btn10', (2, 0, 13), (397, 133), (1, 1, 0, 1, (53, 28))),
              (12, 13),
              (0, 1, 0, 1, (200, 50))),
             ('Frame',
              (2, 0, 11),
              (350, 77),
              ('Button-btn7', (2, 0, 8), (429, 77), (1, 1, 0, 1, (42, 28))),
              ('Button-btn8', (2, 0, 9), (429, 105), (1, 1, 0, 1, (42, 28))),
              ('Button-btn9 ', (2, 0, 12), (350, 133), (1, 1, 0, 1, (47, 28))),
              ('Button-btn10', (2, 0, 13), (397, 133), (1, 1, 0, 1, (53, 28))),
              (8, 10),
              (0, 0, 0, 1, (200, 132))),
             ('Button-btn9 ', (2, 0, 12), (350, 133), (1, 1, 0, 1, (47, 28))),
             ('Button-btn10', (2, 0, 13), (397, 133), (1, 1, 0, 1, (53, 28))),
             ('Button-btn11 ', (2, 1, 14), (320, 219), (1, 1, 0, 1, (58, 28))),
             ('Button-btn12 ', (2, 1, 15), (378, 219), (1, 1, 0, 1, (58, 28))),
             ('Button-btn13', (2, 1, 16), (436, 219), (1, 1, 0, 1, (53, 28))),
             ('Frame',
              (2, 1, 17),
              (320, 219),
              ('Button-btn11 ', (2, 1, 14), (320, 219), (1, 1, 0, 1, (58, 28))),
              ('Button-btn12 ', (2, 1, 15), (378, 219), (1, 1, 0, 1, (58, 28))),
              ('Button-btn13', (2, 1, 16), (436, 219), (1, 1, 0, 1, (53, 28))),
              (14, 16),
              (0, 0, 0, 1, (260, 50))))
        ))

        # Arrow keys
        self.assertEqual(menu.get_selected_widget(), btn0)
        menu.update(PygameUtils.key(pygame_menu.controls.KEY_RIGHT, keydown=True))
        self.assertEqual(menu.get_selected_widget(), btn2)
        menu.update(PygameUtils.key(pygame_menu.controls.KEY_RIGHT, keydown=True))
        self.assertEqual(menu.get_selected_widget(), btn3)
        menu.update(PygameUtils.key(pygame_menu.controls.KEY_RIGHT, keydown=True))
        self.assertEqual(menu.get_selected_widget(), btn4)
        menu.update(PygameUtils.key(pygame_menu.controls.KEY_RIGHT, keydown=True))
        self.assertEqual(menu.get_selected_widget(), btn5)
        menu.update(PygameUtils.key(pygame_menu.controls.KEY_RIGHT, keydown=True))
        self.assertEqual(menu.get_selected_widget(), btn7)
        menu.update(PygameUtils.key(pygame_menu.controls.KEY_RIGHT, keydown=True))
        self.assertEqual(menu.get_selected_widget(), btn0)
        menu.update(PygameUtils.key(pygame_menu.controls.KEY_LEFT, keydown=True))
        self.assertEqual(menu.get_selected_widget(), btn10)
        menu.update(PygameUtils.key(pygame_menu.controls.KEY_LEFT, keydown=True))
        self.assertEqual(menu.get_selected_widget(), btn9)
        menu.update(PygameUtils.key(pygame_menu.controls.KEY_LEFT, keydown=True))
        self.assertEqual(menu.get_selected_widget(), btn5)
        menu.update(PygameUtils.key(pygame_menu.controls.KEY_LEFT, keydown=True))
        self.assertEqual(menu.get_selected_widget(), btn4)
        menu.update(PygameUtils.key(pygame_menu.controls.KEY_LEFT, keydown=True))
        self.assertEqual(menu.get_selected_widget(), btn3)
        menu.update(PygameUtils.key(pygame_menu.controls.KEY_LEFT, keydown=True))
        self.assertEqual(menu.get_selected_widget(), btn2)
        menu.update(PygameUtils.key(pygame_menu.controls.KEY_LEFT, keydown=True))
        self.assertEqual(menu.get_selected_widget(), btn0)
        for bt in (btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12, btn13, btn0, btn1):
            menu.update(PygameUtils.key(pygame_menu.controls.KEY_MOVE_UP, keydown=True))
            self.assertEqual(menu.get_selected_widget(), bt)
        for bt in (btn6, btn11, btn12, btn13, btn1):
            menu.update(PygameUtils.joy_key(pygame_menu.controls.JOY_RIGHT))
            self.assertEqual(menu.get_selected_widget(), bt)
        for bt in (btn0, btn13, btn12, btn11, btn10, btn9, btn8, btn7, btn6, btn5, btn4, btn3, btn2, btn1, btn0):
            menu.update(PygameUtils.key(pygame_menu.controls.KEY_MOVE_DOWN, keydown=True))
            self.assertEqual(menu.get_selected_widget(), bt)
        menu.update(PygameUtils.key(pygame_menu.controls.KEY_MOVE_UP, keydown=True))
        self.assertEqual(menu.get_selected_widget(), btn1)
        for bt in (btn13, btn12, btn11, btn6, btn1):
            menu.update(PygameUtils.joy_key(pygame_menu.controls.JOY_LEFT))
            self.assertEqual(menu.get_selected_widget(), bt)

        # Test removing frame
        self.assertEqual(len(f2._widgets), 3)
        self.assertEqual(len(f3._widgets), 2)
        menu.remove_widget(f3)
        self.assertEqual(len(f2._widgets), 2)
        self.assertEqual(len(f3._widgets), 0)
        self.assertEqual(menu._test_widgets_status(), (
            (('Button-btn0', (0, 0, 0), (18, 77), (1, 0, 0, 1, (42, 28))),
             ('Button-btn1', (0, 1, 1), (18, 115), (1, 0, 1, 1, (42, 28))),
             ('Button-btn2 ', (1, 0, 2), (108, 77), (1, 1, 0, 1, (47, 28))),
             ('Button-btn3 ', (1, 0, 3), (155, 77), (1, 1, 0, 1, (47, 28))),
             ('Button-btn4 ', (1, 0, 4), (202, 77), (1, 1, 0, 1, (47, 28))),
             ('Button-btn5 ', (1, 0, 5), (249, 77), (1, 1, 0, 1, (47, 28))),
             ('Frame',
              (1, 0, 6),
              (108, 77),
              ('Button-btn2 ', (1, 0, 2), (108, 77), (1, 1, 0, 1, (47, 28))),
              ('Button-btn3 ', (1, 0, 3), (155, 77), (1, 1, 0, 1, (47, 28))),
              ('Button-btn4 ', (1, 0, 4), (202, 77), (1, 1, 0, 1, (47, 28))),
              ('Button-btn5 ', (1, 0, 5), (249, 77), (1, 1, 0, 1, (47, 28))),
              (2, 5),
              (0, 0, 0, 1, (200, 50))),
             ('Button-btn6', (1, 1, 7), (187, 137), (1, 0, 0, 1, (42, 28))),
             ('Button-btn7', (2, 0, 8), (448, 77), (1, 1, 0, 1, (42, 28))),
             ('Button-btn8', (2, 0, 9), (448, 105), (1, 1, 0, 1, (42, 28))),
             ('Frame',
              (2, 0, 10),
              (369, 77),
              ('Button-btn7', (2, 0, 8), (448, 77), (1, 1, 0, 1, (42, 28))),
              ('Button-btn8', (2, 0, 9), (448, 105), (1, 1, 0, 1, (42, 28))),
              (8, 9),
              (0, 0, 0, 1, (200, 132))),
             ('Button-btn11 ', (2, 1, 11), (339, 219), (1, 1, 0, 1, (58, 28))),
             ('Button-btn12 ', (2, 1, 12), (397, 219), (1, 1, 0, 1, (58, 28))),
             ('Button-btn13', (2, 1, 13), (455, 219), (1, 1, 0, 1, (53, 28))),
             ('Frame',
              (2, 1, 14),
              (339, 219),
              ('Button-btn11 ', (2, 1, 11), (339, 219), (1, 1, 0, 1, (58, 28))),
              ('Button-btn12 ', (2, 1, 12), (397, 219), (1, 1, 0, 1, (58, 28))),
              ('Button-btn13', (2, 1, 13), (455, 219), (1, 1, 0, 1, (53, 28))),
              (11, 13),
              (0, 0, 0, 1, (260, 50))),
             ('Button-btn9 ', (2, 1, 15), (446, 219), (1, 1, 0, 1, (47, 28))),
             ('Button-btn10', (2, 1, 16), (443, 219), (1, 1, 0, 1, (53, 28))))
        ))

        # btn0 | f1(btn2,btn3,btn4,btn5) | f2(btn7,
        #      |                         |    btn8)
        # btn1 |            btn6         | f4(btn11,btn12,btn13)+(floating9,10)
        menu.select_widget(btn0)
        for i in range(14):
            menu.update(PygameUtils.key(pygame_menu.controls.KEY_MOVE_UP, keydown=True))
        self.assertEqual(menu.get_selected_widget(), btn0)
        for i in range(14):
            menu.update(PygameUtils.key(pygame_menu.controls.KEY_MOVE_DOWN, keydown=True))
        self.assertEqual(menu.get_selected_widget(), btn0)

    # noinspection PyTypeChecker
    def test_widget_move_index(self) -> None:
        """
        Test widget index moving.
        """
        menu = MenuUtils.generic_menu()
        btn1 = menu.add.button('1', None)
        btn2 = menu.add.button('2', None)
        btn3 = menu.add.button('3', None)

        def test_order(button: Tuple['pygame_menu.widgets.Button', ...],
                       selected: 'pygame_menu.widgets.Button') -> None:
            """
            Test button order.
            """
            self.assertEqual(menu.get_selected_widget(), selected)
            sel = []
            for w in button:
                sel.append(int(w == selected))
            if pygame.version.vernum[0] >= 2:
                self.assertEqual(menu._test_widgets_status(), (
                    ('Button-' + button[0].get_title(), (0, 0, 0), (291, 102), (1, 0, sel[0], 1, (17, 41))),
                    ('Button-' + button[1].get_title(), (0, 1, 1), (291, 153), (1, 0, sel[1], 1, (17, 41))),
                    ('Button-' + button[2].get_title(), (0, 2, 2), (291, 204), (1, 0, sel[2], 1, (17, 41)))
                ))
            else:
                self.assertEqual(menu._test_widgets_status(), (
                    ('Button-' + button[0].get_title(), (0, 0, 0), (291, 100), (1, 0, sel[0], 1, (17, 42))),
                    ('Button-' + button[1].get_title(), (0, 1, 1), (291, 152), (1, 0, sel[1], 1, (17, 42))),
                    ('Button-' + button[2].get_title(), (0, 2, 2), (291, 204), (1, 0, sel[2], 1, (17, 42)))
                ))

        test_order((btn1, btn2, btn3), btn1)
        menu.move_widget_index(btn1)  # Move to last
        test_order((btn2, btn3, btn1), btn1)
        menu.move_widget_index(btn3, 0)
        test_order((btn3, btn2, btn1), btn1)
        menu.move_widget_index(btn2, btn1)  # 2 after 1
        test_order((btn3, btn1, btn2), btn1)
        self.assertRaises(AssertionError, lambda: menu.move_widget_index(btn2, btn1, append=False))
        self.assertRaises(AssertionError, lambda: menu.move_widget_index(btn2, btn2))
        menu.move_widget_index(btn1, btn2, append=False)  # 2 after 1
        test_order((btn3, btn2, btn1), btn1)

        # Reverse
        menu.move_widget_index(None)
        test_order((btn1, btn2, btn3), btn1)
        menu.select_widget(btn2)
        test_order((btn1, btn2, btn3), btn2)
        menu.move_widget_index(None)
        self.assertEqual(menu.get_selected_widget(), btn2)
        test_order((btn3, btn2, btn1), btn2)
        menu.move_widget_index(btn1, 0)
        self.assertRaises(AssertionError, lambda: menu.move_widget_index(btn1, -1))
        self.assertRaises(AssertionError, lambda: menu.move_widget_index(btn1, -1.5))
        test_order((btn1, btn3, btn2), btn2)

    def test_mouseover_widget(self) -> None:
        """
        Test mouseover + motion.
        """
        menu = MenuUtils.generic_menu()
        btn1 = menu.add.button('1', None)
        btn2 = menu.add.button('2', None)

        # Setup
        self.assertTrue(btn1.is_selected())
        self.assertFalse(menu._mouse_motion_selection)
        self.assertIsNone(menu._widget_mouseover)

        test = [False, False, False, False]  # btn1over, btn1leave, btn2over, btn2leave

        def onover1(widget, _) -> None:
            """
            Onover event.
            """
            self.assertEqual(btn1, widget)
            test[0] = True

        def onleave1(widget, _) -> None:
            """
            Onleave event.
            """
            self.assertEqual(btn1, widget)
            test[1] = True

        def onover2(widget, _) -> None:
            """
            Onover event.
            """
            self.assertEqual(btn2, widget)
            test[2] = True

        def onleave2(widget, _) -> None:
            """
            Onleave event.
            """
            self.assertEqual(btn2, widget)
            test[3] = True

        btn1.set_onmouseover(onover1)
        btn1.set_onmouseleave(onleave1)
        btn2.set_onmouseover(onover2)
        btn2.set_onmouseleave(onleave2)

        btn1.set_cursor(pygame_menu.locals.CURSOR_HAND)

        # Test before
        self.assertEqual(test, [False, False, False, False])
        if pygame_menu.widgets.core.widget._CURSOR_PREV[0] is not None:
            pygame_menu.widgets.core.widget._CURSOR_PREV[0] = None
        self.assertIsNone(pygame_menu.widgets.core.widget._CURSOR_PREV[0])  # None cursor should be the start

        # Place mouse over widget 1, it should set as mouseover and trigger the events
        deco = menu.get_decorator()

        def drawrect() -> None:
            """
            Draw absolute rect on surface for testing purposes.
            """
            surface.fill((255, 255, 255), btn1.get_rect(to_real_position=True))

        deco.add_callable(drawrect, prev=False, pass_args=False)
        # menu.mainloop(surface)

        menu.update([PygameUtils.middle_rect_click(btn1, menu, evtype=pygame.MOUSEMOTION)])
        self.assertEqual(menu._widget_mouseover, btn1)
        self.assertEqual(menu.get_selected_widget(), btn1)
        self.assertEqual(test, [True, False, False, False])
        if pygame.version.vernum[0] < 2:
            self.assertIsNone(pygame_menu.widgets.core.widget._CURSOR_PREV[0])
        else:
            self.assertIsNotNone(pygame_menu.widgets.core.widget._CURSOR_PREV[0])

        # Place mouse away. This should force widget 1 mouseleave
        menu.update([PygameUtils.middle_rect_click((1000, 1000), menu, evtype=pygame.MOUSEMOTION)])
        self.assertEqual(test, [True, True, False, False])
        self.assertIsNone(pygame_menu.widgets.core.widget._CURSOR_PREV[0])
        self.assertIsNone(menu._widget_mouseover)

        # Place over widget 2
        menu.update([PygameUtils.middle_rect_click(btn2, menu, evtype=pygame.MOUSEMOTION)])
        self.assertEqual(menu._widget_mouseover, btn2)
        self.assertEqual(test, [True, True, True, False])
        self.assertIsNone(pygame_menu.widgets.core.widget._CURSOR_PREV[0])  # button 2 don't have any cursor

        # Place mouse away. This should force widget 1 mouseleave
        menu.update([PygameUtils.middle_rect_click((1000, 1000), menu, evtype=pygame.MOUSEMOTION)])
        self.assertEqual(test, [True, True, True, True])
        self.assertIsNone(pygame_menu.widgets.core.widget._CURSOR_PREV[0])
        self.assertIsNone(menu._widget_mouseover)

        # Test immediate switch, from 1 to 2, then from 2 to 1, then off
        test = [False, False, False, False]
        menu.update([PygameUtils.middle_rect_click(btn1, menu, evtype=pygame.MOUSEMOTION)])
        self.assertEqual(menu._widget_mouseover, btn1)
        self.assertEqual(menu.get_selected_widget(), btn1)
        self.assertEqual(test, [True, False, False, False])
        if pygame.version.vernum[0] < 2:
            self.assertIsNone(pygame_menu.widgets.core.widget._CURSOR_PREV[0])
        else:
            self.assertIsNotNone(pygame_menu.widgets.core.widget._CURSOR_PREV[0])
        menu.update([PygameUtils.middle_rect_click(btn2, menu, evtype=pygame.MOUSEMOTION)])
        self.assertEqual(menu._widget_mouseover, btn2)
        self.assertEqual(menu.get_selected_widget(), btn1)
        self.assertEqual(test, [True, True, True, False])
        self.assertIsNone(pygame_menu.widgets.core.widget._CURSOR_PREV[0])
        menu.update([PygameUtils.middle_rect_click((1000, 1000), menu, evtype=pygame.MOUSEMOTION)])
        self.assertEqual(test, [True, True, True, True])
        self.assertIsNone(pygame_menu.widgets.core.widget._CURSOR_PREV[0])
        self.assertIsNone(menu._widget_mouseover)

        # Same switch test, but now with widget selection by mouse motion
        menu._mouse_motion_selection = True
        test = [False, False, False, False]
        menu.select_widget(btn2)
        self.assertEqual(menu.get_selected_widget(), btn2)
        menu.update([PygameUtils.middle_rect_click(btn1, menu, evtype=pygame.MOUSEMOTION)])
        self.assertEqual(menu._widget_mouseover, btn1)
        self.assertEqual(menu.get_selected_widget(), btn1)
        self.assertEqual(test, [True, False, False, False])
        if pygame.version.vernum[0] < 2:
            self.assertIsNone(pygame_menu.widgets.core.widget._CURSOR_PREV[0])
        else:
            self.assertIsNotNone(pygame_menu.widgets.core.widget._CURSOR_PREV[0])
        menu.update([PygameUtils.middle_rect_click(btn2, menu, evtype=pygame.MOUSEMOTION)])
        self.assertEqual(menu._widget_mouseover, btn2)
        self.assertEqual(menu.get_selected_widget(), btn2)
        self.assertEqual(test, [True, True, True, False])
        self.assertIsNone(pygame_menu.widgets.core.widget._CURSOR_PREV[0])
        menu.update([PygameUtils.middle_rect_click((1000, 1000), menu, evtype=pygame.MOUSEMOTION)])
        self.assertEqual(test, [True, True, True, True])
        self.assertIsNone(pygame_menu.widgets.core.widget._CURSOR_PREV[0])
        self.assertIsNone(menu._widget_mouseover)

    def test_floating_pos(self) -> None:
        """
        Test floating widgets.
        """
        # First, add a widget and test the positioning
        menu = MenuUtils.generic_menu()
        btn = menu.add.button('floating', None)
        self.assertEqual(btn.get_alignment(), pygame_menu.locals.ALIGN_CENTER)
        expc_pos = (247, 153)
        if pygame.version.vernum[0] < 2:
            expc_pos = (247, 152)
        self.assertEqual(btn.get_position(), expc_pos)
        btn.set_float()
        self.assertEqual(btn.get_position(), expc_pos)
        btn.set_float(menu_render=True)
        self.assertEqual(btn.get_position(), expc_pos)

        # Auto set pos width if zero
        menu = MenuUtils.generic_menu(columns=3, rows=[2, 2, 2])
        self.assertEqual(len(menu._column_widths), 0)
        for i in range(6):
            menu.add.none_widget()
        self.assertEqual(menu._column_widths, [200, 200, 200])

        menu = MenuUtils.generic_menu(columns=3, rows=[2, 2, 2], column_min_width=[300, 100, 100])
        self.assertEqual(len(menu._column_widths), 0)
        for i in range(6):
            menu.add.none_widget()
        # This should be proportional
        self.assertEqual(menu._column_widths, [360.0, 120.0, 120.0])

        menu = MenuUtils.generic_menu(columns=3, rows=[2, 2, 2], column_min_width=[600, 600, 600])
        self.assertEqual(len(menu._column_widths), 0)
        for i in range(6):
            menu.add.none_widget()
        # This should be proportional
        self.assertEqual(menu._column_widths, [600, 600, 600])

        menu = MenuUtils.generic_menu(columns=3, rows=[2, 2, 2], column_max_width=[100, None, None])
        self.assertEqual(len(menu._column_widths), 0)
        for i in range(6):
            menu.add.none_widget()

        # This should be proportional
        self.assertEqual(menu._column_widths, [100, 250, 250])

    def test_surface_cache(self) -> None:
        """
        Surface cache tests.
        """
        menu = MenuUtils.generic_menu()
        self.assertFalse(menu._widgets_surface_need_update)
        menu.force_surface_cache_update()
        menu.force_surface_update()
        self.assertTrue(menu._widgets_surface_need_update)
