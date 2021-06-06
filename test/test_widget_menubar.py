"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - MENUBAR
Test MenuBar widget.

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

__all__ = ['MenuBarWidgetTest']

from test._utils import MenuUtils, surface, PygameEventUtils, SYS_PLATFORM_OSX, \
    BaseTest, PYGAME_V2

import pygame
import pygame_menu
import pygame_menu.controls as ctrl

from pygame_menu.locals import POSITION_NORTH, POSITION_SOUTH, POSITION_EAST, \
    POSITION_WEST, POSITION_SOUTHWEST
from pygame_menu.widgets import MENUBAR_STYLE_ADAPTIVE, MENUBAR_STYLE_NONE, \
    MENUBAR_STYLE_SIMPLE, MENUBAR_STYLE_UNDERLINE, MENUBAR_STYLE_UNDERLINE_TITLE, \
    MENUBAR_STYLE_TITLE_ONLY, MENUBAR_STYLE_TITLE_ONLY_DIAGONAL
from pygame_menu.widgets import MenuBar
from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented


class MenuBarWidgetTest(BaseTest):

    # noinspection PyTypeChecker,PyArgumentEqualDefault
    def test_menubar(self) -> None:
        """
        Test menubar widget.
        """
        if SYS_PLATFORM_OSX:
            return

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

        # Test unknown mode
        mb = MenuBar('Menu', 500, (0, 0, 0), back_box=True, mode='unknown')
        mb.set_menu(menu)
        self.assertRaises(ValueError, lambda: mb._render())

        # Check margins
        mb = MenuBar('Menu', 500, (0, 0, 0), back_box=True, mode=MENUBAR_STYLE_ADAPTIVE)
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_SOUTH), (0, (0, 0)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_EAST), (0, (0, 0)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_WEST), (0, (0, 0)))
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_NORTH), (0, (0, 0)))
        mb.set_menu(menu)
        mb._render()
        self.assertEqual(mb.get_scrollbar_style_change(POSITION_SOUTHWEST), (0, (0, 0)))

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
                                      onclose=pygame_menu.events.CLOSE,
                                      touchscreen=True)
        theme.widget_border_inflate = 0
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
        self.assertTrue(mb.update(PygameEventUtils.middle_rect_click(
            mb._backbox_rect, evtype=pygame.FINGERUP, menu=menu)))
        self.assertFalse(mb.update(PygameEventUtils.middle_rect_click(
            mb._backbox_rect, evtype=pygame.MOUSEBUTTONDOWN)))
        self.assertTrue(mb.update(PygameEventUtils.joy_button(ctrl.JOY_BUTTON_BACK)))
        mb.readonly = True
        self.assertFalse(mb.update(PygameEventUtils.joy_button(ctrl.JOY_BUTTON_BACK)))
        mb.readonly = False

        # Test none methods
        self.assertRaises(WidgetTransformationNotImplemented, lambda: mb.rotate(10))
        self.assertEqual(mb._angle, 0)

        self.assertRaises(WidgetTransformationNotImplemented, lambda: mb.resize(10, 10))
        self.assertFalse(mb._scale[0])
        self.assertEqual(mb._scale[1], 1)
        self.assertEqual(mb._scale[2], 1)

        self.assertRaises(WidgetTransformationNotImplemented, lambda: mb.scale(100, 100))
        self.assertFalse(mb._scale[0])
        self.assertEqual(mb._scale[1], 1)
        self.assertEqual(mb._scale[2], 1)

        self.assertRaises(WidgetTransformationNotImplemented, lambda: mb.flip(True, True))
        self.assertFalse(mb._flip[0])
        self.assertFalse(mb._flip[1])

        self.assertRaises(WidgetTransformationNotImplemented, lambda: mb.set_max_width(100))
        self.assertIsNone(mb._max_width[0])

        self.assertRaises(WidgetTransformationNotImplemented, lambda: mb.set_max_height(100))
        self.assertIsNone(mb._max_height[0])

        # Ignore others
        mb.set_padding()
        mb.set_border()
        mb.set_selection_effect()
        menu.add.button('nice')

    def test_empty_title(self) -> None:
        """
        Test empty title.
        """
        title = MenuBar('', 500, (0, 0, 0), back_box=True)
        p = title._padding
        self.assertEqual(title.get_width(), p[1] + p[3])
        self.assertEqual(title.get_height(), p[0] + p[2])

    def test_value(self) -> None:
        """
        Test menubar value.
        """
        mb = MenuBar('Menu', 500, (0, 0, 0), back_box=True)
        self.assertRaises(ValueError, lambda: mb.get_value())
        self.assertRaises(ValueError, lambda: mb.set_value('value'))
        self.assertFalse(mb.value_changed())
        mb.reset_value()
