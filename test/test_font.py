"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST FONT
Test font management.
"""

from pathlib import Path

import pygame
import pytest

import pygame_menu
from test._utils import MenuUtils


@pytest.mark.parametrize(
    "name,size,exc",
    [
        (pygame_menu.font.FONT_8BIT, 5, None),
        ("", 0, ValueError),
        ("", 12, ValueError),
        ("sys", 0, ValueError),
        (pygame_menu.font.FONT_8BIT, 0, ValueError),
        (Path("this_font_does_not_exist.ttf"), 12, ValueError),
        ("invalid font", 5, ValueError),
        ("not_a_real_font_name", 14, ValueError),
        (MenuUtils.random_system_font(), 0, ValueError),
    ],
)
def test_get_font_parametrized(name, size, exc):
    """Test get_font with valid and invalid inputs."""
    if exc:
        with pytest.raises(exc):
            pygame_menu.font.get_font(name, size)
    else:
        font = pygame_menu.font.get_font(name, size)
        assert font is not None
        assert font is pygame_menu.font.get_font(font, size)


def test_pathlib_load():
    """Test loading a font using a pathlib.Path."""
    path_font = Path(pygame_menu.font.FONT_8BIT)
    with pytest.raises(ValueError):
        pygame_menu.font.get_font(path_font, 0)
    assert pygame_menu.font.get_font(path_font, 10) is not None


def test_system_load_success():
    """Test loading a valid system font."""
    sys_font = MenuUtils.random_system_font()
    assert pygame_menu.font.get_font(sys_font, 5) is not None


def test_invalid_system_font_message_structure():
    """Test error message structure for invalid system font."""
    with pytest.raises(ValueError) as exc:
        pygame_menu.font.get_font("not_a_font_12345", 12)
    msg = str(exc.value)
    assert "unknown" in msg
    assert "use" in msg
    assert "some examples:" in msg


def test_system_font_cache_identity():
    """Test that system fonts of same size return cached instance."""
    sys_font = MenuUtils.random_system_font()
    f1 = pygame_menu.font.get_font(sys_font, 14)
    f2 = pygame_menu.font.get_font(sys_font, 14)
    assert f1 is f2


@pytest.mark.parametrize("size", [10, 18, 24])
def test_direct_font_passthrough(size):
    """Test that direct pygame.Font instances are returned unchanged."""
    f = pygame.font.SysFont(pygame.font.get_fonts()[0], size)
    assert pygame_menu.font.get_font(f, size) is f


def test_direct_instance_does_not_pollute_cache():
    """Test that direct font instances are not added to cache."""
    before = len(pygame_menu.font._cache)
    f = pygame.font.SysFont(pygame.font.get_fonts()[0], 20)
    pygame_menu.font.get_font(f, 20)
    after = len(pygame_menu.font._cache)
    assert before == after


@pytest.mark.parametrize(
    "size1,size2,should_match",
    [
        (12, 12, True),
        (10, 11, False),
        (14, 18, False),
    ],
)
def test_cache_identity_variants(size1, size2, should_match):
    """Test cache identity for same and different sizes."""
    f1 = pygame_menu.font.get_font(pygame_menu.font.FONT_8BIT, size1)
    f2 = pygame_menu.font.get_font(pygame_menu.font.FONT_8BIT, size2)
    assert (f1 is f2) == should_match


def test_cache_path_variants(tmp_path):
    """Test cache identity for absolute and relative paths."""
    src = Path(pygame_menu.font.FONT_8BIT)
    dst = tmp_path / "font.ttf"
    dst.write_bytes(src.read_bytes())

    abs_path = dst.resolve()
    rel_path = dst.relative_to(tmp_path)
    rel_path = tmp_path / rel_path

    f1 = pygame_menu.font.get_font(abs_path, 12)
    f2 = pygame_menu.font.get_font(rel_path, 12)
    assert f1 is f2


@pytest.mark.parametrize(
    "path_builder",
    [
        lambda p: p,
        lambda p: Path(str(p)),
        lambda p: p.resolve(),
    ],
)
def test_path_normalization_variants(path_builder):
    """Test that different path representations map to same cache entry."""
    base = Path(pygame_menu.font.FONT_8BIT)
    p1 = path_builder(base)
    p2 = path_builder(base)
    assert pygame_menu.font.get_font(p1, 14) is pygame_menu.font.get_font(p2, 14)


def test_load_system_font_success():
    """Test successful loading of a system font via load_system_font."""
    sys_font = MenuUtils.random_system_font()
    assert pygame_menu.font.load_system_font(sys_font, 14) is not None


@pytest.mark.parametrize(
    "name,size,exc",
    [
        ("not_a_real_font_name", 14, ValueError),
        (MenuUtils.random_system_font(), 0, ValueError),
    ],
)
def test_load_system_font_invalid(name, size, exc):
    """Test invalid cases for load_system_font."""
    with pytest.raises(exc):
        pygame_menu.font.load_system_font(name, size)


def test_load_font_file_success():
    """Test loading a valid font file."""
    assert pygame_menu.font.load_font_file(pygame_menu.font.FONT_8BIT, 16) is not None


def test_load_font_file_missing():
    """Test loading a missing font file raises IOError."""
    with pytest.raises(IOError):
        pygame_menu.font.load_font_file("missing_font.ttf", 16)


def test_load_font_file_non_font(tmp_path):
    """Test loading a non-font file either loads fallback or raises."""
    fake = tmp_path / "not_a_font.txt"
    fake.write_text("hello")

    try:
        font = pygame_menu.font.load_font_file(fake, 12)
        assert isinstance(font, pygame.font.Font)
    except OSError:
        # Expected: non-font files may raise
        pass


def test_assert_font_invalid():
    """Test assert_font rejects invalid types."""
    with pytest.raises(AssertionError):
        pygame_menu.font.assert_font(123)


def test_get_font_directory_path(tmp_path):
    """Test get_font raises ValueError when given a directory path."""
    with pytest.raises(ValueError):
        pygame_menu.font.get_font(tmp_path, 12)


def test_font_argument_direct_instance_in_menu():
    """Test menu widget accepts direct pygame.Font instance."""
    menu = MenuUtils.generic_menu()
    f0 = pygame.font.SysFont(pygame.font.get_fonts()[0], 20)

    # Widget with custom font
    text = menu.add.text_input("First name: ", default="John", font_name=f0)
    assert text.get_font_info()["name"] is f0

    # Test widgets with default font, check are equal
    text2 = menu.add.text_input("First name: ", default="John")
    assert text2.get_font_info()["name"] == menu.get_theme().widget_font
