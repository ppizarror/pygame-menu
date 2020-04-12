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
import pygame


class WidgetsTest(unittest.TestCase):

    def setUp(self):
        """
        Setup sound engine.
        """
        self.menu = PygameMenuUtils.generic_menu()
        self.menu.mainloop()

    def test_selector(self):
        """
        Test Selector widget.
        """
        selector = self.menu.add_selector('selector',
                                          [('1 - Easy', 'EASY'),
                                           ('2 - Medium', 'MEDIUM'),
                                           ('3 - Hard', 'HARD')],
                                          default=1)
        self.menu.draw()

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
        for i in range(10):
            self.assertRaises(AssertionError,
                              lambda: self.menu.add_color_input('title', color_type='rgb', input_separator=str(i)))

        # Empty rgb
        widget = self.menu.add_color_input('color', color_type='rgb', input_separator=',')

        widget.update(PygameUtils.key(pygame.K_BACKSPACE, keydown=True))
        widget.update(PygameUtils.key(pygame.K_DELETE, keydown=True))
        widget.update(PygameUtils.key(pygame.K_LEFT, keydown=True))
        widget.update(PygameUtils.key(pygame.K_RIGHT, keydown=True))
        widget.update(PygameUtils.key(pygame.K_END, keydown=True))
        widget.update(PygameUtils.key(pygame.K_HOME, keydown=True))
        self.assertEqual(widget._cursor_position, 0)
        widget.update(PygameUtils.key(pygame.K_RIGHT, keydown=True))
        self.assertEqual(widget._cursor_position, 0)
        _assert_invalid_color(widget)

        # Write secuence: 2 -> 25 -> 25, -> 25,0,
        # The comma after the zero must be atomatically setted
        widget.update(PygameUtils.key(pygame.K_2, keydown=True, char='2'))
        widget.update(PygameUtils.key(pygame.K_5, keydown=True, char='5'))
        widget.update(PygameUtils.key(pygame.K_COMMA, keydown=True, char=','))
        self.assertEqual(widget._input_string, '25,')
        widget.update(PygameUtils.key(pygame.K_0, keydown=True, char='0'))
        self.assertEqual(widget._input_string, '25,0,')
        _assert_invalid_color(widget)

        # Now, secuence: 25,0,c -> 25c,0, with cursor c
        widget.update(PygameUtils.key(pygame.K_LEFT, keydown=True))
        widget.update(PygameUtils.key(pygame.K_LEFT, keydown=True))
        widget.update(PygameUtils.key(pygame.K_LEFT, keydown=True))
        self.assertEqual(widget._cursor_position, 2)

        # Secuence. 25,0, -> 255,0, -> 255,0, trying to write another 5 in the same position
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

    def test_textinput(self):
        """
        Test TextInput widget.
        """

        # Assert bad settings
        self.assertRaises(ValueError,
                          lambda: self.menu.add_text_input('title',
                                                           input_type=pygameMenu.locals.INPUT_FLOAT,
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
        self.assertRaises(ValueError,  # Password cannot be setted
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

        textinput = self.menu.add_text_input('title',
                                             input_underline='_',
                                             maxwidth=20)
        textinput.set_value('the size of this textinput is way greater than the limit')
        textinput.draw(surface)
        textinput._copy()
        textinput._paste()
        textinput._cut()

        textinput_nocopy = self.menu.add_text_input('title',
                                                    input_underline='_',
                                                    maxwidth=20,
                                                    enable_copy_paste=False)
        textinput_nocopy.set_value('this cannot be copied')
        textinput_nocopy._copy()
        textinput_nocopy._paste()
        textinput_nocopy._cut()

        # Assert events
        textinput.update(PygameUtils.key(0, keydown=True, testmode=False))
        textinput.update(PygameUtils.key(pygame.K_BACKSPACE, keydown=True))
        textinput.update(PygameUtils.key(pygame.K_DELETE, keydown=True))
        textinput.update(PygameUtils.key(pygame.K_LEFT, keydown=True))
        textinput.update(PygameUtils.key(pygame.K_RIGHT, keydown=True))
        textinput.update(PygameUtils.key(pygame.K_END, keydown=True))
        textinput.update(PygameUtils.key(pygame.K_HOME, keydown=True))
        textinput.update(PygameUtils.key(pygameMenu.controls.KEY_APPLY, keydown=True))
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

        # Test selection, if user selects all and types anything the selected
        # text must be destroyed
        textinput._unselect_text()
        self.assertEqual(textinput._get_selected_text(), '')
        textinput._select_all()
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
