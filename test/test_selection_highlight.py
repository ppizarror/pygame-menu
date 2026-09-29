"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET SELECTION HIGHLIGHT.
Test highlight-based widget selection effects.
"""

import pytest

from pygame_menu.widgets import Button
from pygame_menu.widgets.selection import (
    HighlightSelection,
    RoundedHighlightSelection,
)
from test._utils import MenuUtils, surface


@pytest.fixture
def menu():
    """Create and enable a generic menu fixture."""
    m = MenuUtils.generic_menu()
    m.enable()
    return m


def test_highlight_selection(menu):
    """Test highlight selection properties and rendering."""
    w = Button("epic")

    border_width = 1
    margin_x = 18
    margin_y = 10

    w.set_selection_effect(
        HighlightSelection(
            border_width=border_width,
            margin_x=margin_x,
            margin_y=margin_y,
        )
    )

    menu.add.generic_widget(w)
    menu.draw(surface)

    sel: HighlightSelection = w.get_selection_effect()  # type: ignore

    assert sel.get_height() == margin_y
    assert sel.get_width() == margin_x

    rect = w.get_rect()
    inflated = sel.inflate(rect)

    assert -inflated.x + rect.x == sel.get_width() / 2
    assert -inflated.y + rect.y == sel.get_height() / 2

    sel.margin_xy(10, 20)

    assert sel.margin_left == 10
    assert sel.margin_right == 10
    assert sel.margin_top == 20
    assert sel.margin_bottom == 20

    sel._border_width = 0
    sel.draw(surface, w)

    sel.set_background_color("red")
    assert sel.get_background_color() == (255, 0, 0, 255)


def test_highlight_selection_invalid_args():
    """Test highlight validation."""
    with pytest.raises(AssertionError):
        HighlightSelection(border_width=-1)

    with pytest.raises(AssertionError):
        HighlightSelection(margin_x=-1)

    with pytest.raises(AssertionError):
        HighlightSelection(margin_y=-1)


def test_highlight_selection_repr():
    """Test highlight selection repr."""
    sel = HighlightSelection(
        border_width=2,
        margin_x=20,
        margin_y=10,
    )

    r = repr(sel)

    assert "HighlightSelection(" in r
    assert "border_width=2" in r


# --- RoundedHighlightSelection Tests ---


def test_rounded_highlight_selection(menu):
    """Test rounded highlight rendering."""
    w = Button("epic")
    w.set_selection_effect(RoundedHighlightSelection())
    menu.add.generic_widget(w)
    menu.draw(surface)


def test_rounded_highlight_selection_repr():
    """Test rounded highlight repr."""
    sel = RoundedHighlightSelection(
        border_width=2,
        border_radius=10,
    )
    r = repr(sel)
    assert "RoundedHighlightSelection(" in r
    assert "border_width=2" in r
    assert "border_radius=10" in r


def test_rounded_highlight_invalid():
    """Test rounded highlight validation."""
    with pytest.raises(AssertionError):
        RoundedHighlightSelection(border_radius=-1)
