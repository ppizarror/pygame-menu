"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST MANAGER - HMARGIN
Test HMargin widget.
"""

from unittest.mock import Mock

import pytest

import pygame_menu.widgets.manager.hmargin as hmargin_module
from pygame_menu.widgets.manager.hmargin import HMarginManager


class TestableHMarginManager(HMarginManager):
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
    return object.__new__(TestableHMarginManager)


def test_horizontal_margin_creates_configures_appends_and_returns_widget(
    manager,
    monkeypatch,
):
    margin = 24
    margin_id = "main-spacing"
    attributes = {"font_size": 18}
    widget = Mock(name="HMargin")

    filter_attributes = Mock(return_value=attributes)
    configure_widget = Mock()
    append_widget = Mock()
    hmargin_factory = Mock(return_value=widget)

    monkeypatch.setattr(
        hmargin_module,
        "HMargin",
        hmargin_factory,
    )

    manager._filter_widget_attributes = filter_attributes
    manager._configure_widget = configure_widget
    manager._append_widget = append_widget

    result = manager.horizontal_margin(margin, margin_id)

    assert result is widget

    filter_attributes.assert_called_once_with({})

    hmargin_factory.assert_called_once_with(
        margin,
        widget_id=margin_id,
    )

    configure_widget.assert_called_once_with(
        widget=widget,
        **attributes,
    )

    append_widget.assert_called_once_with(widget)


def test_horizontal_margin_uses_empty_string_as_default_id(
    manager,
    monkeypatch,
):
    widget = Mock(name="HMargin")
    hmargin_factory = Mock(return_value=widget)

    monkeypatch.setattr(
        hmargin_module,
        "HMargin",
        hmargin_factory,
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.horizontal_margin(12)

    assert result is widget

    hmargin_factory.assert_called_once_with(
        12,
        widget_id="",
    )


@pytest.mark.parametrize(
    ("margin", "margin_id"),
    [
        (0, ""),
        (1, "one"),
        (10.5, "fractional"),
        (-5, "negative"),
        (None, None),
        ("24", "string-margin"),
    ],
)
def test_horizontal_margin_passes_arguments_unchanged(
    manager,
    monkeypatch,
    margin,
    margin_id,
):
    widget = Mock(name="HMargin")
    hmargin_factory = Mock(return_value=widget)

    monkeypatch.setattr(
        hmargin_module,
        "HMargin",
        hmargin_factory,
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.horizontal_margin(margin, margin_id)

    assert result is widget

    hmargin_factory.assert_called_once_with(
        margin,
        widget_id=margin_id,
    )


def test_horizontal_margin_filters_empty_attribute_dictionary(
    manager,
    monkeypatch,
):
    widget = Mock(name="HMargin")
    hmargin_factory = Mock(return_value=widget)
    filter_attributes = Mock(return_value={})

    monkeypatch.setattr(
        hmargin_module,
        "HMargin",
        hmargin_factory,
    )

    manager._filter_widget_attributes = filter_attributes
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.horizontal_margin(20, "spacing")

    filter_attributes.assert_called_once_with({})


def test_horizontal_margin_configures_before_appending(
    manager,
    monkeypatch,
):
    widget = Mock(name="HMargin")
    events = []

    monkeypatch.setattr(
        hmargin_module,
        "HMargin",
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

    result = manager.horizontal_margin(20, "spacing")

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


def test_horizontal_margin_does_not_append_when_filtering_fails(
    manager,
    monkeypatch,
):
    widget = Mock(name="HMargin")
    hmargin_factory = Mock(return_value=widget)

    monkeypatch.setattr(
        hmargin_module,
        "HMargin",
        hmargin_factory,
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
        manager.horizontal_margin(10)

    hmargin_factory.assert_not_called()
    manager._configure_widget.assert_not_called()
    manager._append_widget.assert_not_called()


def test_horizontal_margin_does_not_append_when_widget_creation_fails(
    manager,
    monkeypatch,
):
    hmargin_factory = Mock(
        side_effect=RuntimeError("creation failed"),
    )

    monkeypatch.setattr(
        hmargin_module,
        "HMargin",
        hmargin_factory,
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    with pytest.raises(
        RuntimeError,
        match="creation failed",
    ):
        manager.horizontal_margin(10)

    manager._configure_widget.assert_not_called()
    manager._append_widget.assert_not_called()


def test_horizontal_margin_does_not_append_when_configuration_fails(
    manager,
    monkeypatch,
):
    widget = Mock(name="HMargin")

    monkeypatch.setattr(
        hmargin_module,
        "HMargin",
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
        manager.horizontal_margin(10)

    manager._append_widget.assert_not_called()


def test_horizontal_margin_propagates_append_errors(
    manager,
    monkeypatch,
):
    widget = Mock(name="HMargin")

    monkeypatch.setattr(
        hmargin_module,
        "HMargin",
        Mock(return_value=widget),
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock(
        side_effect=RuntimeError("append failed"),
    )

    with pytest.raises(
        RuntimeError,
        match="append failed",
    ):
        manager.horizontal_margin(10)

    manager._configure_widget.assert_called_once_with(
        widget=widget,
    )
