"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST MENU
Menu object tests.
"""

__all__ = ['MenuTest']

from test._utils import BaseTest, surface, MenuUtils, PygameEventUtils, \
    TEST_THEME, PYGAME_V2, WIDGET_MOUSEOVER, WIDGET_TOP_CURSOR, reset_widgets_over, \
    THEME_NON_FIXED_TITLE
import copy
import math
import sys
import time
import timeit

import pygame
import pygame_menu
import pygame_menu.controls as ctrl

from pygame_menu import events
# noinspection PyProtectedMember
from pygame_menu._types import Any, Tuple, List
from pygame_menu.locals import FINGERDOWN, FINGERMOTION
from pygame_menu.utils import set_pygame_cursor, get_cursor
from pygame_menu.widgets import Label, Button

# Configure the tests
TEST_TIME_DRAW = False


def dummy_function() -> None:
    """
    Dummy function, this can be achieved with lambda, but it's against
    PEP-8.
    """
    return


class MenuTest(BaseTest):

    def test_mainloop_disabled(self) -> None:
        """
        Test disabled mainloop.
        """
        menu = MenuUtils.generic_menu(title='mainmenu')
        menu.disable()
        self.assertRaises(RuntimeError, lambda: menu.mainloop(surface, bgfun=dummy_function, disable_loop=True))
        menu.enable()

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
            btn_deco = btn.get_decorator()
            if add_decorator:
                for j in range(10):
                    btn_deco.add_pixel(j * 10, j * 20, (10, 10, 150))
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
        self.assertRaises(ValueError, lambda: MenuUtils.generic_menu(width=300, height=1))

    # noinspection SpellCheckingInspection
    def test_position(self) -> None:
        """
        Test position.
        """
        # Test centering
        theme_src = TEST_THEME.copy()

        menu = MenuUtils.generic_menu(theme=theme_src)
        btn = menu.add.button('button')
        menu.center_content()
        self.assertEqual(menu.get_height(), 400)
        self.assertEqual(menu.get_height(inner=True), 345)
        self.assertEqual(menu.get_menubar().get_height(), 55)

        h = 41 if PYGAME_V2 else 42
        self.assertEqual(btn.get_height(), h)
        self.assertEqual(btn.get_size()[1], h)
        self.assertEqual(menu.get_height(widget=True), h)

        v_pos = int((345 - h) / 2)  # available_height - widget_height
        self.assertEqual(menu._widget_offset[1], v_pos)
        self.assertEqual(btn.get_position()[1], v_pos + 1)

        # If there's too many widgets, the centering should be disabled
        for i in range(20):
            menu.add.button('button')
        self.assertEqual(menu._widget_offset[1], 0)

        theme = menu.get_theme()

        # Anyway, as the widget is 0, the first button position should be the height of its selection effect
        btneff = btn.get_selection_effect().get_margin()[0]
        self.assertEqual(btn.get_position()[1], btneff + 1)

        self.assertEqual(h * 21 + theme.widget_margin[1] * 20, menu.get_height(widget=True))

        # Test menu not centered
        menu = MenuUtils.generic_menu(center_content=False, theme=theme_src)
        btn = menu.add.button('button')
        btneff = btn.get_selection_effect().get_margin()[0]
        self.assertEqual(btn.get_position()[1], btneff + 1)

        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(position_x=-1, position_y=0))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(position_x=0, position_y=-1))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(position_x=-1, position_y=-1))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(position_x=101, position_y=0))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(position_x=99, position_y=101))
        menu = MenuUtils.generic_menu(position_x=0, position_y=0)
        menu.set_relative_position(20, 40)

        theme = theme_src.copy()
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
        hidden = menu.add.button('Hidden', font_size=100)
        hidden.hide()
        quit2 = menu.add.button('Quit', pygame_menu.events.EXIT)
        label = menu.add.label('This label is really epic')
        label.rotate(90)
        menu.render()

        self.assertEqual(quit1.get_position(), (170, 5))
        self.assertEqual(name1.get_position(), (115, 73))
        self.assertEqual(sel1.get_position(), (104, 141))
        self.assertEqual(sel2.get_position(), (104, 179))
        self.assertEqual(play1.get_position(), (388, 5))
        self.assertEqual(play2.get_position(), (698, 5))
        self.assertEqual(hidden.get_position(), (0, 0))
        self.assertEqual(quit2.get_position(), (550, 43))
        self.assertEqual(label.get_position(), (556, 81))

        # Test no selectable position
        menu = MenuUtils.generic_menu(center_content=False, theme=theme_src)
        btn = menu.add.button('button')
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
        btn = menu.add.button('Nice')
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
        b1 = menu.add.button('b1')
        b2 = menu.add.button('b2').set_float()
        b3 = menu.add.button('b3')
        b4 = menu.add.button('b4')
        b5 = menu.add.button('b5').set_float()
        b6 = menu.add.button('b6').set_float()
        b7 = menu.add.button('b37')
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

        # Test position relative/absolute
        menu.set_relative_position(50, 50)
        self.assertEqual(menu._position, (0, 100))
        menu.set_absolute_position(50, 50)
        self.assertEqual(menu._position, (50, 50))

        # Test absolute position constructor
        menu = pygame_menu.Menu('', 200, 300, position=(50, 50))
        self.assertEqual(menu._position, (200, 150))
        menu = pygame_menu.Menu('', 200, 300, position=(50, 50, True))
        self.assertEqual(menu._position, (200, 150))
        menu = pygame_menu.Menu('', 200, 300, position=(50, 50, False))
        self.assertEqual(menu._position, (50, 50))

    def test_float_position(self) -> None:
        """
        Tests float position.
        """
        menu = MenuUtils.generic_menu(center_content=False)

        a = menu.add.label('nice')
        a.set_float()
        b = menu.add.label('nice')
        b.set_float()
        self.assertEqual(a.get_position(), b.get_position())

        z = menu.add.label('nice', float=True)
        self.assertEqual(a.get_position(), z.get_position())

        # Now add a frame
        f = menu.add.frame_v(1000, 1000)
        f.set_float()
        self.assertEqual(a.get_position()[1], f.get_position()[1])
        c = menu.add.label('nice')
        c.set_float()
        self.assertEqual(a.get_position(), c.get_position())
        self.assertEqual(c.get_position()[1], f.get_position()[1])
        labels = [menu.add.label(f'Lorem ipsum #{i}', font_size=15, font_color='#000', padding=0) for i in range(20)]
        for j in labels:
            f.pack(j)
        d = menu.add.label('nice')
        d.set_float()
        self.assertEqual(a.get_position(), d.get_position())
        self.assertEqual(len(menu.get_widgets()), 26)

    def test_translate(self) -> None:
        """
        Test menu translation.
        """
        menu = MenuUtils.generic_menu(width=400, theme=THEME_NON_FIXED_TITLE)
        btn = menu.add.button('button')
        self.assertEqual(menu.get_menubar().get_height(), 55)
        self.assertEqual(menu.get_position(), (100, 100))
        self.assertEqual(menu.get_scrollarea().get_position(), (100, 100 + 55))
        self.assertEqual(menu.get_menubar().get_position(), (100, 100))
        self.assertEqual(btn.get_position(), (153, 153 if PYGAME_V2 else 152))  # Position is respective the menu
        self.assertEqual(btn.get_position(to_real_position=True), (253, 308 if PYGAME_V2 else 307))
        self.assertEqual(btn.get_position(to_absolute_position=True), (153, 153 if PYGAME_V2 else 152))
        self.assertEqual(menu.get_translate(), (0, 0))

        # Translate by 0,100
        menu.translate(0, 100)
        self.assertEqual(menu.get_position(), (100, 200))
        self.assertEqual(menu.get_scrollarea().get_position(), (100, 200 + 55))
        self.assertEqual(menu.get_menubar().get_position(), (100, 200))
        self.assertEqual(btn.get_position(), (153, 153 if PYGAME_V2 else 152))  # Position is respective the menu
        self.assertEqual(btn.get_position(to_real_position=True), (253, 408 if PYGAME_V2 else 407))
        self.assertEqual(btn.get_position(to_absolute_position=True), (153, 153 if PYGAME_V2 else 152))
        self.assertEqual(menu.get_translate(), (0, 100))

    # noinspection SpellCheckingInspection
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
        self.assertFalse(menu2.close())  # None status don't change enabled
        self.assertTrue(menu2.is_enabled())
        menu2.set_onclose(pygame_menu.events.NONE)
        self.assertFalse(menu2.close())  # NONE event don't change enabled
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
        # the output should be the same, except it doesn't close

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

        # Close if not enabled
        menu.disable()
        self.assertRaises(RuntimeError, lambda: menu.close())

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
        menu = MenuUtils.generic_menu(title='mainmenu')
        self.assertEqual(menu._get_depth(), 0)

        # Adds some menus
        menu_prev = menu
        menu_ = None
        for i in range(1, 11):
            menu_ = MenuUtils.generic_menu(title=f'submenu {i}')
            button = menu_prev.add.button('open', menu_)
            button.apply()
            menu_prev = menu_
        menu.enable()
        menu.draw(surface)

        self.assertNotEqual(menu.get_current().get_id(), menu.get_id())
        self.assertNotEqual(menu, menu_)
        self.assertEqual(menu_._get_depth(), 10)
        self.assertEqual(menu._get_depth(), 10)

        """
        menu when it was opened it changed to submenu 1, when submenu 1 was opened
        it changed to submenu 2, and so on...
        """
        self.assertEqual(menu.get_title(), 'mainmenu')
        self.assertEqual(menu.get_current().get_title(), 'submenu 10')
        self.assertEqual(menu_.get_current().get_title(), 'submenu 10')

        """
        Submenu 10 has not changed to any, so back will not affect it,
        but mainmenu will reset 1 unit
        """
        menu_._back()
        self.assertEqual(menu_.get_title(), 'submenu 10')

        """
        Mainmenu has changed, go back changes from submenu 10 to 9
        """
        self.assertEqual(menu._get_depth(), 9)
        menu._back()
        self.assertEqual(menu._get_depth(), 8)
        self.assertEqual(menu.get_title(), 'mainmenu')
        self.assertEqual(menu.get_current().get_title(), 'submenu 8')

        """
        Full go back (reset)
        """
        menu.full_reset()
        self.assertEqual(menu._get_depth(), 0)
        self.assertEqual(menu.get_current().get_title(), 'mainmenu')

    # noinspection PyArgumentEqualDefault
    def test_get_widget(self) -> None:
        """
        Test get widget.
        """
        menu = MenuUtils.generic_menu(title='mainmenu')

        widget = menu.add.text_input('test', textinput_id='some_id')
        widget_found = menu.get_widget('some_id')
        self.assertEqual(widget, widget_found)

        # Add a widget to a deepest menu
        prev_menu = menu
        for i in range(11):
            menu_ = MenuUtils.generic_menu()
            prev_menu.add.button('menu', menu_)
            prev_menu = menu_

        # Add a deep input
        deep_widget = prev_menu.add.text_input('title', textinput_id='deep_id')
        deep_selector = prev_menu.add.selector('selector', [('0', 0), ('1', 1)], selector_id='deep_selector', default=1)

        self.assertIsNone(menu.get_widget('deep_id', recursive=False))
        self.assertEqual(menu.get_widget('deep_id', recursive=True), deep_widget)
        self.assertEqual(menu.get_widget('deep_selector', recursive=True), deep_selector)

    def test_add_generic_widget(self) -> None:
        """
        Test generic widget.
        """
        menu = MenuUtils.generic_menu()
        btn = menu.add.button('nice')
        w = Button('title')
        menu.add.generic_widget(w)
        self.assertRaises(ValueError, lambda: menu.add.generic_widget(w))
        btn._menu = None
        self.assertRaises(IndexError, lambda: menu.add.generic_widget(btn))
        btn._menu = menu
        menu.remove_widget(btn)
        self.assertIsNone(btn._menu)
        menu.add.generic_widget(btn)
        self.assertIn(btn, menu.get_widgets())

    # noinspection PyArgumentEqualDefault
    def test_get_selected_widget(self) -> None:
        """
        Tests get current widget.
        """
        menu = MenuUtils.generic_menu(title='mainmenu')

        # Test widget selection and removal
        widget = menu.add.text_input('test', default='some_id')
        self.assertEqual(widget, menu.get_selected_widget())
        menu.remove_widget(widget)
        self.assertIsNone(menu.get_selected_widget())
        self.assertEqual(menu.get_index(), -1)

        # Add two widgets, first widget will be selected first, but if removed the second should be selected
        widget1 = menu.add.text_input('test', default='some_id', textinput_id='epic')
        self.assertRaises(IndexError, lambda: menu.add.text_input('test', default='some_id', textinput_id='epic'))
        widget2 = menu.add.text_input('test', default='some_id')
        self.assertEqual(widget1.get_menu(), menu)
        self.assertEqual(widget1, menu.get_selected_widget())
        menu.remove_widget(widget1)
        self.assertIsNone(widget1.get_menu())
        self.assertEqual(widget2, menu.get_selected_widget())
        menu.remove_widget(widget2)
        self.assertIsNone(widget2.get_menu())
        self.assertEqual(len(menu.get_widgets()), 0)

        # Add 3 widgets, select the last one and remove it, then the selected widget must be the first
        w1 = menu.add.button('1')
        w2 = Label('2')
        menu.add.generic_widget(w2, configure_defaults=True)
        w3 = menu.add.button('3')
        self.assertEqual(menu.get_selected_widget(), w1)
        menu.select_widget(w3)
        self.assertEqual(menu.get_selected_widget(), w3)
        menu.remove_widget(w3)
        # 3 was deleted, so 1 should be selected
        self.assertEqual(menu.get_selected_widget(), w1)

        # Hides w1, then w2 should be selected
        w1.hide()
        self.assertEqual(menu.get_selected_widget(), w2)

        # Un-hide w1, w2 should be keep selected
        w1.show()
        self.assertEqual(menu.get_selected_widget(), w2)

        # Mark w1 as unselectable and remove w2, then no widget should be selected
        w1.is_selectable = False
        menu.remove_widget(w2)
        self.assertIsNone(menu.get_selected_widget())
        self.assertRaises(ValueError, lambda: menu.select_widget(w1))

        # Mark w1 as selectable
        w1.is_selectable = True
        menu.add.generic_widget(w2)
        self.assertEqual(menu.get_selected_widget(), w2)

        # Add a new widget that cannot be selected
        menu.add.label('not selectable')
        menu.add.label('not selectable')
        w_last = menu.add.label('not selectable', selectable=True)

        # If w2 is removed, then menu will try to select labels, but as them are not selectable it should select the last one
        w2.hide()
        self.assertEqual(menu.get_selected_widget(), w_last)

        # Mark w1 as unselectable, then w1 is not selectable, nor w2, and labels are unselectable too
        # so the selected should be the same
        w1.is_selectable = False
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
        self.assertEqual(menu.get_selected_widget(), w_last)

        # Show w2, then if DOWN is pressed again, the selected status should be 2
        w2.show()
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
        self.assertEqual(menu.get_selected_widget(), w2)

        # Hide w2, pass again to w_last
        w2.hide()
        self.assertEqual(menu.get_selected_widget(), w_last)

        # Hide w_last, then nothing is selected
        w_last.hide()
        self.assertIsNone(menu.get_selected_widget())

        # Un-hide w2, then it should be selected
        w2.show()
        self.assertEqual(menu.get_selected_widget(), w2)

        # Remove w2, then nothing should be selected
        menu.remove_widget(w2)
        self.assertIsNone(menu.get_selected_widget())

        # Clear all widgets and get index
        menu._widgets = []
        self._index = 100
        self.assertIsNone(menu.get_selected_widget())

        # Destroy index
        menu._index = '0'
        self.assertIsNone(menu.get_selected_widget())
        self.assertEqual(menu._index, 0)

        # Add new index
        btn = menu.add.button('epic')
        self.assertEqual(menu.get_selected_widget(), btn)
        menu.unselect_widget()
        self.assertIsNone(menu.get_selected_widget())

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
        self.assertIn(menu2, menu.get_submenus())
        self.assertNotIn(menu, menu2.get_submenus())

        # Remove menu2 from menu
        btn.update_callback(lambda: None)
        self.assertFalse(btn.to_menu)
        self.assertFalse(menu.in_submenu(menu2))

        # Test recursive
        menu.clear()
        menu2.clear()

        self.assertRaises(ValueError, lambda: menu.add.button('to self', menu))
        menu.add.button('to2', menu2)
        self.assertRaises(ValueError, lambda: menu2.add.button('to1', menu))

        # Test duplicated submenu
        menu_d = MenuUtils.generic_menu()
        b1 = menu_d.add.button('btn', menu, button_id='1')
        b2 = menu_d.add.button('btn2', menu, button_id='2')

        self.assertEqual(b1._menu_hook, menu)
        self.assertEqual(b2._menu_hook, menu)

        self.assertIn(b1, menu_d._submenus[menu])
        self.assertIn(b2, menu_d._submenus[menu])

        menu_d.remove_widget('1')
        self.assertNotIn(b1, menu_d._submenus[menu])
        self.assertIn(b2, menu_d._submenus[menu])
        menu_d.remove_widget('2')

        self.assertEqual(menu_d._submenus, {})

        # Clear menu
        menu.clear()
        self.assertIsNone(btn._menu)

        # Add more submenus
        menu3 = MenuUtils.generic_menu()
        ba = menu.add.button('btn12A', menu2)
        bb = menu.add.button('btn12B', menu2)
        bc = menu.add.button('btn12C', menu2)
        b23 = menu2.add.button('btn23', menu3)

        menu._test_print_widgets()
        self.assertEqual(menu.get_submenus(), (menu2,))
        self.assertEqual(menu.get_submenus(recursive=True), (menu2, menu3))
        self.assertEqual(menu._submenus[menu2], [ba, bb, bc])

        # Remove links upon submenu disappears
        menu.remove_widget(bb)
        self.assertEqual(menu.get_submenus(), (menu2,))
        self.assertEqual(menu._submenus[menu2], [ba, bc])
        menu.remove_widget(ba)
        self.assertEqual(menu.get_submenus(), (menu2,))
        self.assertEqual(menu._submenus[menu2], [bc])
        menu.remove_widget(bc)
        self.assertEqual(menu.get_submenus(), ())
        self.assertEqual(menu.get_submenus(recursive=True), ())
        self.assertEqual(menu._submenus, {})

        self.assertEqual(b23._menu, menu2)
        menu2.clear()
        self.assertIsNone(b23._menu)

        # Test circular
        menu.add.button('12', menu2)
        menu2.add.button('23', menu3)
        self.assertRaises(ValueError, lambda: menu3.add.button('31', menu))
        self.assertRaises(ValueError, lambda: menu3.add.button('31', menu2))

        # Test update action
        menu.clear()
        menu2.clear()

        b12 = menu.add.button('btn12', menu2)
        b23 = menu2.add.button('btn23', menu3)
        self.assertEqual(menu.get_submenus(), (menu2,))
        self.assertEqual(menu.get_submenus(recursive=True), (menu2, menu3))
        self.assertEqual(menu._submenus, {menu2: [b12]})
        self.assertEqual(menu2._submenus, {menu3: [b23]})

        b12.update_callback(lambda: print('epic'))
        self.assertEqual(menu.get_submenus(), ())
        self.assertEqual(menu.get_submenus(recursive=True), ())
        self.assertEqual(menu._submenus, {})
        self.assertEqual(menu2._submenus, {menu3: [b23]})

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
            title='Images',
            width=400
        )

        menu.add.label('Text #1')
        menu.add.vertical_margin(100)
        menu.add.label('Text #2')
        self.assertEqual(menu._widget_offset[1], 33 if PYGAME_V2 else 32)

    def test_getters(self) -> None:
        """
        Test other getters.
        """
        menu = MenuUtils.generic_menu(title='mainmenu')
        self.assertIsNotNone(menu.get_menubar())
        self.assertIsNotNone(menu.get_scrollarea())

        w, h = menu.get_size()
        self.assertEqual(int(w), 600)
        self.assertEqual(int(h), 400)

        w, h = menu.get_window_size()
        self.assertEqual(int(w), 600)
        self.assertEqual(int(h), 600)

    def test_generic_events(self) -> None:
        """
        Test key events.
        """
        menu = MenuUtils.generic_menu(title='mainmenu')

        # Add a menu and a method that set a function
        event_val = [False]

        def _some_event() -> str:
            event_val[0] = True
            return 'the value'

        # Add some widgets
        button = None
        wid = []
        for i in range(5):
            button = menu.add.button('button', _some_event)
            wid.append(button.get_id())
        self.assertEqual(len(menu.get_widgets()), 5)
        self.assertEqual(len(menu.get_widgets(wid)), 5)

        # Create an event in pygame
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
        self.assertEqual(menu.get_index(), 1)

        # Move down twice
        for i in range(2):
            menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
        self.assertEqual(menu.get_index(), 4)
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
        self.assertEqual(menu.get_index(), 0)

        # Press enter, button should trigger and call function
        self.assertEqual(button.apply(), 'the value')
        menu.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))

        # Other
        menu.update(PygameEventUtils.key(ctrl.KEY_CLOSE_MENU, keydown=True))
        menu.update(PygameEventUtils.key(ctrl.KEY_BACK, keydown=True))

        # Check index is the same as before
        self.assertEqual(menu.get_index(), 0)

        # Check joy
        menu.update(PygameEventUtils.joy_hat_motion(ctrl.JOY_UP))
        self.assertEqual(menu.get_index(), 4)
        menu.update(PygameEventUtils.joy_hat_motion(ctrl.JOY_DOWN))
        self.assertEqual(menu.get_index(), 0)
        menu.update(PygameEventUtils.joy_motion(1, 1))
        self.assertEqual(menu.get_index(), 1)
        menu.update(PygameEventUtils.joy_motion(1, -1))
        self.assertEqual(menu.get_index(), 0)
        menu.update(PygameEventUtils.joy_motion(1, -1))
        self.assertEqual(menu.get_index(), 4)

        click_pos = button.get_rect(to_real_position=True).center
        menu.update(PygameEventUtils.mouse_click(click_pos[0], click_pos[1]))
        self.assertTrue(event_val[0])
        event_val[0] = False

    def test_back_event(self) -> None:
        """
        Test back event.
        """
        menu = MenuUtils.generic_menu(title='mainmenu')
        self.assertEqual(menu._get_depth(), 0)
        menu_ = MenuUtils.generic_menu(title='submenu')
        button = menu.add.button('open', menu_)
        button.apply()
        self.assertEqual(menu._get_depth(), 1)
        menu.update(PygameEventUtils.key(ctrl.KEY_BACK, keydown=True))  # go back
        self.assertEqual(menu._get_depth(), 0)

    def test_mouse_empty_submenu(self) -> None:
        """
        Test mouse event where the following submenu has fewer elements.
        """
        menu = MenuUtils.generic_menu(title='mainmenu')
        menu.enable()

        submenu = MenuUtils.generic_menu()  # 1 option
        submenu.add.button('button', lambda: None)

        menu.add.button('button', lambda: None)
        menu.add.button('button', lambda: None)
        button = menu.add.button('button', submenu)
        menu.disable()
        self.assertRaises(RuntimeError, lambda: menu.draw(surface))
        menu.enable()
        menu.draw(surface)

        click_pos = button.get_rect(to_real_position=True).center
        menu.update(PygameEventUtils.mouse_click(click_pos[0], click_pos[1]))

    # noinspection SpellCheckingInspection
    def test_input_data(self) -> None:
        """
        Test input data gathering.
        """
        menu = MenuUtils.generic_menu(title='mainmenu')

        menu.add.text_input('text1', textinput_id='id1', default=1)
        data = menu.get_input_data(True)
        self.assertEqual(data['id1'], '1')

        menu.add.text_input('text1', textinput_id='id2', default=1.5, input_type=pygame_menu.locals.INPUT_INT)
        data = menu.get_input_data(True)
        self.assertEqual(data['id2'], 1)  # Cast to int
        self.assertRaises(IndexError, lambda: menu.add.text_input('text1', textinput_id='id1', default=1))

        menu.add.text_input('text1', textinput_id='id3', default=1.5, input_type=pygame_menu.locals.INPUT_FLOAT)
        data = menu.get_input_data(True)
        self.assertEqual(data['id3'], 1.5)  # Correct

        # Add input to a submenu
        submenu = MenuUtils.generic_menu()
        submenu.add.text_input('text', textinput_id='id4', default='thewidget')
        menu.add.button('submenu', submenu)
        data = menu.get_input_data(recursive=True)
        self.assertEqual(data['id4'], 'thewidget')

        # Add a submenu within submenu with a repeated id, menu.get_input_data
        # should raise an exception
        subsubmenu = MenuUtils.generic_menu()
        subsubmenu.add.text_input('text', textinput_id='id4', default='repeateddata')
        submenu.add.button('submenu', subsubmenu)
        self.assertRaises(ValueError, lambda: menu.get_input_data(recursive=True))

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

        # Check move if empty
        self.assertFalse(column_menu._right())
        self.assertFalse(column_menu._left())

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
        self.assertRaises(pygame_menu.menu._MenuWidgetOverflow, lambda: column_menu.add.button('test', pygame_menu.events.BACK))
        column_menu._update_widget_position()
        self.assertEqual(len(column_menu._widgets), 8)  # Widget not added

        # Test max width
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(columns=3, rows=4, column_max_width=[500, 500, 500, 500]))
        column_menu = MenuUtils.generic_menu(columns=3, rows=4, column_max_width=0)  # max menu width
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(columns=3, rows=4, column_max_width=-1))
        column_menu = MenuUtils.generic_menu(columns=3, rows=4, column_max_width=500)  # max menu width
        self.assertEqual(len(column_menu._column_max_width), 3)
        for i in range(3):
            self.assertEqual(column_menu._column_max_width[i], 500)

        # Test min width
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(columns=3, rows=4, column_min_width=[500, 500, 500, 500]))
        column_menu = MenuUtils.generic_menu(columns=3, rows=4, column_min_width=100)  # max menu width
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(columns=3, rows=4, column_min_width=-100))
        column_menu = MenuUtils.generic_menu(columns=3, rows=4, column_min_width=500)  # max menu width
        self.assertEqual(len(column_menu._column_min_width), 3)
        for i in range(3):
            self.assertEqual(column_menu._column_min_width[i], 500)
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(columns=3, rows=4, column_min_width=None))

        # Test max width should be greater than min width
        self.assertRaises(AssertionError,
                          lambda: MenuUtils.generic_menu(columns=2, rows=4, column_min_width=[500, 500],
                                                         column_max_width=[100, 500]))
        self.assertRaises(AssertionError,
                          lambda: MenuUtils.generic_menu(columns=2, rows=4, column_min_width=[500, 500],
                                                         column_max_width=[500, 100]))
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(rows=4, column_min_width=10, column_max_width=1))

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
        btn1 = menu.add.button('btn')
        btn2 = menu.add.button('btn')
        btn3 = menu.add.button('btn')
        btn4 = menu.add.button('btn')
        btn5 = menu.add.button('btn')
        btn6 = menu.add.button('btn')
        self.assertEqual(btn1.get_col_row_index(), (0, 0, 0))
        self.assertEqual(btn2.get_col_row_index(), (0, 1, 1))
        self.assertEqual(btn3.get_col_row_index(), (1, 0, 2))
        self.assertEqual(btn4.get_col_row_index(), (1, 1, 3))
        self.assertEqual(btn5.get_col_row_index(), (2, 0, 4))
        self.assertEqual(btn6.get_col_row_index(), (2, 1, 5))

        # Check size
        self.assertEqual(len(menu._column_widths), 3)
        for col_w in menu._column_widths:
            self.assertEqual(col_w, width / 3)

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
        for col_w in menu._column_widths:
            self.assertEqual(col_w, width / 2)  # 600/2

        # Add a new button
        btn7 = menu.add.button('btn')

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

        self.assertEqual(btn3.get_width(apply_selection=True), 63)
        for col_w in menu._column_widths:
            self.assertEqual(col_w, width / 2)

        # Scale 4, this should not change menu column widths
        btn4.scale(5, 5)
        menu.render()
        for col_w in menu._column_widths:
            self.assertEqual(col_w, width / 2)

        # Scale 3, this should change menu column widths
        btn3.scale(5, 1)
        btn3_sz = btn3.get_width(apply_selection=True)
        btn6_sz = btn6.get_width(apply_selection=True)
        menu.render()
        col_width1 = (width * btn3_sz) / (btn3_sz + btn6_sz)
        col_width2 = width - col_width1
        self.assertAlmostEqual(menu._column_widths[0], math.ceil(col_width1))
        self.assertAlmostEqual(menu._column_widths[1], math.ceil(col_width2))

        # Test different rows per column
        menu = MenuUtils.generic_menu(columns=3, rows=[2, 1, 2], width=width, column_max_width=[300, None, 100])
        btn1 = menu.add.button('btn')
        btn2 = menu.add.button('btn')
        btn3 = menu.add.button('btn')
        btn4 = menu.add.button('btn')
        btn5 = menu.add.button('btn')
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
        self.assertEqual(menu._column_widths, [300, 63, 238])
        self.assertEqual(menu._column_pos_x, [150, 331, 482])

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
        btn1 = menu.add.button('btn')
        menu.add.button('btn')
        menu.add.button('btn')
        menu.add.button('btn')
        menu.add.button('btn')
        btn1.resize(200, 10)
        menu.render()  # This should scale 2 column
        self.assertEqual(menu._column_widths, [200, 250, 150])

        menu = MenuUtils.generic_menu(columns=3, rows=[2, 1, 2], width=width,
                                      column_max_width=[200, 150, 150], column_min_width=[150, 150, 150])
        btn1 = menu.add.button('btn')
        btn2 = menu.add.button('btn')
        btn3 = menu.add.button('btn')
        menu.add.button('btn')
        menu.add.button('btn')
        btn1.resize(200, 10)
        btn2.resize(150, 1)
        btn3.resize(150, 1)
        menu.render()
        self.assertEqual(menu._column_widths, [200, 150, 150])

        menu = MenuUtils.generic_menu()
        self.assertEqual(menu.get_col_rows(), (1, [10000000]))

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
        self.assertEqual(menu.get_window_size(), (888, 999))

    def test_touchscreen(self) -> None:
        """
        Test menu touchscreen behaviour.
        """
        self.assertRaises(AssertionError, lambda: MenuUtils.generic_menu(title='mainmenu', touchscreen=False, touchscreen_motion_selection=True, ))
        menu = MenuUtils.generic_menu(title='mainmenu', touchscreen=True, enabled=False, mouse_visible=False)
        self.assertRaises(RuntimeError, lambda: menu.mainloop(surface, bgfun=dummy_function))

        # Add a menu and a method that set a function
        event_val = [False]

        def _some_event() -> str:
            event_val[0] = True
            return 'the value'

        # Add some widgets
        button = menu.add.button('button', _some_event)

        if hasattr(pygame, 'FINGERUP'):
            click_pos = button.get_rect(to_real_position=True).center
            menu.enable()
            # Event must be normalized
            menu.update(PygameEventUtils.touch_click(click_pos[0], click_pos[1], normalize=False))
            self.assertFalse(event_val[0])

            menu.update(PygameEventUtils.touch_click(click_pos[0], click_pos[1], menu=menu))
            self.assertTrue(event_val[0])
            event_val[0] = False
            self.assertEqual(menu.get_selected_widget().get_id(), button.get_id())
            btn = menu.get_selected_widget()
            self.assertGreaterEqual(btn.get_selected_time(), 0)

    def test_remove_widget(self) -> None:
        """
        Test widget remove.
        """
        menu = MenuUtils.generic_menu()
        f = menu.add.frame_h(100, 200)
        menu._update_frames.append(f)
        btn = menu.add.button('epic')
        menu._update_widgets.append(btn)

        menu.remove_widget(f)
        self.assertNotIn(f, menu._update_frames)

        menu.remove_widget(btn)
        self.assertNotIn(btn, menu._update_widgets)

    # noinspection SpellCheckingInspection
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

        # test wait for events
        test = [False, 0]

        def bgfun() -> None:
            """
            Function executed on each mainloop iteration for testing
            waiting for events.
            """
            test[0] = not test[0]
            test[1] += 1
            pygame.event.post(PygameEventUtils.joy_center(inlist=False))

        menu = MenuUtils.generic_menu()
        menu.set_onupdate(menu.disable)
        menu.enable()
        menu.mainloop(surface, bgfun, wait_for_event=True)

        # Test mainloop for a number of frames
        test = [0]
        menu = MenuUtils.generic_menu()

        def bgfun() -> None:
            """
            Checks the number of frames.
            """
            test[0] += 1
            if test[0] == 20:
                self.assertEqual(test[0], menu._stats.loop)
                menu.disable()

        menu.mainloop(surface, bgfun)

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
        menubar = menu.get_menubar()

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
        btn = menu.add.button('hidden')
        btn.hide()
        self.assertEqual(menu.get_height(widget=True), 0)
        menu._runtime_errors.throw(False, 'error')

    # noinspection SpellCheckingInspection
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

        # Test select widget
        def onbeforeopen_select_widget(_from: 'pygame_menu.Menu', _to: 'pygame_menu.Menu'):
            """
            Selects widget before opening.
            """
            _to.select_widget('option2')

        menu = MenuUtils.generic_menu()
        submenu = MenuUtils.generic_menu()
        submenu.add.button('Option 1', button_id='option1')
        submenu.add.button('Option 2', button_id='option2')
        submenu.add.button('Option 3', button_id='option3')
        submenu.set_onbeforeopen(onbeforeopen_select_widget)
        btn_submenu = menu.add.button('Submenu', submenu)

        # Test applying to submenu, which should trigger onbeforeopen
        self.assertEqual(submenu.get_selected_widget().get_id(), 'option1')  # By default, submenu always start as 0
        btn_submenu.apply()
        self.assertEqual(submenu.get_selected_widget().get_id(), 'option2')  # Test if onbeforeopen did its work

    def test_focus(self) -> None:
        """
        Test menu focus effect.
        """
        menu = MenuUtils.generic_menu(title='menu', mouse_motion_selection=True)
        btn = menu.add.button('nice')

        # Test focus
        btn.active = True
        focus = menu._draw_focus_widget(surface, btn)
        self.assertEqual(len(focus), 4)
        if not PYGAME_V2:
            self.assertEqual(focus[1], ((0, 0), (600, 0), (600, 302), (0, 302)))
            self.assertEqual(focus[2], ((0, 303), (262, 303), (262, 352), (0, 352)))
            self.assertEqual(focus[3], ((336, 303), (600, 303), (600, 352), (336, 352)))
            self.assertEqual(focus[4], ((0, 353), (600, 353), (600, 600), (0, 600)))

        else:
            self.assertEqual(focus[1], ((0, 0), (600, 0), (600, 303), (0, 303)))
            self.assertEqual(focus[2], ((0, 304), (262, 304), (262, 352), (0, 352)))
            self.assertEqual(focus[3], ((336, 304), (600, 304), (600, 352), (336, 352)))
            self.assertEqual(focus[4], ((0, 353), (600, 353), (600, 600), (0, 600)))

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
        btn1 = menu.add.button('nice')
        btn2 = menu.add.button('nice')
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

        self.assertEqual(btn1.get_col_row_index(), (-1, -1, 0))
        self.assertEqual(btn2.get_col_row_index(), (-1, -1, 1))

        menu.remove_widget(btn1)
        self.assertEqual(btn1.get_col_row_index(), (-1, -1, -1))
        self.assertEqual(btn2.get_col_row_index(), (-1, -1, 0))

        menu.remove_widget(btn2)
        self.assertEqual(btn1.get_col_row_index(), (-1, -1, -1))
        self.assertEqual(btn2.get_col_row_index(), (-1, -1, -1))

        menu = MenuUtils.generic_menu(title='menu')
        btn = menu.add.button('button')
        self.assertTrue(btn.is_selected())
        btn.hide()

        # As there's no more visible widgets, index must be -1
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
        self.assertEqual(menu._index, -1)  # Menu still don't consider widget as selected
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
        if not PYGAME_V2:
            return

        menu_top = MenuUtils.generic_menu()
        menu = MenuUtils.generic_menu(columns=4, rows=2, touchscreen=True,
                                      touchscreen_motion_selection=True, column_min_width=[400, 300, 400, 300],
                                      joystick_enabled=True)  # submenu
        menu_top.add.button('menu', menu).apply()
        wid_g = []
        for i in range(8):
            b = menu.add.button('test' + str(i))
            wid_g.append(b)

        # btn0 | btn2 | btn4 | btn6
        # btn1 | btn3 | btn5 | btn7
        self.assertEqual(menu_top.get_current(), menu)

        # Arrow keys
        self.assertEqual(menu.get_selected_widget(), wid_g[0])
        menu_top.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
        self.assertEqual(menu.get_selected_widget(), wid_g[6])
        menu_top.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
        self.assertEqual(menu.get_selected_widget(), wid_g[7])
        menu_top.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
        self.assertEqual(menu.get_selected_widget(), wid_g[1])
        menu_top.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
        self.assertEqual(menu.get_selected_widget(), wid_g[0])

        # Joy key
        menu_top.update(PygameEventUtils.joy_hat_motion(ctrl.JOY_LEFT))
        self.assertEqual(menu.get_selected_widget(), wid_g[6])
        menu_top.update(PygameEventUtils.joy_hat_motion(ctrl.JOY_DOWN))
        self.assertEqual(menu.get_selected_widget(), wid_g[7])
        menu_top.update(PygameEventUtils.joy_hat_motion(ctrl.JOY_RIGHT))
        self.assertEqual(menu.get_selected_widget(), wid_g[1])
        menu_top.update(PygameEventUtils.joy_hat_motion(ctrl.JOY_UP))
        self.assertEqual(menu.get_selected_widget(), wid_g[0])

        # Joy hat
        menu_top.update(PygameEventUtils.joy_motion(-10, 0))
        self.assertEqual(menu_top.get_current()._joy_event, pygame_menu.menu.JOY_EVENT_LEFT)
        self.assertEqual(menu.get_selected_widget(), wid_g[6])
        menu_top.update(PygameEventUtils.joy_motion(0, 10))
        self.assertEqual(menu_top.get_current()._joy_event, pygame_menu.menu.JOY_EVENT_DOWN)
        self.assertEqual(menu.get_selected_widget(), wid_g[7])
        menu_top.update(PygameEventUtils.joy_motion(10, 0))
        self.assertEqual(menu_top.get_current()._joy_event, pygame_menu.menu.JOY_EVENT_RIGHT)
        self.assertEqual(menu.get_selected_widget(), wid_g[1])
        menu_top.update(PygameEventUtils.joy_motion(0, -10))
        self.assertEqual(menu_top.get_current()._joy_event, pygame_menu.menu.JOY_EVENT_UP)
        self.assertEqual(menu.get_selected_widget(), wid_g[0])

        # Menu should keep a recursive state of joy
        self.assertNotEqual(menu.get_current()._joy_event, 0)
        menu_top.update(PygameEventUtils.joy_center())  # center !!
        self.assertEqual(menu.get_current()._joy_event, 0)

        # Click widget
        menu_top.enable()
        menu_top.update(PygameEventUtils.middle_rect_click(wid_g[1], evtype=pygame.MOUSEBUTTONDOWN))
        self.assertEqual(menu.get_selected_widget(), wid_g[1])
        menu_top.update(PygameEventUtils.middle_rect_click(wid_g[0], evtype=pygame.MOUSEBUTTONDOWN))
        self.assertEqual(menu.get_selected_widget(), wid_g[0])
        menu_top.update(PygameEventUtils.middle_rect_click(wid_g[1], evtype=pygame.MOUSEBUTTONDOWN))
        self.assertEqual(menu.get_selected_widget(), wid_g[1])

        # It should not change the menu selection (button up)
        self.assertTrue(menu_top.update(PygameEventUtils.middle_rect_click(wid_g[1], evtype=pygame.MOUSEBUTTONUP)))
        self.assertEqual(menu.get_selected_widget(), wid_g[1])

        # Applying button up in a non-selected widget must return false
        self.assertFalse(menu.update(PygameEventUtils.middle_rect_click(wid_g[0], evtype=pygame.MOUSEBUTTONUP)))

        # Fingerdown don't change selected widget if _touchscreen_motion_selection is enabled
        self.assertTrue(menu._touchscreen_motion_selection)
        menu.update(PygameEventUtils.middle_rect_click(wid_g[0], evtype=FINGERDOWN))
        # self.assertNotEqual(menu.get_selected_widget(), wid_g[0])

        # If touchscreen motion is disabled, then fingerdown should select the widget
        menu._touchscreen_motion_selection = False
        menu.update(PygameEventUtils.middle_rect_click(wid_g[1], evtype=FINGERDOWN))
        self.assertEqual(menu.get_selected_widget(), wid_g[1])
        menu._touchscreen_motion_selection = True

        # Fingermotion should select widgets as touchscreen is active
        menu.update(PygameEventUtils.middle_rect_click(wid_g[0], evtype=FINGERMOTION))
        self.assertEqual(menu.get_selected_widget(), wid_g[0])

        # Infinite joy
        menu_top.update(PygameEventUtils.joy_motion(0, 10))
        # noinspection PyArgumentList
        menu.update([pygame.event.Event(menu._joy_event_repeat)])
        self.assertNotEqual(menu._joy_event, 0)

        # Now disable joy event, then event repeat should not continue
        menu._joy_event = 0
        # noinspection PyArgumentList
        menu.update([pygame.event.Event(menu._joy_event_repeat)])
        menu_top.update(PygameEventUtils.joy_center())  # center !!
        self.assertEqual(menu.get_current()._joy_event, 0)

        # Active widget, and click outside to disable it (only if motion selection enabled)
        wid_g = menu.get_selected_widget()
        wid_g.active = True

        # Clicking the same rect should not fire the callback
        menu_top.update(PygameEventUtils.middle_rect_click(wid_g, evtype=pygame.MOUSEBUTTONDOWN))
        self.assertTrue(wid_g.active)
        self.assertTrue(wid_g.is_selected())

        wid_g._rect.x += 500
        menu._mouse_motion_selection = True
        menu_top.update(PygameEventUtils.middle_rect_click(wid_g, evtype=pygame.MOUSEBUTTONDOWN))
        self.assertFalse(wid_g.active)
        self.assertIn(pygame_menu.events.MENU_LAST_WIDGET_DISABLE_ACTIVE_STATE, menu_top.get_last_update_mode()[0])

        # Test same effect but with touchbar
        menu._mouse_motion_selection = True
        menu._touchscreen = True
        menu._touchscreen_motion_selection = True
        wid_g.active = True
        menu_top.update(PygameEventUtils.middle_rect_click(wid_g, evtype=pygame.FINGERDOWN))
        self.assertFalse(wid_g.active)
        self.assertIn(pygame_menu.events.MENU_LAST_WIDGET_DISABLE_ACTIVE_STATE, menu_top.get_last_update_mode()[0])

        # Test mouseover and mouseleave
        test: Any = [None]

        def on_over(m: 'pygame_menu.Menu', e: 'pygame.event.Event') -> None:
            """
            Mouse over menu.
            """
            self.assertIsInstance(m, pygame_menu.Menu)
            self.assertEqual(e.type, pygame.MOUSEMOTION)
            test[0] = True

        def on_leave(m: 'pygame_menu.Menu', e: 'pygame.event.Event') -> None:
            """
            Mouse leave menu.
            """
            self.assertIsInstance(m, pygame_menu.Menu)
            self.assertEqual(e.type, pygame.MOUSEMOTION)
            test[0] = False

        menu = MenuUtils.generic_menu(width=100, height=100)

        menu.set_onmouseover(on_over)
        menu.set_onmouseleave(on_leave)

        self.assertIsNone(test[0])
        ev = PygameEventUtils.mouse_click(50, 50, inlist=True, evtype=pygame.MOUSEMOTION)
        self.assertFalse(menu._mouseover)
        menu.update(ev)
        self.assertFalse(test[0])

        rect = menu.get_rect()
        ev = PygameEventUtils.mouse_click(rect.centerx, rect.centery, inlist=True, evtype=pygame.MOUSEMOTION)
        menu.update(ev)
        self.assertTrue(test[0])
        self.assertTrue(menu._mouseover)

        ev = PygameEventUtils.mouse_click(50, 50, inlist=True, evtype=pygame.MOUSEMOTION)
        menu.update(ev)
        self.assertFalse(menu._mouseover)
        self.assertFalse(test[0])

        # Test empty parameters
        menu.set_onmouseover(lambda: print('Mouse over'))
        menu.set_onmouseleave(lambda: print('Mouse leave'))

        menu.update(PygameEventUtils.mouse_click(50, 50, inlist=True, evtype=pygame.MOUSEMOTION))
        menu.update(PygameEventUtils.mouse_click(rect.centerx, rect.centery,
                                                 inlist=True, evtype=pygame.MOUSEMOTION))
        menu.update(PygameEventUtils.mouse_click(50, 50, inlist=True, evtype=pygame.MOUSEMOTION))

        # Test window mouseover and mouseleave
        test: Any = [None]

        def on_over(m: 'pygame_menu.Menu') -> None:
            """
            Mouse over window.
            """
            self.assertIsInstance(m, pygame_menu.Menu)
            test[0] = True

        def on_leave(m: 'pygame_menu.Menu') -> None:
            """
            Mouse leave window.
            """
            self.assertIsInstance(m, pygame_menu.Menu)
            test[0] = False

        menu.set_onwindowmouseover(on_over)
        menu.set_onwindowmouseleave(on_leave)

        self.assertIsNone(test[0])
        menu.update(PygameEventUtils.enter_window())  # Enter
        self.assertTrue(test[0])
        menu.update(PygameEventUtils.leave_window())  # Leave
        self.assertFalse(test[0])

        # Test empty parameters
        menu.set_onwindowmouseover(lambda: print('Window mouse over'))
        menu.set_onwindowmouseleave(lambda: print('Window mouse leave'))

        menu.update(PygameEventUtils.enter_window())
        menu._mouseover = True
        menu.update(PygameEventUtils.leave_window())
        self.assertEqual(menu.get_last_update_mode()[0], pygame_menu.events.MENU_LAST_MOUSE_LEAVE_WINDOW)

        menu.update([])
        self.assertEqual(menu.get_last_update_mode()[0], pygame_menu.events.MENU_LAST_NONE)

        # Test if not enabled
        menu.disable()
        self.assertRaises(RuntimeError, lambda: menu.update([]))

        menu.enable()
        menu._disable_update = True
        self.assertFalse(menu.update([]))
        menu._disable_update = False

        # Test scrollbars
        menu._scrollarea.update = lambda _: True
        self.assertTrue(menu.update([]))
        self.assertEqual(menu.get_last_update_mode()[0], pygame_menu.events.MENU_LAST_SCROLL_AREA)
        menu._scrollarea.update = lambda _: False

        # Test menubar
        menu._menubar.update = lambda _: True
        self.assertTrue(menu.update([]))
        self.assertEqual(menu.get_last_update_mode()[0], pygame_menu.events.MENU_LAST_MENUBAR)
        menu._menubar.update = lambda _: False

        # Test quit
        menu._disable_exit = True
        self.assertTrue(menu.update([pygame.event.Event(pygame.QUIT)]))
        self.assertEqual(menu.get_last_update_mode()[0], pygame_menu.events.MENU_LAST_QUIT)
        self.assertTrue(menu.update([pygame.event.Event(pygame_menu.events.PYGAME_WINDOWCLOSE)]))
        self.assertEqual(menu.get_last_update_mode()[0], pygame_menu.events.MENU_LAST_QUIT)

        # Test menu close
        menu._onclose = lambda: None
        self.assertTrue(menu.update(PygameEventUtils.key(ctrl.KEY_CLOSE_MENU, keydown=True)))
        self.assertEqual(menu.get_last_update_mode()[0], pygame_menu.events.MENU_LAST_MENU_CLOSE)

    def test_theme_params(self) -> None:
        """
        Test menu theme parameters.
        """
        th = TEST_THEME.copy()

        # Change title visibility
        th.title = False
        menu = MenuUtils.generic_menu(theme=th)
        self.assertFalse(menu.get_menubar().is_visible())
        th.title = True
        menu = MenuUtils.generic_menu(theme=th)
        self.assertTrue(menu.get_menubar().is_visible())

        # Updates window title
        th.title_updates_pygame_display = True
        menu = MenuUtils.generic_menu(theme=th, title='Epic')
        menu.draw(surface)
        self.assertEqual(pygame.display.get_caption()[0], menu.get_title())

    # noinspection PyTypeChecker
    def test_widget_move_index(self) -> None:
        """
        Test widget index moving.
        """
        menu = MenuUtils.generic_menu(theme=TEST_THEME.copy())
        btn1 = menu.add.button('1')
        btn2 = menu.add.button('2')
        btn3 = menu.add.button('3')

        def test_order(button: Tuple['pygame_menu.widgets.Button', ...], selected: 'pygame_menu.widgets.Button') -> None:
            """
            Test button order.
            """
            self.assertEqual(menu.get_selected_widget(), selected)
            sel = []
            for w in button:
                sel.append(int(w == selected))
            if PYGAME_V2:
                self.assertEqual(menu._test_widgets_status(), (
                    (('Button-' + button[0].get_title(),
                      (0, 0, 0, 291, 102, 17, 41, 291, 257, 291, 102),
                      (1, 0, sel[0], 1, 0, 0, 0)),
                     ('Button-' + button[1].get_title(),
                      (0, 1, 1, 291, 153, 17, 41, 291, 308, 291, 153),
                      (1, 0, sel[1], 1, 0, 0, 0)),
                     ('Button-' + button[2].get_title(),
                      (0, 2, 2, 291, 204, 17, 41, 291, 359, 291, 204),
                      (1, 0, sel[2], 1, 0, 0, 0)))
                ))

            else:
                self.assertEqual(menu._test_widgets_status(), (
                    (('Button-' + button[0].get_title(),
                      (0, 0, 0, 291, 100, 17, 42, 291, 255, 291, 100),
                      (1, 0, sel[0], 1, 0, 0, 0)),
                     ('Button-' + button[1].get_title(),
                      (0, 1, 1, 291, 152, 17, 42, 291, 307, 291, 152),
                      (1, 0, sel[1], 1, 0, 0, 0)),
                     ('Button-' + button[2].get_title(),
                      (0, 2, 2, 291, 204, 17, 42, 291, 359, 291, 204),
                      (1, 0, sel[2], 1, 0, 0, 0)))
                ))

        test_order((btn1, btn2, btn3), btn1)
        menu.move_widget_index(btn1)  # Move to last
        test_order((btn2, btn3, btn1), btn1)
        menu.move_widget_index(btn3, 0)
        test_order((btn3, btn2, btn1), btn1)
        menu.move_widget_index(btn2, btn1)  # 2 after 1
        test_order((btn3, btn1, btn2), btn1)
        self.assertRaises(AssertionError, lambda: menu.move_widget_index(btn2, btn2))
        menu.move_widget_index(btn1, btn2)  # 2 after 1
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

    # noinspection SpellCheckingInspection
    def test_mouseover_widget(self) -> None:
        """
        Test mouseover + motion.
        """
        menu = MenuUtils.generic_menu()
        btn1 = menu.add.button('1', cursor=pygame_menu.locals.CURSOR_ARROW, button_id='b1')
        btn2 = menu.add.button('2', cursor=pygame_menu.locals.CURSOR_ARROW, button_id='b2')

        # Setup
        menu.select_widget('b2')
        self.assertEqual(menu.get_selected_widget(), btn2)
        menu.select_widget('b1')
        self.assertTrue(btn1.is_selected())
        self.assertFalse(menu._mouse_motion_selection)

        test = [False, False, False, False]  # btn1over, btn1leave, btn2over, btn2leave
        print_events = False

        def onover1(widget, _) -> None:
            """
            Onover event.
            """
            self.assertEqual(btn1, widget)
            test[0] = not test[0]
            if print_events:
                print('Enter 1')

        def onleave1(widget, _) -> None:
            """
            Onleave event.
            """
            self.assertEqual(btn1, widget)
            test[1] = not test[1]
            if print_events:
                print('Leave 1')

        def onover2(widget, _) -> None:
            """
            Onover event.
            """
            self.assertEqual(btn2, widget)
            test[2] = not test[2]
            if print_events:
                print('Enter 2')

        def onleave2(widget, _) -> None:
            """
            Onleave event.
            """
            self.assertEqual(btn2, widget)
            test[3] = not test[3]
            if print_events:
                print('Leave 2')

        btn1.set_onmouseover(onover1)
        btn1.set_onmouseleave(onleave1)
        btn2.set_onmouseover(onover2)
        btn2.set_onmouseleave(onleave2)

        btn1.set_cursor(pygame_menu.locals.CURSOR_HAND)
        btn2.set_cursor(pygame_menu.locals.CURSOR_CROSSHAIR)

        # Test before
        self.assertEqual(test, [False, False, False, False])

        reset_widgets_over()
        self.assertEqual(WIDGET_MOUSEOVER, [None, []])

        # Get cursors
        cur_none = get_cursor()
        if cur_none is None:
            return

        set_pygame_cursor(btn1._cursor)
        cur1 = get_cursor()

        set_pygame_cursor(btn2._cursor)
        cur2 = get_cursor()

        set_pygame_cursor(cur_none)

        # Place mouse over widget 1, it should set as mouseover and trigger the events
        deco = menu.get_decorator()

        def draw_rect() -> None:
            """
            Draw absolute rect on surface for testing purposes.
            """
            surface.fill((255, 255, 255), btn1.get_rect(to_real_position=True))

        deco.add_callable(draw_rect, prev=False, pass_args=False)
        self.assertEqual(get_cursor(), cur_none)
        menu.update(PygameEventUtils.mouse_motion(btn1))
        self.assertEqual(menu.get_selected_widget(), btn1)
        self.assertEqual(test, [True, False, False, False])
        self.assertEqual(WIDGET_MOUSEOVER, [btn1, [btn1, cur_none, []]])
        self.assertEqual(get_cursor(), cur1)

        # Place mouse away. This should force widget 1 mouseleave
        mouse_away_event = PygameEventUtils.middle_rect_click((1000, 1000), evtype=pygame.MOUSEMOTION)
        menu.update(mouse_away_event)
        self.assertEqual(test, [True, True, False, False])
        self.assertEqual(WIDGET_MOUSEOVER, [None, []])
        self.assertEqual(get_cursor(), cur_none)

        # Place over widget 2
        menu.update(PygameEventUtils.mouse_motion(btn2))
        self.assertEqual(test, [True, True, True, False])
        self.assertEqual(WIDGET_MOUSEOVER, [btn2, [btn2, cur_none, []]])
        self.assertEqual(get_cursor(), cur2)

        # Place mouse away. This should force widget 1 mouseleave
        menu.update(mouse_away_event)
        self.assertEqual(test, [True, True, True, True])
        self.assertEqual(WIDGET_MOUSEOVER, [None, []])
        self.assertEqual(get_cursor(), cur_none)

        # Test immediate switch, from 1 to 2, then from 2 to 1, then off
        test = [False, False, False, False]
        menu.update(PygameEventUtils.mouse_motion(btn1))
        self.assertEqual(menu.get_selected_widget(), btn1)
        self.assertEqual(test, [True, False, False, False])
        self.assertEqual(WIDGET_MOUSEOVER, [btn1, [btn1, cur_none, []]])
        self.assertEqual(get_cursor(), cur1)
        menu.update(PygameEventUtils.mouse_motion(btn2))
        self.assertEqual(menu.get_selected_widget(), btn1)
        self.assertEqual(test, [True, True, True, False])
        self.assertEqual(WIDGET_MOUSEOVER, [btn2, [btn2, cur_none, []]])
        self.assertEqual(get_cursor(), cur2)
        menu.update(mouse_away_event)
        self.assertEqual(test, [True, True, True, True])
        self.assertEqual(WIDGET_MOUSEOVER, [None, []])
        self.assertEqual(get_cursor(), cur_none)

        # Same switch test, but now with widget selection by mouse motion
        menu._mouse_motion_selection = True
        test = [False, False, False, False]
        menu.select_widget(btn2)
        self.assertEqual(menu.get_selected_widget(), btn2)
        menu.update(PygameEventUtils.mouse_motion(btn1))
        self.assertEqual(menu.get_selected_widget(), btn1)
        self.assertEqual(test, [True, False, False, False])
        self.assertEqual(WIDGET_MOUSEOVER, [btn1, [btn1, cur_none, []]])
        self.assertEqual(get_cursor(), cur1)
        menu.update(PygameEventUtils.mouse_motion(btn2))
        self.assertEqual(menu.get_selected_widget(), btn2)
        self.assertEqual(test, [True, True, True, False])
        self.assertEqual(WIDGET_MOUSEOVER, [btn2, [btn2, cur_none, []]])
        self.assertEqual(get_cursor(), cur2)
        menu.update(mouse_away_event)
        self.assertEqual(test, [True, True, True, True])
        self.assertEqual(WIDGET_MOUSEOVER, [None, []])
        self.assertEqual(get_cursor(), cur_none)
        menu.update(mouse_away_event)
        self.assertEqual(test, [True, True, True, True])
        self.assertEqual(WIDGET_MOUSEOVER, [None, []])
        self.assertEqual(get_cursor(), cur_none)
        self.assertEqual(menu.get_selected_widget(), btn2)

        # Mouseover btn1, but then hide it
        menu._mouse_motion_selection = False
        test = [False, False, False, False]
        menu.update(PygameEventUtils.mouse_motion(btn1))
        self.assertEqual(test, [True, False, False, False])
        self.assertEqual(WIDGET_MOUSEOVER, [btn1, [btn1, cur_none, []]])
        self.assertEqual(get_cursor(), cur1)
        btn1.hide()
        self.assertEqual(WIDGET_MOUSEOVER, [None, []])
        self.assertEqual(get_cursor(), cur_none)

        # Test close
        menu.update(PygameEventUtils.mouse_motion(btn2))
        self.assertEqual(test, [True, True, True, False])
        self.assertEqual(WIDGET_MOUSEOVER, [btn2, [btn2, cur_none, []]])
        self.assertEqual(get_cursor(), cur2)
        menu.disable()
        self.assertEqual(test, [True, True, True, True])
        self.assertEqual(WIDGET_MOUSEOVER, [None, []])
        self.assertEqual(get_cursor(), cur_none)
        btn2.mouseleave(PygameEventUtils.mouse_motion(btn2))
        self.assertEqual(test, [True, True, True, True])
        self.assertEqual(WIDGET_MOUSEOVER, [None, []])
        self.assertEqual(get_cursor(), cur_none)

        # Enable
        menu.enable()
        menu.update(PygameEventUtils.mouse_motion(btn2))
        self.assertEqual(test, [True, True, False, True])
        self.assertEqual(WIDGET_MOUSEOVER, [btn2, [btn2, cur_none, []]])
        self.assertEqual(get_cursor(), cur2)

        # Move to hidden
        menu.update(PygameEventUtils.mouse_motion(btn1))
        self.assertEqual(test, [True, True, False, False])
        self.assertEqual(WIDGET_MOUSEOVER, [None, []])
        self.assertEqual(get_cursor(), cur_none)

        # Unhide
        btn1.show()
        test = [False, False, False, False]
        prev_pos1 = PygameEventUtils.mouse_motion(btn1)
        menu.update(prev_pos1)
        self.assertEqual(test, [True, False, False, False])
        self.assertEqual(WIDGET_MOUSEOVER, [btn1, [btn1, cur_none, []]])

        # Move btn1 and btn2
        self.assertEqual(menu.get_widgets(), (btn1, btn2))
        menu.move_widget_index(btn1, btn2)
        self.assertEqual(menu.get_widgets(), (btn2, btn1))
        self.assertEqual(WIDGET_MOUSEOVER, [None, []])

        menu.update(prev_pos1)
        self.assertEqual(WIDGET_MOUSEOVER, [btn2, [btn2, cur_none, []]])

        # Remove btn2
        menu.remove_widget(btn2)
        self.assertEqual(WIDGET_MOUSEOVER, [None, []])
        menu._test_print_widgets()

        # Select btn1
        menu.update(PygameEventUtils.mouse_motion(btn1))
        self.assertEqual(WIDGET_MOUSEOVER, [btn1, [btn1, cur_none, []]])
        self.assertEqual(get_cursor(), cur1)

        # Change previous cursor to assert an error
        self.assertEqual(cur_none, WIDGET_TOP_CURSOR[0])
        WIDGET_MOUSEOVER[1][1] = cur2
        menu.update(mouse_away_event)
        self.assertEqual(get_cursor(), cur_none)

    # noinspection SpellCheckingInspection
    def test_floating_pos(self) -> None:
        """
        Test floating widgets.
        """
        # First, add a widget and test the positioning
        menu = MenuUtils.generic_menu(theme=THEME_NON_FIXED_TITLE)
        btn = menu.add.button('floating')
        self.assertEqual(btn.get_alignment(), pygame_menu.locals.ALIGN_CENTER)
        expc_pos = (247, 153)
        if not PYGAME_V2:
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

    def test_baseimage_selector(self) -> None:
        """
        Test baseimage selector + menulink interaction.
        """
        if sys.version_info.major == 3 and sys.version_info.minor == 8:
            return
        x = 400
        y = 400

        class Sample:
            """
            Sample example which contains a selector that changes an image.
            """
            icons: List['pygame_menu.BaseImage']
            icon: 'pygame_menu.widgets.Image'
            selector: 'pygame_menu.widgets.Selector'

            def __init__(self) -> None:
                """
                Constructor.
                """
                theme = pygame_menu.themes.Theme(
                    title_font_size=8,
                    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
                    background_color=(116, 161, 122),
                    title_background_color=(4, 47, 58),
                    title_font_color=(38, 158, 151),
                    widget_selection_effect=pygame_menu.widgets.NoneSelection()
                )

                self.main_menu = pygame_menu.menu.Menu(
                    title='MAIN MENU',
                    height=x,
                    width=y,
                    theme=theme
                )

                submenu1 = pygame_menu.menu.Menu(
                    title='SUB MENU 1',
                    height=x,
                    width=y,
                    theme=theme
                )

                submenu1.add.label('SUB MENU 1')

                submenu2 = pygame_menu.menu.Menu(
                    title='SUB MENU 2',
                    height=x,
                    width=y,
                    theme=theme
                )

                submenu2.add.label('SUB MENU 2')

                # Here I resized the icons beforehand
                self.icons = [
                    pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU).resize(80, 80),
                    pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_PYTHON).resize(80, 80)
                ]

                self.icon = self.main_menu.add.image(image_path=self.icons[0].copy())

                def update_icon(*args) -> None:
                    """
                    Update icon handler.
                    """
                    icon_idx = args[0][-1]
                    set_icon = self.icons[icon_idx].copy()
                    set_icon.scale(2, 2)
                    self.icon.set_image(set_icon)

                def open_menu(*args) -> None:
                    """
                    Open menu handler.
                    """
                    sub = args[-1][0][1]
                    sub.open()

                self.selector = self.main_menu.add.selector(
                    '',
                    [
                        ('Menu 1', self.main_menu.add.menu_link(submenu1)),
                        ('Menu 2', self.main_menu.add.menu_link(submenu2)),
                    ],
                    onchange=update_icon,
                    onreturn=open_menu,
                )
                self.selector.change()

        s = Sample()
        s.main_menu.draw(surface)

        self.assertEqual(s.icon.get_size(), (176, 168))
        self.assertEqual(s.main_menu.get_title(), 'MAIN MENU')

        # Change selector
        s.selector.apply()
        self.assertEqual(s.icon.get_size(), (176, 168))
        self.assertEqual(s.main_menu.get_current().get_title(), 'SUB MENU 1')

        s.selector._left()
        s.selector.apply()
        self.assertEqual(s.icon.get_size(), (176, 168))
        self.assertEqual(s.main_menu.get_current().get_title(), 'SUB MENU 2')

    def test_resize(self) -> None:
        """
        Test menu resize.
        """
        theme = pygame_menu.themes.THEME_DEFAULT.copy()
        menu = MenuUtils.generic_menu(theme=theme)
        self.assertEqual(menu.get_size(), (600, 400))

        # Disable auto centering depending on the case
        menu._auto_centering = True
        theme.widget_offset = (0, 10)
        menu.resize(300, 300)
        self.assertFalse(menu._auto_centering)
        theme.widget_offset = (0, 0)

        menu._auto_centering = True
        theme.scrollarea_outer_margin = (0, 10)
        menu.resize(300, 300)
        self.assertFalse(menu._auto_centering)
        theme.widget_offset = (0, 0)

        # Test resize
        menu = MenuUtils.generic_menu(theme=theme, column_max_width=[0])
        self.assertEqual(menu._column_max_width_zero, [True])
        self.assertEqual(menu._column_max_width, [600])
        self.assertEqual(menu._menubar._width, 600)
        self.assertFalse(menu._widgets_surface_need_update)
        menu.resize(300, 300)
        self.assertFalse(menu._widgets_surface_need_update)
        self.assertEqual(menu.get_size(), (300, 300))
        self.assertEqual(menu._column_max_width, [300])
        self.assertEqual(menu._menubar._width, 300)

        # Render
        self.assertIsNone(menu._widgets_surface)
        menu.render()
        self.assertIsNotNone(menu._widgets_surface)
        menu.resize(200, 200)
        self.assertTrue(menu._widgets_surface_need_update)

        # Add button to resize
        menu = MenuUtils.generic_menu()

        # noinspection PyMissingTypeHints
        def _resize():
            if menu.get_size()[0] == 300:
                menu.resize(600, 400)
            else:
                menu.resize(300, 300)

        btn = menu.add.button('Resize', _resize)
        self.assertEqual(menu.get_size()[0], 600)
        btn.apply()
        self.assertEqual(menu.get_size()[0], 300)

        # Resize with another surface size
        menu.resize(300, 300, (500, 500))

        # Invalid size
        self.assertRaises(ValueError, lambda: menu.resize(50, 10))

        # Resize but using position absolute
        menu.resize(400, 400, position=(50, 50))
        self.assertTrue(menu._position_relative)
        self.assertEqual(menu._position, (100, 100))
        menu.resize(400, 400, position=(50, 50, False))
        self.assertFalse(menu._position_relative)
        self.assertEqual(menu._position, (50, 50))

        # Resize, hide scrollbars
        theme = pygame_menu.themes.THEME_DEFAULT.copy()
        menu = MenuUtils.generic_menu(theme=theme)
        for i in range(8):
            menu.add.button(i, bool)
        sa = menu.get_scrollarea()

        # Test with force
        self.assertEqual(sa.get_size(inner=True), (580, 400))
        sa.hide_scrollbars(pygame_menu.locals.ORIENTATION_VERTICAL)
        self.assertEqual(sa.get_size(inner=True), (600, 400))
        sa.show_scrollbars(pygame_menu.locals.ORIENTATION_VERTICAL)
        self.assertEqual(sa.get_size(inner=True), (580, 400))

        # Disable force, this will not affect menu as after resizing the scrollbars
        # will re-show again
        sa.hide_scrollbars(pygame_menu.locals.ORIENTATION_VERTICAL, force=False)
        self.assertEqual(sa.get_size(inner=True), (580, 400))
        sa.show_scrollbars(pygame_menu.locals.ORIENTATION_VERTICAL, force=False)
        self.assertEqual(sa.get_size(inner=True), (580, 400))

        # Test submenu recursive resizing
        menu = MenuUtils.generic_menu(theme=theme)
        menu2 = MenuUtils.generic_menu(theme=theme)
        menu3 = MenuUtils.generic_menu(theme=theme)
        menu.add.button('btn', menu2)
        menu2.add.button('btn', menu3)
        self.assertEqual(menu.get_submenus(True), (menu2, menu3))
        for m in (menu, menu2, menu3):
            self.assertEqual(m.get_size(), (600, 400))
        menu.resize(300, 300, recursive=True)  # Now, resize
        for m in (menu, menu2, menu3):
            self.assertEqual(m.get_size(), (300, 300))

    def test_get_size(self) -> None:
        """
        Test get menu size.
        """
        theme = pygame_menu.themes.THEME_DEFAULT.copy()
        menu = MenuUtils.generic_menu(theme=theme)
        self.assertEqual(menu.get_size(), (600, 400))

        # Create new menu with image border
        for scale in [(1, 1), (2, 5), (5, 2)]:
            theme.border_color = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_TILED_BORDER)
            theme.border_color.scale(*scale)
            border_size = theme.border_color.get_size()
            menu = MenuUtils.generic_menu(theme=theme)
            self.assertEqual(menu.get_size(), (600, 400))
            self.assertEqual(menu.get_size(border=True), (600 + 2 * border_size[0] / 3, 400 + 2 * border_size[1] / 3))

        # Create new menu with border color
        theme.border_width = 10
        theme.border_color = 'red'
        menu = MenuUtils.generic_menu(theme=theme)
        self.assertEqual(menu.get_size(border=True), (600 + 2 * theme.border_width, 400 + 2 * theme.border_width))

        # Menu with none border color
        theme.border_width = 10
        theme.border_color = None
        menu = MenuUtils.generic_menu(theme=theme)
        self.assertEqual(menu.get_size(border=True), (600, 400))

        # Menu with selection effect
        theme = pygame_menu.themes.THEME_BLUE.copy()
        theme.title = False
        theme.scrollarea_position = pygame_menu.locals.SCROLLAREA_POSITION_NONE
        theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection(arrow_right_margin=50)

        menu = pygame_menu.Menu('Welcome', 200, 200, theme=theme)
        menu.add.button('Play')
        menu.add.button('Quit', pygame_menu.events.EXIT)
        size = menu.get_size(widget=True)
        self.assertEqual(size, (136, 98))
        self.assertEqual(menu.resize(*size).get_size(), size)

    def test_border_color(self) -> None:
        """
        Test menu border color.
        """
        theme = pygame_menu.themes.THEME_DEFAULT.copy()
        self.assertIsNone(theme.border_color)
        theme.border_width = 10
        theme.title_font_size = 15

        # Test invalid
        theme.border_color = 'invalid'
        self.assertRaises(ValueError, lambda: pygame_menu.Menu('Menu with border color', 250, 250, theme=theme))

        # Test with border color
        theme.border_color = 'red'
        menu = pygame_menu.Menu('Menu with border color', 250, 250, theme=theme)
        menu.draw(surface)

        # Test with image
        theme.border_color = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_TILED_BORDER)
        menu = pygame_menu.Menu('Menu with border image', 250, 250, theme=theme)
        menu.draw(surface)

    def test_menu_render_toggle(self) -> None:
        """
        Test add menu widgets with render enable/disable.
        """
        menu = MenuUtils.generic_menu(columns=3, rows=50)
        nc, nr = menu.get_col_rows()
        self.assertEqual(nc, 3)
        self.assertEqual(nr, [50, 50, 50])

        # Test with rendering enabled
        n = sum(nr)  # Number of widgets to be added
        t0 = time.time()
        widgets: List[Label] = []
        for i in range(n):
            widgets.append(menu.add.label(i))
        t_on = time.time() - t0
        position_before: List[Tuple[int, int]] = []
        for i in range(n):
            position_before.append(widgets[i].get_position())

        # Test with rendering disabled
        menu.clear()
        widgets.clear()
        menu.disable_render()
        t0 = time.time()
        for i in range(n):
            widgets.append(menu.add.label(i))
        menu.enable_render()
        menu.render()
        t_off = time.time() - t0
        self.assertGreater(t_on, t_off)

        # Position after render must be equal!
        for i in range(n):
            self.assertEqual(position_before[i], widgets[i].get_position())

        print(f'Render on: {t_on}s, off: {t_off}s')

    def test_menu_widget_selected_events(self) -> None:
        """
        Test menu passing events to selected widget.
        """
        menu = MenuUtils.generic_menu()
        age = menu.add.text_input('Character age:')
        name = menu.add.text_input('Character name:')
        menu.update(PygameEventUtils.key(pygame.K_a, keydown=True, char='a'))
        self.assertTrue(age.is_selected())
        self.assertFalse(name.is_selected())
        self.assertEqual(age.get_value(), 'a')
        self.assertEqual(name.get_value(), '')
        menu.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
        self.assertFalse(age.is_selected())
        self.assertTrue(name.is_selected())

        # Now, disable global widget selected event
        menu._widget_selected_update = False
        menu.update(PygameEventUtils.key(pygame.K_a, keydown=True, char='a'))
        self.assertEqual(name.get_value(), '')

        # Re-enable global widget selected event
        menu._widget_selected_update = True
        menu.update(PygameEventUtils.key(pygame.K_a, keydown=True, char='a'))
        self.assertEqual(name.get_value(), 'a')

        # Disable local widget accept event
        name.receive_menu_update_events = False
        menu.update(PygameEventUtils.key(pygame.K_a, keydown=True, char='a'))
        self.assertEqual(name.get_value(), 'a')

        # Enable local widget accept event
        name.receive_menu_update_events = True
        menu.update(PygameEventUtils.key(pygame.K_s, keydown=True, char='s'))
        self.assertEqual(name.get_value(), 'as')

    def test_subsurface_offset(self) -> None:
        """
        Test subsurface widget offset.
        """
        main_surface = surface
        w, h = surface.get_size()
        left_surf_w, left_surf_h = 300, h
        menu_w, menu_h = w - left_surf_w, h
        # left_surface = main_surface.subsurface((0, 0, left_surf_w, left_surf_h))
        menu_surface = main_surface.subsurface((300, 0, menu_w, menu_h))
        menu = MenuUtils.generic_menu(title='Subsurface', width=menu_w, height=menu_h, position_x=0, position_y=0, mouse_motion_selection=True, surface=menu_surface)
        btn_click = [False]

        def btn() -> None:
            """
            Method executed by button.
            """
            btn_click[0] = True

        b1 = menu.add.button('Button', btn)
        menu._surface = None
        self.assertEqual(menu.get_last_surface_offset(), (0, 0))
        self.assertEqual(b1.get_rect(to_real_position=True).x, 94)
        self.assertIsNone(menu._surface_last)
        menu._surface = menu_surface
        self.assertEqual(menu._surface, menu_surface)
        self.assertEqual(menu.get_last_surface_offset(), (300, 0))
        r = b1.get_rect(to_real_position=True)
        self.assertEqual(r.x, 394)
        self.assertIsNone(menu._surface_last)
        menu.draw()
        self.assertEqual(menu._surface_last, menu_surface)
        menu.draw(surface)  # This updates last surface
        self.assertEqual(menu._surface_last, surface)
        menu._surface = surface
        self.assertEqual(menu.get_last_surface_offset(), (0, 0))
        surface.fill((0, 0, 0))

        # Now, test click event
        menu._surface = menu_surface
        self.assertFalse(btn_click[0])
        menu.update(PygameEventUtils.middle_rect_click(r))
        self.assertTrue(btn_click[0])

        # Mainloop also updates last surface
        menu.mainloop(disable_loop=True)
        self.assertEqual(menu._surface_last, menu_surface)
