"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST EXAMPLES
Test example files.

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

__all__ = ['ExamplesTest']

from test._utils import test_reset_surface, MenuUtils, PygameEventUtils
import unittest

import pygame

import pygame_menu.examples.game_selector as game_selector
import pygame_menu.examples.multi_input as multi_input
import pygame_menu.examples.scroll_menu as scroll_menu
import pygame_menu.examples.timer_clock as timer_clock

import pygame_menu.examples.other.calculator as calculator
import pygame_menu.examples.other.dynamic_button_append as dynamic_button
import pygame_menu.examples.other.dynamic_widget_update as dynamic_widget
import pygame_menu.examples.other.image_background as image_background
import pygame_menu.examples.other.scrollbar as scroll_bar
import pygame_menu.examples.other.scrollbar_area as scroll_area
import pygame_menu.examples.other.ui_solar_system as ui_solarsystem


class ExamplesTest(unittest.TestCase):

    @staticmethod
    def test_example_timer_clock() -> None:
        """
        Test timer clock example.
        """
        timer_clock.main(test=True)
        timer_clock.mainmenu_background()
        timer_clock.reset_timer()
        test_reset_surface()

    @staticmethod
    def test_example_difficulty_selector() -> None:
        """
        Test multi-input example.
        """
        game_selector.main(test=True)
        font = MenuUtils.load_font(MenuUtils.random_font(), 5)
        game_selector.play_function(['EASY'], font, test=True)
        game_selector.play_function(['MEDIUM'], font, test=True)
        game_selector.play_function(['HARD'], font, test=True)
        test_reset_surface()

    @staticmethod
    def test_example_multi_input() -> None:
        """
        Test multi-input example.
        """
        multi_input.main(test=True)
        test_reset_surface()

    @staticmethod
    def test_example_scroll_menu() -> None:
        """
        Test scroll menu example.
        """
        scroll_menu.main(test=True)
        test_reset_surface()

    @staticmethod
    def test_example_simple() -> None:
        """
        Test example simple.
        """
        # noinspection PyUnresolvedReferences
        import pygame_menu.examples.simple
        test_reset_surface()

    @staticmethod
    def test_example_other_area_menu() -> None:
        """
        Test scrollarea example.
        """
        scroll_area.main(test=True)
        test_reset_surface()

    @staticmethod
    def test_example_other_scroll_bar() -> None:
        """
        Test scrollbar example.
        """
        scroll_bar.main(test=True)
        test_reset_surface()

    def test_example_other_calculator(self) -> None:
        """
        Test calculator example.
        """
        app = calculator.main(test=True)
        app.process_events(PygameEventUtils.keydown([pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                                     pygame.K_5, pygame.K_PLUS]))
        self.assertEqual(app.prev, '12345')
        self.assertEqual(app.op, '+')
        app.process_events(PygameEventUtils.keydown([pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9,
                                                     pygame.K_0]))
        self.assertEqual(app.curr, '67890')
        app.process_events(PygameEventUtils.keydown(pygame.K_EQUALS))
        self.assertEqual(app.op, '')
        self.assertEqual(app.curr, '80235')
        self.assertEqual(app.prev, '')
        app.process_events(PygameEventUtils.keydown([pygame.K_x, pygame.K_2]))
        self.assertEqual(app.op, 'x')
        self.assertEqual(app.curr, '2')
        self.assertEqual(app.prev, '80235')
        app.process_events(PygameEventUtils.keydown([pygame.K_x]))
        self.assertEqual(app.op, 'x')
        self.assertEqual(app.curr, '')
        self.assertEqual(app.prev, '160470')
        app.process_events(PygameEventUtils.keydown([pygame.K_PLUS, pygame.K_3, pygame.K_0]))
        self.assertEqual(app.op, '+')
        self.assertEqual(app.curr, '30')
        self.assertEqual(app.prev, '160470')
        app.process_events(PygameEventUtils.keydown(pygame.K_EQUALS))
        self.assertEqual(app.op, '')
        self.assertEqual(app.curr, '160500')
        self.assertEqual(app.prev, '')
        app.process_events(PygameEventUtils.keydown([pygame.K_SLASH, pygame.K_5, pygame.K_MINUS]))
        self.assertEqual(app.op, '-')
        self.assertEqual(app.curr, '')
        self.assertEqual(app.prev, '32100')
        app.process_events(PygameEventUtils.keydown([pygame.K_3, pygame.K_2, pygame.K_1, pygame.K_0, pygame.K_EQUALS]))
        self.assertEqual(app.op, '')
        self.assertEqual(app.curr, '28890')
        self.assertEqual(app.prev, '')
        app.process_events(PygameEventUtils.keydown([pygame.K_9, pygame.K_BACKSPACE]))
        self.assertEqual(app.op, '')
        self.assertEqual(app.curr, '')
        self.assertEqual(app.prev, '')
        test_reset_surface()

    @staticmethod
    def test_example_other_dynamic_button() -> None:
        """
        Test dynamic button example.
        """
        dynamic_button.add_dynamic_button()
        btn = dynamic_button.menu.get_selected_widget()
        btn.apply()
        dynamic_button.main(test=True)
        test_reset_surface()

    @staticmethod
    def test_example_other_dynamic_widget() -> None:
        """
        Test dynamic widget update example.
        """
        app = dynamic_widget.App()
        app.current = 3
        app.animate_quit_button(app.quit_button, app.menu)
        dynamic_widget.main(test=True)
        test_reset_surface()

    @staticmethod
    def test_example_other_background_image() -> None:
        """
        Test background image example.
        """
        image_background.main(test=True)
        test_reset_surface()

    def test_example_other_ui_solar_system(self) -> None:
        """
        Test solar system.
        """
        app = ui_solarsystem.main(test=True)
        self.assertFalse(app.menu._disable_draw)
        app.process_events(PygameEventUtils.keydown([pygame.K_p]), app.menu)
        self.assertTrue(app.menu._disable_draw)
        app.process_events(PygameEventUtils.keydown([pygame.K_p, pygame.K_q, pygame.K_e, pygame.K_s, pygame.K_c]),
                           app.menu)
        self.assertFalse(app.menu._disable_draw)
        test_reset_surface()
