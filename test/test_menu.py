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

import timeit
import unittest
from test._utils import surface, test_reset_surface, MenuUtils, PygameUtils

import pygame
import pygame_menu
from pygame_menu import events
from pygame_menu.widgets import Label, Button
from pygame_menu.utils import dummy_function

# Configure the tests
_TEST_TIME_DRAW = False


class MenuTest(unittest.TestCase):

    def setUp(self) -> None:
        """
        Test setup.
        """
        test_reset_surface()
        self.menu = MenuUtils.generic_menu(title='mainmenu')
        self.menu.mainloop(surface, bgfun=dummy_function)

    @staticmethod
    def test_time_draw() -> None:
        """
        This test the time that takes to pygame_menu to draw several times.
        """
        if not _TEST_TIME_DRAW:
            return
        menu = MenuUtils.generic_menu(title='EPIC')
        menu.enable()

        # Add several widgets
        for i in range(30):
            menu.add_button(title='epic', action=events.BACK)
            menu.add_vertical_margin(margin=10)
            menu.add_label(title='epic test')
            menu.add_color_input(title='color', color_type='rgb', default=(234, 33, 2))
            menu.add_selector(title='epic selector', items=[('1', '3'), ('2', '4')])
            menu.add_text_input(title='text', default='the default text')

        print(timeit.timeit(lambda: menu.draw(surface), number=100))

    def test_size(self) -> None:
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
        btn = menu.add_button('button', None)
        menu.center_content()
        self.assertEqual(menu.get_height(), 400)
        self.assertEqual(menu.get_height(inner=True), 345)
        self.assertEqual(menu.get_menubar_widget().get_height(), 55)

        h = 41
        if pygame.version.vernum.major < 2:
            h = 42

        self.assertEqual(btn.get_height(), h)
        self.assertEqual(btn.get_size()[1], h)
        self.assertEqual(menu.get_height(widget=True), h)

        vpos = int((345 - h) / 2)  # available_height - widget_height
        self.assertEqual(menu._widget_offset[1], vpos)
        self.assertEqual(btn.get_position()[1], vpos + 1)

        # If there's too many widgets, the centering should be disabled
        for i in range(20):
            menu.add_button('button', None)
        self.assertEqual(menu._widget_offset[1], 0)

        theme = menu.get_theme()

        # Anyway, as the widget is 0, the first button position should be the height of its selection effect
        btneff = btn.get_selection_effect().get_margin()[0]
        self.assertEqual(btn.get_position()[1], btneff + 1)

        self.assertEqual(h * 21 + theme.widget_margin[1] * 20, menu.get_height(widget=True))

        # Test menu not centered
        menu = MenuUtils.generic_menu(center_content=False)
        btn = menu.add_button('button', None)
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
            column_min_width=400,
            columns=2,
            height=300,
            rows=4,
            theme=theme,
            title='Welcome',
            width=400
        )

        quit1 = menu.add_button('Quit', pygame_menu.events.EXIT)
        name1 = menu.add_text_input('Name: ', default='John Doe', maxchar=10, padding=30)
        sel1 = menu.add_selector('Difficulty: ', [('Hard', 1), ('Easy', 2)])
        sel2 = menu.add_selector('Difficulty: ', [('Hard', 1), ('Easy', 2)])
        play1 = menu.add_button('Play', pygame_menu.events.NONE, align=pygame_menu.locals.ALIGN_LEFT)
        play1.set_float(True)
        play2 = menu.add_button('Play 2', pygame_menu.events.NONE, align=pygame_menu.locals.ALIGN_RIGHT)
        hidden = menu.add_button('Hidden', None, font_size=100)
        hidden.hide()
        quit2 = menu.add_button('Quit', pygame_menu.events.EXIT)
        label = menu.add_label('This label is really epic')
        label.rotate(90)

        menu.render()

        x, y = quit1.get_position()
        self.assertEqual(x, 180)
        self.assertEqual(y, 6)
        x, y = name1.get_position()
        self.assertEqual(x, 125)
        self.assertEqual(y, 74)
        x, y = sel1.get_position()
        self.assertEqual(x, 114)
        self.assertEqual(y, 142)
        x, y = sel2.get_position()
        self.assertEqual(x, 114)
        self.assertEqual(y, 180)
        x, y = play1.get_position()
        self.assertEqual(x, 409)
        self.assertEqual(y, 6)
        x, y = play2.get_position()
        self.assertEqual(x, 737)
        self.assertEqual(y, 6)
        x, y = hidden.get_position()
        self.assertEqual(x, 0)
        self.assertEqual(y, 0)
        x, y = quit2.get_position()
        self.assertEqual(x, 580)
        self.assertEqual(y, 44)
        x, y = label.get_position()
        self.assertEqual(x, 586)
        self.assertEqual(y, 82)

        # Test no selectable position
        menu = MenuUtils.generic_menu(center_content=False)
        btn = menu.add_button('button', None)
        btn.is_selectable = False
        menu.render()
        self.assertEqual(btn.get_position()[1], 1)

        # Test no selectable + widget
        menu = MenuUtils.generic_menu()
        img = menu.add_image(
            pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU,
            scale=(0.25, 0.25),
            align=pygame_menu.locals.ALIGN_CENTER
        )
        btn = menu.add_button('Nice', None)
        margin = menu.get_theme().widget_margin[1]
        menu.render()
        self.assertEqual(menu.get_height(widget=True), img.get_height() + btn.get_height() + margin)
        self.assertEqual(int((menu.get_height(inner=True) - menu.get_height(widget=True)) / 2), menu._widget_offset[1])

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
        menu.set_attribute('epic', False)
        menu._back()

        def test_close() -> None:
            menu.set_attribute('epic', True)

        menu.set_onclose(test_close)
        self.assertTrue(not menu.is_enabled())
        menu.enable()
        self.assertFalse(menu.get_attribute('epic'))
        menu._close()
        self.assertTrue(menu.get_attribute('epic'))

    def test_enabled(self) -> None:
        """
        Test menu enable/disable feature.
        """
        menu = MenuUtils.generic_menu(onclose=events.NONE)
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
            button = menu_prev.add_button('open', menu)
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

        widget = self.menu.add_text_input('test', textinput_id='some_id')
        widget_found = self.menu.get_widget('some_id')
        self.assertEqual(widget, widget_found)

        # Add a widget to a deepest menu
        prev_menu = self.menu
        for i in range(11):
            menu = MenuUtils.generic_menu()
            prev_menu.add_button('menu', menu)
            prev_menu = menu

        # Add a deep input
        deep_widget = prev_menu.add_text_input('title', textinput_id='deep_id')
        deep_selector = prev_menu.add_selector('selector', [('0', 0), ('1', 1)], selector_id='deep_selector', default=1)

        self.assertEqual(self.menu.get_widget('deep_id', recursive=False), None)
        self.assertEqual(self.menu.get_widget('deep_id', recursive=True), deep_widget)
        self.assertEqual(self.menu.get_widget('deep_selector', recursive=True), deep_selector)

    def test_add_generic_widget(self) -> None:
        """
        Test generic widget.
        """
        self.menu.clear()
        menu = MenuUtils.generic_menu()
        btn = menu.add_button('nice', None)
        w = Button('title')
        self.menu.add_generic_widget(w)
        self.assertRaises(ValueError, lambda: menu.add_generic_widget(w))
        btn._menu = None
        self.menu.add_generic_widget(btn)

    # noinspection PyArgumentEqualDefault
    def test_get_selected_widget(self) -> None:
        """
        Tests get current widget.
        """
        self.menu.clear()

        # Test widget selection and removal
        widget = self.menu.add_text_input('test', default='some_id')
        self.assertEqual(widget, self.menu.get_selected_widget())
        self.menu.remove_widget(widget)
        self.assertEqual(self.menu.get_selected_widget(), None)
        self.assertEqual(self.menu.get_index(), -1)

        # Add two widgets, first widget will be selected first, but if removed the second should be selected
        widget1 = self.menu.add_text_input('test', default='some_id', textinput_id='epic')
        self.assertRaises(IndexError, lambda: self.menu.add_text_input('test', default='some_id', textinput_id='epic'))
        widget2 = self.menu.add_text_input('test', default='some_id')
        self.assertEqual(widget1.get_menu(), self.menu)
        self.assertEqual(widget1, self.menu.get_selected_widget())
        self.menu.remove_widget(widget1)
        self.assertEqual(widget1.get_menu(), None)
        self.assertEqual(widget2, self.menu.get_selected_widget())
        self.menu.remove_widget(widget2)
        self.assertEqual(widget2.get_menu(), None)
        self.assertEqual(len(self.menu.get_widgets()), 0)

        # Add 3 widgets, select the last one and remove it, then the selected widget must be the first
        w1 = self.menu.add_button('1', None)
        w2 = Label('2')
        self.menu.add_generic_widget(w2, configure_defaults=True)
        w3 = self.menu.add_button('3', None)
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
        self.assertEqual(self.menu.get_selected_widget(), None)
        self.assertRaises(ValueError, lambda: self.menu.select_widget(w1))

        # Mark w1 as selectable
        w1.is_selectable = True
        self.menu.add_generic_widget(w2)
        self.assertEqual(self.menu.get_selected_widget(), w2)

        # Add a new widget that cannot be selected
        self.menu.add_label('not selectable')
        self.menu.add_label('not selectable')
        wlast = self.menu.add_label('not selectable', selectable=True)

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
        self.assertEqual(self.menu.get_selected_widget(), None)

        # Unhide w2, then it should be selected
        w2.show()
        self.assertEqual(self.menu.get_selected_widget(), w2)

        # Remove w2, then nothing should be selected
        self.menu.remove_widget(w2)
        self.assertEqual(self.menu.get_selected_widget(), None)

        # Clear all widgets and get index
        self.menu._widgets = []
        self._index = 100
        self.assertEqual(self.menu.get_selected_widget(), None)

        # Destroy index
        self.menu._index = '0'
        self.assertEqual(None, self.menu.get_selected_widget())
        self.assertEqual(self.menu._index, 0)

    def test_submenu(self) -> None:
        """
        Test submenus.
        """
        menu = MenuUtils.generic_menu()
        menu2 = MenuUtils.generic_menu()
        btn = menu.add_button('btn', menu2)
        self.assertTrue(btn.to_menu)
        self.assertTrue(menu.in_submenu(menu2))
        self.assertFalse(menu2.in_submenu(menu))

        btn.update_callback(lambda: None)
        self.assertFalse(btn.to_menu)
        self.assertFalse(menu.in_submenu(menu2))

        # Test recursive
        menu.clear()
        menu2.clear()

        self.assertRaises(ValueError, lambda: menu.add_button('to self', menu))
        menu.add_button('to2', menu2)
        self.assertRaises(ValueError, lambda: menu2.add_button('to1', menu))

    def test_centering(self) -> None:
        """
        Test centering menu.
        """
        # Vertical offset disables centering
        theme = pygame_menu.themes.THEME_BLUE.copy()
        theme.widget_offset = (0, 100)
        menu = MenuUtils.generic_menu(theme=theme)
        self.assertEqual(menu.get_theme(), theme)
        self.assertFalse(menu._center_content)

        # Outer scrollarea margin disables centering
        theme = pygame_menu.themes.THEME_BLUE.copy()
        theme.scrollarea_outer_margin = (0, 100)
        menu = MenuUtils.generic_menu(theme=theme)
        self.assertFalse(menu._center_content)

        # Normal
        theme = pygame_menu.themes.THEME_BLUE.copy()
        menu = MenuUtils.generic_menu(theme=theme)
        self.assertTrue(menu._center_content)

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
            button = self.menu.add_button('button', _some_event)
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

        click_pos = PygameUtils.get_middle_rect(button.get_rect())
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
        button = self.menu.add_button('open', menu)
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
        submenu.add_button('button', lambda: None)

        self.menu.add_button('button', lambda: None)
        self.menu.add_button('button', lambda: None)
        button = self.menu.add_button('button', submenu)
        self.menu.disable()
        self.assertRaises(RuntimeError, lambda: self.menu.draw(surface))
        self.menu.enable()
        self.menu.draw(surface)

        click_pos = PygameUtils.get_middle_rect(button.get_rect())
        self.menu.update(PygameUtils.mouse_click(click_pos[0], click_pos[1]))

    def test_input_data(self) -> None:
        """
        Test input data gathering.
        """
        self.menu.clear()

        self.menu.add_text_input('text1', textinput_id='id1', default=1)  # Force to string
        data = self.menu.get_input_data(True)
        self.assertEqual(data['id1'], '1')

        self.menu.add_text_input('text1', textinput_id='id2', default=1.5, input_type=pygame_menu.locals.INPUT_INT)
        data = self.menu.get_input_data(True)
        self.assertEqual(data['id2'], 1)  # Cast to int
        self.assertRaises(IndexError, lambda: self.menu.add_text_input('text1', textinput_id='id1', default=1))

        self.menu.add_text_input('text1', textinput_id='id3', default=1.5, input_type=pygame_menu.locals.INPUT_FLOAT)
        data = self.menu.get_input_data(True)
        self.assertEqual(data['id3'], 1.5)  # Correct

        # Add input to a submenu
        submenu = MenuUtils.generic_menu()
        submenu.add_text_input('text', textinput_id='id4', default='thewidget')
        self.menu.add_button('submenu', submenu)
        data = self.menu.get_input_data(recursive=True)
        self.assertEqual(data['id4'], 'thewidget')

        # Add a submenu within submenu with a repeated id, menu.get_input_data
        # should raise an exception
        subsubmenu = MenuUtils.generic_menu()
        subsubmenu.add_text_input('text', textinput_id='id4', default='repeateddata')
        submenu.add_button('submenu', subsubmenu)
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
        column_menu = MenuUtils.generic_menu(columns=2, rows=4)
        for _ in range(8):
            column_menu.add_button('test', pygame_menu.events.BACK)
        column_menu.mainloop(surface, bgfun=dummy_function)
        column_menu._move_selected_left_right(-1)
        column_menu._move_selected_left_right(1)
        column_menu.disable()
        self.assertRaises(RuntimeError, lambda: column_menu.draw(surface))
        column_menu.enable()
        column_menu.draw(surface)
        column_menu.disable()
        self.assertRaises(RuntimeError, lambda: column_menu.draw(surface))
        self.assertRaises(AssertionError, lambda: column_menu.add_button('test', pygame_menu.events.BACK))
        self.assertRaises(AssertionError, lambda: column_menu._update_widget_position())  # 9th item

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
        btn1 = menu.add_button('btn', None)
        btn2 = menu.add_button('btn', None)
        btn3 = menu.add_button('btn', None)
        btn4 = menu.add_button('btn', None)
        btn5 = menu.add_button('btn', None)
        btn6 = menu.add_button('btn', None)
        c, r, i = btn1.get_col_row_index()
        self.assertEqual(c, 0)
        self.assertEqual(r, 0)
        self.assertEqual(i, 0)
        c, r, i = btn2.get_col_row_index()
        self.assertEqual(c, 0)
        self.assertEqual(r, 1)
        self.assertEqual(i, 1)
        c, r, i = btn3.get_col_row_index()
        self.assertEqual(c, 1)
        self.assertEqual(r, 0)
        self.assertEqual(i, 2)
        c, r, i = btn4.get_col_row_index()
        self.assertEqual(c, 1)
        self.assertEqual(r, 1)
        self.assertEqual(i, 3)
        c, r, i = btn5.get_col_row_index()
        self.assertEqual(c, 2)
        self.assertEqual(r, 0)
        self.assertEqual(i, 4)
        c, r, i = btn6.get_col_row_index()
        self.assertEqual(c, 2)
        self.assertEqual(r, 1)
        self.assertEqual(i, 5)

        # Check size
        self.assertEqual(len(menu._column_widths), 3)
        for colw in menu._column_widths:
            self.assertEqual(colw, width / 3)

        # If removing widget, all column row should change
        menu.remove_widget(btn1)
        c, r, i = btn1.get_col_row_index()
        self.assertEqual(c, -1)
        self.assertEqual(r, -1)
        self.assertEqual(i, -1)
        c, r, i = btn2.get_col_row_index()
        self.assertEqual(c, 0)
        self.assertEqual(r, 0)
        self.assertEqual(i, 0)
        c, r, i = btn3.get_col_row_index()
        self.assertEqual(c, 0)
        self.assertEqual(r, 1)
        self.assertEqual(i, 1)
        c, r, i = btn4.get_col_row_index()
        self.assertEqual(c, 1)
        self.assertEqual(r, 0)
        self.assertEqual(i, 2)
        c, r, i = btn5.get_col_row_index()
        self.assertEqual(c, 1)
        self.assertEqual(r, 1)
        self.assertEqual(i, 3)
        c, r, i = btn6.get_col_row_index()
        self.assertEqual(c, 2)
        self.assertEqual(r, 0)
        self.assertEqual(i, 4)

        # Hide widget, the column layout should change
        btn2.hide()
        menu.render()
        c, r, i = btn2.get_col_row_index()
        self.assertEqual(c, -1)
        self.assertEqual(r, -1)
        self.assertEqual(i, 0)
        c, r, i = btn3.get_col_row_index()
        self.assertEqual(c, 0)
        self.assertEqual(r, 0)
        self.assertEqual(i, 1)
        c, r, i = btn4.get_col_row_index()
        self.assertEqual(c, 0)
        self.assertEqual(r, 1)
        self.assertEqual(i, 2)
        c, r, i = btn5.get_col_row_index()
        self.assertEqual(c, 1)
        self.assertEqual(r, 0)
        self.assertEqual(i, 3)
        c, r, i = btn6.get_col_row_index()
        self.assertEqual(c, 1)
        self.assertEqual(r, 1)
        self.assertEqual(i, 4)

        # Show again
        btn2.show()
        menu.render()
        c, r, i = btn1.get_col_row_index()
        self.assertEqual(c, -1)
        self.assertEqual(r, -1)
        self.assertEqual(i, -1)
        c, r, i = btn2.get_col_row_index()
        self.assertEqual(c, 0)
        self.assertEqual(r, 0)
        self.assertEqual(i, 0)
        c, r, i = btn3.get_col_row_index()
        self.assertEqual(c, 0)
        self.assertEqual(r, 1)
        self.assertEqual(i, 1)
        c, r, i = btn4.get_col_row_index()
        self.assertEqual(c, 1)
        self.assertEqual(r, 0)
        self.assertEqual(i, 2)
        c, r, i = btn5.get_col_row_index()
        self.assertEqual(c, 1)
        self.assertEqual(r, 1)
        self.assertEqual(i, 3)
        c, r, i = btn6.get_col_row_index()
        self.assertEqual(c, 2)
        self.assertEqual(r, 0)
        self.assertEqual(i, 4)

        # Remove button
        menu.remove_widget(btn2)
        c, r, i = btn3.get_col_row_index()
        self.assertEqual(c, 0)
        self.assertEqual(r, 0)
        self.assertEqual(i, 0)
        c, r, i = btn4.get_col_row_index()
        self.assertEqual(c, 0)
        self.assertEqual(r, 1)
        self.assertEqual(i, 1)
        c, r, i = btn5.get_col_row_index()
        self.assertEqual(c, 1)
        self.assertEqual(r, 0)
        self.assertEqual(i, 2)
        c, r, i = btn6.get_col_row_index()
        self.assertEqual(c, 1)
        self.assertEqual(r, 1)
        self.assertEqual(i, 3)

        self.assertEqual(len(menu._column_widths), 2)
        for colw in menu._column_widths:
            self.assertEqual(colw, width / 2)  # 600/2

        # Add a new button
        btn7 = menu.add_button('btn', None)

        # Layout:
        # btn3 | btn5 | btn7
        # btn4 | btn6 |

        # Select second button
        self.assertRaises(ValueError, lambda: menu.select_widget(btn2))
        menu.select_widget(btn4)
        self.assertTrue(btn4.selected)

        # Move to right, btn6 should be selected
        menu._move_selected_left_right(1)
        self.assertFalse(btn4.selected)
        self.assertTrue(btn6.selected)
        self.assertFalse(btn7.selected)

        # Move right, as third column only has 1 widget, that should be selected
        menu._move_selected_left_right(1)
        self.assertFalse(btn6.selected)
        self.assertTrue(btn7.selected)

        # Move right, moves from 3 to 1 column, then button 3 should be selected
        menu._move_selected_left_right(1)
        self.assertFalse(btn7.selected)
        self.assertTrue(btn3.selected)

        # Set btn4 as floating, then the layout should be
        # btn3   | btn6
        # btn4,5 | btn7
        btn4.set_float(True)
        menu.render()
        c, r, i = btn3.get_col_row_index()
        self.assertEqual(c, 0)
        self.assertEqual(r, 0)
        self.assertEqual(i, 0)
        c, r, i = btn4.get_col_row_index()
        self.assertEqual(c, 0)
        self.assertEqual(r, 1)
        self.assertEqual(i, 1)
        c, r, i = btn5.get_col_row_index()
        self.assertEqual(c, 0)
        self.assertEqual(r, 1)
        self.assertEqual(i, 2)
        c, r, i = btn6.get_col_row_index()
        self.assertEqual(c, 1)
        self.assertEqual(r, 0)
        self.assertEqual(i, 3)
        c, r, i = btn7.get_col_row_index()
        self.assertEqual(c, 1)
        self.assertEqual(r, 1)
        self.assertEqual(i, 4)

        # Test sizing
        # btn3   | btn6
        # btn4,5 | btn7
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
        self.assertAlmostEqual(menu._column_widths[0], col_width1)
        self.assertAlmostEqual(menu._column_widths[1], col_width2)

        # Test different rows per column
        menu = MenuUtils.generic_menu(columns=3, rows=[2, 1, 2], width=width, column_max_width=[300, None, 100])
        btn1 = menu.add_button('btn', None)
        btn2 = menu.add_button('btn', None)
        btn3 = menu.add_button('btn', None)
        btn4 = menu.add_button('btn', None)
        btn5 = menu.add_button('btn', None)
        c, r, i = btn1.get_col_row_index()
        self.assertEqual(c, 0)
        self.assertEqual(r, 0)
        self.assertEqual(i, 0)
        c, r, i = btn2.get_col_row_index()
        self.assertEqual(c, 0)
        self.assertEqual(r, 1)
        self.assertEqual(i, 1)
        c, r, i = btn3.get_col_row_index()
        self.assertEqual(c, 1)
        self.assertEqual(r, 0)
        self.assertEqual(i, 2)
        c, r, i = btn4.get_col_row_index()
        self.assertEqual(c, 2)
        self.assertEqual(r, 0)
        self.assertEqual(i, 3)
        c, r, i = btn5.get_col_row_index()
        self.assertEqual(c, 2)
        self.assertEqual(r, 1)
        self.assertEqual(i, 4)

        btn1.scale(10, 1)
        menu.render()

        self.assertEqual(menu._column_widths[0], 300)
        self.assertEqual(menu._column_widths[1], 200)
        self.assertEqual(menu._column_widths[2], 100)
        self.assertEqual(menu._column_pos_x[0], 150)
        self.assertEqual(menu._column_pos_x[1], 400)
        self.assertEqual(menu._column_pos_x[2], 550)

        # btn1 | btn3 | btn4
        # btn2 |      | btn5

        # Change menu max column width, this should
        # fullfill third column to its maximum possible less than 300
        # col2 should keep its current width
        menu._column_max_width = [300, None, 300]
        menu.render()
        self.assertEqual(menu._column_widths[0], 300)
        self.assertEqual(menu._column_widths[1], 65)
        self.assertEqual(menu._column_widths[2], 235)
        self.assertEqual(menu._column_pos_x[0], 150)
        self.assertEqual(menu._column_pos_x[1], 332.5)
        self.assertEqual(menu._column_pos_x[2], 482.5)

        # Chance maximum width of third column and enlarge button 4, then
        # middle column 3 will take 600-300-100 = 200
        menu._column_max_width = [300, None, 100]
        btn5.scale(10, 1)
        menu.render()
        self.assertEqual(menu._column_widths[0], 300)
        self.assertEqual(menu._column_widths[1], 200)
        self.assertEqual(menu._column_widths[2], 100)

        # Test minimum width
        menu = MenuUtils.generic_menu(columns=3, rows=[2, 1, 2], width=width,
                                      column_max_width=[200, None, 150], column_min_width=[150, 150, 150])
        # btn1 | btn3 | btn4
        # btn2 |      | btn5
        btn1 = menu.add_button('btn', None)
        menu.add_button('btn', None)
        menu.add_button('btn', None)
        menu.add_button('btn', None)
        menu.add_button('btn', None)
        btn1.scale(10, 1)
        menu.render()  # This should scale 2 column
        self.assertEqual(menu._column_widths[0], 200)
        self.assertEqual(menu._column_widths[1], 250)
        self.assertEqual(menu._column_widths[2], 150)

        menu = MenuUtils.generic_menu(columns=3, rows=[2, 1, 2], width=width,
                                      column_max_width=[200, 150, 150], column_min_width=[150, 150, 150])
        btn1 = menu.add_button('btn', None)
        btn2 = menu.add_button('btn', None)
        btn3 = menu.add_button('btn', None)
        menu.add_button('btn', None)
        menu.add_button('btn', None)
        btn1.scale(10, 1)
        btn2.scale(10, 1)
        btn3.scale(10, 1)
        menu.render()
        self.assertEqual(menu._column_widths[0], 200)
        self.assertEqual(menu._column_widths[1], 150)
        self.assertEqual(menu._column_widths[2], 150)

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
        menu = MenuUtils.generic_menu(title='mainmenu', touchscreen=True)
        menu.mainloop(surface, bgfun=dummy_function)

        # Add a menu and a method that set a function
        event_val = [False]

        def _some_event() -> str:
            event_val[0] = True
            return 'the value'

        # Add some widgets
        button = menu.add_button('button', _some_event)

        # Check touch
        click_pos = PygameUtils.get_middle_rect(button.get_rect())
        menu.update(PygameUtils.touch_click(click_pos[0], click_pos[1], normalize=False))  # Event must be normalized
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

        color = menu.add_color_input('title', default='ff0000', color_type='hex')
        text = menu.add_text_input('title', default='epic')
        selector = menu.add_selector('title', items=[('a', 1), ('b', 2)], default=1)
        text2 = menu2.add_text_input('titlesub', default='not epic')
        menu.add_label('mylabel')
        menu.add_button('submenu', menu2)

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
        btn = menu.add_button('hidden', None)
        btn.hide()
        self.assertEqual(menu.get_height(widget=True), 0)

        # Get the size of the scrollarea
        sa = menu.get_scrollarea()

        sa_height = menu.get_height() - menu.get_menubar_widget().get_height()
        sa_width = menu.get_width()
        self.assertEqual(sa.get_world_size()[0], sa_width)
        self.assertEqual(sa.get_world_size()[1], sa_height)
        rect = sa.get_view_rect()
        self.assertEqual(rect.x, 0)
        self.assertEqual(rect.y, 155)
        self.assertEqual(rect.width, sa_width)
        self.assertEqual(rect.height, sa_height)
        self.assertEqual(sa.get_hidden_width(), 0)
        self.assertEqual(sa.get_hidden_height(), 0)

        rect = sa.to_world_position(btn.get_rect())
        self.assertEqual(rect.x, 0)
        self.assertEqual(rect.y, -155)
        self.assertEqual(rect.width, btn.get_width())
        self.assertEqual(rect.height, btn.get_height())

        posrect = sa.to_world_position((10, 10))
        self.assertEqual(posrect[0], 10)
        self.assertEqual(posrect[1], -145)

        self.assertFalse(sa.is_scrolling())
        self.assertEqual(sa.get_menu(), menu)

        sa._on_vertical_scroll(50)
        sa._on_horizontal_scroll(50)

        # Remove the world of surface
        world = sa._world
        sa._world = None
        self.assertEqual(sa.get_world_size()[0], 0)
        self.assertEqual(sa.get_world_size()[0], 0)
        sa._world = world

    def test_focus(self) -> None:
        """
        Test menu focus effect.
        """
        menu = MenuUtils.generic_menu(title='menu', mouse_motion_selection=True)
        btn = menu.add_button('nice', None)

        # Test focus
        btn.active = True
        focus = menu._draw_focus_widget(surface, btn)
        self.assertEqual(len(focus), 4)
        if pygame.version.vernum.major < 2:
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
        btn.selected = False
        self.assertEqual(None, menu._draw_focus_widget(surface, btn))
        btn.selected = True

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
        btn.selected = True
        self.assertNotEqual(None, menu._draw_focus_widget(surface, btn))

    def test_visible(self) -> None:
        """
        Test visible.
        """
        menu = MenuUtils.generic_menu(title='menu')
        btn1 = menu.add_button('nice', None)
        btn2 = menu.add_button('nice', None)
        self.assertTrue(btn1.selected)
        btn2.hide()
        menu.select_widget(btn1)

        # btn2 cannot be selected as it is hidden
        self.assertRaises(ValueError, lambda: menu.select_widget(btn2))
        btn2.show()
        menu.select_widget(btn2)

        # Hide buttons
        btn1.hide()
        btn2.hide()

        self.assertFalse(btn1.selected)
        self.assertFalse(btn2.selected)

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
        btn = menu.add_button('button', None)
        self.assertTrue(btn.selected)
        btn.hide()

        # As theres no more visible widgets, index must be -1
        self.assertEqual(menu._index, -1)
        self.assertFalse(btn.selected)
        btn.show()

        # Widget should be selected, and index must be 0
        self.assertTrue(btn.selected)
        self.assertEqual(menu._index, 0)

        # Hide button, and set is as unselectable
        btn.hide()
        btn.is_selectable = False
        self.assertEqual(menu._index, -1)
        btn.show()

        # Now, as widget is not selectable, button should not
        # be selected and index still -1
        self.assertFalse(btn.selected)
        self.assertEqual(menu._index, -1)

        # Set selectable again
        btn.is_selectable = True
        btn.select()
        self.assertEqual(menu._index, -1)  # Menu still don't considers widget as selected
        self.assertEqual(menu.get_selected_widget(), None)
        btn.select(update_menu=True)
        self.assertEqual(menu.get_selected_widget(), btn)
