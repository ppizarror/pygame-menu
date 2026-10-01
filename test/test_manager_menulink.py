"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - MENULINK
Test MenuLink widget.
"""

from unittest.mock import Mock

import pytest

import pygame_menu.widgets.manager.menulink as menulink_module
from pygame_menu.widgets.manager.menulink import MenuLinkManager


class FakeMenu:
    def __init__(self, title="Menu"):
        self.title = title
        self._open = Mock(name=f"{title}._open")
        self.in_submenu = Mock(
            name=f"{title}.in_submenu",
            return_value=False,
        )

    def get_title(self):
        return self.title


class TestableMenuLinkManager(MenuLinkManager):
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
    manager = object.__new__(TestableMenuLinkManager)
    manager._menu = FakeMenu("Parent menu")
    return manager


def test_menu_link_creates_configures_appends_adds_submenu_and_returns_widget(
    manager,
    monkeypatch,
):
    menu = FakeMenu("Child menu")
    link_id = "settings"
    widget = Mock(name="MenuLink")

    menu_link_factory = Mock(return_value=widget)
    configure_defaults_widget = Mock()
    append_widget = Mock()
    add_submenu = Mock()

    monkeypatch.setattr(
        menulink_module,
        "MenuLink",
        menu_link_factory,
    )

    manager.configure_defaults_widget = configure_defaults_widget
    manager._append_widget = append_widget
    manager._add_submenu = add_submenu

    result = manager.menu_link(menu, link_id)

    assert result is widget

    menu_link_factory.assert_called_once_with(
        menu=menu,
        menu_opener_handler=manager._menu._open,
        link_id=link_id,
    )

    configure_defaults_widget.assert_called_once_with(widget)
    append_widget.assert_called_once_with(widget)
    add_submenu.assert_called_once_with(menu, widget)


def test_menu_link_uses_empty_string_as_default_id(
    manager,
    monkeypatch,
):
    menu = FakeMenu("Child menu")
    widget = Mock(name="MenuLink")

    menu_link_factory = Mock(return_value=widget)

    monkeypatch.setattr(
        menulink_module,
        "MenuLink",
        menu_link_factory,
    )

    manager.configure_defaults_widget = Mock()
    manager._append_widget = Mock()
    manager._add_submenu = Mock()

    result = manager.menu_link(menu)

    assert result is widget

    menu_link_factory.assert_called_once_with(
        menu=menu,
        menu_opener_handler=manager._menu._open,
        link_id="",
    )


@pytest.mark.parametrize(
    "link_id",
    [
        "",
        "settings",
        "menu-link",
        "link_123",
        None,
        123,
    ],
)
def test_menu_link_passes_link_id_unchanged(
    manager,
    monkeypatch,
    link_id,
):
    menu = FakeMenu("Child menu")
    widget = Mock(name="MenuLink")

    menu_link_factory = Mock(return_value=widget)

    monkeypatch.setattr(
        menulink_module,
        "MenuLink",
        menu_link_factory,
    )

    manager.configure_defaults_widget = Mock()
    manager._append_widget = Mock()
    manager._add_submenu = Mock()

    manager.menu_link(menu, link_id)

    menu_link_factory.assert_called_once_with(
        menu=menu,
        menu_opener_handler=manager._menu._open,
        link_id=link_id,
    )


def test_menu_link_uses_parent_menu_open_handler(
    manager,
    monkeypatch,
):
    menu = FakeMenu("Child menu")
    widget = Mock(name="MenuLink")

    menu_link_factory = Mock(return_value=widget)

    monkeypatch.setattr(
        menulink_module,
        "MenuLink",
        menu_link_factory,
    )

    manager.configure_defaults_widget = Mock()
    manager._append_widget = Mock()
    manager._add_submenu = Mock()

    manager.menu_link(menu)

    _, kwargs = menu_link_factory.call_args

    assert kwargs["menu_opener_handler"] is manager._menu._open


def test_menu_link_configures_before_appending_and_adding_submenu(
    manager,
    monkeypatch,
):
    menu = FakeMenu("Child menu")
    widget = Mock(name="MenuLink")
    events = []

    monkeypatch.setattr(
        menulink_module,
        "MenuLink",
        Mock(return_value=widget),
    )

    manager.configure_defaults_widget = Mock(
        side_effect=lambda value: events.append(("configure", value))
    )
    manager._append_widget = Mock(
        side_effect=lambda value: events.append(("append", value))
    )
    manager._add_submenu = Mock(
        side_effect=lambda *args: events.append(("add_submenu", *args))
    )

    manager.menu_link(menu, "child")

    assert events == [
        ("configure", widget),
        ("append", widget),
        ("add_submenu", menu, widget),
    ]


def test_menu_link_rejects_invalid_menu_object(
    manager,
    monkeypatch,
):
    invalid_menu = object()
    menu_link_factory = Mock()

    monkeypatch.setattr(
        menulink_module,
        "MenuLink",
        menu_link_factory,
    )

    manager.configure_defaults_widget = Mock()
    manager._append_widget = Mock()
    manager._add_submenu = Mock()

    with pytest.raises(
        ValueError,
        match="menu object is not a pygame_menu.Menu class",
    ):
        manager.menu_link(invalid_menu)

    menu_link_factory.assert_not_called()
    manager.configure_defaults_widget.assert_not_called()
    manager._append_widget.assert_not_called()
    manager._add_submenu.assert_not_called()


def test_menu_link_rejects_link_to_current_menu(
    manager,
    monkeypatch,
):
    menu_link_factory = Mock()

    monkeypatch.setattr(
        menulink_module,
        "MenuLink",
        menu_link_factory,
    )

    manager.configure_defaults_widget = Mock()
    manager._append_widget = Mock()
    manager._add_submenu = Mock()

    with pytest.raises(
        ValueError,
        match="recursive menus lead to unexpected behaviours",
    ):
        manager.menu_link(manager._menu)

    menu_link_factory.assert_not_called()
    manager.configure_defaults_widget.assert_not_called()
    manager._append_widget.assert_not_called()
    manager._add_submenu.assert_not_called()


def test_menu_link_rejects_menu_already_in_parent_submenu_structure(
    manager,
    monkeypatch,
):
    menu = FakeMenu("Existing submenu")
    menu.in_submenu.return_value = True

    menu_link_factory = Mock()

    monkeypatch.setattr(
        menulink_module,
        "MenuLink",
        menu_link_factory,
    )

    manager.configure_defaults_widget = Mock()
    manager._append_widget = Mock()
    manager._add_submenu = Mock()

    with pytest.raises(
        ValueError,
        match="recursive menus lead to unexpected behaviours",
    ):
        manager.menu_link(menu, "recursive-link")

    menu.in_submenu.assert_called_once_with(
        manager._menu,
        recursive=True,
    )

    menu_link_factory.assert_not_called()
    manager.configure_defaults_widget.assert_not_called()
    manager._append_widget.assert_not_called()
    manager._add_submenu.assert_not_called()


def test_menu_link_checks_recursive_structure_before_creating_widget(
    manager,
    monkeypatch,
):
    menu = FakeMenu("Recursive menu")
    menu.in_submenu.return_value = True

    menu_link_factory = Mock(return_value=Mock(name="MenuLink"))

    monkeypatch.setattr(
        menulink_module,
        "MenuLink",
        menu_link_factory,
    )

    manager.configure_defaults_widget = Mock()
    manager._append_widget = Mock()
    manager._add_submenu = Mock()

    with pytest.raises(ValueError):
        manager.menu_link(menu)

    menu_link_factory.assert_not_called()


def test_menu_link_does_not_add_submenu_when_configuration_fails(
    manager,
    monkeypatch,
):
    menu = FakeMenu("Child menu")
    widget = Mock(name="MenuLink")

    monkeypatch.setattr(
        menulink_module,
        "MenuLink",
        Mock(return_value=widget),
    )

    manager.configure_defaults_widget = Mock(
        side_effect=RuntimeError("configuration failed"),
    )
    manager._append_widget = Mock()
    manager._add_submenu = Mock()

    with pytest.raises(
        RuntimeError,
        match="configuration failed",
    ):
        manager.menu_link(menu)

    manager._append_widget.assert_not_called()
    manager._add_submenu.assert_not_called()


def test_menu_link_does_not_add_submenu_when_appending_fails(
    manager,
    monkeypatch,
):
    menu = FakeMenu("Child menu")
    widget = Mock(name="MenuLink")

    monkeypatch.setattr(
        menulink_module,
        "MenuLink",
        Mock(return_value=widget),
    )

    manager.configure_defaults_widget = Mock()
    manager._append_widget = Mock(
        side_effect=RuntimeError("append failed"),
    )
    manager._add_submenu = Mock()

    with pytest.raises(
        RuntimeError,
        match="append failed",
    ):
        manager.menu_link(menu)

    manager._add_submenu.assert_not_called()


def test_menu_link_propagates_submenu_addition_errors(
    manager,
    monkeypatch,
):
    menu = FakeMenu("Child menu")
    widget = Mock(name="MenuLink")

    monkeypatch.setattr(
        menulink_module,
        "MenuLink",
        Mock(return_value=widget),
    )

    manager.configure_defaults_widget = Mock()
    manager._append_widget = Mock()
    manager._add_submenu = Mock(
        side_effect=RuntimeError("submenu registration failed"),
    )

    with pytest.raises(
        RuntimeError,
        match="submenu registration failed",
    ):
        manager.menu_link(menu)

    manager.configure_defaults_widget.assert_called_once_with(widget)
    manager._append_widget.assert_called_once_with(widget)
