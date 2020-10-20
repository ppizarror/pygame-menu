# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGETS
Test widgets.

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
from pygame_menu import locals as _locals
from pygame_menu.widgets import ScrollBar, Label
import sys


class WidgetsTest(unittest.TestCase):

    def setUp(self):
        """
        Setup sound engine.
        """
        self.menu = MenuUtils.generic_menu()

    def test_nonascii(self):
        """
        Test non-ascii.
        """
        m = MenuUtils.generic_menu(title=u'Ménu')
        m.clear()
        self.menu.add_button(0, pygame_menu.events.NONE)
        self.menu.add_button('Test', pygame_menu.events.NONE)
        self.menu.add_button(u'Menú', pygame_menu.events.NONE)
        self.menu.add_color_input(u'Cólor', 'rgb')
        self.menu.add_text_input(u'Téxt')
        self.menu.add_label(u'Téxt')
        if sys.version_info < (3, 0):
            self.assertRaises(Exception, lambda: self.menu.add_selector(u'Sélect', [('a', 'a')]))  # Strict
        self.menu.add_selector(u'Sélect'.encode('latin1'), [('a', 'a')])
        self.menu.enable()
        self.menu.draw(surface)

    def test_selector(self):
        """
        Test Selector widget.
        """
        selector = self.menu.add_selector('selector',
                                          [('1 - Easy', 'EASY'),
                                           ('2 - Medium', 'MEDIUM'),
                                           ('3 - Hard', 'HARD')],
                                          default=1)
        self.menu.enable()
        self.menu.draw(surface)

        selector.draw(surface)
        selector.selected = False
        selector.draw(surface)

        # Test events
        selector.update(PygameUtils.key(0, keydown=True, testmode=False))
        selector.update(PygameUtils.key(pygame_menu.controls.KEY_LEFT, keydown=True))
        selector.update(PygameUtils.key(pygame_menu.controls.KEY_RIGHT, keydown=True))
        selector.update(PygameUtils.key(pygame_menu.controls.KEY_APPLY, keydown=True))
        selector.update(PygameUtils.joy_key(pygame_menu.controls.JOY_LEFT))
        selector.update(PygameUtils.joy_key(pygame_menu.controls.JOY_RIGHT))
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
        self.assertEqual(selector.get_value()[1], 2)
        self.assertRaises(AssertionError, lambda: selector.set_value(bool))
        self.assertRaises(AssertionError, lambda: selector.set_value(200))
        selector.set_value(1)
        self.assertEqual(selector.get_value()[1], 1)
        self.assertEqual(selector.get_value()[0], '5 - Medium')

    # noinspection PyArgumentEqualDefault
    def test_colorinput(self):
        """
        Test ColorInput widget.
        """

        def _assert_invalid_color(_widget):
            """
            Assert that the widget color is invalid.
            :param _widget: Widget object
            """
            _r, _g, _b = _widget.get_value()
            self.assertEqual(_r, -1)
            self.assertEqual(_g, -1)
            self.assertEqual(_b, -1)

        def _assert_color(_widget, cr, cg, cb):
            """
            Assert that the widget color is invalid.
            :param _widget: Widget object
            :param cr: Red channel, number between 0 and 255
            :param cg: Green channel, number between 0 and 255
            :param cb: Blue channel, number between 0 and 255
            """
            _r, _g, _b = _widget.get_value()
            self.assertEqual(_r, cr)
            self.assertEqual(_g, cg)
            self.assertEqual(_b, cb)

        # Base rgb
        widget = self.menu.add_color_input('title', color_type='rgb', input_separator=',')
        widget.set_value((123, 234, 55))
        self.assertRaises(AssertionError,
                          lambda: widget.set_value('0,0,0'))
        self.assertRaises(AssertionError,
                          lambda: widget.set_value((255, 0,)))
        self.assertRaises(AssertionError,
                          lambda: widget.set_value((255, 255, -255)))
        _assert_color(widget, 123, 234, 55)

        # Test separator
        widget = self.menu.add_color_input('color', color_type='rgb', input_separator='+')
        widget.set_value((34, 12, 12))
        self.assertEqual(widget._input_string, '34+12+12')
        self.assertRaises(AssertionError,
                          lambda: self.menu.add_color_input('title', color_type='rgb', input_separator=''))
        self.assertRaises(AssertionError,
                          lambda: self.menu.add_color_input('title', color_type='rgb', input_separator='  '))
        self.assertRaises(AssertionError,
                          lambda: self.menu.add_color_input('title', color_type='unknown'))
        for i in range(10):
            self.assertRaises(AssertionError,
                              lambda: self.menu.add_color_input('title', color_type='rgb', input_separator=str(i)))

        # Empty rgb
        widget = self.menu.add_color_input('color', color_type='rgb', input_separator=',')

        PygameUtils.test_widget_key_press(widget)
        self.assertEqual(widget._cursor_position, 0)
        widget.update(PygameUtils.key(pygame.K_RIGHT, keydown=True))
        self.assertEqual(widget._cursor_position, 0)
        _assert_invalid_color(widget)

        # Write sequence: 2 -> 25 -> 25, -> 25,0,
        # The comma after the zero must be automatically set
        widget.update(PygameUtils.key(pygame.K_2, keydown=True, char='2'))
        widget.update(PygameUtils.key(pygame.K_5, keydown=True, char='5'))
        widget.update(PygameUtils.key(pygame.K_COMMA, keydown=True, char=','))
        self.assertEqual(widget._input_string, '25,')
        widget.update(PygameUtils.key(pygame.K_0, keydown=True, char='0'))
        self.assertEqual(widget._input_string, '25,0,')
        _assert_invalid_color(widget)

        # Now, sequence: 25,0,c -> 25c,0, with cursor c
        widget.update(PygameUtils.key(pygame.K_LEFT, keydown=True))
        widget.update(PygameUtils.key(pygame.K_LEFT, keydown=True))
        widget.update(PygameUtils.key(pygame.K_LEFT, keydown=True))
        self.assertEqual(widget._cursor_position, 2)

        # Sequence. 25,0, -> 255,0, -> 255,0, trying to write another 5 in the same position
        # That should be cancelled because 2555 > 255
        widget.update(PygameUtils.key(pygame.K_5, keydown=True, char='5'))
        self.assertEqual(widget._input_string, '255,0,')
        widget.update(PygameUtils.key(pygame.K_5, keydown=True, char='5'))
        self.assertEqual(widget._input_string, '255,0,')

        # Invalid left zeros, try to write 255,0, -> 255,00, but that should be disabled
        widget.update(PygameUtils.key(pygame.K_RIGHT, keydown=True))
        widget.update(PygameUtils.key(pygame.K_0, keydown=True, char='0'))
        self.assertEqual(widget._input_string, '255,0,')

        # Second comma cannot be deleted because there's a number between ,0,
        widget.update(PygameUtils.key(pygame.K_BACKSPACE, keydown=True))
        self.assertEqual(widget._input_string, '255,0,')
        widget.update(PygameUtils.key(pygame.K_LEFT, keydown=True))
        widget.update(PygameUtils.key(pygame.K_DELETE, keydown=True))
        self.assertEqual(widget._input_string, '255,0,')

        # Current cursor is at 255c,0,
        # Now right comma and 0 can be deleted
        widget.update(PygameUtils.key(pygame.K_END, keydown=True))
        widget.update(PygameUtils.key(pygame.K_BACKSPACE, keydown=True))
        widget.update(PygameUtils.key(pygame.K_BACKSPACE, keydown=True))
        self.assertEqual(widget._input_string, '255,')

        # Fill with zeros, then number with 2 consecutive 0 types must be 255,0,0
        # Commas should be inserted automatically
        widget.update(PygameUtils.key(pygame.K_0, keydown=True, char='0'))
        widget.update(PygameUtils.key(pygame.K_0, keydown=True, char='0'))
        self.assertEqual(widget._input_string, '255,0,0')
        _assert_color(widget, 255, 0, 0)

        # At this state, user cannot add more zeros at right
        for i in range(5):
            widget.update(PygameUtils.key(pygame.K_0, keydown=True, char='0'))
        self.assertEqual(widget._input_string, '255,0,0')
        widget._previsualize_color(surface)
        widget.get_rect()

        widget.clear()
        self.assertEqual(widget._input_string, '')

        # Assert invalid defaults rgb
        self.assertRaises(AssertionError,
                          lambda: self.menu.add_color_input('title', color_type='rgb', default=(255, 255,)))
        self.assertRaises(AssertionError,
                          lambda: self.menu.add_color_input('title', color_type='rgb', default=(255, 255)))
        self.assertRaises(AssertionError,
                          lambda: self.menu.add_color_input('title', color_type='rgb', default=(255, 255, 255, 255)))

        # Assert hex widget
        widget = self.menu.add_color_input('title', color_type='hex')
        self.assertEqual(widget._input_string, '#')
        self.assertEqual(widget._cursor_position, 1)
        _assert_invalid_color(widget)
        self.assertRaises(AssertionError,
                          lambda: widget.set_value('#FF'))
        self.assertRaises(AssertionError,
                          lambda: widget.set_value('#FFFFF<'))
        self.assertRaises(AssertionError,
                          lambda: widget.set_value('#FFFFF'))
        self.assertRaises(AssertionError,
                          lambda: widget.set_value('#F'))
        self.assertRaises(AssertionError,
                          lambda: widget.set_value('FFFFF'))
        self.assertRaises(AssertionError,
                          lambda: widget.set_value('F'))
        widget.set_value('FF00FF')
        _assert_color(widget, 255, 0, 255)
        widget.set_value('#12FfAa')
        _assert_color(widget, 18, 255, 170)
        widget.set_value('   59C1e5')
        _assert_color(widget, 89, 193, 229)
        widget.clear()
        self.assertEqual(widget._input_string, '#')  # This cannot be empty
        self.assertEqual(widget._cursor_position, 1)

        # In hex widget # cannot be deleted
        widget.update(PygameUtils.key(pygame.K_BACKSPACE, keydown=True))
        self.assertEqual(widget._cursor_position, 1)
        widget.update(PygameUtils.key(pygame.K_LEFT, keydown=True))
        widget.update(PygameUtils.key(pygame.K_DELETE, keydown=True))
        self.assertEqual(widget._input_string, '#')
        widget.update(PygameUtils.key(pygame.K_END, keydown=True))
        for i in range(10):
            widget.update(PygameUtils.key(pygame.K_f, keydown=True, char='f'))
        self.assertEqual(widget._input_string, '#ffffff')
        _assert_color(widget, 255, 255, 255)
        widget._previsualize_color(surface=None)

    def test_label(self):
        """
        Test label widget.
        """
        label = self.menu.add_label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod '
                                    'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, '
                                    'quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. '
                                    'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu '
                                    'fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in '
                                    'culpa qui officia deserunt mollit anim id est laborum.',
                                    max_char=33,
                                    margin=(3, 5),
                                    align=_locals.ALIGN_LEFT,
                                    selectable=False,
                                    font_size=3)  # type: list
        self.assertEqual(len(label), 15)
        _w = label[0]  # type: Label
        self.assertFalse(_w.is_selectable)
        self.assertEqual(_w.get_margin()[0], 3)
        self.assertEqual(_w.get_margin()[1], 5)
        self.assertEqual(_w.get_alignment(), _locals.ALIGN_LEFT)
        self.assertEqual(_w.get_font_info()['size'], 3)
        _w.draw(surface)
        self.assertFalse(_w.update([]))

    def test_textinput(self):
        """
        Test TextInput widget.
        """

        # Assert bad settings
        self.assertRaises(ValueError,
                          lambda: self.menu.add_text_input('title',
                                                           input_type=pygame_menu.locals.INPUT_FLOAT,
                                                           default='bad'))
        self.assertRaises(ValueError,  # Default and password cannot coexist
                          lambda: self.menu.add_text_input('title',
                                                           password=True,
                                                           default='bad'))

        # Create text input widget
        textinput = self.menu.add_text_input('title', input_underline='_')
        textinput.set_value('new_value')  # No error
        textinput.selected = False
        textinput.draw(surface)
        textinput.selected = True
        textinput.draw(surface)
        self.assertEqual(textinput.get_value(), 'new_value')
        textinput.clear()
        self.assertEqual(textinput.get_value(), '')

        passwordinput = self.menu.add_text_input('title', password=True, input_underline='_')
        self.assertRaises(ValueError,  # Password cannot be set
                          lambda: passwordinput.set_value('new_value'))
        passwordinput.set_value('')  # No error
        passwordinput.selected = False
        passwordinput.draw(surface)
        passwordinput.selected = True
        passwordinput.draw(surface)
        self.assertEqual(passwordinput.get_value(), '')
        passwordinput.clear()
        self.assertEqual(passwordinput.get_value(), '')

        # Create selection box
        string = 'the text'
        textinput._cursor_render = True
        textinput.set_value(string)
        textinput._select_all()
        self.assertEqual(textinput._get_selected_text(), 'the text')
        textinput.draw(surface)
        textinput._unselect_text()
        textinput.draw(surface)

        # Test maxchar and undo/redo
        textinput = self.menu.add_text_input('title',
                                             input_underline='_',
                                             maxchar=20)
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
        textinput._cut()
        self.assertEqual(textinput.get_value(), '')
        textinput._undo()
        self.assertEqual(textinput.get_value(), 'eater than the limit')

        # Test copy/paste
        textinput_nocopy = self.menu.add_text_input('title',
                                                    input_underline='_',
                                                    maxwidth=20,
                                                    copy_paste_enable=False)
        textinput_nocopy.set_value('this cannot be copied')
        textinput_nocopy._copy()
        textinput_nocopy._paste()
        textinput_nocopy._cut()

        # Assert events
        textinput.update(PygameUtils.key(0, keydown=True, testmode=False))
        PygameUtils.test_widget_key_press(textinput)
        textinput.update(PygameUtils.key(pygame_menu.controls.KEY_APPLY, keydown=True))
        textinput.update(PygameUtils.key(pygame.K_LSHIFT, keydown=True))
        textinput.clear()

        # Type
        textinput.update(PygameUtils.key(pygame.K_t, keydown=True, char='t'))
        textinput.update(PygameUtils.key(pygame.K_e, keydown=True, char='e'))
        textinput.update(PygameUtils.key(pygame.K_s, keydown=True, char='s'))
        textinput.update(PygameUtils.key(pygame.K_t, keydown=True, char='t'))

        # Keyup
        textinput.update(PygameUtils.key(pygame.K_a, keyup=True, char='a'))
        self.assertEqual(textinput.get_value(), 'test')  # The text we typed

        # Ctrl events
        textinput.update(PygameUtils.keydown_mod_ctrl(pygame.K_c))  # copy
        textinput.update(PygameUtils.keydown_mod_ctrl(pygame.K_v))  # paste
        textinput.update(PygameUtils.keydown_mod_ctrl(pygame.K_z))  # undo
        self.assertEqual(textinput.get_value(), 'tes')
        textinput.update(PygameUtils.keydown_mod_ctrl(pygame.K_y))  # redo
        self.assertEqual(textinput.get_value(), 'test')
        textinput.update(PygameUtils.keydown_mod_ctrl(pygame.K_x))  # cut
        self.assertEqual(textinput.get_value(), '')
        textinput.update(PygameUtils.keydown_mod_ctrl(pygame.K_z))  # undo
        self.assertEqual(textinput.get_value(), 'test')
        textinput.update(PygameUtils.keydown_mod_ctrl(pygame.K_y))  # redo
        self.assertEqual(textinput.get_value(), '')
        textinput.update(PygameUtils.keydown_mod_ctrl(pygame.K_z))  # undo
        self.assertEqual(textinput.get_value(), 'test')
        textinput.update(PygameUtils.keydown_mod_ctrl(pygame.K_a))  # select all

        # Test selection, if user selects all and types anything the selected
        # text must be destroyed
        textinput._unselect_text()
        self.assertEqual(textinput._get_selected_text(), '')
        textinput._select_all()
        self.assertEqual(textinput._get_selected_text(), 'test')
        textinput._unselect_text()
        self.assertEqual(textinput._get_selected_text(), '')
        textinput.update(PygameUtils.keydown_mod_ctrl(pygame.K_a))
        self.assertEqual(textinput._get_selected_text(), 'test')
        textinput.update(PygameUtils.key(pygame.K_t, keydown=True, char='t'))
        textinput.update(PygameUtils.key(pygame.K_ESCAPE, keydown=True))

        # Now the value must be t
        self.assertEqual(textinput._get_selected_text(), '')
        self.assertEqual(textinput.get_value(), 't')

        # Update mouse
        for i in range(50):
            textinput.update(PygameUtils.key(pygame.K_t, keydown=True, char='t'))
        textinput._update_cursor_mouse(50)
        textinput._cursor_render = True
        textinput._render_cursor()

    def test_vmargin(self):
        """
        Test vertical margin widget.
        """
        menu = MenuUtils.generic_menu()
        w = menu.add_vertical_margin(999)
        w._render()
        self.assertEqual(w.get_rect().width, 0)
        self.assertEqual(w.get_rect().height, 0)
        self.assertEqual(w.update([]), False)
        self.assertEqual(w._font_size, 0)
        self.assertEqual(w.get_margin()[0], 0)
        self.assertEqual(w.get_margin()[1], 999)
        w.draw(surface)

    # noinspection PyArgumentEqualDefault
    def test_scrollbar(self):
        """
        Test ScrollBar widget.
            """
        screen_size = surface.get_size()
        world = MenuUtils.get_large_surface()

        # Vertical right scrollbar
        thick = 80
        length = screen_size[1]
        world_range = (50, world.get_height())
        orientation = _locals.ORIENTATION_VERTICAL
        x, y = screen_size[0] - thick, 0

        sb = ScrollBar(length,
                       world_range,
                       '',
                       orientation,
                       slider_pad=2,
                       slider_color=(210, 120, 200),
                       page_ctrl_thick=thick,
                       page_ctrl_color=(235, 235, 230))

        sb.set_shadow(color=(245, 245, 245),
                      position=_locals.POSITION_SOUTHEAST,
                      offset=2)

        sb.set_position(x, y)

        self.assertEqual(sb.get_orientation(), _locals.ORIENTATION_VERTICAL)
        self.assertEqual(sb.get_minimum(), world_range[0])
        self.assertEqual(sb.get_maximum(), world_range[1])

        sb.set_value(80)
        self.assertAlmostEqual(sb.get_value(), 80, delta=2)  # Scaling delta

        sb.update(PygameUtils.mouse_click(x + thick / 2, y + 2, evtype=pygame.MOUSEBUTTONDOWN))
        self.assertEqual(sb.get_value(), 50)

        sb.set_page_step(length)
        self.assertAlmostEqual(sb.get_page_step(), length, delta=2)  # Scaling delta

        sb.draw(surface)
