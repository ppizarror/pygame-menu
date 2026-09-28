"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET SELECTION DECORATION.
Test decoration-based widget selection effects (Underline, Dot, Image).
"""

import pytest

from pygame_menu.baseimage import IMAGE_EXAMPLE_PYGAME_MENU, BaseImage
from pygame_menu.widgets import Button
from pygame_menu.widgets.selection import (
    DotSelection,
    ImageSelection,
    UnderlineSelection,
)
from test._utils import MenuUtils, surface


@pytest.fixture
def menu():
    """Create and enable a generic menu fixture."""
    m = MenuUtils.generic_menu()
    m.enable()
    return m


# --- UnderlineSelection Tests ---


def test_underline_selection(menu):
    """Test underline selection rendering."""
    w = Button("epic")
    w.set_selection_effect(UnderlineSelection())
    menu.add.generic_widget(w)
    menu.draw(surface)


def test_underline_selection_repr():
    """Test underline selection repr."""
    sel = UnderlineSelection(
        line_width=3,
        margin=4,
        line_length_offset=10,
    )
    r = repr(sel)
    assert "UnderlineSelection(" in r
    assert "line_width=3" in r
    assert "margin=4" in r
    assert "line_length_offset=10" in r


def test_underline_selection_invalid():
    """Test underline validation."""
    with pytest.raises(AssertionError):
        UnderlineSelection(line_width=0)
    with pytest.raises(AssertionError):
        UnderlineSelection(margin=-1)
    with pytest.raises(AssertionError):
        UnderlineSelection(line_length_offset=-1)


# --- DotSelection Tests ---


def test_dot_selection(menu):
    """Test dot selection rendering."""
    w = Button("epic")
    w.set_selection_effect(DotSelection())
    menu.add.generic_widget(w)
    menu.draw(surface)


def test_dot_selection_margin_geometry():
    """Test dot margin calculations."""
    sel = DotSelection(
        radius=5,
        margin=6,
    )
    assert sel.margin_left == 16
    assert sel.margin_right == 0


def test_dot_selection_repr():
    """Test dot selection repr."""
    sel = DotSelection(
        radius=7,
        margin=8,
        vertical_offset=2,
    )
    r = repr(sel)
    assert "DotSelection(" in r
    assert "radius=7" in r
    assert "margin=8" in r


def test_dot_selection_invalid():
    """Test dot validation."""
    with pytest.raises(AssertionError):
        DotSelection(radius=0)
    with pytest.raises(AssertionError):
        DotSelection(margin=-1)


# --- ImageSelection Tests ---


def test_image_selection(menu):
    """Test image selection rendering."""
    image = BaseImage(IMAGE_EXAMPLE_PYGAME_MENU)
    w = Button("epic")
    w.set_selection_effect(ImageSelection(image))
    menu.add.generic_widget(w)
    menu.draw(surface)


def test_image_selection_geometry():
    """Test image margin geometry."""
    image = BaseImage(IMAGE_EXAMPLE_PYGAME_MENU)
    sel = ImageSelection(
        image=image,
        margin=5,
    )
    assert sel.margin_left == image.get_width() + 5


def test_image_selection_repr():
    """Test image selection repr."""
    image = BaseImage(IMAGE_EXAMPLE_PYGAME_MENU)
    sel = ImageSelection(
        image=image,
        margin=8,
    )
    r = repr(sel)
    assert "ImageSelection(" in r
    assert "image_width=" in r
    assert "image_height=" in r


def test_image_selection_invalid():
    """Test image selection validation."""
    with pytest.raises(AssertionError):
        ImageSelection(  # type: ignore[arg-type]
            image="invalid"
        )
