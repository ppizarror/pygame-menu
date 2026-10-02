"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - TOGGLESWITCH
Test ToggleSwitch widget.
"""

from unittest.mock import Mock

import pytest

import pygame_menu.widgets.manager.toggleswitch as toggleswitch_module


class DummyToggleSwitchManager(toggleswitch_module.ToggleSwitchManager):
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
        return self.theme

    def configure_defaults_widget(self, *args, **kwargs):
        pass


@pytest.fixture
def theme():
    return Mock(
        widget_box_background_color="theme-background",
        scrollbar_thick=11,
        widget_box_border_color="theme-border",
        widget_box_border_width=3,
        widget_box_margin=(4, 5),
    )


@pytest.fixture
def manager(theme):
    manager = object.__new__(DummyToggleSwitchManager)
    manager.theme = theme
    return manager


@pytest.fixture
def toggle_switch_setup(manager, monkeypatch):
    widget = Mock(name="ToggleSwitch")
    factory = Mock(return_value=widget)

    monkeypatch.setattr(
        toggleswitch_module,
        "ToggleSwitch",
        factory,
    )

    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    return widget, factory


def test_toggle_switch_creates_configures_appends_and_returns_widget(
    manager,
    toggle_switch_setup,
):
    widget, factory = toggle_switch_setup

    attributes = {
        "font_size": 18,
        "align": "left",
    }
    manager._filter_widget_attributes = Mock(return_value=attributes)

    onchange = Mock(name="onchange")
    onselect = Mock(name="onselect")

    result = manager.toggle_switch(
        "Enable feature",
        default=1,
        onchange=onchange,
        onselect=onselect,
        toggleswitch_id="feature-toggle",
        single_click=False,
        state_text=("Disabled", "Enabled"),
        state_values=("off", "on"),
        width=220,
        infinite=True,
        slider_color="blue",
        slider_thickness=7,
        state_color=("gray", "green"),
        state_text_font_color=("white", "black"),
        state_text_font_size=16,
        switch_border_color="red",
        switch_border_width=2,
        switch_height=1.5,
        switch_margin=(8, 9),
        single_click_dir=False,
        **attributes,
    )

    assert result is widget

    factory.assert_called_once_with(
        default_state=1,
        infinite=True,
        onchange=onchange,
        onselect=onselect,
        single_click=False,
        single_click_dir=False,
        slider_color="blue",
        slider_thickness=7,
        state_color=("gray", "green"),
        state_text=("Disabled", "Enabled"),
        state_text_font_color=("white", "black"),
        state_text_font_size=16,
        state_values=("off", "on"),
        switch_border_color="red",
        switch_border_width=2,
        switch_height=1.5,
        switch_margin=(8, 9),
        title="Enable feature",
        state_width=220,
        toggleswitch_id="feature-toggle",
        font_size=18,
        align="left",
    )

    manager._configure_widget.assert_called_once_with(
        widget=widget,
        **attributes,
    )
    manager._append_widget.assert_called_once_with(widget)


def test_toggle_switch_uses_all_documented_defaults(
    manager,
    toggle_switch_setup,
):
    widget, factory = toggle_switch_setup
    manager._filter_widget_attributes = Mock(return_value={})

    result = manager.toggle_switch("Default toggle")

    assert result is widget

    factory.assert_called_once_with(
        default_state=0,
        infinite=False,
        onchange=None,
        onselect=None,
        single_click=True,
        single_click_dir=True,
        slider_color="theme-background",
        slider_thickness=11,
        state_color=((178, 178, 178), (117, 185, 54)),
        state_text=("Off", "On"),
        state_text_font_color=(
            "theme-background",
            "theme-background",
        ),
        state_text_font_size=None,
        state_values=(False, True),
        switch_border_color="theme-border",
        switch_border_width=3,
        switch_height=1,
        switch_margin=(4, 5),
        title="Default toggle",
        state_width=150,
        toggleswitch_id="",
    )


@pytest.mark.parametrize("default", [0, 1, False, True])
def test_toggle_switch_accepts_valid_default_values(
    manager,
    toggle_switch_setup,
    default,
):
    _, factory = toggle_switch_setup
    manager._filter_widget_attributes = Mock(return_value={})

    manager.toggle_switch("Toggle", default=default)

    assert factory.call_args.kwargs["default_state"] == default


@pytest.mark.parametrize("default", [-1, 2, 3])
def test_toggle_switch_rejects_out_of_range_default_values(
    manager,
    toggle_switch_setup,
    default,
):
    _, factory = toggle_switch_setup
    manager._filter_widget_attributes = Mock(return_value={})

    with pytest.raises(
        AssertionError,
        match="default value can be 0 or 1",
    ):
        manager.toggle_switch("Toggle", default=default)

    factory.assert_not_called()
    manager._configure_widget.assert_not_called()
    manager._append_widget.assert_not_called()


@pytest.mark.parametrize(
    "default",
    [
        0.5,
        1.0,
        None,
        "0",
        "1",
        [],
        {},
        object(),
    ],
)
def test_toggle_switch_rejects_invalid_default_types(
    manager,
    toggle_switch_setup,
    default,
):
    _, factory = toggle_switch_setup
    manager._filter_widget_attributes = Mock(return_value={})

    with pytest.raises(ValueError, match="invalid value type"):
        manager.toggle_switch("Toggle", default=default)

    factory.assert_not_called()
    manager._configure_widget.assert_not_called()
    manager._append_widget.assert_not_called()


def test_toggle_switch_converts_width_to_integer(
    manager,
    toggle_switch_setup,
):
    _, factory = toggle_switch_setup
    manager._filter_widget_attributes = Mock(return_value={})

    manager.toggle_switch("Toggle", width=125.75)

    assert factory.call_args.kwargs["state_width"] == 125


def test_toggle_switch_preserves_callback_arguments(
    manager,
    toggle_switch_setup,
):
    _, factory = toggle_switch_setup
    manager._filter_widget_attributes = Mock(return_value={})

    onchange = Mock(name="onchange")
    onselect = Mock(name="onselect")

    manager.toggle_switch(
        "Callback toggle",
        onchange=onchange,
        onselect=onselect,
    )

    factory_kwargs = factory.call_args.kwargs

    assert factory_kwargs["onchange"] is onchange
    assert factory_kwargs["onselect"] is onselect


def test_toggle_switch_passes_custom_attributes_to_configuration(
    manager,
    toggle_switch_setup,
):
    widget, _ = toggle_switch_setup

    attributes = {
        "font_size": 24,
        "font_color": "white",
        "padding": (1, 2, 3, 4),
    }
    manager._filter_widget_attributes = Mock(return_value=attributes)

    manager.toggle_switch("Styled toggle")

    manager._configure_widget.assert_called_once_with(
        widget=widget,
        **attributes,
    )


def test_toggle_switch_forwards_unrecognized_kwargs(
    manager,
    toggle_switch_setup,
):
    _, factory = toggle_switch_setup
    manager._filter_widget_attributes = Mock(return_value={})

    manager.toggle_switch(
        "Toggle",
        custom_option="custom-value",
        another_option=42,
    )

    factory_kwargs = factory.call_args.kwargs

    assert factory_kwargs["custom_option"] == "custom-value"
    assert factory_kwargs["another_option"] == 42


def test_toggle_switch_configures_before_appending(
    manager,
    toggle_switch_setup,
):
    widget, _ = toggle_switch_setup
    events = []

    manager._filter_widget_attributes = Mock(return_value={})

    manager._configure_widget.side_effect = lambda **kwargs: events.append(
        ("configure", kwargs)
    )
    manager._append_widget.side_effect = lambda value: events.append(("append", value))

    manager.toggle_switch("Toggle")

    assert events == [
        ("configure", {"widget": widget}),
        ("append", widget),
    ]


def test_toggle_switch_does_not_append_when_configuration_fails(
    manager,
    toggle_switch_setup,
):
    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget.side_effect = RuntimeError("configuration failed")

    with pytest.raises(RuntimeError, match="configuration failed"):
        manager.toggle_switch("Toggle")

    manager._append_widget.assert_not_called()


def test_toggle_switch_propagates_factory_errors(
    manager,
    monkeypatch,
):
    factory = Mock(side_effect=ValueError("widget creation failed"))
    monkeypatch.setattr(
        toggleswitch_module,
        "ToggleSwitch",
        factory,
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    with pytest.raises(ValueError, match="widget creation failed"):
        manager.toggle_switch("Toggle")

    manager._configure_widget.assert_not_called()
    manager._append_widget.assert_not_called()


def test_toggle_switch_uses_explicit_values_over_theme_defaults(
    manager,
    toggle_switch_setup,
):
    _, factory = toggle_switch_setup
    manager._filter_widget_attributes = Mock(return_value={})

    manager.toggle_switch(
        "Toggle",
        slider_color="custom-slider",
        slider_thickness=99,
        switch_border_color="custom-border",
        switch_border_width=8,
        switch_margin=(20, 21),
    )

    factory_kwargs = factory.call_args.kwargs

    assert factory_kwargs["slider_color"] == "custom-slider"
    assert factory_kwargs["slider_thickness"] == 99
    assert factory_kwargs["switch_border_color"] == "custom-border"
    assert factory_kwargs["switch_border_width"] == 8
    assert factory_kwargs["switch_margin"] == (20, 21)


def test_toggle_switch_returns_exact_widget_instance(
    manager,
    toggle_switch_setup,
):
    widget, _ = toggle_switch_setup
    manager._filter_widget_attributes = Mock(return_value={})

    result = manager.toggle_switch("Toggle")

    assert result is widget
