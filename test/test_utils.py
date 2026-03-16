"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST UTILS
Library utils.
"""

import pytest

import pygame_menu.utils as ut
from pygame_menu.locals import POSITION_NORTHWEST
from pygame_menu.widgets.widget.button import Button


def test_alpha():
    assert ut._ALPHA_CHANNEL[0] is True

    ut.configure_alpha(False)
    assert ut._ALPHA_CHANNEL[0] is False

    ut.configure_alpha(True)
    assert ut._ALPHA_CHANNEL[0] is True


def test_callable():
    assert ut.is_callable(bool)
    assert not ut.is_callable(1)


def test_position_str():
    assert ut.assert_position_vector(POSITION_NORTHWEST) is None


@pytest.mark.parametrize(
    "value,expected",
    [
        (1.0, (1, 1, 1, 1)),
        (1.05, (1, 1, 1, 1)),
        ([1.0], (1, 1, 1, 1)),
        ((1.0,), (1, 1, 1, 1)),
    ],
)
def test_padding(value, expected):
    assert ut.parse_padding(value) == expected


def test_terminal_widget_title():
    w = Button("epic")
    w.hide()
    s = ut.widget_terminal_title(w)
    assert "╳" in s


def test_shadows():
    shadow = ut.ShadowGenerator()

    s1 = shadow.create_new_rectangle_shadow(100, 100, 15, 25)
    s2 = shadow.create_new_ellipse_shadow(100, 100, 10)

    shadow.create_new_ellipse_shadow(100, 100, 10)  # cached
    assert shadow.create_new_ellipse_shadow(100, 100, 0) is None

    assert s1.get_size() == (100, 100)
    assert s2.get_size() == (100, 100)

    shadow.create_new_rectangle_shadow(100, 100, 15, 25)  # cached
    shadow.create_new_rectangle_shadow(100, 150, 15, 25)

    shadow.clear_short_term_caches(force=True)
