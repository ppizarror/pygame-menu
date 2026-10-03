"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - COLORINPUT
Test ColorInput widget.
"""

from unittest.mock import Mock

import pytest

import pygame_menu.widgets.manager.colorinput as colorinput_module


class DummyColorInputManager(colorinput_module.ColorInputManager):
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
    instance = object.__new__(DummyColorInputManager)
    instance._mock_theme = Mock(
        cursor_color="cursor-color",
        cursor_switch_ms=250,
    )
    return instance


@pytest.fixture
def color_input_factory(monkeypatch):
    widget = Mock(name="ColorInput")
    factory = Mock(return_value=widget)

    monkeypatch.setattr(
        colorinput_module,
        "ColorInput",
        factory,
    )

    return factory, widget


def test_color_input_creates_configures_appends_sets_default_and_returns_widget(
    manager,
    color_input_factory,
):
    color_input_factory, widget = color_input_factory

    title = "Favorite color"
    color_type = "rgb"
    color_id = "favorite-color"
    default = (12, 34, 56)

    attributes = {
        "font_size": 18,
        "font_color": "white",
    }

    filter_attributes = Mock(return_value=attributes)
    configure_widget = Mock()
    append_widget = Mock()

    manager._filter_widget_attributes = filter_attributes
    manager._configure_widget = configure_widget
    manager._append_widget = append_widget

    result = manager.color_input(
        title,
        color_type,
        color_id=color_id,
        default=default,
    )

    assert result is widget

    filter_attributes.assert_called_once_with({})

    color_input_factory.assert_called_once_with(
        color_type=color_type,
        colorinput_id=color_id,
        cursor_color="cursor-color",
        cursor_switch_ms=250,
        dynamic_width=True,
        hex_format=colorinput_module.COLORINPUT_HEX_FORMAT_NONE,
        input_separator=",",
        input_underline="_",
        input_underline_vmargin=0,
        onchange=None,
        onreturn=None,
        onselect=None,
        prev_margin=10,
        prev_width_factor=3,
        title=title,
    )

    configure_widget.assert_called_once_with(
        widget=widget,
        **attributes,
    )
    append_widget.assert_called_once_with(widget)
    widget.set_default_value.assert_called_once_with(default)


def test_color_input_uses_default_color_id_and_default_values(
    manager,
    color_input_factory,
):
    color_input_factory, widget = color_input_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.color_input(
        "Color",
        "hex",
    )

    assert result is widget

    color_input_factory.assert_called_once_with(
        color_type="hex",
        colorinput_id="",
        cursor_color="cursor-color",
        cursor_switch_ms=250,
        dynamic_width=True,
        hex_format=colorinput_module.COLORINPUT_HEX_FORMAT_NONE,
        input_separator=",",
        input_underline="_",
        input_underline_vmargin=0,
        onchange=None,
        onreturn=None,
        onselect=None,
        prev_margin=10,
        prev_width_factor=3,
        title="Color",
    )

    widget.set_default_value.assert_called_once_with("")


@pytest.mark.parametrize(
    (
        "dynamic_width",
        "input_underline_vmargin",
        "previsualization_margin",
        "previsualization_width",
    ),
    [
        (False, 4, 8, 5),
        (True, 0, 0, 3),
        (False, 12, 20, 1.5),
    ],
)
def test_color_input_passes_optional_constructor_arguments_unchanged(
    manager,
    color_input_factory,
    dynamic_width,
    input_underline_vmargin,
    previsualization_margin,
    previsualization_width,
):
    color_input_factory, widget = color_input_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.color_input(
        "Color",
        "rgb",
        dynamic_width=dynamic_width,
        input_underline_vmargin=input_underline_vmargin,
        previsualization_margin=previsualization_margin,
        previsualization_width=previsualization_width,
    )

    color_input_factory.assert_called_once_with(
        color_type="rgb",
        colorinput_id="",
        cursor_color="cursor-color",
        cursor_switch_ms=250,
        dynamic_width=dynamic_width,
        hex_format=colorinput_module.COLORINPUT_HEX_FORMAT_NONE,
        input_separator=",",
        input_underline="_",
        input_underline_vmargin=input_underline_vmargin,
        onchange=None,
        onreturn=None,
        onselect=None,
        prev_margin=previsualization_margin,
        prev_width_factor=previsualization_width,
        title="Color",
    )


def test_color_input_passes_explicit_input_and_callback_arguments(
    manager,
    color_input_factory,
):
    color_input_factory, widget = color_input_factory

    onchange = Mock(name="onchange")
    onreturn = Mock(name="onreturn")
    onselect = Mock(name="onselect")

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.color_input(
        title="Color",
        color_type="rgb",
        color_id="rgb-input",
        default=(255, 0, 10),
        hex_format="short",
        input_separator=";",
        input_underline="-",
        onchange=onchange,
        onreturn=onreturn,
        onselect=onselect,
    )

    color_input_factory.assert_called_once_with(
        color_type="rgb",
        colorinput_id="rgb-input",
        cursor_color="cursor-color",
        cursor_switch_ms=250,
        dynamic_width=True,
        hex_format="short",
        input_separator=";",
        input_underline="-",
        input_underline_vmargin=0,
        onchange=onchange,
        onreturn=onreturn,
        onselect=onselect,
        prev_margin=10,
        prev_width_factor=3,
        title="Color",
    )

    widget.set_default_value.assert_called_once_with((255, 0, 10))


def test_color_input_filters_widget_attributes_before_constructing_widget(
    manager,
    color_input_factory,
):
    color_input_factory, widget = color_input_factory

    kwargs = {
        "font_size": 20,
        "font_color": "red",
        "dynamic_width": False,
        "previsualization_margin": 6,
    }

    filtered_attributes = {
        "font_size": 20,
        "font_color": "red",
    }

    filtered_kwargs_at_call_time = {}

    def filter_attributes(attributes):
        filtered_kwargs_at_call_time.update(attributes)
        return filtered_attributes

    manager._filter_widget_attributes = Mock(side_effect=filter_attributes)
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.color_input(
        "Color",
        "rgb",
        **kwargs,
    )

    assert filtered_kwargs_at_call_time == {
        "font_size": 20,
        "font_color": "red",
        "dynamic_width": False,
        "previsualization_margin": 6,
    }

    manager._configure_widget.assert_called_once_with(
        widget=widget,
        **filtered_attributes,
    )

    configure_kwargs = manager._configure_widget.call_args.kwargs

    assert "dynamic_width" not in configure_kwargs
    assert "previsualization_margin" not in configure_kwargs
    assert "previsualization_width" not in configure_kwargs
    assert "input_underline_vmargin" not in configure_kwargs


def test_color_input_passes_remaining_kwargs_to_color_input(
    manager,
    color_input_factory,
):
    color_input_factory, widget = color_input_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.color_input(
        "Color",
        "rgb",
        custom_constructor_option="custom-value",
    )

    constructor_kwargs = color_input_factory.call_args.kwargs

    assert constructor_kwargs["custom_constructor_option"] == "custom-value"


def test_color_input_configures_before_appending_and_sets_default_last(
    manager,
    color_input_factory,
):
    color_input_factory, widget = color_input_factory
    events = []

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

    widget.set_default_value.side_effect = lambda value: events.append(
        ("set_default_value", value)
    )

    manager.color_input(
        "Color",
        "rgb",
        default=(1, 2, 3),
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
        ("set_default_value", (1, 2, 3)),
    ]


def test_color_input_does_not_append_when_configuration_fails(
    manager,
    color_input_factory,
):
    color_input_factory, widget = color_input_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock(side_effect=RuntimeError("configuration failed"))
    manager._append_widget = Mock()

    with pytest.raises(RuntimeError, match="configuration failed"):
        manager.color_input(
            "Color",
            "rgb",
            default=(1, 2, 3),
        )

    manager._append_widget.assert_not_called()
    widget.set_default_value.assert_not_called()


def test_color_input_does_not_set_default_when_append_fails(
    manager,
    color_input_factory,
):
    color_input_factory, widget = color_input_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock(side_effect=RuntimeError("append failed"))

    with pytest.raises(RuntimeError, match="append failed"):
        manager.color_input(
            "Color",
            "rgb",
            default="#abcdef",
        )

    widget.set_default_value.assert_not_called()


@pytest.mark.parametrize(
    "default",
    [
        "",
        "#abcdef",
        (0, 0, 0),
        (255, 128, 1),
        tuple(range(3)),
    ],
)
def test_color_input_accepts_string_and_tuple_defaults(
    manager,
    color_input_factory,
    default,
):
    color_input_factory, widget = color_input_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.color_input(
        "Color",
        "rgb",
        default=default,
    )

    assert result is widget
    widget.set_default_value.assert_called_once_with(default)


@pytest.mark.parametrize(
    "invalid_default",
    [
        None,
        123,
        1.5,
        ["red", "green", "blue"],
        {"r": 255, "g": 0, "b": 0},
    ],
)
def test_color_input_rejects_non_string_and_non_tuple_defaults(
    manager,
    color_input_factory,
    invalid_default,
):
    color_input_factory, widget = color_input_factory

    manager._filter_widget_attributes = Mock()
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    with pytest.raises(AssertionError):
        manager.color_input(
            "Color",
            "rgb",
            default=invalid_default,
        )

    color_input_factory.assert_not_called()
    manager._filter_widget_attributes.assert_not_called()
    manager._configure_widget.assert_not_called()
    manager._append_widget.assert_not_called()
