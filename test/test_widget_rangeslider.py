"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - RANGE SLIDER
Test RangeSlider widget.
"""

__all__ = ['RangeSliderWidgetTest']

from test._utils import MenuUtils, surface, PygameEventUtils, BaseTest, sleep

import pygame
import pygame_menu
import pygame_menu.controls as ctrl

from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented


class RangeSliderWidgetTest(BaseTest):

    # noinspection PyTypeChecker
    def test_single_rangeslider(self) -> None:
        """
        Test single range slider.
        """
        menu = MenuUtils.generic_menu()

        # Single slider
        slider = pygame_menu.widgets.RangeSlider('Range S')

        test = [0, 0]

        def onchange(x: float) -> None:
            """
            Change slider.
            """
            # noinspection PyTypeChecker
            test[0] = x

        def onreturn(x: float) -> None:
            """
            Return slider.
            """
            # noinspection PyTypeChecker
            test[1] = x

        slider.set_onchange(onchange)
        slider.set_onreturn(onreturn)

        menu.add.generic_widget(slider, True)
        self.assertEqual(slider.get_value(), 0)
        slider.set_value(0.5)
        self.assertEqual(slider.get_value(), 0.5)
        self.assertEqual(slider._value, [0.5, 0])

        self.assertEqual(test[0], 0)
        slider.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
        self.assertEqual(test[0], 0.4)
        self.assertEqual(slider.get_value(), 0.4)
        slider.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
        self.assertAlmostEqual(slider.get_value(), 0.3)
        for _ in range(10):
            slider.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
        self.assertEqual(slider.get_value(), 0)
        self.assertTrue(slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True)))
        self.assertEqual(slider.get_value(), 0.1)
        self.assertEqual(test[1], 0)
        slider.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        self.assertEqual(test[1], 0.1)

        # Ignore invalid key
        self.assertFalse(slider.update(
            PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True, testmode=False)))

        # Ignore for readonly
        slider.draw(surface)
        slider.draw_after_if_selected(surface)
        slider.readonly = True
        self.assertFalse(slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True)))
        self.assertEqual(slider.get_value(), 0.1)
        slider._update_value(0)
        self.assertEqual(slider.get_value(), 0.1)
        slider.readonly = False

        # Test invalid values
        self.assertRaises(AssertionError, lambda: slider.set_value(-1))
        self.assertRaises(AssertionError, lambda: slider.set_value([0.4, 0.5]))

        # Test invalid transforms
        self.assertRaises(WidgetTransformationNotImplemented, lambda: slider.rotate())
        self.assertRaises(WidgetTransformationNotImplemented, lambda: slider.flip())
        self.assertRaises(WidgetTransformationNotImplemented, lambda: slider.scale())
        self.assertRaises(WidgetTransformationNotImplemented, lambda: slider.resize())
        self.assertRaises(WidgetTransformationNotImplemented, lambda: slider.set_max_width())
        self.assertRaises(WidgetTransformationNotImplemented, lambda: slider.set_max_height())

        # Test mouse click
        self.assertFalse(slider._selected_mouse)
        pos = slider._test_get_pos_value(0.5)
        slider.update(PygameEventUtils.middle_rect_click(pos, evtype=pygame.MOUSEBUTTONDOWN))
        self.assertEqual(slider.get_value(), 0.1)
        self.assertTrue(slider._selected_mouse)
        self.assertFalse(slider._scrolling)
        slider.update(PygameEventUtils.middle_rect_click(pos))
        self.assertFalse(slider._scrolling)
        self.assertEqual(slider.get_value(), 0.5)
        self.assertFalse(slider._selected_mouse)

        # Mouse click out of range
        slider._selected_mouse = True
        pos = slider._test_get_pos_value(1, dx=100)
        slider.update(PygameEventUtils.middle_rect_click(pos))
        self.assertEqual(slider.get_value(), 0.5)
        self.assertFalse(slider._selected_mouse)

        slider._selected_mouse = True
        pos = slider._test_get_pos_value(0, dx=-100)
        slider.update(PygameEventUtils.middle_rect_click(pos))
        self.assertEqual(slider.get_value(), 0.5)
        self.assertFalse(slider._selected_mouse)

        # Test extremes
        slider._selected_mouse = True
        pos = slider._test_get_pos_value(0)
        slider.update(PygameEventUtils.middle_rect_click(pos))
        self.assertEqual(slider.get_value(), 0)
        slider._selected_mouse = True
        pos = slider._test_get_pos_value(1)
        slider.update(PygameEventUtils.middle_rect_click(pos))
        self.assertEqual(slider.get_value(), 1)

        # Scroll to 0.5
        pos2 = slider._test_get_pos_value(0.5)
        self.assertFalse(slider._scrolling)
        slider_rect = slider._get_slider_inflate_rect(0, to_real_position=True)
        slider.update(PygameEventUtils.middle_rect_click(slider_rect, evtype=pygame.MOUSEBUTTONDOWN))
        self.assertTrue(slider._scrolling)
        self.assertTrue(slider._selected_mouse)
        dx = pos[0] - pos2[0]
        slider.update(PygameEventUtils.mouse_motion(slider_rect, rel=(-dx, pos[1]), update_mouse=True))
        self.assertEqual(slider.get_value(), 0.5)
        self.assertTrue(slider._scrolling)
        slider.update(PygameEventUtils.middle_rect_click(pos))
        self.assertFalse(slider._scrolling)

        # Check invalid constructor for single slider
        self.assertRaises(AssertionError, lambda: pygame_menu.widgets.RangeSlider('Range S', default_value=2))
        self.assertRaises(AssertionError, lambda: pygame_menu.widgets.RangeSlider('Range S', default_value=1, range_values=[1, 0]))
        self.assertRaises(AssertionError, lambda: pygame_menu.widgets.RangeSlider('Range S', default_value=1, range_values=[1, 1]))
        self.assertRaises(AssertionError, lambda: pygame_menu.widgets.RangeSlider('Range S', default_value='a'))

        # Ignore tabs
        self.assertFalse(slider.update(PygameEventUtils.key(ctrl.KEY_TAB, keydown=True)))

        # Check LEFT key in repeat
        self.assertIn(ctrl.KEY_RIGHT, slider._keyrepeat_counters.keys())
        self.assertEqual(slider.get_value(), 0.5)

        # Make left repeat
        slider._keyrepeat_counters[ctrl.KEY_RIGHT] += 1e4
        self.assertEqual(len(slider._events), 0)
        self.assertFalse(slider.update([]))
        self.assertEqual(len(slider._events), 1)
        self.assertFalse(slider.update([]))  # As key is not pressed, event continues
        self.assertEqual(len(slider._events), 0)

        # Keyup, removes counters
        slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keyup=True))
        self.assertNotIn(ctrl.KEY_RIGHT, slider._keyrepeat_counters.keys())
        self.assertFalse(hasattr(slider, '_range_box'))

        # Single slider with range box
        slider_rb = pygame_menu.widgets.RangeSlider('Range', range_box_single_slider=True)
        menu.add.generic_widget(slider_rb, True)
        slider_rb.draw(surface)
        self.assertTrue(hasattr(slider_rb, '_range_box'))
        self.assertEqual(slider_rb._range_box.get_width(), 0)
        slider_rb.set_value(1)
        self.assertEqual(slider_rb._range_box.get_width(), 150)

    def test_single_discrete(self) -> None:
        """
        Test single range slider with discrete values.
        """
        menu = MenuUtils.generic_menu()

        # Single slider with discrete values
        rv = [0, 1, 2, 3, 4, 5]
        slider = pygame_menu.widgets.RangeSlider('Range', range_values=rv)
        menu.add.generic_widget(slider, True)

        self.assertRaises(AssertionError, lambda: pygame_menu.widgets.RangeSlider('Range', default_value=0.5, range_values=rv))
        self.assertRaises(AssertionError, lambda: pygame_menu.widgets.RangeSlider('Range', default_value=-1, range_values=rv))

        self.assertRaises(AssertionError, lambda: slider.set_value(-1))
        self.assertRaises(AssertionError, lambda: slider.set_value([0, 1]))
        self.assertRaises(AssertionError, lambda: slider.set_value((0, 1)))

        # Test key events
        self.assertFalse(slider.update(PygameEventUtils.key(ctrl.KEY_TAB, keydown=True)))
        slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
        self.assertEqual(slider.get_value(), 1)
        slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
        self.assertEqual(slider.get_value(), 2)
        slider._increment = 0
        slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
        self.assertEqual(slider.get_value(), 3)
        slider.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
        self.assertEqual(slider.get_value(), 2)
        slider.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
        self.assertEqual(slider.get_value(), 1)
        slider.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
        self.assertEqual(slider.get_value(), 0)
        slider.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
        self.assertEqual(slider.get_value(), 0)

        # Test click mouse
        slider._selected_mouse = True
        pos = slider._test_get_pos_value(2)
        slider.update(PygameEventUtils.middle_rect_click(pos))
        self.assertEqual(slider.get_value(), 2)
        self.assertFalse(slider._selected_mouse)

        # Test invalid click
        slider._selected_mouse = True
        pos = slider._test_get_pos_value(2, dx=1000)
        slider.update(PygameEventUtils.middle_rect_click(pos))
        self.assertEqual(slider.get_value(), 2)
        self.assertFalse(slider._selected_mouse)

        # Scroll to 4
        pos = slider._test_get_pos_value(2)
        pos2 = slider._test_get_pos_value(4)
        self.assertFalse(slider._scrolling)
        slider_rect = slider._get_slider_inflate_rect(0, to_real_position=True)
        slider.update(PygameEventUtils.middle_rect_click(slider_rect, evtype=pygame.MOUSEBUTTONDOWN))
        self.assertTrue(slider._scrolling)
        self.assertTrue(slider._selected_mouse)
        dx = pos[0] - pos2[0]
        slider.update(PygameEventUtils.mouse_motion(slider_rect, rel=(-dx, pos[1]), update_mouse=True))
        self.assertEqual(slider.get_value(), 4)
        self.assertTrue(slider._scrolling)
        slider.update(PygameEventUtils.middle_rect_click(pos))
        self.assertFalse(slider._scrolling)

        # Back to 2
        slider.set_value(2)

        # Invalid scrolling if clicked outside the slider
        slider.update(PygameEventUtils.middle_rect_click(slider._test_get_pos_value(0), evtype=pygame.MOUSEBUTTONDOWN))
        self.assertFalse(slider._scrolling)

    # noinspection PyTypeChecker
    def test_double(self) -> None:
        """
        Test double range slider.
        """
        menu = MenuUtils.generic_menu()

        # Double slider
        slider = pygame_menu.widgets.RangeSlider(
            'Range',
            range_text_value_tick_number=3,
            default_value=(0.2, 1.0),
            slider_text_value_font=pygame_menu.font.FONT_BEBAS,
            range_text_value_font=pygame_menu.font.FONT_8BIT,
            slider_text_value_triangle=False
        )
        slider._slider_text_value_vmargin = -2
        menu.add.generic_widget(slider, True)
        slider.draw(surface)
        slider.draw_after_if_selected(surface)

        self.assertEqual(slider.get_value(), (0.2, 1.0))
        self.assertRaises(AssertionError, lambda: slider.set_value(0.2))
        self.assertRaises(AssertionError, lambda: slider.set_value((0.2, 0.2)))
        self.assertRaises(AssertionError, lambda: slider.set_value((1.0, 0.2)))
        self.assertRaises(AssertionError, lambda: slider.set_value((0.2, 0.5, 1.0)))

        # Test slider selection
        self.assertTrue(slider._slider_selected[0])
        self.assertTrue(slider.update(PygameEventUtils.key(ctrl.KEY_TAB, keydown=True)))
        self.assertFalse(slider._slider_selected[0])
        slider.draw(surface)
        slider.draw_after_if_selected(surface)

        # Test click sliders
        slider_rect = slider._get_slider_inflate_rect(0, to_real_position=True)
        self.assertTrue(slider.update(PygameEventUtils.middle_rect_click(slider_rect, evtype=pygame.MOUSEBUTTONDOWN)))
        self.assertTrue(slider._slider_selected[0])
        self.assertFalse(slider.update(PygameEventUtils.middle_rect_click(slider_rect, evtype=pygame.MOUSEBUTTONDOWN)))  # Slider already selected

        # Click if sliders are colliding
        slider.set_value((0.5, 0.50000001))
        slider_rect = slider._get_slider_inflate_rect(1, to_real_position=True)
        self.assertFalse(slider.update(PygameEventUtils.middle_rect_click(slider_rect, evtype=pygame.MOUSEBUTTONDOWN)))
        self.assertTrue(slider._slider_selected[0])
        slider.set_value((0.5, 0.7))
        slider_rect = slider._get_slider_inflate_rect(1, to_real_position=True)
        self.assertTrue(slider.update(PygameEventUtils.middle_rect_click(slider_rect, evtype=pygame.MOUSEBUTTONDOWN)))
        self.assertTrue(slider._slider_selected[1])

        # Test left slider
        pos = slider._test_get_pos_value(0.5)
        pos2 = slider._test_get_pos_value(0.6)
        slider_rect = slider._get_slider_inflate_rect(0, to_real_position=True)
        self.assertEqual(slider_rect, pygame.Rect(344, 311, 15, 28))
        slider.update(PygameEventUtils.middle_rect_click(slider_rect, evtype=pygame.MOUSEBUTTONDOWN))
        self.assertTrue(slider._slider_selected[0])
        self.assertTrue(slider._scrolling)
        self.assertTrue(slider._selected_mouse)
        dx = pos[0] - pos2[0]
        slider.update(PygameEventUtils.mouse_motion(slider_rect, rel=(-dx, pos[1]), update_mouse=True))
        self.assertEqual(slider.get_value(), (0.6, 0.7))

        # As slider moved, ignore this
        slider.update(PygameEventUtils.mouse_motion(slider_rect, rel=(-dx, pos[1]), update_mouse=True))
        self.assertEqual(slider.get_value(), (0.6, 0.7))
        self.assertTrue(slider._scrolling)
        self.assertTrue(slider._slider_selected[0])

        # Move to 0
        self.assertTrue(slider._selected_mouse)
        pos = slider._test_get_pos_value(0)
        pos2 = slider._test_get_pos_value(0.6)
        dx = pos[0] - pos2[0]
        slider.update(PygameEventUtils.mouse_motion(slider_rect, rel=(dx, pos[1]), update_mouse=True))
        self.assertEqual(slider.get_value(), (0, 0.7))

        # Move more than 0.7
        pos = slider._test_get_pos_value(0)
        pos2 = slider._test_get_pos_value(0.75)
        slider_rect = slider._get_slider_inflate_rect(0, to_real_position=True)
        dx = pos[0] - pos2[0]
        slider.update(PygameEventUtils.mouse_motion(slider_rect, rel=(-dx, pos[1]), update_mouse=True))
        self.assertEqual(slider.get_value(), (0, 0.7))

        # Move to 0.7 - eps
        pos = slider._test_get_pos_value(0)
        pos2 = slider._test_get_pos_value(0.7 - 1e-6)
        slider_rect = slider._get_slider_inflate_rect(0, to_real_position=True)
        dx = pos[0] - pos2[0]
        slider.update(PygameEventUtils.mouse_motion(slider_rect, rel=(-dx, pos[1]), update_mouse=True))
        self.assertAlmostEqual(slider.get_value()[0], 0.7 - 1e-7, places=1)

        # Ignore if move 0.7 + eps
        self.assertFalse(slider.update(PygameEventUtils.mouse_motion(slider_rect, rel=(1, pos[1]), update_mouse=True)))

        # Change to right
        slider_rect = slider._get_slider_inflate_rect(1, to_real_position=True)
        self.assertTrue(slider.update(PygameEventUtils.key(ctrl.KEY_TAB, keydown=True)))
        pos = slider._test_get_pos_value(0.7)
        pos2 = slider._test_get_pos_value(0.8)
        dx = pos[0] - pos2[0]
        self.assertFalse(slider.update(PygameEventUtils.mouse_motion(slider_rect, rel=(-1, pos[1]), update_mouse=True)))
        self.assertTrue(slider.update(PygameEventUtils.mouse_motion(slider_rect, rel=(-dx, pos[1]), update_mouse=True)))
        self.assertAlmostEqual(slider.get_value()[1], 0.8)

        # Test left/right
        slider.set_value((0.7, 0.8))
        slider.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
        slider.set_value((0.7, 0.8))  # Ignored
        slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
        slider.set_value((0.7, 0.9))
        slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
        slider.set_value((0.7, 1.0))
        slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
        slider.set_value((0.7, 1.0))
        slider.set_value((0.7, 0.8))
        slider.update(PygameEventUtils.key(ctrl.KEY_TAB, keydown=True))
        slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
        slider.set_value((0.7, 0.8))
        slider.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
        slider.set_value((0.6, 0.8))

        # Reset value
        slider.reset_value()
        self.assertEqual(slider.get_value(), (0.2, 1.0))

    def test_double_discrete(self) -> None:
        """
        Test double range slider with discrete values.
        """
        menu = MenuUtils.generic_menu()
        rv = [0, 1, 2, 3, 4, 5]

        # Double slider discrete
        slider = pygame_menu.widgets.RangeSlider('Range', range_text_value_tick_number=3, range_values=rv, default_value=(1, 4))
        menu.add.generic_widget(slider, True)
        slider.draw(surface)

        # Test set values
        slider.set_value([1, 2])
        self.assertEqual(slider.get_value(), (1, 2))

        # Test invalid values
        self.assertRaises(AssertionError, lambda: slider.set_value((1.1, 2.2)))
        self.assertRaises(AssertionError, lambda: slider.set_value((1, 1)))
        self.assertRaises(AssertionError, lambda: slider.set_value((2, 1)))
        self.assertRaises(AssertionError, lambda: slider.set_value(1))

        # Test left/right
        self.assertTrue(slider.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True)))
        self.assertEqual(slider.get_value(), (0, 2))
        self.assertFalse(slider.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True)))
        self.assertEqual(slider.get_value(), (0, 2))
        self.assertTrue(slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True)))
        self.assertEqual(slider.get_value(), (1, 2))
        self.assertFalse(slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True)))
        self.assertEqual(slider.get_value(), (1, 2))

        slider._update_value(0.99)
        self.assertEqual(slider.get_value(), (1, 2))

        self.assertEqual(slider._get_slider_inflate_rect(0, to_absolute_position=True), pygame.Rect(301, 209, 15, 28))

    def test_kwargs(self) -> None:
        """
        Test rangeslider kwargs from manager.
        """
        menu = MenuUtils.generic_menu()
        slider = menu.add.range_slider('Range', 0.5, (0, 1), 1, range_margin=(100, 0))
        self.assertEqual(len(slider._kwargs), 0)
        self.assertEqual(slider._range_margin, (100, 0))

    def test_empty_title(self) -> None:
        """
        Test empty title.
        """
        menu = MenuUtils.generic_menu()
        r = menu.add.range_slider('', 0.5, (0, 1), 0.1)
        self.assertEqual(r.get_size(), (198, 66))

    def test_invalid_range(self) -> None:
        """
        Test invalid ranges. #356
        """
        menu = MenuUtils.generic_menu()
        r = menu.add.range_slider('Infection Rate', default=2, increment=0.5, range_values=(2, 10))
        self.assertEqual(r.get_value(), 2)
        self.assertTrue(r.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True)))
        self.assertEqual(r.get_value(), 2.5)
        self.assertTrue(r.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True)))
        self.assertEqual(r.get_value(), 2)
        self.assertFalse(r.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True)))
        self.assertEqual(r.get_value(), 2)
        for _ in range(20):
            r.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
        self.assertEqual(r.get_value(), 10)

    def test_value(self) -> None:
        """
        Test rangeslider value.
        """
        menu = MenuUtils.generic_menu()

        # Single
        r = menu.add.range_slider('Range', 0.5, (0, 1), 0.1)
        self.assertEqual(r.get_value(), 0.5)
        self.assertFalse(r.value_changed())
        r.set_value(0.8)
        self.assertTrue(r.value_changed())
        self.assertEqual(r.get_value(), 0.8)
        r.reset_value()
        self.assertEqual(r.get_value(), 0.5)
        self.assertFalse(r.value_changed())

        # Double
        r = menu.add.range_slider('Range', [0.2, 0.6], (0, 1), 0.1)
        self.assertEqual(r.get_value(), (0.2, 0.6))
        self.assertFalse(r.value_changed())
        self.assertRaises(AssertionError, lambda: r.set_value(0.8))
        r.set_value((0.5, 1))
        self.assertTrue(r.value_changed())
        self.assertEqual(r.get_value(), (0.5, 1))
        r.reset_value()
        self.assertEqual(r.get_value(), (0.2, 0.6))
        self.assertFalse(r.value_changed())

    def test_keyrepeat(self) -> None:
        """
        Test keyrepeat.
        """
        menu = MenuUtils.generic_menu(keyboard_ignore_nonphysical=False)

        e = PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True)
        slider_on = menu.add.range_slider('', 0, [0, 1], increment=0.1)
        slider_on.update(e)
        slider_off = menu.add.range_slider('', 0, [0, 1], increment=0.1, repeat_keys=False)
        slider_off.update(e)

        # Test with time
        for i in range(5):
            sleep(0.5)
            slider_on.update([])
            slider_off.update([])
        self.assertGreater(slider_on.get_value(), 0.1)
        self.assertEqual(slider_off.get_value(), 0.1)
