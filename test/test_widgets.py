"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGETS
Test widgets.

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

__all__ = ['WidgetsTest']

import copy
import unittest

from test._utils import MenuUtils, surface, PygameUtils, test_reset_surface, TEST_THEME, PYGAME_V2

import pygame
import pygame_menu
from pygame_menu import locals as _locals
from pygame_menu.controls import KEY_LEFT, KEY_RIGHT, KEY_APPLY, JOY_RIGHT, JOY_LEFT
from pygame_menu.locals import ORIENTATION_VERTICAL
from pygame_menu.widgets import ScrollBar, Label, Button, MenuBar, NoneWidget, NoneSelection
from pygame_menu.widgets import MENUBAR_STYLE_ADAPTIVE, MENUBAR_STYLE_NONE, \
    MENUBAR_STYLE_SIMPLE, MENUBAR_STYLE_UNDERLINE, MENUBAR_STYLE_UNDERLINE_TITLE, \
    MENUBAR_STYLE_TITLE_ONLY, MENUBAR_STYLE_TITLE_ONLY_DIAGONAL


class WidgetsTest(unittest.TestCase):

    def setUp(self) -> None:
        """
        Setup widgets test.
        """
        test_reset_surface()

    def test_kwargs(self) -> None:
        """
        Test kwargs addition.
        """

        def function_kwargs(*args, **kwargs) -> None:
            """
            Button callback.
            """
            self.assertEqual(len(args), 0)
            kwargsk = list(kwargs.keys())
            self.assertEqual(kwargsk[0], 'test')
            self.assertEqual(kwargsk[1], 'widget')

        menu = MenuUtils.generic_menu()
        self.assertRaises(ValueError, lambda: menu.add.button('btn', function_kwargs, test=True))
        btn = menu.add.button('btn', function_kwargs, test=True, accept_kwargs=True, padding=10)
        self.assertEqual(len(btn._kwargs), 1)
        self.assertRaises(KeyError, lambda: btn.add_self_to_kwargs('test'))
        self.assertEqual(len(btn._kwargs), 1)
        btn.add_self_to_kwargs()
        self.assertEqual(len(btn._kwargs), 2)
        self.assertEqual(btn._kwargs['widget'], btn)
        btn.apply()

    def test_copy(self) -> None:
        """
        Test widget copy.
        """
        widget = pygame_menu.widgets.Widget()
        self.assertRaises(pygame_menu.widgets.core.widget._WidgetCopyException, lambda: copy.copy(widget))
        self.assertRaises(pygame_menu.widgets.core.widget._WidgetCopyException, lambda: copy.deepcopy(widget))

    def test_onselect(self) -> None:
        """
        Test onselect widgets.
        """
        menu = MenuUtils.generic_menu()
        test = [None]

        def on_select(selected, widget, _) -> None:
            """
            Callback.
            """
            if selected:
                test[0] = widget

        # Button
        self.assertIsNone(test[0])
        btn = menu.add.button('nice', onselect=on_select)  # The first to be selected
        self.assertEqual(test[0], btn)

        btn2 = menu.add.button('nice', onselect=on_select)
        self.assertEqual(test[0], btn)
        btn2.is_selectable = False
        btn2.select(update_menu=True)
        self.assertEqual(test[0], btn)
        btn2.is_selectable = True
        btn2.select(update_menu=True)
        self.assertEqual(test[0], btn2)

        # Color
        color = menu.add.color_input('nice', 'rgb', onselect=on_select)
        color.select(update_menu=True)
        self.assertEqual(test[0], color)

        # Image
        image = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES, onselect=on_select, font_color=(2, 9))
        image.select(update_menu=True)
        self.assertEqual(test[0], color)
        image.is_selectable = True
        image.select(update_menu=True)
        self.assertEqual(test[0], image)

        # Label
        label = menu.add.label('label', onselect=on_select)
        label.is_selectable = True
        label.select(update_menu=True)
        self.assertEqual(test[0], label)

        # None, it cannot be selected
        none = menu.add.none_widget()
        none.select(update_menu=True)
        self.assertEqual(test[0], label)

        # Selector
        selector = menu.add.selector('nice', ['nice', 'epic'], onselect=on_select)
        selector.select(update_menu=True)
        self.assertEqual(test[0], selector)

        # Textinput
        text = menu.add.text_input('nice', onselect=on_select)
        text.select(update_menu=True)
        self.assertEqual(test[0], text)

        # Vmargin
        vmargin = menu.add.vertical_margin(10)
        vmargin.select(update_menu=True)
        self.assertEqual(test[0], text)

    @staticmethod
    def test_nonascii() -> None:
        """
        Test non-ascii.
        """
        menu = MenuUtils.generic_menu()
        m = MenuUtils.generic_menu(title=u'Ménu')
        m.clear()
        menu.add.button('0', pygame_menu.events.NONE)
        menu.add.button('Test', pygame_menu.events.NONE)
        menu.add.button(u'Menú', pygame_menu.events.NONE)
        menu.add.color_input(u'Cólor', 'rgb')
        menu.add.text_input(u'Téxt')
        menu.add.label(u'Téxt')
        menu.add.selector(u'Sélect'.encode('latin1'), [('a', 'a')])
        menu.enable()
        menu.draw(surface)

    def test_background(self) -> None:
        """
        Test widget background.
        """
        menu = MenuUtils.generic_menu()
        w = menu.add.label('Text')
        w.set_background_color((255, 255, 255), (10, 10))
        w.draw(surface)
        self.assertEqual(w._background_inflate[0], 10)
        self.assertEqual(w._background_inflate[1], 10)
        w.set_background_color(pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES))
        w.draw(surface)

    def test_transform(self) -> None:
        """
        Transform widgets.
        """
        menu = MenuUtils.generic_menu()
        w = menu.add.label('Text')
        w.rotate(45)
        w.translate(10, 10)
        w.scale(1, 1)
        w.set_max_width(None)
        self.assertFalse(w._scale[0])  # Scaling is disabled
        w.scale(1.5, 1)
        self.assertTrue(w._scale[0])  # Scaling is enabled
        w.scale(1, 1)
        self.assertFalse(w._scale[0])
        w.resize(40, 40)
        self.assertTrue(w._scale[0])  # Scaling is enabled
        w.scale(1, 1)
        self.assertFalse(w._scale[0])
        w.flip(False, False)

        # Test all widgets
        widgs = [
            menu.add.button('e'),
            menu.add.selector('e', [('1', 2),
                                    ('The second', 2),
                                    ('The final mode', 3)]),
            menu.add.color_input('color', 'rgb'),
            menu.add.label('nice'),
            menu.add.image(pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)),
            menu.add.vertical_margin(10),
            menu.add.text_input('nice')
        ]
        for w in widgs:
            w.rotate(45)
            w.translate(10, 10)
            w.scale(1.5, 1.5)
            w.resize(10, 10)
            w.flip(True, True)
        menu.draw(surface)

        # If widget max width is enabled, disable scaling
        w = menu.add.label('Text')
        self.assertFalse(w._scale[0])  # Scaling is disabled
        w.scale(1.5, 1)
        self.assertTrue(w._scale[0])  # Scaling is enabled
        w.set_max_width(100)
        self.assertFalse(w._scale[0])

        # Translate
        w = menu.add.label('text')
        x, y = w.get_position()
        w.translate(10, 10)
        xt, yt = w.get_position()
        self.assertNotEqual(xt - x, 10)
        self.assertNotEqual(yt - y, 10)
        menu.render()
        xt, yt = w.get_position()
        self.assertEqual(xt - x, 10)
        self.assertEqual(yt - y, 10)

    def test_max_width_height(self) -> None:
        """
        Test widget max width/height.
        """
        label = Label('my label is really long yeah, it should be scalled in the width')
        label.set_font(pygame_menu.font.FONT_OPEN_SANS, 25, (255, 255, 255), (0, 0, 0),
                       (0, 0, 0), (0, 0, 0), (0, 0, 0))
        label.render()

        # The padding is zero, also the selection box and all transformations
        self.assertEqual(label.get_width(), 692)
        self.assertEqual(label.get_height(), 35)
        self.assertEqual(label.get_size()[0], 692)
        self.assertEqual(label.get_size()[1], 35)

        # Add padding, this will increase the width of the widget
        label.set_padding(54)
        self.assertEqual(label.get_width(), 800)

        # Apply scaling
        label.scale(0.5, 0.5)
        self.assertEqual(label.get_width(), 400)
        label.scale(0.5, 0.5)
        self.assertEqual(label.get_width(), 400)
        self.assertEqual(label.get_padding()[0], 26)
        self.assertEqual(label.get_padding(transformed=False)[0], 54)

        # Set size
        label.resize(450, 100)
        self.assertEqual(label.get_width(), 449)
        self.assertEqual(label.get_height(), 98)

        # Set size back
        label.scale(1, 1)
        label.set_padding(0)
        self.assertEqual(label.get_width(), 692)
        self.assertEqual(label.get_height(), 35)

        # Test max width
        label.scale(2, 2)
        label.set_padding(52)
        label.set_max_width(250)
        self.assertFalse(label._scale[0])  # max width disables scale
        self.assertEqual(label.get_width(), 249)
        self.assertEqual(label.get_height(), 35 + 52 * 2)

        # Apply the same, but this time height is scaled
        label.set_max_width(250, scale_height=True)
        self.assertEqual(label.get_height(), 104)

        # Set max height, this will disabled max width
        label.set_max_height(100)
        self.assertIsNone(label._max_width[0])
        self.assertEqual(label.get_height(), 99)

        # Scale, disable both max width and max height
        label.set_max_width(100)
        label.set_max_height(100)
        label.scale(1.5, 1.5)
        self.assertIsNone(label._max_width[0])
        self.assertIsNone(label._max_height[0])
        self.assertTrue(label._scale[0])

        # Set scale back
        label.scale(1, 1)
        label.set_padding(0)
        self.assertEqual(label.get_width(), 692)
        self.assertEqual(label.get_height(), 35)

    def test_visibility(self) -> None:
        """
        Test widget visibility.
        """
        menu = MenuUtils.generic_menu()
        w = menu.add.label('Text')
        lasthash = w._last_render_hash
        w.hide()
        self.assertFalse(w.is_visible())
        self.assertNotEqual(w._last_render_hash, lasthash)
        lasthash = w._last_render_hash
        w.show()
        self.assertTrue(w.is_visible())
        self.assertNotEqual(w._last_render_hash, lasthash)

        w = Button('title')
        menu.add.generic_widget(w)
        w.hide()

    def test_font(self) -> None:
        """
        Test widget font.
        """
        menu = MenuUtils.generic_menu()
        w = menu.add.label('Text')  # type: Label
        self.assertRaises(AssertionError, lambda: w.update_font({}))
        w.update_font({'color': (255, 0, 0)})

    def test_padding(self) -> None:
        """
        Test widget padding.
        """
        menu = MenuUtils.generic_menu()
        self.assertRaises(Exception, lambda: menu.add.button(0, pygame_menu.events.NONE, padding=-1))
        self.assertRaises(Exception, lambda: menu.add.button(0, pygame_menu.events.NONE, padding='a'))
        self.assertRaises(Exception,
                          lambda: menu.add.button(0, pygame_menu.events.NONE, padding=(0, 0, 0, 0, 0)))
        self.assertRaises(Exception,
                          lambda: menu.add.button(0, pygame_menu.events.NONE, padding=(0, 0, -1, 0)))
        self.assertRaises(Exception,
                          lambda: menu.add.button(0, pygame_menu.events.NONE, padding=(0, 0, 'a', 0)))

        w = menu.add.button(0, pygame_menu.events.NONE, padding=25)
        self.assertEqual(w.get_padding(), (25, 25, 25, 25))

        w = menu.add.button(0, pygame_menu.events.NONE, padding=(25, 50, 75, 100))
        self.assertEqual(w.get_padding(), (25, 50, 75, 100))

        w = menu.add.button(0, pygame_menu.events.NONE, padding=(25, 50))
        self.assertEqual(w.get_padding(), (25, 50, 25, 50))

        w = menu.add.button(0, pygame_menu.events.NONE, padding=(25, 75, 50))
        self.assertEqual(w.get_padding(), (25, 75, 50, 75))

    # noinspection PyTypeChecker
    def test_menubar(self) -> None:
        """
        Test menubar widget.
        """
        menu = MenuUtils.generic_menu()
        for mode in [MENUBAR_STYLE_ADAPTIVE, MENUBAR_STYLE_NONE, MENUBAR_STYLE_SIMPLE,
                     MENUBAR_STYLE_UNDERLINE, MENUBAR_STYLE_UNDERLINE_TITLE, MENUBAR_STYLE_TITLE_ONLY,
                     MENUBAR_STYLE_TITLE_ONLY_DIAGONAL]:
            mb = MenuBar('Menu', 500, (0, 0, 0), True, mode=mode)
            menu.add.generic_widget(mb)
        mb = MenuBar('Menu', 500, (0, 0, 0), True)
        mb.set_backbox_border_width(2)
        self.assertRaises(AssertionError, lambda: mb.set_backbox_border_width(1.5))
        self.assertRaises(AssertionError, lambda: mb.set_backbox_border_width(0))
        self.assertRaises(AssertionError, lambda: mb.set_backbox_border_width(-1))
        self.assertEqual(mb._backbox_border_width, 2)
        menu.draw(surface)
        menu.disable()

    # noinspection PyArgumentEqualDefault,PyTypeChecker
    def test_selector(self) -> None:
        """
        Test selector widget.
        """
        menu = MenuUtils.generic_menu()
        selector = menu.add.selector('selector',
                                     [('1 - Easy', 'EASY'),
                                      ('2 - Medium', 'MEDIUM'),
                                      ('3 - Hard', 'HARD')],
                                     default=1)
        menu.enable()
        menu.draw(surface)

        selector.draw(surface)
        selector._selected = False
        selector.draw(surface)

        # Test events
        selector.update(PygameUtils.key(0, keydown=True, testmode=False))
        selector.update(PygameUtils.key(KEY_LEFT, keydown=True))
        selector.update(PygameUtils.key(KEY_RIGHT, keydown=True))
        selector.update(PygameUtils.key(KEY_APPLY, keydown=True))
        selector.update(PygameUtils.joy_key(JOY_LEFT))
        selector.update(PygameUtils.joy_key(JOY_RIGHT))
        selector.update(PygameUtils.joy_motion(1, 0))
        selector.update(PygameUtils.joy_motion(-1, 0))
        click_pos = selector.get_rect(to_real_position=True, apply_padding=False).center
        selector.update(PygameUtils.mouse_click(click_pos[0], click_pos[1]))

        # Check left/right clicks
        self.assertEqual(selector.get_index(), 0)
        click_pos = selector.get_rect(to_real_position=True, apply_padding=False).midleft
        selector.update(PygameUtils.mouse_click(click_pos[0] + 150, click_pos[1]))
        self.assertEqual(selector.get_index(), 2)
        selector.update(PygameUtils.mouse_click(click_pos[0] + 150, click_pos[1]))
        self.assertEqual(selector.get_index(), 1)
        selector.update(PygameUtils.mouse_click(click_pos[0] + 150, click_pos[1]))
        self.assertEqual(selector.get_index(), 0)
        selector.update(PygameUtils.mouse_click(click_pos[0] + 250, click_pos[1]))
        self.assertEqual(selector.get_index(), 1)
        selector.update(PygameUtils.mouse_click(click_pos[0] + 250, click_pos[1]))
        self.assertEqual(selector.get_index(), 2)
        selector.update(PygameUtils.mouse_click(click_pos[0] + 250, click_pos[1]))
        self.assertEqual(selector.get_index(), 0)

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
        self.assertEqual(selector.get_value()[0][0], '5 - Medium')
        selector.update(PygameUtils.key(KEY_LEFT, keydown=True))
        self.assertEqual(selector.get_value()[0][0], '4 - Easy')
        selector.readonly = True
        selector.update(PygameUtils.key(KEY_LEFT, keydown=True))
        self.assertEqual(selector.get_value()[0][0], '4 - Easy')

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
        self.assertRaises(AssertionError,
                          lambda: widget.set_value('0,0,0'))
        self.assertRaises(AssertionError,
                          lambda: widget.set_value((255, 0,)))
        self.assertRaises(AssertionError,
                          lambda: widget.set_value((255, 255, -255)))
        _assert_color(widget, 123, 234, 55)

        # Test separator
        widget = menu.add.color_input('color', color_type='rgb', input_separator='+')
        widget.set_value((34, 12, 12))
        self.assertEqual(widget._input_string, '34+12+12')
        self.assertRaises(AssertionError,
                          lambda: menu.add.color_input('title', color_type='rgb', input_separator=''))
        self.assertRaises(AssertionError,
                          lambda: menu.add.color_input('title', color_type='rgb', input_separator='  '))
        self.assertRaises(AssertionError,
                          lambda: menu.add.color_input('title', color_type='unknown'))
        for i in range(10):
            self.assertRaises(AssertionError,
                              lambda: menu.add.color_input('title', color_type='rgb', input_separator=str(i)))

        # Empty rgb
        widget = menu.add.color_input('color', color_type='rgb', input_separator=',')

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
        widget.get_rect()

        widget.clear()
        self.assertEqual(widget._input_string, '')

        # Assert invalid defaults rgb
        self.assertRaises(AssertionError,
                          lambda: menu.add.color_input('title', color_type='rgb', default=(255, 255,)))
        self.assertRaises(AssertionError,
                          lambda: menu.add.color_input('title', color_type='rgb', default=(255, 255)))
        self.assertRaises(AssertionError,
                          lambda: menu.add.color_input('title', color_type='rgb', default=(255, 255, 255, 255)))

        # Assert hex widget
        widget = menu.add.color_input('title', color_type='hex')
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

        # Test hex formats
        widget = menu.add.color_input('title', color_type='hex', hex_format='none')
        widget.set_value('#ff00ff')
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
        width = 342
        if not PYGAME_V2:
            width = 345
        self.assertEqual(widget.get_width(), width)
        widget.set_value(None)
        self.assertEqual(widget.get_width(), 200)
        self.assertEqual(widget.get_value(as_string=True), '#')
        widget.set_value('#ffffff')
        self.assertEqual(widget.get_width(), width)
        widget.update(
            PygameUtils.key(pygame.K_BACKSPACE, keydown=True))  # remove the last character, now color is invalid
        self.assertEqual(widget.get_value(as_string=True), '#FFFFF')  # is upper
        self.assertEqual(widget.get_width(), 200)

        widget = menu.add.color_input('title', color_type='hex', hex_format='upper', dynamic_width=False)
        self.assertEqual(widget.get_width(), width)
        widget.set_value('#ffffff')
        self.assertEqual(widget.get_width(), width)

    def test_label(self) -> None:
        """
        Test label widget.
        """
        menu = MenuUtils.generic_menu()
        label = menu.add.label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod '
                               'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, '
                               'quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. '
                               'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu '
                               'fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in '
                               'culpa qui officia deserunt mollit anim id est laborum.',
                               max_char=33,
                               margin=(3, 5),
                               align=_locals.ALIGN_LEFT,
                               font_size=3)
        self.assertEqual(len(label), 15)
        w = label[0]
        self.assertFalse(w.is_selectable)
        self.assertEqual(w.get_margin()[0], 3)
        self.assertEqual(w.get_margin()[1], 5)
        self.assertEqual(w.get_alignment(), _locals.ALIGN_LEFT)
        self.assertEqual(w.get_font_info()['size'], 3)
        w.draw(surface)
        self.assertFalse(w.update([]))
        labeltext = ['Lorem ipsum dolor sit amet,', 'consectetur adipiscing elit, sed',
                     'do eiusmod tempor incididunt ut', 'labore et dolore magna aliqua. Ut',
                     'enim ad minim veniam, quis', 'nostrud exercitation ullamco',
                     'laboris nisi ut aliquip ex ea', 'commodo consequat. Duis aute',
                     'irure dolor in reprehenderit in', 'voluptate velit esse cillum',
                     'dolore eu fugiat nulla pariatur.', 'Excepteur sint occaecat cupidatat',
                     'non proident, sunt in culpa qui', 'officia deserunt mollit anim id',
                     'est laborum.']
        for i in range(len(label)):
            self.assertEqual(label[i].get_title(), labeltext[i])

        # Split label
        label = menu.add.label('This label should split.\nIn two lines')
        self.assertEqual(label[0].get_title(), 'This label should split.')
        self.assertEqual(label[1].get_title(), 'In two lines')

        # Split label, but also with maxchar enabled
        label = menu.add.label(
            'This label should split, this line is really long so it should split.\nThe second line', max_char=40)
        self.assertEqual(label[0].get_title(), 'This label should split, this line is')
        self.assertEqual(label[1].get_title(), 'really long so it should split.')
        self.assertEqual(label[2].get_title(), 'The second line')

        # Split label with -1 maxchar
        label = menu.add.label(
            'This label should split, this line is really long so it should split.\nThe second line', max_char=-1)
        self.assertEqual(label[0].get_title(), 'This label should split, this line is really')
        self.assertEqual(label[1].get_title(), 'long so it should split.')
        self.assertEqual(label[2].get_title(), 'The second line')

        # Add underline
        label = menu.add.label('nice')
        self.assertEqual(label._decorator._total_decor(), 0)
        label.add_underline((0, 0, 0), 1, 1, force_render=True)
        self.assertEqual(label._decorator._total_decor(), 1)

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

        passwordinput = menu.add.text_input('title', password=True, input_underline='_')
        self.assertRaises(ValueError,  # Password cannot be set
                          lambda: passwordinput.set_value('new_value'))
        passwordinput.set_value('')  # No error
        passwordinput._selected = False
        passwordinput.draw(surface)
        passwordinput.select(update_menu=True)
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
        textinput = menu.add.text_input('title',
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
        textinput_nocopy = menu.add.text_input('title',
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
        textinput.update(PygameUtils.key(KEY_APPLY, keydown=True))
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

        # Test readonly
        textinput.update(PygameUtils.key(pygame.K_t, keydown=True, char='k'))
        self.assertEqual(textinput.get_value(), 'tk')
        textinput.readonly = True
        textinput.update(PygameUtils.key(pygame.K_t, keydown=True, char='k'))
        self.assertEqual(textinput.get_value(), 'tk')
        textinput.readonly = False

        # Update mouse
        for i in range(50):
            textinput.update(PygameUtils.key(pygame.K_t, keydown=True, char='t'))
        textinput._update_cursor_mouse(50)
        textinput._cursor_render = True
        textinput._render_cursor()

        # Test underline edge cases
        theme = TEST_THEME.copy()
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
        width = 107
        if not PYGAME_V2:
            width = 106
        self.assertEqual(menu._widget_offset[1], width)
        self.assertEqual(textinput.get_width(), 376)
        self.assertEqual(textinput._current_underline_string, '______________________________')
        menu.render()
        self.assertEqual((menu.get_width(widget=True), menu.get_width(inner=True)), (376, 400))
        self.assertEqual(textinput.get_width(), 376)
        self.assertEqual(textinput._current_underline_string, '______________________________')
        menu.render()
        self.assertEqual((menu.get_width(widget=True), menu.get_width(inner=True)), (376, 400))
        textinput.set_title('nice')
        self.assertEqual(textinput.get_width(), 379)
        self.assertEqual(textinput._current_underline_string, '______________________________')
        menu.render()
        self.assertEqual((menu.get_width(widget=True), menu.get_width(inner=True)), (379, 400))
        textinput.set_value('QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ')
        self.assertEqual(textinput.get_width(), 712)
        self.assertEqual(textinput._current_underline_string,
                         '____________________________________________________________')
        menu.render()
        self.assertEqual((menu.get_width(widget=True), menu.get_width(inner=True)), (712, 400))
        textinput.set_padding(100)
        self.assertEqual(textinput.get_width(), 912)
        self.assertEqual(textinput._current_underline_string,
                         '____________________________________________________________')
        menu.render()
        self.assertEqual((menu.get_width(widget=True), menu.get_width(inner=True)), (912, 400))
        textinput.set_padding(200)
        self.assertEqual(textinput.get_width(), 1112)
        self.assertEqual(textinput._current_underline_string,
                         '____________________________________________________________')
        menu.render()
        self.assertEqual((menu.get_width(widget=True), menu.get_width(inner=True)), (1112, 380))

        # Test underline
        textinput = menu.add.text_input('title: ')
        textinput.set_value('this is a test value')
        self.assertEqual(textinput.get_width(), 266)

        menu.clear()
        textinput = menu.add.text_input('title: ', input_underline='.-')
        textinput.set_value('QQQQQQQQQQQQQQQ')
        self.assertEqual(textinput.get_width(), 373)
        self.assertEqual(textinput._current_underline_string, '.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')

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
        if not PYGAME_V2:
            self.assertEqual(menu._widget_offset[1], 106)
        else:
            self.assertEqual(menu._widget_offset[1], 107)
        self.assertEqual(textinput.get_width(), 178)
        self.assertEqual(textinput._current_underline_string, '____________')
        vframe = menu.add.frame_v(150, 100, background_color=(20, 20, 20))
        vframe.pack(textinput)
        if not PYGAME_V2:
            self.assertEqual(menu._widget_offset[1], 75)
        else:
            self.assertEqual(menu._widget_offset[1], 76)
        self.assertEqual(textinput.get_width(), 134)
        self.assertEqual(textinput._current_underline_string, '________')

    def test_button(self) -> None:
        """
        Test button widget.
        """
        menu = MenuUtils.generic_menu()
        menu2 = MenuUtils.generic_menu()

        # Valid
        def test() -> bool:
            """
            Callback.
            """
            return True

        # Invalid ones
        invalid = [
            bool,  # type
            object,  # object
            1,  # int
            'a',  # str
            True,  # bool
            _locals,  # module
            surface,  # pygame
            1.1,  # float
            menu.add.button('eee'),  # widget
            [1, 2, 3],  # list
            (1, 2, 3),  # tuple
            pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)  # baseimage
        ]
        for i in invalid:
            self.assertRaises(ValueError, lambda: menu.add.button('b1', i))

        # Valid
        valid = [
            menu2,
            test,
            pygame_menu.events.NONE,
            pygame_menu.events.PYGAME_QUIT,
            pygame_menu.events.PYGAME_WINDOWCLOSE,
            None,
            lambda: test(),
            None
        ]
        for v in valid:
            self.assertTrue(menu.add.button('b1', v) is not None)

        btn = menu.add.button('b1', menu2)
        for v in [menu, 1, bool, object, [1, 2, 3], (1, 2, 3)]:
            self.assertRaises(AssertionError, lambda: btn.update_callback(v))
        btn.update_callback(test)

        # Invalid recursive menu
        self.assertRaises(ValueError, lambda: menu.add.button('bt', menu))

        # Test callback
        test = [False]

        def callback(t=False) -> None:
            """
            Callback.
            """
            test[0] = t

        btn = Button('epic', t=True, onreturn=callback)
        btn.apply()
        self.assertTrue(test[0])
        test[0] = False

        def callback() -> None:
            """
            Callback.
            """
            test[0] = False

        btn = Button('epic', onreturn=callback)
        btn.apply()
        self.assertFalse(test[0])

        # Test with no kwargs
        def callback(**kwargs) -> None:
            """
            Callback.
            """
            self.assertEqual(len(kwargs.keys()), 0)

        btn = menu.add.button('epic', callback, accept_kwargs=False)
        btn.apply()

        # Test with kwargs
        def callback(**kwargs) -> None:
            """
            Callback.
            """
            self.assertEqual(len(kwargs.keys()), 1)
            self.assertTrue(kwargs.get('key', False))

        btn = Button('epic', onreturn=callback, key=True)
        btn.apply()
        btn = menu.add.button('epic', callback, accept_kwargs=True, key=True)
        btn.apply()

        # Test pygame events
        btn = menu.add.button('epic', pygame_menu.events.PYGAME_QUIT)
        self.assertEqual(btn._onreturn, menu._exit)
        btn = menu.add.button('epic', pygame_menu.events.PYGAME_WINDOWCLOSE)
        self.assertEqual(btn._onreturn, menu._exit)

        # Test None
        btn = menu.add.button('epic', pygame_menu.events.NONE)
        self.assertIsNone(btn._onreturn)
        btn = menu.add.button('epic')
        self.assertIsNone(btn._onreturn)

        # Test invalid kwarg
        self.assertRaises(ValueError, lambda: menu.add.button('epic', callback, key=True))

        # Remove button
        menu.remove_widget(btn)
        self.assertRaises(ValueError, lambda: menu.remove_widget(btn))

        # Test underline
        # Add underline
        btn = menu.add.button('epic', pygame_menu.events.NONE)
        self.assertEqual(btn._decorator._total_decor(), 0)
        btn.add_underline((0, 0, 0), 1, 1, force_render=True)
        self.assertEqual(btn._decorator._total_decor(), 1)

        # Test return fun
        def fun() -> str:
            """
            This should return "nice".
            """
            return 'nice'

        btn = menu.add.button('', fun)
        self.assertEqual(btn.apply(), 'nice')
        btn.readonly = True
        self.assertIsNone(btn.apply())

    def test_attributes(self) -> None:
        """
        Test widget attributes.
        """
        menu = MenuUtils.generic_menu()
        widget = menu.add.label('epic')
        self.assertFalse(widget.has_attribute('epic'))
        self.assertRaises(IndexError, lambda: widget.remove_attribute('epic'))
        widget.set_attribute('epic', True)
        self.assertTrue(widget.has_attribute('epic'))
        self.assertTrue(widget.get_attribute('epic'))
        widget.set_attribute('epic', False)
        self.assertFalse(widget.get_attribute('epic'))
        widget.remove_attribute('epic')
        self.assertFalse(widget.has_attribute('epic'))
        self.assertEqual(widget.get_attribute('epic', 420), 420)

    def test_draw_callback(self) -> None:
        """
        Test drawing callback.
        """
        menu = MenuUtils.generic_menu()

        def call(widget, _) -> None:
            """
            Callback.
            """
            widget.set_attribute('attr', True)

        btn = menu.add.button('btn')
        callid = btn.add_draw_callback(call)
        self.assertFalse(btn.get_attribute('attr', False))
        menu.draw(surface)
        self.assertTrue(btn.get_attribute('attr', False))
        btn.remove_draw_callback(callid)
        self.assertRaises(IndexError, lambda: btn.remove_draw_callback(callid))  # Already removed
        menu.disable()

    def test_update_callback(self) -> None:
        """
        Test update callback.
        """

        def update(widget, _) -> None:
            """
            Callback.
            """
            widget.set_attribute('attr', True)

        menu = MenuUtils.generic_menu(theme=TEST_THEME.copy())
        btn = menu.add.button('button', lambda: print('Clicked'))
        callid = btn.add_update_callback(update)
        self.assertFalse(btn.get_attribute('attr', False))
        click_pos = btn.get_rect(to_real_position=True).center
        deco = menu.get_decorator()
        test_draw_rects = True

        def drawrect() -> None:
            """
            Draw absolute rect on surface for testing purposes.
            """
            if not test_draw_rects:
                return
            surface.fill((0, 255, 0), btn.get_rect(to_real_position=True))

        deco.add_callable(drawrect, prev=False, pass_args=False)
        click_pos_absolute = btn.get_rect(to_absolute_position=True).center
        self.assertNotEqual(click_pos, click_pos_absolute)
        self.assertEqual(menu.get_scrollarea()._view_rect, menu.get_scrollarea().get_absolute_view_rect())
        self.assertEqual(btn.get_scrollarea(), menu.get_current().get_scrollarea())
        if PYGAME_V2:
            self.assertEqual(btn.get_rect(), pygame.Rect(253, 153, 94, 41))
            self.assertEqual(btn.get_rect(to_real_position=True), pygame.Rect(253, 308, 94, 41))
        else:
            self.assertEqual(btn.get_rect(), pygame.Rect(253, 152, 94, 42))
            self.assertEqual(btn.get_rect(to_real_position=True), pygame.Rect(253, 307, 94, 42))
        self.assertEqual(len(menu._widgets_scrollable), 0)
        self.assertEqual(len(menu.get_current()._widgets_scrollable), 0)
        btn.update(PygameUtils.mouse_click(click_pos[0], click_pos[1]))  # MOUSEBUTTONUP
        self.assertTrue(btn.get_attribute('attr', False))
        btn.set_attribute('attr', False)
        btn.remove_update_callback(callid)
        self.assertRaises(IndexError, lambda: btn.remove_update_callback(callid))
        self.assertFalse(btn.get_attribute('attr', False))
        btn.update(PygameUtils.mouse_click(click_pos[0], click_pos[1]))
        self.assertFalse(btn.get_attribute('attr', False))

        def update2(widget, _) -> None:
            """
            Callback.
            """
            widget.set_attribute('epic', 'bass')

        btn.add_update_callback(update2)
        self.assertFalse(btn.has_attribute('epic'))
        btn.draw(surface)
        self.assertFalse(btn.has_attribute('epic'))
        btn.update(PygameUtils.mouse_click(click_pos[0], click_pos[1]))
        self.assertTrue(btn.has_attribute('epic'))
        btn.remove_attribute('epic')
        self.assertRaises(IndexError, lambda: btn.remove_attribute('epic'))
        self.assertFalse(btn.has_attribute('epic'))

    def test_change_id(self) -> None:
        """
        Test widget id change.
        """
        menu = MenuUtils.generic_menu()
        menu.add.button('b1', button_id='id')
        w = menu.add.button('b1', button_id='other')
        self.assertRaises(IndexError, lambda: w.change_id('id'))
        w.change_id('id2')
        v = menu.add.vertical_margin(10, 'margin')
        self.assertEqual(menu.get_widget('margin'), v)
        self.assertRaises(IndexError, lambda: v.change_id('id2'))

    def test_vmargin(self) -> None:
        """
        Test vertical margin widget.
        """
        menu = MenuUtils.generic_menu()
        w = menu.add.vertical_margin(999)
        w._render()
        self.assertEqual(w.get_rect().width, 0)
        self.assertEqual(w.get_rect().height, 999)
        self.assertFalse(w.update([]))
        self.assertEqual(w._font_size, 0)
        self.assertEqual(w.get_margin(), (0, 0))
        w.draw(surface)

    def test_hmargin(self) -> None:
        """
        Test horizontal margin widget.
        """
        w = pygame_menu.widgets.HMargin(999)
        w._render()
        self.assertEqual(w.get_rect().width, 999)
        self.assertEqual(w.get_rect().height, 0)
        self.assertFalse(w.update([]))
        self.assertEqual(w._font_size, 0)
        self.assertEqual(w.get_margin(), (0, 0))
        w.draw(surface)

    def test_none(self) -> None:
        """
        Test none widget.
        """
        wid = NoneWidget()
        wid.change_id('none')
        self.assertEqual(wid.get_id(), 'none')

        wid.set_margin(9, 9)
        self.assertEqual(wid.get_margin(), (0, 0))

        wid.set_padding(9)
        self.assertEqual(wid.get_padding(), (0, 0, 0, 0))

        wid.set_background_color((1, 1, 1))
        wid._draw_background_color(surface)
        self.assertIsNone(wid._background_color)

        nosel = NoneSelection()
        wid.set_selection_effect(nosel)
        self.assertNotEqual(nosel, wid.get_selection_effect())

        wid.set_title('none')
        self.assertEqual(wid.get_title(), '')

        r = wid.get_rect(inflate=(10, 10))
        self.assertEqual(r.x, 0)
        self.assertEqual(r.y, 0)
        self.assertEqual(r.width, 0)
        self.assertEqual(r.height, 0)

        self.assertFalse(wid.is_selectable)
        self.assertTrue(wid.is_visible())

        wid.apply()
        wid.change()

        wid.set_font('myfont', 0, (1, 1, 1), (1, 1, 1), (1, 1, 1), (0, 0, 0), (0, 0, 0))
        wid.update_font({'name': ''})
        wid._apply_font()
        self.assertIsNone(wid._font)

        # Test font rendering
        surf = wid._render_string('nice', (1, 1, 1))
        self.assertEqual(surf.get_width(), 0)
        self.assertEqual(surf.get_height(), 0)

        wid._apply_transforms()

        wid.hide()
        self.assertFalse(wid.is_visible())
        wid.show()
        self.assertTrue(wid.is_visible())

        wid.set_value('epic')
        self.assertRaises(ValueError, lambda: wid.get_value())

        wid.remove_update_callback('none')
        wid.add_update_callback(None)
        wid.apply_update_callbacks()

        draw = [False]

        surf = wid.get_surface()
        self.assertEqual(surf.get_width(), 0)
        self.assertEqual(surf.get_height(), 0)

        # Apply transforms
        wid.set_position(1, 1)
        self.assertEqual(wid.get_position(), (0, 0))

        wid.translate(1, 1)
        self.assertEqual(wid.get_translate(), (0, 0))

        wid.rotate(10)
        self.assertEqual(wid._angle, 0)

        wid.resize(10, 10)
        self.assertFalse(wid._scale[0])
        self.assertEqual(wid._scale[1], 1)
        self.assertEqual(wid._scale[2], 1)

        wid.scale(100, 100)
        self.assertFalse(wid._scale[0])
        self.assertEqual(wid._scale[1], 1)
        self.assertEqual(wid._scale[2], 1)

        wid.flip(True, True)
        self.assertFalse(wid._flip[0])
        self.assertFalse(wid._flip[1])

        wid.set_max_width(100)
        self.assertIsNone(wid._max_width[0])

        wid.set_max_height(100)
        self.assertIsNone(wid._max_height[0])

        # Selection
        wid.select()
        self.assertFalse(wid.is_selected())
        self.assertFalse(wid.is_selectable)

        # noinspection PyUnusedLocal
        def _draw(*args) -> None:
            draw[0] = True

        drawid = wid.add_draw_callback(_draw)
        wid.draw(surface)
        self.assertTrue(draw[0])
        draw[0] = False
        wid.remove_draw_callback(drawid)
        wid.draw(surface)
        self.assertFalse(draw[0])

        # noinspection PyTypeChecker
        wid.set_sound(None)
        self.assertIsNotNone(wid._sound)

        wid.set_border(1, (0, 0, 0), (0, 0))
        self.assertEqual(wid._border_width, 0)
        self.assertEqual(wid.get_selected_time(), 0)

    def test_border(self) -> None:
        """
        Test widget border.
        """
        menu = MenuUtils.generic_menu()
        self.assertRaises(AssertionError, lambda: menu.add.button('', border_width=-1))
        self.assertRaises(AssertionError, lambda: menu.add.button('', border_width=1.5))
        self.assertRaises(AssertionError, lambda: menu.add.button('', border_width=1, border_color=(0, 0, 0),
                                                                  border_inflate=(-1, - 1)))
        btn = menu.add.button('', border_width=1, border_color=(0, 0, 0), border_inflate=(1, 1))
        self.assertEqual(btn._border_width, 1)
        self.assertEqual(btn._border_color, (0, 0, 0, 255))
        self.assertEqual(btn._border_inflate, (1, 1))

    def test_scrollbar(self) -> None:
        """
        Test ScrollBar widget.
        """
        screen_size = surface.get_size()
        world = MenuUtils.get_large_surface()

        # Vertical right scrollbar
        thick = 80
        length = screen_size[1]
        world_range = (50, world.get_height())
        x, y = screen_size[0] - thick, 0

        # noinspection PyArgumentEqualDefault
        sb = ScrollBar(
            length,
            world_range,
            '',
            ORIENTATION_VERTICAL,
            slider_pad=2,
            slider_color=(210, 120, 200),
            page_ctrl_thick=thick,
            page_ctrl_color=(235, 235, 230)
        )
        self.assertEqual(sb.get_thickness(), 80)

        sb.set_shadow(color=(245, 245, 245), position=_locals.POSITION_SOUTHEAST)
        self.assertFalse(sb._font_shadow)

        sb.set_position(x, y)

        self.assertEqual(sb.get_orientation(), ORIENTATION_VERTICAL)
        self.assertEqual(sb.get_minimum(), world_range[0])
        self.assertEqual(sb.get_maximum(), world_range[1])

        sb.set_value(80)
        self.assertAlmostEqual(sb.get_value(), 80, delta=2)  # Scaling delta

        sb.update(PygameUtils.mouse_click(x + thick / 2, y + 2, evtype=pygame.MOUSEBUTTONDOWN))
        self.assertEqual(sb.get_value(), 50)

        sb.set_page_step(length)
        self.assertAlmostEqual(sb.get_page_step(), length, delta=2)  # Scaling delta

        sb.draw(surface)

        # Test remove onreturn
        # noinspection PyArgumentEqualDefault
        sb = ScrollBar(length,
                       world_range,
                       '',
                       ORIENTATION_VERTICAL,
                       onreturn=-1
                       )
        self.assertIsNone(sb._onreturn)
        self.assertTrue(sb._kwargs.get('onreturn', 0))

        # Scrollbar ignores scaling
        sb.scale(2, 2)
        self.assertFalse(sb._scale[0])
        sb.resize(2, 2)
        self.assertFalse(sb._scale[0])
        sb.set_max_width(10)
        self.assertIsNone(sb._max_width[0])
        sb.set_max_height(10)
        self.assertIsNone(sb._max_height[0])
        sb._apply_font()
        sb.set_padding(10)
        self.assertEqual(sb._padding[0], 0)
        sb.rotate(10)
        self.assertEqual(sb._angle, 0)
        sb.flip(True, True)
        self.assertFalse(sb._flip[0])
        self.assertFalse(sb._flip[1])

        # Set minimum
        sb.set_minimum(0.5 * sb._values_range[1])

    # noinspection PyTypeChecker
    def test_toggleswitch(self) -> None:
        """
        Test toggleswitch widget.
        """
        menu = MenuUtils.generic_menu()

        value = [None]

        def onchange(val) -> None:
            """
            Function executed by toggle.
            """
            value[0] = val

        switch = menu.add.toggle_switch('toggle', False, onchange=onchange, infinite=False)
        self.assertFalse(switch.get_value())
        self.assertIsNone(value[0])
        switch.apply()
        self.assertFalse(value[0])

        switch.update(PygameUtils.key(KEY_LEFT, keydown=True))  # not infinite
        self.assertFalse(value[0])  # as this is false, dont change
        switch.update(PygameUtils.key(KEY_RIGHT, keydown=True))
        self.assertTrue(value[0])
        switch.update(PygameUtils.key(KEY_LEFT, keydown=True))
        self.assertFalse(value[0])
        switch.update(PygameUtils.key(KEY_LEFT, keydown=True))
        self.assertFalse(value[0])

        switch = menu.add.toggle_switch('toggle', False, onchange=onchange, infinite=True)
        switch.update(PygameUtils.key(KEY_LEFT, keydown=True))
        self.assertTrue(value[0])
        switch.update(PygameUtils.key(KEY_LEFT, keydown=True))
        self.assertFalse(value[0])

        # As there's only 2 states, return should change too
        switch.update(PygameUtils.key(KEY_APPLY, keydown=True))
        self.assertTrue(value[0])
        switch.update(PygameUtils.key(KEY_APPLY, keydown=True))
        self.assertFalse(value[0])

        # Check left/right clicks
        click_pos = switch.get_rect(to_real_position=True, apply_padding=False).midleft
        switch.update(PygameUtils.mouse_click(click_pos[0] + 150, click_pos[1]))
        self.assertFalse(value[0])
        switch.update(PygameUtils.mouse_click(click_pos[0] + 250, click_pos[1]))
        self.assertTrue(value[0])
        switch.update(PygameUtils.mouse_click(click_pos[0] + 150, click_pos[1]))
        self.assertFalse(value[0])

        # Test readonly
        switch.readonly = True
        switch.update(PygameUtils.key(KEY_APPLY, keydown=True))
        self.assertFalse(value[0])
        switch.update(PygameUtils.key(KEY_APPLY, keydown=True))
        self.assertFalse(value[0])
        switch.update(PygameUtils.key(KEY_APPLY, keydown=True))
        self.assertFalse(value[0])

        switch.readonly = False
        switch.update(PygameUtils.key(KEY_RIGHT, keydown=True))
        self.assertTrue(value[0])
        switch.update(PygameUtils.key(KEY_RIGHT, keydown=True))
        self.assertFalse(value[0])

        switch.draw(surface)

        # Test transforms
        switch.set_position(1, 1)
        self.assertEqual(switch.get_position(), (1, 1))

        switch.translate(1, 1)
        self.assertEqual(switch.get_translate(), (1, 1))

        switch.rotate(10)
        self.assertEqual(switch._angle, 0)

        switch.scale(100, 100)
        self.assertFalse(switch._scale[0])
        self.assertEqual(switch._scale[1], 1)
        self.assertEqual(switch._scale[2], 1)

        switch.resize(100, 100)
        self.assertFalse(switch._scale[0])
        self.assertEqual(switch._scale[1], 1)
        self.assertEqual(switch._scale[2], 1)

        switch.flip(True, True)
        self.assertFalse(switch._flip[0])
        self.assertFalse(switch._flip[1])

        switch.set_max_width(100)
        self.assertIsNone(switch._max_width[0])

        switch.set_max_height(100)
        self.assertIsNone(switch._max_height[0])

        # Assert switch values
        self.assertRaises(ValueError, lambda: menu.add.toggle_switch('toggle', 'false',
                                                                     onchange=onchange, infinite=False))
