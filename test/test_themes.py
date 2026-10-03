"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST THEME
Test theme.
"""

import json
from pathlib import Path

import pytest

import pygame_menu
from test._utils import MenuUtils


@pytest.fixture
def example_image():
    """Return a reusable example image fixture."""
    return pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)


@pytest.fixture
def default_theme():
    """Return a copy of the default theme fixture."""
    return pygame_menu.themes.THEME_DEFAULT.copy()


def test_theme_validation():
    """Test theme validation behavior and bypass flag."""
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


def test_theme_copy(example_image):
    """Test theme copy semantics and selection color isolation."""
    theme = pygame_menu.themes.THEME_DEFAULT.copy()  # Create theme
    theme.background_color = example_image

    theme_copy = theme.__copy__()  # Copy the theme
    assert theme.background_color != theme_copy.background_color
    assert theme.background_color != pygame_menu.themes.THEME_DEFAULT.background_color

    # Test attribute copy
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

    # Test the widget effect color is different in both objects
    m1 = MenuUtils.generic_menu(theme=theme_white)
    m2 = MenuUtils.generic_menu(theme=sub_theme_white)
    b1 = m1.add.button("1")
    b2 = m2.add.button("2")

    assert b1._selection_effect.color == theme_white.selection_color
    assert b2._selection_effect.color == sub_theme_white.selection_color
    assert b1._selection_effect.color != b2._selection_effect.color

    # Main Theme selection effect class should not be modified
    assert b1.get_menu().get_theme() is theme_white
    assert theme_white.widget_selection_effect.color == (0, 0, 0)


def test_methods(default_theme, example_image):
    """Test helper methods related to opacity and background handling."""
    theme = default_theme
    theme.background_color = example_image

    with pytest.raises(AssertionError):
        theme.set_background_color_opacity(0.5)

    assert theme._format_color_opacity([1, 1, 1, 1]) == (1, 1, 1, 1)
    assert theme._format_color_opacity([1, 1, 1]) == (1, 1, 1, 255)


def test_invalid_kwargs():
    """Test invalid keyword arguments in theme constructor."""
    with pytest.raises(ValueError):
        pygame_menu.themes.Theme(this_is_an_invalid_kwarg=True)


@pytest.mark.parametrize(
    "value,expected",
    [
        ((1, 2, 3), (1, 2, 3)),
        ([1, 2, 3], (1, 2, 3)),
    ],
)
def test_vec_to_tuple_valid(value, expected):
    """Test valid vector-to-tuple conversion."""
    t = pygame_menu.themes.THEME_DEFAULT
    assert t._vec_to_tuple(value) == expected


@pytest.mark.parametrize("value", [1, (1, 2, 3)])
def test_vec_to_tuple_invalid(value):
    """Test invalid vector-to-tuple conversion cases."""
    t = pygame_menu.themes.THEME_DEFAULT
    with pytest.raises(ValueError):
        t._vec_to_tuple(value, check_length=4)


@pytest.mark.parametrize(
    "value,expected",
    [
        ((1, 2, 3), (1, 2, 3, 255)),
        ([1, 2, 3], (1, 2, 3, 255)),
        ([1, 2, 3, 25], (1, 2, 3, 25)),
    ],
)
def test_format_opacity_valid(value, expected):
    """Test valid color opacity formatting."""
    t = pygame_menu.themes.THEME_DEFAULT
    assert t._format_color_opacity(value) == expected


def test_format_opacity_invalid(example_image):
    """Test invalid color opacity formatting cases."""
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


def test_str_int_color():
    """Test color parsing from strings and integers."""
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


@pytest.mark.parametrize(
    "value",
    [
        (1, 1, 1),
        [11, 1, 0, 55],
        [11, 1, 0],
    ],
)
def test_get_color_valid(value):
    """Test valid color retrieval through internal getter."""
    t = pygame_menu.themes.THEME_DEFAULT
    t._get({}, "", "color", value)


def test_get_misc(example_image):
    """Test miscellaneous valid cases for internal getter."""
    t = pygame_menu.themes.THEME_DEFAULT

    class Test:
        """Class to test."""

        pass

    def dummy():
        """Return a truthy marker for callable checks."""
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
    """Test invalid color retrieval through internal getter."""
    t = pygame_menu.themes.THEME_DEFAULT
    with pytest.raises(AssertionError):
        t._get({}, "", "color", value)


def test_get_invalid_cases():
    """Test invalid internal getter cases across supported types."""
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


def test_from_theme():
    """Test theme inheritance and overrides."""
    parent = pygame_menu.themes.THEME_DARK

    child = pygame_menu.themes.Theme.from_theme(
        parent,
        widget_font_size=123,
    )

    assert child.widget_font_size == 123
    assert parent.widget_font_size != 123
    assert child.background_color == parent.background_color


def test_from_theme_invalid_kwarg():
    """Test invalid overrides in from_theme."""
    with pytest.raises(ValueError):
        pygame_menu.themes.Theme.from_theme(
            pygame_menu.themes.THEME_DEFAULT,
            invalid_attribute=True,
        )


def test_diff_equal_themes():
    """Test diff between equal themes."""
    t1 = pygame_menu.themes.Theme()
    t2 = t1.copy()

    assert t1.diff(t2) == {}


def test_diff_different_themes():
    """Test diff between different themes."""
    t1 = pygame_menu.themes.Theme()
    t2 = t1.copy()

    t2.widget_font_size = 999

    diff = t1.diff(t2)

    assert len(diff) == 1
    assert "widget_font_size" in diff
    assert diff["widget_font_size"] == (
        t1.widget_font_size,
        999,
    )


def test_to_dict():
    """Test dictionary serialization."""
    theme = pygame_menu.themes.Theme(
        widget_font_size=123,
        title_font_size=456,
    )

    data = theme.to_dict()

    assert data["widget_font_size"] == 123
    assert data["title_font_size"] == 456
    assert "_disable_validation" not in data


def test_from_dict():
    """Test dictionary deserialization."""
    theme = pygame_menu.themes.Theme(
        widget_font_size=321,
        title_font_size=654,
    )

    restored = pygame_menu.themes.Theme.from_dict(theme.to_dict())

    diff = restored.diff(theme)
    diff.pop("widget_selection_effect", None)
    assert diff == {}


def test_json_roundtrip():
    """Test json serialization roundtrip."""
    theme = pygame_menu.themes.Theme(
        widget_font_size=123,
        title_font_size=456,
    )

    restored = pygame_menu.themes.Theme.from_json(theme.to_json())

    diff = restored.diff(theme)
    diff.pop("widget_selection_effect", None)
    assert diff == {}


def test_to_dict_skips_baseimage(example_image):
    """Test BaseImage fields are omitted."""
    theme = pygame_menu.themes.Theme()
    theme.background_color = example_image

    data = theme.to_dict()

    assert "background_color" not in data


def test_repr():
    """Test repr contains modified values."""
    theme = pygame_menu.themes.Theme(
        widget_font_size=999,
    )

    text = repr(theme)

    assert "widget_font_size" in text
    assert "999" in text


def test_repr_default_theme():
    """Test repr of default theme."""
    theme = pygame_menu.themes.Theme()

    assert repr(theme).startswith("Theme(")


def test_selection_effect_none_normalization():
    """Test None selection effect normalization."""
    theme = pygame_menu.themes.Theme()

    theme.widget_selection_effect = None

    theme.validate()

    assert isinstance(
        theme.widget_selection_effect,
        pygame_menu.widgets.core.Selection,
    )


def test_slots_prevent_unknown_attributes():
    """Test __slots__ prevents dynamic attributes."""
    theme = pygame_menu.themes.Theme()

    with pytest.raises(AttributeError):
        theme.this_attribute_does_not_exist = True


def test_copy_independence():
    """Test copied themes are independent."""
    t1 = pygame_menu.themes.Theme()
    t2 = t1.copy()

    t2.widget_font_size = 999

    assert t1.widget_font_size != t2.widget_font_size


def test_dict_roundtrip_preserves_configuration():
    """Roundtrip through dict should preserve equality."""
    theme = pygame_menu.themes.THEME_BLUE.copy()

    restored = pygame_menu.themes.Theme.from_dict(theme.to_dict())

    diff = restored.diff(theme)
    diff.pop("widget_selection_effect", None)
    assert diff == {}


def test_json_roundtrip_preserves_configuration():
    """Roundtrip through json should preserve equality."""
    theme = pygame_menu.themes.THEME_GREEN.copy()

    restored = pygame_menu.themes.Theme.from_json(theme.to_json())

    diff = restored.diff(theme)
    diff.pop("widget_selection_effect", None)
    assert diff == {}


def test_from_json_invalid():
    """Test invalid json input."""
    with pytest.raises(json.JSONDecodeError):
        pygame_menu.themes.Theme.from_json("{invalid json}")


def test_to_dict_skips_selection_effect():
    """Selection objects are not serializable and should be omitted."""
    theme = pygame_menu.themes.Theme()

    data = theme.to_dict()

    assert "widget_selection_effect" not in data


def test_json_roundtrip_restores_tuples():
    """Tuple-based attributes should survive json roundtrip."""
    theme = pygame_menu.themes.Theme(
        widget_margin=(10, 20),
        title_offset=(5, 6),
    )

    restored = pygame_menu.themes.Theme.from_json(
        theme.to_json()
    )

    assert restored.widget_margin == (10, 20)
    assert restored.title_offset == (5, 6)
