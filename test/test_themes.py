"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST THEME
Test theme.
"""

from pathlib import Path

import pytest

import pygame_menu
from test._utils import MenuUtils


@pytest.fixture
def example_image():
    return pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)


@pytest.fixture
def default_theme():
    return pygame_menu.themes.THEME_DEFAULT.copy()


# Validation


def test_theme_validation():
    theme = pygame_menu.themes.THEME_ORANGE.copy()
    assert theme.validate() is theme

    invalid_values = ["Epic", -1, (-1, -1)]
    for val in invalid_values:
        theme.widget_padding = val
        with pytest.raises(AssertionError):
            theme.validate()

    theme.widget_padding = (1, 1)
    assert theme.validate() is theme

    theme._disable_validation = True
    theme.widget_padding = "Epic"
    assert theme.validate() is theme


# Copy behavior


def test_theme_copy(example_image):
    theme = pygame_menu.themes.THEME_DEFAULT.copy()
    theme.background_color = example_image

    theme_copy = theme.__copy__()
    assert theme.background_color != theme_copy.background_color
    assert theme.background_color != pygame_menu.themes.THEME_DEFAULT.background_color

    color_main = (29, 120, 107, 255)
    color_copy = (241, 125, 1)

    theme_white = pygame_menu.themes.Theme(
        scrollbar_thick=50, selection_color=color_main
    )

    sub_theme_white = theme_white.copy()
    sub_theme_white.selection_color = color_copy

    assert theme_white.selection_color == color_main
    assert sub_theme_white.selection_color == color_copy
    assert theme_white.selection_color != sub_theme_white.selection_color
    assert (
        theme_white.widget_selection_effect != sub_theme_white.widget_selection_effect
    )

    m1 = MenuUtils.generic_menu(theme=theme_white)
    m2 = MenuUtils.generic_menu(theme=sub_theme_white)
    b1 = m1.add.button("1")
    b2 = m2.add.button("2")

    assert b1._selection_effect.color == theme_white.selection_color
    assert b2._selection_effect.color == sub_theme_white.selection_color
    assert b1._selection_effect.color != b2._selection_effect.color

    assert b1.get_menu().get_theme() is theme_white
    assert theme_white.widget_selection_effect.color == (0, 0, 0)


# Methods


def test_methods(default_theme, example_image):
    theme = default_theme
    theme.background_color = example_image

    with pytest.raises(AssertionError):
        theme.set_background_color_opacity(0.5)

    assert theme._format_color_opacity([1, 1, 1, 1]) == (1, 1, 1, 1)
    assert theme._format_color_opacity([1, 1, 1]) == (1, 1, 1, 255)


# Invalid kwargs


def test_invalid_kwargs():
    with pytest.raises(ValueError):
        pygame_menu.themes.Theme(this_is_an_invalid_kwarg=True)


# Tuple formatting


@pytest.mark.parametrize(
    "value,expected",
    [
        ((1, 2, 3), (1, 2, 3)),
        ([1, 2, 3], (1, 2, 3)),
    ],
)
def test_vec_to_tuple_valid(value, expected):
    t = pygame_menu.themes.THEME_DEFAULT
    assert t._vec_to_tuple(value) == expected


@pytest.mark.parametrize("value", [1, (1, 2, 3)])
def test_vec_to_tuple_invalid(value):
    t = pygame_menu.themes.THEME_DEFAULT
    with pytest.raises(ValueError):
        t._vec_to_tuple(value, check_length=4)


# Opacity formatting


@pytest.mark.parametrize(
    "value,expected",
    [
        ((1, 2, 3), (1, 2, 3, 255)),
        ([1, 2, 3], (1, 2, 3, 255)),
        ([1, 2, 3, 25], (1, 2, 3, 25)),
    ],
)
def test_format_opacity_valid(value, expected):
    t = pygame_menu.themes.THEME_DEFAULT
    assert t._format_color_opacity(value) == expected


def test_format_opacity_invalid(example_image):
    t = pygame_menu.themes.THEME_DEFAULT

    assert t._format_color_opacity(example_image) == example_image
    assert t._format_color_opacity(None, none=True) is None

    with pytest.raises(ValueError):
        t._format_color_opacity(None)

    with pytest.raises(ValueError):
        t._format_color_opacity("1,2,3")

    with pytest.raises(AssertionError):
        t._format_color_opacity((1, 1, -1))

    with pytest.raises(AssertionError):
        t._format_color_opacity((1, 1, 1.1))


# String/int color parsing


def test_str_int_color():
    t = pygame_menu.themes.THEME_DEFAULT.copy()
    t.cursor_color = "#ffffff"
    t.validate()
    assert t.cursor_color == (255, 255, 255, 255)

    t2 = pygame_menu.themes.Theme(
        cursor_color="#ffffff",
        selection_color="0xFFFFFF",
        surface_clear_color=0x00,
        title_font_color="chocolate3",
    )

    assert t2.cursor_color == (255, 255, 255, 255)
    assert t2.selection_color == (255, 255, 255, 255)
    assert t2.surface_clear_color == (0, 0, 0, 0)
    assert t2.title_font_color == (205, 102, 29, 255)


# _get() behavior


@pytest.mark.parametrize(
    "value",
    [
        (1, 1, 1),
        [11, 1, 0, 55],
        [11, 1, 0],
    ],
)
def test_get_color_valid(value):
    t = pygame_menu.themes.THEME_DEFAULT
    t._get({}, "", "color", value)


def test_get_misc(example_image):
    t = pygame_menu.themes.THEME_DEFAULT

    class Test:
        pass

    def dummy():
        return True

    t._get({}, "", "alignment", pygame_menu.locals.ALIGN_LEFT)
    t._get({}, "", "callable", dummy)
    t._get({}, "", "color_image", example_image)
    t._get({}, "", "color_image_none", None)
    t._get({}, "", "cursor", None)
    t._get({}, "", "font", "font")
    t._get({}, "", "font", Path("."))
    t._get({}, "", "image", example_image)
    t._get({}, "", "none", None)
    t._get({}, "", "position", pygame_menu.locals.POSITION_SOUTHWEST)
    t._get({}, "", "tuple2", (1, -1))
    t._get({}, "", "tuple2int", (1.0, -1))
    t._get({}, "", "tuple3", [1, -1, 1])
    t._get({}, "", "tuple3int", [1, -1.0, 1])
    t._get({}, "", "type", bool)
    t._get({}, "", bool, True)
    t._get({}, "", callable, dummy)
    t._get({}, "", int, 4)
    t._get({}, "", str, "hi")
    t._get({}, "", Test, Test())

    assert t._get({}, "", "callable", dummy)() is True


@pytest.mark.parametrize(
    "value",
    [
        [1, 1, 1, 256],
        [11, 1, -1],
        [11, 1],
        None,
    ],
)
def test_get_color_invalid(value):
    t = pygame_menu.themes.THEME_DEFAULT
    with pytest.raises(AssertionError):
        t._get({}, "", "color", value)


def test_get_invalid_cases():
    t = pygame_menu.themes.THEME_DEFAULT

    invalid_pos_vector = [
        [pygame_menu.locals.POSITION_WEST, pygame_menu.locals.POSITION_WEST],
        [pygame_menu.locals.POSITION_WEST, 2],
        [pygame_menu.locals.POSITION_WEST, bool],
    ]

    with pytest.raises(AssertionError):
        t._get({}, "", "cursor", "hi")

    with pytest.raises(AssertionError):
        t._get({}, "", "font", 1)

    with pytest.raises(AssertionError):
        t._get({}, "", "image", bool)

    with pytest.raises(AssertionError):
        t._get({}, "", "none", 1)

    with pytest.raises(AssertionError):
        t._get({}, "", "position", "invalid")

    for val in invalid_pos_vector:
        with pytest.raises(AssertionError):
            t._get({}, "", "position_vector", val)

    with pytest.raises(AssertionError):
        t._get({}, "", "tuple2", (1, 1, 1))

    with pytest.raises(AssertionError):
        t._get({}, "", "tuple2.1", (1, 1))

    with pytest.raises(AssertionError):
        t._get({}, "", "tuple2int", (1.5, 1))

    with pytest.raises(AssertionError):
        t._get({}, "", "tuple3", (1, 1, 1, 1))

    with pytest.raises(AssertionError):
        t._get({}, "", "tuple3int", (1, 1, 1.000001))

    with pytest.raises(AssertionError):
        t._get({}, "", "type", "bool")

    with pytest.raises(AssertionError):
        t._get({}, "", "unknown", object())

    with pytest.raises(AssertionError):
        t._get({}, "", bool, 4.4)

    with pytest.raises(AssertionError):
        t._get({}, "", callable, object())

    with pytest.raises(AssertionError):
        t._get({}, "", int, 4.4)
