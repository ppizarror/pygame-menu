"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - FPS
Test FPS widget.
"""

from unittest.mock import Mock

import pygame
import pytest

import pygame_menu.widgets.manager.fps as fps_module


class FPSManagerForTest(fps_module.FPSManager):
    def _add_submenu(self, *args, **kwargs):
        pass

    def _append_widget(self, *args, **kwargs):
        pass

    def _check_kwargs(self, *args, **kwargs):
        pass

    def _configure_widget(self, *args, **kwargs):
        pass

    def _filter_widget_attributes(self, *args, **kwargs):
        pass

    @property
    def _theme(self):
        return None

    def configure_defaults_widget(self, *args, **kwargs):
        pass


@pytest.fixture
def manager():
    return object.__new__(FPSManagerForTest)


@pytest.fixture
def clock():
    return pygame.time.Clock()


def test_fps_creates_configures_appends_and_returns_widget(
    manager,
    clock,
    monkeypatch,
):
    title_format = "Current FPS: {0:.1f}"
    label_id = "fps-label"
    attributes = {
        "font_size": 18,
        "font_color": "white",
    }
    widget = Mock(name="FPS")

    filter_attributes = Mock(return_value=attributes)
    configure_widget = Mock()
    append_widget = Mock()
    fps_factory = Mock(return_value=widget)

    monkeypatch.setattr(fps_module, "FPS", fps_factory)

    manager._filter_widget_attributes = filter_attributes
    manager._configure_widget = configure_widget
    manager._append_widget = append_widget

    result = manager.fps(
        clock,
        title_format=title_format,
        label_id=label_id,
        font_size=18,
        font_color="white",
    )

    assert result is widget
    filter_attributes.assert_called_once_with(
        {
            "font_size": 18,
            "font_color": "white",
        }
    )
    fps_factory.assert_called_once_with(
        clock=clock,
        title_format=title_format,
        label_id=label_id,
    )
    configure_widget.assert_called_once_with(
        widget=widget,
        **attributes,
    )
    append_widget.assert_called_once_with(widget)


def test_fps_uses_default_title_format_and_empty_label_id(
    manager,
    clock,
    monkeypatch,
):
    widget = Mock(name="FPS")
    fps_factory = Mock(return_value=widget)

    monkeypatch.setattr(fps_module, "FPS", fps_factory)

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.fps(clock)

    assert result is widget
    fps_factory.assert_called_once_with(
        clock=clock,
        title_format="FPS: {0:.0f}",
        label_id="",
    )


@pytest.mark.parametrize(
    ("title_format", "label_id"),
    [
        ("FPS: {0:.0f}", ""),
        ("FPS: {0:.1f}", "fps"),
        ("Current FPS = {0}", "current-fps"),
        ("", "empty-format"),
    ],
)
def test_fps_passes_title_format_and_label_id_unchanged(
    manager,
    clock,
    monkeypatch,
    title_format,
    label_id,
):
    widget = Mock(name="FPS")
    fps_factory = Mock(return_value=widget)

    monkeypatch.setattr(fps_module, "FPS", fps_factory)

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.fps(
        clock,
        title_format=title_format,
        label_id=label_id,
    )

    fps_factory.assert_called_once_with(
        clock=clock,
        title_format=title_format,
        label_id=label_id,
    )


def test_fps_passes_widget_attributes_to_filter(
    manager,
    clock,
    monkeypatch,
):
    widget = Mock(name="FPS")
    fps_factory = Mock(return_value=widget)
    filter_attributes = Mock(return_value={})

    monkeypatch.setattr(fps_module, "FPS", fps_factory)

    manager._filter_widget_attributes = filter_attributes
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.fps(
        clock,
        align="center",
        font_size=24,
        font_color=(255, 255, 255),
        label_id="fps",
    )

    filter_attributes.assert_called_once_with(
        {
            "align": "center",
            "font_size": 24,
            "font_color": (255, 255, 255),
        }
    )


def test_fps_removes_label_id_from_widget_attributes(
    manager,
    clock,
    monkeypatch,
):
    widget = Mock(name="FPS")
    fps_factory = Mock(return_value=widget)
    filter_attributes = Mock(return_value={})

    monkeypatch.setattr(fps_module, "FPS", fps_factory)

    manager._filter_widget_attributes = filter_attributes
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.fps(
        clock,
        label_id="fps-label",
        font_size=20,
    )

    filter_attributes.assert_called_once_with(
        {
            "font_size": 20,
        }
    )
    fps_factory.assert_called_once_with(
        clock=clock,
        title_format="FPS: {0:.0f}",
        label_id="fps-label",
    )


def test_fps_configures_before_appending(
    manager,
    clock,
    monkeypatch,
):
    widget = Mock(name="FPS")
    events = []

    monkeypatch.setattr(
        fps_module,
        "FPS",
        Mock(return_value=widget),
    )

    manager._filter_widget_attributes = Mock(
        side_effect=lambda attributes: (
            events.append(("filter", attributes)) or {"custom_attribute": True}
        )
    )
    manager._configure_widget = Mock(
        side_effect=lambda **kwargs: events.append(("configure", kwargs))
    )
    manager._append_widget = Mock(
        side_effect=lambda value: events.append(("append", value))
    )

    manager.fps(clock, label_id="fps")

    assert events == [
        ("filter", {}),
        (
            "configure",
            {
                "widget": widget,
                "custom_attribute": True,
            },
        ),
        ("append", widget),
    ]


def test_fps_does_not_append_when_configuration_fails(
    manager,
    clock,
    monkeypatch,
):
    widget = Mock(name="FPS")

    monkeypatch.setattr(
        fps_module,
        "FPS",
        Mock(return_value=widget),
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock(side_effect=RuntimeError("configuration failed"))
    manager._append_widget = Mock()

    with pytest.raises(RuntimeError, match="configuration failed"):
        manager.fps(clock)

    manager._append_widget.assert_not_called()


def test_fps_rejects_invalid_clock(manager):
    with pytest.raises(AssertionError):
        manager.fps(Mock())


@pytest.mark.parametrize(
    "invalid_title_format",
    [
        None,
        123,
        [],
        {},
    ],
)
def test_fps_rejects_non_string_title_format(
    manager,
    clock,
    invalid_title_format,
):
    with pytest.raises(AssertionError):
        manager.fps(
            clock,
            title_format=invalid_title_format,
        )
