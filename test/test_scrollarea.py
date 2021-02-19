"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST SCROLLAREA
Test scrollarea.

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

__all__ = ['ScrollAreaTest']

import copy
import unittest
from test._utils import MenuUtils, PygameEventUtils, surface, TEST_THEME

import pygame_menu
import pygame_menu.locals as _locals
from pygame_menu.scrollarea import get_scrollbars_from_position


class ScrollAreaTest(unittest.TestCase):

    def test_scrollarea_position(self) -> None:
        """
        Test position.
        """
        self.assertEqual(len(get_scrollbars_from_position(_locals.SCROLLAREA_POSITION_FULL)), 4)
        for i in (_locals.POSITION_EAST, _locals.POSITION_EAST, _locals.POSITION_WEST, _locals.POSITION_NORTH):
            self.assertIsInstance(get_scrollbars_from_position(i), str)
        self.assertEqual(get_scrollbars_from_position(_locals.POSITION_NORTHWEST),
                         (_locals.POSITION_NORTH, _locals.POSITION_WEST))
        self.assertEqual(get_scrollbars_from_position(_locals.POSITION_NORTHEAST),
                         (_locals.POSITION_NORTH, _locals.POSITION_EAST))
        self.assertEqual(get_scrollbars_from_position(_locals.POSITION_SOUTHEAST),
                         (_locals.POSITION_SOUTH, _locals.POSITION_EAST))
        self.assertEqual(get_scrollbars_from_position(_locals.POSITION_SOUTHWEST),
                         (_locals.POSITION_SOUTH, _locals.POSITION_WEST))
        self.assertEqual(get_scrollbars_from_position(_locals.SCROLLAREA_POSITION_BOTH_HORIZONTAL),
                         (_locals.POSITION_SOUTH, _locals.POSITION_NORTH))
        self.assertEqual(get_scrollbars_from_position(_locals.SCROLLAREA_POSITION_BOTH_VERTICAL),
                         (_locals.POSITION_EAST, _locals.POSITION_WEST))

        # Invalid
        self.assertRaises(ValueError, lambda: get_scrollbars_from_position(_locals.INPUT_TEXT))
        self.assertRaises(ValueError, lambda: get_scrollbars_from_position(_locals.POSITION_CENTER))

    def test_surface_cache(self) -> None:
        """
        Surface cache tests.
        """
        menu = MenuUtils.generic_menu()
        sa = menu.get_scrollarea()
        self.assertFalse(menu._widgets_surface_need_update)
        sa.force_menu_surface_cache_update()
        sa.force_menu_surface_update()
        self.assertTrue(menu._widgets_surface_need_update)

        # Remove world and draw
        sa._world = None
        sa.draw(surface)

    def test_surface_id(self) -> None:
        """
        Test surface id.
        """
        menu = MenuUtils.generic_menu()
        sa = menu.get_scrollarea()
        sa.set_id('nice')
        self.assertEqual(sa.get_id(), 'nice')

    def test_copy(self) -> None:
        """
        Test copy.
        """
        sa = MenuUtils.generic_menu().get_scrollarea()
        self.assertRaises(pygame_menu.scrollarea._ScrollAreaCopyException, lambda: copy.copy(sa))
        self.assertRaises(pygame_menu.scrollarea._ScrollAreaCopyException, lambda: copy.deepcopy(sa))

    def test_decorator(self) -> None:
        """
        Test decorator.
        """
        sa = MenuUtils.generic_menu().get_scrollarea()
        dec = sa.get_decorator()
        self.assertEqual(sa, dec._obj)

    def test_translate(self) -> None:
        """
        Translate scrollbar.
        """
        menu = MenuUtils.generic_menu()
        sa = menu.get_scrollarea()
        self.assertEqual(sa.get_translate(), (0, 0))
        r = sa.get_rect()
        sa.translate(10, 10)
        self.assertEqual(sa.get_translate(), (10, 10))
        new_r = sa.get_rect()
        self.assertEqual(new_r.x, r.x + 10)
        self.assertEqual(new_r.y, r.y + 10)
        sa.translate(50, 90)
        new_r = sa.get_rect()
        self.assertEqual(new_r.x, r.x + 50)
        self.assertEqual(new_r.y, r.y + 90)

    def test_show_hide_scrollbars(self) -> None:
        """
        Test show hide scrollbars.
        """
        menu = MenuUtils.generic_menu()
        sa = menu.get_scrollarea()
        menu.render()
        menu.draw(surface)
        for s in sa._scrollbars:
            s.show()
        if sa._scrollbars[1].get_orientation() == _locals.ORIENTATION_VERTICAL:
            s1 = sa._scrollbars[1]
            s2 = sa._scrollbars[0]
        else:
            s1 = sa._scrollbars[0]
            s2 = sa._scrollbars[1]
        self.assertTrue(s1.is_visible())
        sa.hide_scrollbars(_locals.ORIENTATION_VERTICAL)
        self.assertFalse(s1.is_visible())
        self.assertTrue(s2.is_visible())
        sa.hide_scrollbars(_locals.ORIENTATION_HORIZONTAL)
        self.assertFalse(s1.is_visible())
        self.assertFalse(s2.is_visible())
        sa.show_scrollbars(_locals.ORIENTATION_HORIZONTAL)
        sa.show_scrollbars(_locals.ORIENTATION_VERTICAL)
        self.assertTrue(s1.is_visible())
        self.assertTrue(s2.is_visible())

    def test_size(self) -> None:
        """
        Test size.
        """
        menu = MenuUtils.generic_menu(title='menu', theme=TEST_THEME.copy())
        menu.render()
        self.assertEqual(menu.get_height(widget=True), 0)

        # Adds a button, hide it, then the height should be 0 as well
        btn = menu.add.button('hidden')
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
        self.assertEqual(posrect, (10, -145))

        self.assertFalse(sa.is_scrolling())
        self.assertEqual(sa.get_menu(), menu)

        sa._on_vertical_scroll(50)
        sa._on_horizontal_scroll(50)

        # Remove the world of surface
        world = sa._world
        sa._world = None
        self.assertEqual(sa.get_world_size(), (0, 0))
        sa._world = world

        # Test collide
        event = PygameEventUtils.mouse_click(100, 100, inlist=False)
        self.assertFalse(sa.collide(btn, event))

        # Create virtual rect from button
        rect_virtual = sa.to_real_position(btn.get_rect())
        event_click_widget = PygameEventUtils.middle_rect_click(rect_virtual, inlist=False)
        self.assertTrue(sa.collide(btn, event_click_widget))
