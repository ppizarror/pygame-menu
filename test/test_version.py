"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST VERSION
Test version management.
"""

import pytest

from pygame_menu.version import Version


def test_version_str():
    """Verify string formatting of Version."""
    v = Version(4, 5, 5)
    assert str(v) == "4.5.5"


def test_version_repr():
    """Verify repr formatting of Version."""
    v = Version(4, 5, 5)
    assert repr(v) == "Version(major=4, minor=5, patch=5)"


def test_version_fields():
    """Verify major/minor/patch fields."""
    v = Version(4, 5, 5)
    assert v.major == 4
    assert v.minor == 5
    assert v.patch == 5


def test_version_ordering():
    """Verify lexicographic ordering of Version."""
    assert Version(1, 2, 3) < Version(1, 3, 0)
    assert Version(1, 2, 3) <= Version(1, 2, 3)
    assert Version(2, 0, 0) > Version(1, 9, 9)


def test_version_equality():
    """Verify equality and inequality of Version."""
    assert Version(4, 5, 5) == Version(4, 5, 5)
    assert Version(4, 5, 5) != Version(4, 5, 6)


def test_version_immutability():
    """Verify Version objects cannot be modified."""
    v = Version(4, 5, 5)
    with pytest.raises(AttributeError):
        v.major = 10
    with pytest.raises(TypeError):
        v[0] = 10


def test_version_tuple_behavior():
    """Verify tuple-like behavior of Version."""
    v = Version(4, 5, 5)
    assert len(v) == 3
    assert v[0] == 4
    assert tuple(v) == (4, 5, 5)


def test_version_type_validation():
    """Verify invalid Version components raise TypeError."""
    with pytest.raises(TypeError):
        Version("a", 1, 1)
    with pytest.raises(TypeError):
        Version(1, None, 1)
    with pytest.raises(TypeError):
        Version(1.2, 3, 4)


def test_version_parse():
    """Verify parsing from string to Version."""
    v2 = Version.parse("1.2.3")
    assert v2.major == 1
    assert v2.minor == 2
    assert v2.patch == 3


def test_version_parse_errors():
    """Verify invalid version strings raise ValueError."""
    with pytest.raises(ValueError):
        Version.parse("1.2")
    with pytest.raises(ValueError):
        Version.parse("1.2.3.4")
    with pytest.raises(ValueError):
        Version.parse("abc")


def test_version_ordering_parsed():
    """Verify ordering works for parsed versions."""
    assert Version.parse("1.2.3") < Version.parse("1.3.0")
