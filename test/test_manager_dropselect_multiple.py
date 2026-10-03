"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST MANAGER - DROP SELECT MULTIPLE
Test DropSelectMultiple widget.
"""

from unittest.mock import Mock

import pytest

import pygame_menu.widgets.manager.dropselect_multiple as dsm_module
from pygame_menu.locals import (
    POSITION_SOUTHEAST,
    POSITION_SOUTHWEST,
    SCROLLAREA_POSITION_NONE,
)


class TestableDropSelectMultipleManager(dsm_module.DropSelectMultipleManager):
    __test__ = False  # Prevents pytest from collecting this as a test class

    def _add_submenu(self, *args, **kwargs):
        pass

    def _append_widget(self, *args, **kwargs):
        pass

    def _check_kwargs(self, *args, **kwargs):
        pass

    def _configure_widget(self, *args, **kwargs):
        pass

    def _filter_widget_attributes(self, *args, **kwargs):
        return {"font_color": (255, 255, 255)}

    def configure_defaults_widget(self, *args, **kwargs):
        pass

    @property
    def _theme(self):
        theme = Mock()
        theme.widget_box_arrow_color = (200, 200, 200)
        theme.widget_box_arrow_margin = (5, 5, 5)
        theme.widget_box_background_color = (50, 50, 50)
        theme.widget_box_border_color = (100, 100, 100)
        theme.widget_box_border_width = 1
        theme.widget_border_inflate = (0, 0)
        theme.widget_box_margin = (10, 10)
        theme.scrollbar_color = (120, 120, 120)
        theme.scrollbar_cursor = None
        theme.scrollbar_shadow_color = (0, 0, 0)
        theme.scrollbar_shadow_offset = 2
        theme.scrollbar_shadow_position = POSITION_SOUTHEAST
        theme.scrollbar_shadow = False
        theme.scrollbar_slider_color = (150, 150, 150)
        theme.scrollbar_slider_hover_color = (180, 180, 180)
        theme.scrollbar_slider_pad = 1
        theme.scrollbar_thick = 12
        theme.scrollarea_position = SCROLLAREA_POSITION_NONE
        return theme


@pytest.fixture
def manager():
    return object.__new__(TestableDropSelectMultipleManager)


def test_dropselect_multiple_basic_creation(manager, monkeypatch):
    widget_mock = Mock(name="DropSelectMultiple")
    dsm_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(dsm_module, "DropSelectMultiple", dsm_factory)

    items = [("Option A", 1), ("Option B", 2), ("Option C", 3)]
    result = manager.dropselect_multiple(
        title="Multi Choose:",
        items=items,
        default=[0, 1],
        dropselect_multiple_id="dsm-1",
        max_selected=2,
    )

    assert result is widget_mock
    dsm_factory.assert_called_once()
    _, kwargs = dsm_factory.call_args
    assert kwargs["title"] == "Multi Choose:"
    assert kwargs["items"] == items
    assert kwargs["default"] == [0, 1]
    assert kwargs["dropselect_id"] == "dsm-1"
    assert kwargs["max_selected"] == 2
    assert kwargs["placeholder"] == "Select an option"
    assert kwargs["placeholder_selected"] == "{0} selected"


def test_dropselect_multiple_custom_selection_box_properties(manager, monkeypatch):
    widget_mock = Mock(name="DropSelectMultiple")
    dsm_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(dsm_module, "DropSelectMultiple", dsm_factory)

    manager.dropselect_multiple(
        title="Options:",
        items=["A", "B", "C"],
        selection_box_height=4,
        selection_box_width=200,
        selection_infinite=True,
        open_middle=True,
        selection_option_selected_box=False,
    )

    _, kwargs = dsm_factory.call_args
    assert kwargs["selection_box_height"] == 4
    assert kwargs["selection_box_width"] == 200
    assert kwargs["selection_infinite"] is True
    assert kwargs["open_middle"] is True
    assert kwargs["selection_option_selected_box"] is False


def test_dropselect_multiple_theme_defaults_applied(manager, monkeypatch):
    widget_mock = Mock(name="DropSelectMultiple")
    dsm_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(dsm_module, "DropSelectMultiple", dsm_factory)

    manager.dropselect_multiple(
        title="Theme Defaults:",
        items=["X", "Y"],
    )

    _, kwargs = dsm_factory.call_args
    assert kwargs["selection_box_bgcolor"] == manager._theme.widget_box_background_color
    assert (
        kwargs["selection_box_border_color"] == manager._theme.widget_box_border_color
    )
    assert kwargs["scrollbar_color"] == manager._theme.scrollbar_color
    assert (
        kwargs["selection_option_selected_box_border"]
        == manager._theme.widget_box_border_width
    )


def test_dropselect_multiple_callbacks_and_scrollbars(manager, monkeypatch):
    widget_mock = Mock(name="DropSelectMultiple")
    dsm_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(dsm_module, "DropSelectMultiple", dsm_factory)

    onchange_mock = Mock()
    onreturn_mock = Mock()
    onselect_mock = Mock()

    manager.dropselect_multiple(
        title="Callbacks:",
        items=["1", "2"],
        onchange=onchange_mock,
        onreturn=onreturn_mock,
        onselect=onselect_mock,
        scrollbars=POSITION_SOUTHWEST,
    )

    _, kwargs = dsm_factory.call_args
    assert kwargs["onchange"] is onchange_mock
    assert kwargs["onreturn"] is onreturn_mock
    assert kwargs["onselect"] is onselect_mock
    assert kwargs["scrollbars"] == POSITION_SOUTHWEST


def test_dropselect_multiple_custom_option_styling(manager, monkeypatch):
    widget_mock = Mock(name="DropSelectMultiple")
    dsm_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(dsm_module, "DropSelectMultiple", dsm_factory)

    manager.dropselect_multiple(
        title="Styling:",
        items=["1", "2"],
        selection_option_active_bgcolor=(10, 20, 30),
        selection_option_selected_bgcolor=(40, 50, 60),
        selection_option_padding=(5, 10),
    )

    _, kwargs = dsm_factory.call_args
    assert kwargs["selection_option_active_bgcolor"] == (10, 20, 30)
    assert kwargs["selection_option_selected_bgcolor"] == (40, 50, 60)
    assert kwargs["selection_option_padding"] == (5, 10)


def test_dropselect_multiple_appends_and_configures(manager, monkeypatch):
    widget_mock = Mock(name="DropSelectMultiple")
    dsm_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(dsm_module, "DropSelectMultiple", dsm_factory)

    append_mock = Mock()
    configure_mock = Mock()
    monkeypatch.setattr(manager, "_append_widget", append_mock)
    monkeypatch.setattr(manager, "_configure_widget", configure_mock)

    manager.dropselect_multiple(
        title="Hook Test:",
        items=["Foo", "Bar"],
    )

    append_mock.assert_called_once_with(widget_mock)
    configure_mock.assert_called_once()
