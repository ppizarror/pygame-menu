"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST BASE
Test base class.
"""

import pytest

# noinspection PyProtectedMember
from pygame_menu._base import Base


def test_counter_increments_from_zero():
    """Counter starts at default and increments sequentially."""
    obj = Base("")
    for i in range(1, 7):
        assert obj.get_counter_attribute("count", 1) == i


def test_counter_float_default_string():
    """Counter initializes from float-like string default and increments."""
    obj = Base("")
    assert pytest.approx(obj.get_counter_attribute("epic", 1, "3.14")) == 4.14
    assert pytest.approx(obj.get_counter_attribute("epic", 1, "3.14")) == 5.14
    assert pytest.approx(obj.get_counter_attribute("epic", 1, "3.14")) == 6.14


def test_counter_integer_default_string():
    """Counter initializes from int-like string default and increments."""
    obj = Base("")
    assert obj.get_counter_attribute("count1", 1, "1") == 2
    assert obj.get_counter_attribute("count1", 1, "1") == 3


def test_counter_float_increment_with_string_default():
    """Float increment works with string default coerced to number."""
    obj = Base("")
    assert obj.get_counter_attribute("count2", 1.0, "1") == 2.0
    assert obj.get_counter_attribute("count2", 1.0, "1") == 3.0


def test_counter_non_numeric_default_raises():
    """Non-numeric default value raises ValueError."""
    obj = Base("")
    with pytest.raises(ValueError):
        obj.get_counter_attribute("c", 1, "not_a_number")


def test_counter_non_numeric_increment_casts_to_float():
    """Non-numeric increment is coerced to float."""
    obj = Base("")
    assert obj.get_counter_attribute("c", "5") == 5.0


def test_attribute_missing():
    """Missing attribute returns default and reports absence."""
    obj = Base("")
    assert not obj.has_attribute("epic")
    assert obj.get_attribute("missing", 99) == 99


def test_attribute_remove_missing_raises():
    """Removing a missing attribute raises IndexError."""
    obj = Base("")
    with pytest.raises(IndexError):
        obj.remove_attribute("epic")


def test_attribute_set_get_remove_cycle():
    """Attributes can be set, updated, removed, and defaulted."""
    obj = Base("")
    obj.set_attribute("epic", True)
    assert obj.has_attribute("epic")
    assert obj.get_attribute("epic") is True

    obj.set_attribute("epic", False)
    assert obj.get_attribute("epic") is False

    obj.remove_attribute("epic")
    assert not obj.has_attribute("epic")
    assert obj.get_attribute("epic", 420) == 420


def test_attribute_overwrite():
    """Setting an attribute twice overwrites previous value."""
    obj = Base("")
    obj.set_attribute("x", 1)
    obj.set_attribute("x", "hello")
    assert obj.get_attribute("x") == "hello"


def test_attribute_key_type_error():
    """Non-string attribute key raises TypeError."""
    obj = Base("")
    with pytest.raises(TypeError):
        obj.set_attribute(123, "value")  # type: ignore


def test_repr_default_does_not_include_id():
    """Default repr does not include object ID."""
    obj = Base("id")
    r = repr(obj)
    assert "object at" in r
    assert "id" not in r


def test_repr_id_injection():
    """ID repr flag injects ID into repr output."""
    obj = Base("id")
    obj._id__repr__ = True
    assert '["id"]' in repr(obj)


def test_repr_class_id():
    """Class ID repr flag returns Class<id> format."""
    obj = Base("id2")
    obj._class_id__repr__ = True
    assert repr(obj) == "Base<\"id2\">"


def test_repr_conflict_raises():
    """Enabling both repr flags raises AssertionError."""
    obj = Base("id")
    obj._class_id__repr__ = True
    obj._id__repr__ = True
    with pytest.raises(AssertionError):
        repr(obj)


def test_update_repr_flags():
    """_update__repr___ copies repr flags from another Base."""
    a = Base("a")
    b = Base("b")
    b._class_id__repr__ = True
    b._id__repr__ = True
    a._update__repr___(b)
    assert a._class_id__repr__ is True
    assert a._id__repr__ is True


def test_object_id_zero_string():
    """Object ID '0' is preserved."""
    assert Base("0").get_id() == "0"


def test_object_id_whitespace():
    """Whitespace-only object ID is preserved."""
    assert Base("   ").get_id() == "   "


def test_object_id_type_error():
    """Non-string object ID raises TypeError."""
    with pytest.raises(TypeError):
        Base(123)  # type: ignore


def test_verbose_type_error():
    """Non-bool verbose flag raises TypeError."""
    with pytest.raises(TypeError):
        Base("id", verbose="yes")  # type: ignore


def test_class_id_format():
    """get_class_id returns Class<id> format."""
    obj = Base("id")
    assert obj.get_class_id() == "Base<\"id\">"
