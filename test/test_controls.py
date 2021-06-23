"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST CONTROLS
Test controls configuration.

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

__all__ = ['ControlsTest']

from test._utils import MenuUtils, PygameEventUtils, BaseTest

import pygame
import os

# Fix pyautogui travis tests
if 'DISPLAY' not in os.environ.keys():
    os.environ['DISPLAY'] = ':0'

# noinspection PyPackageRequirements
from pyautogui import press

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

        # Rollback change
        ctrl.KEY_APPLY = pygame.K_RETURN

        button.update(PygameEventUtils.key(pygame.K_END, keydown=True))
        self.assertTrue(test[0])
        button.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        self.assertFalse(test[0])

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
        self.assertTrue(down)
        self.assertEqual(main_menu.get_index(), 0)

        main_menu.update(events)
        self.assertEqual(main_menu.get_index(), 0)  # Does not changed

        main_menu._keyboard_ignore_nonphysical = False
        main_menu.update(events)
        self.assertEqual(main_menu.get_index(), 1)  # Does not changed

        # Ignore only applies to menus, currently appended widgets does not change
        self.assertTrue(b0._keyboard_ignore_nonphysical)
        self.assertFalse(b0._ignores_keyboard_nonphysical())
