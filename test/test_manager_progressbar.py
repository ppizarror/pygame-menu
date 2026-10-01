"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - PROGRESSBAR
Test ProgressBar widget.
"""

from unittest.mock import Mock

import pytest

import pygame_menu.widgets.manager.progressbar as progressbar_module
from pygame_menu.locals import (
    ORIENTATION_HORIZONTAL,
    ORIENTATION_VERTICAL,
)


class DummyProgressBarManager(progressbar_module.ProgressBarManager):
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
    instance = object.__new__(DummyProgressBarManager)
    instance._mock_theme = Mock(
        widget_box_background_color="theme-background-color",
        widget_box_border_color="theme-border-color",
        widget_box_border_width=3,
        widget_box_margin="theme-margin",
        widget_font_color="theme-font-color",
    )
    return instance


@pytest.fixture
def progress_bar_factory(monkeypatch):
    widget = Mock(name="ProgressBar")
    factory = Mock(return_value=widget)

    monkeypatch.setattr(
        progressbar_module,
        "ProgressBar",
        factory,
    )

    return factory, widget


def test_progress_bar_creates_configures_appends_and_returns_widget(
    manager,
    progress_bar_factory,
):
    progress_bar_factory, widget = progress_bar_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.progress_bar(title="Loading")

    assert result is widget

    constructor_kwargs = progress_bar_factory.call_args.kwargs

    assert constructor_kwargs == {
        "title": "Loading",
        "progressbar_id": "",
        "default": 0,
        "min_value": 0,
        "max_value": 100,
        "width": 150,
        "height": 20,
        "orientation": ORIENTATION_HORIZONTAL,
        "onselect": None,
        "box_background_color": "theme-background-color",
        "box_border_color": "theme-border-color",
        "box_border_width": 3,
        "box_margin": "theme-margin",
        "box_progress_color": (53, 172, 78),
        "progress_text_font_color": "theme-font-color",
        "progress_text_format": constructor_kwargs["progress_text_format"],
    }

    assert callable(constructor_kwargs["progress_text_format"])
    assert widget.is_selectable is False

    manager._configure_widget.assert_called_once_with(
        widget=widget,
    )
    manager._append_widget.assert_called_once_with(widget)


def test_progress_bar_uses_default_arguments(
    manager,
    progress_bar_factory,
):
    progress_bar_factory, widget = progress_bar_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.progress_bar("Progress")

    assert result is widget

    constructor_kwargs = progress_bar_factory.call_args.kwargs

    assert constructor_kwargs["default"] == 0
    assert constructor_kwargs["min_value"] == 0
    assert constructor_kwargs["max_value"] == 100
    assert constructor_kwargs["height"] == 20
    assert constructor_kwargs["width"] == 150
    assert constructor_kwargs["orientation"] == ORIENTATION_HORIZONTAL
    assert constructor_kwargs["progressbar_id"] == ""
    assert constructor_kwargs["onselect"] is None
    assert widget.is_selectable is False


@pytest.mark.parametrize(
    "orientation",
    [
        ORIENTATION_HORIZONTAL,
        ORIENTATION_VERTICAL,
    ],
)
def test_progress_bar_accepts_valid_orientations(
    manager,
    progress_bar_factory,
    orientation,
):
    progress_bar_factory, widget = progress_bar_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.progress_bar(
        title="Progress",
        orientation=orientation,
    )

    assert progress_bar_factory.call_args.kwargs["orientation"] == orientation


def test_progress_bar_passes_explicit_constructor_arguments(
    manager,
    progress_bar_factory,
):
    progress_bar_factory, widget = progress_bar_factory

    onselect = Mock(name="onselect")
    progress_text_format = Mock(name="progress_text_format")

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.progress_bar(
        title="Download",
        default=25,
        min_value=10,
        max_value=200,
        height=30,
        orientation=ORIENTATION_VERTICAL,
        onselect=onselect,
        progressbar_id="download-progress",
        progress_text_format=progress_text_format,
        selectable=True,
        width=300,
    )

    progress_bar_factory.assert_called_once_with(
        title="Download",
        progressbar_id="download-progress",
        default=25,
        min_value=10,
        max_value=200,
        width=300,
        height=30,
        orientation=ORIENTATION_VERTICAL,
        onselect=onselect,
        box_background_color="theme-background-color",
        box_border_color="theme-border-color",
        box_border_width=3,
        box_margin="theme-margin",
        box_progress_color=(53, 172, 78),
        progress_text_font_color="theme-font-color",
        progress_text_format=progress_text_format,
    )

    assert widget.is_selectable is True


@pytest.mark.parametrize("selectable", [True, False])
def test_progress_bar_sets_selectable_after_construction(
    manager,
    progress_bar_factory,
    selectable,
):
    progress_bar_factory, widget = progress_bar_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.progress_bar(
        title="Progress",
        selectable=selectable,
    )

    assert widget.is_selectable is selectable
    assert progress_bar_factory.called


def test_progress_bar_rejects_non_boolean_selectable(
    manager,
    progress_bar_factory,
):
    progress_bar_factory, widget = progress_bar_factory

    manager._filter_widget_attributes = Mock()
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    with pytest.raises(AssertionError):
        manager.progress_bar(
            title="Progress",
            selectable=1,
        )

    progress_bar_factory.assert_not_called()
    manager._filter_widget_attributes.assert_not_called()
    manager._configure_widget.assert_not_called()
    manager._append_widget.assert_not_called()


@pytest.mark.parametrize(
    "orientation",
    [
        "invalid",
        None,
        1,
        "",
    ],
)
def test_progress_bar_rejects_invalid_orientation(
    manager,
    progress_bar_factory,
    orientation,
):
    progress_bar_factory, widget = progress_bar_factory

    manager._filter_widget_attributes = Mock()
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    with pytest.raises(
        AssertionError,
        match=("orientation must be ORIENTATION_HORIZONTAL or ORIENTATION_VERTICAL"),
    ):
        manager.progress_bar(
            title="Progress",
            orientation=orientation,
        )

    progress_bar_factory.assert_not_called()
    manager._filter_widget_attributes.assert_not_called()
    manager._configure_widget.assert_not_called()
    manager._append_widget.assert_not_called()


def test_progress_bar_passes_explicit_box_arguments(
    manager,
    progress_bar_factory,
):
    progress_bar_factory, widget = progress_bar_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.progress_bar(
        title="Progress",
        box_background_color="background",
        box_border_color="border",
        box_border_width=8,
        box_margin=(5, 6),
        box_progress_color="progress",
        progress_text_font_color="font",
    )

    constructor_kwargs = progress_bar_factory.call_args.kwargs

    assert constructor_kwargs["box_background_color"] == "background"
    assert constructor_kwargs["box_border_color"] == "border"
    assert constructor_kwargs["box_border_width"] == 8
    assert constructor_kwargs["box_margin"] == (5, 6)
    assert constructor_kwargs["box_progress_color"] == "progress"
    assert constructor_kwargs["progress_text_font_color"] == "font"


def test_progress_bar_filters_widget_attributes_before_construction(
    manager,
    progress_bar_factory,
):
    progress_bar_factory, widget = progress_bar_factory

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

    manager.progress_bar(
        "Progress",
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


def test_progress_bar_passes_remaining_kwargs_to_constructor(
    manager,
    progress_bar_factory,
):
    progress_bar_factory, widget = progress_bar_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.progress_bar(
        "Progress",
        custom_constructor_option="custom-value",
    )

    constructor_kwargs = progress_bar_factory.call_args.kwargs

    assert constructor_kwargs["custom_constructor_option"] == ("custom-value")


def test_progress_bar_uses_theme_values_for_missing_box_arguments(
    manager,
    progress_bar_factory,
):
    progress_bar_factory, widget = progress_bar_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.progress_bar("Progress")

    constructor_kwargs = progress_bar_factory.call_args.kwargs

    assert constructor_kwargs["box_background_color"] == ("theme-background-color")
    assert constructor_kwargs["box_border_color"] == "theme-border-color"
    assert constructor_kwargs["box_border_width"] == 3
    assert constructor_kwargs["box_margin"] == "theme-margin"
    assert constructor_kwargs["box_progress_color"] == (53, 172, 78)
    assert constructor_kwargs["progress_text_font_color"] == ("theme-font-color")


def test_progress_bar_configures_before_appending(
    manager,
    progress_bar_factory,
):
    progress_bar_factory, widget = progress_bar_factory
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

    manager.progress_bar(
        "Progress",
        default=50,
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


def test_progress_bar_does_not_append_when_configuration_fails(
    manager,
    progress_bar_factory,
):
    progress_bar_factory, widget = progress_bar_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock(side_effect=RuntimeError("configuration failed"))
    manager._append_widget = Mock()

    with pytest.raises(RuntimeError, match="configuration failed"):
        manager.progress_bar(
            "Progress",
            default=50,
        )

    manager._append_widget.assert_not_called()


def test_progress_bar_propagates_append_failure(
    manager,
    progress_bar_factory,
):
    progress_bar_factory, widget = progress_bar_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock(side_effect=RuntimeError("append failed"))

    with pytest.raises(RuntimeError, match="append failed"):
        manager.progress_bar(
            "Progress",
            default=50,
        )

    manager._configure_widget.assert_called_once_with(
        widget=widget,
    )
