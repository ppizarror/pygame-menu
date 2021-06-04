"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - BUTTON
Test Button widget.

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

__all__ = ['ButtonWidgetTest']

from test._utils import MenuUtils, surface, PygameEventUtils, BaseTest

import pygame
import pygame_menu

from pygame_menu.widgets import Button


class ButtonWidgetTest(BaseTest):

    def test_button(self) -> None:
        """
        Test button widget.
        """
        menu = MenuUtils.generic_menu()
        menu2 = MenuUtils.generic_menu()

        # Valid
        def test() -> bool:
            """
            Callback.
            """
            return True

        # Invalid ones
        invalid = [
            bool,  # type
            object,  # object
            1,  # int
            'a',  # str
            True,  # bool
            pygame,  # module
            surface,  # pygame
            1.1,  # float
            menu.add.button('eee'),  # widget
            [1, 2, 3],  # list
            (1, 2, 3),  # tuple
            pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)  # baseimage
        ]
        for i in invalid:
            self.assertRaises(ValueError, lambda: menu.add.button('b1', i))

        # Valid
        valid = [
            menu2,
            test,
            pygame_menu.events.NONE,
            pygame_menu.events.PYGAME_QUIT,
            pygame_menu.events.PYGAME_WINDOWCLOSE,
            None,
            lambda: test(),
            None
        ]
        for v in valid:
            self.assertTrue(menu.add.button('b1', v) is not None)

        btn = menu.add.button('b1', menu2)
        for v in [menu, 1, bool, object, [1, 2, 3], (1, 2, 3)]:
            self.assertRaises(AssertionError, lambda: btn.update_callback(v))
        btn.update_callback(test)

        # Invalid recursive menu
        self.assertRaises(ValueError, lambda: menu.add.button('bt', menu))

        # Test callback
        test = [False]

        def callback(t=False) -> None:
            """
            Callback.
            """
            test[0] = t

        btn = Button('epic', t=True, onreturn=callback)
        btn.apply()
        self.assertTrue(test[0])
        test[0] = False

        def callback() -> None:
            """
            Callback.
            """
            test[0] = False

        btn = Button('epic', onreturn=callback)
        btn.apply()
        self.assertFalse(test[0])

        # Test with no kwargs
        def callback(**kwargs) -> None:
            """
            Callback.
            """
            self.assertEqual(len(kwargs.keys()), 0)

        btn = menu.add.button('epic', callback, accept_kwargs=False)
        btn.apply()

        # Test with kwargs
        def callback(**kwargs) -> None:
            """
            Callback.
            """
            self.assertEqual(len(kwargs.keys()), 1)
            self.assertTrue(kwargs.get('key', False))

        btn = Button('epic', onreturn=callback, key=True)
        btn.apply()
        btn = menu.add.button('epic', callback, accept_kwargs=True, key=True)
        btn.apply()

        # Test pygame events
        btn = menu.add.button('epic', pygame_menu.events.PYGAME_QUIT)
        self.assertEqual(btn._onreturn, menu._exit)
        btn = menu.add.button('epic', pygame_menu.events.PYGAME_WINDOWCLOSE)
        self.assertEqual(btn._onreturn, menu._exit)

        # Test None
        btn = menu.add.button('epic', pygame_menu.events.NONE)
        self.assertIsNone(btn._onreturn)
        btn = menu.add.button('epic')
        self.assertIsNone(btn._onreturn)

        # Test invalid kwarg
        self.assertRaises(ValueError, lambda: menu.add.button('epic', callback, key=True))

        # Remove button
        menu.remove_widget(btn)
        self.assertRaises(ValueError, lambda: menu.remove_widget(btn))

        # Test underline
        # Add underline
        btn = menu.add.button('epic', pygame_menu.events.NONE)
        self.assertEqual(btn._decorator._total_decor(), 0)
        btn.add_underline((0, 0, 0), 1, 1, force_render=True)
        self.assertNotEqual(btn._last_underline[0], '')
        self.assertEqual(btn._decorator._total_decor(), 1)
        btn.remove_underline()
        self.assertEqual(btn._last_underline[0], '')

        # Test return fun
        def fun() -> str:
            """
            This should return "nice".
            """
            return 'nice'

        btn = menu.add.button('', fun)
        self.assertEqual(btn.apply(), 'nice')
        btn.readonly = True
        self.assertIsNone(btn.apply())
        self.assertFalse(btn.update(PygameEventUtils.keydown(pygame_menu.controls.KEY_APPLY)))

        # Test button to menu
        btn_menu = menu.add.button('to2', menu2)
        self.assertTrue(btn_menu.to_menu)
        menu.full_reset()
        self.assertTrue(btn_menu.update(PygameEventUtils.keydown(pygame_menu.controls.KEY_APPLY)))
        self.assertEqual(menu.get_current(), menu2)
        menu.full_reset()
        self.assertEqual(menu.get_current(), menu)

        # Warns if adding button to menu
        btn.set_menu(None)
        btn.to_menu = True
        menu2.add.generic_widget(btn)

        # Test extreme resize
        btn.resize(1, 1)
        btn.set_max_height(None)
        btn.set_max_width(None)
        btn.flip(True, True)
        self.assertEqual(btn._flip, (True, True))

        # Test consistency if active
        btn.active = True
        btn._selected = False
        btn.draw(surface)
        self.assertFalse(btn.active)

        # Try onchange
        btn._onchange = lambda: None
        self.assertIsNone(btn.change())
