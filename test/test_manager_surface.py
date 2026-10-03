"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - SURFACE WIDGET
Test SurfaceWidget widget.
"""

from unittest.mock import Mock

import pytest

import pygame_menu.widgets.manager.surface as surface_module


class TestableSurfaceWidgetManager(surface_module.SurfaceWidgetManager):
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
        return None

    def configure_defaults_widget(self, *args, **kwargs):
        pass


@pytest.fixture
def manager():
    return object.__new__(TestableSurfaceWidgetManager)


@pytest.fixture
def mock_surface():
    return Mock(name="pygame.Surface")


def test_surface_creates_configures_checks_kwargs_appends_and_returns_widget(
    manager,
    monkeypatch,
    mock_surface,
):
    surface_id = "my-surface"
    onselect_cb = Mock()
    selectable = True
    kwargs = {
        "align": "center",
        "background_color": (0, 0, 0),
        "invalid_key": "drop_me",
    }
    filtered_attributes = {"align": "center", "background_color": (0, 0, 0)}
    widget = Mock(name="SurfaceWidget")

    filter_attributes = Mock(return_value=filtered_attributes)
    configure_widget = Mock()
    append_widget = Mock()
    check_kwargs = Mock()
    surface_factory = Mock(return_value=widget)

    monkeypatch.setattr(surface_module, "SurfaceWidget", surface_factory)

    manager._filter_widget_attributes = filter_attributes
    manager._configure_widget = configure_widget
    manager._append_widget = append_widget
    manager._check_kwargs = check_kwargs

    result = manager.surface(
        surface=mock_surface,
        surface_id=surface_id,
        onselect=onselect_cb,
        selectable=selectable,
        **kwargs,
    )

    assert result is widget
    assert widget.is_selectable is selectable

    expected_cleaned_kwargs = {"align": "center", "background_color": (0, 0, 0)}

    filter_attributes.assert_called_once_with(expected_cleaned_kwargs)
    surface_factory.assert_called_once_with(
        surface=mock_surface,
        surface_id=surface_id,
        onselect=onselect_cb,
    )
    check_kwargs.assert_called_once_with(expected_cleaned_kwargs)
    configure_widget.assert_called_once_with(
        widget=widget,
        **filtered_attributes,
    )
    append_widget.assert_called_once_with(widget)


def test_surface_asserts_selectable_is_boolean(manager, mock_surface):
    with pytest.raises(AssertionError):
        manager.surface(surface=mock_surface, selectable="true")


def test_surface_uses_defaults_for_id_and_onselect(
    manager,
    monkeypatch,
    mock_surface,
):
    widget = Mock(name="SurfaceWidget")
    surface_factory = Mock(return_value=widget)

    monkeypatch.setattr(surface_module, "SurfaceWidget", surface_factory)

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()
    manager._check_kwargs = Mock()

    result = manager.surface(surface=mock_surface)

    assert result is widget
    assert widget.is_selectable is False
    surface_factory.assert_called_once_with(
        surface=mock_surface,
        surface_id="",
        onselect=None,
    )


@pytest.mark.parametrize(
    ("surface_id", "selectable", "kwargs"),
    [
        ("", False, {}),
        ("custom-id", True, {"padding": 5}),
        ("logo", False, {"margin": (10, 20), "shadow_width": 2}),
    ],
)
def test_surface_passes_arguments_unchanged(
    manager,
    monkeypatch,
    mock_surface,
    surface_id,
    selectable,
    kwargs,
):
    widget = Mock(name="SurfaceWidget")
    surface_factory = Mock(return_value=widget)

    monkeypatch.setattr(surface_module, "SurfaceWidget", surface_factory)

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock()
    manager._append_widget = Mock()
    manager._check_kwargs = Mock()

    manager.surface(
        surface=mock_surface,
        surface_id=surface_id,
        selectable=selectable,
        **kwargs,
    )

    surface_factory.assert_called_once_with(
        surface=mock_surface,
        surface_id=surface_id,
        onselect=None,
    )
    assert widget.is_selectable is selectable


def test_surface_lifecycle_order(
    manager,
    monkeypatch,
    mock_surface,
):
    widget = Mock(name="SurfaceWidget")
    events = []
    kwargs = {"cursor": 1}

    monkeypatch.setattr(
        surface_module,
        "SurfaceWidget",
        Mock(return_value=widget),
    )

    manager._filter_widget_attributes = Mock(
        side_effect=lambda attrs: events.append(("filter", attrs)) or {"cursor": 1}
    )
    manager._check_kwargs = Mock(
        side_effect=lambda kw: events.append(("check_kwargs", kw))
    )
    manager._configure_widget = Mock(
        side_effect=lambda **cfg: events.append(("configure", cfg))
    )
    manager._append_widget = Mock(
        side_effect=lambda val: events.append(("append", val))
    )

    manager.surface(mock_surface, **kwargs)

    assert events == [
        ("filter", kwargs),
        ("check_kwargs", kwargs),
        (
            "configure",
            {
                "widget": widget,
                "cursor": 1,
            },
        ),
        ("append", widget),
    ]


def test_surface_does_not_append_when_configuration_fails(
    manager,
    monkeypatch,
    mock_surface,
):
    widget = Mock(name="SurfaceWidget")

    monkeypatch.setattr(
        surface_module,
        "SurfaceWidget",
        Mock(return_value=widget),
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._configure_widget = Mock(side_effect=RuntimeError("configuration failed"))
    manager._append_widget = Mock()
    manager._check_kwargs = Mock()

    with pytest.raises(RuntimeError, match="configuration failed"):
        manager.surface(mock_surface)

    manager._append_widget.assert_not_called()
