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
