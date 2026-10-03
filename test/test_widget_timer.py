"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - TIMER
Test Timer widget.
"""

import time

import pytest

import pygame_menu
from test._utils import MenuUtils


@pytest.fixture
def menu():
    """Provides a fresh generic menu for each test."""
    return MenuUtils.generic_menu()


def test_timer_creation(menu):
    """Test timer creation."""
    timer = menu.add.timer()

    assert isinstance(timer, pygame_menu.widgets.Timer)
    assert timer.get_elapsed() == 0.0
    assert not timer.is_running()
    assert not timer.is_paused()


def test_timer_initial_title(menu):
    """Test initial timer title."""
    timer = menu.add.timer()

    timer.update([])

    assert timer.get_title() == "00:00"


def test_timer_start(menu):
    """Test timer start."""
    timer = menu.add.timer()

    timer.start()

    assert timer.is_running()
    assert not timer.is_paused()
    assert timer._start_time is not None


def test_timer_pause_before_start(menu):
    """Pause before start must be safe."""
    timer = menu.add.timer()

    timer.pause()

    assert timer.get_elapsed() == 0
    assert not timer.is_running()


def test_timer_resume_before_start(menu):
    """Resume before start must do nothing."""
    timer = menu.add.timer()

    timer.resume()

    assert not timer.is_running()
    assert timer.get_elapsed() == 0


def test_timer_double_start(menu):
    """Starting twice must not reset start time."""
    timer = menu.add.timer()

    timer.start()
    start = timer._start_time

    timer.start()

    assert timer._start_time == start


def test_timer_pause(menu):
    """Pause timer."""
    timer = menu.add.timer()

    timer.start()
    timer.pause()

    assert not timer.is_running()


def test_timer_resume(menu):
    """Resume paused timer."""
    timer = menu.add.timer()

    timer.start()
    timer.pause()
    timer.resume()

    assert timer.is_running()


def test_timer_double_pause(menu):
    """Double pause must be safe."""
    timer = menu.add.timer()

    timer.start()
    timer.pause()

    elapsed = timer.get_elapsed()

    timer.pause()

    assert timer.get_elapsed() == elapsed


def test_timer_reset(menu):
    """Reset timer state."""
    timer = menu.add.timer()

    timer.start()
    timer.reset()

    assert timer.get_elapsed() == 0
    assert not timer.is_running()
    assert not timer.is_paused()
    assert timer.get_title() == "00:00"


def test_timer_set_elapsed(menu):
    """Set elapsed time."""
    timer = menu.add.timer()

    timer.set_elapsed(90)

    assert timer.get_elapsed() == pytest.approx(90)


def test_timer_negative_elapsed(menu):
    """Reject negative elapsed values."""
    timer = menu.add.timer()

    with pytest.raises(AssertionError):
        timer.set_elapsed(-1)


def test_timer_is_paused(menu):
    """Paused state detection."""
    timer = menu.add.timer()

    timer.start()
    timer.pause()

    assert timer.is_paused()


def test_timer_custom_format(menu):
    """Custom timer format."""
    timer = menu.add.timer(title_format="{0}m {1}s")

    timer.set_elapsed(125)
    timer.update([])

    assert timer.get_title() == "2m 5s"


def test_timer_generator_active(menu):
    """Timer uses title generator."""
    timer = menu.add.timer()

    assert timer._title_generator is not None


def test_timer_clear(menu):
    """Timer inherits label helper methods."""
    timer = menu.add.timer()

    timer.clear()

    assert timer.is_empty()


def test_timer_label_id(menu):
    """Timer label id."""
    timer = menu.add.timer(label_id="timer1")

    assert timer.get_id() == "timer1"


def test_timer_invalid_format(menu):
    """Reject invalid title format."""
    with pytest.raises(AssertionError):
        menu.add.timer(title_format=123)  # type: ignore


def test_timer_elapsed_progress(menu):
    """Timer accumulates elapsed time."""
    timer = menu.add.timer()

    timer.start()
    time.sleep(0.05)
    timer.pause()

    assert timer.get_elapsed() > 0


def test_timer_resume_accumulates(menu):
    """Resume continues accumulation."""
    timer = menu.add.timer()

    timer.start()
    time.sleep(0.02)
    timer.pause()

    first = timer.get_elapsed()

    timer.resume()
    time.sleep(0.02)
    timer.pause()

    second = timer.get_elapsed()

    assert second > first


def test_timer_set_elapsed_while_running(menu):
    """Setting elapsed time while running preserves running state."""
    timer = menu.add.timer()

    timer.start()
    timer.set_elapsed(100)

    assert timer.is_running()
    assert timer.get_elapsed() >= 100


def test_timer_reset_after_pause(menu):
    """Reset after pause clears state."""
    timer = menu.add.timer()

    timer.start()
    timer.pause()
    timer.reset()

    assert timer.get_elapsed() == 0
    assert not timer.is_running()
    assert not timer.is_paused()


def test_timer_manager_returns_widget(menu):
    """Timer manager returns the widget."""
    timer = menu.add.timer()

    assert timer in menu.get_widgets()


def test_timer_multiple_resumes(menu):
    """Multiple resumes must be safe."""
    timer = menu.add.timer()

    timer.start()
    timer.pause()

    timer.resume()
    start = timer._start_time

    timer.resume()

    assert timer._start_time == start


def test_timer_state_transitions(menu):
    """Test complete timer lifecycle."""
    timer = menu.add.timer()

    assert not timer.is_running()

    timer.start()
    assert timer.is_running()

    timer.pause()
    assert timer.is_paused()

    timer.resume()
    assert timer.is_running()

    timer.reset()
    assert not timer.is_running()
    assert not timer.is_paused()


def test_timer_elapsed_with_fake_clock(menu, monkeypatch):
    now = 100.0

    def fake_monotonic():
        return now

    monkeypatch.setattr(time, "monotonic", fake_monotonic)

    timer = menu.add.timer()
    timer.start()

    now += 10.5

    assert timer.get_elapsed() == pytest.approx(10.5)


def test_timer_pause_preserves_elapsed(menu, monkeypatch):
    now = 100.0
    monkeypatch.setattr(time, "monotonic", lambda: now)

    timer = menu.add.timer()
    timer.start()

    now += 12
    timer.pause()

    assert timer.get_elapsed() == pytest.approx(12)
    assert not timer.is_running()
    assert timer.is_paused()


def test_timer_resume_at_zero_elapsed(menu, monkeypatch):
    clock = [100.0]
    monkeypatch.setattr(time, "monotonic", lambda: clock[0])

    timer = menu.add.timer()
    timer.start()
    timer.pause()

    assert timer.get_elapsed() == 0.0
    assert timer.is_paused()

    timer.resume()
    clock[0] += 5

    assert timer.get_elapsed() == pytest.approx(5)


def test_timer_update_refreshes_running_title(menu, monkeypatch):
    clock = [100.0]
    monkeypatch.setattr(time, "monotonic", lambda: clock[0])

    timer = menu.add.timer()
    timer.start()

    timer.update([])
    assert timer.get_title() == "00:00"

    clock[0] += 61
    timer.update([])

    assert timer.get_title() == "01:01"


def test_timer_set_elapsed_while_paused(menu):
    timer = menu.add.timer()

    timer.start()
    timer.pause()
    timer.set_elapsed(90)

    assert timer.get_elapsed() == pytest.approx(90)
    assert not timer.is_running()
    assert timer.is_paused()


def test_timer_set_elapsed_rejects_non_numeric_values(menu):
    timer = menu.add.timer()

    with pytest.raises((AssertionError, TypeError)):
        timer.set_elapsed("10")  # type: ignore


def test_timer_fractional_seconds_are_formatted_down(menu):
    timer = menu.add.timer()

    timer.set_elapsed(125.99)
    timer.update([])

    assert timer.get_title() == "02:05"


def test_timer_over_one_hour(menu):
    timer = menu.add.timer()

    timer.set_elapsed(3661)
    timer.update([])

    assert timer.get_title() == "61:01"


def test_timer_update_after_clear_restores_generated_title(menu):
    timer = menu.add.timer()

    timer.clear()
    assert timer.is_empty()

    timer.update([])

    assert timer.get_title() == "00:00"
