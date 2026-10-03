"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - COUNTER
Test Counter widget.
"""

from unittest.mock import Mock

import pytest

import pygame_menu.widgets.manager.counter as counter_module


class CounterManagerForTest(counter_module.CounterManager):
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
    return object.__new__(CounterManagerForTest)


def test_counter_creates_configures_appends_and_returns_widget(
    manager,
    monkeypatch,
):
    value = 42
    title_format = "Score: {0}"
    label_id = "score-counter"
    attributes = {
        "font_size": 24,
        "font_color": "white",
    }
    widget = Mock(name="Counter")

    filter_attributes = Mock(return_value=attributes)
    configure_widget = Mock()
    append_widget = Mock()
    counter_factory = Mock(return_value=widget)

    monkeypatch.setattr(counter_module, "Counter", counter_factory)

    manager._filter_widget_attributes = filter_attributes
    manager._configure_widget = configure_widget
    manager._append_widget = append_widget

    result = manager.counter(
        value=value,
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
    counter_factory.assert_called_once_with(
        value=value,
        title_format=title_format,
        label_id=label_id,
    )
    configure_widget.assert_called_once_with(
        widget=widget,
        **attributes,
    )
    append_widget.assert_called_once_with(widget)


def test_counter_uses_default_value_title_format_and_empty_label_id(
    manager,
    monkeypatch,
):
    widget = Mock(name="Counter")
    counter_factory = Mock(return_value=widget)

    monkeypatch.setattr(counter_module, "Counter", counter_factory)

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.counter()

    assert result is widget

    counter_factory.assert_called_once_with(
        value=0,
        title_format="{0}",
        label_id="",
    )


@pytest.mark.parametrize(
    ("value", "title_format", "label_id"),
    [
        (0, "{0}", ""),
        (1, "Count: {0}", "count"),
        (-10, "Remaining: {0}", "remaining"),
        (100, "Total = {0}", "total"),
    ],
)
def test_counter_passes_arguments_unchanged(
    manager,
    monkeypatch,
    value,
    title_format,
    label_id,
):
    widget = Mock(name="Counter")
    counter_factory = Mock(return_value=widget)

    monkeypatch.setattr(counter_module, "Counter", counter_factory)

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.counter(
        value=value,
        title_format=title_format,
        label_id=label_id,
    )

    counter_factory.assert_called_once_with(
        value=value,
        title_format=title_format,
        label_id=label_id,
    )


def test_counter_passes_widget_attributes_to_filter(
    manager,
    monkeypatch,
):
    widget = Mock(name="Counter")
    counter_factory = Mock(return_value=widget)
    filter_attributes = Mock(return_value={})

    monkeypatch.setattr(counter_module, "Counter", counter_factory)

    manager._filter_widget_attributes = filter_attributes
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.counter(
        value=5,
        align="center",
        font_size=20,
        font_color=(255, 255, 255),
        margin=(4, 8),
        padding=3,
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


def test_counter_removes_label_id_from_widget_attributes(
    manager,
    monkeypatch,
):
    widget = Mock(name="Counter")
    counter_factory = Mock(return_value=widget)
    filter_attributes = Mock(return_value={})

    monkeypatch.setattr(counter_module, "Counter", counter_factory)

    manager._filter_widget_attributes = filter_attributes
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.counter(
        value=10,
        label_id="counter-label",
        font_size=18,
    )

    filter_attributes.assert_called_once_with(
        {
            "font_size": 18,
        }
    )
    counter_factory.assert_called_once_with(
        value=10,
        title_format="{0}",
        label_id="counter-label",
    )


def test_counter_configures_before_appending(
    manager,
    monkeypatch,
):
    widget = Mock(name="Counter")
    events = []

    monkeypatch.setattr(
        counter_module,
        "Counter",
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

    manager.counter(value=20, label_id="counter")

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


def test_counter_does_not_append_when_configuration_fails(
    manager,
    monkeypatch,
):
    widget = Mock(name="Counter")

    monkeypatch.setattr(
        counter_module,
        "Counter",
        Mock(return_value=widget),
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock(side_effect=RuntimeError("configuration failed"))
    manager._append_widget = Mock()

    with pytest.raises(RuntimeError, match="configuration failed"):
        manager.counter(value=10)

    manager._append_widget.assert_not_called()


@pytest.mark.parametrize(
    "invalid_value",
    [
        None,
        "10",
        10.5,
        [],
        {},
    ],
)
def test_counter_rejects_non_integer_values(
    manager,
    invalid_value,
):
    with pytest.raises(AssertionError):
        manager.counter(value=invalid_value)


@pytest.mark.parametrize(
    "invalid_title_format",
    [
        None,
        123,
        [],
        {},
    ],
)
def test_counter_rejects_non_string_title_formats(
    manager,
    invalid_title_format,
):
    with pytest.raises(AssertionError):
        manager.counter(title_format=invalid_title_format)
