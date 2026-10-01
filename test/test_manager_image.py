"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - IMAGE
Test Image widget.
"""

from io import BytesIO
from pathlib import Path
from unittest.mock import Mock

import pygame
import pytest

import pygame_menu.widgets.manager.image as image_module
from pygame_menu.widgets.manager.image import ImageManager


class TestableImageManager(ImageManager):
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
    return object.__new__(TestableImageManager)


@pytest.fixture
def surface():
    return pygame.Surface((16, 16))


def test_image_creates_configures_appends_and_returns_widget(
    manager,
    monkeypatch,
    surface,
):
    image_id = "logo"
    angle = 45
    onselect = Mock(name="onselect")
    scale = (2, 3)
    scale_smooth = False
    selectable = True

    attributes = {
        "align": "center",
        "padding": 8,
    }
    widget = Mock(name="Image")
    widget.is_selectable = False

    image_factory = Mock(return_value=widget)
    filter_attributes = Mock(return_value=attributes)
    check_kwargs = Mock()
    configure_widget = Mock()
    append_widget = Mock()

    monkeypatch.setattr(
        image_module,
        "Image",
        image_factory,
    )

    manager._filter_widget_attributes = filter_attributes
    manager._check_kwargs = check_kwargs
    manager._configure_widget = configure_widget
    manager._append_widget = append_widget

    result = manager.image(
        image_path=surface,
        angle=angle,
        image_id=image_id,
        onselect=onselect,
        scale=scale,
        scale_smooth=scale_smooth,
        selectable=selectable,
        align="center",
        padding=8,
    )

    assert result is widget
    assert widget.is_selectable is True

    filter_attributes.assert_called_once_with(
        {
            "align": "center",
            "padding": 8,
        }
    )

    image_factory.assert_called_once_with(
        angle=angle,
        image_id=image_id,
        image_path=surface,
        onselect=onselect,
        scale=scale,
        scale_smooth=scale_smooth,
    )

    check_kwargs.assert_called_once_with(
        {
            "align": "center",
            "padding": 8,
        }
    )

    configure_widget.assert_called_once_with(
        widget=widget,
        **attributes,
    )

    append_widget.assert_called_once_with(widget)


def test_image_uses_default_arguments(
    manager,
    monkeypatch,
    surface,
):
    widget = Mock(name="Image")
    image_factory = Mock(return_value=widget)

    monkeypatch.setattr(
        image_module,
        "Image",
        image_factory,
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._check_kwargs = Mock()
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.image(surface)

    assert result is widget
    assert widget.is_selectable is False

    image_factory.assert_called_once_with(
        angle=0,
        image_id="",
        image_path=surface,
        onselect=None,
        scale=(1, 1),
        scale_smooth=True,
    )


@pytest.mark.parametrize(
    "image_path",
    [
        "assets/image.png",
        Path("assets/image.png"),
        BytesIO(b"image-data"),
    ],
)
def test_image_accepts_supported_path_types(
    manager,
    monkeypatch,
    image_path,
):
    widget = Mock(name="Image")
    image_factory = Mock(return_value=widget)

    monkeypatch.setattr(
        image_module,
        "Image",
        image_factory,
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._check_kwargs = Mock()
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    result = manager.image(image_path)

    assert result is widget

    image_factory.assert_called_once_with(
        angle=0,
        image_id="",
        image_path=image_path,
        onselect=None,
        scale=(1, 1),
        scale_smooth=True,
    )


def test_image_passes_surface_unchanged(
    manager,
    monkeypatch,
    surface,
):
    widget = Mock(name="Image")
    image_factory = Mock(return_value=widget)

    monkeypatch.setattr(
        image_module,
        "Image",
        image_factory,
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._check_kwargs = Mock()
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.image(surface)

    _, kwargs = image_factory.call_args

    assert kwargs["image_path"] is surface


@pytest.mark.parametrize(
    "image_id",
    [
        "",
        "logo",
        "image_123",
        None,
        123,
    ],
)
def test_image_passes_image_id_unchanged(
    manager,
    monkeypatch,
    surface,
    image_id,
):
    widget = Mock(name="Image")
    image_factory = Mock(return_value=widget)

    monkeypatch.setattr(
        image_module,
        "Image",
        image_factory,
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._check_kwargs = Mock()
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.image(
        image_path=surface,
        image_id=image_id,
    )

    _, kwargs = image_factory.call_args

    assert kwargs["image_id"] == image_id


@pytest.mark.parametrize(
    "selectable",
    [True, False],
)
def test_image_sets_selectable_state(
    manager,
    monkeypatch,
    surface,
    selectable,
):
    widget = Mock(name="Image")
    image_factory = Mock(return_value=widget)

    monkeypatch.setattr(
        image_module,
        "Image",
        image_factory,
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._check_kwargs = Mock()
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.image(
        image_path=surface,
        selectable=selectable,
    )

    assert widget.is_selectable is selectable


@pytest.mark.parametrize(
    "selectable",
    [
        None,
        0,
        1,
        "True",
        [],
        {},
    ],
)
def test_image_rejects_non_boolean_selectable(
    manager,
    surface,
    selectable,
):
    manager._filter_widget_attributes = Mock()
    manager._check_kwargs = Mock()
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    with pytest.raises(AssertionError):
        manager.image(
            image_path=surface,
            selectable=selectable,
        )

    manager._filter_widget_attributes.assert_not_called()
    manager._check_kwargs.assert_not_called()
    manager._configure_widget.assert_not_called()
    manager._append_widget.assert_not_called()


@pytest.mark.parametrize(
    "image_path",
    [
        None,
        123,
        object(),
        [],
        {},
    ],
)
def test_image_rejects_unsupported_image_path(
    manager,
    image_path,
):
    manager._filter_widget_attributes = Mock()
    manager._check_kwargs = Mock()
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    with pytest.raises(AssertionError):
        manager.image(image_path)

    manager._filter_widget_attributes.assert_not_called()
    manager._check_kwargs.assert_not_called()
    manager._configure_widget.assert_not_called()
    manager._append_widget.assert_not_called()


def test_image_removes_unsupported_kwargs_before_filtering(
    manager,
    monkeypatch,
    surface,
):
    widget = Mock(name="Image")
    image_factory = Mock(return_value=widget)
    filter_attributes = Mock(return_value={})
    check_kwargs = Mock()

    monkeypatch.setattr(
        image_module,
        "Image",
        image_factory,
    )

    manager._filter_widget_attributes = filter_attributes
    manager._check_kwargs = check_kwargs
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.image(
        surface,
        align="center",
        padding=4,
        unsupported_value="remove-me",
        another_invalid_kwarg=True,
    )

    expected_kwargs = {
        "align": "center",
        "padding": 4,
    }

    filter_attributes.assert_called_once_with(expected_kwargs)
    check_kwargs.assert_called_once_with(expected_kwargs)


def test_image_keeps_all_supported_kwargs(
    manager,
    monkeypatch,
    surface,
):
    widget = Mock(name="Image")
    supported_kwargs = {
        "align": "center",
        "background_color": "red",
        "background_inflate": (1, 2),
        "border_color": "blue",
        "border_inflate": (3, 4),
        "border_width": 2,
        "cursor": None,
        "margin": (5, 6),
        "padding": 7,
        "selection_color": "white",
        "selection_effect": Mock(name="selection_effect"),
        "border_position": "north",
        "float": True,
        "float_origin_position": True,
        "shadow_color": "black",
        "shadow_radius": 3,
        "shadow_type": "ellipse",
        "shadow_width": 4,
    }

    monkeypatch.setattr(
        image_module,
        "Image",
        Mock(return_value=widget),
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._check_kwargs = Mock()
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    manager.image(
        surface,
        **supported_kwargs,
    )

    manager._filter_widget_attributes.assert_called_once_with(
        supported_kwargs,
    )
    manager._check_kwargs.assert_called_once_with(
        supported_kwargs,
    )


def test_image_filters_attributes_before_creating_widget(
    manager,
    monkeypatch,
    surface,
):
    events = []
    widget = Mock(name="Image")

    monkeypatch.setattr(
        image_module,
        "Image",
        Mock(side_effect=lambda **kwargs: events.append(("create", kwargs)) or widget),
    )

    manager._filter_widget_attributes = Mock(
        side_effect=lambda kwargs: (
            events.append(("filter", kwargs)) or {"custom_attribute": True}
        )
    )
    manager._check_kwargs = Mock(
        side_effect=lambda kwargs: events.append(("check", kwargs))
    )
    manager._configure_widget = Mock(
        side_effect=lambda **kwargs: events.append(("configure", kwargs))
    )
    manager._append_widget = Mock(
        side_effect=lambda value: events.append(("append", value))
    )

    manager.image(
        surface,
        align="center",
    )

    assert [event[0] for event in events] == [
        "filter",
        "create",
        "check",
        "configure",
        "append",
    ]


def test_image_configures_before_appending(
    manager,
    monkeypatch,
    surface,
):
    widget = Mock(name="Image")
    events = []

    monkeypatch.setattr(
        image_module,
        "Image",
        Mock(return_value=widget),
    )

    manager._filter_widget_attributes = Mock(
        return_value={"custom_attribute": True},
    )
    manager._check_kwargs = Mock(
        side_effect=lambda kwargs: events.append(("check", kwargs)),
    )
    manager._configure_widget = Mock(
        side_effect=lambda **kwargs: events.append(("configure", kwargs)),
    )
    manager._append_widget = Mock(
        side_effect=lambda value: events.append(("append", value)),
    )

    manager.image(surface)

    assert events == [
        ("check", {}),
        (
            "configure",
            {
                "widget": widget,
                "custom_attribute": True,
            },
        ),
        ("append", widget),
    ]


def test_image_does_not_append_when_checking_kwargs_fails(
    manager,
    monkeypatch,
    surface,
):
    widget = Mock(name="Image")

    monkeypatch.setattr(
        image_module,
        "Image",
        Mock(return_value=widget),
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._check_kwargs = Mock(
        side_effect=ValueError("invalid keyword arguments"),
    )
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    with pytest.raises(
        ValueError,
        match="invalid keyword arguments",
    ):
        manager.image(surface)

    manager._configure_widget.assert_not_called()
    manager._append_widget.assert_not_called()


def test_image_does_not_append_when_configuration_fails(
    manager,
    monkeypatch,
    surface,
):
    widget = Mock(name="Image")

    monkeypatch.setattr(
        image_module,
        "Image",
        Mock(return_value=widget),
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._check_kwargs = Mock()
    manager._configure_widget = Mock(
        side_effect=RuntimeError("configuration failed"),
    )
    manager._append_widget = Mock()

    with pytest.raises(
        RuntimeError,
        match="configuration failed",
    ):
        manager.image(surface)

    manager._append_widget.assert_not_called()


def test_image_does_not_append_when_widget_creation_fails(
    manager,
    monkeypatch,
    surface,
):
    monkeypatch.setattr(
        image_module,
        "Image",
        Mock(side_effect=RuntimeError("creation failed")),
    )

    manager._filter_widget_attributes = Mock(return_value={})
    manager._check_kwargs = Mock()
    manager._configure_widget = Mock()
    manager._append_widget = Mock()

    with pytest.raises(
        RuntimeError,
        match="creation failed",
    ):
        manager.image(surface)

    manager._check_kwargs.assert_not_called()
    manager._configure_widget.assert_not_called()
    manager._append_widget.assert_not_called()
