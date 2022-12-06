"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - SELECTOR
Test Selector widget.
"""

__all__ = ['SelectorWidgetTest']

from test._utils import MenuUtils, surface, PygameEventUtils, BaseTest

import pygame_menu
import pygame_menu.controls as ctrl


class SelectorWidgetTest(BaseTest):

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
        selector.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
        selector.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
        selector.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        selector.update(PygameEventUtils.joy_hat_motion(ctrl.JOY_LEFT))
        selector.update(PygameEventUtils.joy_hat_motion(ctrl.JOY_RIGHT))
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

        # Test left/right touch
        click_pos = selector.get_rect(to_real_position=True, apply_padding=False).midleft
        selector._touchscreen_enabled = True
        selector.update(PygameEventUtils.touch_click(click_pos[0] + 150, click_pos[1], menu=selector.get_menu()))
        self.assertEqual(selector.get_index(), 2)
        selector.update(PygameEventUtils.touch_click(click_pos[0] + 250, click_pos[1], menu=selector.get_menu()))
        self.assertEqual(selector.get_index(), 0)
        selector.update(PygameEventUtils.touch_click(click_pos[0] + 250, click_pos[1], menu=selector.get_menu()))
        self.assertEqual(selector.get_index(), 1)

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
        selector.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
        self.assertEqual(selector.get_value()[0][0], '4 - Easy')
        selector.readonly = True
        selector.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
        self.assertEqual(selector.get_value()[0][0], '4 - Easy')
        selector._left()
        self.assertEqual(selector.get_value()[0][0], '4 - Easy')
        selector._right()
        self.assertEqual(selector.get_value()[0][0], '4 - Easy')

        # Test fancy selector
        sel_fancy = menu.add.selector(
            'Fancy ',
            [('1 - Easy', 'EASY'),
             ('2 - Medium', 'MEDIUM'),
             ('3 - Hard', 'HARD')],
            default=1,
            style=pygame_menu.widgets.widget.selector.SELECTOR_STYLE_FANCY
        )
        self.assertEqual(sel_fancy.get_items(), [('1 - Easy', 'EASY'),
                                                 ('2 - Medium', 'MEDIUM'),
                                                 ('3 - Hard', 'HARD')])
        self.assertRaises(AssertionError, lambda: menu.add.selector(
            'title', [('a', 'a'), ('b', 'b')], default=2))

    def test_value(self) -> None:
        """
        Test selector value.
        """
        menu = MenuUtils.generic_menu()
        sel = menu.add.selector('title', [('a', 'a'), ('b', 'b')], default=1)

        self.assertEqual(sel.get_value(), (('b', 'b'), 1))
        self.assertFalse(sel.value_changed())
        sel.set_value('a')
        self.assertEqual(sel.get_value(), (('a', 'a'), 0))
        self.assertTrue(sel.value_changed())
        sel.reset_value()
        self.assertEqual(sel.get_value(), (('b', 'b'), 1))
        self.assertFalse(sel.value_changed())

    def test_empty_title(self) -> None:
        """
        Test empty title.
        """
        menu = MenuUtils.generic_menu()
        sel = menu.add.selector('', [('a', 'a'), ('b', 'b')])
        self.assertEqual(sel.get_size(), (83, 49))
