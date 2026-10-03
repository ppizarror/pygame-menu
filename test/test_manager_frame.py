"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - FRAME
Test Frame widget.
"""

from unittest.mock import Mock

import pytest

import pygame_menu.widgets.manager.frame as frame_module
from pygame_menu.locals import (
    ORIENTATION_HORIZONTAL,
    ORIENTATION_VERTICAL,
    POSITION_SOUTHWEST,
    SCROLLAREA_POSITION_NONE,
)


class TestableFrameManager(frame_module.FrameManager):
    __test__ = False  # Prevents pytest from collecting this as a test class

    def _add_submenu(self, *args, **kwargs):
        pass

    def _append_widget(self, *args, **kwargs):
        pass

    def _check_kwargs(self, *args, **kwargs):
        pass

    def _configure_widget(self, *args, **kwargs):
        pass

    def _filter_widget_attributes(self, *args, **kwargs):
        return {"padding": 10}

    def configure_defaults_widget(self, *args, **kwargs):
        pass

    @property
    def _theme(self):
        theme = Mock()
        theme.scrollbar_color = (100, 100, 100)
        theme.scrollbar_cursor = None
        theme.scrollbar_shadow = False
        theme.scrollbar_shadow_color = (0, 0, 0)
        theme.scrollbar_shadow_offset = 2
        theme.scrollbar_shadow_position = "se"
        theme.scrollbar_slider_color = (150, 150, 150)
        theme.scrollbar_slider_hover_color = (200, 200, 200)
        theme.scrollbar_slider_pad = 1
        theme.scrollbar_thick = 12
        theme.scrollarea_position = SCROLLAREA_POSITION_NONE
        return theme


@pytest.fixture
def manager():
    return object.__new__(TestableFrameManager)


def test_frame_horizontal_happy_path(manager, monkeypatch):
    widget_mock = Mock(name="Frame")
    frame_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(frame_module, "Frame", frame_factory)
    monkeypatch.setattr(frame_module, "parse_padding", lambda p: (10, 10, 10, 10))

    result = manager.frame_h(
        width=200,
        height=100,
        frame_id="frame-h-1",
        align="left",
    )

    assert result is widget_mock
    frame_factory.assert_called_once_with(
        width=180,
        height=80,
        orientation=ORIENTATION_HORIZONTAL,
        frame_id="frame-h-1",
    )
    widget_mock.make_scrollarea.assert_called_once()


def test_frame_vertical_happy_path(manager, monkeypatch):
    widget_mock = Mock(name="Frame")
    frame_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(frame_module, "Frame", frame_factory)
    monkeypatch.setattr(frame_module, "parse_padding", lambda p: (5, 5, 5, 5))

    result = manager.frame_v(
        width=150,
        height=300,
        frame_id="frame-v-1",
    )

    assert result is widget_mock
    frame_factory.assert_called_once_with(
        width=140,
        height=290,
        orientation=ORIENTATION_VERTICAL,
        frame_id="frame-v-1",
    )


def test_frame_filters_invalid_kwargs(manager, monkeypatch):
    widget_mock = Mock(name="Frame")
    frame_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(frame_module, "Frame", frame_factory)
    monkeypatch.setattr(frame_module, "parse_padding", lambda p: (0, 0, 0, 0))

    filter_attributes = Mock(return_value={"padding": 0})
    manager._filter_widget_attributes = filter_attributes

    manager.frame_h(
        width=100,
        height=100,
        align="center",
        invalid_key_to_drop="should_be_removed",
        background_color=(255, 255, 255),
    )

    filter_attributes.assert_called_once()
    widget_mock.make_scrollarea.assert_called_once()


def test_frame_width_height_padding_assertions(manager, monkeypatch):
    monkeypatch.setattr(frame_module, "Frame", Mock())
    monkeypatch.setattr(frame_module, "parse_padding", lambda p: (50, 50, 50, 50))

    with pytest.raises(
        AssertionError, match="frame width.*cannot be lower than horizontal padding"
    ):
        manager.frame_h(width=80, height=200)

    with pytest.raises(
        AssertionError, match="frame height.*cannot be lower than vertical padding"
    ):
        manager.frame_h(width=200, height=80)


def test_frame_scrollarea_custom_arguments(manager, monkeypatch):
    widget_mock = Mock(name="Frame")
    frame_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(frame_module, "Frame", frame_factory)
    monkeypatch.setattr(frame_module, "parse_padding", lambda p: (0, 0, 0, 0))

    manager.frame_h(
        width=100,
        height=100,
        max_height=80,
        max_width=80,
        scrollarea_color=(50, 50, 50),
        scrollbar_thick=15,
        scrollbars=POSITION_SOUTHWEST,
    )

    _, scrollarea_kwargs = widget_mock.make_scrollarea.call_args
    assert scrollarea_kwargs["max_height"] == 80
    assert scrollarea_kwargs["max_width"] == 80
    assert scrollarea_kwargs["scrollarea_color"] == (50, 50, 50)
    assert scrollarea_kwargs["scrollbar_thick"] == 15


def test_frame_theme_defaults_used(manager, monkeypatch):
    widget_mock = Mock(name="Frame")
    frame_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(frame_module, "Frame", frame_factory)
    monkeypatch.setattr(frame_module, "parse_padding", lambda p: (0, 0, 0, 0))

    manager.frame_v(width=100, height=100)

    _, scrollarea_kwargs = widget_mock.make_scrollarea.call_args
    assert scrollarea_kwargs["scrollbar_color"] == manager._theme.scrollbar_color
    assert scrollarea_kwargs["scrollbar_thick"] == manager._theme.scrollbar_thick


def test_frame_max_dimensions_default_to_full(manager, monkeypatch):
    widget_mock = Mock(name="Frame")
    frame_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(frame_module, "Frame", frame_factory)
    monkeypatch.setattr(frame_module, "parse_padding", lambda p: (10, 10, 10, 10))

    manager.frame_h(width=200, height=150)

    _, scrollarea_kwargs = widget_mock.make_scrollarea.call_args
    # width=200 - pad_h(20) = 180, height=150 - pad_v(20) = 130
    assert scrollarea_kwargs["max_width"] == 180
    assert scrollarea_kwargs["max_height"] == 130


def test_frame_appends_and_checks_kwargs(manager, monkeypatch):
    widget_mock = Mock(name="Frame")
    frame_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(frame_module, "Frame", frame_factory)
    monkeypatch.setattr(frame_module, "parse_padding", lambda p: (0, 0, 0, 0))

    append_mock = Mock()
    check_kwargs_mock = Mock()
    monkeypatch.setattr(manager, "_append_widget", append_mock)
    monkeypatch.setattr(manager, "_check_kwargs", check_kwargs_mock)

    manager.frame_h(width=100, height=100, custom_param="test")

    append_mock.assert_called_once_with(widget_mock)
    check_kwargs_mock.assert_called_once()
