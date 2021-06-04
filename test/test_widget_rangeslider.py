"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - RANGE SLIDER
Test RangeSlider widget.

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

__all__ = ['RangeSliderWidgetTest']

from test._utils import MenuUtils, surface, PygameEventUtils, BaseTest

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

        # Test invalid values for double
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
        self.assertRaises(AssertionError, lambda: pygame_menu.widgets.RangeSlider(
            'Range S', default_value=2))
        self.assertRaises(AssertionError, lambda: pygame_menu.widgets.RangeSlider(
            'Range S', default_value=1, range_values=[1, 0]))
        self.assertRaises(AssertionError, lambda: pygame_menu.widgets.RangeSlider(
            'Range S', default_value=1, range_values=[1, 1]))
        self.assertRaises(AssertionError, lambda: pygame_menu.widgets.RangeSlider(
            'Range S', default_value='a'))

        # Ignore tabs
        self.assertFalse(slider.update(PygameEventUtils.key(ctrl.KEY_TAB, keydown=True)))

        # Single slider with range box
        slider_rb = pygame_menu.widgets.RangeSlider('Range', range_box_single_slider=True)
        menu.add.generic_widget(slider_rb, True)
        slider_rb.draw(surface)

    def test_single_discrete(self) -> None:
        """
        Test single range slider with discrete values.
        """
        menu = MenuUtils.generic_menu()

        # Single slider with discrete values
        rv = [0, 1, 2, 3, 4, 5]
        slider = pygame_menu.widgets.RangeSlider('Range', range_values=rv)
        menu.add.generic_widget(slider, True)

        self.assertRaises(AssertionError, lambda: pygame_menu.widgets.RangeSlider(
            'Range', default_value=0.5, range_values=rv))

    def test_double(self) -> None:
        """
        Test double range slider.
        """
        menu = MenuUtils.generic_menu()

        # Double slider
        slider = pygame_menu.widgets.RangeSlider('Range', range_text_value_number=3,
                                                 default_value=(0.2, 1.0))
        menu.add.generic_widget(slider, True)
        slider.draw(surface)

    def test_double_discrete(self) -> None:
        """
        Test double range slider with discrete values.
        """
        menu = MenuUtils.generic_menu()
        rv = [0, 1, 2, 3, 4, 5]

        # Double slider discrete
        slider = pygame_menu.widgets.RangeSlider('Range', range_text_value_number=3,
                                                 range_values=rv, default_value=(1, 4))
        menu.add.generic_widget(slider, True)
        slider.draw(surface)
