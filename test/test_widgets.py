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

from test._utils import MenuUtils, surface, PygameEventUtils, test_reset_surface, \
    TEST_THEME, PYGAME_V2, WINDOW_SIZE, THEME_NON_FIXED_TITLE
import copy
import unittest

import pygame
import pygame_menu

from pygame_menu.controls import KEY_LEFT, KEY_RIGHT, KEY_APPLY, JOY_RIGHT, JOY_LEFT, \
    KEY_MOVE_DOWN, KEY_MOVE_UP
from pygame_menu.locals import ORIENTATION_VERTICAL, FINGERDOWN, ALIGN_LEFT, \
    POSITION_SOUTHEAST, POSITION_NORTH, POSITION_SOUTH, POSITION_EAST, POSITION_WEST
from pygame_menu.widgets import MENUBAR_STYLE_ADAPTIVE, MENUBAR_STYLE_NONE, \
    MENUBAR_STYLE_SIMPLE, MENUBAR_STYLE_UNDERLINE, MENUBAR_STYLE_UNDERLINE_TITLE, \
    MENUBAR_STYLE_TITLE_ONLY, MENUBAR_STYLE_TITLE_ONLY_DIAGONAL
from pygame_menu.widgets import ScrollBar, Label, Button, MenuBar, NoneWidget, \
    NoneSelection


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
            kwargs_k = list(kwargs.keys())
            self.assertEqual(kwargs_k[0], 'test')
            self.assertEqual(kwargs_k[1], 'widget')

        menu = MenuUtils.generic_menu()
        self.assertRaises(ValueError, lambda: menu.add.button('btn', function_kwargs, test=True))
        btn = menu.add.button('btn', function_kwargs, test=True, accept_kwargs=True,
                              padding=10)
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
        self.assertRaises(pygame_menu.widgets.core.widget._WidgetCopyException,
                          lambda: copy.copy(widget))
        self.assertRaises(pygame_menu.widgets.core.widget._WidgetCopyException,
                          lambda: copy.deepcopy(widget))

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
        image = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
                               onselect=on_select, font_color=(2, 9))
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

    def test_non_ascii(self) -> None:
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
        text = menu.add.text_input(u'Téxt')
        menu.add.label(u'Téxt')
        menu.add.selector(u'Sélect'.encode('latin1'), [('a', 'a')])
        menu.enable()
        menu.draw(surface)

        # Text text input
        text.set_value('ą, ę, ś, ć, ż, ź, ó, ł, ń')
        self.assertEqual(text.get_value(), 'ą, ę, ś, ć, ż, ź, ó, ł, ń')
        text.set_value('')
        text.update(PygameEventUtils.key(pygame.K_l, char='ł', keydown=True))
        self.assertEqual(text.get_value(), 'ł')

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
        label = Label('my label is really long yeah, it should be scaled in the width')
        label.set_font(pygame_menu.font.FONT_OPEN_SANS, 25, (255, 255, 255), (0, 0, 0),
                       (0, 0, 0), (0, 0, 0), (0, 0, 0))
        label.render()

        # The padding is zero, also the selection box and all transformations
        self.assertEqual(label.get_width(), 686)
        self.assertEqual(label.get_height(), 35)
        self.assertEqual(label.get_size()[0], 686)
        self.assertEqual(label.get_size()[1], 35)

        # Add padding, this will increase the width of the widget
        label.set_padding(58)
        self.assertEqual(label.get_width(), 802)

        # Apply scaling
        label.scale(0.5, 0.5)
        self.assertEqual(label.get_width(), 401)
        label.scale(0.5, 0.5)
        self.assertEqual(label.get_width(), 401)
        self.assertEqual(label.get_padding()[0], 28)
        self.assertEqual(label.get_padding(transformed=False)[0], 58)

        # Set size
        label.resize(450, 100)
        self.assertEqual(label.get_width(), 448)
        self.assertEqual(label.get_height(), 99)

        # Set size back
        label.scale(1, 1)
        label.set_padding(0)
        self.assertEqual(label.get_width(), 686)
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
        self.assertEqual(label.get_height(), 113)

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
        self.assertEqual(label.get_width(), 686)
        self.assertEqual(label.get_height(), 35)

    def test_visibility(self) -> None:
        """
        Test widget visibility.
        """
        menu = MenuUtils.generic_menu()
        w = menu.add.label('Text')
        last_hash = w._last_render_hash
        w.hide()
        self.assertFalse(w.is_visible())
        self.assertNotEqual(w._last_render_hash, last_hash)
        last_hash = w._last_render_hash
        w.show()
        self.assertTrue(w.is_visible())
        self.assertNotEqual(w._last_render_hash, last_hash)

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
        self.assertRaises(Exception,
                          lambda: menu.add.button(0, pygame_menu.events.NONE, padding=-1))
        self.assertRaises(Exception,
                          lambda: menu.add.button(0, pygame_menu.events.NONE, padding='a'))
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

    # noinspection PyTypeChecker,PyArgumentEqualDefault
    def test_menubar(self) -> None:
        """
        Test menubar widget.
        """
        menu = MenuUtils.generic_menu()
        for mode in (MENUBAR_STYLE_ADAPTIVE, MENUBAR_STYLE_NONE, MENUBAR_STYLE_SIMPLE,
                     MENUBAR_STYLE_UNDERLINE, MENUBAR_STYLE_UNDERLINE_TITLE,
                     MENUBAR_STYLE_TITLE_ONLY, MENUBAR_STYLE_TITLE_ONLY_DIAGONAL):
            mb = MenuBar('Menu', 500, (0, 0, 0), back_box=True, mode=mode)
            menu.add.generic_widget(mb)
        mb = MenuBar('Menu', 500, (0, 0, 0), back_box=True)
        mb.set_backbox_border_width(2)
        self.assertRaises(AssertionError, lambda: mb.set_backbox_border_width(1.5))
        self.assertRaises(AssertionError, lambda: mb.set_backbox_border_width(0))
        self.assertRaises(AssertionError, lambda: mb.set_backbox_border_width(-1))
        self.assertEqual(mb._backbox_border_width, 2)
        menu.draw(surface)
        menu.disable()

        # Check margins
        mb = MenuBar('Menu', 500, (0, 0, 0), back_box=True, mode=MENUBAR_STYLE_ADAPTIVE)
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_SOUTH), (0, (0, 0)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_EAST), (0, (0, 0)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_WEST), (0, (0, 0)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_NORTH), (0, (0, 0)))

        # Test displacements
        theme = pygame_menu.themes.THEME_DEFAULT.copy()
        theme.title_bar_style = MENUBAR_STYLE_TITLE_ONLY
        menu = MenuUtils.generic_menu(theme=theme, title='my title')
        mb = menu.get_menubar()
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_SOUTH), (0, (0, 0)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_EAST), (0, (0, 0)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_WEST), (-55, (0, 55)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_NORTH), (0, (0, 55)))

        # Test with close button
        menu = MenuUtils.generic_menu(theme=theme, title='my title',
                                      onclose=pygame_menu.events.CLOSE)
        mb = menu.get_menubar()
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_SOUTH), (0, (0, 0)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_EAST), (-33, (0, 33)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_WEST), (-55, (0, 55)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_NORTH), (0, (0, 55)))

        # Hide the title, and check
        mb.hide()
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_SOUTH), (0, (0, 0)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_EAST), (0, (0, 0)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_WEST), (0, (0, 0)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_NORTH), (0, (0, 0)))

        mb.show()
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_SOUTH), (0, (0, 0)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_EAST), (-33, (0, 33)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_WEST), (-55, (0, 55)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_NORTH), (0, (0, 55)))

        # Floating
        mb.set_float(True)
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_SOUTH), (0, (0, 0)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_EAST), (0, (0, 0)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_WEST), (0, (0, 0)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_NORTH), (0, (0, 0)))

        mb.set_float(False)
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_SOUTH), (0, (0, 0)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_EAST), (-33, (0, 33)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_WEST), (-55, (0, 55)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_NORTH), (0, (0, 55)))

        # Fixed
        mb.fixed = False
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_SOUTH), (0, (0, 0)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_EAST), (0, (0, 0)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_WEST), (0, (0, 0)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_NORTH), (0, (0, 0)))

        # Test menubar
        self.assertFalse(mb.update(PygameEventUtils.middle_rect_click(mb._rect)))
        self.assertTrue(mb.update(PygameEventUtils.middle_rect_click(mb._backbox_rect)))
        self.assertFalse(mb.update(PygameEventUtils.middle_rect_click(mb._backbox_rect, evtype=pygame.MOUSEBUTTONDOWN)))
        self.assertTrue(mb.update(PygameEventUtils.joy_button(pygame_menu.controls.JOY_BUTTON_BACK)))

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
        selector.update(PygameEventUtils.key(0, keydown=True, testmode=False))
        selector.update(PygameEventUtils.key(KEY_LEFT, keydown=True))
        selector.update(PygameEventUtils.key(KEY_RIGHT, keydown=True))
        selector.update(PygameEventUtils.key(KEY_APPLY, keydown=True))
        selector.update(PygameEventUtils.joy_hat_motion(JOY_LEFT))
        selector.update(PygameEventUtils.joy_hat_motion(JOY_RIGHT))
        selector.update(PygameEventUtils.joy_motion(1, 0))
        selector.update(PygameEventUtils.joy_motion(-1, 0))
        click_pos = selector.get_rect(to_real_position=True, apply_padding=False).center
        selector.update(PygameEventUtils.mouse_click(click_pos[0], click_pos[1]))

        # Check left/right clicks
        self.assertEqual(selector.get_index(), 0)
        click_pos = selector.get_rect(to_real_position=True, apply_padding=False).midleft
        selector.update(PygameEventUtils.mouse_click(click_pos[0] + 150, click_pos[1]))
        self.assertEqual(selector.get_index(), 2)
        selector.update(PygameEventUtils.mouse_click(click_pos[0] + 150, click_pos[1]))
        self.assertEqual(selector.get_index(), 1)
        selector.update(PygameEventUtils.mouse_click(click_pos[0] + 150, click_pos[1]))
        self.assertEqual(selector.get_index(), 0)
        selector.update(PygameEventUtils.mouse_click(click_pos[0] + 250, click_pos[1]))
        self.assertEqual(selector.get_index(), 1)
        selector.update(PygameEventUtils.mouse_click(click_pos[0] + 250, click_pos[1]))
        self.assertEqual(selector.get_index(), 2)
        selector.update(PygameEventUtils.mouse_click(click_pos[0] + 250, click_pos[1]))
        self.assertEqual(selector.get_index(), 0)

        # Update elements
        new_elements = [('4 - Easy', 'EASY'),
                        ('5 - Medium', 'MEDIUM'),
                        ('6 - Hard', 'HARD')]
        selector.update_items(new_elements)
        selector.set_value('6 - Hard')
        self.assertEqual(selector.get_value()[1], 2)
        self.assertRaises(AssertionError, lambda: selector.set_value(bool))
        self.assertRaises(AssertionError, lambda: selector.set_value(200))
        selector.set_value(1)
        self.assertEqual(selector.get_value()[1], 1)
        self.assertEqual(selector.get_value()[0][0], '5 - Medium')
        selector.update(PygameEventUtils.key(KEY_LEFT, keydown=True))
        self.assertEqual(selector.get_value()[0][0], '4 - Easy')
        selector.readonly = True
        selector.update(PygameEventUtils.key(KEY_LEFT, keydown=True))
        self.assertEqual(selector.get_value()[0][0], '4 - Easy')

        # Test fancy selector
        menu.add.selector(
            'Fancy ',
            [('1 - Easy', 'EASY'),
             ('2 - Medium', 'MEDIUM'),
             ('3 - Hard', 'HARD')],
            default=1,
            style=pygame_menu.widgets.widget.selector.SELECTOR_STYLE_FANCY
        )

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

        PygameEventUtils.test_widget_key_press(widget)
        self.assertEqual(widget._cursor_position, 0)
        widget.update(PygameEventUtils.key(pygame.K_RIGHT, keydown=True))
        self.assertEqual(widget._cursor_position, 0)
        _assert_invalid_color(widget)

        # Write sequence: 2 -> 25 -> 25, -> 25,0,
        # The comma after the zero must be automatically set
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
        # noinspection SpellCheckingInspection
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
            PygameEventUtils.key(pygame.K_BACKSPACE, keydown=True))  # remove the last character, now color is invalid
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
        # noinspection SpellCheckingInspection
        label = menu.add.label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod '
                               'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, '
                               'quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. '
                               'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu '
                               'fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in '
                               'culpa qui officia deserunt mollit anim id est laborum.',
                               max_char=33,
                               margin=(3, 5),
                               align=ALIGN_LEFT,
                               font_size=3)
        self.assertEqual(len(label), 15)
        w = label[0]
        self.assertFalse(w.is_selectable)
        self.assertEqual(w.get_margin()[0], 3)
        self.assertEqual(w.get_margin()[1], 5)
        self.assertEqual(w.get_alignment(), ALIGN_LEFT)
        self.assertEqual(w.get_font_info()['size'], 3)
        w.draw(surface)
        self.assertFalse(w.update([]))
        # noinspection SpellCheckingInspection
        label_text = ['Lorem ipsum dolor sit amet,', 'consectetur adipiscing elit, sed',
                      'do eiusmod tempor incididunt ut', 'labore et dolore magna aliqua. Ut',
                      'enim ad minim veniam, quis', 'nostrud exercitation ullamco',
                      'laboris nisi ut aliquip ex ea', 'commodo consequat. Duis aute',
                      'irure dolor in reprehenderit in', 'voluptate velit esse cillum',
                      'dolore eu fugiat nulla pariatur.', 'Excepteur sint occaecat cupidatat',
                      'non proident, sunt in culpa qui', 'officia deserunt mollit anim id',
                      'est laborum.']
        for i in range(len(label)):
            self.assertEqual(label[i].get_title(), label_text[i])

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

        # Test generator
        gen_index = [-1]

        def generator() -> str:
            """
            Label generator.
            """
            s = ('a', 'b', 'c')
            gen_index[0] = (gen_index[0] + 1) % len(s)
            return s[gen_index[0]]

        self.assertNotIn(label, menu._update_widgets)
        label.set_title_generator(generator)
        self.assertIn(label, menu._update_widgets)
        self.assertEqual(label.get_title(), 'nice')
        label._render()
        self.assertEqual(label.get_title(), 'nice')
        label.render()
        self.assertEqual(label.get_title(), 'nice')

        label.update([])
        self.assertEqual(label.get_title(), 'a')
        label.update([])
        self.assertEqual(label.get_title(), 'b')
        label.update([])
        self.assertEqual(label.get_title(), 'c')
        label.update([])
        self.assertEqual(label.get_title(), 'a')

        # Update title with generator, it should raise a warning
        label.set_title('this should be overridden')

        label.set_title('this should be overridden 2')

        label.update([])
        self.assertEqual(label.get_title(), 'b')

        # Remove generator, it also should remove the widget from update
        label.set_title_generator(None)
        self.assertNotIn(label, menu._update_widgets)
        label.update([])
        self.assertEqual(label.get_title(), 'b')
        self.assertIsNone(label._title_generator)

    def test_clock(self) -> None:
        """
        Test clock.
        """
        menu = MenuUtils.generic_menu()
        clock = menu.add.clock()
        self.assertNotEqual(clock.get_title(), '')

        # Check title format
        self.assertRaises(AssertionError, lambda: menu.add.clock(title_format='bad'))

    # noinspection SpellCheckingInspection
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

        password_input = menu.add.text_input('title', password=True, input_underline='_')
        self.assertRaises(ValueError,  # Password cannot be set
                          lambda: password_input.set_value('new_value'))
        password_input.set_value('')  # No error
        password_input._selected = False
        password_input.draw(surface)
        password_input.select(update_menu=True)
        password_input.draw(surface)
        self.assertEqual(password_input.get_value(), '')
        password_input.clear()
        self.assertEqual(password_input.get_value(), '')

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
        textinput._block_copy_paste = False
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
        textinput_copy._cut()
        self.assertEqual(textinput_copy.get_value(), '')
        textinput_copy._block_copy_paste = False
        textinput_copy._paste()
        #  self.assertEqual(textinput_copy.get_value(), 'er than the max char')
        textinput_copy._cut()
        textinput_copy._block_copy_paste = False
        # self.assertEqual(textinput_copy.get_value(), '')
        textinput_copy._valid_chars = ['e', 'r']
        textinput_copy._paste()
        # noinspection SpellCheckingInspection
        # self.assertEqual(textinput_copy.get_value(), 'erer')

        # Assert events
        textinput.update(PygameEventUtils.key(0, keydown=True, testmode=False))
        PygameEventUtils.test_widget_key_press(textinput)
        textinput.update(PygameEventUtils.key(KEY_APPLY, keydown=True))
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
        textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_x))  # cut
        self.assertEqual(textinput.get_value(), '')
        textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_z))  # undo
        self.assertEqual(textinput.get_value(), 'test')
        textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_y))  # redo
        self.assertEqual(textinput.get_value(), '')
        textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_z))  # undo
        self.assertEqual(textinput.get_value(), 'test')

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
        textinput.update(PygameEventUtils.key(pygame.K_ESCAPE, keydown=True))

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

        # Test tab
        self.assertEqual(textinput._tab_size, 4)
        textinput.update(PygameEventUtils.key(pygame.K_TAB, keydown=True))
        self.assertEqual(textinput.get_value(), '±±    ')

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

        # Update mouse
        for i in range(50):
            textinput.update(PygameEventUtils.key(pygame.K_t, keydown=True, char='t'))
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
        self.assertEqual(menu._widget_offset[1], 107 if PYGAME_V2 else 106)
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
        # noinspection SpellCheckingInspection
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
        self.assertEqual((menu.get_width(widget=True), menu.get_width(inner=True)), (912, 380))
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
        # noinspection SpellCheckingInspection
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
        self.assertEqual(menu._widget_offset[1], 107 if PYGAME_V2 else 106)
        self.assertEqual(textinput.get_width(), 178)
        self.assertEqual(textinput._current_underline_string, '____________')
        v_frame = menu.add.frame_v(150, 100, background_color=(20, 20, 20))
        v_frame.pack(textinput)
        self.assertEqual(menu._widget_offset[1], 76 if PYGAME_V2 else 75)
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
            pygame,  # module
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
        call_id = btn.add_draw_callback(call)
        self.assertFalse(btn.get_attribute('attr', False))
        menu.draw(surface)
        self.assertTrue(btn.get_attribute('attr', False))
        btn.remove_draw_callback(call_id)
        self.assertRaises(IndexError, lambda: btn.remove_draw_callback(call_id))  # Already removed
        menu.disable()

    def test_update_callback(self) -> None:
        """
        Test update callback.
        """

        def update(event, widget, _) -> None:
            """
            Callback.
            """
            assert isinstance(event, list)
            widget.set_attribute('attr', True)

        menu = MenuUtils.generic_menu(theme=TEST_THEME.copy())
        btn = menu.add.button('button', lambda: print('Clicked'))
        call_id = btn.add_update_callback(update)
        self.assertFalse(btn.get_attribute('attr', False))
        click_pos = btn.get_rect(to_real_position=True).center
        deco = menu.get_decorator()
        test_draw_rects = True

        def draw_rect() -> None:
            """
            Draw absolute rect on surface for testing purposes.
            """
            if not test_draw_rects:
                return
            surface.fill((0, 255, 0), btn.get_rect(to_real_position=True))

        deco.add_callable(draw_rect, prev=False, pass_args=False)
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
        self.assertEqual(len(menu._update_frames), 0)
        self.assertEqual(len(menu.get_current()._update_frames), 0)
        btn.update(PygameEventUtils.mouse_click(click_pos[0], click_pos[1]))  # MOUSEBUTTONUP
        self.assertTrue(btn.get_attribute('attr', False))
        btn.set_attribute('attr', False)
        btn.remove_update_callback(call_id)
        self.assertRaises(IndexError, lambda: btn.remove_update_callback(call_id))
        self.assertFalse(btn.get_attribute('attr', False))
        btn.update(PygameEventUtils.mouse_click(click_pos[0], click_pos[1]))
        self.assertFalse(btn.get_attribute('attr', False))

        def update2(event, widget, _) -> None:
            """
            Callback.
            """
            assert isinstance(event, list)
            widget.set_attribute('epic', 'bass')

        btn.add_update_callback(update2)
        self.assertFalse(btn.has_attribute('epic'))
        btn.draw(surface)
        self.assertFalse(btn.has_attribute('epic'))
        btn.update(PygameEventUtils.mouse_click(click_pos[0], click_pos[1]))
        self.assertTrue(btn.has_attribute('epic'))
        btn.remove_attribute('epic')
        self.assertRaises(IndexError, lambda: btn.remove_attribute('epic'))
        self.assertFalse(btn.has_attribute('epic'))

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

        menu = MenuUtils.generic_menu()
        w = menu.add._horizontal_margin(999)
        self.assertEqual(w.get_rect().width, 999)
        self.assertEqual(w.get_rect().height, 0)

    def test_dropselect_multiple(self) -> None:
        """
        Test dropselect multiple widget.
        """
        theme = pygame_menu.themes.THEME_DEFAULT.copy()
        theme.widget_font_size = 25
        menu = MenuUtils.generic_menu(mouse_motion_selection=True, theme=theme)
        items = [('This is a really long selection item', 1), ('epic', 2)]
        for i in range(10):
            items.append(('item{}'.format(i + 1), i + 1))
        # noinspection SpellCheckingInspection
        drop = pygame_menu.widgets.DropSelectMultiple('dropsel', items, open_middle=True, selection_box_height=5)
        self.assertNotEqual(id(items), id(drop._items))
        menu.add.generic_widget(drop, configure_defaults=True)
        self.assertEqual(drop._selection_box_width, 225)
        drop.make_selection_drop()

        # Check drop is empty
        self.assertEqual(drop.get_value(), ([], []))
        self.assertEqual(drop.get_index(), [])
        self.assertEqual(drop._get_current_selected_text(), 'Select an option')

        # Check events
        self.assertFalse(drop.active)
        drop.update(PygameEventUtils.key(KEY_APPLY, keydown=True))
        self.assertTrue(drop.active)
        self.assertEqual(drop._index, -1)
        drop.update(PygameEventUtils.key(KEY_APPLY, keydown=True))  # Index is -1
        self.assertFalse(drop.active)
        drop.update(PygameEventUtils.key(KEY_APPLY, keydown=True))
        self.assertTrue(drop.active)
        drop.update(PygameEventUtils.key(KEY_MOVE_UP, keydown=True))
        self.assertEqual(drop._index, 0)
        drop.update(PygameEventUtils.key(KEY_MOVE_UP, keydown=True))
        self.assertEqual(drop._index, 1)

        # Apply on current
        drop.update(PygameEventUtils.key(KEY_APPLY, keydown=True))
        self.assertEqual(drop.get_value(), ([('epic', 2)], [1]))
        self.assertEqual(drop.get_index(), [1])
        self.assertEqual(drop._get_current_selected_text(), '1 selected')
        drop.update(PygameEventUtils.key(KEY_MOVE_UP, keydown=True))
        drop.update(PygameEventUtils.key(KEY_MOVE_UP, keydown=True))
        drop.update(PygameEventUtils.key(KEY_APPLY, keydown=True))
        self.assertEqual(drop.get_value(), ([('epic', 2), ('item2', 2)], [1, 3]))
        self.assertEqual(drop._get_current_selected_text(), '2 selected')

        # Click item 2, this should unselect
        self.assertTrue(drop.active)
        drop.update(PygameEventUtils.middle_rect_click(drop._option_buttons[3]))
        self.assertEqual(drop.get_value(), ([('epic', 2)], [1]))
        self.assertEqual(drop._get_current_selected_text(), '1 selected')
        drop.update(PygameEventUtils.key(KEY_MOVE_UP, keydown=True))
        self.assertEqual(drop._index, 4)
        drop.update(PygameEventUtils.key(KEY_APPLY, keydown=True))
        self.assertEqual(drop.get_value(), ([('epic', 2), ('item3', 3)], [1, 4]))
        self.assertEqual(drop._get_current_selected_text(), '2 selected')

        # Close
        drop.update(PygameEventUtils.key(pygame.K_ESCAPE, keydown=True))
        self.assertFalse(drop.active)
        self.assertEqual(drop.get_value(), ([('epic', 2), ('item3', 3)], [1, 4]))
        self.assertEqual(drop._get_current_selected_text(), '2 selected')

        # Set max limit
        drop._max_selected = 3
        self.assertEqual(drop.get_total_selected(), 2)
        drop.update(PygameEventUtils.key(KEY_APPLY, keydown=True))
        drop.update(PygameEventUtils.key(KEY_MOVE_UP, keydown=True))
        drop.update(PygameEventUtils.key(KEY_APPLY, keydown=True))
        self.assertEqual(drop.get_total_selected(), 3)
        self.assertTrue(drop.active)
        drop.update(PygameEventUtils.key(KEY_MOVE_UP, keydown=True))
        drop.update(PygameEventUtils.key(KEY_APPLY, keydown=True))
        self.assertEqual(drop.get_total_selected(), 3)  # Limit reached
        self.assertEqual(drop.get_value(), ([('epic', 2), ('item3', 3), ('item4', 4)], [1, 4, 5]))
        drop.update(PygameEventUtils.key(KEY_MOVE_DOWN, keydown=True))
        drop.update(PygameEventUtils.key(KEY_APPLY, keydown=True))  # Unselect previous
        self.assertEqual(drop.get_total_selected(), 2)  # Limit reached
        self.assertEqual(drop.get_value(), ([('epic', 2), ('item3', 3)], [1, 4]))

        # Update elements
        drop.update_items([('This is a really long selection item', 1), ('epic', 2)])
        self.assertEqual(drop.get_value(), ([], []))
        self.assertEqual(drop._get_current_selected_text(), 'Select an option')
        drop.set_value(1, process_index=True)
        self.assertEqual(drop.get_value(), ([('epic', 2)], [1]))
        drop.set_value('This is a really long selection item', process_index=True)
        self.assertEqual(drop.get_value(), ([('This is a really long selection item', 1), ('epic', 2)], [0, 1]))
        self.assertEqual(drop._get_current_selected_text(), '2 selected')
        drop.set_default_value(1)
        self.assertEqual(drop.get_value(), ([('epic', 2)], [1]))
        self.assertEqual(drop._get_current_selected_text(), '1 selected')
        drop.make_selection_drop()

        # Use manager
        drop2 = menu.add.dropselect_multiple('nice', [('This is a really long selection item', 1), ('epic', 2)],
                                             placeholder_selected='nice {0}', placeholder='epic', max_selected=1)
        self.assertEqual(drop2._selection_box_width, 134)
        self.assertEqual(drop2._get_current_selected_text(), 'epic')
        drop2.set_value('epic', process_index=True)
        self.assertEqual(drop2.get_index(), [1])
        self.assertEqual(drop2._get_current_selected_text(), 'nice 1')
        drop2.set_value(0, process_index=True)
        self.assertEqual(drop2.get_index(), [1])
        self.assertEqual(drop2._get_current_selected_text(), 'nice 1')
        self.assertEqual(drop2._default_value, [])
        self.assertEqual(drop2._index, 0)

        # Reset
        drop2.reset_value()
        self.assertEqual(drop2._get_current_selected_text(), 'epic')
        self.assertEqual(drop2._default_value, [])
        self.assertEqual(drop2._index, -1)
        self.assertEqual(drop2.get_index(), [])
        self.assertNotEqual(id(drop2._default_value), id(drop2._selected_indices))

        menu.select_widget(drop2)
        self.assertTrue(drop2.update(PygameEventUtils.key(pygame.K_TAB, keydown=True)))

        # Test hide
        self.assertTrue(drop2._drop_frame.is_visible())
        self.assertTrue(drop2.active)
        drop2.hide()  # Hiding selects the other widget
        self.assertEqual(menu.get_selected_widget(), drop)
        self.assertFalse(drop2._drop_frame.is_visible())
        self.assertFalse(drop2.active)
        drop2.show()
        self.assertFalse(drop2._drop_frame.is_visible())
        self.assertFalse(drop2.active)
        self.assertEqual(menu.get_selected_widget(), drop)
        menu.select_widget(drop2)
        drop2._toggle_drop()
        self.assertTrue(drop2.active)
        self.assertTrue(drop2._drop_frame.is_visible())

        # Test change
        test = [-1]

        def onchange(value) -> None:
            """
            Test onchange.
            """
            test[0] = value[1]

        drop2.set_onchange(onchange)

        # Pick any option
        menu.render()
        self.assertEqual(test, [-1])
        drop2._option_buttons[0].apply()
        self.assertEqual(test[0], [0])
        drop2._option_buttons[0].apply()
        self.assertEqual(test[0], [])
        drop2._option_buttons[0].apply()
        drop2._option_buttons[1].apply()
        self.assertEqual(test[0], [0])  # As max selected is only 1
        drop2._max_selected = 2
        drop2._option_buttons[1].apply()
        self.assertEqual(test[0], [0, 1])

    def test_dropselect(self) -> None:
        """
        Test dropselect widget.
        """
        menu = MenuUtils.generic_menu(mouse_motion_selection=True, theme=THEME_NON_FIXED_TITLE)
        items = [('This is a really long selection item', 1), ('epic', 2)]
        for i in range(10):
            items.append(('item{}'.format(i + 1), i + 1))
        # noinspection SpellCheckingInspection
        drop = pygame_menu.widgets.DropSelect('dropsel', items,
                                              selection_option_font_size=int(0.75 * menu._theme.widget_font_size),
                                              placeholder_add_to_selection_box=False)
        menu.add.generic_widget(drop, configure_defaults=True)
        self.assertEqual(drop._selection_box_width, 207 if PYGAME_V2 else 208)
        drop.make_selection_drop()
        self.assertEqual(drop.get_frame_depth(), 0)
        drop.render()
        self.assertTrue(drop._drop_frame.is_scrollable)
        drop_frame = drop._drop_frame

        self.assertIn(drop_frame, menu._update_frames)
        if PYGAME_V2:
            # noinspection SpellCheckingInspection
            self.assertEqual(menu._test_widgets_status(), (
                (('DropSelect-dropsel',
                  (0, 0, 0, 123, 149, 354, 49, 123, 304, 123, 149),
                  (1, 0, 1, 1, 0, 0, 0),
                  ('Frame',
                   (-1, -1, -1, 261, 193, 207, 136, 261, 348, 261, 193),
                   (0, 0, 0, 0, 1, 0, 0),
                   (-1, -1)),
                  ('Button-This is a really long selection item',
                   (-1, -1, -1, 0, -1, 356, 40, 261, 348, 0, 154),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-epic',
                   (-1, -1, -1, 0, 38, 356, 40, 261, 386, 0, 193),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-item1',
                   (-1, -1, -1, 0, 77, 356, 40, 261, 425, 0, 232),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-item2',
                   (-1, -1, -1, 0, 116, 356, 40, 261, 348, 0, 271),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-item3',
                   (-1, -1, -1, 0, 155, 356, 40, 261, 348, 0, 310),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-item4',
                   (-1, -1, -1, 0, 194, 356, 40, 261, 348, 0, 349),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-item5',
                   (-1, -1, -1, 0, 233, 356, 40, 261, 348, 0, 388),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-item6',
                   (-1, -1, -1, 0, 272, 356, 40, 261, 348, 0, 427),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-item7',
                   (-1, -1, -1, 0, 311, 356, 40, 261, 348, 0, 466),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-item8',
                   (-1, -1, -1, 0, 350, 356, 40, 261, 348, 0, 505),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-item9',
                   (-1, -1, -1, 0, 389, 356, 40, 261, 348, 0, 544),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-item10',
                   (-1, -1, -1, 0, 428, 356, 40, 261, 348, 0, 583),
                   (1, 0, 0, 0, 0, 1, 1))),)
            ))
        self.assertEqual(drop._drop_frame.get_attribute('height'), 135 if PYGAME_V2 else 138)
        self.assertEqual(drop._drop_frame.get_attribute('width'), 187 if PYGAME_V2 else 188)

        # Test events
        self.assertFalse(drop.active)
        self.assertFalse(drop._drop_frame.is_visible())
        drop.update(PygameEventUtils.key(KEY_APPLY, keydown=True))
        self.assertTrue(drop.active)
        self.assertTrue(drop._drop_frame.is_visible())
        self.assertEqual(drop.get_index(), -1)
        drop.update(PygameEventUtils.key(KEY_MOVE_UP, keydown=True))
        self.assertEqual(drop.get_index(), 0)
        self.assertTrue(drop.active)
        drop.update(PygameEventUtils.key(KEY_APPLY, keydown=True))
        self.assertFalse(drop.active)
        self.assertFalse(drop._drop_frame.is_visible())
        drop.update(PygameEventUtils.key(KEY_MOVE_DOWN, keydown=True))
        self.assertEqual(drop.get_index(), 0)
        self.assertFalse(drop.active)
        drop.update(PygameEventUtils.key(pygame.K_TAB, keydown=True))  # Enable
        self.assertTrue(drop.active)
        drop.update(PygameEventUtils.key(pygame.K_TAB, keydown=True))
        self.assertFalse(drop.active)
        drop.update(PygameEventUtils.key(pygame.K_TAB, keydown=True))  # Enable
        self.assertTrue(drop.active)
        drop.update(PygameEventUtils.key(KEY_MOVE_DOWN, keydown=True))  # Not infinite
        self.assertEqual(drop.get_index(), 0)
        scroll_values = [-1, 0, 0, 0.114, 0.228, 0.33, 0.447, 0.561, 0.664, 0.778, 0.895, 0.997]
        for i in range(1, 12):
            drop.update(PygameEventUtils.key(KEY_MOVE_UP, keydown=True))
            self.assertEqual(drop.get_index(), i)
            if PYGAME_V2:
                self.assertEqual(drop.get_scroll_value_percentage(ORIENTATION_VERTICAL),
                                 scroll_values[i])
        drop.update(PygameEventUtils.key(KEY_MOVE_UP, keydown=True))  # Not infinite
        self.assertEqual(drop.get_index(), 11)  # Not infinite
        if PYGAME_V2:
            self.assertEqual(drop.get_scroll_value_percentage(ORIENTATION_VERTICAL), 0.997)

        # Mouseup over rect returns True updated status
        self.assertTrue(drop.active)
        self.assertTrue(drop.update(PygameEventUtils.middle_rect_click(drop.get_focus_rect(),
                                                                       evtype=pygame.MOUSEBUTTONDOWN)))
        self.assertTrue(drop.active)

        # Touch also does the same trick
        if PYGAME_V2:
            drop._touchscreen_enabled = True
            self.assertTrue(drop.update(PygameEventUtils.middle_rect_click(drop.get_focus_rect(), menu=menu,
                                                                           evtype=FINGERDOWN)))
            self.assertTrue(drop.active)

        # Scroll to bottom and close, then open again, this should scroll to current selected
        drop.scrollh(0)
        drop.scrollv(0)
        self.assertEqual(drop._drop_frame.get_scroll_value_percentage(ORIENTATION_VERTICAL), 0)
        drop._toggle_drop()
        drop._toggle_drop()
        if PYGAME_V2:
            self.assertEqual(drop._drop_frame.get_scroll_value_percentage(ORIENTATION_VERTICAL), 0.997)

        # Click drop box should toggle it
        self.assertTrue(drop.active)
        drop.update(PygameEventUtils.middle_rect_click(drop))
        self.assertFalse(drop.active)
        drop.update(PygameEventUtils.middle_rect_click(drop))
        self.assertTrue(drop.active)

        # Click middle option
        drop.update(PygameEventUtils.middle_rect_click(drop.get_focus_rect()))
        self.assertEqual(drop.get_index(), 10)
        self.assertFalse(drop.active)

        # Test focus
        if not drop.active:
            drop.update(PygameEventUtils.key(KEY_APPLY, keydown=True))
        if PYGAME_V2:
            self.assertEqual(menu._draw_focus_widget(surface, drop),
                             {1: ((0, 0), (600, 0), (600, 307), (0, 307)),
                              2: ((0, 308), (260, 308), (260, 483), (0, 483)),
                              3: ((468, 308), (600, 308), (600, 483), (468, 483)),
                              4: ((0, 484), (600, 484), (600, 600), (0, 600))}
                             )
        else:
            self.assertEqual(menu._draw_focus_widget(surface, drop),
                             {1: ((0, 0), (600, 0), (600, 306), (0, 306)),
                              2: ((0, 307), (259, 307), (259, 486), (0, 486)),
                              3: ((468, 307), (600, 307), (600, 486), (468, 486)),
                              4: ((0, 487), (600, 487), (600, 600), (0, 600))}
                             )

        # Test change items
        drop.update_items([])
        self.assertRaises(pygame_menu.widgets.widget.dropselect._SelectionDropNotMakedException,
                          lambda: drop._check_drop_maked())
        drop.make_selection_drop()  # This selection drop is empty
        self.assertEqual(drop._drop_frame.get_attribute('height'), 0)
        self.assertEqual(drop._drop_frame.get_attribute('width'), 0)
        self.assertFalse(drop.active)
        drop._toggle_drop()
        self.assertFalse(drop.active)
        fr = drop.get_focus_rect()
        r = drop.get_rect(apply_padding=False, to_real_position=True)
        self.assertEqual(fr.x, r.x)
        self.assertEqual(fr.y, r.y)
        self.assertEqual(fr.width + drop._selection_box_border_width, r.width)
        self.assertEqual(fr.height, r.height)
        self.assertEqual(drop.get_index(), -1)
        self.assertRaises(ValueError, lambda: drop.get_value())
        drop._up()
        self.assertEqual(drop.get_index(), -1)
        drop._down()
        self.assertEqual(drop.get_index(), -1)

        # Check previous frame not in scrollable frames
        self.assertFalse(drop._drop_frame.is_scrollable)
        self.assertNotIn(drop_frame, menu._update_frames)

        # Restore previous values
        drop.update_items(items)
        drop.make_selection_drop()
        self.assertEqual(drop.get_index(), -1)

        # Apply transforms
        drop.translate(1, 1)
        self.assertEqual(drop.get_translate(), (1, 1))
        drop.translate(0, 0)

        drop.rotate(10)
        self.assertEqual(drop._angle, 0)

        drop.resize(10, 10)
        self.assertFalse(drop._scale[0])
        self.assertEqual(drop._scale[1], 1)
        self.assertEqual(drop._scale[2], 1)

        drop.scale(100, 100)
        self.assertFalse(drop._scale[0])
        self.assertEqual(drop._scale[1], 1)
        self.assertEqual(drop._scale[2], 1)

        drop.flip(True, True)
        self.assertFalse(drop._flip[0])
        self.assertFalse(drop._flip[1])

        drop.set_max_width(100)
        self.assertIsNone(drop._max_width[0])

        drop.set_max_height(100)
        self.assertIsNone(drop._max_height[0])
        self.assertFalse(drop.active)

        # Add margin
        vm = menu.add.vertical_margin(500)
        self.assertEqual(vm.get_height(), 500)

        # Add drop from widgetmanager, this has the placeholder button
        drop2 = menu.add.dropselect('drop2', items, dropselect_id='2', selection_infinite=True,
                                    selection_option_font_size=int(0.75 * menu._theme.widget_font_size))
        self.assertEqual(drop2._tab_size, menu._theme.widget_tab_size)
        for btn in drop2._option_buttons:
            self.assertEqual(btn._tab_size, menu._theme.widget_tab_size)
        self.assertEqual(drop2._drop_frame._tab_size, 4)
        self.assertEqual(drop2.get_id(), '2')
        self.assertEqual(menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_VERTICAL), 0)
        self.assertTrue(drop._open_bottom)
        self.assertFalse(drop2._open_bottom)

        # Move to bottom
        menu.get_scrollarea().scroll_to(ORIENTATION_VERTICAL, 1)
        menu.render()
        self.assertTrue(drop._open_bottom)
        self.assertFalse(drop2._open_bottom)
        menu.select_widget(drop2)
        drop2._toggle_drop()

        self.assertEqual(drop2.get_position(), (132, 554) if PYGAME_V2 else (131, 555))
        self.assertEqual(drop2._drop_frame.get_attribute('height'), 117 if PYGAME_V2 else 120)
        self.assertEqual(drop2._drop_frame.get_attribute('width'), 187 if PYGAME_V2 else 188)

        # Test infinite
        self.assertTrue(drop2.active)
        self.assertEqual(drop2.get_index(), -1)
        drop2._down()
        self.assertEqual(drop2.get_index(), 11)
        drop2.draw(surface)
        drop._index = -1
        drop2._up()
        self.assertEqual(drop2.get_index(), 0)
        drop2._up()
        self.assertEqual(drop2.get_index(), 1)
        drop2._down()
        self.assertEqual(drop2.get_index(), 0)
        drop2._down()
        self.assertEqual(drop2.get_index(), 11)
        drop2._up()
        self.assertEqual(drop2.get_index(), 0)
        drop2.set_value('item6')
        self.assertEqual(drop2.get_index(), 7)

        drop2.readonly = True
        drop2._up()
        self.assertEqual(drop2.get_index(), 7)
        drop2._down()
        self.assertEqual(drop2.get_index(), 7)
        drop2.readonly = False
        menu.render()
        self.assertEqual(drop2.get_scroll_value_percentage(ORIENTATION_VERTICAL), 0.606 if PYGAME_V2 else 0.603)
        drop2.reset_value()
        self.assertTrue(drop2.active)
        self.assertEqual(drop2.get_index(), -1)
        drop2.set_scrollarea(drop2.get_scrollarea())

        if PYGAME_V2:
            self.assertEqual(
                menu._draw_focus_widget(surface, drop2),
                {1: ((0, 0), (600, 0), (600, 338), (0, 338)),
                 2: ((0, 339), (239, 339), (239, 496), (0, 496)),
                 3: ((447, 339), (600, 339), (600, 496), (447, 496)),
                 4: ((0, 497), (600, 497), (600, 600), (0, 600))}
            )

        menu.draw(surface)
        self.assertIsNone(drop2.get_frame())
        self.assertEqual(drop2.last_surface, menu._widgets_surface)  # Outside frame, must be the widgets surface

        # Add drop inside frame
        f = menu.add.frame_v(400, 500, max_height=200, background_color=(0, 0, 255))
        f.pack(drop2)
        self.assertEqual(drop2.get_scrollarea(), f.get_scrollarea(inner=True))
        self.assertEqual(drop2._drop_frame.get_scrollarea(), f.get_scrollarea(inner=True))
        self.assertEqual(drop2.get_scrollarea().get_parent(), menu.get_scrollarea())
        self.assertEqual(drop2._drop_frame.get_scrollarea().get_parent(), menu.get_scrollarea())
        drop2.update_items([('optionA', 1), ('optionB', 2)])
        drop2.make_selection_drop()

        if PYGAME_V2:
            self.assertEqual(drop2._get_status(), (
                ('DropSelect-drop2',
                 (0, 2, 3, 0, 0, 332, 49, 88, 308, 0, -242),
                 (1, 0, 1, 1, 0, 1, 1),
                 ('Frame',
                  (-1, -1, -1, 116, 44, 207, 100, 204, 352, 116, -198),
                  (0, 0, 0, 0, 0, 1, 1),
                  (-1, -1)),
                 ('Button-optionA',
                  (-1, -1, -1, 116, 77, 207, 34, 204, 385, 116, -165),
                  (1, 0, 0, 0, 0, 1, 2)),
                 ('Button-optionB',
                  (-1, -1, -1, 116, 110, 207, 34, 204, 418, 116, -132),
                  (1, 0, 0, 0, 0, 1, 2)))
            ))
        self.assertEqual(drop2._drop_frame.get_attribute('height'), 100 if PYGAME_V2 else 103)
        self.assertEqual(drop2._drop_frame.get_attribute('width'), 207 if PYGAME_V2 else 208)
        self.assertEqual(drop2.get_scrollarea().get_parent_scroll_value_percentage(ORIENTATION_VERTICAL),
                         (0, 1))
        self.assertTrue(drop2._open_bottom)

        # Test onchange
        test = [-1, False]

        def test_change(item, v) -> None:
            """
            Test change.
            """
            assert item[0][1] == v
            test[0] = item[0][0]

        def test_apply(item, v) -> None:
            """
            Test apply.
            """
            assert item[0][1] == v
            test[1] = not test[1]

        drop2.set_onchange(test_change)
        drop2.set_onreturn(test_apply)
        drop2._toggle_drop()
        self.assertEqual(drop2.get_index(), -1)
        self.assertEqual(test[0], -1)
        drop2._up()
        self.assertEqual(test[0], 'optionA')
        drop2._up()
        self.assertEqual(test[0], 'optionB')
        drop2._up()
        self.assertEqual(test[0], 'optionA')
        self.assertFalse(test[1])
        drop2.update(PygameEventUtils.key(KEY_APPLY, keydown=True))  # Now it's closed
        self.assertTrue(test[1])
        self.assertFalse(drop2.active)
        drop2.update(PygameEventUtils.key(KEY_APPLY, keydown=True))  # This only opens but not apply
        self.assertTrue(test[1])
        self.assertTrue(drop2.active)
        menu.draw(surface)
        self.assertEqual(drop2.get_frame(), f)
        self.assertEqual(drop2.last_surface, f.get_surface())  # Frame surface as drop is not in middle
        drop2.update(PygameEventUtils.key(KEY_APPLY, keydown=True))  # Now applies
        self.assertFalse(test[1])
        self.assertFalse(drop2.active)

        # Unpack from frame
        f.unpack(drop2)
        self.assertTrue(drop2.is_floating())
        drop2.set_float(False)
        self.assertEqual(drop2._drop_frame.get_attribute('height'), 100 if PYGAME_V2 else 103)
        self.assertEqual(drop2._drop_frame.get_attribute('width'), 207 if PYGAME_V2 else 208)

        # Test close if mouse clicks outside
        menu.select_widget(drop)
        drop._toggle_drop()
        self.assertTrue(drop.active)
        drop.update(PygameEventUtils.mouse_click(0, 0))
        self.assertFalse(drop.active)

        # Set drop in middle
        if PYGAME_V2:
            self.assertEqual(drop._drop_frame.get_position(), (251, 45))
            self.assertEqual(drop.get_focus_rect(), pygame.Rect(121, 160, 337, 41))

        drop._open_middle = True
        menu.render()

        # For this test, hide all widgets except drop
        # for w in menu.get_widgets():
        #     w.hide()
        # drop.show()

        if PYGAME_V2:
            self.assertEqual(drop._drop_frame.get_position(), (196, 105))
            self.assertEqual(drop.get_focus_rect(), pygame.Rect(121, 160, 337, 41))

        scr = drop._drop_frame.get_scrollarea()
        sfr = drop._drop_frame.get_frame()

        # Add drop to frame
        f.pack(drop)
        menu.render()
        self.assertEqual(drop._drop_frame.get_scrollarea(), scr)
        self.assertEqual(drop._drop_frame.get_frame(), sfr)
        if PYGAME_V2:
            self.assertEqual(drop._drop_frame.get_position(), (196, 453))
            self.assertEqual(drop.get_focus_rect(), pygame.Rect(96, 312, 337, 41))
        self.assertFalse(drop.active)
        drop._toggle_drop()
        menu.render()
        menu.draw(surface)
        self.assertEqual(drop.last_surface, menu._widgets_surface)  # Menu surface as drop is in middle
        if PYGAME_V2:
            self.assertEqual(
                menu._draw_focus_widget(surface, drop),
                {1: ((0, 0), (600, 0), (600, 259), (0, 259)),
                 2: ((0, 260), (195, 260), (195, 394), (0, 394)),
                 3: ((403, 260), (600, 260), (600, 394), (403, 394)),
                 4: ((0, 395), (600, 395), (600, 600), (0, 600))}
            )
        drop._toggle_drop()

        drop2._open_middle = True
        menu.render()
        menu.select_widget(drop2)
        drop2._toggle_drop()
        menu.draw(surface)
        self.assertEqual(drop2.last_surface, menu._widgets_surface)
        if PYGAME_V2:
            self.assertEqual(drop2._drop_frame.get_position(), (196, 519))
            self.assertEqual(drop2.get_focus_rect(), pygame.Rect(196, 277, 207, 99))

        # Disable focus
        menu._mouse_motion_selection = False

        # As drop1 is scrollable, remove from menu, this should remove the widget too
        drop_frame = drop._drop_frame
        self.assertIn(drop_frame, menu._update_frames)
        menu.remove_widget(drop)
        self.assertNotIn(drop_frame, menu._update_frames)

        def draw_rect() -> None:
            """
            Draw absolute rect on surface for testing purposes.
            """
            # surface.fill((255, 0, 0), drop2.get_focus_rect())
            # surface.fill((0, 0, 255), drop2.get_scrollarea().get_absolute_view_rect())
            # surface.fill((255, 255, 0), drop2.get_scrollarea().get_absolute_view_rect().clip(drop.get_focus_rect()))
            return

        menu.get_decorator().add_callable(draw_rect, prev=False, pass_args=False)

        # Test active with different menu settings
        menu_theme = pygame_menu.themes.THEME_ORANGE.copy()
        menu_theme.title_fixed = False
        menu_theme.title_offset = (5, -2)
        menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        menu_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_LIGHT
        menu_theme.widget_font_size = 20

        menu2 = MenuUtils.generic_menu(theme=menu_theme, width=400)
        menu2.add_vertical_margin(1000)

        drop3 = menu2.add.dropselect_multiple(
            title='Pick 3 colors',
            items=[('Black', (0, 0, 0)),
                   ('Blue', (0, 0, 255)),
                   ('Cyan', (0, 255, 255)),
                   ('Fuchsia', (255, 0, 255)),
                   ('Green', (0, 255, 0)),
                   ('Red', (255, 0, 0)),
                   ('White', (255, 255, 255)),
                   ('Yellow', (255, 255, 0))],
            dropselect_multiple_id='pickcolors',
            open_middle=True,
            max_selected=3
        )
        self.assertEqual(drop3.get_focus_rect(), pygame.Rect(108, 468, 320, 28))

        # Translate the menu, this should also modify focus
        menu2.translate(100, 50)
        self.assertEqual(drop3.get_focus_rect(), pygame.Rect(108 + 100, 468 + 50, 320, 28))
        menu2.translate(100, 150)
        self.assertEqual(drop3.get_focus_rect(), pygame.Rect(108 + 100, 468 + 150, 320, 28))
        menu2.translate(0, 0)
        self.assertEqual(drop3.get_focus_rect(), pygame.Rect(108, 468, 320, 28))

    def test_none(self) -> None:
        """
        Test none widget.
        """
        wid = NoneWidget()

        wid.set_margin(9, 9)
        self.assertEqual(wid.get_margin(), (0, 0))

        wid.set_padding(9)
        self.assertEqual(wid.get_padding(), (0, 0, 0, 0))

        wid.set_background_color((1, 1, 1))
        wid._draw_background_color(surface)
        self.assertIsNone(wid._background_color)

        no_sel = NoneSelection()
        wid.set_selection_effect(no_sel)
        self.assertNotEqual(no_sel, wid.get_selection_effect())

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

        # noinspection SpellCheckingInspection
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

        draw_id = wid.add_draw_callback(_draw)
        wid.draw(surface)
        self.assertTrue(draw[0])
        draw[0] = False
        wid.remove_draw_callback(draw_id)
        wid.draw(surface)
        self.assertFalse(draw[0])

        # noinspection PyTypeChecker
        wid.set_sound(None)
        self.assertIsNotNone(wid._sound)

        wid.set_border(1, (0, 0, 0), (0, 0))
        self.assertEqual(wid._border_width, 0)
        self.assertEqual(wid.get_selected_time(), 0)

        # Test events
        def my_event() -> None:
            """
            Generic event object.
            """
            return

        wid.set_onchange(my_event)
        self.assertIsNone(wid._onchange)
        wid.set_onmouseover(my_event)
        self.assertIsNone(wid._onmouseover)
        wid.set_onmouseleave(my_event)
        self.assertIsNone(wid._onmouseleave)
        wid.set_onselect(my_event)
        self.assertIsNone(wid._onselect)
        wid.set_onreturn(my_event)
        self.assertIsNone(wid._onreturn)
        wid.mouseleave()
        wid.mouseover()
        wid._mouseover = True
        wid._check_mouseover()
        self.assertFalse(wid._mouseover)

        # Defaults
        wid.set_default_value(None)
        self.assertIsNotNone(wid._default_value)

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
        self.assertEqual(btn._border_position, pygame_menu.widgets.core.widget.WIDGET_BORDER_POSITION_FULL)

        # Test positioning
        btn._draw_border(surface)

        # Change border position
        self.assertRaises(AssertionError, lambda: btn.set_border(1, 'black', (1, 1), POSITION_SOUTHEAST))
        btn.set_border(1, 'black', (1, 1), POSITION_NORTH)
        btn._draw_border(surface)
        btn.set_border(1, 'black', (1, 1), POSITION_SOUTH)
        btn._draw_border(surface)
        btn.set_border(1, 'black', (1, 1), POSITION_EAST)
        btn._draw_border(surface)
        btn.set_border(1, 'black', (1, 1), POSITION_WEST)

        # Invalid
        btn._border_position = [POSITION_SOUTHEAST]
        self.assertRaises(RuntimeError, lambda: btn._draw_border(surface))

    def test_scrollbar(self) -> None:
        """
        Test ScrollBar widget.
        """
        screen_size = surface.get_size()
        world = pygame.Surface((WINDOW_SIZE[0] * 2, WINDOW_SIZE[1] * 3))
        world.fill((200, 200, 200))
        for x in range(100, world.get_width(), 200):
            for y in range(100, world.get_height(), 200):
                pygame.draw.circle(world, (225, 34, 43), (x, y), 100, 10)

        # Vertical right scrollbar
        thick = 80
        length = screen_size[1]
        world_range = (50, world.get_height())
        x, y = screen_size[0] - thick, 0

        sb = ScrollBar(
            length, world_range, 'sb2', ORIENTATION_VERTICAL,
            slider_pad=2,
            slider_color=(210, 120, 200),
            page_ctrl_thick=thick,
            page_ctrl_color=(235, 235, 230)
        )
        self.assertEqual(sb.get_thickness(), 80)
        self.assertIsNone(sb.get_scrollarea())

        sb.set_shadow(color=(245, 245, 245), position=POSITION_SOUTHEAST)
        self.assertFalse(sb._font_shadow)

        sb.set_position(x, y)

        self.assertEqual(sb._orientation, 1)
        self.assertEqual(sb.get_orientation(), ORIENTATION_VERTICAL)
        self.assertEqual(sb.get_minimum(), world_range[0])
        self.assertEqual(sb.get_maximum(), world_range[1])

        sb.set_value(80)
        self.assertAlmostEqual(sb.get_value(), 80, delta=2)  # Scaling delta

        sb.update(PygameEventUtils.mouse_click(x + thick / 2, y + 2, evtype=pygame.MOUSEBUTTONDOWN))
        self.assertEqual(sb.get_value(), 50)
        self.assertEqual(sb.get_value_percentage(), 0)

        sb.set_page_step(length)
        self.assertAlmostEqual(sb.get_page_step(), length, delta=2)  # Scaling delta

        sb.draw(surface)

        # Test events
        sb.update(PygameEventUtils.key(pygame.K_PAGEDOWN, keydown=True))
        self.assertEqual(sb.get_value(), 964)
        sb.update(PygameEventUtils.key(pygame.K_PAGEUP, keydown=True))
        self.assertEqual(sb.get_value(), 50)
        self.assertEqual(sb._last_mouse_pos, (-1, -1))
        sb.update(PygameEventUtils.enter_window())
        self.assertEqual(sb._last_mouse_pos, (-1, -1))
        sb.update(PygameEventUtils.leave_window())
        self.assertEqual(sb._last_mouse_pos, pygame.mouse.get_pos())
        self.assertFalse(sb.scrolling)
        sb.update(PygameEventUtils.middle_rect_click(sb.get_slider_rect(), evtype=pygame.MOUSEBUTTONDOWN))
        self.assertTrue(sb.scrolling)
        sb.update(PygameEventUtils.mouse_click(1, 1))
        self.assertFalse(sb.scrolling)
        self.assertEqual(sb.get_value(), 50)
        sb.update(PygameEventUtils.middle_rect_click(sb.get_rect(to_absolute_position=True),
                                                     evtype=pygame.MOUSEBUTTONDOWN))
        self.assertEqual(sb.get_value(), 964)
        sb.update(PygameEventUtils.middle_rect_click(sb.get_slider_rect(), evtype=pygame.MOUSEBUTTONDOWN))
        self.assertTrue(sb.scrolling)
        sb.update(PygameEventUtils.middle_rect_click(sb.get_slider_rect(), button=4,
                                                     evtype=pygame.MOUSEBUTTONDOWN))
        self.assertEqual(sb.get_value(), 875)
        sb.update(PygameEventUtils.middle_rect_click(sb.get_slider_rect(), button=5,
                                                     evtype=pygame.MOUSEBUTTONDOWN))
        self.assertEqual(sb.get_value(), 964)
        self.assertEqual(sb.get_value_percentage(), 0.522)

        # Test mouse motion while scrolling
        sb.update(PygameEventUtils.middle_rect_click(sb.get_slider_rect(), button=5, delta=(0, 50), rel=(0, 10),
                                                     evtype=pygame.MOUSEMOTION))
        self.assertEqual(sb.get_value_percentage(), 0.547)
        sb.update(PygameEventUtils.middle_rect_click(sb.get_slider_rect(), button=5, delta=(0, 50), rel=(0, -10),
                                                     evtype=pygame.MOUSEMOTION))
        self.assertEqual(sb.get_value_percentage(), 0.522)
        sb.update(PygameEventUtils.middle_rect_click(sb.get_slider_rect(), button=5, delta=(0, 50), rel=(0, 999),
                                                     evtype=pygame.MOUSEMOTION))
        self.assertEqual(sb.get_value_percentage(), 1)

        # Ignore events if mouse outside the region
        sb.update(PygameEventUtils.middle_rect_click(sb.get_slider_rect(), button=5, delta=(0, 999), rel=(0, -10),
                                                     evtype=pygame.MOUSEMOTION))
        self.assertIn(sb.get_value_percentage(), (0.976, 1))

        # Test remove onreturn
        sb = ScrollBar(length, world_range, 'sb', ORIENTATION_VERTICAL, onreturn=-1)
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

        switch.update(PygameEventUtils.key(KEY_LEFT, keydown=True))  # not infinite
        self.assertFalse(value[0])  # as this is false, dont change
        switch.update(PygameEventUtils.key(KEY_RIGHT, keydown=True))
        self.assertTrue(value[0])
        switch.update(PygameEventUtils.key(KEY_LEFT, keydown=True))
        self.assertFalse(value[0])
        switch.update(PygameEventUtils.key(KEY_LEFT, keydown=True))
        self.assertFalse(value[0])

        switch = menu.add.toggle_switch('toggle', False, onchange=onchange, infinite=True)
        switch.update(PygameEventUtils.key(KEY_LEFT, keydown=True))
        self.assertTrue(value[0])
        switch.update(PygameEventUtils.key(KEY_LEFT, keydown=True))
        self.assertFalse(value[0])

        # As there's only 2 states, return should change too
        switch.update(PygameEventUtils.key(KEY_APPLY, keydown=True))
        self.assertTrue(value[0])
        switch.update(PygameEventUtils.key(KEY_APPLY, keydown=True))
        self.assertFalse(value[0])

        # Check left/right clicks
        click_pos = switch.get_rect(to_real_position=True, apply_padding=False).midleft
        switch.update(PygameEventUtils.mouse_click(click_pos[0] + 150, click_pos[1]))
        self.assertFalse(value[0])
        switch.update(PygameEventUtils.mouse_click(click_pos[0] + 250, click_pos[1]))
        self.assertTrue(value[0])
        switch.update(PygameEventUtils.mouse_click(click_pos[0] + 150, click_pos[1]))
        self.assertFalse(value[0])

        # Test readonly
        switch.readonly = True
        switch.update(PygameEventUtils.key(KEY_APPLY, keydown=True))
        self.assertFalse(value[0])
        switch.update(PygameEventUtils.key(KEY_APPLY, keydown=True))
        self.assertFalse(value[0])
        switch.update(PygameEventUtils.key(KEY_APPLY, keydown=True))
        self.assertFalse(value[0])

        switch.readonly = False
        switch.update(PygameEventUtils.key(KEY_RIGHT, keydown=True))
        self.assertTrue(value[0])
        switch.update(PygameEventUtils.key(KEY_RIGHT, keydown=True))
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

    def test_image_widget(self) -> None:
        """
        Test image widget.
        """
        menu = MenuUtils.generic_menu()
        image = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES, font_color=(2, 9))
        image.set_max_width(100)
        self.assertIsNone(image._max_width[0])

        image.set_max_height(100)
        self.assertIsNone(image._max_height[0])

        image.set_title('epic')
        self.assertEqual(image.get_title(), '')
        self.assertEqual(image.get_image(), image._image)
        image.update(PygameEventUtils.middle_rect_mouse_motion(image))

    def test_surface_widget(self) -> None:
        """
        Test surface widget.
        """
        menu = MenuUtils.generic_menu()
        surf = pygame.Surface((150, 150))
        surf.fill((255, 192, 203))
        surf_widget = menu.add.surface(surf)

        self.assertEqual(surf_widget.get_size(), (166, 158))
        self.assertEqual(surf_widget.get_size(apply_padding=False), (150, 150))
        self.assertEqual(surf_widget.get_surface(), surf)

        surf_widget.rotate(10)
        self.assertEqual(surf_widget._angle, 0)

        surf_widget.resize(10, 10)
        self.assertFalse(surf_widget._scale[0])
        self.assertEqual(surf_widget._scale[1], 1)
        self.assertEqual(surf_widget._scale[2], 1)

        surf_widget.scale(100, 100)
        self.assertFalse(surf_widget._scale[0])
        self.assertEqual(surf_widget._scale[1], 1)
        self.assertEqual(surf_widget._scale[2], 1)

        surf_widget.flip(True, True)
        self.assertFalse(surf_widget._flip[0])
        self.assertFalse(surf_widget._flip[1])

        surf_widget.set_max_width(100)
        self.assertIsNone(surf_widget._max_width[0])

        surf_widget.set_max_height(100)
        self.assertIsNone(surf_widget._max_height[0])

        surf_widget.set_title('epic')
        self.assertEqual(surf_widget.get_title(), '')

        new_surface = pygame.Surface((160, 160))
        new_surface.fill((255, 192, 203))
        inner_surface = pygame.Surface((80, 80))
        inner_surface.fill((75, 0, 130))
        new_surface.blit(inner_surface, (40, 40))
        surf_widget.set_surface(new_surface)
        self.assertEqual(surf_widget.get_size(apply_padding=False), (160, 160))
        menu.draw(surface)
        surf_widget.update(PygameEventUtils.middle_rect_mouse_motion(surf_widget))
