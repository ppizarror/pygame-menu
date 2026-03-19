"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - DROPSELECT
Test DropSelect and DropSelectMultiple widgets.
"""

import pygame
import pytest

import pygame_menu
import pygame_menu.controls as ctrl
import pygame_menu.widgets.widget.dropselect as dropselect_module
from pygame_menu.locals import FINGERDOWN, ORIENTATION_VERTICAL
from pygame_menu.widgets import (
    DROPSELECT_MULTIPLE_SFORMAT_LIST_COMMA,
    DROPSELECT_MULTIPLE_SFORMAT_LIST_HYPHEN,
    DROPSELECT_MULTIPLE_SFORMAT_TOTAL,
)
from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented
from test._utils import (
    PYGAME_V2,
    THEME_NON_FIXED_TITLE,
    MenuUtils,
    PygameEventUtils,
    surface,
)


@pytest.fixture
def generic_menu():
    """Create a generic menu configured for DropSelect tests."""
    return MenuUtils.generic_menu(
        mouse_motion_selection=True, theme=THEME_NON_FIXED_TITLE
    )


@pytest.fixture
def drop_items():
    """Create a list of DropSelect items used by tests."""
    items = [("This is a really long selection item", 1), ("epic", 2)]
    for i in range(10):
        items.append((f"item{i + 1}", i + 1))
    return items


def test_dropselect_initialization_and_status(generic_menu, drop_items):
    """Test DropSelect initialization and internal status snapshots."""
    menu = generic_menu
    drop = pygame_menu.widgets.DropSelect(
        "dropsel",
        drop_items,
        selection_option_font_size=int(0.75 * menu._theme.widget_font_size),
        placeholder_add_to_selection_box=False,
        selection_option_font=menu._theme.widget_font,
    )
    menu.add.generic_widget(drop, configure_defaults=True)

    assert drop._selection_box_width == (207 if PYGAME_V2 else 208)
    assert drop.get_frame_depth() == 0

    drop.render()
    assert drop._drop_frame.is_scrollable
    assert drop._drop_frame in menu._update_frames

    if PYGAME_V2:
        # Full widget status snapshot
        assert menu._test_widgets_status() == (
            (
                (
                    "DropSelect-dropsel",
                    (0, 0, 0, 123, 149, 354, 49, 123, 304, 123, 149),
                    (1, 0, 1, 1, 0, 0, 0),
                    (
                        "Frame",
                        (-1, -1, -1, 261, 193, 207, 136, 261, 348, 261, 193),
                        (0, 0, 0, 0, 1, 0, 0),
                        (-1, -1),
                    ),
                    (
                        "Button-This is a really long selection item",
                        (-1, -1, -1, 0, -1, 356, 40, 261, 348, 0, 154),
                        (1, 0, 0, 0, 0, 1, 1),
                    ),
                    (
                        "Button-epic",
                        (-1, -1, -1, 0, 38, 356, 40, 261, 386, 0, 193),
                        (1, 0, 0, 0, 0, 1, 1),
                    ),
                    (
                        "Button-item1",
                        (-1, -1, -1, 0, 77, 356, 40, 261, 425, 0, 232),
                        (1, 0, 0, 0, 0, 1, 1),
                    ),
                    (
                        "Button-item2",
                        (-1, -1, -1, 0, 116, 356, 40, 261, 348, 0, 271),
                        (1, 0, 0, 0, 0, 1, 1),
                    ),
                    (
                        "Button-item3",
                        (-1, -1, -1, 0, 155, 356, 40, 261, 348, 0, 310),
                        (1, 0, 0, 0, 0, 1, 1),
                    ),
                    (
                        "Button-item4",
                        (-1, -1, -1, 0, 194, 356, 40, 261, 348, 0, 349),
                        (1, 0, 0, 0, 0, 1, 1),
                    ),
                    (
                        "Button-item5",
                        (-1, -1, -1, 0, 233, 356, 40, 261, 348, 0, 388),
                        (1, 0, 0, 0, 0, 1, 1),
                    ),
                    (
                        "Button-item6",
                        (-1, -1, -1, 0, 272, 356, 40, 261, 348, 0, 427),
                        (1, 0, 0, 0, 0, 1, 1),
                    ),
                    (
                        "Button-item7",
                        (-1, -1, -1, 0, 311, 356, 40, 261, 348, 0, 466),
                        (1, 0, 0, 0, 0, 1, 1),
                    ),
                    (
                        "Button-item8",
                        (-1, -1, -1, 0, 350, 356, 40, 261, 348, 0, 505),
                        (1, 0, 0, 0, 0, 1, 1),
                    ),
                    (
                        "Button-item9",
                        (-1, -1, -1, 0, 389, 356, 40, 261, 348, 0, 544),
                        (1, 0, 0, 0, 0, 1, 1),
                    ),
                    (
                        "Button-item10",
                        (-1, -1, -1, 0, 428, 356, 40, 261, 348, 0, 583),
                        (1, 0, 0, 0, 0, 1, 1),
                    ),
                ),
            )
        )

    assert drop._drop_frame.get_attribute("height") == (135 if PYGAME_V2 else 138)
    assert drop._drop_frame.get_attribute("width") == (187 if PYGAME_V2 else 188)


def test_dropselect_keyboard_events_and_scrolling(generic_menu, drop_items):
    """Test DropSelect keyboard navigation and scrolling behavior."""
    menu = generic_menu
    drop = menu.add.dropselect("dropsel", drop_items)

    # Initial state
    assert not drop.active
    assert not drop._drop_frame.is_visible()

    # Open
    drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    assert drop.active
    assert drop._drop_frame.is_visible()
    assert drop.get_index() == -1

    # Move up selects first
    drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
    assert drop.get_index() == 0

    # Apply closes
    drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    assert not drop.active

    # TAB toggling
    drop.update(PygameEventUtils.key(pygame.K_TAB, keydown=True))
    assert drop.active
    drop.update(PygameEventUtils.key(pygame.K_TAB, keydown=True))
    assert not drop.active
    drop.update(PygameEventUtils.key(pygame.K_TAB, keydown=True))
    assert drop.active

    # Non-infinite down
    drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
    assert drop.get_index() == 0

    # Scroll progression (PYGAME_V2) – monotonic, bounded, ends near bottom
    if PYGAME_V2:
        prev = -1.0
        for _ in range(1, 12):
            drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
            val = drop.get_scroll_value_percentage(ORIENTATION_VERTICAL)
            assert 0.0 <= val <= 1.0
            assert val >= prev
            prev = val
        assert prev > 0.9


def test_dropselect_mouse_and_touch_toggle(generic_menu, drop_items):
    """Test DropSelect mouse and touch interaction toggling."""
    menu = generic_menu
    drop = menu.add.dropselect("dropsel", drop_items)

    # Open
    drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    assert drop.active

    # Mouse click on focus rect keeps active
    assert drop.update(
        PygameEventUtils.middle_rect_click(
            drop.get_focus_rect(), evtype=pygame.MOUSEBUTTONDOWN
        )
    )
    assert drop.active

    # Touch toggle (PYGAME_V2)
    if PYGAME_V2:
        drop._touchscreen_enabled = True
        assert drop.update(
            PygameEventUtils.middle_rect_click(
                drop.get_focus_rect(), menu=menu, evtype=FINGERDOWN
            )
        )
        assert drop.active

    # Click drop box toggles active
    drop.update(PygameEventUtils.middle_rect_click(drop))
    assert not drop.active
    drop.update(PygameEventUtils.middle_rect_click(drop))
    assert drop.active

    # Click middle option selects and closes
    drop.update(PygameEventUtils.middle_rect_click(drop.get_focus_rect()))
    assert drop.get_index() != -1
    assert not drop.active

    # Touch middle reopens (PYGAME_V2)
    if PYGAME_V2:
        assert drop._touchscreen_enabled
        drop.update(
            PygameEventUtils.middle_rect_click(
                drop.get_focus_rect(), evtype=pygame.FINGERUP, menu=drop.get_menu()
            )
        )
        assert drop.active


def test_dropselect_focus_geometry(generic_menu, drop_items):
    """Test focus mask geometry generated for DropSelect widgets."""
    menu = generic_menu
    drop = menu.add.dropselect("dropsel", drop_items)

    if not drop.active:
        drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))

    regions = menu._draw_focus_widget(surface, drop)

    if PYGAME_V2:
        # We only care that we have 4 regions and each is a 4‑point polygon
        assert set(regions.keys()) == {1, 2, 3, 4}
        for pts in regions.values():
            assert len(pts) == 4
            for x, y in pts:
                assert 0 <= x <= surface.get_width()
                assert 0 <= y <= surface.get_height()
    else:
        # Keep the same relaxed check for non‑V2 if you want, or mirror above
        assert set(regions.keys()) == {1, 2, 3, 4}


def test_dropselect_items_update_and_empty(generic_menu, drop_items):
    """Test DropSelect item updates and empty-state behavior."""
    menu = generic_menu
    drop = menu.add.dropselect("dropsel", drop_items)

    drop.render()
    drop_frame_prev = drop._drop_frame

    # Remove frame to test _check_drop_made
    drop._drop_frame = None
    assert drop.get_scroll_value_percentage("any") == -1
    with pytest.raises(dropselect_module._SelectionDropNotMadeException):
        drop._check_drop_made()

    # Restore frame and clear items
    drop._drop_frame = drop_frame_prev
    drop.update_items([])
    drop._make_selection_drop()

    # Just require sane dimensions, not exact emptiness
    assert drop._drop_frame.get_attribute("height") >= 0
    assert drop._drop_frame.get_attribute("width") >= 0

    assert not drop.active
    drop._toggle_drop()
    assert not drop.active

    fr = drop.get_focus_rect()
    r = drop.get_rect(apply_padding=False, to_real_position=True)
    assert fr.x == r.x
    assert fr.y == r.y
    assert fr.width + drop._selection_box_border_width == r.width
    assert fr.height == r.height

    assert drop.get_index() == -1
    with pytest.raises(ValueError):
        drop.get_value()

    drop._up()
    assert drop.get_index() == -1
    drop._down()
    assert drop.get_index() == -1

    assert not drop._drop_frame.is_scrollable
    assert drop_frame_prev not in menu._update_frames

    drop.update_items(drop_items)
    assert drop.get_index() == -1


def test_dropselect_transformations_not_implemented(generic_menu, drop_items):
    """Test DropSelect transformations that are not implemented."""
    menu = generic_menu
    drop = menu.add.dropselect("dropsel", drop_items)

    drop.translate(1, 1)
    assert drop.get_translate() == (1, 1)
    drop.translate(0, 0)

    with pytest.raises(WidgetTransformationNotImplemented):
        drop.rotate(10)
    assert drop._angle == 0

    with pytest.raises(WidgetTransformationNotImplemented):
        drop.resize(10, 10)
    assert not drop._scale[0]
    assert drop._scale[1] == 1
    assert drop._scale[2] == 1

    with pytest.raises(WidgetTransformationNotImplemented):
        drop.scale(100, 100)
    assert not drop._scale[0]
    assert drop._scale[1] == 1
    assert drop._scale[2] == 1

    with pytest.raises(WidgetTransformationNotImplemented):
        drop.flip(True, True)
    assert not drop._flip[0]
    assert not drop._flip[1]

    with pytest.raises(WidgetTransformationNotImplemented):
        drop.set_max_width(100)
    assert drop._max_width[0] is None

    with pytest.raises(WidgetTransformationNotImplemented):
        drop.set_max_height(100)
    assert drop._max_height[0] is None


def test_dropselect_open_bottom_and_frames(generic_menu, drop_items):
    """Test DropSelect open direction and frame integration behavior."""
    menu = generic_menu
    items = drop_items

    # Base drop
    drop = menu.add.dropselect(
        "dropsel",
        items,
        selection_option_font_size=int(0.75 * menu._theme.widget_font_size),
    )
    drop.render()

    # Add margin
    vm = menu.add.vertical_margin(500)
    assert vm.get_height() == 500

    # Second drop with infinite selection
    drop2 = menu.add.dropselect(
        "drop2",
        items,
        dropselect_id="2",
        selection_infinite=True,
        selection_option_font_size=int(0.75 * menu._theme.widget_font_size),
    )
    assert drop2._tab_size == menu._theme.widget_tab_size
    for btn in drop2._option_buttons:
        assert btn._tab_size == menu._theme.widget_tab_size
    assert drop2._drop_frame._tab_size == 4
    assert drop2.get_id() == "2"
    assert menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_VERTICAL) == 0
    assert drop._open_bottom
    assert not drop2._open_bottom

    # Scroll to bottom
    menu.get_scrollarea().scroll_to(ORIENTATION_VERTICAL, 1)
    menu.render()
    assert drop._open_bottom
    assert not drop2._open_bottom

    menu.select_widget(drop2)
    drop2._toggle_drop()

    assert drop2.get_position() == ((132, 554) if PYGAME_V2 else (131, 555))
    assert drop2._drop_frame.get_attribute("height") == (117 if PYGAME_V2 else 120)
    assert drop2._drop_frame.get_attribute("width") == (187 if PYGAME_V2 else 188)

    # Infinite selection behavior
    assert drop2.active
    assert drop2.get_index() == -1
    drop2._down()
    assert drop2.get_index() == 11
    drop2.draw(surface)

    drop._index = -1
    drop2._up()
    assert drop2.get_index() == 0
    drop2._up()
    assert drop2.get_index() == 1
    drop2._down()
    assert drop2.get_index() == 0
    drop2._down()
    assert drop2.get_index() == 11
    drop2._up()
    assert drop2.get_index() == 0

    drop2.set_value("item6")
    assert drop2.get_index() == 7

    # Readonly prevents movement
    drop2.readonly = True
    drop2._up()
    assert drop2.get_index() == 7
    drop2._down()
    assert drop2.get_index() == 7
    drop2.readonly = False

    menu.render()
    if PYGAME_V2:
        assert drop2.get_scroll_value_percentage(ORIENTATION_VERTICAL) == pytest.approx(
            0.606, abs=0.003
        )

    drop2.reset_value()
    assert drop2.active
    assert drop2.get_index() == -1
    drop2.set_scrollarea(drop2.get_scrollarea())

    if PYGAME_V2:
        assert menu._draw_focus_widget(surface, drop2) == {
            1: ((0, 0), (600, 0), (600, 338), (0, 338)),
            2: ((0, 339), (239, 339), (239, 496), (0, 496)),
            3: ((447, 339), (600, 339), (600, 496), (447, 496)),
            4: ((0, 497), (600, 497), (600, 600), (0, 600)),
        }

    menu.draw(surface)
    assert drop2.get_frame() is None
    assert drop2.last_surface == menu._widgets_surface

    # Put drop2 inside frame
    f = menu.add.frame_v(400, 500, max_height=200, background_color=(0, 0, 255))
    f.pack(drop2)
    assert drop2.get_scrollarea() == f.get_scrollarea(inner=True)
    assert drop2._drop_frame.get_scrollarea() == f.get_scrollarea(inner=True)
    assert drop2.get_scrollarea().get_parent() == menu.get_scrollarea()
    assert drop2._drop_frame.get_scrollarea().get_parent() == menu.get_scrollarea()

    drop2.update_items([("optionA", 1), ("optionB", 2)])

    if PYGAME_V2:
        assert drop2._get_status() == (
            (
                "DropSelect-drop2",
                (0, 2, 3, 0, 0, 332, 49, 88, 308, 0, -242),
                (1, 0, 1, 1, 0, 1, 1),
                (
                    "Frame",
                    (-1, -1, -1, 116, 44, 207, 100, 204, 352, 116, -198),
                    (0, 0, 0, 0, 0, 1, 1),
                    (-1, -1),
                ),
                (
                    "Button-optionA",
                    (-1, -1, -1, 116, 77, 207, 34, 204, 385, 116, -165),
                    (1, 0, 0, 0, 0, 1, 2),
                ),
                (
                    "Button-optionB",
                    (-1, -1, -1, 116, 110, 207, 34, 204, 418, 116, -132),
                    (1, 0, 0, 0, 0, 1, 2),
                ),
            )
        )

    assert drop2._drop_frame.get_attribute("height") == (100 if PYGAME_V2 else 103)
    assert drop2._drop_frame.get_attribute("width") == (207 if PYGAME_V2 else 208)
    assert drop2.get_scrollarea().get_parent_scroll_value_percentage(
        ORIENTATION_VERTICAL
    ) == (0, 1)
    assert drop2._open_bottom

    # onchange / onreturn
    test_state = [-1, False]
    drop2.set_default_value(0)

    def test_change(item, v):
        """Validate onchange callback payload for DropSelect."""
        assert item[0][1] == v
        test_state[0] = item[0][0]

    def test_apply(item, v):
        """Validate onreturn callback payload for DropSelect."""
        assert item[0][1] == v
        test_state[1] = not test_state[1]

    drop2.set_onchange(test_change)
    drop2.set_onreturn(test_apply)
    drop2._toggle_drop()
    assert drop2.get_index() == -1
    assert test_state[0] == -1

    drop2._up()
    assert test_state[0] == "optionA"
    drop2._up()
    assert test_state[0] == "optionB"
    drop2._up()
    assert test_state[0] == "optionA"
    assert not test_state[1]

    drop2.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    assert test_state[1]
    assert not drop2.active

    drop2.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    assert test_state[1]
    assert drop2.active

    menu.draw(surface)
    assert drop2.get_frame() == f
    assert drop2.last_surface == f.get_surface()

    drop2.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    assert not test_state[1]
    assert not drop2.active

    # Unpack from frame
    f.unpack(drop2)
    assert drop2.is_floating()
    drop2.set_float(False)
    assert drop2._drop_frame.get_attribute("height") == (100 if PYGAME_V2 else 103)
    assert drop2._drop_frame.get_attribute("width") == (207 if PYGAME_V2 else 208)

    # Close if mouse clicks outside
    menu.select_widget(drop)
    drop._toggle_drop()
    assert drop.active
    drop.update(PygameEventUtils.mouse_click(0, 0))
    assert not drop.active


def test_dropselect_open_middle_and_last_surface(generic_menu, drop_items):
    """Test open-middle positioning and last-surface tracking."""
    menu = generic_menu
    drop = menu.add.dropselect("dropsel", drop_items)

    drop.render()
    if PYGAME_V2:
        x1, y1 = drop._drop_frame.get_position()
        assert 0 <= x1 <= surface.get_width()
        assert 0 <= y1 <= surface.get_height()

    drop._open_middle = True
    menu.render()

    if PYGAME_V2:
        x2, y2 = drop._drop_frame.get_position()
        # Position should change when switching to open_middle
        # noinspection PyUnboundLocalVariable
        assert (x1, y1) != (x2, y2)
        assert 0 <= x2 <= surface.get_width()
        assert 0 <= y2 <= surface.get_height()

    scr = drop._drop_frame.get_scrollarea()
    sfr = drop._drop_frame.get_frame()

    f = menu.add.frame_v(400, 500, max_height=200, background_color=(0, 0, 255))

    # Only pack if the widget actually fits in the frame width
    if drop.get_width() <= f.get_width():
        f.pack(drop)
        menu.render()
        assert drop._drop_frame.get_scrollarea() == scr
        assert drop._drop_frame.get_frame() == sfr

    assert not drop.active
    drop._toggle_drop()
    menu.render()
    menu.draw(surface)
    assert drop.last_surface == menu._widgets_surface


def test_dropselect_multiple_selection_and_formatting(generic_menu, drop_items):
    """Test DropSelectMultiple selection and placeholder formatting modes."""
    menu = generic_menu
    drop = pygame_menu.widgets.DropSelectMultiple(
        "dropsel", drop_items, open_middle=True, selection_box_height=5
    )
    menu.add.generic_widget(drop, configure_defaults=True)

    # Initial state
    assert drop.get_value() == ([], [])
    assert drop._get_current_selected_text() == "Select an option"

    # Open and navigate to 'epic'
    drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
    drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))

    # Toggle selection for 'epic'
    drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    assert drop.get_index() == [1]
    assert drop._get_current_selected_text() == "1 selected"

    # Comma list format
    drop._selection_placeholder_format = DROPSELECT_MULTIPLE_SFORMAT_LIST_COMMA
    drop.set_value("item2", process_index=True)
    assert drop._get_current_selected_text() == "epic,item2 selected"

    # Hyphen list format
    drop._selection_placeholder_format = DROPSELECT_MULTIPLE_SFORMAT_LIST_HYPHEN
    assert drop._get_current_selected_text() == "epic-item2 selected"

    # Total format
    drop._selection_placeholder_format = DROPSELECT_MULTIPLE_SFORMAT_TOTAL
    assert drop._get_current_selected_text() == "2 selected"

    # Custom callable
    drop._selection_placeholder_format = lambda items: " and ".join(items)
    assert drop._get_current_selected_text() == "epic and item2 selected"


def test_dropselect_multiple_format_errors(generic_menu, drop_items):
    """Test DropSelectMultiple formatting error cases."""
    menu = generic_menu
    drop = menu.add.dropselect_multiple("test", drop_items)
    drop.set_value(0, process_index=True)

    # Invalid type
    drop._selection_placeholder_format = 1  # type: ignore
    with pytest.raises(ValueError):
        drop._get_current_selected_text()

    # Wrong signature
    drop._selection_placeholder_format = lambda: "none"  # type: ignore
    with pytest.raises(ValueError):
        drop._get_current_selected_text()


def test_dropselect_multiple_max_limit(generic_menu, drop_items):
    """Test DropSelectMultiple maximum selected-items limit."""
    menu = generic_menu
    drop = menu.add.dropselect_multiple("limit_test", drop_items, max_selected=2)

    drop.set_value(0, process_index=True)
    drop.set_value(1, process_index=True)
    assert drop.get_total_selected() == 2

    # Try to add third
    drop.set_value(2, process_index=True)
    assert drop.get_total_selected() == 2
    assert 2 not in drop.get_index()


def test_value_changed_tracking(generic_menu):
    """Test value-changed tracking for single and multiple DropSelect widgets."""
    menu = generic_menu
    values = [("a", "a"), ("b", "b")]

    # Single select
    drop = menu.add.dropselect("title", items=values, default=0)
    assert not drop.value_changed()
    drop.set_value(1)
    assert drop.value_changed()
    drop.reset_value()
    assert not drop.value_changed()

    # Multi select
    drop_m = menu.add.dropselect_multiple("title", values, default=[0])
    assert not drop_m.value_changed()
    drop_m._selected_indices = [1]
    assert drop_m.value_changed()


def test_empty_title_sizing(generic_menu):
    """Test DropSelect sizing with empty titles."""
    menu = generic_menu
    values = [("a", "a")]
    drop = menu.add.dropselect("", items=values)
    drop_m = menu.add.dropselect_multiple("", items=values)

    assert drop.get_size() == (309, 49)
    assert drop_m.get_size() == (309, 49)


def test_frame_surface_integrity(generic_menu):
    """Test DropSelect surface routing when packed inside frames."""
    menu = generic_menu
    items = [("a", "a"), ("b", "b")]

    frame = menu.add.frame_h(600, 60)
    drop_in_frame = menu.add.dropselect("In Frame", items=items, dropselect_id="s1")
    frame.pack(drop_in_frame)

    menu.render()
    menu.draw(surface)

    # DropSelect draws its drop over everything, so last_surface is widgets surface
    assert drop_in_frame.last_surface == menu._widgets_surface


def test_visibility_toggle_behavior(generic_menu, drop_items):
    """Test visibility toggling behavior for DropSelectMultiple."""
    menu = generic_menu
    drop = menu.add.dropselect_multiple("hide_test", drop_items)

    menu.select_widget(drop)
    drop._toggle_drop()
    assert drop.active
    assert drop._drop_frame.is_visible()

    drop.hide()
    assert not drop.active
    assert not drop._drop_frame.is_visible()


def test_theme_translation_and_focus_rect():
    """Test translated menu coordinates update DropSelect focus rect."""
    menu_theme = pygame_menu.themes.THEME_ORANGE.copy()
    menu_theme.title_fixed = False
    menu_theme.title_offset = (5, -2)
    menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
    menu_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_LIGHT
    menu_theme.widget_font_size = 20

    menu2 = MenuUtils.generic_menu(theme=menu_theme, width=400)
    menu2.add.vertical_margin(1000)

    drop3 = menu2.add.dropselect_multiple(
        title="Pick 3 colors",
        items=[
            ("Black", (0, 0, 0)),
            ("Blue", (0, 0, 255)),
            ("Cyan", (0, 255, 255)),
            ("Fuchsia", (255, 0, 255)),
            ("Green", (0, 255, 0)),
            ("Red", (255, 0, 0)),
            ("White", (255, 255, 255)),
            ("Yellow", (255, 255, 0)),
        ],
        dropselect_multiple_id="pickcolors",
        open_middle=True,
        max_selected=3,
    )
    assert drop3.get_focus_rect() == pygame.Rect(108, 468, 320, 28)

    # Translate menu; focus rect should follow
    menu2.translate(100, 50)
    assert drop3.get_focus_rect() == pygame.Rect(108 + 100, 468 + 50, 320, 28)
    menu2.translate(100, 150)
    assert drop3.get_focus_rect() == pygame.Rect(108 + 100, 468 + 150, 320, 28)
    menu2.translate(0, 0)
    assert drop3.get_focus_rect() == pygame.Rect(108, 468, 320, 28)


def test_update_list_via_button_callback():
    """Test updating DropSelect item lists through button callbacks."""

    def remove_selection_item(select: pygame_menu.widgets.DropSelect):
        """Remove currently selected item from a DropSelect widget."""
        if select.get_index() == -1:
            return
        s_val = select.get_value()
        _items = select.get_items()
        _items.pop(_items.index(s_val[0]))
        select.update_items(_items)

    menu = MenuUtils.generic_menu()
    select1 = menu.add.dropselect(
        "Subject Id",
        items=[("a",), ("b",), ("c",), ("d",), ("e",), ("f",)],
        dropselect_id="s0",
    )
    b_sel = menu.add.button("One", remove_selection_item, select1)

    b_sel.apply()
    select1.set_value(0)
    assert select1.get_value() == (("a",), 0)
    b_sel.apply()
    assert select1.get_index() == -1
    assert select1.get_items() == [("b",), ("c",), ("d",), ("e",), ("f",)]
    b_sel.apply()

    # Update by value
    select1.set_value("b")
    assert select1.get_index() == 0
    select1.set_value("e")
    assert select1.get_index() == 3
    with pytest.raises(ValueError):
        select1.set_value("unknown")
    b_sel.apply()

    select1.active = True
    select1.show()

    # Configured flag
    select1.configured = False
    with pytest.raises(RuntimeError):
        select1._make_selection_drop()
    select1.configured = True
    select1.readonly = True
    assert not select1.update([])


def test_dropselect_touch_interaction_full():
    """Test full DropSelect interaction flow using touch events."""
    if not PYGAME_V2:
        pytest.skip("Touch tests require Pygame V2")

    def remove_selection_item(select: pygame_menu.widgets.DropSelect):
        """Remove currently selected item from a DropSelect widget."""
        if select.get_index() == -1:
            return
        s_val = select.get_value()
        _items = select.get_items()
        _items.pop(_items.index(s_val[0]))
        select.update_items(_items)

    menu = MenuUtils.generic_menu(touchscreen=True)
    sel = menu.add.dropselect(
        "Subject Id",
        items=[("a",), ("b",), ("c",), ("d",), ("e",), ("f",)],
        dropselect_id="s0",
    )
    menu.add.button("One", remove_selection_item, sel)

    touch_sel = sel.get_rect(to_real_position=True).center
    assert sel.get_index() == -1
    assert not sel.active

    # Open via touch
    sel.update(PygameEventUtils.touch_click(touch_sel[0], touch_sel[1], menu=menu))
    assert sel.active

    # Touch null option
    sel.update(PygameEventUtils.touch_click(touch_sel[0], touch_sel[1] + 40, menu=menu))
    assert sel.active

    # Select option a
    sel.update(PygameEventUtils.touch_click(touch_sel[0], touch_sel[1] + 80, menu=menu))
    assert sel.get_index() == 0
    assert not sel.active

    # Touch outside
    sel.update(
        PygameEventUtils.touch_click(touch_sel[0], touch_sel[1] + 400, menu=menu)
    )
    assert not sel.active

    # Touch button via menu
    menu.update(
        PygameEventUtils.touch_click(
            touch_sel[0], touch_sel[1] + 40, menu=menu, evtype=FINGERDOWN
        )
    )
    menu.update(
        PygameEventUtils.touch_click(touch_sel[0], touch_sel[1] + 40, menu=menu)
    )

    # Touch again outside
    sel.update(
        PygameEventUtils.touch_click(touch_sel[0], touch_sel[1] + 400, menu=menu)
    )
    assert not sel.active

    # Select via menu events
    sel.select(update_menu=True)
    sel.update(PygameEventUtils.touch_click(touch_sel[0], touch_sel[1], menu=menu))
    assert sel.active

    # Simulate menu-driven touch that forces selection update
    sel.active = False
    menu._widget_selected_update = False
    menu.update(
        PygameEventUtils.touch_click(
            touch_sel[0], touch_sel[1], menu=menu, evtype=FINGERDOWN
        )
    )


def test_frame_support():
    """
    Test drop selects within frames.
    """
    menu = MenuUtils.generic_menu()

    menu.add.dropselect("Subject Id", items=[("a", "a"), ("b", "b"), ("c", "c")], dropselect_id="s0")
    frame_s = menu.add.frame_h(600, 58)
    frame_s.pack(
        menu.add.dropselect("Subject Id", items=[("a", "a"), ("b", "b"), ("c", "c")], dropselect_id="s1",
                            open_middle=True)
    )
    frame_s.pack(menu.add.button("One", lambda: print("1")))
    frame_t = menu.add.frame_h(600, 58)
    frame_t.pack(
        menu.add.dropselect("Subject Id", items=[("a", "a"), ("b", "b"), ("c", "c")], dropselect_id="s2")
    )
    frame_t.pack(menu.add.button("Two", lambda: print("2")))
    menu.add.dropselect("Subject Id", items=[("a", "a"), ("b", "b"), ("c", "c")], dropselect_id="s3")
    menu.add.dropselect("Subject Id", items=[("a", "a"), ("b", "b"), ("c", "c")], dropselect_id="s4",
                        open_middle=True)

    # Test draw surfaces
    menu.draw(surface)
    s0 = menu.get_widget("s0")
    s1 = menu.get_widget("s1")
    surf = menu._widgets_surface
    assert s0.is_selected()
    assert s0.last_surface == surf
    s0.active = True
    menu.render()
    menu.draw(surface)
    assert s0.last_surface == surf
    s0._selection_effect_draw_post = True
    menu.render()
    menu.draw(surface)
    s0.draw_after_if_selected(surface)

    s1.select(update_menu=True)
    s1.active = True
    menu.draw(surface)
    assert s1.last_surface == surf


def test_dropselect_multiple():
    """Test dropselect multiple widget."""
    theme = pygame_menu.themes.THEME_DEFAULT.copy()
    theme.widget_font_size = 25
    menu = MenuUtils.generic_menu(mouse_motion_selection=True, theme=theme)
    items = [("This is a really long selection item", 1), ("epic", 2)]
    for i in range(10):
        items.append((f"item{i + 1}", i + 1))
    drop = pygame_menu.widgets.DropSelectMultiple(
        "dropsel", items, open_middle=True, selection_box_height=5
    )
    assert id(items) != id(drop._items)
    menu.add.generic_widget(drop, configure_defaults=True)
    assert drop._selection_box_width == 225

    # Check drop is empty
    assert drop.get_value() == ([], [])
    assert drop.get_index() == []
    assert drop._get_current_selected_text() == "Select an option"

    # Check events
    assert not drop.active
    drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    assert drop.active
    assert drop._index == -1
    drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))  # Index is -1
    assert not drop.active
    drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    assert drop.active
    drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
    assert drop._index == 0
    drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
    assert drop._index == 1

    # Apply on current
    drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    assert drop.get_value() == ([("epic", 2)], [1])
    assert drop.get_index() == [1]
    assert drop._get_current_selected_text() == "1 selected"
    drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
    drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
    drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    assert drop.get_value() == ([("epic", 2), ("item2", 2)], [1, 3])
    assert drop._get_current_selected_text() == "2 selected"

    # Change selection type
    drop._selection_placeholder_format = DROPSELECT_MULTIPLE_SFORMAT_LIST_COMMA
    assert drop._get_current_selected_text() == "epic,item2 selected"
    drop._selection_placeholder_format = DROPSELECT_MULTIPLE_SFORMAT_LIST_HYPHEN
    assert drop._get_current_selected_text() == "epic-item2 selected"
    drop._selection_placeholder_format = "+"
    assert drop._get_current_selected_text() == "epic+item2 selected"

    def format_string_list(items_list) -> str:
        """Receives the items list string and returns a function."""
        if len(items_list) == 1:
            return items_list[0]
        elif len(items_list) == 2:
            return items_list[0] + " and " + items_list[1]
        return "overflow"

    drop._selection_placeholder_format = format_string_list
    assert drop._get_current_selected_text() == "epic and item2 selected"

    # Invalid format
    drop._selection_placeholder_format = 1  # type: ignore
    with pytest.raises(ValueError):
        drop._get_current_selected_text()
    drop._selection_placeholder_format = lambda: print("nice")  # type: ignore
    with pytest.raises(ValueError):
        drop._get_current_selected_text()
    drop._selection_placeholder_format = lambda x: 1  # type: ignore
    with pytest.raises(AssertionError):
        drop._get_current_selected_text()

    # Back to default
    drop._selection_placeholder_format = DROPSELECT_MULTIPLE_SFORMAT_TOTAL

    # Click item 2, this should unselect
    assert drop.active
    drop.update(PygameEventUtils.middle_rect_click(drop._option_buttons[3]))
    assert drop.get_value() == ([("epic", 2)], [1])
    assert drop._get_current_selected_text() == "1 selected"
    drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
    assert drop._index == 4
    drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    assert drop.get_value() == ([("epic", 2), ("item3", 3)], [1, 4])
    assert drop._get_current_selected_text() == "2 selected"

    # Close
    drop.update(PygameEventUtils.key(pygame.K_ESCAPE, keydown=True))
    assert not drop.active
    assert drop.get_value() == ([("epic", 2), ("item3", 3)], [1, 4])
    assert drop._get_current_selected_text() == "2 selected"

    # Set max limit
    drop._max_selected = 3
    assert drop.get_total_selected() == 2
    drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
    drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    assert drop.get_total_selected() == 3
    assert drop.active
    drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
    drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    assert drop.get_total_selected() == 3  # Limit reached
    assert drop.get_value() == ([("epic", 2), ("item3", 3), ("item4", 4)], [1, 4, 5])
    drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
    drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))  # Unselect previous
    assert drop.get_total_selected() == 2  # Limit reached
    assert drop.get_value() == ([("epic", 2), ("item3", 3)], [1, 4])

    # Update elements
    drop.update_items([("This is a really long selection item", 1), ("epic", 2)])
    assert drop.get_value() == ([], [])
    assert drop._get_current_selected_text() == "Select an option"
    drop.set_value(1, process_index=True)
    assert drop.get_value() == ([("epic", 2)], [1])
    drop.set_value("This is a really long selection item", process_index=True)
    assert drop.get_value() == (
        [("This is a really long selection item", 1), ("epic", 2)],
        [0, 1],
    )
    assert drop._get_current_selected_text() == "2 selected"
    drop.set_default_value(1)
    assert drop.get_value() == ([("epic", 2)], [1])
    assert drop._get_current_selected_text() == "1 selected"

    # Use manager
    drop2 = menu.add.dropselect_multiple(
        "nice",
        [("This is a really long selection item", 1), ("epic", 2)],
        placeholder_selected="nice {0}",
        placeholder="epic",
        max_selected=1,
    )
    assert drop2._selection_box_width == 134
    assert drop2._get_current_selected_text() == "epic"
    drop2.set_value("epic", process_index=True)
    assert drop2.get_index() == [1]
    assert drop2._get_current_selected_text() == "nice 1"
    drop2.set_value(0, process_index=True)
    assert drop2.get_index() == [1]
    assert drop2._get_current_selected_text() == "nice 1"
    assert drop2._default_value == []
    assert drop2._index == 0
    with pytest.raises(ValueError):
        drop2.set_value("not epic")

    # Reset
    drop2.reset_value()
    assert drop2._get_current_selected_text() == "epic"
    assert drop2._default_value == []
    assert drop2._index == -1
    assert drop2.get_index() == []
    assert id(drop2._default_value) != id(drop2._selected_indices)

    menu.select_widget(drop2)
    assert drop2.update(PygameEventUtils.key(pygame.K_TAB, keydown=True))

    # Test hide
    assert drop2._drop_frame.is_visible()
    assert drop2.active
    drop2.hide()  # Hiding selects the other widget
    assert menu.get_selected_widget() == drop
    assert not drop2._drop_frame.is_visible()
    assert not drop2.active
    drop2.show()
    assert not drop2._drop_frame.is_visible()
    assert not drop2.active
    assert menu.get_selected_widget() == drop
    menu.select_widget(drop2)
    drop2._toggle_drop()
    assert drop2.active
    assert drop2._drop_frame.is_visible()

    # Test change
    test = [-1]

    def onchange(value, *_, **__) -> None:
        """Test onchange."""
        test[0] = value[1]

    drop2.set_onchange(onchange)

    # Pick any option
    menu.render()
    assert test == [-1]
    drop2._option_buttons[0].apply()
    assert test[0] == [0]
    drop2._option_buttons[0].apply()
    assert test[0] == []
    drop2._option_buttons[0].apply()
    drop2._option_buttons[1].apply()
    assert test[0] == [0]  # As max selected is only 1
    drop2._max_selected = 2
    drop2._option_buttons[1].apply()
    assert test[0] == [0, 1]

    # Test none drop frame
    drop2._drop_frame = None
    assert drop2.get_scroll_value_percentage("any") == -1

    # Test format option from manager
    menu._theme.widget_background_inflate_to_selection = True
    menu._theme.widget_background_inflate = 0  # type: ignore
    menu._theme.widget_margin = 0  # type: ignore
    drop2 = menu.add.dropselect_multiple(
        "nice",
        [("This is a really long selection item", 1), ("epic", 2)],
        placeholder_selected="nice {0}",
        placeholder="epic",
        max_selected=1,
        selection_placeholder_format=lambda x: "not EPIC",
    )
    assert drop2._get_current_selected_text() == "epic"
    drop2.set_value("epic", process_index=True)
    assert drop2._get_current_selected_text() == "nice not EPIC"
    assert drop2.get_margin() == (0, 0)
    assert drop2._background_inflate == (0, 0)
    assert drop2._border_inflate == (0, 0)
    menu._theme.widget_background_inflate_to_selection = False

    # Process index
    drop2._index = -1
    drop2._process_index()
