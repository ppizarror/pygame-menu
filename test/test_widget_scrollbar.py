"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - SCROLLBAR
Test ScrollBar widget.
"""

__all__ = ['ScrollBarWidgetTest']

from test._utils import surface, PygameEventUtils, WINDOW_SIZE, BaseTest, MenuUtils

import pygame

from pygame_menu.locals import ORIENTATION_VERTICAL, POSITION_SOUTHEAST
from pygame_menu.widgets import ScrollBar
from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented


class ScrollBarWidgetTest(BaseTest):

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
        sb.update(PygameEventUtils.middle_rect_click(sb.get_rect(to_absolute_position=True), evtype=pygame.MOUSEBUTTONDOWN))
        self.assertEqual(sb.get_value(), 964)
        sb.update(PygameEventUtils.middle_rect_click(sb.get_slider_rect(), evtype=pygame.MOUSEBUTTONDOWN))
        self.assertTrue(sb.scrolling)
        sb.update(PygameEventUtils.middle_rect_click(sb.get_slider_rect(), button=4, evtype=pygame.MOUSEBUTTONDOWN))
        self.assertEqual(sb.get_value(), 875)
        sb.update(PygameEventUtils.middle_rect_click(sb.get_slider_rect(), button=5, evtype=pygame.MOUSEBUTTONDOWN))
        self.assertEqual(sb.get_value(), 964)
        self.assertEqual(sb.get_value_percentage(), 0.522)

        # Test mouse motion while scrolling
        sb.update(PygameEventUtils.middle_rect_click(sb.get_slider_rect(), button=5, delta=(0, 50), rel=(0, 10), evtype=pygame.MOUSEMOTION))
        self.assertEqual(sb.get_value_percentage(), 0.547)
        sb.update(PygameEventUtils.middle_rect_click(sb.get_slider_rect(), button=5, delta=(0, 50), rel=(0, -10), evtype=pygame.MOUSEMOTION))
        self.assertEqual(sb.get_value_percentage(), 0.522)
        sb.update(PygameEventUtils.middle_rect_click(sb.get_slider_rect(), button=5, delta=(0, 50), rel=(0, 999), evtype=pygame.MOUSEMOTION))
        self.assertEqual(sb.get_value_percentage(), 1)
        sb.readonly = True
        self.assertFalse(sb.update([]))

        # Ignore events if mouse outside the region
        sb.update(PygameEventUtils.middle_rect_click(sb.get_slider_rect(), button=5, delta=(0, 999), rel=(0, -10), evtype=pygame.MOUSEMOTION))
        self.assertIn(sb.get_value_percentage(), (0.976, 1))

        # Test remove onreturn
        sb = ScrollBar(length, world_range, 'sb', ORIENTATION_VERTICAL, onreturn=-1)
        self.assertIsNone(sb._onreturn)
        self.assertTrue(sb._kwargs.get('onreturn', 0))

        # Scrollbar ignores scaling
        self.assertRaises(WidgetTransformationNotImplemented, lambda: sb.scale(2, 2))
        self.assertFalse(sb._scale[0])
        self.assertRaises(WidgetTransformationNotImplemented, lambda: sb.resize(2, 2))
        self.assertFalse(sb._scale[0])
        self.assertRaises(WidgetTransformationNotImplemented, lambda: sb.set_max_width(10))
        self.assertIsNone(sb._max_width[0])
        self.assertRaises(WidgetTransformationNotImplemented, lambda: sb.set_max_height(10))
        self.assertIsNone(sb._max_height[0])
        sb._apply_font()
        sb.set_padding(10)
        self.assertEqual(sb._padding[0], 0)
        self.assertRaises(WidgetTransformationNotImplemented, lambda: sb.rotate(10))
        self.assertEqual(sb._angle, 0)
        self.assertRaises(WidgetTransformationNotImplemented, lambda: sb.flip(True, True))
        self.assertFalse(sb._flip[0])
        self.assertFalse(sb._flip[1])

        # Set minimum
        sb.set_minimum(0.5 * sb._values_range[1])

        # Test hide
        sb._mouseover = True
        sb.hide()

    def test_value(self) -> None:
        """
        Test scrollbar value.
        """
        menu = MenuUtils.generic_menu()
        sb = menu.get_scrollarea()._scrollbars[0]

        self.assertEqual(sb._default_value, 0)
        self.assertEqual(sb.get_value(), 0)
        self.assertFalse(sb.value_changed())
        sb.set_value(1)
        self.assertEqual(sb.get_value(), 1)
        self.assertTrue(sb.value_changed())
        sb.reset_value()
        self.assertEqual(sb.get_value(), 0)
        self.assertFalse(sb.value_changed())
