"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - NONE WIDGET
Test NoneWidget widget.
"""

from unittest.mock import Mock

import pytest

import pygame_menu.widgets.manager.none as none_module


class TestableNoneWidgetManager(none_module.NoneWidgetManager):
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
    return object.__new__(TestableNoneWidgetManager)


def test_none_widget_creates_configures_appends_and_returns_widget(
    manager,
    monkeypatch,
):
    widget_id = "placeholder"
    attributes = {"draw_callback": Mock()}
    widget = Mock(name="NoneWidget")

    filter_attributes = Mock(return_value=attributes)
    configure_widget = Mock()
    append_widget = Mock()
    none_widget_factory = Mock(return_value=widget)

    monkeypatch.setattr(
        none_module,
        "NoneWidget",
        none_widget_factory,
    )

    manager._filter_widget_attributes = filter_attributes
    manager._configure_widget = configure_widget
    manager._append_widget = append_widget

    result = manager.none_widget(widget_id)

    assert result is widget

    filter_attributes.assert_called_once_with({})

    none_widget_factory.assert_called_once_with(
        widget_id=widget_id,
    )

    configure_widget.assert_called_once_with(
        widget=widget,
        **attributes,
    )

    append_widget.assert_called_once_with(widget)


def test_none_widget_uses_empty_string_as_default_id(
    manager,
    monkeypatch,
):
    widget = Mock(name="NoneWidget")
    none_widget_factory = Mock(return_value=widget)

    monkeypatch.setattr(
        none_module,
        "NoneWidget",
        none_widget_factory,
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.none_widget()

    assert result is widget

    none_widget_factory.assert_called_once_with(
        widget_id="",
    )


@pytest.mark.parametrize(
    "widget_id",
    [
        "",
        "placeholder",
        "none-widget",
        "widget_123",
        "0",
        None,
        123,
    ],
)
def test_none_widget_passes_widget_id_unchanged(
    manager,
    monkeypatch,
    widget_id,
):
    widget = Mock(name="NoneWidget")
    none_widget_factory = Mock(return_value=widget)

    monkeypatch.setattr(
        none_module,
        "NoneWidget",
        none_widget_factory,
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.none_widget(widget_id)

    assert result is widget

    none_widget_factory.assert_called_once_with(
        widget_id=widget_id,
    )


def test_none_widget_filters_empty_attribute_dictionary(
    manager,
    monkeypatch,
):
    widget = Mock(name="NoneWidget")
    none_widget_factory = Mock(return_value=widget)
    filter_attributes = Mock(return_value={})

    monkeypatch.setattr(
        none_module,
        "NoneWidget",
        none_widget_factory,
    )

    manager._filter_widget_attributes = filter_attributes
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.none_widget("placeholder")

    filter_attributes.assert_called_once_with({})


def test_none_widget_passes_filtered_attributes_to_configuration(
    manager,
    monkeypatch,
):
    widget = Mock(name="NoneWidget")
    attributes = {
        "font_size": 18,
        "background_color": (255, 0, 0),
        "draw_callback": Mock(),
    }

    monkeypatch.setattr(
        none_module,
        "NoneWidget",
        Mock(return_value=widget),
    )

    manager._filter_widget_attributes = Mock(
        return_value=attributes,
    )
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.none_widget("placeholder")

    manager._configure_widget.assert_called_once_with(
        widget=widget,
        **attributes,
    )


def test_none_widget_configures_before_appending(
    manager,
    monkeypatch,
):
    widget = Mock(name="NoneWidget")
    events = []

    monkeypatch.setattr(
        none_module,
        "NoneWidget",
        Mock(return_value=widget),
    )

    manager._filter_widget_attributes = Mock(
        side_effect=lambda attributes: (
            events.append(("filter", attributes))
            or {
                "custom_attribute": True,
            }
        )
    )

    manager._configure_widget = Mock(
        side_effect=lambda **kwargs: events.append(("configure", kwargs))
    )

    manager._append_widget = Mock(
        side_effect=lambda value: events.append(("append", value))
    )

    result = manager.none_widget("placeholder")

    assert result is widget

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


def test_none_widget_does_not_append_when_configuration_fails(
    manager,
    monkeypatch,
):
    widget = Mock(name="NoneWidget")

    monkeypatch.setattr(
        none_module,
        "NoneWidget",
        Mock(return_value=widget),
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock(
        side_effect=RuntimeError("configuration failed"),
    )
    manager._append_widget = Mock()

    with pytest.raises(
        RuntimeError,
        match="configuration failed",
    ):
        manager.none_widget("placeholder")

    manager._append_widget.assert_not_called()


def test_none_widget_does_not_append_when_filtering_fails(
    manager,
    monkeypatch,
):
    widget = Mock(name="NoneWidget")
    none_widget_factory = Mock(return_value=widget)

    monkeypatch.setattr(
        none_module,
        "NoneWidget",
        none_widget_factory,
    )

    manager._filter_widget_attributes = Mock(
        side_effect=ValueError("filtering failed"),
    )
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    with pytest.raises(
        ValueError,
        match="filtering failed",
    ):
        manager.none_widget("placeholder")

    none_widget_factory.assert_not_called()
    manager._configure_widget.assert_not_called()
    manager._append_widget.assert_not_called()


def test_none_widget_does_not_append_when_widget_creation_fails(
    manager,
    monkeypatch,
):
    monkeypatch.setattr(
        none_module,
        "NoneWidget",
        Mock(side_effect=RuntimeError("creation failed")),
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    with pytest.raises(
        RuntimeError,
        match="creation failed",
    ):
        manager.none_widget("placeholder")

    manager._configure_widget.assert_not_called()
    manager._append_widget.assert_not_called()
