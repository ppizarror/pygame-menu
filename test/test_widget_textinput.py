"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - TEXTINPUT
Test TextInput and ColorInput widgets.
"""

__all__ = ['TextInputWidgetTest']

from test._utils import MenuUtils, surface, PygameEventUtils, TEST_THEME, PYGAME_V2, \
    BaseTest, sleep

import pygame
import pygame_menu
import pygame_menu.controls as ctrl

from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented


class TextInputWidgetTest(BaseTest):

    # noinspection SpellCheckingInspection,PyTypeChecker
    def test_textinput(self) -> None:
        """
        Test TextInput widget.
        """
        menu = MenuUtils.generic_menu()

        # Assert bad settings
        self.assertRaises(ValueError,
                          lambda: menu.add.text_input('title',
                                                      input_type=pygame_menu.locals.INPUT_FLOAT,
                                                      default='bad'))
        self.assertRaises(ValueError,  # Default and password cannot coexist
                          lambda: menu.add.text_input('title',
                                                      password=True,
                                                      default='bad'))

        # Create text input widget
        textinput = menu.add.text_input('title', input_underline='_')
        textinput.set_value('new_value')  # No error
        textinput._selected = False
        textinput.draw(surface)
        textinput.select(update_menu=True)
        textinput.draw(surface)
        self.assertEqual(textinput.get_value(), 'new_value')
        textinput.clear()
        self.assertEqual(textinput.get_value(), '')

        # Create selection box
        string = 'the text'
        textinput._cursor_render = True
        textinput.set_value(string)
        textinput._select_all()
        self.assertEqual(textinput._get_selected_text(), 'the text')
        textinput.draw(surface)
        textinput._unselect_text()
        textinput.draw(surface)

        # Assert events
        textinput.update(PygameEventUtils.key(0, keydown=True, testmode=False))
        PygameEventUtils.test_widget_key_press(textinput)
        textinput.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        textinput.update(PygameEventUtils.key(pygame.K_LSHIFT, keydown=True))
        textinput.clear()

        # Type
        textinput.update(PygameEventUtils.key(pygame.K_t, keydown=True, char='t'))
        textinput.update(PygameEventUtils.key(pygame.K_e, keydown=True, char='e'))
        textinput.update(PygameEventUtils.key(pygame.K_s, keydown=True, char='s'))
        textinput.update(PygameEventUtils.key(pygame.K_t, keydown=True, char='t'))

        # Keyup
        textinput.update(PygameEventUtils.key(pygame.K_a, keyup=True, char='a'))
        self.assertEqual(textinput.get_value(), 'test')  # The text we typed

        # Ctrl events
        textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_c))  # copy
        textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_v))  # paste
        textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_z))  # undo
        self.assertEqual(textinput.get_value(), 'tes')
        textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_y))  # redo
        self.assertEqual(textinput.get_value(), 'test')
        textinput._select_all()
        textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_x))  # cut
        self.assertEqual(textinput.get_value(), '')
        textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_z))  # undo
        self.assertEqual(textinput.get_value(), 'test')
        textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_y))  # redo
        self.assertEqual(textinput.get_value(), '')
        textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_z))  # undo
        self.assertEqual(textinput.get_value(), 'test')

        # Test ignore ctrl events
        textinput._copy_paste_enabled = False
        self.assertFalse(textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_c)))
        self.assertFalse(textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_v)))
        max_history = textinput._max_history
        textinput._max_history = 0
        self.assertFalse(textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_z)))
        self.assertFalse(textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_y)))
        self.assertFalse(textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_x)))
        textinput._selection_enabled = False
        self.assertFalse(textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_a)))
        self.assertFalse(textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_r)))  # invalid

        # Reset
        textinput._copy_paste_enabled = True
        textinput._max_history = max_history
        textinput._selection_enabled = True

        # Test selection, if user selects all and types anything the selected
        # text must be destroyed
        textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_a))  # select all
        textinput._unselect_text()
        self.assertEqual(textinput._get_selected_text(), '')
        textinput._select_all()
        self.assertEqual(textinput._get_selected_text(), 'test')
        textinput._unselect_text()
        self.assertEqual(textinput._get_selected_text(), '')
        textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_a))
        self.assertEqual(textinput._get_selected_text(), 'test')
        textinput.update(PygameEventUtils.key(pygame.K_t, keydown=True, char='t'))
        textinput._select_all()
        self.assertTrue(textinput.update(PygameEventUtils.key(pygame.K_ESCAPE, keydown=True)))
        textinput._select_all()
        self.assertTrue(textinput.update(PygameEventUtils.key(pygame.K_BACKSPACE, keydown=True)))
        self.assertEqual(textinput.get_value(), '')
        textinput.set_value('t')

        # Releasing shift disable selection
        textinput._selection_active = True
        textinput.update(PygameEventUtils.key(pygame.K_LSHIFT, keyup=True))
        self.assertFalse(textinput._selection_active)

        # Arrows while selection
        textinput._select_all()
        self.assertIsNotNone(textinput._selection_surface)
        textinput.update(PygameEventUtils.key(pygame.K_LEFT, keydown=True))
        self.assertIsNone(textinput._selection_surface)
        textinput._select_all()
        self.assertIsNotNone(textinput._selection_surface)
        textinput.update(PygameEventUtils.key(pygame.K_RIGHT, keydown=True))
        self.assertIsNone(textinput._selection_surface)

        textinput._select_all()
        textinput._selection_active = True
        self.assertEqual(textinput._selection_box, [0, 1])
        textinput.update(PygameEventUtils.key(pygame.K_LEFT, keydown=True))
        self.assertEqual(textinput._selection_box, [0, 0])
        textinput._select_all()
        textinput._selection_active = True
        textinput.update(PygameEventUtils.key(pygame.K_RIGHT, keydown=True))
        self.assertEqual(textinput._selection_box, [0, 1])

        # Remove while selection
        textinput._select_all()
        textinput.update(PygameEventUtils.key(pygame.K_DELETE, keydown=True))
        self.assertEqual(textinput.get_value(), '')
        textinput.set_value('t')

        # Now the value must be t
        self.assertEqual(textinput._get_selected_text(), '')
        self.assertEqual(textinput.get_value(), 't')

        # Test readonly
        textinput.update(PygameEventUtils.key(pygame.K_t, keydown=True, char='k'))
        self.assertEqual(textinput.get_value(), 'tk')
        textinput.readonly = True
        textinput.update(PygameEventUtils.key(pygame.K_t, keydown=True, char='k'))
        self.assertEqual(textinput.get_value(), 'tk')
        textinput.readonly = False

        # Test keyup
        self.assertIn(pygame.K_t, textinput._keyrepeat_counters.keys())
        self.assertFalse(textinput.update(
            PygameEventUtils.key(pygame.K_t, keyup=True, char='1')))
        self.assertNotIn(pygame.K_t, textinput._keyrepeat_counters.keys())

        # Test tab
        self.assertEqual(textinput._tab_size, 4)
        textinput.update(PygameEventUtils.key(pygame.K_TAB, keydown=True))
        self.assertEqual(textinput.get_value(), 'tk    ')

        # Test invalid unicode
        self.assertFalse(textinput.update(PygameEventUtils.key(pygame.K_1, keydown=True)))

        # Up/Down disable active status
        textinput.active = True
        textinput.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
        self.assertFalse(textinput.active)
        textinput.active = True
        textinput.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
        self.assertFalse(textinput.active)
        textinput.active = True
        self.assertTrue(textinput.update(PygameEventUtils.key(pygame.K_ESCAPE, keydown=True)))
        self.assertFalse(textinput.active)

        # Test mouse
        textinput._selected = True
        textinput._selection_time = 0
        textinput.update(PygameEventUtils.middle_rect_click(textinput))
        self.assertTrue(textinput._cursor_visible)
        textinput._select_all()
        textinput._selection_active = True
        self.assertEqual(textinput._cursor_position, 6)
        self.assertEqual(textinput._selection_box, [0, 6])
        textinput.update(PygameEventUtils.middle_rect_click(textinput, evtype=pygame.MOUSEBUTTONDOWN))
        self.assertEqual(textinput._selection_box, [0, 0])

        # Check click pos
        textinput._check_mouse_collide_input(PygameEventUtils.middle_rect_click(textinput)[0].pos)
        self.assertEqual(textinput._cursor_position, 6)

        # Test touch
        textinput._cursor_position = 0
        textinput._check_touch_collide_input(PygameEventUtils.middle_rect_click(textinput)[0].pos)
        self.assertEqual(textinput._cursor_position, 6)

        # Update mouse
        for i in range(50):
            textinput.update(PygameEventUtils.key(pygame.K_t, keydown=True, char='t'))
        textinput._update_cursor_mouse(50)
        textinput._cursor_render = True
        textinput._render_cursor()

        # Test multiple are selected
        menu.add.text_input('title', password=True, input_underline='_').select()
        self.assertRaises(pygame_menu.menu._MenuMultipleSelectedWidgetsException, lambda: menu.draw(surface))
        textinput.clear()
        textinput.select(update_menu=True)
        menu.draw(surface)

        # Clear the menu
        self.assertEqual(menu._stats.removed_widgets, 0)
        self.assertEqual(textinput.get_menu(), menu)
        menu.clear()
        self.assertIsNone(textinput.get_menu())
        self.assertEqual(menu._stats.removed_widgets, 3)
        menu.add.generic_widget(textinput)
        self.assertEqual(textinput.get_menu(), menu)
        menu.clear()
        self.assertEqual(menu._stats.removed_widgets, 4)

    def test_password(self) -> None:
        """
        Test password.
        """
        menu = MenuUtils.generic_menu()

        password_input = menu.add.text_input('title', password=True, input_underline='_')
        self.assertRaises(ValueError, lambda: password_input.set_value('new_value'))  # Password cannot be set
        password_input.set_value('')  # No error
        password_input._selected = False
        password_input.draw(surface)
        password_input.select(update_menu=True)
        password_input.draw(surface)
        self.assertEqual(password_input.get_value(), '')
        password_input.clear()
        self.assertEqual(password_input.get_value(), '')

        # Test none width password
        password_input._password_char = ''
        self.assertRaises(ValueError, lambda: password_input._apply_font())

    def test_unicode(self) -> None:
        """
        Test unicode support.
        """
        menu = MenuUtils.generic_menu()
        textinput = menu.add.text_input('title', input_underline='_')
        textinput.set_value('tk')

        # Test alt+x
        textinput.update(PygameEventUtils.key(pygame.K_SPACE, keydown=True))
        textinput.update(PygameEventUtils.key(pygame.K_2, keydown=True, char='2'))
        textinput.update(PygameEventUtils.key(pygame.K_1, keydown=True, char='1'))
        textinput.update(PygameEventUtils.key(pygame.K_1, keydown=True, char='5'))
        self.assertEqual(textinput.get_value(), 'tk 215')
        textinput.update(PygameEventUtils.keydown_mod_alt(pygame.K_x))  # convert 215 to unicode
        self.assertEqual(textinput.get_value(), 'tkȕ')
        textinput.update(PygameEventUtils.key(pygame.K_SPACE, keydown=True))
        textinput.update(PygameEventUtils.key(pygame.K_SPACE, keydown=True))
        textinput.update(PygameEventUtils.key(pygame.K_b, keydown=True, char='B'))
        textinput.update(PygameEventUtils.key(pygame.K_1, keydown=True, char='1'))
        textinput.update(PygameEventUtils.keydown_mod_alt(pygame.K_x))  # convert 215 to unicode
        self.assertEqual(textinput.get_value(), 'tkȕ ±')

        # Remove all
        textinput.clear()
        textinput.update(PygameEventUtils.key(pygame.K_b, keydown=True, char='B'))
        textinput.update(PygameEventUtils.key(pygame.K_1, keydown=True, char='1'))
        textinput.update(PygameEventUtils.keydown_mod_alt(pygame.K_x))  # convert 215 to unicode
        self.assertEqual(textinput.get_value(), '±')
        textinput.update(PygameEventUtils.keydown_mod_alt(pygame.K_x))  # convert same to unicode, do nothing
        self.assertEqual(textinput.get_value(), '±')

        # Test consecutive
        textinput.update(PygameEventUtils.key(pygame.K_2, keydown=True, char='2'))
        textinput.update(PygameEventUtils.key(pygame.K_0, keydown=True, char='0'))
        textinput.update(PygameEventUtils.key(pygame.K_1, keydown=True, char='1'))
        textinput.update(PygameEventUtils.key(pygame.K_3, keydown=True, char='3'))
        textinput.update(PygameEventUtils.keydown_mod_alt(pygame.K_x))  # convert 215 to unicode
        self.assertEqual(textinput.get_value(), '±–')

        # Test 0x
        textinput.clear()
        PygameEventUtils.release_key_mod()
        textinput.update(PygameEventUtils.key(pygame.K_0, keydown=True, char='0'))
        self.assertEqual(textinput.get_value(), '0')
        textinput.update(PygameEventUtils.key(pygame.K_x, keydown=True, char='x'))
        self.assertEqual(textinput.get_value(), '0x')
        textinput.update(PygameEventUtils.keydown_mod_alt(pygame.K_x))
        self.assertEqual(textinput.get_value(), '0x')
        textinput.update(PygameEventUtils.key(pygame.K_b, keydown=True, char='B'))
        textinput.update(PygameEventUtils.key(pygame.K_1, keydown=True, char='1'))
        self.assertEqual(textinput.get_value(), '0xB1')
        textinput.update(PygameEventUtils.keydown_mod_alt(pygame.K_x))
        self.assertEqual(textinput.get_value(), '±')
        PygameEventUtils.release_key_mod()

        textinput.update(PygameEventUtils.key(pygame.K_0, keydown=True, char='0'))
        textinput.update(PygameEventUtils.key(pygame.K_x, keydown=True, char='x'))
        textinput.update(PygameEventUtils.key(pygame.K_b, keydown=True, char='B'))
        textinput.update(PygameEventUtils.key(pygame.K_1, keydown=True, char='1'))
        textinput.update(PygameEventUtils.keydown_mod_alt(pygame.K_x))
        self.assertEqual(textinput.get_value(), '±±')

        # Test keyup
        self.assertIn(pygame.K_1, textinput._keyrepeat_counters.keys())
        self.assertFalse(textinput.update(PygameEventUtils.key(pygame.K_1, keyup=True, char='1')))
        self.assertNotIn(pygame.K_1, textinput._keyrepeat_counters.keys())

        # Test tab
        self.assertEqual(textinput._tab_size, 4)
        textinput.update(PygameEventUtils.key(pygame.K_TAB, keydown=True))
        self.assertEqual(textinput.get_value(), '±±    ')

        # Test invalid unicode
        self.assertFalse(textinput.update(PygameEventUtils.key(pygame.K_1, keydown=True)))

        # Test others
        textinput._input_type = 'other'
        self.assertTrue(textinput._check_input_type('-'))
        self.assertFalse(textinput._check_input_type('x'))
        textinput._maxwidth_update = None
        self.assertIsNone(textinput._update_maxlimit_renderbox())

    def test_undo_redo(self) -> None:
        """
        Test undo/redo.
        """
        menu = MenuUtils.generic_menu()

        # Test maxchar and undo/redo
        textinput = menu.add.text_input('title', input_underline='_', maxchar=20)
        textinput.set_value('the size of this textinput is way greater than the limit')
        self.assertEqual(textinput.get_value(), 'eater than the limit')  # same as maxchar
        self.assertEqual(textinput._cursor_position, 20)
        textinput._undo()  # This must set default at ''
        self.assertEqual(textinput.get_value(), '')
        textinput._redo()
        self.assertEqual(textinput.get_value(), 'eater than the limit')
        textinput.draw(surface)
        textinput._copy()
        textinput._paste()
        textinput._block_copy_paste = False
        textinput._select_all()
        textinput._cut()
        self.assertEqual(textinput.get_value(), '')
        textinput._undo()
        self.assertEqual(textinput.get_value(), 'eater than the limit')

        self.assertEqual(textinput._history_index, 1)
        textinput._history_index = 0
        self.assertFalse(textinput._undo())
        textinput._history_index = len(textinput._history) - 1
        self.assertFalse(textinput._redo())

    def test_copy_paste(self) -> None:
        """
        Test copy/paste.
        """
        menu = MenuUtils.generic_menu()

        # Test copy/paste
        textinput_nocopy = menu.add.text_input('title',
                                               input_underline='_',
                                               maxwidth=20,
                                               copy_paste_enable=False)
        textinput_nocopy.set_value('this cannot be copied')
        textinput_nocopy._copy()
        textinput_nocopy._paste()
        textinput_nocopy._cut()
        self.assertEqual(textinput_nocopy.get_value(), 'this cannot be copied')

        # Test copy/paste without block
        textinput_copy = menu.add.text_input('title',
                                             input_underline='_',
                                             maxwidth=20,
                                             maxchar=20)
        textinput_copy.set_value('this value should be cropped as this is longer than the max char')
        self.assertFalse(textinput_copy._block_copy_paste)
        textinput_copy._copy()
        self.assertTrue(textinput_copy._block_copy_paste)
        textinput_copy._block_copy_paste = False
        textinput_copy._select_all()
        textinput_copy._cut()
        self.assertEqual(textinput_copy.get_value(), '')
        textinput_copy._block_copy_paste = False
        textinput_copy._paste()
        textinput_copy._cut()
        textinput_copy._block_copy_paste = False
        # self.assertEqual(textinput_copy.get_value(), '')
        textinput_copy._valid_chars = ['e', 'r']
        textinput_copy._paste()

        # Copy password
        textinput_copy._password = True
        self.assertFalse(textinput_copy._copy())

    def test_overflow_removal(self) -> None:
        """
        Test text with max width and right overflow removal.
        """
        menu = MenuUtils.generic_menu()
        menu._copy_theme()
        menu._theme.widget_font_size = 20
        textinput = menu.add.text_input(
            'Some long text: ',
            maxwidth=19,
            textinput_id='long_text',
            input_underline='_'
        )
        self.assertRaises(WidgetTransformationNotImplemented, lambda: textinput.resize())
        self.assertRaises(WidgetTransformationNotImplemented, lambda: textinput.set_max_width())
        self.assertRaises(WidgetTransformationNotImplemented, lambda: textinput.set_max_height())
        self.assertRaises(WidgetTransformationNotImplemented, lambda: textinput.scale())
        self.assertRaises(WidgetTransformationNotImplemented, lambda: textinput.rotate())
        textinput.flip(True, True)
        self.assertEqual(textinput._flip, (False, True))
        # noinspection SpellCheckingInspection
        textinput.set_value('aaaaaaaaaaaaaaaaaaaaaaaaaa')
        self.assertEqual(textinput._cursor_position, 26)
        self.assertEqual(textinput._renderbox, [1, 26, 25])
        textinput.update(PygameEventUtils.key(pygame.K_BACKSPACE, keydown=True))
        self.assertEqual(textinput._cursor_position, 25)
        self.assertEqual(textinput._renderbox, [0, 25, 25])
        textinput.update(PygameEventUtils.key(pygame.K_a, keydown=True, char='a'))
        self.assertEqual(textinput._cursor_position, 26)
        self.assertEqual(textinput._renderbox, [1, 26, 25])
        textinput.update(PygameEventUtils.key(pygame.K_BACKSPACE, keydown=True))
        self.assertEqual(textinput._cursor_position, 25)
        self.assertEqual(textinput._renderbox, [0, 25, 25])

    # noinspection PyTypeChecker
    def test_textinput_underline(self) -> None:
        """
        Test underline.
        """
        # Test underline edge cases
        theme = TEST_THEME.copy()
        theme.widget_selection_effect = None
        theme.title_font_size = 35
        theme.widget_font_size = 25

        menu = pygame_menu.Menu(
            column_min_width=400,
            height=300,
            theme=theme,
            title='Label',
            onclose=pygame_menu.events.CLOSE,
            width=400
        )
        textinput = menu.add.text_input('title', input_underline='_')
        self.assertEqual(menu._widget_offset[1], 107 if PYGAME_V2 else 106)
        self.assertEqual(textinput.get_width(), 398)
        self.assertEqual(textinput._current_underline_string, '________________________________')
        menu.render()
        self.assertEqual((menu.get_width(widget=True), menu.get_width(inner=True)), (398, 400))
        self.assertEqual(textinput.get_width(), 398)
        self.assertEqual(textinput._current_underline_string, '________________________________')
        menu.render()
        self.assertEqual((menu.get_width(widget=True), menu.get_width(inner=True)), (398, 400))
        textinput.set_title('nice')
        self.assertEqual(textinput.get_width(), 401)
        self.assertEqual(textinput._current_underline_string, '________________________________')
        menu.render()
        self.assertEqual((menu.get_width(widget=True), menu.get_width(inner=True)), (401, 400))
        # noinspection SpellCheckingInspection
        textinput.set_value('QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ')
        self.assertEqual(textinput.get_width(), 731)
        self.assertEqual(textinput._current_underline_string,
                         '______________________________________________________________')
        menu.render()
        self.assertEqual((menu.get_width(widget=True), menu.get_width(inner=True)), (731, 400))
        textinput.set_padding(100)
        self.assertEqual(textinput.get_width(), 931)
        self.assertEqual(textinput._current_underline_string,
                         '______________________________________________________________')
        menu.render()
        self.assertEqual((menu.get_width(widget=True), menu.get_width(inner=True)), (931, 380))
        textinput.set_padding(200)
        self.assertEqual(textinput.get_width(), 1131)
        self.assertEqual(textinput._current_underline_string,
                         '______________________________________________________________')
        menu.render()
        self.assertEqual((menu.get_width(widget=True), menu.get_width(inner=True)), (1131, 380))

        # Test underline
        textinput = menu.add.text_input('title: ')
        textinput.set_value('this is a test value')
        self.assertEqual(textinput.get_width(), 266)

        menu.clear()
        textinput = menu.add.text_input('title: ', input_underline='.-')
        # noinspection SpellCheckingInspection
        textinput.set_value('QQQQQQQQQQQQQQQ')
        self.assertEqual(textinput.get_width(), 403)
        self.assertEqual(textinput._current_underline_string,
                         '.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')

        textinput = menu.add.text_input('title: ', input_underline='_', input_underline_len=10)
        self.assertEqual(textinput._current_underline_string, '_' * 10)

        # Text underline with different column widths
        menu = pygame_menu.Menu(
            column_max_width=200,
            height=300,
            theme=theme,
            title='Label',
            onclose=pygame_menu.events.CLOSE,
            width=400
        )
        self.assertRaises(pygame_menu.menu._MenuSizingException, lambda: menu.add.frame_v(300, 100))
        self.assertRaises(pygame_menu.menu._MenuSizingException, lambda: menu.add.frame_v(201, 100))
        self.assertEqual(len(menu._widgets), 0)
        textinput = menu.add.text_input('title', input_underline='_')
        self.assertEqual(menu._widget_offset[1], 107 if PYGAME_V2 else 106)
        self.assertEqual(textinput.get_width(), 200)
        self.assertEqual(textinput._current_underline_string, '______________')
        v_frame = menu.add.frame_v(150, 100, background_color=(20, 20, 20))
        v_frame.pack(textinput)
        self.assertEqual(menu._widget_offset[1], 76 if PYGAME_V2 else 75)
        self.assertEqual(textinput.get_width(), 145)
        self.assertEqual(textinput._current_underline_string, '_________')

        # Test cursor size
        self.assertRaises(AssertionError, lambda: menu.add.text_input('title', cursor_size=(1, 0)))
        self.assertRaises(AssertionError, lambda: menu.add.text_input('title', cursor_size=(-1, -1)))
        self.assertRaises(AssertionError, lambda: menu.add.text_input('title', cursor_size=(1, 1, 0)))
        self.assertRaises(AssertionError, lambda: menu.add.text_input('title', cursor_size=[1, 1]))
        self.assertRaises(AssertionError, lambda: menu.add.text_input('title', cursor_size=(1.6, 2.5)))

        textinput_cursor = menu.add.text_input('title', cursor_size=(10, 2))
        self.assertEqual(textinput_cursor._cursor_size, (10, 2))

    # noinspection PyArgumentEqualDefault,PyTypeChecker
    def test_colorinput(self) -> None:
        """
        Test ColorInput widget.
        """

        def _assert_invalid_color(widg) -> None:
            """
            Assert that the widget color is invalid.
            :param widg: Widget object
            """
            r, g, b = widg.get_value()
            self.assertEqual(r, -1)
            self.assertEqual(g, -1)
            self.assertEqual(b, -1)

        def _assert_color(widg, cr, cg, cb) -> None:
            """
            Assert that the widget color is invalid.
            :param widg: Widget object
            :param cr: Red channel, number between 0 and 255
            :param cg: Green channel, number between 0 and 255
            :param cb: Blue channel, number between 0 and 255
            """
            r, g, b = widg.get_value()
            self.assertEqual(r, cr)
            self.assertEqual(g, cg)
            self.assertEqual(b, cb)

        menu = MenuUtils.generic_menu(theme=TEST_THEME.copy())

        # Base rgb
        widget = menu.add.color_input('title', color_type='rgb', input_separator=',')
        widget.set_value((123, 234, 55))
        self.assertRaises(AssertionError, lambda: widget.set_value('0,0,0'))
        self.assertRaises(AssertionError, lambda: widget.set_value((255, 0,)))
        self.assertRaises(AssertionError, lambda: widget.set_value((255, 255, -255)))
        _assert_color(widget, 123, 234, 55)

        # Test separator
        widget = menu.add.color_input('color', color_type='rgb', input_separator='+')
        widget.set_value((34, 12, 12))
        self.assertEqual(widget._input_string, '34+12+12')
        self.assertRaises(AssertionError, lambda: menu.add.color_input('title', color_type='rgb', input_separator=''))
        self.assertRaises(AssertionError, lambda: menu.add.color_input('title', color_type='rgb', input_separator='  '))
        self.assertRaises(AssertionError, lambda: menu.add.color_input('title', color_type='unknown'))
        for i in range(10):
            self.assertRaises(AssertionError, lambda: menu.add.color_input('title', color_type='rgb', input_separator=str(i)))

        # Empty rgb
        widget = menu.add.color_input('color', color_type='rgb', input_separator=',')

        PygameEventUtils.test_widget_key_press(widget)
        self.assertEqual(widget._cursor_position, 0)
        widget.update(PygameEventUtils.key(pygame.K_RIGHT, keydown=True))
        self.assertEqual(widget._cursor_position, 0)
        _assert_invalid_color(widget)

        # Write sequence: 2 -> 25 -> 25, -> 25,0,
        # The comma after the zero must be automatically set
        self.assertFalse(widget.update(PygameEventUtils.key(0, keydown=True, testmode=False)))
        widget.update(PygameEventUtils.key(pygame.K_2, keydown=True, char='2'))
        widget.update(PygameEventUtils.key(pygame.K_5, keydown=True, char='5'))
        widget.update(PygameEventUtils.key(pygame.K_COMMA, keydown=True, char=','))
        self.assertEqual(widget._input_string, '25,')
        widget.update(PygameEventUtils.key(pygame.K_0, keydown=True, char='0'))
        self.assertEqual(widget._input_string, '25,0,')
        _assert_invalid_color(widget)

        # Now, sequence: 25,0,c -> 25c,0, with cursor c
        widget.update(PygameEventUtils.key(pygame.K_LEFT, keydown=True))
        widget.update(PygameEventUtils.key(pygame.K_LEFT, keydown=True))
        widget.update(PygameEventUtils.key(pygame.K_LEFT, keydown=True))
        self.assertEqual(widget._cursor_position, 2)

        # Sequence. 25,0, -> 255,0, -> 255,0, trying to write another 5 in the same position
        # That should be cancelled because 2555 > 255
        widget.update(PygameEventUtils.key(pygame.K_5, keydown=True, char='5'))
        self.assertEqual(widget._input_string, '255,0,')
        widget.update(PygameEventUtils.key(pygame.K_5, keydown=True, char='5'))
        self.assertEqual(widget._input_string, '255,0,')

        # Invalid left zeros, try to write 255,0, -> 255,00, but that should be disabled
        widget.update(PygameEventUtils.key(pygame.K_RIGHT, keydown=True))
        widget.update(PygameEventUtils.key(pygame.K_0, keydown=True, char='0'))
        self.assertEqual(widget._input_string, '255,0,')

        # Second comma cannot be deleted because there's a number between ,0,
        widget.update(PygameEventUtils.key(pygame.K_BACKSPACE, keydown=True))
        self.assertEqual(widget._input_string, '255,0,')
        widget.update(PygameEventUtils.key(pygame.K_LEFT, keydown=True))
        widget.update(PygameEventUtils.key(pygame.K_DELETE, keydown=True))
        self.assertEqual(widget._input_string, '255,0,')

        # Current cursor is at 255c,0,
        # Now right comma and 0 can be deleted
        widget.update(PygameEventUtils.key(pygame.K_END, keydown=True))
        widget.update(PygameEventUtils.key(pygame.K_BACKSPACE, keydown=True))
        widget.update(PygameEventUtils.key(pygame.K_BACKSPACE, keydown=True))
        self.assertEqual(widget._input_string, '255,')

        # Fill with zeros, then number with 2 consecutive 0 types must be 255,0,0
        # Commas should be inserted automatically
        widget.readonly = True
        widget.update(PygameEventUtils.key(pygame.K_0, keydown=True, char='0'))
        self.assertEqual(widget._input_string, '255,')
        widget.readonly = False
        widget.update(PygameEventUtils.key(pygame.K_0, keydown=True, char='0'))
        widget.update(PygameEventUtils.key(pygame.K_0, keydown=True, char='0'))
        self.assertEqual(widget._input_string, '255,0,0')
        _assert_color(widget, 255, 0, 0)

        # At this state, user cannot add more zeros at right
        for i in range(5):
            widget.update(PygameEventUtils.key(pygame.K_0, keydown=True, char='0'))
        self.assertEqual(widget._input_string, '255,0,0')
        widget.get_rect()

        widget.clear()
        self.assertEqual(widget._input_string, '')

        # Assert invalid defaults rgb
        self.assertRaises(AssertionError, lambda: menu.add.color_input('title', color_type='rgb', default=(255, 255,)))
        self.assertRaises(AssertionError, lambda: menu.add.color_input('title', color_type='rgb', default=(255, 255)))
        self.assertRaises(AssertionError, lambda: menu.add.color_input('title', color_type='rgb', default=(255, 255, 255, 255)))

        # Assert hex widget
        widget = menu.add.color_input('title', color_type='hex')
        self.assertEqual(widget._input_string, '#')
        self.assertEqual(widget._cursor_position, 1)
        _assert_invalid_color(widget)
        self.assertRaises(AssertionError, lambda: widget.set_value('#FF'))
        self.assertRaises(AssertionError, lambda: widget.set_value('#FFFFF<'))
        self.assertRaises(AssertionError, lambda: widget.set_value('#FFFFF'))
        self.assertRaises(AssertionError, lambda: widget.set_value('#F'))
        # noinspection SpellCheckingInspection
        self.assertRaises(AssertionError, lambda: widget.set_value('FFFFF'))
        self.assertRaises(AssertionError, lambda: widget.set_value('F'))
        widget.set_value('FF00FF')
        _assert_color(widget, 255, 0, 255)
        widget.set_value('#12FfAa')
        _assert_color(widget, 18, 255, 170)
        widget.set_value('   59C1e5')
        _assert_color(widget, 89, 193, 229)

        widget.render()
        widget.draw(surface)

        widget.clear()
        self.assertEqual(widget._input_string, '#')  # This cannot be empty
        self.assertEqual(widget._cursor_position, 1)

        # In hex widget # cannot be deleted
        widget.update(PygameEventUtils.key(pygame.K_BACKSPACE, keydown=True))
        self.assertEqual(widget._cursor_position, 1)
        widget.update(PygameEventUtils.key(pygame.K_LEFT, keydown=True))
        widget.update(PygameEventUtils.key(pygame.K_DELETE, keydown=True))
        self.assertEqual(widget._input_string, '#')
        widget.update(PygameEventUtils.key(pygame.K_END, keydown=True))
        for i in range(10):
            widget.update(PygameEventUtils.key(pygame.K_f, keydown=True, char='f'))
        self.assertEqual(widget._input_string, '#ffffff')
        _assert_color(widget, 255, 255, 255)

        # Test hex formats
        widget = menu.add.color_input('title', color_type='hex', hex_format='none')
        widget.set_value('#ff00ff')
        self.assertFalse(widget.update(PygameEventUtils.key(0, keydown=True, testmode=False)))
        self.assertEqual(widget.get_value(as_string=True), '#ff00ff')
        widget.set_value('#FF00ff')
        self.assertEqual(widget.get_value(as_string=True), '#FF00ff')

        widget = menu.add.color_input('title', color_type='hex', hex_format='lower')
        widget.set_value('#FF00ff')
        self.assertEqual(widget.get_value(as_string=True), '#ff00ff')
        widget.set_value('AABBcc')
        self.assertEqual(widget.get_value(as_string=True), '#aabbcc')

        widget = menu.add.color_input('title', color_type='hex', hex_format='upper')
        widget.set_value('#FF00ff')
        self.assertEqual(widget.get_value(as_string=True), '#FF00FF')
        widget.set_value('AABBcc')
        self.assertEqual(widget.get_value(as_string=True), '#AABBCC')

        # Test dynamic sizing
        widget = menu.add.color_input('title', color_type='hex', hex_format='upper', dynamic_width=True)
        self.assertEqual(widget.get_width(), 200)
        widget.set_value('#ffffff')
        width = 342 if PYGAME_V2 else 345
        self.assertEqual(widget.get_width(), width)
        widget.set_value(None)
        self.assertEqual(widget.get_width(), 200)
        self.assertEqual(widget.get_value(as_string=True), '#')
        widget.set_value('#ffffff')
        self.assertEqual(widget.get_width(), width)
        widget.update(PygameEventUtils.key(pygame.K_BACKSPACE, keydown=True))  # remove the last character, now color is invalid
        self.assertEqual(widget.get_value(as_string=True), '#FFFFF')  # is upper
        widget.render()
        self.assertEqual(widget.get_width(), 200)

        widget = menu.add.color_input('title', color_type='hex', hex_format='upper', dynamic_width=False)
        self.assertEqual(widget.get_width(), width)
        widget.set_value('#ffffff')
        self.assertEqual(widget.get_width(), width)

    def test_value(self) -> None:
        """
        Test textinput value.
        """
        menu = MenuUtils.generic_menu()

        test = ['']

        def onwidgetchange(m: 'pygame_menu.Menu', w: 'pygame_menu.widgets.Widget') -> None:
            """
            Callback executed if widget changes.
            """
            self.assertIn(w, m.get_widgets())
            test[0] = w.get_value()

        menu.set_onwidgetchange(onwidgetchange)

        # Text
        text = menu.add.text_input('title', 'value')
        self.assertEqual(test[0], '')
        self.assertEqual(text.get_value(), 'value')
        self.assertFalse(text.value_changed())
        text.set_value('new')
        self.assertEqual(text.get_value(), 'new')
        self.assertTrue(text.value_changed())
        text.reset_value()
        self.assertEqual(text.get_value(), 'value')
        self.assertFalse(text.value_changed())
        text.change()
        self.assertEqual(test[0], 'value')

        # Color
        color = menu.add.color_input('title', color_type='hex', hex_format='none')
        self.assertEqual(color._default_value, '')
        self.assertEqual(color.get_value(), (-1, -1, -1))
        self.assertFalse(color.value_changed())
        self.assertRaises(AssertionError, lambda: color.set_value((255, 0, 0)))
        color.set_value('ff0000')
        self.assertEqual(color.get_value(), (255, 0, 0))
        self.assertTrue(color.value_changed())
        color.reset_value()
        self.assertEqual(color.get_value(), (-1, -1, -1))
        self.assertFalse(color.value_changed())

        color = menu.add.color_input('title', color_type='hex', hex_format='none', default='#ff0000')
        self.assertEqual(color._default_value, '#ff0000')
        self.assertEqual(color.get_value(), (255, 0, 0))
        self.assertFalse(color.value_changed())
        color.set_value('#00ff00')
        self.assertEqual(color.get_value(), (0, 255, 0))
        self.assertTrue(color.value_changed())
        color.reset_value()
        self.assertEqual(color.get_value(), (255, 0, 0))
        self.assertFalse(color.value_changed())

    def test_empty_title(self) -> None:
        """
        Test empty title.
        """
        menu = MenuUtils.generic_menu()
        text = menu.add.text_input('')
        self.assertEqual(text.get_size(), (16, 49))

    def test_keyrepeat(self) -> None:
        """
        Test keyrepeat.
        """
        menu = MenuUtils.generic_menu(keyboard_ignore_nonphysical=False)

        e = PygameEventUtils.key(pygame.K_a, keydown=True, char='a')
        textinput_on = menu.add.text_input('On', repeat_keys=True)
        textinput_on.update(e)
        textinput_off = menu.add.text_input('Off', repeat_keys=False)
        textinput_off.update(e)

        # Test with time
        for i in range(5):
            sleep(0.5)
            textinput_on.update([])
            textinput_off.update([])
        self.assertGreater(len(textinput_on.get_value()), 1)
        self.assertEqual(len(textinput_off.get_value()), 1)
