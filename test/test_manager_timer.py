"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - TIMER
Test Timer widget.
"""

from unittest.mock import Mock

import pytest

import pygame_menu.widgets.manager.timer as timer_module


class TimerManagerForTest(timer_module.TimerManager):
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
    return object.__new__(TimerManagerForTest)


def test_timer_creates_configures_appends_registers_and_returns_widget(
    manager,
    monkeypatch,
):
    title_format = "Elapsed: {0:02d}:{1:02d}"
    label_id = "timer-label"
    attributes = {
        "font_size": 24,
        "font_color": "white",
    }
    widget = Mock(name="Timer")

    filter_attributes = Mock(return_value=attributes)
    configure_widget = Mock()
    append_widget = Mock()
    timer_factory = Mock(return_value=widget)

    monkeypatch.setattr(timer_module, "Timer", timer_factory)

    manager._filter_widget_attributes = filter_attributes
    manager._configure_widget = configure_widget
    manager._append_widget = append_widget

    result = manager.timer(
        title_format=title_format,
        label_id=label_id,
        font_size=24,
        font_color="white",
    )

    assert result is widget

    filter_attributes.assert_called_once_with(
        {
            "font_size": 24,
            "font_color": "white",
        }
    )
    timer_factory.assert_called_once_with(
        title_format=title_format,
        label_id=label_id,
    )
    configure_widget.assert_called_once_with(
        widget=widget,
        **attributes,
    )
    append_widget.assert_called_once_with(widget)
    widget.set_title_generator.assert_called_once_with(widget._generate_title)


def test_timer_uses_default_title_format_and_empty_label_id(
    manager,
    monkeypatch,
):
    widget = Mock(name="Timer")
    timer_factory = Mock(return_value=widget)

    monkeypatch.setattr(timer_module, "Timer", timer_factory)

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.timer()

    assert result is widget

    timer_factory.assert_called_once_with(
        title_format="{0:02d}:{1:02d}",
        label_id="",
    )
    widget.set_title_generator.assert_called_once_with(widget._generate_title)


@pytest.mark.parametrize(
    ("title_format", "label_id"),
    [
        ("{0:02d}:{1:02d}", ""),
        ("Time: {0:02d}:{1:02d}", "timer"),
        ("Elapsed = {0}:{1}", "elapsed-time"),
        ("", "empty-format"),
    ],
)
def test_timer_passes_title_format_and_label_id_unchanged(
    manager,
    monkeypatch,
    title_format,
    label_id,
):
    widget = Mock(name="Timer")
    timer_factory = Mock(return_value=widget)

    monkeypatch.setattr(timer_module, "Timer", timer_factory)

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.timer(
        title_format=title_format,
        label_id=label_id,
    )

    timer_factory.assert_called_once_with(
        title_format=title_format,
        label_id=label_id,
    )


def test_timer_passes_widget_attributes_to_filter(
    manager,
    monkeypatch,
):
    widget = Mock(name="Timer")
    timer_factory = Mock(return_value=widget)
    filter_attributes = Mock(return_value={})

    monkeypatch.setattr(timer_module, "Timer", timer_factory)

    manager._filter_widget_attributes = filter_attributes
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.timer(
        align="center",
        font_size=20,
        font_color=(255, 255, 255),
        margin=(4, 8),
        padding=3,
        label_id="timer",
    )

    filter_attributes.assert_called_once_with(
        {
            "align": "center",
            "font_size": 20,
            "font_color": (255, 255, 255),
            "margin": (4, 8),
            "padding": 3,
        }
    )


def test_timer_removes_label_id_from_widget_attributes(
    manager,
    monkeypatch,
):
    widget = Mock(name="Timer")
    timer_factory = Mock(return_value=widget)
    filter_attributes = Mock(return_value={})

    monkeypatch.setattr(timer_module, "Timer", timer_factory)

    manager._filter_widget_attributes = filter_attributes
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.timer(
        label_id="timer-label",
        font_size=18,
    )

    filter_attributes.assert_called_once_with(
        {
            "font_size": 18,
        }
    )
    timer_factory.assert_called_once_with(
        title_format="{0:02d}:{1:02d}",
        label_id="timer-label",
    )


def test_timer_configures_before_appending_and_registering_generator(
    manager,
    monkeypatch,
):
    widget = Mock(name="Timer")
    events = []

    monkeypatch.setattr(
        timer_module,
        "Timer",
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
    widget.set_title_generator = Mock(
        side_effect=lambda generator: events.append(("set_title_generator", generator))
    )

    manager.timer(label_id="timer")

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
        ("set_title_generator", widget._generate_title),
    ]


def test_timer_does_not_append_or_register_generator_when_configuration_fails(
    manager,
    monkeypatch,
):
    widget = Mock(name="Timer")

    monkeypatch.setattr(
        timer_module,
        "Timer",
        Mock(return_value=widget),
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock(side_effect=RuntimeError("configuration failed"))
    manager._append_widget = Mock()

    with pytest.raises(RuntimeError, match="configuration failed"):
        manager.timer()

    manager._append_widget.assert_not_called()
    widget.set_title_generator.assert_not_called()


def test_timer_does_not_register_generator_when_appending_fails(
    manager,
    monkeypatch,
):
    widget = Mock(name="Timer")

    monkeypatch.setattr(
        timer_module,
        "Timer",
        Mock(return_value=widget),
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock(side_effect=RuntimeError("append failed"))

    with pytest.raises(RuntimeError, match="append failed"):
        manager.timer()

    widget.set_title_generator.assert_not_called()


@pytest.mark.parametrize(
    "invalid_title_format",
    [
        None,
        123,
        10.5,
        [],
        {},
    ],
)
def test_timer_rejects_non_string_title_formats(
    manager,
    invalid_title_format,
):
    with pytest.raises(AssertionError):
        manager.timer(title_format=invalid_title_format)
