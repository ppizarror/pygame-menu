"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - TABLE
Test Table widget.
"""

from unittest.mock import Mock

import pytest

import pygame_menu.widgets.manager.table as table_module


class TestableTableManager(table_module.TableManager):
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
    return object.__new__(TestableTableManager)


def test_table_creates_configures_checks_kwargs_appends_and_returns_widget(
    manager,
    monkeypatch,
):
    table_id = "main-table"
    kwargs = {"background_color": (255, 255, 255), "padding": 10}
    attributes = {"background_color": (255, 255, 255), "padding": 10}
    widget = Mock(name="Table")

    filter_attributes = Mock(return_value=attributes)
    configure_widget = Mock()
    append_widget = Mock()
    check_kwargs = Mock()
    table_factory = Mock(return_value=widget)

    monkeypatch.setattr(table_module, "Table", table_factory)

    manager._filter_widget_attributes = filter_attributes
    manager._configure_widget = configure_widget
    manager._append_widget = append_widget
    manager._check_kwargs = check_kwargs

    result = manager.table(table_id, **kwargs)

    assert result is widget
    filter_attributes.assert_called_once_with(kwargs)
    table_factory.assert_called_once_with(
        table_id=table_id,
    )
    configure_widget.assert_called_once_with(
        widget=widget,
        **attributes,
    )
    append_widget.assert_called_once_with(widget)
    check_kwargs.assert_called_once_with(kwargs)


def test_table_uses_empty_string_as_default_id(
    manager,
    monkeypatch,
):
    widget = Mock(name="Table")
    table_factory = Mock(return_value=widget)

    monkeypatch.setattr(table_module, "Table", table_factory)

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()
    manager._check_kwargs = Mock()

    result = manager.table()

    assert result is widget
    table_factory.assert_called_once_with(
        table_id="",
    )


@pytest.mark.parametrize(
    ("table_id", "kwargs"),
    [
        ("", {}),
        ("custom-id", {"align": "left"}),
        ("data-grid", {"max_width": 400, "max_height": 300}),
        ("styled", {"border_width": 2, "border_color": "red"}),
    ],
)
def test_table_passes_arguments_unchanged(
    manager,
    monkeypatch,
    table_id,
    kwargs,
):
    widget = Mock(name="Table")
    table_factory = Mock(return_value=widget)

    monkeypatch.setattr(table_module, "Table", table_factory)

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()
    manager._check_kwargs = Mock()

    manager.table(table_id, **kwargs)

    table_factory.assert_called_once_with(
        table_id=table_id,
    )


def test_table_lifecycle_order(
    manager,
    monkeypatch,
):
    widget = Mock(name="Table")
    events = []
    kwargs = {"font_size": 16}

    monkeypatch.setattr(
        table_module,
        "Table",
        Mock(return_value=widget),
    )

    manager._filter_widget_attributes = Mock(
        side_effect=lambda attrs: events.append(("filter", attrs)) or {"font_size": 16}
    )
    manager._configure_widget = Mock(
        side_effect=lambda **cfg: events.append(("configure", cfg))
    )
    manager._append_widget = Mock(
        side_effect=lambda val: events.append(("append", val))
    )
    manager._check_kwargs = Mock(
        side_effect=lambda kw: events.append(("check_kwargs", kw))
    )

    manager.table("my-table", **kwargs)

    assert events == [
        ("filter", kwargs),
        (
            "configure",
            {
                "widget": widget,
                "font_size": 16,
            },
        ),
        ("append", widget),
        ("check_kwargs", kwargs),
    ]


def test_table_does_not_append_when_configuration_fails(
    manager,
    monkeypatch,
):
    widget = Mock(name="Table")

    monkeypatch.setattr(
        table_module,
        "Table",
        Mock(return_value=widget),
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock(side_effect=RuntimeError("configuration failed"))
    manager._append_widget = Mock()
    manager._check_kwargs = Mock()

    with pytest.raises(RuntimeError, match="configuration failed"):
        manager.table("error-table")

    manager._append_widget.assert_not_called()
    manager._check_kwargs.assert_not_called()
