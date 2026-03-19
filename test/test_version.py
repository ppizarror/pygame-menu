"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST VERSION
Test version management.
"""

import pygame_menu


def test_version_types():
    """Test version."""
    assert isinstance(pygame_menu.version.ver, str)
    assert isinstance(repr(pygame_menu.version.vernum), str)
    assert isinstance(str(pygame_menu.version.vernum), str)
