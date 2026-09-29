"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET SELECTION ARROW.
Test arrow-based widget selection effects.
"""

import pytest

from pygame_menu.widgets import Button
from pygame_menu.widgets.selection import (
    DoubleArrowSelection,
    LeftArrowSelection,
    RightArrowSelection,
)
from pygame_menu.widgets.selection.arrow_selection import ArrowSelection
from test._utils import MenuUtils, surface


@pytest.fixture
def menu():
    """Create and enable a generic menu fixture."""
    m = MenuUtils.generic_menu()
    m.enable()
    return m


def test_arrow_selection(menu):
    """Test arrow-based selection effects."""
    w = Button("epic")

    w.set_selection_effect(LeftArrowSelection())
    menu.add.generic_widget(w)
    menu.draw(surface)

    w.set_selection_effect(RightArrowSelection())
    menu.draw(surface)

    arrow = ArrowSelection(0, 0, 0, 0)

    with pytest.raises(NotImplementedError):
        arrow.draw(surface, w)


def test_left_arrow_invalid_args():
    """Test left arrow validation."""
    with pytest.raises(AssertionError):
        LeftArrowSelection(arrow_right_margin=-1)


def test_right_arrow_invalid_args():
    """Test right arrow validation."""
    with pytest.raises(AssertionError):
        RightArrowSelection(arrow_left_margin=-1)


def test_arrow_selection_invalid_constructor():
    """Test abstract arrow constructor validation."""
    with pytest.raises(AssertionError):
        ArrowSelection(
            0,
            0,
            0,
            0,
            arrow_size=(0, 10),
        )

    with pytest.raises(AssertionError):
        ArrowSelection(
            0,
            0,
            0,
            0,
            blink_ms=-1,
        )


def test_arrow_blink_disabled(menu):
    """Test drawing with blinking disabled."""
    w = Button("epic")

    w.set_selection_effect(LeftArrowSelection(blink_ms=0))

    menu.add.generic_widget(w)

    menu.draw(surface)
    menu.draw(surface)
    menu.draw(surface)


def test_left_arrow_selection_repr():
    """Test left arrow selection repr."""
    sel = LeftArrowSelection(
        arrow_size=(20, 30),
        arrow_right_margin=4,
        blink_ms=500,
    )

    r = repr(sel)

    assert "LeftArrowSelection(" in r
    assert "arrow_size=(20, 30)" in r
    assert "blink_ms=500" in r


def test_right_arrow_selection_repr():
    """Test right arrow selection repr."""
    sel = RightArrowSelection(
        arrow_size=(15, 25),
        arrow_left_margin=7,
        blink_ms=250,
    )

    r = repr(sel)

    assert "RightArrowSelection(" in r
    assert "arrow_size=(15, 25)" in r
    assert "blink_ms=250" in r


# --- DoubleArrowSelection Tests ---


def test_double_arrow_selection(menu):
    """Test double arrow rendering."""
    w = Button("epic")
    w.set_selection_effect(DoubleArrowSelection())
    menu.add.generic_widget(w)
    menu.draw(surface)


def test_double_arrow_selection_geometry():
    """Test double arrow margins."""
    sel = DoubleArrowSelection(
        arrow_size=(10, 15),
        arrow_margin=5,
    )
    assert sel.margin_left == 15
    assert sel.margin_right == 15


def test_double_arrow_selection_repr():
    """Test double arrow repr."""
    sel = DoubleArrowSelection(
        arrow_size=(20, 30),
        arrow_margin=10,
    )
    r = repr(sel)
    assert "DoubleArrowSelection(" in r
    assert "arrow_size=(20, 30)" in r


def test_double_arrow_selection_invalid():
    """Test double arrow validation."""
    with pytest.raises(AssertionError):
        DoubleArrowSelection(arrow_margin=-1)
