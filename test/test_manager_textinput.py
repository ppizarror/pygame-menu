"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - TEXTINPUT
Test TextInput widget.
"""

from unittest.mock import Mock

import pytest

import pygame_menu.widgets.manager.textinput as textinput_module
from pygame_menu.locals import INPUT_TEXT


class DummyTextInputManager(textinput_module.TextInputManager):
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
    instance = object.__new__(DummyTextInputManager)
    instance._mock_theme = Mock(
        cursor_color="cursor-color",
        cursor_selection_color="selection-color",
        cursor_switch_ms=250,
    )
    return instance


@pytest.fixture
def text_input_factory(monkeypatch):
    widget = Mock(name="TextInput")
    factory = Mock(return_value=widget)

    monkeypatch.setattr(
        textinput_module,
        "TextInput",
        factory,
    )

    return factory, widget


def test_text_input_creates_configures_appends_sets_default_and_returns_widget(
    manager,
    text_input_factory,
):
    text_input_factory, widget = text_input_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.text_input(
        title="Username",
        default="alice",
    )

    assert result is widget

    text_input_factory.assert_called_once_with(
        copy_paste_enable=True,
        cursor_color="cursor-color",
        cursor_selection_color="selection-color",
        cursor_selection_enable=True,
        cursor_size=None,
        cursor_switch_ms=250,
        input_type=INPUT_TEXT,
        input_underline="",
        input_underline_len=0,
        input_underline_vmargin=0,
        maxchar=0,
        maxwidth=0,
        onchange=None,
        onreturn=None,
        onselect=None,
        password=False,
        textinput_id="",
        title="Username",
        valid_chars=None,
    )

    manager._configure_widget.assert_called_once_with(
        widget=widget,
    )
    manager._append_widget.assert_called_once_with(widget)
    widget.set_default_value.assert_called_once_with("alice")


def test_text_input_uses_default_arguments(
    manager,
    text_input_factory,
):
    text_input_factory, widget = text_input_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.text_input("Input")

    assert result is widget
    widget.set_default_value.assert_called_once_with("")


@pytest.mark.parametrize(
    "default",
    [
        "",
        "hello",
        0,
        42,
        -10,
        3.14,
    ],
)
def test_text_input_accepts_string_and_numeric_defaults(
    manager,
    text_input_factory,
    default,
):
    text_input_factory, widget = text_input_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.text_input(
        title="Input",
        default=default,
    )

    assert result is widget
    widget.set_default_value.assert_called_once_with(default)


@pytest.mark.parametrize(
    "default",
    [
        None,
        [],
        {},
        ("a", "b"),
        object(),
    ],
)
def test_text_input_rejects_invalid_default_types(
    manager,
    text_input_factory,
    default,
):
    text_input_factory, widget = text_input_factory

    manager._filter_widget_attributes = Mock()
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    with pytest.raises(AssertionError):
        manager.text_input(
            title="Input",
            default=default,
        )

    text_input_factory.assert_not_called()
    manager._filter_widget_attributes.assert_not_called()
    manager._configure_widget.assert_not_called()
    manager._append_widget.assert_not_called()


def test_text_input_passes_explicit_constructor_arguments(
    manager,
    text_input_factory,
):
    text_input_factory, widget = text_input_factory

    onchange = Mock(name="onchange")
    onreturn = Mock(name="onreturn")
    onselect = Mock(name="onselect")

    cursor_size = (2, 24)
    valid_chars = ["a", "b", "c"]

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.text_input(
        title="Code",
        default=123,
        copy_paste_enable=False,
        cursor_selection_enable=False,
        cursor_size=cursor_size,
        input_type="numeric",
        input_underline="-",
        input_underline_len=10,
        maxchar=6,
        maxwidth=20,
        onchange=onchange,
        onreturn=onreturn,
        onselect=onselect,
        password=False,
        textinput_id="code-input",
        valid_chars=valid_chars,
    )

    text_input_factory.assert_called_once_with(
        copy_paste_enable=False,
        cursor_color="cursor-color",
        cursor_selection_color="selection-color",
        cursor_selection_enable=False,
        cursor_size=cursor_size,
        cursor_switch_ms=250,
        input_type="numeric",
        input_underline="-",
        input_underline_len=10,
        input_underline_vmargin=0,
        maxchar=6,
        maxwidth=20,
        onchange=onchange,
        onreturn=onreturn,
        onselect=onselect,
        password=False,
        textinput_id="code-input",
        title="Code",
        valid_chars=valid_chars,
    )

    widget.set_default_value.assert_called_once_with(123)


def test_text_input_passes_input_underline_vmargin_to_constructor(
    manager,
    text_input_factory,
):
    text_input_factory, widget = text_input_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.text_input(
        title="Input",
        input_underline_vmargin=7,
    )

    text_input_factory.assert_called_once_with(
        copy_paste_enable=True,
        cursor_color="cursor-color",
        cursor_selection_color="selection-color",
        cursor_selection_enable=True,
        cursor_size=None,
        cursor_switch_ms=250,
        input_type=INPUT_TEXT,
        input_underline="",
        input_underline_len=0,
        input_underline_vmargin=7,
        maxchar=0,
        maxwidth=0,
        onchange=None,
        onreturn=None,
        onselect=None,
        password=False,
        textinput_id="",
        title="Input",
        valid_chars=None,
    )


def test_text_input_filters_widget_attributes_before_constructing_widget(
    manager,
    text_input_factory,
):
    text_input_factory, widget = text_input_factory

    kwargs = {
        "font_size": 20,
        "font_color": "red",
        "input_underline_vmargin": 8,
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

    manager.text_input(
        "Input",
        **kwargs,
    )

    assert captured_kwargs == kwargs

    manager._configure_widget.assert_called_once_with(
        widget=widget,
        font_size=20,
        font_color="red",
    )

    configure_kwargs = manager._configure_widget.call_args.kwargs
    assert "input_underline_vmargin" not in configure_kwargs


def test_text_input_passes_remaining_kwargs_to_constructor(
    manager,
    text_input_factory,
):
    text_input_factory, widget = text_input_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.text_input(
        "Input",
        custom_constructor_option="custom-value",
    )

    constructor_kwargs = text_input_factory.call_args.kwargs
    assert constructor_kwargs["custom_constructor_option"] == "custom-value"


def test_text_input_configures_before_appending_and_sets_default_last(
    manager,
    text_input_factory,
):
    text_input_factory, widget = text_input_factory
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

    widget.set_default_value.side_effect = lambda value: events.append(
        ("set_default_value", value)
    )

    manager.text_input(
        "Input",
        default="hello",
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
        ("set_default_value", "hello"),
    ]


def test_text_input_rejects_nonempty_default_when_password_is_enabled(
    manager,
    text_input_factory,
):
    text_input_factory, widget = text_input_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    with pytest.raises(
        ValueError,
        match="default value must be empty if the input is a password",
    ):
        manager.text_input(
            title="Password",
            default="secret",
            password=True,
        )

    text_input_factory.assert_not_called()
    manager._filter_widget_attributes.assert_not_called()
    manager._configure_widget.assert_not_called()
    manager._append_widget.assert_not_called()


def test_text_input_allows_empty_default_when_password_is_enabled(
    manager,
    text_input_factory,
):
    text_input_factory, widget = text_input_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.text_input(
        title="Password",
        default="",
        password=True,
    )

    assert result is widget

    text_input_factory.assert_called_once()
    assert text_input_factory.call_args.kwargs["password"] is True
    widget.set_default_value.assert_called_once_with("")


def test_text_input_does_not_append_when_configuration_fails(
    manager,
    text_input_factory,
):
    text_input_factory, widget = text_input_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock(side_effect=RuntimeError("configuration failed"))
    manager._append_widget = Mock()

    with pytest.raises(RuntimeError, match="configuration failed"):
        manager.text_input(
            "Input",
            default="hello",
        )

    manager._append_widget.assert_not_called()
    widget.set_default_value.assert_not_called()


def test_text_input_does_not_set_default_when_append_fails(
    manager,
    text_input_factory,
):
    text_input_factory, widget = text_input_factory

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock(side_effect=RuntimeError("append failed"))

    with pytest.raises(RuntimeError, match="append failed"):
        manager.text_input(
            "Input",
            default="hello",
        )

    widget.set_default_value.assert_not_called()
