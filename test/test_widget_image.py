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


def test_image_set_image(menu):
    """Test replacing image object."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

    new_img = pygame_menu.baseimage.BaseImage(
        pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU
    )

    img.set_image(new_img)

    assert img.get_image() is new_img
    assert img._surface is not None


def test_image_flip_noop(menu):
    """Flipping False/False should not invalidate the image."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

    original_surface = img._surface

    img.flip(False, False)

    assert img._flip == (False, False)
    assert img._surface is original_surface


def test_image_set_max_width_no_resize(menu):
    """set_max_width should do nothing if image is already smaller."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

    img.resize(100, 100)

    size_before = img.get_size()

    img.set_max_width(500)

    assert img.get_size() == size_before


def test_image_set_max_height_no_resize(menu):
    """set_max_height should do nothing if image is already smaller."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

    img.resize(100, 100)

    size_before = img.get_size()

    img.set_max_height(500)

    assert img.get_size() == size_before


def test_image_deferred_rotate(menu):
    """Deferred rotation should invalidate surface without breaking angle/render."""
    surf = pygame.Surface((200, 100))
    img = menu.add.image(surf)

    old_size = img.get_size()  # (200, 100)

    img.rotate(90, render=False)

    assert img._surface is None
    assert img.get_angle() == 90

    # Drawing should trigger re-render and swap dimensions due to 90° rotation
    img.draw(surface)

    assert img._surface is not None
    assert img.get_size() != old_size


def test_image_deferred_resize(menu):
    """Deferred resize should invalidate without immediate render."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    img.set_padding(0)

    img.resize(400, 250, render=False)

    assert img._surface is None

    # Size information should remain coherent
    assert img.get_size() == (400, 250)

    img.draw(surface)

    assert img._surface is not None
    assert img.get_size() == (400, 250)


def test_image_deferred_scale(menu):
    """Deferred scale should invalidate without immediate render."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    img.set_padding(0)

    img.scale(2, 2, render=False)

    assert img._surface is None

    img.draw(surface)

    assert img._surface is not None


def test_image_deferred_flip(menu):
    """Deferred flip should lazily render."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

    img.flip(True, False, render=False)

    assert img._flip == (True, False)
    assert img._surface is None

    img.draw(surface)

    assert img._surface is not None


def test_image_chained_deferred_transformations(menu):
    """Multiple deferred transformations should only require one redraw."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

    img.scale(2, 2, render=False)
    img.rotate(45, render=False)
    img.flip(True, False, render=False)

    assert img._surface is None
    assert img.get_angle() == 45
    assert img._flip == (True, False)

    img.draw(surface)

    assert img._surface is not None


def test_image_render_false_updates_size(menu):
    """Deferred operations must still update layout dimensions."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    img.set_padding(0)

    img.resize(200, 100, render=False)

    assert img.get_size() == (200, 100)


def test_image_deferred_set_max_width(menu):
    """Deferred max-width resize should update dimensions."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    img.set_padding(0)

    img.set_max_width(100, render=False)

    assert img._surface is None
    assert img.get_width() == 100

    img.draw(surface)

    assert img._surface is not None


def test_image_deferred_set_max_height(menu):
    """Deferred max-height resize should update dimensions."""
    img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
    img.set_padding(0)

    img.set_max_height(100, render=False)

    assert img._surface is None
    assert img.get_height() == 100

    img.draw(surface)

    assert img._surface is not None


def test_image_from_baseimage(menu):
    """Image should accept an existing BaseImage."""
    base = pygame_menu.baseimage.BaseImage(
        pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES
    )

    img = menu.add.image(base)

    assert img.get_image() is base


def test_image_widget_id(menu):
    """Image id should be preserved."""
    img = menu.add.image(
        pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
        image_id="test_image",
    )

    assert img.get_id() == "test_image"


def test_image_flip_changes_pixels(menu):
    """Flipping should actually change the image pixels."""
    surf = pygame.Surface((2, 1))
    surf.set_at((0, 0), pygame.Color("red"))
    surf.set_at((1, 0), pygame.Color("blue"))

    img = menu.add.image(surf)
    img.set_padding(0)

    before = img.get_image().get_surface(new=False).copy()
    img.flip(True, False)
    after = img.get_image().get_surface(new=False)

    assert before.get_at((0, 0)) == after.get_at((1, 0))
    assert before.get_at((1, 0)) == after.get_at((0, 0))


def test_image_flip_twice_restores_pixels(menu):
    """Applying the same flip twice should restore the original image."""
    surf = pygame.Surface((2, 1))
    surf.set_at((0, 0), pygame.Color("red"))
    surf.set_at((1, 0), pygame.Color("blue"))

    img = menu.add.image(surf)
    img.set_padding(0)

    original = img.get_image().get_surface(new=False).copy()

    img.flip(True, False)
    img.flip(False, False)

    result = img.get_image().get_surface(new=False)

    assert result.get_at((0, 0)) == original.get_at((0, 0))
    assert result.get_at((1, 0)) == original.get_at((1, 0))


def test_image_flip_each_axis_independently(menu):
    """X and Y flips should be tracked independently."""
    img = menu.add.image(pygame.Surface((20, 10)))

    img.flip(True, False)
    assert img._flip == (True, False)

    img.flip(True, True)
    assert img._flip == (True, True)

    img.flip(False, True)
    assert img._flip == (False, True)

    img.flip(False, False)
    assert img._flip == (False, False)


def test_image_noop_flip_does_not_invalidate_surface(menu):
    """Repeating the current flip state should not invalidate the surface."""
    img = menu.add.image(pygame.Surface((20, 20)))
    original_surface = img._surface

    img.flip(False, False)

    assert img._surface is original_surface


def test_image_rotation_updates_exact_dimensions(menu):
    """A 90-degree rotation should swap width and height."""
    img = menu.add.image(pygame.Surface((200, 100)))
    img.set_padding(0)

    img.rotate(90, render=False)

    assert img.get_size() == (100, 200)

    img.draw(surface)

    assert img.get_size() == (100, 200)


def test_image_rotation_replaces_previous_angle(menu):
    """rotate() should set the current angle rather than accumulate it."""
    img = menu.add.image(pygame.Surface((100, 50)))

    img.rotate(90)
    assert img.get_angle() == 90

    img.rotate(30)
    assert img.get_angle() == 30


def test_image_deferred_scale_updates_dimensions(menu):
    """Deferred scaling should update layout dimensions before drawing."""
    img = menu.add.image(pygame.Surface((100, 50)))
    img.set_padding(0)

    img.scale(2, 3, render=False)

    assert img._surface is None
    assert img.get_size() == (200, 150)


def test_image_deferred_rotation_updates_dimensions_before_draw(menu):
    """Deferred rotation should update layout dimensions before drawing."""
    img = menu.add.image(pygame.Surface((200, 100)))
    img.set_padding(0)

    img.rotate(90, render=False)

    assert img._surface is None
    assert img.get_size() == (100, 200)


def test_image_deferred_flip_preserves_dimensions(menu):
    """Flipping should not change image dimensions."""
    img = menu.add.image(pygame.Surface((100, 50)))
    img.set_padding(0)

    img.flip(True, True, render=False)

    assert img._surface is None
    assert img.get_size() == (100, 50)


def test_image_deferred_transformations_render_once_on_draw(menu, monkeypatch):
    """Multiple deferred transformations should be rendered when drawn."""
    img = menu.add.image(pygame.Surface((100, 50)))
    img.set_padding(0)

    render_count = 0
    original_render = img._render

    def counted_render():
        nonlocal render_count
        render_count += 1
        return original_render()

    monkeypatch.setattr(img, "_render", counted_render)

    img.scale(2, 2, render=False)
    img.rotate(45, render=False)
    img.flip(True, False, render=False)

    assert img._surface is None

    img.draw(surface)

    assert img._surface is not None
    assert render_count >= 1


def test_image_draw_renders_missing_surface(menu):
    """draw() should render safely when the cached surface is missing."""
    img = menu.add.image(pygame.Surface((50, 50)))
    img.set_padding(0)

    img._surface = None
    img.draw(surface)

    assert img._surface is not None


def test_image_set_image_resets_flip_state(menu):
    """Replacing the image should reset the flip state."""
    img = menu.add.image(pygame.Surface((50, 50)))
    img.flip(True, False)

    replacement = pygame_menu.baseimage.BaseImage(pygame.Surface((30, 20)))
    img.set_image(replacement)

    assert img.get_image() is replacement
    assert img._flip == (False, False)


def test_image_set_image_updates_dimensions(menu):
    """Replacing the image should update widget dimensions."""
    img = menu.add.image(pygame.Surface((50, 50)))
    img.set_padding(0)

    replacement = pygame_menu.baseimage.BaseImage(pygame.Surface((120, 80)))
    img.set_image(replacement)

    assert img.get_size() == (120, 80)


def test_image_set_image_invalidates_old_surface(menu):
    """Replacing the image should not retain the old rendered surface."""
    old = pygame.Surface((50, 50))
    new = pygame_menu.baseimage.BaseImage(pygame.Surface((80, 40)))

    img = menu.add.image(old)
    img.set_padding(0)
    old_surface = img._surface

    img.set_image(new)

    assert img._surface is not old_surface
    assert img._surface is not None


def test_image_set_image_accepts_only_baseimage(menu):
    """set_image() should reject unsupported image types."""
    img = menu.add.image(pygame.Surface((20, 20)))

    with pytest.raises(AssertionError):
        img.set_image(pygame.Surface((30, 30)))


def test_image_set_image_after_deferred_transform(menu):
    """set_image() should replace a deferred, not-yet-rendered image safely."""
    img = menu.add.image(pygame.Surface((50, 50)))
    img.scale(2, 2, render=False)

    replacement = pygame_menu.baseimage.BaseImage(pygame.Surface((30, 20)))
    img.set_image(replacement)

    assert img.get_image() is replacement
    assert img._surface is not None
    assert img._flip == (False, False)


def test_image_set_max_width_with_scale_height_preserves_ratio(menu):
    """Scaling height should preserve the image aspect ratio."""
    img = menu.add.image(pygame.Surface((200, 100)))
    img.set_padding(0)

    img.set_max_width(100, scale_height=True)

    assert img.get_size() == (100, 50)


def test_image_set_max_height_with_scale_width_preserves_ratio(menu):
    """Scaling width should preserve the image aspect ratio."""
    img = menu.add.image(pygame.Surface((200, 100)))
    img.set_padding(0)

    img.set_max_height(50, scale_width=True)

    assert img.get_size() == (100, 50)


def test_image_set_max_width_render_false(menu):
    """Deferred maximum-width resizing should update dimensions."""
    img = menu.add.image(pygame.Surface((200, 100)))
    img.set_padding(0)

    img.set_max_width(100, scale_height=True, render=False)

    assert img._surface is None
    assert img.get_size() == (100, 50)

    img.draw(surface)

    assert img._surface is not None


def test_image_set_max_height_render_false(menu):
    """Deferred maximum-height resizing should update dimensions."""
    img = menu.add.image(pygame.Surface((200, 100)))
    img.set_padding(0)

    img.set_max_height(50, scale_width=True, render=False)

    assert img._surface is None
    assert img.get_size() == (100, 50)

    img.draw(surface)

    assert img._surface is not None


def test_image_set_max_width_none_does_nothing(menu):
    """None should disable the maximum-width constraint."""
    img = menu.add.image(pygame.Surface((100, 50)))
    img.set_padding(0)

    before = img.get_size()
    img.set_max_width(None)

    assert img.get_size() == before


def test_image_set_max_height_none_does_nothing(menu):
    """None should disable the maximum-height constraint."""
    img = menu.add.image(pygame.Surface((100, 50)))
    img.set_padding(0)

    before = img.get_size()
    img.set_max_height(None)

    assert img.get_size() == before


def test_image_baseimage_ignores_constructor_transformations(menu):
    """angle and scale should be ignored for an existing BaseImage."""
    base = pygame_menu.baseimage.BaseImage(pygame.Surface((40, 20)))

    img = menu.add.image(
        base,
        angle=90,
        scale=(2, 2),
    )

    assert img.get_image() is base
    assert img.get_angle() == 0


def test_image_constructor_applies_angle(menu):
    """angle should be applied when constructing from a normal image source."""
    img = menu.add.image(pygame.Surface((100, 50)), angle=90)

    assert img.get_angle() == 90


def test_image_constructor_applies_scale(menu):
    """scale should be applied when constructing from a normal image source."""
    img = menu.add.image(pygame.Surface((100, 50)), scale=(2, 3))
    img.set_padding(0)

    assert img.get_size() == (200, 150)


def test_image_constructor_applies_angle_and_scale(menu):
    """angle and scale should both be applied."""
    img = menu.add.image(
        pygame.Surface((100, 50)),
        angle=90,
        scale=(2, 2),
    )
    img.set_padding(0)

    assert img.get_angle() == 90
    assert img.get_size() == (100, 200)


@pytest.mark.parametrize("value", [None, 0, 1, "true", []])
def test_image_flip_rejects_non_boolean_x(menu, value):
    """flip() should validate x."""
    img = menu.add.image(pygame.Surface((10, 10)))

    with pytest.raises(AssertionError):
        img.flip(value, False)


@pytest.mark.parametrize("value", [None, 0, 1, "true", []])
def test_image_flip_rejects_non_boolean_y(menu, value):
    """flip() should validate y."""
    img = menu.add.image(pygame.Surface((10, 10)))

    with pytest.raises(AssertionError):
        img.flip(False, value)


@pytest.mark.parametrize("value", [None, 0, 1, "true", []])
def test_image_flip_rejects_invalid_render(menu, value):
    """flip() should validate render."""
    img = menu.add.image(pygame.Surface((10, 10)))

    with pytest.raises(AssertionError):
        img.flip(False, False, render=value)


@pytest.mark.parametrize("value", [None, 0, 1, "true", []])
def test_image_resize_rejects_invalid_smooth(menu, value):
    """resize() should validate smooth."""
    img = menu.add.image(pygame.Surface((10, 10)))

    with pytest.raises(AssertionError):
        img.resize(20, 20, smooth=value)


@pytest.mark.parametrize("value", [None, 0, 1, "true", []])
def test_image_resize_rejects_invalid_render(menu, value):
    """resize() should validate render."""
    img = menu.add.image(pygame.Surface((10, 10)))

    with pytest.raises(AssertionError):
        img.resize(20, 20, render=value)


def test_selectable_image_configuration(menu):
    """selectable should be stored on the widget."""
    img = menu.add.image(
        pygame.Surface((20, 20)),
        selectable=True,
    )

    assert img.is_selectable


def test_nonselectable_image_configuration(menu):
    """Images should be nonselectable by default."""
    img = menu.add.image(pygame.Surface((20, 20)))

    assert not img.is_selectable


def test_image_onselect_callback_is_preserved(menu):
    """The image callback should be stored."""
    callback = lambda selected, widget, callback_menu: None

    img = menu.add.image(
        pygame.Surface((20, 20)),
        selectable=True,
        onselect=callback,
    )

    assert img._onselect is callback


def test_image_accepts_path(menu, tmp_path):
    """Image should accept a filesystem path."""
    path = tmp_path / "image.png"
    pygame.image.save(pygame.Surface((20, 20)), path)

    img = menu.add.image(path)
    img.set_padding(0)

    assert img.get_size() == (20, 20)
