"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - COUNTER
Test Counter widget.
"""

import pytest

import pygame_menu
from test._utils import MenuUtils


@pytest.fixture
def menu():
    """Provides a fresh generic menu for each test."""
    return MenuUtils.generic_menu()


def test_counter_creation(menu):
    """Test counter creation."""
    counter = menu.add.counter()

    assert isinstance(counter, pygame_menu.widgets.Counter)
    assert counter.get_value() == 0


def test_counter_initial_value(menu):
    """Test initial counter value."""
    counter = menu.add.counter(value=10)

    assert counter.get_value() == 10


def test_counter_increment(menu):
    """Test increment."""
    counter = menu.add.counter()

    returned = counter.increment()

    assert returned is counter
    assert counter.get_value() == 1


def test_counter_increment_amount(menu):
    """Test increment by amount."""
    counter = menu.add.counter()

    counter.increment(10)

    assert counter.get_value() == 10


def test_counter_decrement(menu):
    """Test decrement."""
    counter = menu.add.counter(10)

    returned = counter.decrement()

    assert returned is counter
    assert counter.get_value() == 9


def test_counter_decrement_amount(menu):
    """Test decrement by amount."""
    counter = menu.add.counter(20)

    counter.decrement(7)

    assert counter.get_value() == 13


def test_counter_set_value(menu):
    """Test set value."""
    counter = menu.add.counter()

    returned = counter.set_value(99)

    assert returned is counter
    assert counter.get_value() == 99


def test_counter_reset(menu):
    """Test reset restores initial value."""
    counter = menu.add.counter(value=50)

    counter.increment(25)

    assert counter.get_value() == 75

    counter.reset()

    assert counter.get_value() == 50


def test_counter_reset_after_set_value(menu):
    """Reset returns to original value, not most recent value."""
    counter = menu.add.counter(value=5)

    counter.set_value(100)

    assert counter.get_value() == 100

    counter.reset()

    assert counter.get_value() == 5


def test_counter_negative_values(menu):
    """Counter accepts negative values."""
    counter = menu.add.counter()

    counter.decrement(10)

    assert counter.get_value() == -10


def test_counter_custom_format(menu):
    """Test custom formatting."""
    counter = menu.add.counter(
        value=10,
        title_format="Score: {0}",
    )

    counter.update([])

    assert counter.get_title() == "Score: 10"


def test_counter_title_updates_after_increment(menu):
    """Rendered title updates after increment."""
    counter = menu.add.counter(
        value=1,
        title_format="Value {0}",
    )

    counter.increment()

    assert counter.get_title() == "Value 2"


def test_counter_title_updates_after_decrement(menu):
    """Rendered title updates after decrement."""
    counter = menu.add.counter(
        value=5,
        title_format="Value {0}",
    )

    counter.decrement()

    assert counter.get_title() == "Value 4"


def test_counter_title_updates_after_set_value(menu):
    """Rendered title updates after setting value."""
    counter = menu.add.counter(
        title_format="Count={0}",
    )

    counter.set_value(123)

    assert counter.get_title() == "Count=123"


@pytest.mark.parametrize(
    "bad_value",
    [
        1.5,
        "10",
        [],
        {},
        None,
    ],
)
def test_counter_invalid_initial_value(menu, bad_value):
    """Reject invalid initial values."""
    with pytest.raises(AssertionError):
        menu.add.counter(value=bad_value)  # type: ignore


@pytest.mark.parametrize(
    "bad_amount",
    [
        1.5,
        "1",
        [],
        {},
        None,
    ],
)
def test_counter_invalid_increment(menu, bad_amount):
    """Reject invalid increment values."""
    counter = menu.add.counter()

    with pytest.raises(AssertionError):
        counter.increment(bad_amount)  # type: ignore


@pytest.mark.parametrize(
    "bad_amount",
    [
        1.5,
        "1",
        [],
        {},
        None,
    ],
)
def test_counter_invalid_decrement(menu, bad_amount):
    """Reject invalid decrement values."""
    counter = menu.add.counter()

    with pytest.raises(AssertionError):
        counter.decrement(bad_amount)  # type: ignore


@pytest.mark.parametrize(
    "bad_value",
    [
        1.5,
        "10",
        [],
        {},
        None,
    ],
)
def test_counter_invalid_set_value(menu, bad_value):
    """Reject invalid set values."""
    counter = menu.add.counter()

    with pytest.raises(AssertionError):
        counter.set_value(bad_value)  # type: ignore


@pytest.mark.parametrize(
    "bad_format",
    [
        1,
        1.5,
        [],
        {},
        None,
    ],
)
def test_counter_invalid_format(menu, bad_format):
    """Reject invalid title format."""
    with pytest.raises(AssertionError):
        menu.add.counter(title_format=bad_format)  # type: ignore


def test_counter_label_id(menu):
    """Test label id."""
    counter = menu.add.counter(
        label_id="counter_id",
    )

    assert counter.get_id() == "counter_id"


def test_counter_manager_returns_widget(menu):
    """Manager returns widget instance."""
    counter = menu.add.counter()

    assert counter in menu.get_widgets()


def test_counter_generator_exists(menu):
    """Counter uses a title generator."""
    counter = menu.add.counter()

    assert counter._title_generator is not None


def test_counter_generator_updates(menu):
    """Generator reflects current value."""
    counter = menu.add.counter()

    counter.increment(5)
    counter.update([])

    assert counter.get_title() == "5"


def test_counter_inherits_label_helpers(menu):
    """Counter inherits label helper methods."""
    counter = menu.add.counter(value=5)

    counter.update([])

    assert not counter.is_empty()
    assert counter.get_line_count() == 1


def test_counter_multiple_operations(menu):
    """Test chained counter operations."""
    counter = menu.add.counter(value=10)

    counter.increment(5)
    counter.decrement(3)
    counter.increment(8)

    assert counter.get_value() == 20


def test_counter_large_value(menu):
    """Counter handles large values."""
    counter = menu.add.counter(
        value=1_000_000,
    )

    assert counter.get_value() == 1_000_000


def test_counter_zero_increment(menu):
    """Incrementing by zero leaves value unchanged."""
    counter = menu.add.counter(value=10)

    counter.increment(0)

    assert counter.get_value() == 10


def test_counter_zero_decrement(menu):
    """Decrementing by zero leaves value unchanged."""
    counter = menu.add.counter(value=10)

    counter.decrement(0)

    assert counter.get_value() == 10


def test_counter_initial_title_after_update(menu):
    counter = menu.add.counter(value=10, title_format="Score: {0}")

    counter.update([])

    assert counter.get_title() == "Score: 10"


def test_counter_reset_updates_title(menu):
    counter = menu.add.counter(value=5, title_format="Count={0}")

    counter.set_value(20)
    counter.reset()

    assert counter.get_title() == "Count=5"
