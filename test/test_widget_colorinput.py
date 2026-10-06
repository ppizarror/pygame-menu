"""
pygame-menu

TEST WIDGET - COLORINPUT
Test ColorInput widget.
"""

import pygame
import pytest

from test._utils import (
    PYGAME_V2,
    TEST_THEME,
    MenuUtils,
    PygameEventUtils,
    surface,
)


def assert_color(widget, r, g, b):
    """Assert widget RGB color value."""
    assert widget.get_value() == (r, g, b)


def assert_invalid_color(widget):
    """Assert widget color is invalid."""
    assert widget.get_value() == (-1, -1, -1)


def test_colorinput_rgb_basics():
    """Test ColorInput RGB validation and value assignment."""
    menu = MenuUtils.generic_menu(theme=TEST_THEME.copy())

    widget = menu.add.color_input(
        "title",
        color_type="rgb",
        input_separator=",",
    )

    widget.set_value((123, 234, 55))
    assert_color(widget, 123, 234, 55)

    with pytest.raises(AssertionError):
        widget.set_value("0,0,0")

    with pytest.raises(AssertionError):
        widget.set_value((255, 0))  # type: ignore

    with pytest.raises(AssertionError):
        widget.set_value((255, 255, -255))


@pytest.mark.parametrize(
    "separator",
    ["", "  ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
)
def test_colorinput_invalid_separator(separator):
    """Test invalid RGB separators."""
    menu = MenuUtils.generic_menu()

    with pytest.raises(AssertionError):
        menu.add.color_input(
            "title",
            color_type="rgb",
            input_separator=separator,
        )


def test_colorinput_invalid_type():
    """Test invalid color type."""
    menu = MenuUtils.generic_menu()

    with pytest.raises(AssertionError):
        menu.add.color_input(
            "title",
            color_type="unknown",
        )


def test_colorinput_rgb_typing_and_validation():
    """Test RGB typing rules and automatic separators."""
    menu = MenuUtils.generic_menu()

    widget = menu.add.color_input(
        "color",
        color_type="rgb",
        input_separator=",",
    )

    PygameEventUtils.test_widget_key_press(widget)

    assert widget._cursor_position == 0

    widget.update(
        PygameEventUtils.key(
            pygame.K_RIGHT,
            keydown=True,
        )
    )

    assert widget._cursor_position == 0
    assert_invalid_color(widget)

    widget.update(
        PygameEventUtils.key(
            pygame.K_2,
            keydown=True,
            char="2",
        )
    )

    widget.update(
        PygameEventUtils.key(
            pygame.K_5,
            keydown=True,
            char="5",
        )
    )

    widget.update(
        PygameEventUtils.key(
            pygame.K_COMMA,
            keydown=True,
            char=",",
        )
    )

    assert widget._input_string == "25,"

    widget.update(
        PygameEventUtils.key(
            pygame.K_0,
            keydown=True,
            char="0",
        )
    )

    assert widget._input_string == "25,0,"
    assert_invalid_color(widget)

    widget.update(PygameEventUtils.key(pygame.K_LEFT, keydown=True))
    widget.update(PygameEventUtils.key(pygame.K_LEFT, keydown=True))
    widget.update(PygameEventUtils.key(pygame.K_LEFT, keydown=True))

    assert widget._cursor_position == 2

    widget.update(
        PygameEventUtils.key(
            pygame.K_5,
            keydown=True,
            char="5",
        )
    )

    assert widget._input_string == "255,0,"

    widget.update(
        PygameEventUtils.key(
            pygame.K_5,
            keydown=True,
            char="5",
        )
    )

    assert widget._input_string == "255,0,"

    widget.update(PygameEventUtils.key(pygame.K_RIGHT, keydown=True))

    widget.update(
        PygameEventUtils.key(
            pygame.K_0,
            keydown=True,
            char="0",
        )
    )

    assert widget._input_string == "255,0,"


def test_colorinput_rgb_deletion_and_completion():
    """Test RGB deletion behavior and automatic completion."""
    menu = MenuUtils.generic_menu()

    widget = menu.add.color_input(
        "color",
        color_type="rgb",
        input_separator=",",
    )

    # Reproduce original state
    widget._input_string = "255,0,"
    widget._cursor_position = len(widget._input_string)

    widget.update(PygameEventUtils.key(pygame.K_BACKSPACE, keydown=True))
    widget.update(PygameEventUtils.key(pygame.K_BACKSPACE, keydown=True))

    assert widget._input_string == "255,"

    widget.update(
        PygameEventUtils.key(
            pygame.K_0,
            keydown=True,
            char="0",
        )
    )

    widget.update(
        PygameEventUtils.key(
            pygame.K_0,
            keydown=True,
            char="0",
        )
    )

    assert widget._input_string == "255,0,0"
    assert_color(widget, 255, 0, 0)


def test_colorinput_rgb_defaults():
    """Test invalid RGB defaults."""
    menu = MenuUtils.generic_menu()

    with pytest.raises(AssertionError):
        menu.add.color_input(
            "title",
            color_type="rgb",
            default=(255, 255),  # type: ignore
        )

    with pytest.raises(AssertionError):
        menu.add.color_input(
            "title",
            color_type="rgb",
            default=(255, 255, 255, 255),  # type: ignore
        )


def test_colorinput_hex_validation():
    """Test HEX validation and parsing."""
    menu = MenuUtils.generic_menu()

    widget = menu.add.color_input(
        "title",
        color_type="hex",
    )

    assert widget._input_string == "#"
    assert widget._cursor_position == 1

    assert_invalid_color(widget)

    for value in (
        "#FF",
        "#FFFFF<",
        "#FFFFF",
        "#F",
        "FFFFF",
        "F",
    ):
        with pytest.raises(AssertionError):
            widget.set_value(value)

    widget.set_value("FF00FF")
    assert_color(widget, 255, 0, 255)

    widget.set_value("#12FfAa")
    assert_color(widget, 18, 255, 170)

    widget.set_value("   59C1e5")
    assert_color(widget, 89, 193, 229)


def test_colorinput_hex_formatting():
    """Test HEX formatting modes."""
    menu = MenuUtils.generic_menu()

    widget = menu.add.color_input(
        "title",
        color_type="hex",
        hex_format="none",
    )

    widget.set_value("#FF00ff")
    assert widget.get_value(as_string=True) == "#FF00ff"

    widget = menu.add.color_input(
        "title",
        color_type="hex",
        hex_format="lower",
    )

    widget.set_value("#FF00ff")
    assert widget.get_value(as_string=True) == "#ff00ff"

    widget = menu.add.color_input(
        "title",
        color_type="hex",
        hex_format="upper",
    )

    widget.set_value("#FF00ff")
    assert widget.get_value(as_string=True) == "#FF00FF"


def test_colorinput_dynamic_width():
    """Test dynamic sizing."""
    menu = MenuUtils.generic_menu(theme=TEST_THEME.copy())

    widget = menu.add.color_input(
        "title",
        color_type="hex",
        hex_format="upper",
        dynamic_width=True,
    )

    assert widget.get_width() == 200

    widget.set_value("#ffffff")

    width = 342 if PYGAME_V2 else 345

    assert widget.get_width() == width

    widget.set_value(None)

    assert widget.get_width() == 200
    assert widget.get_value(as_string=True) == "#"

    widget.set_value("#ffffff")

    assert widget.get_width() == width

    widget.update(
        PygameEventUtils.key(
            pygame.K_BACKSPACE,
            keydown=True,
        )
    )

    assert widget.get_value(as_string=True) == "#FFFFF"

    widget.render()

    assert widget.get_width() == 200

    widget.draw(surface)

    widget = menu.add.color_input(
        "title",
        color_type="hex",
        hex_format="upper",
        dynamic_width=False,
    )

    assert widget.get_width() == width

    widget.set_value("#ffffff")

    assert widget.get_width() == width


def test_colorinput_copy_paste_exceptions():
    """Test clipboard exception handling."""
    import pygame_menu.widgets.widget.textinput as tinput

    menu = MenuUtils.generic_menu()

    widget = menu.add.color_input(
        "title",
        color_type="rgb",
    )

    def invalid_clipboard(*_):
        raise tinput.PyperclipException("test")

    original_copy = tinput.clipboard_copy
    tinput.clipboard_copy = invalid_clipboard
    assert not widget._copy()
    tinput.clipboard_copy = original_copy

    original_paste = tinput.clipboard_paste
    tinput.clipboard_paste = invalid_clipboard
    assert not widget._paste()
    tinput.clipboard_paste = original_paste
