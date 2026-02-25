"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - BUTTON
Test Button widget.
"""

from __future__ import annotations

__all__ = ['ButtonWidgetTest']

from test._utils import (PYGAME_V2, BaseTest, MenuUtils, PygameEventUtils,
                         surface)

import pygame

import pygame_menu
from pygame_menu.themes import THEME_DEFAULT
from pygame_menu.widgets import Button
from pygame_menu.widgets.core.widget import WIDGET_SHADOW_TYPE_ELLIPSE


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
            self.assertIsNotNone(menu.add.button('b1', v))

        btn = menu.add.button('b1', menu2)
        for v in [menu, 1, [1, 2, 3], (1, 2, 3)]:
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
        self.assertTrue(btn._ignores_keyboard_nonphysical())
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

    def test_empty_title(self) -> None:
        """
        Test empty title.
        """
        menu = MenuUtils.generic_menu()
        btn = menu.add.button('')
        p = btn._padding
        self.assertEqual(btn.get_width(), p[1] + p[3])
        self.assertEqual(btn.get_height(), p[0] + p[2] + 41 if PYGAME_V2 else 42)

    def test_shadow(self) -> None:
        """
        Test button shadow.
        """
        menu = MenuUtils.generic_menu()
        menu.add.button('my button')
        btn = menu.add.button('my buton 2')
        btn.shadow(shadow_width=20, color='black')
        self.assertTrue(btn._shadow['enabled'])
        self.assertEqual(btn._shadow['properties'][4], (0, 0, 0))
        btn.shadow(shadow_width=0, color=(250, 250, 30, 40))
        self.assertFalse(btn._shadow['enabled'])
        self.assertEqual(btn._shadow['properties'][4], (250, 250, 30))
        self.assertIsNone(btn._shadow['surface'])
        btn.shadow(shadow_width=0, color=(250, 250, 100))
        self.assertFalse(btn._shadow['enabled'])
        self.assertEqual(btn._shadow['properties'][4], (250, 250, 100))

        # Check size modify
        btn.shadow(shadow_width=20, color='black')
        self.assertIsNone(btn._shadow['surface'])
        btn.draw(surface)
        self.assertIsNotNone(btn._shadow['surface'])
        s = btn._shadow['surface'].get_size()
        self.assertEqual(btn.get_size()[0] + 40, s[0])
        self.assertEqual(btn.get_size()[1] + 40, s[1])

        btn.scale(2, 2)
        self.assertIsNone(btn._shadow['surface'])
        btn.draw(surface)
        s = btn._shadow['surface'].get_size()
        self.assertEqual(btn.get_size()[0] + 40, s[0])
        self.assertEqual(btn.get_size()[1] + 40, s[1])

        # Add ellipse shadow
        btn2 = menu.add.button('my buton 3')
        btn2.shadow(WIDGET_SHADOW_TYPE_ELLIPSE, 50)
        btn2.draw(surface)

        # Set invalid width
        btn2.shadow(corner_radius=4000)
        self.assertTrue(btn2._shadow['enabled'])
        btn2.draw(surface)
        self.assertFalse(btn2._shadow['enabled'])

    def test_value(self) -> None:
        """
        Test button value.
        """
        menu = MenuUtils.generic_menu()
        btn = menu.add.button('button')
        self.assertRaises(ValueError, lambda: btn.get_value())
        self.assertRaises(ValueError, lambda: btn.set_value('value'))
        self.assertFalse(btn.value_changed())
        btn.reset_value()

    def test_add_url(self) -> None:
        """
        Test add url.
        """
        menu = MenuUtils.generic_menu()
        self.assertRaises(AssertionError, lambda: menu.add.url('invalid'))
        self.assertRaises(AssertionError, lambda: menu.add.url('127.0.0.1'))
        btn = menu.add.url('https://127.0.0.1')
        self.assertEqual(btn.get_title(), 'https://127.0.0.1')
        btn2 = menu.add.url('https://github.com/ppizarror/pygame-menu', 'github')
        self.assertEqual(btn2.get_title(), 'github')

    def test_controller(self) -> None:
        """
        Test controller.
        """
        theme = THEME_DEFAULT.copy()
        menu = MenuUtils.generic_menu(theme=theme)
        from random import randrange

        from pygame_menu.controls import Controller
        custom_controller = Controller()
        test = [0]

        # noinspection PyMissingOrEmptyDocstring
        def btn_apply(event, _) -> bool:
            applied = event.key in (pygame.K_a, pygame.K_b, pygame.K_c)
            if applied:
                menu.get_scrollarea().update_area_color((randrange(0, 255), randrange(0, 255), randrange(0, 255)))
                test[0] += 1
            return applied

        custom_controller.apply = btn_apply
        btn = menu.add.button('My button', lambda: print('Clicked!'))
        btn.set_controller(custom_controller)
        menu.update(PygameEventUtils.keydown(pygame.K_d))
        self.assertEqual(test[0], 0)
        menu.update(PygameEventUtils.keydown(pygame.K_a))
        self.assertEqual(test[0], 1)
        menu.update(PygameEventUtils.keydown(pygame.K_b))
        self.assertEqual(test[0], 2)
        menu.update(PygameEventUtils.keydown(pygame.K_c))
        self.assertEqual(test[0], 3)

        # Test select
        self.assertTrue(btn.update(PygameEventUtils.joy_button(pygame_menu.controls.JOY_BUTTON_SELECT)))

    def test_button_image(self) -> None:
        """
        Test button with an image.
        """
        menu = MenuUtils.generic_menu()

        # Test existing BaseImage support
        image = pygame_menu.BaseImage(
            image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU
        ).scale(0.25, 0.25)

        btn = menu.add.banner(image)

        # Size must match the BaseImage
        self.assertEqual(btn.get_width(), image.get_width())
        self.assertEqual(btn.get_height(), image.get_height())

        # Banner text is always a single space
        self.assertEqual(btn.get_title(), ' ')

        # Padding override (default = 0)
        self.assertEqual(btn._padding, (0, 0, 0, 0))

        # Selection color override (transparent)
        self.assertEqual(btn._selection_effect.color, (0, 0, 0, 0))

        # Test pygame.Surface support
        surf_size = (120, 60)
        raw_surf = pygame.Surface(surf_size)
        btn_from_surf = menu.add.banner(raw_surf)

        # Size must match the raw surface
        self.assertEqual(btn_from_surf.get_width(), surf_size[0])
        self.assertEqual(btn_from_surf.get_height(), surf_size[1])

        # Internally converted to BaseImage
        self.assertIsInstance(btn_from_surf._background_color, pygame_menu.BaseImage)

        # Padding override still applies
        self.assertEqual(btn_from_surf._padding, (0, 0, 0, 0))

        # Transparent selection color still applies
        self.assertEqual(btn_from_surf._selection_effect.color, (0, 0, 0, 0))

        # Verify Selection Fix (NoneSelection)
        from pygame_menu.widgets import NoneSelection
        self.assertIsInstance(btn_from_surf.get_selection_effect(), NoneSelection)

        # Ensure theme selection effect did NOT leak through
        theme_effect_type = type(menu.get_theme().widget_selection_effect)
        self.assertNotEqual(type(btn_from_surf.get_selection_effect()), theme_effect_type)

    def test_multiline(self) -> None:
        """
        Test multiline button capabilities.
        """
        menu = MenuUtils.generic_menu()
        s = 'lorem ipsum dolor sit amet this was very important nice a test is required ' \
            'lorem ipsum dolor sit amet this was very important nice a test is required'
        button = menu.add.button(s, wordwrap=True, max_nlines=3)  # Maximum number of lines
        self.assertEqual(len(button.get_lines()), 3)  # The widget needs 4 lines, but maximum is 3
        self.assertEqual(button.get_height(), 131)
        self.assertEqual(button.get_overflow_lines(), ['important nice a test is required'])

        # Test multiline within Frame
        f1 = menu.add.frame_h(200, 200)
        f1.pack(button)
        self.assertEqual(button.get_overflow_lines(),
                         ['required', 'nice a test is', 'important', 'was very', 'amet this', 'dolor sit',
                          'lorem ipsum', 'required', 'nice a test is', 'important', 'was very'])
        self.assertLessEqual(abs(button.get_width() - button._get_max_container_width()), 2)

        # Taking button out from Frame must restore its container and reassemble wrap
        f1.unpack(button)
        self.assertEqual(button.get_overflow_lines(), ['important nice a test is required'])

    def test_banner_respects_user_padding(self):
        menu = MenuUtils.generic_menu()
        surf = pygame.Surface((40, 40))
        btn = menu.add.banner(surf, padding=(5, 10, 5, 10))
        self.assertEqual(btn._padding, (5, 10, 5, 10))

    def test_banner_respects_user_selection_effect(self):
        menu = MenuUtils.generic_menu()
        from pygame_menu.widgets import HighlightSelection
        custom = HighlightSelection()
        image = pygame.Surface((50, 50))
        btn = menu.add.banner(image, selection_effect=custom)
        # User override must win → same TYPE, not same INSTANCE
        self.assertIsInstance(btn._selection_effect, HighlightSelection)

    def test_banner_inside_frame(self):
        menu = MenuUtils.generic_menu()
        frame = menu.add.frame_h(200, 200)
        surf = pygame.Surface((80, 30))
        btn = menu.add.banner(surf)
        frame.pack(btn)
        # Width must not exceed frame width
        self.assertLessEqual(btn.get_width(), frame.get_width())

    def test_banner_height_not_affected_by_text(self):
        menu = MenuUtils.generic_menu()
        surf = pygame.Surface((100, 40))
        btn = menu.add.banner(surf)
        self.assertEqual(btn.get_height(), 40)

    def test_banner_apply_via_event(self):
        menu = MenuUtils.generic_menu()
        applied = [False]

        def cb():
            applied[0] = True

        surf = pygame.Surface((60, 60))
        menu.add.banner(surf, cb)
        events = PygameEventUtils.keydown(pygame_menu.controls.KEY_APPLY)
        menu.update(events)
        self.assertTrue(applied[0])

    def test_banner_respects_user_cursor(self):
        menu = MenuUtils.generic_menu()
        surf = pygame.Surface((50, 50))
        btn = menu.add.banner(surf, cursor=pygame.SYSTEM_CURSOR_CROSSHAIR)
        self.assertEqual(btn._cursor, pygame.SYSTEM_CURSOR_CROSSHAIR)

    def test_banner_float_behavior(self):
        menu = MenuUtils.generic_menu()
        surf = pygame.Surface((30, 30))
        btn = menu.add.banner(surf, float=True)
        self.assertTrue(btn.is_floating())
