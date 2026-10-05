"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST MANAGER - BUTTON
Test Button widget.
"""

from unittest.mock import Mock, patch

import pygame
import pytest

import pygame_menu
import pygame_menu.events as _events
import pygame_menu.widgets.manager.button as button_module


class TestableButtonManager(button_module.ButtonManager):
    __test__ = False  # Prevents pytest from collecting this as a test class

    def __init__(self, menu=None):
        self._menu = menu or Mock()
        self._verbose = True

    def _add_submenu(self, *args, **kwargs):
        pass

    def _append_widget(self, *args, **kwargs):
        pass

    def _check_kwargs(self, kwargs):
        if "unsupported_key" in kwargs:
            raise ValueError("Unsupported keyword argument")

    def _configure_widget(self, *args, **kwargs):
        pass

    def _filter_widget_attributes(self, *args, **kwargs):
        return {"font_color": (255, 255, 255)}

    def configure_defaults_widget(self, *args, **kwargs):
        pass

    @property
    def _theme(self):
        theme = Mock()
        theme.widget_url_color = (0, 0, 255)
        return theme


@pytest.fixture
def manager():
    return object.__new__(TestableButtonManager)


@pytest.fixture(autouse=True)
def setup_manager(manager):
    manager._menu = Mock()
    manager._verbose = True


def test_button_basic_creation(manager, monkeypatch):
    widget_mock = Mock(name="Button")
    btn_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(button_module, "Button", btn_factory)

    action_func = Mock()
    btn = manager.button("Click Me", action_func, 10, button_id="btn-1", underline=True)

    assert btn is widget_mock
    btn_factory.assert_called_once_with("Click Me", "btn-1", action_func, 10)
    widget_mock.add_underline.assert_called_once()
    widget_mock.set_selection_callback.assert_called_once_with(None)
    assert widget_mock._wordwrap is False


def test_button_accept_kwargs(manager, monkeypatch):
    widget_mock = Mock(name="Button")
    btn_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(button_module, "Button", btn_factory)

    action_func = Mock()
    manager.button(
        "Save",
        action_func,
        accept_kwargs=True,
        custom_param="value",
        button_id="save-btn",
    )

    btn_factory.assert_called_once_with(
        "Save", "save-btn", action_func, custom_param="value"
    )


def test_button_menu_navigation_actions(manager, monkeypatch):
    widget_mock = Mock(name="Button")
    btn_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(button_module, "Button", btn_factory)

    # Test BACK event
    manager.button("Back", _events.BACK, back_count=2)
    btn_factory.assert_called_with("Back", "", manager._menu.reset, 2)

    # Test CLOSE event
    manager.button("Close", _events.CLOSE)
    btn_factory.assert_called_with("Close", "", manager._menu._close)

    # Test EXIT event
    manager.button("Exit", _events.EXIT)
    btn_factory.assert_called_with("Exit", "", manager._menu._exit)

    # Test RESET event
    manager.button("Reset", _events.RESET)
    btn_factory.assert_called_with("Reset", "", manager._menu.full_reset)

    # Test NONE action
    manager.button("None", _events.NONE)
    btn_factory.assert_called_with("None", "")


def test_button_submenu_action(manager, monkeypatch):
    widget_mock = Mock(name="Button")
    widget_mock.to_menu = True
    btn_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(button_module, "Button", btn_factory)

    submenu_mock = Mock(spec=pygame_menu.Menu)
    submenu_mock.in_submenu.return_value = False

    add_submenu_mock = Mock()
    monkeypatch.setattr(manager, "_add_submenu", add_submenu_mock)

    manager.button("Submenu", submenu_mock)

    btn_factory.assert_called_once_with(
        "Submenu", "", manager._menu._open, submenu_mock
    )
    add_submenu_mock.assert_called_once_with(submenu_mock, widget_mock)


def test_banner_creation_surface_and_baseimage(manager, monkeypatch):
    widget_mock = Mock(name="Button")
    widget_mock.resize.return_value = widget_mock
    btn_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(button_module, "Button", btn_factory)

    surface = pygame.Surface((100, 50))
    action_func = Mock()

    banner_btn = manager.banner(surface, action=action_func)

    assert banner_btn is widget_mock
    btn_factory.assert_called_once()
    widget_mock.resize.assert_called_once_with(100, 50)


@patch("webbrowser.open")
def test_url_creation_and_click(mock_webbrowser_open, manager, monkeypatch):
    widget_mock = Mock(name="Button")
    btn_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(button_module, "Button", btn_factory)

    url_btn = manager.url(href="https://www.python.org", title="Python")

    assert url_btn is widget_mock
    btn_factory.assert_called_once()

    # Extract the lambda action passed to button and verify it triggers webbrowser.open
    passed_action = btn_factory.call_args[0][2]
    passed_action()
    mock_webbrowser_open.assert_called_once_with("https://www.python.org")


def test_url_empty_title_uses_href(manager, monkeypatch):
    widget_mock = Mock(name="Button")
    btn_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(button_module, "Button", btn_factory)

    manager.url(href="http://localhost:8000", title="")

    title_arg = btn_factory.call_args[0][0]
    assert title_arg == "http://localhost:8000"


def test_button_recursive_menu_raises_error(manager):
    recursive_menu = Mock(spec=pygame_menu.Menu)
    recursive_menu.in_submenu.return_value = True

    with pytest.raises(ValueError, match="is already on submenu structure"):
        manager.button("Recursive", recursive_menu)


def test_button_invalid_action_raises_error(manager):
    with pytest.raises(ValueError, match="action must be a Menu, a MenuAction"):
        manager.button("Invalid", action=12345)


def test_button_invalid_back_count_raises_assertion(manager):
    with pytest.raises(AssertionError):
        manager.button("Bad Back", _events.BACK, back_count=0)


def test_button_invalid_id_type_raises_assertion(manager):
    with pytest.raises(AssertionError, match="id must be a string"):
        manager.button("Bad ID", button_id=123)  # type: ignore


def test_button_keyword_collision_validation_error(manager):
    with pytest.raises(ValueError, match="Unsupported keyword argument"):
        manager.button("Bad Kwargs", action=Mock(), unsupported_key=True)


def test_url_invalid_format_raises_assertion(manager):
    with pytest.raises(AssertionError, match="invalid link format"):
        manager.url(href="not-a-valid-url")


def test_create_button_from_action_pygame_quit(manager, monkeypatch):
    widget_mock = Mock()
    btn_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(button_module, "Button", btn_factory)

    manager._create_button_from_action(
        title="Quit",
        button_id="",
        action=_events.PYGAME_QUIT,
        total_back=1,
        accept_kwargs=False,
        args=(),
        kwargs={},
    )

    btn_factory.assert_called_once_with(
        "Quit",
        "",
        manager._menu._exit,
    )


def test_button_none_action_maps_to_none_event(manager, monkeypatch):
    widget_mock = Mock()
    btn_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(button_module, "Button", btn_factory)

    result = manager.button("Test", None)

    assert result is widget_mock
    btn_factory.assert_called_once_with("Test", "")


def test_create_button_from_action_window_close(manager, monkeypatch):
    widget_mock = Mock()
    btn_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(button_module, "Button", btn_factory)

    manager._create_button_from_action(
        title="Quit",
        button_id="",
        action=_events.PYGAME_WINDOWCLOSE,
        total_back=1,
        accept_kwargs=False,
        args=(),
        kwargs={},
    )

    btn_factory.assert_called_once_with(
        "Quit",
        "",
        manager._menu._exit,
    )


def test_create_event_button_invalid_event(manager):
    with pytest.raises(ValueError, match="unsupported event action"):
        manager._create_event_button(
            "Test",
            "",
            9999,
            1,
        )


def test_normalize_button_action(manager):
    assert manager._normalize_button_action(_events.PYGAME_QUIT) == _events.EXIT
    assert manager._normalize_button_action(_events.PYGAME_WINDOWCLOSE) == _events.EXIT
    assert manager._normalize_button_action(None) == _events.NONE

    custom_callable = lambda: None
    assert manager._normalize_button_action(custom_callable) is custom_callable


def test_button_wordwrap_and_leading(manager, monkeypatch):
    widget_mock = Mock(name="Button")
    btn_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(button_module, "Button", btn_factory)

    manager.button(
        "Wrapped",
        action=None,
        wordwrap=True,
        leading=12,
        max_nlines=5,
    )

    assert widget_mock._wordwrap is True
    assert widget_mock._leading == 12
    assert widget_mock._max_nlines == 5
