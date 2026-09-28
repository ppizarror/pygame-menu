"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET SELECTION CORE.
Test widget core selection effects and general helper methods.
"""

import copy

import pygame
import pytest

from pygame_menu.baseimage import IMAGE_EXAMPLE_PYGAME_MENU, BaseImage
from pygame_menu.widgets import Button
from pygame_menu.widgets.core.selection import Selection
from pygame_menu.widgets.selection import (
    NoneSelection,
    SimpleSelection,
)
from test._utils import MenuUtils, surface


@pytest.fixture
def menu():
    """Create and enable a generic menu fixture."""
    m = MenuUtils.generic_menu()
    m.enable()
    return m


def test_copy():
    """Test selection effect copy behavior."""
    s = SimpleSelection()

    s1 = copy.copy(s)
    s2 = copy.deepcopy(s)
    s3 = s.copy()

    assert s is not s1
    assert s is not s2
    assert s is not s3


def test_abstract_selection_draw_raises():
    """Test abstract selection draw methods raise errors."""
    w = Button("epic")

    sel = Selection(0, 0, 0, 0)
    with pytest.raises(NotImplementedError):
        sel.draw(surface, w)


def test_margin_xy():
    """Test margin_xy helper."""
    sel = SimpleSelection()

    sel.margin_xy(10, 20)

    assert sel.margin_left == 10
    assert sel.margin_right == 10
    assert sel.margin_top == 20
    assert sel.margin_bottom == 20


def test_margin_xy_invalid():
    """Test margin_xy rejects negative values."""
    sel = SimpleSelection()

    with pytest.raises(AssertionError):
        sel.margin_xy(-1, 0)

    with pytest.raises(AssertionError):
        sel.margin_xy(0, -1)


def test_zero_margin():
    """Test zero_margin helper."""
    sel = SimpleSelection()

    sel.zero_margin()

    assert sel.margin_left == 0
    assert sel.margin_right == 0
    assert sel.margin_top == 0
    assert sel.margin_bottom == 0


def test_get_margin():
    """Test get_margin."""
    sel = Selection(
        margin_left=1,
        margin_right=2,
        margin_top=3,
        margin_bottom=4,
    )

    assert sel.get_margin() == (3, 1, 4, 2)


def test_get_xy_margin():
    """Test xy margin calculation."""
    sel = Selection(
        margin_left=10,
        margin_right=20,
        margin_top=30,
        margin_bottom=40,
    )

    assert sel.get_xy_margin() == (30, 70)


def test_get_width_height():
    """Test width and height helpers."""
    sel = Selection(
        margin_left=10,
        margin_right=15,
        margin_top=5,
        margin_bottom=7,
    )

    assert sel.get_width() == 25
    assert sel.get_height() == 12


def test_set_color():
    """Test setting selection color."""
    sel = SimpleSelection()

    sel.set_color("red")

    assert sel.color == (255, 0, 0, 255)


def test_set_background_color():
    """Test background color setter."""
    sel = SimpleSelection()

    sel.set_background_color("red")

    assert sel.get_background_color() == (255, 0, 0, 255)


def test_set_background_image():
    """Test image backgrounds are supported."""
    sel = SimpleSelection()

    img = BaseImage(IMAGE_EXAMPLE_PYGAME_MENU)

    sel.set_background_color(img)

    assert sel.get_background_color() is img


def test_inflate():
    """Test rectangle inflation."""
    sel = Selection(
        margin_left=10,
        margin_right=10,
        margin_top=5,
        margin_bottom=5,
    )

    rect = pygame.Rect(50, 50, 100, 40)

    inflated = sel.inflate(rect)

    assert inflated.x == 40
    assert inflated.y == 45
    assert inflated.width == 120
    assert inflated.height == 50


def test_inflate_with_extra_border():
    """Test rectangle inflation including extra border."""
    sel = SimpleSelection()

    rect = pygame.Rect(10, 10, 100, 50)

    inflated = sel.inflate(rect, (10, 20))

    assert inflated.width == 110
    assert inflated.height == 70


def test_inflate_none_parameter():
    """Test inflate with default parameter."""
    sel = SimpleSelection()

    rect = pygame.Rect(0, 0, 100, 50)

    inflated = sel.inflate(rect)

    assert inflated == rect


def test_none_selection(menu):
    """Test none selection behavior."""
    w = Button("epic")

    w.set_selection_effect(NoneSelection())

    menu.add.generic_widget(w)
    menu.draw(surface)

    rect = w.get_rect()

    new_rect = w.get_selection_effect().inflate(rect)

    assert rect == new_rect

    assert not w.get_selection_effect().widget_apply_font_color

    last_sel = w.get_selection_effect()

    w.set_selection_effect()

    assert isinstance(
        w.get_selection_effect(),
        NoneSelection,
    )

    assert w.get_selection_effect() != last_sel


def test_simple_selection(menu):
    """Test simple selection behavior."""
    w = Button("epic")

    w.set_selection_effect(SimpleSelection())

    menu.add.generic_widget(w)
    menu.draw(surface)

    rect = w.get_rect()

    new_rect = w.get_selection_effect().inflate(rect)

    assert rect == new_rect

    assert w.get_selection_effect().widget_apply_font_color


def test_simple_selection_font_color_flag():
    """Test custom font-color application flag."""
    sel = SimpleSelection(widget_apply_font_color=False)

    assert not sel.widget_apply_font_color


def test_selection_repr():
    """Test selection string representation."""
    sel = Selection(
        margin_left=1,
        margin_right=2,
        margin_top=3,
        margin_bottom=4,
    )

    r = repr(sel)

    assert "Selection(" in r
    assert "margin_left=1" in r
    assert "margin_right=2" in r
    assert "margin_top=3" in r
    assert "margin_bottom=4" in r
    assert "color=" in r
    assert "color_bg=" in r


def test_none_selection_repr():
    """Test none selection repr."""
    sel = NoneSelection()

    r = repr(sel)

    assert "NoneSelection(" in r
    assert "widget_apply_font_color=False" in r


def test_repr_with_background_color():
    """Test repr includes background color."""
    sel = SimpleSelection()

    sel.set_background_color("red")

    r = repr(sel)

    assert "color_bg=(255, 0, 0, 255)" in r
