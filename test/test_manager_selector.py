"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - SELECTOR
Test Selector widget.
"""

from unittest.mock import Mock

import pytest

import pygame_menu.widgets.manager.selector as selector_module
from pygame_menu.widgets.manager.selector import SelectorManager
from pygame_menu.widgets.widget.selector import SELECTOR_STYLE_CLASSIC


class DummySelectorManager(SelectorManager):
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
        return self._mock_theme

    def configure_defaults_widget(self, *args, **kwargs):
        pass


@pytest.fixture
def manager():
    instance = object.__new__(DummySelectorManager)
    instance._mock_theme = Mock(
        widget_box_arrow_color="theme-arrow-color",
        widget_box_arrow_margin="theme-arrow-margin",
        widget_box_background_color="theme-background-color",
        widget_box_border_color="theme-border-color",
        widget_box_border_width=3,
        widget_box_inflate="theme-inflate",
        widget_box_margin="theme-margin",
    )
    return instance


@pytest.fixture
def selector_factory(monkeypatch):
    widget = Mock(name="Selector")
    factory = Mock(return_value=widget)

    monkeypatch.setattr(
        selector_module,
        "Selector",
        factory,
    )

    return factory, widget


def test_selector_creates_configures_appends_and_returns_widget(
    manager,
    selector_factory,
):
    selector_factory, widget = selector_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    items = ["Easy", "Medium", "Hard"]

    result = manager.selector(
        title="Difficulty",
        items=items,
    )

    assert result is widget

    selector_factory.assert_called_once_with(
        default=0,
        items=items,
        onchange=None,
        onreturn=None,
        onselect=None,
        selector_id="",
        style=SELECTOR_STYLE_CLASSIC,
        style_fancy_arrow_color="theme-arrow-color",
        style_fancy_arrow_margin="theme-arrow-margin",
        style_fancy_bgcolor="theme-background-color",
        style_fancy_bordercolor="theme-border-color",
        style_fancy_borderwidth=3,
        style_fancy_box_inflate="theme-inflate",
        style_fancy_box_margin="theme-margin",
        title="Difficulty",
    )

    manager._configure_widget.assert_called_once_with(
        widget=widget,
    )
    manager._append_widget.assert_called_once_with(widget)


def test_selector_uses_default_arguments(
    manager,
    selector_factory,
):
    selector_factory, widget = selector_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.selector(
        "Selector",
        ["One", "Two"],
    )

    assert result is widget

    constructor_kwargs = selector_factory.call_args.kwargs

    assert constructor_kwargs["default"] == 0
    assert constructor_kwargs["onchange"] is None
    assert constructor_kwargs["onreturn"] is None
    assert constructor_kwargs["onselect"] is None
    assert constructor_kwargs["selector_id"] == ""
    assert constructor_kwargs["style"] is SELECTOR_STYLE_CLASSIC


@pytest.mark.parametrize(
    "default",
    [
        0,
        1,
        -1,
        42,
    ],
)
def test_selector_passes_default_index(
    manager,
    selector_factory,
    default,
):
    selector_factory, widget = selector_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    items = ["One", "Two", "Three"]

    result = manager.selector(
        title="Input",
        items=items,
        default=default,
    )

    assert result is widget
    assert selector_factory.call_args.kwargs["default"] == default


def test_selector_accepts_tuple_items(
    manager,
    selector_factory,
):
    selector_factory, widget = selector_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    items = [
        ("Item 1", "value-1", 10),
        ("Item 2", "value-2", 20),
    ]

    manager.selector(
        title="Items",
        items=items,
    )

    assert selector_factory.call_args.kwargs["items"] == items


def test_selector_passes_explicit_constructor_arguments(
    manager,
    selector_factory,
):
    selector_factory, widget = selector_factory

    onchange = Mock(name="onchange")
    onreturn = Mock(name="onreturn")
    onselect = Mock(name="onselect")

    items = [
        ("First", 1),
        ("Second", 2),
    ]

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.selector(
        title="Values",
        items=items,
        default=1,
        onchange=onchange,
        onreturn=onreturn,
        onselect=onselect,
        selector_id="values-selector",
        style="fancy",
    )

    selector_factory.assert_called_once_with(
        default=1,
        items=items,
        onchange=onchange,
        onreturn=onreturn,
        onselect=onselect,
        selector_id="values-selector",
        style="fancy",
        style_fancy_arrow_color="theme-arrow-color",
        style_fancy_arrow_margin="theme-arrow-margin",
        style_fancy_bgcolor="theme-background-color",
        style_fancy_bordercolor="theme-border-color",
        style_fancy_borderwidth=3,
        style_fancy_box_inflate="theme-inflate",
        style_fancy_box_margin="theme-margin",
        title="Values",
    )


def test_selector_passes_explicit_fancy_style_arguments(
    manager,
    selector_factory,
):
    selector_factory, widget = selector_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.selector(
        title="Selector",
        items=["One", "Two"],
        style_fancy_arrow_color="arrow",
        style_fancy_arrow_margin=(1, 2, 3),
        style_fancy_bgcolor="background",
        style_fancy_bordercolor="border",
        style_fancy_borderwidth=7,
        style_fancy_box_inflate=(4, 5),
        style_fancy_box_margin=(6, 7),
    )

    selector_factory.assert_called_once_with(
        default=0,
        items=["One", "Two"],
        onchange=None,
        onreturn=None,
        onselect=None,
        selector_id="",
        style=SELECTOR_STYLE_CLASSIC,
        style_fancy_arrow_color="arrow",
        style_fancy_arrow_margin=(1, 2, 3),
        style_fancy_bgcolor="background",
        style_fancy_bordercolor="border",
        style_fancy_borderwidth=7,
        style_fancy_box_inflate=(4, 5),
        style_fancy_box_margin=(6, 7),
        title="Selector",
    )


def test_selector_filters_widget_attributes_before_constructing_widget(
    manager,
    selector_factory,
):
    selector_factory, widget = selector_factory

    kwargs = {
        "font_size": 20,
        "font_color": "red",
        "padding": 8,
    }

    captured_kwargs = {}

    def filter_attributes(attributes):
        captured_kwargs.update(attributes)
        return {
            "font_size": attributes["font_size"],
            "font_color": attributes["font_color"],
        }

    manager._filter_widget_attributes = Mock(side_effect=filter_attributes)
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.selector(
        "Selector",
        ["One", "Two"],
        **kwargs,
    )

    assert captured_kwargs == kwargs

    manager._configure_widget.assert_called_once_with(
        widget=widget,
        font_size=20,
        font_color="red",
    )

    configure_kwargs = manager._configure_widget.call_args.kwargs
    assert "padding" not in configure_kwargs


def test_selector_passes_remaining_kwargs_to_constructor(
    manager,
    selector_factory,
):
    selector_factory, widget = selector_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.selector(
        "Selector",
        ["One", "Two"],
        custom_constructor_option="custom-value",
    )

    constructor_kwargs = selector_factory.call_args.kwargs

    assert constructor_kwargs["custom_constructor_option"] == "custom-value"


def test_selector_uses_theme_values_for_missing_fancy_style_arguments(
    manager,
    selector_factory,
):
    selector_factory, widget = selector_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.selector(
        "Selector",
        ["One", "Two"],
    )

    constructor_kwargs = selector_factory.call_args.kwargs

    assert constructor_kwargs["style_fancy_arrow_color"] == ("theme-arrow-color")
    assert constructor_kwargs["style_fancy_arrow_margin"] == ("theme-arrow-margin")
    assert constructor_kwargs["style_fancy_bgcolor"] == ("theme-background-color")
    assert constructor_kwargs["style_fancy_bordercolor"] == ("theme-border-color")
    assert constructor_kwargs["style_fancy_borderwidth"] == 3
    assert constructor_kwargs["style_fancy_box_inflate"] == "theme-inflate"
    assert constructor_kwargs["style_fancy_box_margin"] == "theme-margin"


def test_selector_configures_before_appending(
    manager,
    selector_factory,
):
    selector_factory, widget = selector_factory
    events = []

    manager._filter_widget_attributes = Mock(
        side_effect=lambda attributes: (
            events.append(("filter", dict(attributes))) or {"custom_attribute": True}
        )
    )

    manager._configure_widget = Mock(
        side_effect=lambda **kwargs: events.append(("configure", kwargs))
    )

    manager._append_widget = Mock(
        side_effect=lambda value: events.append(("append", value))
    )

    manager.selector(
        "Selector",
        ["One", "Two"],
    )

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


def test_selector_does_not_append_when_configuration_fails(
    manager,
    selector_factory,
):
    selector_factory, widget = selector_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock(side_effect=RuntimeError("configuration failed"))
    manager._append_widget = Mock()

    with pytest.raises(RuntimeError, match="configuration failed"):
        manager.selector(
            "Selector",
            ["One", "Two"],
        )

    manager._append_widget.assert_not_called()


def test_selector_propagates_append_failure(
    manager,
    selector_factory,
):
    selector_factory, widget = selector_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock(side_effect=RuntimeError("append failed"))

    with pytest.raises(RuntimeError, match="append failed"):
        manager.selector(
            "Selector",
            ["One", "Two"],
        )

    manager._configure_widget.assert_called_once_with(
        widget=widget,
    )
