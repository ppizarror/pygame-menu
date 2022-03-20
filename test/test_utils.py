"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST UTILS
Library utils.
"""

__all__ = ['UtilsTest']

from test._utils import BaseTest

from pygame_menu.locals import POSITION_NORTHWEST

import pygame_menu
import pygame_menu.utils as ut


class UtilsTest(BaseTest):

    def test_callable(self) -> None:
        """
        Test is callable.
        """
        self.assertTrue(ut.is_callable(bool))
        self.assertFalse(ut.is_callable(1))

    def test_position_str(self) -> None:
        """
        Test position assert values as str.
        """
        self.assertIsNone(ut.assert_position_vector(POSITION_NORTHWEST))

    def test_padding(self) -> None:
        """
        Padding test.
        """
        self.assertEqual(ut.parse_padding(1.0), (1, 1, 1, 1))
        self.assertEqual(ut.parse_padding(1.05), (1, 1, 1, 1))
        self.assertEqual(ut.parse_padding([1.0]), (1, 1, 1, 1))
        self.assertEqual(ut.parse_padding((1.0,)), (1, 1, 1, 1))

    def test_terminal_widget_title(self) -> None:
        """
        Test terminal title.
        """
        w = pygame_menu.widgets.Button('epic')
        w.hide()
        s = ut.widget_terminal_title(w)
        self.assertIn('╳', s)

    def test_shadows(self) -> None:
        """
        Test shadows.
        """
        shadow = ut.ShadowGenerator()
        s1 = shadow.create_new_rectangle_shadow(100, 100, 15, 25)
        s2 = shadow.create_new_ellipse_shadow(100, 100, 10)
        shadow.create_new_ellipse_shadow(100, 100, 10)
        self.assertIsNone(shadow.create_new_ellipse_shadow(100, 100, 0))
        self.assertEqual(s1.get_size(), (100, 100))
        self.assertEqual(s2.get_size(), (100, 100))
        # Use cache
        shadow.create_new_rectangle_shadow(100, 100, 15, 25)
        shadow.create_new_rectangle_shadow(100, 150, 15, 25)
        # Remove cache
        shadow.clear_short_term_caches(force=True)
