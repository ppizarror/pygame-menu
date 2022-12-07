"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST CONTROLS
Test controls configuration.
"""

__all__ = ['ControlsTest']

from test._utils import MenuUtils, PygameEventUtils, BaseTest

import pygame
import os


# Fix pyautogui tests
def press(key: str) -> None:
    """
    Press a key.
    """
    print(key)


PY_AUTO_GUI = False
if 'DISPLAY' in os.environ.keys():
    try:
        # noinspection PyPackageRequirements,PyUnresolvedReferences
        from pyautogui import press

        PY_AUTO_GUI = True
    except (ImportError, ModuleNotFoundError, FileNotFoundError, KeyError):
        pass

import pygame_menu.controls as ctrl


class ControlsTest(BaseTest):

    def test_config(self) -> None:
        """
        Configure controls.
        """
        self.assertEqual(ctrl.KEY_APPLY, pygame.K_RETURN)

        # Change apply to new key
        ctrl.KEY_APPLY = pygame.K_END
        self.assertEqual(ctrl.KEY_APPLY, pygame.K_END)

        # Create new button
        menu = MenuUtils.generic_menu()
        test = [False]

        def click_button() -> None:
            """
            Button apply handler.
            """
            test[0] = not test[0]
            print('new test value', test)

        button = menu.add.button('button', click_button)
        self.assertFalse(test[0])
        button.apply()
        self.assertTrue(test[0])
        button.apply()
        self.assertFalse(test[0])

        # Now test new apply button
        button.update(PygameEventUtils.key(pygame.K_END, keydown=True))
        self.assertTrue(test[0])
        button.update(PygameEventUtils.key(pygame.K_END, keydown=True))
        self.assertFalse(test[0])

        # Rollback change
        ctrl.KEY_APPLY = pygame.K_RETURN

        # Create new controller object
        new_ctrl = ctrl.Controller()
        test_apply = [0]

        def new_apply(event, _) -> bool:
            """
            Updates apply.
            """
            test_apply[0] += 1
            return event.key == pygame.K_a

        new_ctrl.apply = new_apply
        button.set_controller(new_ctrl)
        self.assertEqual(button.get_controller(), new_ctrl)

        # Now test new apply button
        button.update(PygameEventUtils.key(pygame.K_a, keydown=True))
        self.assertTrue(test[0])
        button.update(PygameEventUtils.key(pygame.K_a, keydown=True))
        self.assertFalse(test[0])
        self.assertEqual(test_apply[0], 2)

        button.update(PygameEventUtils.key(pygame.K_END, keydown=True))
        self.assertFalse(test[0])
        button.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        self.assertFalse(test[0])  # It should do nothing as object has new controller

        # Test selector apply
        sel_apply = [False]
        joy_apply = [False]

        def custom_widget_apply(event, _) -> bool:
            """
            Custom widget apply event.
            """
            condition = event.key == pygame.K_SPACE
            sel_apply[0] = condition
            return condition

        def custom_joy_apply(event, _) -> bool:
            """
            Custom widget apply event.
            """
            condition = event.button == 8
            joy_apply[0] = condition
            return condition

        new_ctrl_sel = ctrl.Controller()
        new_ctrl_sel.apply = custom_widget_apply
        new_ctrl_sel.joy_select = custom_joy_apply

        selector = menu.add.selector('select', ['a', 'b', 'c'])
        selector.set_controller(new_ctrl_sel)
        selector.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        self.assertFalse(sel_apply[0])
        selector.update(PygameEventUtils.key(pygame.K_SPACE, keydown=True))
        self.assertTrue(sel_apply[0])
        selector.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))  # Rollback
        self.assertFalse(sel_apply[0])

        # Now tests joy buttons
        self.assertFalse(joy_apply[0])
        selector.update(PygameEventUtils.joy_button(8))
        self.assertTrue(joy_apply[0])

        # The same can be done with menu
        original_controller = menu.get_controller()
        menu.set_controller(new_ctrl)
        self.assertEqual(menu.get_controller(), new_ctrl)

        # Check set controller but to widgets
        self.assertEqual(button.get_controller(), new_ctrl)
        menu.set_controller(original_controller, True)
        self.assertEqual(button.get_controller(), original_controller)

    def test_pyautogui(self) -> None:
        """
        Test pyautogui support.
        """
        main_menu = MenuUtils.generic_menu()

        b0 = main_menu.add.button('Input Test')
        main_menu.add.button('Steering Wheel Test')
        main_menu.add.button('Motor Test')
        main_menu.add.button('Coin Chute Test')
        main_menu.add.button('Time Settings')

        # Menu ignores non physical events
        press('down')  # This emulates the arrow down key being pressed
        events = pygame.event.get()  # The press down is captured here
        down = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_LEFT:
                #     print('Left')
                # elif event.key == pygame.K_RIGHT:
                #     print('Right')
                # elif event.key == pygame.K_UP:
                #     print('Up')
                if event.key == pygame.K_DOWN:
                    down = True
        if PY_AUTO_GUI:
            self.assertTrue(down)
        else:
            self.assertFalse(down)
        self.assertEqual(main_menu.get_index(), 0)

        main_menu.update(events)
        self.assertEqual(main_menu.get_index(), 0)  # Does not change

        main_menu._keyboard_ignore_nonphysical = False
        main_menu.update(events)
        self.assertEqual(main_menu.get_index(), 1 if PY_AUTO_GUI else 0)  # Does not change

        # Ignore only applies to menus, currently appended widgets does not change
        self.assertTrue(b0._keyboard_ignore_nonphysical)
        self.assertFalse(b0._ignores_keyboard_nonphysical())
