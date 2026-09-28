"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - PROGRESSBAR
Test ProgressBar widget.
"""

import pytest

import pygame_menu
from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented
from pygame_menu.widgets.widget.progressbar import (
    ORIENTATION_HORIZONTAL,
    ORIENTATION_VERTICAL,
)
from test._utils import PYGAME_V2, MenuUtils, surface


@pytest.fixture
def menu():
    """Return a generic menu fixture."""
    return MenuUtils.generic_menu()


def test_progressbar_basic(menu):
    """Test progressbar widget."""
    pb = pygame_menu.widgets.ProgressBar(
        "progress", progress_text_font=pygame_menu.font.FONT_BEBAS
    )

    menu.add.generic_widget(pb, configure_defaults=True)
    menu.draw(surface)

    with pytest.raises(AssertionError):
        pygame_menu.widgets.ProgressBar("progress", default=-1)

    assert pb.get_size() == (312, 49)
    assert pb._width == 150


@pytest.mark.parametrize(
    "method",
    [
        "rotate",
        "flip",
        "scale",
        "resize",
        "set_max_width",
        "set_max_height",
    ],
)
def test_progressbar_invalid_transforms(menu, method):
    """Test invalid progressbar transforms."""
    pb = pygame_menu.widgets.ProgressBar("progress")
    with pytest.raises(WidgetTransformationNotImplemented):
        getattr(pb, method)()


def test_progressbar_update(menu):
    """Test progressbar update."""
    pb = pygame_menu.widgets.ProgressBar("progress")
    menu.add.generic_widget(pb, configure_defaults=True)
    assert not pb.update([])


def test_progressbar_value(menu):
    """Test progressbar value."""
    pb = menu.add.progress_bar(
        "progress", default=50, progress_text_align=pygame_menu.locals.ALIGN_LEFT
    )

    with pytest.raises(AssertionError):
        pb.set_value(-1)

    with pytest.raises(AssertionError):
        pb.set_value("a")  # type: ignore

    assert pb.get_value() == 50
    assert not pb.value_changed()

    pb.set_value(75)
    assert pb.get_value() == 75
    assert pb.value_changed()

    pb.reset_value()
    assert pb.get_value() == 50
    assert not pb.value_changed()


def test_progressbar_empty_title(menu):
    """Test progressbar empty title."""
    pb = menu.add.progress_bar(
        "",
        box_margin=(0, 0),
        padding=0,
        progress_text_align=pygame_menu.locals.ALIGN_RIGHT,
    )

    expected_height = 41 if PYGAME_V2 else 42
    assert pb.get_size() == (150, expected_height)
    assert not pb.is_selected()


def test_progressbar_custom_range_and_clamping(menu):
    """Test progressbar custom min/max range, bounds validation, and clamping."""
    with pytest.raises(AssertionError):
        pygame_menu.widgets.ProgressBar("progress", min_value=50, max_value=50)
    with pytest.raises(AssertionError):
        pygame_menu.widgets.ProgressBar("progress", min_value=100, max_value=10)

    with pytest.raises(AssertionError):
        pygame_menu.widgets.ProgressBar(
            "progress", default=150, min_value=0, max_value=100
        )
    with pytest.raises(AssertionError):
        pygame_menu.widgets.ProgressBar(
            "progress", default=-5, min_value=0, max_value=100
        )

    pb = pygame_menu.widgets.ProgressBar(
        "progress", default=25, min_value=0, max_value=50
    )
    assert pb.get_min_value() == 0
    assert pb.get_max_value() == 50
    assert pb.get_value() == 25
    assert pb.get_percentage() == 50.0

    pb.set_range(20, 30)
    assert pb.get_min_value() == 20
    assert pb.get_max_value() == 30
    assert pb.get_value() == 25

    pb.set_value(30)
    pb.set_range(0, 20)
    assert pb.get_value() == 20

    with pytest.raises(AssertionError):
        pb.set_range(50, 20)


def test_progressbar_orientation_edge_cases(menu):
    """Test horizontal and vertical orientations and their layouts."""
    pb_h = pygame_menu.widgets.ProgressBar(
        "h",
        orientation=ORIENTATION_HORIZONTAL,
        width=150,
        height=30,
    )
    pb_v = pygame_menu.widgets.ProgressBar(
        "v", orientation=ORIENTATION_VERTICAL, width=150, height=200
    )

    menu.add.generic_widget(pb_h, configure_defaults=True)
    menu.add.generic_widget(pb_v, configure_defaults=True)
    menu.draw(surface)

    assert pb_h._orientation == ORIENTATION_HORIZONTAL
    assert pb_v._orientation == ORIENTATION_VERTICAL

    with pytest.raises(AssertionError):
        pygame_menu.widgets.ProgressBar("invalid", orientation="diagonal")


def test_progressbar_increments_and_boundaries(menu):
    """Test increment/decrement boundaries and custom step amounts."""
    pb = pygame_menu.widgets.ProgressBar(
        "progress", default=10, min_value=0, max_value=20
    )

    pb.increment(5)
    assert pb.get_value() == 15

    pb.decrement(3)
    assert pb.get_value() == 12

    pb.increment(100)
    assert pb.get_value() == 20

    pb.decrement(100)
    assert pb.get_value() == 0


def test_progressbar_increment_decrement_invalid_type():
    """Test increment/decrement reject non-numeric values."""
    pb = pygame_menu.widgets.ProgressBar("progress")

    with pytest.raises(AssertionError):
        pb.increment("1")  # type: ignore

    with pytest.raises(AssertionError):
        pb.decrement("1")  # type: ignore


def test_progressbar_set_range_invalid_types():
    """Test set_range validates numeric arguments."""
    pb = pygame_menu.widgets.ProgressBar("progress")

    with pytest.raises(AssertionError):
        pb.set_range("0", 10)  # type: ignore

    with pytest.raises(AssertionError):
        pb.set_range(0, "10")  # type: ignore


def test_progressbar_percentage_boundaries():
    """Test percentage calculation at minimum and maximum values."""
    pb = pygame_menu.widgets.ProgressBar(
        "progress",
        default=0,
        min_value=0,
        max_value=20,
    )

    assert pb.get_percentage() == 0.0

    pb.set_value(20)
    assert pb.get_percentage() == 100.0

    pb.set_value(10)
    assert pb.get_percentage() == 50.0


def test_progressbar_get_value_as_string_default():
    """Test default progress text formatting."""
    pb = pygame_menu.widgets.ProgressBar(
        "progress",
        default=25.5,
    )

    assert pb.get_value(as_string=True) == "25.5 %"


def test_progressbar_vertical_layout_geometry(menu):
    """Verify vertical progress bars place the box below the title."""
    pb = pygame_menu.widgets.ProgressBar(
        "progress",
        orientation=ORIENTATION_VERTICAL,
        width=150,
        height=20,
    )

    menu.add.generic_widget(pb, configure_defaults=True)
    menu.draw(surface)

    assert pb._box_offset_x == 0
    assert pb._box_offset_y > 0


def test_progressbar_horizontal_layout_geometry(menu):
    """Verify horizontal progress bars place the box beside the title."""
    pb = pygame_menu.widgets.ProgressBar(
        "progress",
        orientation=ORIENTATION_HORIZONTAL,
        width=150,
        height=20,
    )

    menu.add.generic_widget(pb, configure_defaults=True)
    menu.draw(surface)

    assert pb._box_offset_x > 0
    assert pb._box_offset_y == 0


def test_progressbar_vertical_dimensions(menu):
    """Verify vertical progress bars swap width and height."""
    pb = pygame_menu.widgets.ProgressBar(
        "progress",
        orientation=ORIENTATION_VERTICAL,
        width=150,
        height=20,
    )

    menu.add.generic_widget(pb, configure_defaults=True)
    menu.draw(surface)

    assert pb._box.get_width() == 20
    assert pb._box.get_height() == 150


def test_progressbar_box_margin_affects_widget_size(menu):
    """Verify box margin contributes to widget geometry."""
    pb_no_margin = pygame_menu.widgets.ProgressBar(
        "progress",
        box_margin=(0, 0),
    )

    pb_margin = pygame_menu.widgets.ProgressBar(
        "progress",
        box_margin=(50, 0),
    )

    menu.add.generic_widget(pb_no_margin, configure_defaults=True)
    menu.draw(surface)
    size_no_margin = pb_no_margin.get_size()

    menu.clear()
    menu.add.generic_widget(pb_margin, configure_defaults=True)
    menu.draw(surface)
    size_margin = pb_margin.get_size()

    assert size_margin[0] > size_no_margin[0]


def test_progressbar_percentage_custom_range():
    """Verify percentage is computed correctly for arbitrary ranges."""
    pb = pygame_menu.widgets.ProgressBar(
        "progress",
        default=75,
        min_value=50,
        max_value=150,
    )

    assert pb.get_percentage() == 25.0

    pb.set_value(100)
    assert pb.get_percentage() == 50.0

    pb.set_value(150)
    assert pb.get_percentage() == 100.0


def test_progressbar_increment_decrement_default_step():
    """Verify increment and decrement use a default step of one."""
    pb = pygame_menu.widgets.ProgressBar(
        "progress",
        default=10,
        min_value=0,
        max_value=20,
    )

    pb.increment()
    assert pb.get_value() == 11

    pb.decrement()
    assert pb.get_value() == 10


def test_progressbar_is_complete():
    """Test is_complete method under various progress values."""
    pb = pygame_menu.widgets.ProgressBar(
        "progress",
        default=50,
        min_value=0,
        max_value=100,
    )

    assert not pb.is_complete()

    pb.set_value(100)
    assert pb.is_complete()

    pb.set_value(75)
    assert not pb.is_complete()


def test_progressbar_set_percentage():
    """Test set_percentage method with valid values, clamping, and invalid inputs."""
    pb = pygame_menu.widgets.ProgressBar(
        "progress",
        min_value=0,
        max_value=100,
    )

    # Happy path: 50% of range (0 to 100, span is 100) -> value should be 50.0
    pb.set_percentage(50.0)
    assert pb.get_value() == 50.0

    # Clamping: below 0% clamps to min_value (0)
    pb.set_percentage(-10.0)
    assert pb.get_value() == 0.0

    # Clamping: above 100% clamps to max_value (100)
    pb.set_percentage(150.0)
    assert pb.get_value() == 100.0

    # Error handling: non-numeric type validation
    with pytest.raises(AssertionError):
        pb.set_percentage("50")  # type: ignore


def test_progressbar_reset():
    """Test reset method restores the default value correctly."""
    pb = pygame_menu.widgets.ProgressBar(
        "progress",
        default=25,
        min_value=0,
        max_value=100,
    )

    pb.set_value(90)
    assert pb.get_value() == 90

    pb.reset()
    assert pb.get_value() == 25
