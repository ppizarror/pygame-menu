"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST UTILS
Library utils.
"""

import pygame
import pytest

import pygame_menu.utils as ut
from pygame_menu.locals import POSITION_NORTHWEST
from pygame_menu.widgets.widget.button import Button


def test_alpha():
    """Configure alpha state."""
    assert ut._ALPHA_CHANNEL[0] is True
    ut.configure_alpha(False)
    assert ut._ALPHA_CHANNEL[0] is False
    ut.configure_alpha(True)
    assert ut._ALPHA_CHANNEL[0] is True


def test_callable():
    """Test is callable."""
    assert ut.is_callable(bool)
    assert not ut.is_callable(1)


def test_position_str():
    """Test position assert values as str."""
    assert ut.assert_position_vector(POSITION_NORTHWEST) is None


@pytest.mark.parametrize(
    "value,expected",
    [
        (10, (10, 10, 10, 10)),  # Single number
        (10.5, (10, 10, 10, 10)),  # Single float
        ((5, 15), (5, 15, 5, 15)),  # 2-item tuple (top/bottom, left/right)
        ((5, 15, 25), (5, 15, 25, 15)),  # 3-item tuple (top, left/right, bottom)
        ((1, 2, 3, 4), (1, 2, 3, 4)),  # 4-item tuple (top, right, bottom, left)
        (False, (0, 0, 0, 0)),  # False falls back to 0
        (None, (0, 0, 0, 0)),  # None falls back to 0
    ],
)
def test_parse_padding_variants(value, expected):
    """Test CSS-style padding parsing for all valid input lengths and types."""
    assert ut.parse_padding(value) == expected


@pytest.mark.parametrize(
    "invalid_padding",
    [
        -5,  # Negative number
        (10, -5),  # Negative in tuple
        (1, 2, 3, 4, 5),  # Too many items (>4)
        ("invalid",),  # Non-numeric element
    ],
)
def test_parse_padding_exceptions(invalid_padding):
    """Test that invalid padding values correctly raise assertions."""
    with pytest.raises((AssertionError, TypeError, ValueError)):
        ut.parse_padding(invalid_padding)


@pytest.mark.parametrize(
    "vertical,forward",
    [
        (True, True),
        (True, False),
        (False, True),
        (False, False),
    ],
)
def test_fill_gradient_configurations(vertical, forward):
    """Test all layout permutations of fill_gradient (vertical/horizontal, forward/reverse)."""
    surface = pygame.Surface((50, 50), pygame.SRCALPHA, 32)

    # Should execute successfully without throwing errors
    ut.fill_gradient(
        surface,
        color=(255, 0, 0),
        gradient=(0, 255, 0),
        vertical=vertical,
        forward=forward,
    )

    # Test with custom sub-rect
    sub_rect = pygame.Rect(5, 5, 20, 30)
    ut.fill_gradient(
        surface,
        color="#ff0000",
        gradient="#0000ff",
        rect=sub_rect,
        vertical=vertical,
        forward=forward,
    )


def test_fill_gradient_zero_bounds():
    """Test that fill_gradient handles zero-width or zero-height rectangles safely."""
    surface = pygame.Surface((50, 50), pygame.SRCALPHA, 32)
    zero_rect = pygame.Rect(0, 0, 0, 50)

    # Should return early without raising errors
    ut.fill_gradient(surface, (0, 0, 0), (255, 255, 255), rect=zero_rect)


@pytest.mark.parametrize(
    "color_input,expected",
    [
        ((255, 100, 50), (255, 100, 50, 255)),  # RGB tuple defaults to opaque alpha
        ((10, 20, 30, 128), (10, 20, 30, 128)),  # RGBA tuple preserves alpha
        ("#ff0000", (255, 0, 0, 255)),  # Hex string conversion
    ],
)
def test_format_color_normalization(color_input, expected):
    """Test color formatting and RGBA expansion."""
    assert ut.format_color(color_input) == expected


@pytest.mark.parametrize(
    "valid_color",
    [
        (0, 0, 0),
        (255, 255, 255, 255),
        "#00ff00",
    ],
)
def test_assert_color_valid(valid_color):
    """Test that valid colors pass assertion checks."""
    formatted = ut.assert_color(valid_color)
    assert len(formatted) == 4
    assert all(0 <= c <= 255 for c in formatted)


@pytest.mark.parametrize(
    "invalid_color",
    [
        (300, 0, 0),  # Out of bounds (> 255)
        (-1, 50, 50),  # Out of bounds (< 0)
        ("bad", 0, 0),  # Non-integer value
        (10, 20, 30, 300),  # Alpha out of bounds
    ],
)
def test_assert_color_invalid(invalid_color):
    """Test that out-of-range or malformed colors raise validation errors."""
    with pytest.raises((AssertionError, ValueError)):
        ut.assert_color(invalid_color, warn_if_invalid=False)


def test_terminal_widget_title():
    """Test terminal title generation."""
    w = Button("epic")
    w.hide()
    s = ut.widget_terminal_title(w)
    assert "╳" in s
