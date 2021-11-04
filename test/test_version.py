"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST VERSION
Test version management.
"""

__all__ = ['VersionTest']

from test._utils import BaseTest

import pygame_menu


class VersionTest(BaseTest):

    def test_version(self) -> None:
        """
        Test version.
        """
        self.assertTrue(isinstance(pygame_menu.version.ver, str))
        self.assertTrue(isinstance(repr(pygame_menu.version.vernum), str))
        self.assertTrue(isinstance(str(pygame_menu.version.vernum), str))
