"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST BASE IMAGE
Test base image management.
"""

import base64
import copy
import io
from pathlib import Path

import pygame
import pytest

import pygame_menu
from pygame_menu.baseimage import (
    IMAGE_MODE_CENTER,
    IMAGE_MODE_FILL,
    IMAGE_MODE_REPEAT_X,
    IMAGE_MODE_REPEAT_XY,
    IMAGE_MODE_REPEAT_Y,
    IMAGE_MODE_SIMPLE,
)
from pygame_menu.utils import load_pygame_image_file
from test._utils import PYGAME_V2, surface


def test_pathlib():
    """Test image load with pathlib."""
    path_img = Path(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    image = pygame_menu.BaseImage(path_img)
    image.draw(surface)
    assert image.get_path() == str(path_img)


def test_from_bytesio():
    """Test image load from base64."""
    photo = (
        "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"
        "zveVVABFSQBYIgIBAA7"
    )
    output = io.BytesIO(base64.b64decode(photo))
    image = pygame_menu.BaseImage(output)
    assert image.get_width() == 70
    assert image.get_height() == 70
    assert image.get_bitsize() == 8
    assert image.get_size() == (70, 70)
    assert image.get_path() == output
    assert image.get_extension() == "BytesIO"

    # Assemble new from base64 bs
    image2 = pygame_menu.BaseImage(photo, frombase64=True)
    assert image.equals(image2)
    assert image2.get_extension() == "base64"

    # Clone base64
    image3 = image2.copy()
    if PYGAME_V2:
        assert image2.equals(image3)


def test_rotation():
    """Test rotation."""
    image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    image.rotate(360)
    prev_size = image.get_size()
    assert prev_size == (256, 256)
    i_sum = 0
    for i in range(91):
        image.rotate(i_sum)
        i_sum += 1  # Rotate the image many angles
    assert image.get_size() == prev_size

    image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU)
    assert image.get_size() == (640, 505)
    image.rotate(90)
    assert image.get_size() == (505, 640)
    image.rotate(180)
    assert image.get_size() == (640, 505)
    image.rotate(270)
    assert image.get_size() == (505, 640)
    image.rotate(360)
    assert image.get_size() == (640, 505)

    assert image.get_angle() == 0
    image.rotate(60)
    assert image.get_size() == (757, 806)
    assert image.get_angle() == 60
    image.rotate(160)
    assert image.get_size() == (774, 693)
    assert image.get_angle() == 160
    image.rotate(180)
    assert image.get_angle() == 180
    assert image.get_size() == (640, 505)


def test_crop():
    """Test baseimage crop."""
    image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    image_c = image.get_crop(0, 0, 10, 10)
    image_cr = image.get_crop_rect(pygame.Rect(0, 0, 10, 10))
    im1 = pygame.image.tostring(image_c, "RGBA")
    im2 = pygame.image.tostring(image_cr, "RGBA")
    assert im1 == im2

    # Save the whole image crop
    w, h = image.get_size()
    image2 = image.copy()
    image2.crop(0, 0, w, h)
    assert image2.equals(image)

    # Crop from rect
    image.crop_rect(pygame.Rect(0, 0, 8, 8))
    assert image.get_size() == (8, 8)


@pytest.mark.parametrize("alpha", [0.5, -1, 267])
def test_alpha_invalid(alpha):
    """Test alpha modes."""
    image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    with pytest.raises(AssertionError):
        image.set_alpha(alpha)


def test_alpha_none():
    """Test setting alpha to None."""
    image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    image.set_alpha(None)


@pytest.mark.parametrize(
    "mode",
    [
        IMAGE_MODE_CENTER,
        IMAGE_MODE_FILL,
        IMAGE_MODE_REPEAT_X,
        IMAGE_MODE_REPEAT_XY,
        IMAGE_MODE_REPEAT_Y,
        IMAGE_MODE_SIMPLE,
    ],
)
def test_modes(mode):
    """Test drawing modes."""
    image = pygame_menu.BaseImage(
        pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES, drawing_mode=mode
    )
    image.draw(surface)


def test_modes_invalid():
    """Test invalid drawing mode."""
    with pytest.raises(AssertionError):
        pygame_menu.BaseImage(
            pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES, drawing_mode=-1
        )


def test_modes_get():
    """Get drawing mode."""
    image = pygame_menu.BaseImage(
        pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES, drawing_mode=IMAGE_MODE_CENTER
    )
    assert image.get_drawing_mode() == IMAGE_MODE_CENTER


def test_drawing_offset():
    """Test drawing offset."""
    image = pygame_menu.BaseImage(
        pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES, drawing_mode=IMAGE_MODE_CENTER
    )
    image.set_drawing_offset((50, 150))
    assert image.get_drawing_offset() == (50, 150)


def test_image_path():
    """Test path."""
    image = pygame_menu.BaseImage(
        pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES, drawing_mode=IMAGE_MODE_CENTER
    )
    assert image.get_path() == pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES


@pytest.mark.parametrize(
    "invalid_path", ["invalid.pnng", "invalid", "file_invalid.png"]
)
def test_extension_validation(invalid_path):
    """Validate a image extension."""
    with pytest.raises(AssertionError):
        pygame_menu.BaseImage(invalid_path)


def test_extension_validation_valid():
    """Test valid extension."""
    pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)


def test_image_properties():
    """Test the getters of the image object."""
    image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    w, h = image.get_size()
    assert w == 256
    assert h == 256
    assert image.get_filename() == "gray_lines"
    assert image.get_extension() == ".png"


def test_scale():
    """Test scale."""
    image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    w, h = image.get_size()
    assert w == 256
    assert h == 256

    image4 = image.copy().scale(4, 4)
    assert image4.get_size() == (1024, 1024)

    # Apply scale 2x algorithm
    image4a = image.copy().scale2x().scale2x()
    assert image4a.get_size() == (1024, 1024)

    image4b = image.copy().scale4x()

    image.scale(2, 2).scale(2, 2)
    assert image.get_size() == (1024, 1024)

    # Check if equal
    assert image.equals(image4)
    assert not image.equals(image4a)
    assert image4a.equals(image4b)


def test_operations():
    """Test the file operations."""
    image_original = pygame_menu.BaseImage(
        pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES
    )
    image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    assert image.equals(image_original)

    # Flip
    image.flip(True, False)
    assert not image.equals(image_original)
    image.restore()
    assert image.equals(image_original)

    # Checkpoint
    image.flip(True, False)
    assert not image.equals(image_original)
    image.checkpoint()
    assert not image.equals(image_original)
    image.restore()
    assert not image.equals(image_original)


def test_invalid_image():
    """Test invalid image opening."""
    image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_PYTHON)
    assert image.get_size() == (110, 109)

    image._drawing_position = "invalid"
    with pytest.raises(ValueError):
        image._get_position_delta()

    # Test invalid image
    with pytest.raises(Exception):
        load_pygame_image_file(pygame_menu.baseimage.IMAGE_EXAMPLE_PYTHON, test=True)


def test_copy():
    """Test copy image."""
    image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    image_copied = image.copy()
    assert image.equals(image_copied)
    image_copy = copy.copy(image)
    image_copy2 = copy.deepcopy(image)
    assert image.equals(image_copy)
    assert image.equals(image_copy2)


def test_transform():
    """Test the image transformation."""
    image_original = pygame_menu.BaseImage(
        pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES
    )
    image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

    # Scale
    image.scale(0.5, 0.5)
    assert image.get_size() == (128, 128)
    with pytest.raises(AssertionError):
        image.scale(0, 1)
    image.scale(2, 1)
    assert image.get_size() == (256, 128)
    assert not image.equals(image_original)

    # Set size
    image.restore()
    image.resize(100, 50)
    image.resize(100, 50)  # This should do nothing
    assert image.get_size() == (100, 50)
    image.restore()
    assert image.equals(image_original)

    # As the example is not 24/32 bits smooth scale fails, but baseimage should notice that
    imag_c = image.copy()
    imag_c.resize(100, 100)

    # Get rect
    rect = image.get_rect()
    assert rect.width == 256

    # Rotate
    image.rotate(45)
    assert image.get_size() == (362, 362)
    image.restore()

    # Scale 2x
    image.scale2x()
    assert image.get_size() == (512, 512)
    image.restore()

    # Scale should not change
    image.scale(1, 1)

    # Image bw
    image.to_bw()

    # Image channels
    image.pick_channels(("r", "g", "b"))

    assert image.get_at((10, 10)) == (56, 56, 56, 255)

    image.set_at((10, 10), (0, 0, 0))
    # assert image.get_at((10, 10)) == (0, 0, 0, 255)


@pytest.mark.parametrize(
    "position,expected_delta",
    [
        (pygame_menu.locals.POSITION_NORTHWEST, (0, 0)),
        (pygame_menu.locals.POSITION_NORTH, lambda w, h: (w / 2, 0)),
        (pygame_menu.locals.POSITION_NORTHEAST, lambda w, h: (w, 0)),
        (pygame_menu.locals.POSITION_WEST, lambda w, h: (0, h / 2)),
        (pygame_menu.locals.POSITION_CENTER, lambda w, h: (w / 2, h / 2)),
        (pygame_menu.locals.POSITION_EAST, lambda w, h: (w, h / 2)),
        (pygame_menu.locals.POSITION_SOUTHWEST, lambda w, h: (0, h)),
        (pygame_menu.locals.POSITION_SOUTH, lambda w, h: (w / 2, h)),
        (pygame_menu.locals.POSITION_SOUTHEAST, lambda w, h: (w, h)),
    ],
)
def test_drawing_position(position, expected_delta):
    """Test drawing position."""
    image = pygame_menu.BaseImage(
        pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES, drawing_offset=(100, 100)
    )
    w, h = image.get_size()
    image.set_drawing_position(position)
    if callable(expected_delta):
        expected = expected_delta(w, h)
    else:
        expected = expected_delta
    assert image._get_position_delta() == expected


def test_drawing_position_invalid():
    """Test invalid drawing position."""
    image = pygame_menu.BaseImage(
        pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES, drawing_offset=(100, 100)
    )
    with pytest.raises(AssertionError):
        image.set_drawing_position(pygame_menu.locals.ALIGN_LEFT)


def test_attributes_copy():
    """Test image attributes on object copy."""
    image = pygame_menu.BaseImage(
        pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES, drawing_offset=(100, 100)
    )
    image.set_attribute("angle", 0)
    image2 = image.copy()
    assert image2.has_attribute("angle")
    assert image2.get_attribute("angle") == 0
    assert image.get_attribute("angle") == 0
    image2.set_attribute("angle", 1)
    assert image2.get_attribute("angle") == 1
    assert image.get_attribute("angle") == 0


def test_cache():
    """Cache draw test."""
    image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    assert image._last_transform[2] is None

    image.set_drawing_mode(pygame_menu.baseimage.IMAGE_MODE_FILL)

    # Draw, this should force cache
    image.draw(surface)
    assert image._last_transform[2] is not None
    s = image._last_transform[2]
    image.draw(surface)  # Draw again, then the image should be the same
    assert image._last_transform[2] == s
    assert image._last_transform[0] == 600

    # Changes the area, then image should change
    r = image.get_rect()
    r.width = 300
    image.draw(surface, r)
    assert image._last_transform[2] != s
    assert image._last_transform[0] == 300


def test_subsurface():
    """Test subsurface."""
    image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_TILED_BORDER)
    assert image.get_size() == (18, 18)
    assert image.subsurface((0, 0, 3, 3)).get_size() == (3, 3)


def test_from_surface():
    """Test image load from a pygame.Surface object."""
    # Create a simple surface
    surf = pygame.Surface((50, 50))
    surf.fill((255, 0, 0))

    # Load BaseImage from surface
    image = pygame_menu.BaseImage(surf)

    # Basic properties
    assert image.get_width() == 50
    assert image.get_height() == 50
    assert image.get_extension() == "<surface>"
    assert image.get_path() == "<surface>"

    # Ensure the internal surface is not the same object
    assert image._surface is not surf

    assert image._original_surface is not surf

    image.to_bw()
    color = image.get_at((10, 10))
    assert color[0] == color[1]
    assert color[1] == color[2]

    image_copy = image.copy()
    assert image.equals(image_copy)
    assert image_copy.get_extension() == "<surface>"

    assert image_copy._surface is not image._surface

    image.set_at((0, 0), (0, 255, 0))
    assert image.get_at((0, 0)) != color
    image.restore()
    assert image.get_at((0, 0)) == surf.get_at((0, 0))

    surf2 = pygame.Surface((50, 50))
    surf2.fill((0, 0, 255))
    image2 = pygame_menu.BaseImage(surf2)
    image2.set_at((0, 0), (255, 255, 0))
    assert surf2.get_at((0, 0)) == (0, 0, 255, 255)
