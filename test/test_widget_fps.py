"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - FPS
Test FPS widget.
"""

import pygame
import pytest

import pygame_menu
from test._utils import MenuUtils


@pytest.fixture
def menu():
    """Provides a fresh generic menu for each test."""
    return MenuUtils.generic_menu()


@pytest.fixture
def clock():
    """Provides a pygame clock."""
    return pygame.time.Clock()


def test_fps_creation(menu, clock):
    """Test FPS widget creation."""
    fps = menu.add.fps(clock)

    assert isinstance(fps, pygame_menu.widgets.FPS)
    assert fps.get_fps() >= 0


def test_fps_generator_exists(menu, clock):
    """Test FPS title generator exists."""
    fps = menu.add.fps(clock)

    assert fps._title_generator is not None


def test_fps_initial_title_is_not_empty(menu, clock):
    """FPS should have a title immediately after creation."""
    fps = menu.add.fps(clock)

    assert not fps.is_empty()
    assert fps.get_title().startswith("FPS:")


def test_fps_get_fps(menu, clock):
    """Test FPS getter."""
    fps = menu.add.fps(clock)

    value = fps.get_fps()

    assert isinstance(value, float)
    assert value >= 0


def test_fps_custom_format(menu, clock):
    """Test custom FPS format."""
    fps = menu.add.fps(clock, title_format="{0:.1f} FPS")

    fps.update([])

    assert "FPS" in fps.get_title()


def test_fps_label_id(menu, clock):
    """Test FPS label id."""
    fps = menu.add.fps(
        clock,
        label_id="fps_counter",
    )

    assert fps.get_id() == "fps_counter"


def test_fps_invalid_clock(menu):
    """Reject invalid clock."""
    with pytest.raises(AssertionError):
        menu.add.fps("bad_clock")  # type: ignore


@pytest.mark.parametrize(
    "bad_format",
    [
        1,
        1.5,
        [],
        {},
        True,
    ],
)
def test_fps_invalid_format(menu, clock, bad_format):
    """Reject invalid title formats."""
    with pytest.raises(AssertionError):
        menu.add.fps(clock, title_format=bad_format)  # type: ignore


def test_fps_update_title(menu, clock):
    """Updating FPS should update title."""
    fps = menu.add.fps(clock)

    clock.tick(60)

    fps.update([])

    assert isinstance(fps.get_title(), str)
    assert len(fps.get_title()) > 0


def test_fps_manager_returns_widget(menu, clock):
    """Manager should return a widget."""
    fps = menu.add.fps(clock)

    assert fps in menu.get_widgets()


def test_fps_inherits_label_helpers(menu, clock):
    """FPS inherits label helper API."""
    fps = menu.add.fps(clock)

    assert not fps.is_empty()

    fps.clear()

    assert fps.is_empty()


def test_fps_renders_after_clear(menu, clock):
    """Cleared FPS label regenerates title on update."""
    fps = menu.add.fps(clock)

    fps.clear()
    assert fps.is_empty()

    fps.update([])

    assert not fps.is_empty()


def test_fps_multiple_updates(menu, clock):
    """Multiple updates should not fail."""
    fps = menu.add.fps(clock)

    for _ in range(10):
        clock.tick(60)
        fps.update([])

    assert isinstance(fps.get_title(), str)


def test_fps_title_changes_with_generator(menu, clock):
    """FPS title generator remains active."""
    fps = menu.add.fps(clock)

    fps.get_title()

    clock.tick(60)
    fps.update([])

    title_b = fps.get_title()

    assert isinstance(title_b, str)
    assert title_b != ""


def test_fps_accepts_widget_configuration(menu, clock):
    """FPS accepts widget configuration kwargs."""
    fps = menu.add.fps(
        clock,
        font_size=20,
        margin=(5, 5),
        padding=5,
    )

    assert fps.get_margin() == (5, 5)
    assert fps.get_font_info()["size"] == 20


def test_fps_width_and_height(menu, clock):
    """FPS widget has valid geometry."""
    fps = menu.add.fps(clock)

    fps.update([])

    assert fps.get_width() >= 0
    assert fps.get_height() >= 0


def test_fps_draw(menu, clock):
    """FPS can be drawn."""
    from test._utils import surface

    fps = menu.add.fps(clock)

    fps.draw(surface)

    assert fps.get_width() >= 0


def test_fps_generator_returns_string(menu, clock):
    """FPS generator returns string values."""
    fps = menu.add.fps(clock)

    fps.update([])

    assert isinstance(fps.get_title(), str)


def test_fps_title_formatting(menu, clock):
    """FPS title formatting is respected."""
    fps = menu.add.fps(clock, title_format="Current FPS = {0:.0f}")

    fps.update([])

    assert fps.get_title().startswith("Current FPS =")


def test_fps_clock_reference(menu, clock):
    """FPS stores clock reference."""
    fps = menu.add.fps(clock)

    assert fps._clock is clock


def test_fps_zero_fps(menu):
    """New clocks should report valid FPS values."""
    clock = pygame.time.Clock()

    fps = menu.add.fps(clock)

    assert fps.get_fps() >= 0
