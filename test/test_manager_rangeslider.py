"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - RANGESLIDER
Test RangeSlider widget.
"""

from unittest.mock import Mock

import pytest

import pygame_menu.widgets.manager.rangeslider as rangeslider_module


class TestableRangeSliderManager(rangeslider_module.RangeSliderManager):
    __test__ = False  # Prevents pytest from trying to collect this as a test class

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
        theme = Mock()
        theme.widget_box_margin = (5, 5)
        theme.widget_font_color = (255, 255, 255)
        return theme

    def configure_defaults_widget(self, *args, **kwargs):
        pass


@pytest.fixture
def manager():
    return object.__new__(TestableRangeSliderManager)


def test_range_slider_creates_configures_appends_and_returns_widget(
    manager,
    monkeypatch,
):
    title = "Volume"
    default = 50
    range_values = [0, 100]
    increment = 1
    onchange_cb = Mock()
    onreturn_cb = Mock()
    onselect_cb = Mock()
    rangeslider_id = "vol-slider"
    value_format = str
    width = 200

    kwargs = {
        "range_margin": (10, 10),
        "range_line_color": (0, 0, 0),
        "align": "left",
    }
    filtered_attributes = {"align": "left"}
    widget = Mock(name="RangeSlider")

    filter_attributes = Mock(return_value=filtered_attributes)
    configure_widget = Mock()
    append_widget = Mock()
    rangeslider_factory = Mock(return_value=widget)

    monkeypatch.setattr(rangeslider_module, "RangeSlider", rangeslider_factory)
    monkeypatch.setattr(rangeslider_module, "assert_vector", Mock())

    manager._filter_widget_attributes = filter_attributes
    manager._configure_widget = configure_widget
    manager._append_widget = append_widget

    result = manager.range_slider(
        title=title,
        default=default,
        range_values=range_values,
        increment=increment,
        onchange=onchange_cb,
        onreturn=onreturn_cb,
        onselect=onselect_cb,
        rangeslider_id=rangeslider_id,
        value_format=value_format,
        width=width,
        **kwargs,
    )

    assert result is widget
    filter_attributes.assert_called_once_with(
        {
            "align": "left",
        }
    )
    rangeslider_factory.assert_called_once_with(
        title=title,
        rangeslider_id=rangeslider_id,
        default_value=default,
        range_values=range_values,
        range_width=width,
        increment=increment,
        onchange=onchange_cb,
        onreturn=onreturn_cb,
        onselect=onselect_cb,
        range_line_color=(0, 0, 0),
        range_margin=(10, 10),
        range_text_value_color=(255, 255, 255),
        range_text_value_font_height=0.6,
        range_text_value_tick_hfactor=0.5,
        slider_text_value_font_height=0.6,
        value_format=value_format,
        align="left",
    )
    configure_widget.assert_called_once_with(
        widget=widget,
        **filtered_attributes,
    )
    append_widget.assert_called_once_with(widget)


def test_range_slider_uses_theme_defaults_when_kwargs_omitted(
    manager,
    monkeypatch,
):
    widget = Mock(name="RangeSlider")
    rangeslider_factory = Mock(return_value=widget)

    monkeypatch.setattr(rangeslider_module, "RangeSlider", rangeslider_factory)
    monkeypatch.setattr(rangeslider_module, "assert_vector", Mock())

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.range_slider(
        title="Brightness",
        default=10,
        range_values=[0, 20],
        increment=1,
    )

    _, kwargs_passed = rangeslider_factory.call_args
    assert kwargs_passed["range_margin"] == (5, 5)
    assert kwargs_passed["range_line_color"] == (255, 255, 255)
    assert kwargs_passed["range_text_value_color"] == (255, 255, 255)


def test_range_slider_increments_default_for_discrete_values(
    manager,
    monkeypatch,
):
    widget = Mock(name="RangeSlider")
    rangeslider_factory = Mock(return_value=widget)

    monkeypatch.setattr(rangeslider_module, "RangeSlider", rangeslider_factory)
    monkeypatch.setattr(rangeslider_module, "assert_vector", Mock())

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.range_slider(
        title="Discrete",
        default=1,
        range_values=[1, 2, 3, 4, 5],
        increment=None,
    )

    _, kwargs_passed = rangeslider_factory.call_args
    assert kwargs_passed["increment"] == 1


def test_range_slider_asserts_increment_for_continuous_range(
    manager,
    monkeypatch,
):
    monkeypatch.setattr(rangeslider_module, "assert_vector", Mock())

    with pytest.raises(AssertionError, match="increment must be defined"):
        manager.range_slider(
            title="Continuous",
            default=5.0,
            range_values=[0.0, 10.0],
            increment=None,
        )


def test_range_slider_lifecycle_order(
    manager,
    monkeypatch,
):
    widget = Mock(name="RangeSlider")
    events = []

    monkeypatch.setattr(
        rangeslider_module,
        "RangeSlider",
        Mock(return_value=widget),
    )
    monkeypatch.setattr(rangeslider_module, "assert_vector", Mock())

    manager._filter_widget_attributes = Mock(
        side_effect=lambda attrs: (
            events.append(("filter", attrs)) or {"align": "center"}
        )
    )
    manager._configure_widget = Mock(
        side_effect=lambda **cfg: events.append(("configure", cfg))
    )
    manager._append_widget = Mock(
        side_effect=lambda val: events.append(("append", val))
    )

    manager.range_slider(
        title="Speed",
        default=5,
        range_values=[0, 10],
        increment=1,
    )

    assert events == [
        (
            "filter",
            {},
        ),
        (
            "configure",
            {
                "widget": widget,
                "align": "center",
            },
        ),
        ("append", widget),
    ]


def test_range_slider_does_not_append_when_configuration_fails(
    manager,
    monkeypatch,
):
    widget = Mock(name="RangeSlider")

    monkeypatch.setattr(
        rangeslider_module,
        "RangeSlider",
        Mock(return_value=widget),
    )
    monkeypatch.setattr(rangeslider_module, "assert_vector", Mock())

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock(side_effect=RuntimeError("configuration failed"))
    manager._append_widget = Mock()

    with pytest.raises(RuntimeError, match="configuration failed"):
        manager.range_slider(
            title="Error Slider",
            default=1,
            range_values=[0, 5],
            increment=1,
        )

    manager._append_widget.assert_not_called()


def test_range_slider_respects_explicit_increment_for_discrete_values(
    manager,
    monkeypatch,
):
    widget = Mock(name="RangeSlider")
    rangeslider_factory = Mock(return_value=widget)

    monkeypatch.setattr(rangeslider_module, "RangeSlider", rangeslider_factory)
    monkeypatch.setattr(rangeslider_module, "assert_vector", Mock())

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.range_slider(
        title="Discrete Custom Increment",
        default=2,
        range_values=[2, 4, 6, 8],
        increment=2,
    )

    _, kwargs_passed = rangeslider_factory.call_args
    assert kwargs_passed["increment"] == 2


def test_range_slider_calls_assert_vector_on_range_values(
    manager,
    monkeypatch,
):
    widget = Mock(name="RangeSlider")
    rangeslider_factory = Mock(return_value=widget)
    assert_vector_mock = Mock()

    monkeypatch.setattr(rangeslider_module, "RangeSlider", rangeslider_factory)
    monkeypatch.setattr(rangeslider_module, "assert_vector", assert_vector_mock)

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    custom_range = [10, 20, 30]
    manager.range_slider(
        title="Vector Check",
        default=10,
        range_values=custom_range,
        increment=1,
    )

    assert_vector_mock.assert_called_once_with(custom_range, 0)
