"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - DROPSELECTMULTIPLE
Test DropSelectMultiple widget.
"""

import pygame
import pytest

import pygame_menu
import pygame_menu.controls as ctrl
import pygame_menu.widgets.widget.dropselect_multiple as dropselect_module
from pygame_menu.widgets import (
    DROPSELECT_MULTIPLE_SFORMAT_LIST_COMMA,
    DROPSELECT_MULTIPLE_SFORMAT_LIST_HYPHEN,
    DROPSELECT_MULTIPLE_SFORMAT_TOTAL,
)
from test._utils import (
    THEME_NON_FIXED_TITLE,
    MenuUtils,
    PygameEventUtils,
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


def test_dropselect_multiple_selection_and_formatting(generic_menu, drop_items):
    """Test DropSelectMultiple selection and placeholder formatting modes."""
    menu = generic_menu
    drop = dropselect_module.DropSelectMultiple(
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


def test_dropselect_multiple():
    """Test dropselect multiple widget."""
    theme = pygame_menu.themes.THEME_DEFAULT.copy()
    theme.widget_font_size = 25
    menu = MenuUtils.generic_menu(mouse_motion_selection=True, theme=theme)
    items = [("This is a really long selection item", 1), ("epic", 2)]
    for i in range(10):
        items.append((f"item{i + 1}", i + 1))
    drop = dropselect_module.DropSelectMultiple(
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


def test_dropselect_multiple_init_assertions(drop_items):
    """Test that invalid initializations correctly trigger assertions."""
    # Test negative max_selected assertion
    with pytest.raises(AssertionError):
        dropselect_module.DropSelectMultiple("dropsel", drop_items, max_selected=-1)

    # Test out-of-bounds default index assertion
    with pytest.raises(AssertionError):
        dropselect_module.DropSelectMultiple("dropsel", drop_items, default=99)


def test_dropselect_multiple_box_height_bounds(drop_items):
    """Test selection box height factor bounds assertions."""
    # Height factor = 0 should fail assertion (0 < height <= 1)
    with pytest.raises(AssertionError):
        dropselect_module.DropSelectMultiple(
            "dropsel", drop_items, selection_option_selected_box_height=0
        )

    # Height factor > 1 should fail assertion
    with pytest.raises(AssertionError):
        dropselect_module.DropSelectMultiple(
            "dropsel", drop_items, selection_option_selected_box_height=1.5
        )


def test_dropselect_multiple_empty_items(generic_menu):
    """Test that dropselect multiple initialization with empty items raises an error."""
    with pytest.raises(AssertionError, match="item list cannot be empty"):
        dropselect_module.DropSelectMultiple(
            title="Empty:",
            items=[],
            default=None,
        )


def test_dropselect_multiple_custom_placeholder_formats(generic_menu, drop_items):
    """Test custom placeholder formatting functions through direct configuration."""
    custom_formatter = lambda items: " | ".join(items)
    drop = dropselect_module.DropSelectMultiple(
        title="Format Test:",
        items=drop_items,
        placeholder_selected="Chosen: {0}",
        selection_placeholder_format=custom_formatter,
    )
    generic_menu.add.generic_widget(drop, configure_defaults=True)
    assert drop._placeholder_selected == "Chosen: {0}"
    assert drop._selection_placeholder_format == custom_formatter


def test_dropselect_multiple_missing_id_defaults(generic_menu, drop_items):
    """Test that an automatic ID is generated when dropselect_id is omitted."""
    drop = dropselect_module.DropSelectMultiple(
        title="No ID:",
        items=drop_items,
    )
    generic_menu.add.generic_widget(drop, configure_defaults=True)
    # Verify that an auto-generated ID string is assigned instead of remaining blank
    assert isinstance(drop.get_id(), str)
    assert len(drop.get_id()) > 0
