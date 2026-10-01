"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - DROPSELCT
Test DropSelect widget.
"""

from unittest.mock import Mock

import pytest

import pygame_menu.widgets.manager.dropselect as dropselect_module
from pygame_menu.locals import (
    POSITION_SOUTHEAST,
    POSITION_SOUTHWEST,
    SCROLLAREA_POSITION_NONE,
)


class TestableDropSelectManager(dropselect_module.DropSelectManager):
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
    return object.__new__(TestableDropSelectManager)


def test_dropselect_basic_creation(manager, monkeypatch):
    widget_mock = Mock(name="DropSelect")
    dropselect_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(dropselect_module, "DropSelect", dropselect_factory)

    items = [("Option 1", 1), ("Option 2", 2)]
    result = manager.dropselect(
        title="Choose:",
        items=items,
        default=0,
        dropselect_id="ds-1",
    )

    assert result is widget_mock
    dropselect_factory.assert_called_once()
    _, kwargs = dropselect_factory.call_args
    assert kwargs["title"] == "Choose:"
    assert kwargs["items"] == items
    assert kwargs["default"] == 0
    assert kwargs["dropselect_id"] == "ds-1"
    assert kwargs["placeholder"] == "Select an option"
    assert kwargs["placeholder_add_to_selection_box"] is True


def test_dropselect_custom_selection_box_properties(manager, monkeypatch):
    widget_mock = Mock(name="DropSelect")
    dropselect_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(dropselect_module, "DropSelect", dropselect_factory)

    manager.dropselect(
        title="Settings:",
        items=["A", "B", "C"],
        selection_box_height=5,
        selection_box_width=150,
        selection_infinite=True,
        open_middle=True,
    )

    _, kwargs = dropselect_factory.call_args
    assert kwargs["selection_box_height"] == 5
    assert kwargs["selection_box_width"] == 150
    assert kwargs["selection_infinite"] is True
    assert kwargs["open_middle"] is True


def test_dropselect_number_margin_conversion(manager, monkeypatch):
    widget_mock = Mock(name="DropSelect")
    dropselect_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(dropselect_module, "DropSelect", dropselect_factory)

    # Numeric selection_box_margin converts to a 2-tuple (margin, margin)
    manager.dropselect(
        title="Margin Test:",
        items=["1", "2"],
        selection_box_margin=15,
    )

    _, kwargs = dropselect_factory.call_args
    assert kwargs["selection_box_margin"] == (15, 15)


def test_dropselect_tuple_margin_preserved(manager, monkeypatch):
    widget_mock = Mock(name="DropSelect")
    dropselect_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(dropselect_module, "DropSelect", dropselect_factory)

    manager.dropselect(
        title="Tuple Margin:",
        items=["1", "2"],
        selection_box_margin=(20, 10),
    )

    _, kwargs = dropselect_factory.call_args
    assert kwargs["selection_box_margin"] == (20, 10)


def test_dropselect_theme_defaults_applied(manager, monkeypatch):
    widget_mock = Mock(name="DropSelect")
    dropselect_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(dropselect_module, "DropSelect", dropselect_factory)

    manager.dropselect(
        title="Defaults:",
        items=["X", "Y"],
    )

    _, kwargs = dropselect_factory.call_args
    assert kwargs["selection_box_bgcolor"] == manager._theme.widget_box_background_color
    assert (
        kwargs["selection_box_border_color"] == manager._theme.widget_box_border_color
    )
    assert kwargs["scrollbar_color"] == manager._theme.scrollbar_color


def test_dropselect_callbacks_and_scrollbars(manager, monkeypatch):
    widget_mock = Mock(name="DropSelect")
    dropselect_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(dropselect_module, "DropSelect", dropselect_factory)

    onchange_mock = Mock()
    onreturn_mock = Mock()
    onselect_mock = Mock()

    manager.dropselect(
        title="Callbacks:",
        items=["1", "2"],
        onchange=onchange_mock,
        onreturn=onreturn_mock,
        onselect=onselect_mock,
        scrollbars=POSITION_SOUTHWEST,
    )

    _, kwargs = dropselect_factory.call_args
    assert kwargs["onchange"] is onchange_mock
    assert kwargs["onreturn"] is onreturn_mock
    assert kwargs["onselect"] is onselect_mock
    assert kwargs["scrollbars"] == POSITION_SOUTHWEST


def test_dropselect_appends_and_configures(manager, monkeypatch):
    widget_mock = Mock(name="DropSelect")
    dropselect_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(dropselect_module, "DropSelect", dropselect_factory)

    append_mock = Mock()
    configure_mock = Mock()
    monkeypatch.setattr(manager, "_append_widget", append_mock)
    monkeypatch.setattr(manager, "_configure_widget", configure_mock)

    manager.dropselect(
        title="Hook Test:",
        items=["Foo", "Bar"],
    )

    append_mock.assert_called_once_with(widget_mock)
    configure_mock.assert_called_once()
