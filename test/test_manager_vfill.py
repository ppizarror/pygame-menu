"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - VFILL
Test VFill widget.
"""

from unittest.mock import Mock

import pytest

import pygame_menu.widgets.manager.vfill as vfill_module


class TestableVFillManager(vfill_module.VFillManager):
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
    return object.__new__(TestableVFillManager)


def test_vertical_fill_creates_configures_appends_and_returns_widget(
    manager,
    monkeypatch,
):
    min_height = 24
    vfill_id = "main-fill"
    attributes = {"opacity": 128}
    widget = Mock(name="VFill")

    filter_attributes = Mock(return_value=attributes)
    configure_widget = Mock()
    append_widget = Mock()
    vfill_factory = Mock(return_value=widget)

    monkeypatch.setattr(vfill_module, "VFill", vfill_factory)

    manager._filter_widget_attributes = filter_attributes
    manager._configure_widget = configure_widget
    manager._append_widget = append_widget

    result = manager.vertical_fill(min_height, vfill_id)

    assert result is widget

    filter_attributes.assert_called_once_with({})

    vfill_factory.assert_called_once_with(
        min_height,
        widget_id=vfill_id,
    )

    configure_widget.assert_called_once_with(
        widget=widget,
        **attributes,
    )

    append_widget.assert_called_once_with(widget)


def test_vertical_fill_uses_default_arguments(
    manager,
    monkeypatch,
):
    widget = Mock(name="VFill")
    vfill_factory = Mock(return_value=widget)

    monkeypatch.setattr(vfill_module, "VFill", vfill_factory)

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.vertical_fill()

    assert result is widget

    vfill_factory.assert_called_once_with(
        0,
        widget_id="",
    )


def test_vertical_fill_uses_empty_string_as_default_id(
    manager,
    monkeypatch,
):
    widget = Mock(name="VFill")
    vfill_factory = Mock(return_value=widget)

    monkeypatch.setattr(vfill_module, "VFill", vfill_factory)

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.vertical_fill(12)

    assert result is widget

    vfill_factory.assert_called_once_with(
        12,
        widget_id="",
    )


@pytest.mark.parametrize(
    ("min_height", "vfill_id"),
    [
        (0, ""),
        (1, "one"),
        (10.5, "fractional"),
        (-5, "negative"),
        (None, "none"),
        ("20", "string-height"),
    ],
)
def test_vertical_fill_passes_arguments_unchanged(
    manager,
    monkeypatch,
    min_height,
    vfill_id,
):
    widget = Mock(name="VFill")
    vfill_factory = Mock(return_value=widget)

    monkeypatch.setattr(vfill_module, "VFill", vfill_factory)

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.vertical_fill(min_height, vfill_id)

    vfill_factory.assert_called_once_with(
        min_height,
        widget_id=vfill_id,
    )


def test_vertical_fill_filters_attributes_before_creating_widget(
    manager,
    monkeypatch,
):
    widget = Mock(name="VFill")
    events = []

    filter_attributes = Mock(
        side_effect=lambda attributes: (
            events.append(("filter", attributes)) or {"custom_attribute": True}
        )
    )

    vfill_factory = Mock(
        side_effect=lambda *args, **kwargs: (
            events.append(("create", args, kwargs)) or widget
        )
    )

    configure_widget = Mock(
        side_effect=lambda **kwargs: events.append(("configure", kwargs))
    )

    append_widget = Mock(side_effect=lambda value: events.append(("append", value)))

    monkeypatch.setattr(vfill_module, "VFill", vfill_factory)

    manager._filter_widget_attributes = filter_attributes
    manager._configure_widget = configure_widget
    manager._append_widget = append_widget

    result = manager.vertical_fill(20, "spacing")

    assert result is widget

    assert events == [
        ("filter", {}),
        (
            "create",
            (20,),
            {"widget_id": "spacing"},
        ),
        (
            "configure",
            {
                "widget": widget,
                "custom_attribute": True,
            },
        ),
        ("append", widget),
    ]


def test_vertical_fill_configures_before_appending(
    manager,
    monkeypatch,
):
    widget = Mock(name="VFill")
    events = []

    monkeypatch.setattr(
        vfill_module,
        "VFill",
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

    manager.vertical_fill(20, "spacing")

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


def test_vertical_fill_does_not_append_when_configuration_fails(
    manager,
    monkeypatch,
):
    widget = Mock(name="VFill")

    monkeypatch.setattr(
        vfill_module,
        "VFill",
        Mock(return_value=widget),
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock(side_effect=RuntimeError("configuration failed"))
    manager._append_widget = Mock()

    with pytest.raises(RuntimeError, match="configuration failed"):
        manager.vertical_fill(10)

    manager._append_widget.assert_not_called()


def test_vertical_fill_propagates_factory_errors(
    manager,
    monkeypatch,
):
    factory_error = ValueError("invalid minimum height")

    monkeypatch.setattr(
        vfill_module,
        "VFill",
        Mock(side_effect=factory_error),
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    with pytest.raises(ValueError, match="invalid minimum height"):
        manager.vertical_fill(10, "fill")

    manager._configure_widget.assert_not_called()
    manager._append_widget.assert_not_called()


def test_vertical_fill_does_not_append_when_factory_fails(
    manager,
    monkeypatch,
):
    monkeypatch.setattr(
        vfill_module,
        "VFill",
        Mock(side_effect=RuntimeError("creation failed")),
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    with pytest.raises(RuntimeError, match="creation failed"):
        manager.vertical_fill(10)

    manager._configure_widget.assert_not_called()
    manager._append_widget.assert_not_called()


def test_vertical_fill_passes_filtered_attributes_to_configuration(
    manager,
    monkeypatch,
):
    widget = Mock(name="VFill")
    attributes = {
        "font_size": 18,
        "readonly": True,
        "custom_value": "example",
    }

    monkeypatch.setattr(
        vfill_module,
        "VFill",
        Mock(return_value=widget),
    )

    manager._filter_widget_attributes = Mock(return_value=attributes)
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.vertical_fill(32, "content-fill")

    manager._configure_widget.assert_called_once_with(
        widget=widget,
        font_size=18,
        readonly=True,
        custom_value="example",
    )


def test_vertical_fill_returns_exact_widget_instance(
    manager,
    monkeypatch,
):
    widget = object()

    monkeypatch.setattr(
        vfill_module,
        "VFill",
        Mock(return_value=widget),
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.vertical_fill()

    assert result is widget
