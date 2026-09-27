"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST ShadowGenerator
Library ShadowGenerator.
"""

import pytest

from pygame_menu._shadow import ShadowGenerator


@pytest.fixture
def sg():
    return ShadowGenerator()


@pytest.mark.parametrize(
    "width,height,sw,cr",
    [
        (100, 100, 15, 25),
        (120, 80, 10, 20),
        (200, 150, 5, 10),
    ],
)
def test_rectangle_shadow_basic(sg, width, height, sw, cr):
    """Ensure basic rectangular shadow surfaces are generated with correct dimensions."""
    surf = sg.create_new_rectangle_shadow(width, height, sw, cr)
    assert surf is not None
    assert surf.get_size() == (width, height)


@pytest.mark.parametrize(
    "width,height,sw",
    [
        (100, 100, 10),
        (150, 80, 5),
        (200, 200, 20),
    ],
)
def test_ellipse_shadow_basic(sg, width, height, sw):
    """Ensure basic ellipse shadow surfaces are generated with correct dimensions."""
    surf = sg.create_new_ellipse_shadow(width, height, sw)
    assert surf is not None
    assert surf.get_size() == (width, height)


def test_zero_shadow_width_returns_none(sg):
    """Verify that zero shadow width correctly returns None for both types."""
    assert sg.create_new_ellipse_shadow(100, 100, 0) is None
    assert sg.create_new_rectangle_shadow(100, 100, 0, 20) is None


@pytest.mark.parametrize(
    "width,height,cr",
    [
        (10, 10, 20),  # corner radius too large
        (5, 100, 10),  # width too small
        (100, 5, 10),  # height too small
    ],
)
def test_invalid_rectangle_dimensions(sg, width, height, cr):
    """Verify that invalid rectangular dimensions or oversized corner radii return None."""
    assert sg.create_new_rectangle_shadow(width, height, 5, cr) is None


def test_rectangle_shadow_cache(sg):
    """Confirm rectangular shadow requests hit the short-term cache correctly."""
    s1 = sg.create_new_rectangle_shadow(100, 100, 15, 25)
    s2 = sg.create_new_rectangle_shadow(100, 100, 15, 25)
    assert s1 is s2  # same object from cache


def test_ellipse_shadow_cache(sg):
    """Confirm ellipse shadow requests hit the cache correctly."""
    s1 = sg.create_new_ellipse_shadow(100, 100, 10)
    s2 = sg.create_new_ellipse_shadow(100, 100, 10)
    assert s1 is s2


def test_cache_clearing(sg):
    """Ensure forced cache clearing successfully empties all internal shadow caches."""
    sg.create_new_rectangle_shadow(100, 100, 15, 25)
    sg.create_new_ellipse_shadow(100, 100, 10)

    assert len(sg._short_term_rect_cache) > 0
    assert len(sg._created_ellipse_shadows) > 0

    sg.clear_short_term_caches(force=True)

    assert len(sg._short_term_rect_cache) == 0
    assert len(sg._created_ellipse_shadows) == 0
    assert len(sg._preloaded_shadow_corners) == 0


@pytest.mark.parametrize("opacity", [0.0, 0.25, 0.5, 1.0])
def test_opacity_rectangle(sg, opacity):
    """Validate rectangular shadow generation across various opacity levels."""
    surf = sg.create_new_rectangle_shadow(100, 100, 15, 25, opacity=opacity)
    assert surf is not None


@pytest.mark.parametrize("opacity", [0.0, 0.25, 0.5, 1.0])
def test_opacity_ellipse(sg, opacity):
    """Validate ellipse shadow generation across various opacity levels."""
    surf = sg.create_new_ellipse_shadow(100, 100, 10, opacity=opacity)
    assert surf is not None


@pytest.mark.parametrize(
    "ox,oy",
    [
        (0, 0),
        (5, 10),
        (-5, -10),  # negative offsets should clamp to 0
    ],
)
def test_offsets_rectangle(sg, ox, oy):
    """Test rectangular shadow generation with positive and negative directional offsets."""
    surf = sg.create_new_rectangle_shadow(120, 120, 15, 25, offset_x=ox, offset_y=oy)
    assert surf is not None


@pytest.mark.parametrize(
    "ox,oy",
    [
        (0, 0),
        (3, 7),
        (-3, -7),
    ],
)
def test_offsets_ellipse(sg, ox, oy):
    """Test ellipse shadow generation with positive and negative directional offsets."""
    surf = sg.create_new_ellipse_shadow(120, 120, 10, offset_x=ox, offset_y=oy)
    assert surf is not None


@pytest.mark.parametrize("aa", [1, 2, 4, 8])
def test_aa_levels_rectangle(sg, aa):
    """Verify rectangular shadow rendering supports different anti-aliasing steps."""
    surf = sg.create_new_rectangle_shadow(100, 100, 15, 25, aa_amount=aa)
    assert surf is not None


@pytest.mark.parametrize("aa", [1, 2, 4, 8])
def test_aa_levels_ellipse(sg, aa):
    """Verify ellipse shadow rendering supports different anti-aliasing steps."""
    surf = sg.create_new_ellipse_shadow(100, 100, 10, aa_amount=aa)
    assert surf is not None


@pytest.mark.parametrize(
    "color",
    [
        (0, 0, 0),
        (255, 255, 255),
        (128, 64, 32),
    ],
)
def test_color_rectangle(sg, color):
    """Check that rectangular shadows handle alternative custom RGB colors."""
    surf = sg.create_new_rectangle_shadow(100, 100, 15, 25, color=color)
    assert surf is not None


@pytest.mark.parametrize(
    "color",
    [
        (0, 0, 0),
        (255, 255, 255),
        (128, 64, 32),
    ],
)
def test_color_ellipse(sg, color):
    """Check that ellipse shadows handle alternative custom RGB colors."""
    surf = sg.create_new_ellipse_shadow(100, 100, 10, color=color)
    assert surf is not None


def test_rectangle_shadow_cache_isolation(sg):
    """Ensure different colors, opacities, or offsets do not incorrectly hit the same cache entry."""
    s1 = sg.create_new_rectangle_shadow(100, 100, 15, 25, opacity=0.5)
    s2 = sg.create_new_rectangle_shadow(100, 100, 15, 25, opacity=1.0)
    s3 = sg.create_new_rectangle_shadow(100, 100, 15, 25, offset_x=5)

    assert s1 is not s2
    assert s1 is not s3
    assert s2 is not s3


def test_ellipse_shadow_cache_isolation(sg):
    """Ensure different colors, opacities, or offsets isolate ellipse shadow cache entries."""
    s1 = sg.create_new_ellipse_shadow(100, 100, 10, color=(255, 0, 0))
    s2 = sg.create_new_ellipse_shadow(100, 100, 10, color=(0, 255, 0))
    s3 = sg.create_new_ellipse_shadow(100, 100, 10, opacity=0.5)

    assert s1 is not s2
    assert s1 is not s3
