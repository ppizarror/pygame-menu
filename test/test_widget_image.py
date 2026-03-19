"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - IMAGE
Test Image widget.
"""

import pygame
import pytest

import pygame_menu
from test._utils import MenuUtils, PygameEventUtils, surface


@pytest.fixture
def menu():
    """Create a generic menu fixture for image tests."""
    return MenuUtils.generic_menu()


def test_image_widget_basic(menu):
    """Test image widget."""
    img = menu.add.image(
        pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES, font_color=(2, 9)
    )

    img.set_title("epic")
    assert img.get_title() == ""
    assert img.get_image() is img._image

    img.update(PygameEventUtils.mouse_motion(img))

    assert img.get_height(apply_selection=True) == 264
    assert not img._selected
    assert img.get_selected_time() == 0


def test_image_widget_transformations(menu):
    """Test image widget transformations."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

    assert img.get_size() == (272, 264)

    img.scale(2, 2)
    assert img.get_size() == (528, 520)

    img.resize(500, 500)
    img.set_padding(0)
    assert img.get_size() == (500, 500)

    # Max width
    img.set_max_width(400)
    assert img.get_size() == (400, 500)

    img.set_max_width(800)
    assert img.get_size() == (400, 500)

    img.set_max_width(300, scale_height=True)
    assert img.get_size() == (300, 375)

    # Max height
    img.set_max_height(400)
    assert img.get_size() == (300, 375)

    img.set_max_height(300)
    assert img.get_size() == (300, 300)

    img.set_max_height(200, scale_width=True)
    assert img.get_size() == (200, 200)

    # Rotation
    assert img.get_angle() == 0
    img.rotate(90)
    assert img.get_angle() == 90
    img.rotate(60)
    assert img.get_angle() == 60

    # Flip
    img.flip(True, True)
    assert img._flip == (True, True)

    img.flip(False, False)
    assert img._flip == (False, False)

    img.draw(surface)


def test_image_widget_value_api(menu):
    """Test image value."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

    with pytest.raises(ValueError):
        img.get_value()

    with pytest.raises(ValueError):
        img.set_value("value")

    assert not img.value_changed()
    img.reset_value()


def test_image_from_surface(menu):
    """Test that Image accepts a pygame.Surface and wraps it correctly."""
    surf = pygame.Surface((120, 80))
    img = menu.add.image(surf)
    img.set_padding(0)

    assert isinstance(img.get_image(), pygame_menu.baseimage.BaseImage)
    assert img.get_size() == (120, 80)


def test_image_surface_transformations(menu):
    """Test transformations on an Image created from a pygame.Surface."""
    surf = pygame.Surface((100, 50))
    img = menu.add.image(surf)
    img.set_padding(0)

    img.scale(2, 2)
    assert img.get_size() == (200, 100)

    img.resize(300, 150)
    assert img.get_size() == (300, 150)

    img.rotate(45)
    assert img.get_angle() == 45


def test_image_surface_widget_behavior(menu):
    """Ensure Surface-based Image behaves like a normal widget."""
    surf = pygame.Surface((60, 60))
    img = menu.add.image(surf)

    img.set_padding(10)
    assert img.get_size() == (80, 80)

    img.update(PygameEventUtils.mouse_motion(img))
    assert img._mouseover
