"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - TOGGLESWITCH
Test ToggleSwitch widget.
"""

__all__ = ['ToggleSwitchWidgetTest']

from test._utils import MenuUtils, surface, PygameEventUtils, BaseTest

import pygame_menu
import pygame_menu.controls as ctrl

from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented


class ToggleSwitchWidgetTest(BaseTest):

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

        switch = menu.add.toggle_switch('toggle', False, onchange=onchange, infinite=False, single_click=False)
        self.assertFalse(switch.get_value())
        self.assertIsNone(value[0])
        switch.apply()
        self.assertFalse(value[0])

        switch.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))  # not infinite
        self.assertFalse(value[0])  # as this is false, don't change
        switch.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
        self.assertTrue(value[0])
        switch.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
        self.assertFalse(value[0])
        switch.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
        self.assertFalse(value[0])
        self.assertFalse(switch.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True, testmode=False)))

        switch = menu.add.toggle_switch('toggle', False, onchange=onchange, infinite=True, single_click=False)
        switch.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
        self.assertTrue(value[0])
        switch.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
        self.assertFalse(value[0])

        # As there's only 2 states, return should change too
        switch.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        self.assertTrue(value[0])
        switch.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        self.assertFalse(value[0])

        # Check left/right clicks
        click_pos = switch.get_rect(to_real_position=True, apply_padding=False).midleft
        switch.update(PygameEventUtils.mouse_click(click_pos[0] + 150, click_pos[1]))
        self.assertFalse(value[0])
        switch.update(PygameEventUtils.mouse_click(click_pos[0] + 250, click_pos[1]))
        self.assertTrue(value[0])
        switch.update(PygameEventUtils.mouse_click(click_pos[0] + 150, click_pos[1]))
        self.assertFalse(value[0])

        # Test left/right touch
        switch._touchscreen_enabled = True
        switch.update(PygameEventUtils.touch_click(click_pos[0] + 250, click_pos[1], menu=switch.get_menu()))
        self.assertTrue(value[0])
        switch.update(PygameEventUtils.touch_click(click_pos[0] + 250, click_pos[1], menu=switch.get_menu()))
        self.assertTrue(value[0])
        switch.update(PygameEventUtils.touch_click(click_pos[0] + 150, click_pos[1], menu=switch.get_menu()))
        self.assertFalse(value[0])

        # Test readonly
        switch.readonly = True
        switch.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        self.assertFalse(value[0])
        switch.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        self.assertFalse(value[0])
        switch.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        self.assertFalse(value[0])
        switch._left()
        self.assertFalse(value[0])
        switch._right()
        self.assertFalse(value[0])

        switch.readonly = False
        switch.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
        self.assertTrue(value[0])
        switch.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
        self.assertFalse(value[0])

        switch.draw(surface)

        # Test transforms
        switch.set_position(1, 1)
        self.assertEqual(switch.get_position(), (1, 1))

        switch.translate(1, 1)
        self.assertEqual(switch.get_translate(), (1, 1))

        self.assertRaises(WidgetTransformationNotImplemented, lambda: switch.rotate(10))
        self.assertEqual(switch._angle, 0)

        self.assertRaises(WidgetTransformationNotImplemented, lambda: switch.scale(100, 100))
        self.assertFalse(switch._scale[0])
        self.assertEqual(switch._scale[1], 1)
        self.assertEqual(switch._scale[2], 1)

        self.assertRaises(WidgetTransformationNotImplemented, lambda: switch.resize(100, 100))
        self.assertFalse(switch._scale[0])
        self.assertEqual(switch._scale[1], 1)
        self.assertEqual(switch._scale[2], 1)

        self.assertRaises(WidgetTransformationNotImplemented, lambda: switch.flip(True, True))
        self.assertFalse(switch._flip[0])
        self.assertFalse(switch._flip[1])

        self.assertRaises(WidgetTransformationNotImplemented, lambda: switch.set_max_width(100))
        self.assertIsNone(switch._max_width[0])

        self.assertRaises(WidgetTransformationNotImplemented, lambda: switch.set_max_height(100))
        self.assertIsNone(switch._max_height[0])

        # Assert switch values
        self.assertRaises(ValueError, lambda: menu.add.toggle_switch('toggle', 'false', onchange=onchange, infinite=False))

        # Test single click toggle
        switch_single = menu.add.toggle_switch('toggle', False, onchange=onchange)
        self.assertTrue(switch_single._infinite)  # Infinite sets to True if using single click

        self.assertFalse(switch_single.get_value())
        switch_single._left()
        self.assertTrue(switch_single.get_value())

        click_pos = switch_single.get_rect(to_real_position=True, apply_padding=False).midleft

        # Test single click toggle between two states
        switch_single.update(PygameEventUtils.mouse_click(click_pos[0] + 150, click_pos[1]))
        self.assertFalse(switch_single.get_value())  # single_click_dir=True, move to left
        switch_single.update(PygameEventUtils.mouse_click(click_pos[0] + 250, click_pos[1]))
        self.assertTrue(switch_single.get_value())
        switch_single.update(PygameEventUtils.mouse_click(click_pos[0] + 250, click_pos[1]))
        self.assertFalse(switch_single.get_value())

        switch_single._single_click_dir = False
        switch_single.update(PygameEventUtils.mouse_click(click_pos[0] + 250, click_pos[1]))
        self.assertTrue(switch_single.get_value())

        # Create invalid single click params
        self.assertRaises(AssertionError, lambda: menu.add.toggle_switch('toggle', False, single_click='true'))
        self.assertRaises(AssertionError, lambda: menu.add.toggle_switch('toggle', False, single_click_dir='true'))

        # Test other constructor params
        pygame_menu.widgets.ToggleSwitch('Epic', state_text_font=menu._theme.widget_font)
        self.assertRaises(AssertionError, lambda: pygame_menu.widgets.ToggleSwitch('Epic', state_text_font_size=-1))

    def test_value(self) -> None:
        """
        Test toggleswitch value.
        """
        menu = MenuUtils.generic_menu()
        switch = menu.add.toggle_switch('toggle', False)
        self.assertEqual(switch._default_value, 0)
        self.assertFalse(switch.value_changed())
        switch.set_value(1)
        self.assertEqual(switch.get_value(), 1)
        self.assertTrue(switch.value_changed())
        switch.reset_value()
        self.assertEqual(switch.get_value(), 0)
        self.assertFalse(switch.value_changed())

    def test_empty_title(self) -> None:
        """
        Test empty title.
        """
        menu = MenuUtils.generic_menu()
        switch = menu.add.toggle_switch('')
        self.assertEqual(switch.get_size(), (191, 49))

    def test_update_font(self) -> None:
        """
        Test update font.
        """
        menu = MenuUtils.generic_menu()
        switch = menu.add.toggle_switch('abc')
        self.assertEqual(switch.get_size(), (240, 49))
        self.assertEqual(switch._state_font.get_height(), 41)
        switch.update_font(dict(size=100))
        self.assertEqual(switch._state_font.get_height(), 137)
        self.assertEqual(switch.get_size(), (356, 145))
