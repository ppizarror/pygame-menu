"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - SURFACE
Test Surface widget.
"""

import pygame
import pytest

from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented
from test._utils import MenuUtils, PygameEventUtils, surface


@pytest.fixture
def menu():
    return MenuUtils.generic_menu()


def test_surface_widget_basic(menu):
    surf = pygame.Surface((150, 150))
    surf.fill((255, 192, 203))

    widget = menu.add.surface(surf, font_color="red")

    assert widget.get_size() == (166, 158)
    assert widget.get_size(apply_padding=False) == (150, 150)
    assert widget.get_surface() is surf

    # Theme overrides font_color → not red
    assert widget._font_color == (70, 70, 70, 255)


@pytest.mark.parametrize(
    "method,args",
    [
        ("rotate", (10,)),
        ("resize", (10, 10)),
        ("scale", (100, 100)),
        ("flip", (True, True)),
        ("set_max_width", (100,)),
        ("set_max_height", (100,)),
    ],
)
def test_surface_widget_invalid_transforms(menu, method, args):
    surf = pygame.Surface((150, 150))
    widget = menu.add.surface(surf)

    with pytest.raises(WidgetTransformationNotImplemented):
        getattr(widget, method)(*args)


def test_surface_widget_transform_state(menu):
    surf = pygame.Surface((150, 150))
    widget = menu.add.surface(surf)

    # Angle unchanged
    with pytest.raises(WidgetTransformationNotImplemented):
        widget.rotate(10)
    assert widget._angle == 0

    # Scale unchanged
    with pytest.raises(WidgetTransformationNotImplemented):
        widget.scale(100, 100)
    assert widget._scale[:3] == [False, 1, 1]

    # Resize unchanged
    with pytest.raises(WidgetTransformationNotImplemented):
        widget.resize(100, 100)
    assert widget._scale[:3] == [False, 1, 1]

    # Flip unchanged
    with pytest.raises(WidgetTransformationNotImplemented):
        widget.flip(True, True)
    assert widget._flip == (False, False)

    # Max width/height unchanged
    with pytest.raises(WidgetTransformationNotImplemented):
        widget.set_max_width(100)
    assert widget._max_width[0] is None

    with pytest.raises(WidgetTransformationNotImplemented):
        widget.set_max_height(100)
    assert widget._max_height[0] is None


def test_surface_widget_title_and_surface_update(menu):
    surf = pygame.Surface((150, 150))
    surf.fill((255, 192, 203))

    widget = menu.add.surface(surf)

    widget.set_title("epic")
    assert widget.get_title() == ""  # Surface widgets ignore titles

    # Replace surface
    new_surface = pygame.Surface((160, 160))
    new_surface.fill((255, 192, 203))

    inner = pygame.Surface((80, 80))
    inner.fill((75, 0, 130))
    new_surface.blit(inner, (40, 40))

    widget.set_surface(new_surface)
    assert widget.get_size(apply_padding=False) == (160, 160)

    menu.draw(surface)
    widget.update(PygameEventUtils.mouse_motion(widget))
    widget.draw(surface)


def test_surface_widget_value_api(menu):
    widget = menu.add.surface(pygame.Surface((150, 150)))

    with pytest.raises(ValueError):
        widget.get_value()

    with pytest.raises(ValueError):
        widget.set_value("value")

    assert not widget.value_changed()
    widget.reset_value()
