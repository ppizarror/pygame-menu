"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST SCROLLAREA
Test scrollarea.
"""

__all__ = ['ScrollAreaTest']

import copy
from test._utils import MenuUtils, PygameEventUtils, surface, TEST_THEME, PYGAME_V2, \
    BaseTest

import pygame
import pygame_menu

from pygame_menu.locals import POSITION_SOUTHEAST, POSITION_CENTER, POSITION_NORTHWEST, \
    POSITION_SOUTH, POSITION_NORTHEAST, POSITION_SOUTHWEST, POSITION_EAST, \
    POSITION_WEST, POSITION_NORTH, SCROLLAREA_POSITION_FULL, \
    SCROLLAREA_POSITION_BOTH_VERTICAL, SCROLLAREA_POSITION_BOTH_HORIZONTAL, \
    INPUT_TEXT, ORIENTATION_VERTICAL, ORIENTATION_HORIZONTAL, SCROLLAREA_POSITION_NONE

# noinspection PyProtectedMember
from pygame_menu._scrollarea import get_scrollbars_from_position


class ScrollAreaTest(BaseTest):

    def test_scrollarea_position(self) -> None:
        """
        Test position.
        """
        self.assertEqual(len(get_scrollbars_from_position(SCROLLAREA_POSITION_FULL)), 4)
        for i in (POSITION_EAST, POSITION_EAST, POSITION_WEST, POSITION_NORTH):
            self.assertIsInstance(get_scrollbars_from_position(i), str)
        self.assertEqual(get_scrollbars_from_position(POSITION_NORTHWEST), (POSITION_NORTH, POSITION_WEST))
        self.assertEqual(get_scrollbars_from_position(POSITION_NORTHEAST), (POSITION_NORTH, POSITION_EAST))
        self.assertEqual(get_scrollbars_from_position(POSITION_SOUTHEAST), (POSITION_SOUTH, POSITION_EAST))
        self.assertEqual(get_scrollbars_from_position(POSITION_SOUTHWEST), (POSITION_SOUTH, POSITION_WEST))
        self.assertEqual(get_scrollbars_from_position(SCROLLAREA_POSITION_BOTH_HORIZONTAL), (POSITION_SOUTH, POSITION_NORTH))
        self.assertEqual(get_scrollbars_from_position(SCROLLAREA_POSITION_BOTH_VERTICAL), (POSITION_EAST, POSITION_WEST))
        self.assertEqual(get_scrollbars_from_position(SCROLLAREA_POSITION_NONE), '')

        # Invalid
        self.assertRaises(ValueError, lambda: get_scrollbars_from_position(INPUT_TEXT))
        self.assertRaises(ValueError, lambda: get_scrollbars_from_position(POSITION_CENTER))

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

    def test_copy(self) -> None:
        """
        Test copy.
        """
        sa = MenuUtils.generic_menu().get_scrollarea()
        self.assertRaises(pygame_menu._scrollarea._ScrollAreaCopyException, lambda: copy.copy(sa))
        self.assertRaises(pygame_menu._scrollarea._ScrollAreaCopyException, lambda: copy.deepcopy(sa))

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
        if sa._scrollbars[1].get_orientation() == ORIENTATION_VERTICAL:
            s1 = sa._scrollbars[1]
            s2 = sa._scrollbars[0]
        else:
            s1 = sa._scrollbars[0]
            s2 = sa._scrollbars[1]
        sa.show_scrollbars(ORIENTATION_VERTICAL)
        sa.show_scrollbars(ORIENTATION_HORIZONTAL)

        self.assertTrue(s1.is_visible())
        sa.hide_scrollbars(ORIENTATION_VERTICAL)
        self.assertFalse(s1.is_visible())
        self.assertTrue(s2.is_visible())
        sa.hide_scrollbars(ORIENTATION_HORIZONTAL)
        self.assertFalse(s1.is_visible())
        self.assertFalse(s2.is_visible())
        sa.show_scrollbars(ORIENTATION_HORIZONTAL)
        sa.show_scrollbars(ORIENTATION_VERTICAL)
        self.assertTrue(s1.is_visible())
        self.assertTrue(s2.is_visible())

        # Test show hide but with force
        s1.disable_visibility_force()
        s1.hide()
        self.assertFalse(s1.is_visible())
        s1.show()
        self.assertTrue(s1.is_visible())
        s1.hide(True)  # Hide with force
        self.assertFalse(s1.is_visible())
        s1.show()  # Without force, it will not change the status
        self.assertFalse(s1.is_visible())
        s1.show(True)  # Without force, it will not change the status
        self.assertTrue(s1.is_visible())
        s1.hide()  # Without force, it will not change the status
        self.assertTrue(s1.is_visible())

        # Disable visibility force
        s1.disable_visibility_force()
        s1.hide()
        self.assertFalse(s1.is_visible())
        s1.show()
        self.assertTrue(s1.is_visible())
        s1.hide()
        self.assertFalse(s1.is_visible())

        # Check scrollbar render
        s1._slider_rect = None
        self.assertIsNone(s1._render())

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
        menu.render()

        # Get the size of the scrollarea
        sa = menu.get_scrollarea()

        sa_height = menu.get_height() - menu.get_menubar().get_height()
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

        pos_rect = sa.to_world_position((10, 10))
        self.assertEqual(pos_rect, (10, -145))

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
        self.assertEqual(sa.get_world_rect(absolute=True), pygame.Rect(0, 0, 600, 345))
        self.assertEqual(sa.get_size(), (600, 345))
        self.assertIsInstance(sa.mouse_is_over(), bool)

        # Append many items within menu, thus, scrollbars will appear
        self.assertEqual(sa.get_scrollbar_thickness(ORIENTATION_VERTICAL), 0)
        self.assertEqual(sa.get_scrollbar_thickness(ORIENTATION_HORIZONTAL), 0)

        sa._scrollbar_positions = (POSITION_NORTH, POSITION_EAST, POSITION_WEST, POSITION_SOUTH)
        self.assertEqual(sa.get_view_rect(), pygame.Rect(0, 155, 600, 345))

        for i in range(10):
            menu.add.button(f'b{i}').scale(20, 1)

        self.assertEqual(sa.get_scrollbar_thickness(ORIENTATION_VERTICAL), 20)
        self.assertEqual(sa.get_scrollbar_thickness(ORIENTATION_HORIZONTAL), 20)

        sa._on_vertical_scroll(0.5)
        sa._on_horizontal_scroll(0.5)

        self.assertEqual(sa.to_real_position((10, 10)), (10, 165))
        sa.get_view_rect()

        # Test rect
        sa = pygame_menu._scrollarea.ScrollArea(100, 100)
        self.assertEqual(sa.get_rect(to_real_position=True), pygame.Rect(0, 0, 100, 100))
        self.assertEqual(sa.get_scrollbar_thickness(ORIENTATION_VERTICAL, visible=False), 0)
        self.assertEqual(sa.get_scrollbar_thickness(ORIENTATION_HORIZONTAL, visible=False), 0)
        self.assertEqual(sa.get_scrollbar_thickness(ORIENTATION_VERTICAL, visible=False), 0)
        self.assertRaises(AssertionError, lambda: sa.get_scrollbar_thickness('fake', visible=False))

        # Test size with all scrollbars
        theme = pygame_menu.themes.THEME_DEFAULT.copy()
        theme.scrollarea_position = SCROLLAREA_POSITION_FULL
        menu = MenuUtils.generic_menu(theme=theme)
        for i in range(20):
            menu.add.button(i, bool)
        menu.get_scrollarea().show_scrollbars(ORIENTATION_VERTICAL)
        menu.get_scrollarea().show_scrollbars(ORIENTATION_HORIZONTAL)
        self.assertEqual(menu.get_scrollarea().get_view_rect(), (20, 100, 560, 400))

    # noinspection PyTypeChecker
    def test_widget_relative_to_view_rect(self) -> None:
        """
        Test widget relative position to view rect.
        """
        if not PYGAME_V2:
            return

        menu = MenuUtils.generic_menu()
        buttons = []
        for i in range(20):
            btn_title = f'b{i}'
            buttons.append(menu.add.button(btn_title, button_id=btn_title))
        sa = menu.get_scrollarea()

        def test_relative(widget: 'pygame_menu.widgets.Widget', x: float, y: float) -> None:
            """
            Test relative position from widget to scroll view rect.

            :param widget: Widget
            :param x: X relative position
            :param y: Y relative position
            """
            rx, ry = widget.get_scrollarea().get_widget_position_relative_to_view_rect(widget)
            self.assertAlmostEqual(x, rx)
            self.assertAlmostEqual(y, ry)

        test_relative(buttons[0], 0.4689655172413793, 0.15)
        test_relative(buttons[-1], 0.45517241379310347, 2.4775)

        # Scroll to middle
        sa.scroll_to(ORIENTATION_VERTICAL, 0.5)
        test_relative(buttons[0], 0.4689655172413793, -0.645)
        test_relative(buttons[-1], 0.45517241379310347, 1.6825)

        # Scroll to bottom
        sa.scroll_to(ORIENTATION_VERTICAL, 1)
        test_relative(buttons[0], 0.4689655172413793, -1.4375)
        test_relative(buttons[-1], 0.45517241379310347, 0.89)

    def test_bg_image(self) -> None:
        """
        Test background image.
        """
        img = pygame_menu.baseimage.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU)
        sa = pygame_menu._scrollarea.ScrollArea(100, 100, scrollbars=POSITION_EAST, area_color=img)
        sa._make_background_surface()
        self.assertIsInstance(sa._area_color, pygame_menu.BaseImage)

    def test_position(self) -> None:
        """
        Test different scrollbar and scrollarea positions.
        """
        sa = pygame_menu._scrollarea.ScrollArea(100, 100)
        sa_scrolls = sa._scrollbar_positions

        # Test invalid position
        sa._scrollbar_positions = 'fake'
        self.assertRaises(ValueError, lambda: sa._apply_size_changes())
        sa._scrollbar_positions = sa_scrolls

    def test_scrollbars(self) -> None:
        """
        Test scrollarea scrollbar's.
        """
        menu = MenuUtils.generic_menu(touchscreen=False, mouse_enabled=False,
                                      joystick_enabled=False, keyboard_enabled=False)
        sa = menu.get_scrollarea()
        sb = sa._scrollbars[0]
        self.assertFalse(sb._joystick_enabled)
        self.assertFalse(sb._keyboard_enabled)
        self.assertFalse(sb._mouse_enabled)
        self.assertFalse(sb._touchscreen_enabled)

        # Test scrollarea within frame
        drop = menu.add.dropselect('Subject Id', items=[('a',), ('b',), ('c',)], dropselect_id='s0')
        d_frame_sa = drop._drop_frame.get_scrollarea(inner=True)
        sb_frame = d_frame_sa._scrollbars[0]
        self.assertFalse(sb_frame._joystick_enabled)
        self.assertFalse(sb_frame._keyboard_enabled)
        self.assertFalse(sb_frame._mouse_enabled)
        self.assertFalse(sb_frame._touchscreen_enabled)
        self.assertEqual(sb_frame.get_menu(), menu)
        self.assertEqual(d_frame_sa.get_menu(), menu)

    def test_empty_scrollarea(self) -> None:
        """
        Test menu without scrollbars.
        """
        theme = pygame_menu.themes.THEME_DEFAULT.copy()
        theme.scrollarea_position = SCROLLAREA_POSITION_NONE
        menu = MenuUtils.generic_menu(theme=theme)
        for i in range(10):
            menu.add.button(i, bool)
        sa = menu.get_scrollarea()
        self.assertEqual(sa._scrollbars, [])
        self.assertEqual(sa._scrollbar_positions, ())
        self.assertEqual(sa.get_size(), (600, 400))
        self.assertEqual(sa.get_scrollbar_thickness(ORIENTATION_VERTICAL), 0)
        self.assertEqual(sa.get_scrollbar_thickness(ORIENTATION_HORIZONTAL), 0)

    def test_change_area_color(self) -> None:
        """
        Test area color.
        """
        menu = MenuUtils.generic_menu()
        sa = menu.get_scrollarea()
        sf = sa._bg_surface
        self.assertEqual(sa.update_area_color('red'), sa)
        self.assertNotEqual(sf, sa._bg_surface)
