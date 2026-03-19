"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST SCROLLAREA
Test scrollarea.
"""

import copy

import pygame
import pytest

import pygame_menu

# noinspection PyProtectedMember
from pygame_menu._scrollarea import get_scrollbars_from_position
from pygame_menu.locals import (
    INPUT_TEXT,
    ORIENTATION_HORIZONTAL,
    ORIENTATION_VERTICAL,
    POSITION_CENTER,
    POSITION_EAST,
    POSITION_NORTH,
    POSITION_NORTHEAST,
    POSITION_NORTHWEST,
    POSITION_SOUTH,
    POSITION_SOUTHEAST,
    POSITION_SOUTHWEST,
    POSITION_WEST,
    SCROLLAREA_POSITION_BOTH_HORIZONTAL,
    SCROLLAREA_POSITION_BOTH_VERTICAL,
    SCROLLAREA_POSITION_FULL,
    SCROLLAREA_POSITION_NONE,
)
from test._utils import (
    PYGAME_V2,
    TEST_THEME,
    MenuUtils,
    PygameEventUtils,
    surface,
)


def _menu_with_default_theme():
    """Return a generic menu using the default test theme."""
    return MenuUtils.generic_menu(title="menu", theme=TEST_THEME.copy())


@pytest.fixture
def menu():
    """Provides a generic menu instance for testing."""
    return MenuUtils.generic_menu()


@pytest.fixture
def sa(menu):
    """Provides the scrollarea from the generic menu."""
    return menu.get_scrollarea()


def test_scrollarea_position_logic():
    """Test the mapping of position constants to scrollbar identifiers."""
    assert len(get_scrollbars_from_position(SCROLLAREA_POSITION_FULL)) == 4

    for pos in (POSITION_EAST, POSITION_WEST, POSITION_NORTH):
        assert isinstance(get_scrollbars_from_position(pos), str)

    assert get_scrollbars_from_position(POSITION_NORTHWEST) == (
        POSITION_NORTH,
        POSITION_WEST,
    )
    assert get_scrollbars_from_position(POSITION_NORTHEAST) == (
        POSITION_NORTH,
        POSITION_EAST,
    )
    assert get_scrollbars_from_position(POSITION_SOUTHEAST) == (
        POSITION_SOUTH,
        POSITION_EAST,
    )
    assert get_scrollbars_from_position(POSITION_SOUTHWEST) == (
        POSITION_SOUTH,
        POSITION_WEST,
    )
    assert get_scrollbars_from_position(SCROLLAREA_POSITION_BOTH_HORIZONTAL) == (
        POSITION_SOUTH,
        POSITION_NORTH,
    )
    assert get_scrollbars_from_position(SCROLLAREA_POSITION_BOTH_VERTICAL) == (
        POSITION_EAST,
        POSITION_WEST,
    )
    assert get_scrollbars_from_position(SCROLLAREA_POSITION_NONE) == ""

    # Invalid positions should raise ValueError
    for invalid in (INPUT_TEXT, POSITION_CENTER):
        with pytest.raises(ValueError):
            get_scrollbars_from_position(invalid)


def test_surface_cache(menu, sa):
    """Test surface cache update flags."""
    assert not menu._widgets_surface_need_update
    sa.force_menu_surface_cache_update()
    sa.force_menu_surface_update()
    assert menu._widgets_surface_need_update

    # Ensure draw handles a None world gracefully
    sa._world = None
    sa.draw(surface)


def test_copy_exception(sa):
    """ScrollArea should strictly forbid copying."""
    with pytest.raises(pygame_menu._scrollarea._ScrollAreaCopyException):
        copy.copy(sa)
    with pytest.raises(pygame_menu._scrollarea._ScrollAreaCopyException):
        copy.deepcopy(sa)


def test_decorator_association(sa):
    """Test that the decorator correctly references the scrollarea."""
    dec = sa.get_decorator()
    assert dec._obj == sa


def test_translate(sa):
    """Test relative translation of the scrollarea."""
    assert sa.get_translate() == (0, 0)
    rect = sa.get_rect()

    sa.translate(10, 10)
    assert sa.get_translate() == (10, 10)

    new_rect = sa.get_rect()
    assert new_rect.x == rect.x + 10
    assert new_rect.y == rect.y + 10


def test_scrollbar_visibility_logic(sa):
    """Test granular control over scrollbar visibility and force-states."""
    # Logic for finding the vertical/horizontal scrollbars
    s_vert = next(
        s for s in sa._scrollbars if s.get_orientation() == ORIENTATION_VERTICAL
    )

    # Test visibility toggle
    s_vert.show()
    assert s_vert.is_visible()

    sa.hide_scrollbars(ORIENTATION_VERTICAL)
    assert not s_vert.is_visible()

    # Test force-hide logic
    s_vert.disable_visibility_force()
    s_vert.hide(force=True)
    assert not s_vert.is_visible()

    s_vert.show()  # Standard show should fail if forced hide is active
    assert not s_vert.is_visible()

    s_vert.show(force=True)
    assert s_vert.is_visible()


def test_scrollarea_dimensions():
    """Test world size and coordinate transformations."""
    menu = _menu_with_default_theme()
    sa = menu.get_scrollarea()

    menu.render()
    menubar_h = menu.get_menubar().get_height()
    expected_sa_height = menu.get_height() - menubar_h

    assert sa.get_world_size() == (menu.get_width(), expected_sa_height)

    # Coordinate transformation: (10, 10) in local sa should be (10, 10 - menubar) in world
    pos_world = sa.to_world_position((10, 10))
    padding_top = sa.get_view_rect().y
    assert pos_world == (10, 10 - padding_top)


def test_collision_detection(menu, sa):
    """Test collision logic with widgets inside the scrollarea."""
    btn = menu.add.button("test")
    menu.render()

    # Create a click event at the center of the widget's real screen position
    rect_real = sa.to_real_position(btn.get_rect())
    event_click = PygameEventUtils.middle_rect_click(rect_real, inlist=False)

    assert sa.collide(btn, event_click)


@pytest.mark.parametrize(
    "pos, expected_orientation",
    [
        (POSITION_SOUTH, ORIENTATION_HORIZONTAL),
        (POSITION_EAST, ORIENTATION_VERTICAL),
    ],
)
def test_get_scrollbar_default_config(sa, pos, expected_orientation):
    """Test scrollbar retrieval in default (South-East) config."""
    scrollbar = sa.get_scrollbar(pos)
    assert scrollbar is not None
    assert scrollbar.get_orientation() == expected_orientation


@pytest.mark.parametrize("pos", [POSITION_NORTH, POSITION_WEST, POSITION_CENTER])
def test_get_scrollbar_none_for_missing_positions(sa, pos):
    """Test that non-existent scrollbars return None."""
    assert sa.get_scrollbar(pos) is None


def test_full_scrollarea_config():
    """Test that all 4 scrollbars exist when using SCROLLAREA_POSITION_FULL."""
    theme = TEST_THEME.copy()
    theme.scrollarea_position = SCROLLAREA_POSITION_FULL
    menu_full = MenuUtils.generic_menu(theme=theme)
    sa_full = menu_full.get_scrollarea()

    for pos in (POSITION_NORTH, POSITION_SOUTH, POSITION_EAST, POSITION_WEST):
        assert sa_full.get_scrollbar(pos) is not None


def test_bg_image_support():
    """Test that BaseImage is correctly accepted as an area color."""
    img = pygame_menu.baseimage.BaseImage(
        pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU
    )
    sa_custom = pygame_menu._scrollarea.ScrollArea(100, 100, area_color=img)
    sa_custom._make_background_surface()
    assert isinstance(sa_custom._area_color, pygame_menu.BaseImage)


def test_show_hide_scrollbars_full(menu, sa):
    """Full visibility/force logic test for scrollbars."""
    menu.render()
    menu.draw(surface)

    # Show all scrollbars first
    for s in sa._scrollbars:
        s.show()

    # Identify vertical and horizontal scrollbars
    if sa._scrollbars[1].get_orientation() == ORIENTATION_VERTICAL:
        s_vert = sa._scrollbars[1]
        s_horiz = sa._scrollbars[0]
    else:
        s_vert = sa._scrollbars[0]
        s_horiz = sa._scrollbars[1]

    sa.show_scrollbars(ORIENTATION_VERTICAL)
    sa.show_scrollbars(ORIENTATION_HORIZONTAL)

    assert s_vert.is_visible()
    sa.hide_scrollbars(ORIENTATION_VERTICAL)
    assert not s_vert.is_visible()
    assert s_horiz.is_visible()

    sa.hide_scrollbars(ORIENTATION_HORIZONTAL)
    assert not s_vert.is_visible()
    assert not s_horiz.is_visible()

    sa.show_scrollbars(ORIENTATION_HORIZONTAL)
    sa.show_scrollbars(ORIENTATION_VERTICAL)
    assert s_vert.is_visible()
    assert s_horiz.is_visible()

    # Force‑hide logic
    s_vert.disable_visibility_force()
    s_vert.hide()
    assert not s_vert.is_visible()

    s_vert.show()
    assert s_vert.is_visible()

    s_vert.hide(force=True)
    assert not s_vert.is_visible()

    s_vert.show()  # Should NOT override force
    assert not s_vert.is_visible()

    s_vert.show(force=True)
    assert s_vert.is_visible()

    s_vert.hide()  # Should NOT override force
    assert s_vert.is_visible()

    # Reset force and test again
    s_vert.disable_visibility_force()
    s_vert.hide()
    assert not s_vert.is_visible()
    s_vert.show()
    assert s_vert.is_visible()
    s_vert.hide()
    assert not s_vert.is_visible()

    # Slider render test
    s_vert._slider_rect = None
    assert s_vert._render() is None


def test_position_invalid():
    """Test invalid scrollbar position handling."""
    sa = pygame_menu._scrollarea.ScrollArea(100, 100)
    original = sa._scrollbar_positions

    sa._scrollbar_positions = "fake"
    with pytest.raises(ValueError):
        sa._apply_size_changes()

    sa._scrollbar_positions = original


def test_scrollbars_input_flags():
    """Test scrollarea scrollbars input flags and frame scrollarea."""
    menu = MenuUtils.generic_menu(
        touchscreen=False,
        mouse_enabled=False,
        joystick_enabled=False,
        keyboard_enabled=False,
    )
    sa = menu.get_scrollarea()
    sb = sa._scrollbars[0]

    assert not sb._joystick_enabled
    assert not sb._keyboard_enabled
    assert not sb._mouse_enabled
    assert not sb._touchscreen_enabled

    drop = menu.add.dropselect(
        "Subject Id", items=[("a",), ("b",), ("c",)], dropselect_id="s0"
    )
    d_sa = drop._drop_frame.get_scrollarea(inner=True)
    sb_frame = d_sa._scrollbars[0]

    assert not sb_frame._joystick_enabled
    assert not sb_frame._keyboard_enabled
    assert not sb_frame._mouse_enabled
    assert not sb_frame._touchscreen_enabled
    assert sb_frame.get_menu() == menu
    assert d_sa.get_menu() == menu


def test_empty_scrollarea_config():
    """Test scrollarea with SCROLLAREA_POSITION_NONE."""
    theme = TEST_THEME.copy()
    theme.scrollarea_position = SCROLLAREA_POSITION_NONE
    menu = MenuUtils.generic_menu(title="menu", theme=theme)

    for i in range(10):
        menu.add.button(i, bool)

    sa = menu.get_scrollarea()
    expected_height = menu.get_height() - menu.get_menubar().get_height()

    assert sa.get_size() == (600, expected_height)
    assert sa.get_scrollbar_thickness(ORIENTATION_VERTICAL) == 0
    assert sa.get_scrollbar_thickness(ORIENTATION_HORIZONTAL) == 0


def test_change_area_color(menu, sa):
    """Test area color update."""
    old_surface = sa._bg_surface
    assert sa.update_area_color("red") is sa
    assert sa._bg_surface != old_surface


def test_size_full(menu):
    """Full port of the original test_size logic."""
    menu = MenuUtils.generic_menu(title="menu", theme=TEST_THEME.copy())
    menu.render()
    assert menu.get_height(widget=True) == 0

    btn = menu.add.button("hidden")
    btn.hide()
    assert menu.get_height(widget=True) == 0
    menu.render()

    sa = menu.get_scrollarea()
    sa_height = menu.get_height() - menu.get_menubar().get_height()
    sa_width = menu.get_width()

    assert sa.get_world_size() == (sa_width, sa_height)

    rect = sa.get_view_rect()
    assert rect.x == 0
    assert rect.y == 155
    assert rect.width == sa_width
    assert rect.height == sa_height
    assert sa.get_hidden_width() == 0
    assert sa.get_hidden_height() == 0

    rect_world = sa.to_world_position(btn.get_rect())
    assert rect_world.x == 0
    assert rect_world.y == -155

    assert sa.to_world_position((10, 10)) == (10, -145)
    assert not sa.is_scrolling()
    assert sa.get_menu() == menu

    sa._on_vertical_scroll(50)
    sa._on_horizontal_scroll(50)

    world = sa._world
    sa._world = None
    assert sa.get_world_size() == (0, 0)
    sa._world = world

    event = PygameEventUtils.mouse_click(100, 100, inlist=False)
    assert not sa.collide(btn, event)

    rect_real = sa.to_real_position(btn.get_rect())
    event_widget = PygameEventUtils.middle_rect_click(rect_real, inlist=False)
    assert sa.collide(btn, event_widget)

    assert sa.get_world_rect(absolute=True) == pygame.Rect(0, 0, 600, 345)
    assert sa.get_size() == (600, 345)
    assert isinstance(sa.mouse_is_over(), bool)

    assert sa.get_scrollbar_thickness(ORIENTATION_VERTICAL) == 0
    assert sa.get_scrollbar_thickness(ORIENTATION_HORIZONTAL) == 0

    sa._scrollbar_positions = (
        POSITION_NORTH,
        POSITION_EAST,
        POSITION_WEST,
        POSITION_SOUTH,
    )
    assert sa.get_view_rect() == pygame.Rect(0, 155, 600, 345)

    for i in range(10):
        menu.add.button(f"b{i}").scale(20, 1)

    assert sa.get_scrollbar_thickness(ORIENTATION_VERTICAL) == 20
    assert sa.get_scrollbar_thickness(ORIENTATION_HORIZONTAL) == 20

    sa._on_vertical_scroll(0.5)
    sa._on_horizontal_scroll(0.5)

    assert sa.to_real_position((10, 10)) == (10, 165)

    sa2 = pygame_menu._scrollarea.ScrollArea(100, 100)
    assert sa2.get_rect(to_real_position=True) == pygame.Rect(0, 0, 100, 100)
    assert sa2.get_scrollbar_thickness(ORIENTATION_VERTICAL, visible=False) == 0
    assert sa2.get_scrollbar_thickness(ORIENTATION_HORIZONTAL, visible=False) == 0

    with pytest.raises(AssertionError):
        sa2.get_scrollbar_thickness("fake", visible=False)

    theme = pygame_menu.themes.THEME_DEFAULT.copy()
    theme.scrollarea_position = SCROLLAREA_POSITION_FULL
    menu_full = MenuUtils.generic_menu(theme=theme)

    for i in range(20):
        menu_full.add.button(i, bool)

    sa_full = menu_full.get_scrollarea()
    sa_full.show_scrollbars(ORIENTATION_VERTICAL)
    sa_full.show_scrollbars(ORIENTATION_HORIZONTAL)

    assert sa_full.get_view_rect() == (20, 100, 560, 400)


@pytest.mark.skipif(not PYGAME_V2, reason="Requires Pygame V2")
def test_widget_relative_to_view_rect():
    """
    Test widget relative position to view rect.
    """
    menu = MenuUtils.generic_menu()
    buttons = []
    for i in range(20):
        btn_title = f'b{i}'
        buttons.append(menu.add.button(btn_title, button_id=btn_title))
    sa = menu.get_scrollarea()

    def test_relative(widget: pygame_menu.widgets.Widget, x: float, y: float) -> None:
        """Test relative position from widget to scroll view rect."""
        rx, ry = widget.get_scrollarea().get_widget_position_relative_to_view_rect(widget)
        assert rx == pytest.approx(x)
        assert ry == pytest.approx(y)

    test_relative(buttons[0], 0.4689655172413793, 0.15)
    test_relative(buttons[-1], 0.45517241379310347, 2.4775)

    # Scroll to middle
    sa.scroll_to(ORIENTATION_VERTICAL, 0.5)
    test_relative(buttons[0], 0.4689655172413793, -0.645)
    test_relative(buttons[-1], 0.45517241379310347, 1.6825)

    # Scroll to bottom
    sa.scroll_to(ORIENTATION_VERTICAL, 1)
    test_relative(buttons[0], 0.4689655172413793, -1.4375)
    test_relative(buttons[-1], 0.45517241379310347, 0.89)
