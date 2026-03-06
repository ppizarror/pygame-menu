"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - TEXTINPUT
Test TextInput and ColorInput widgets.
"""

import pygame
import pytest

import pygame_menu
import pygame_menu.controls as ctrl
from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented
from test._utils import (
    TEST_THEME,
    MenuUtils,
    PygameEventUtils,
    sleep,
    surface,
)


def assert_color(widget, r, g, b):
    """Utility to assert widget color value."""
    assert widget.get_value() == (r, g, b)


def assert_invalid_color(widget):
    """Utility to assert widget color is in invalid state (-1, -1, -1)."""
    assert widget.get_value() == (-1, -1, -1)


def test_textinput_basic_behavior():
    """
    Test basic TextInput widget functionality and constraints.
    """
    menu = MenuUtils.generic_menu()

    # Assert bad settings using pytest.raises
    with pytest.raises(ValueError):
        menu.add.text_input(
            "title", input_type=pygame_menu.locals.INPUT_FLOAT, default="bad"
        )

    with pytest.raises(ValueError):  # Default and password cannot coexist
        menu.add.text_input("title", password=True, default="bad")

    # Create text input widget
    textinput = menu.add.text_input("title", input_underline="_")
    textinput.set_value("new_value")
    textinput._selected = False
    textinput.draw(surface)

    textinput.select(update_menu=True)
    textinput.draw(surface)

    assert textinput.get_value() == "new_value"
    textinput.clear()
    assert textinput.get_value() == ""


def test_textinput_selection_and_events():
    """
    Test selection box logic and event handling.
    """
    menu = MenuUtils.generic_menu()
    textinput = menu.add.text_input("title")

    string = "the text"
    textinput._cursor_render = True
    textinput.set_value(string)
    textinput._select_all()

    assert textinput._get_selected_text() == "the text"
    textinput.draw(surface)
    textinput._unselect_text()

    # Simulate typing 'test'
    textinput.clear()
    for char in "test":
        key_code = getattr(pygame, f"K_{char}")
        textinput.update(PygameEventUtils.key(key_code, keydown=True, char=char))

    assert textinput.get_value() == "test"


def test_textinput_undo_redo_logic():
    """
    Test undo/redo and clipboard operations.
    """
    menu = MenuUtils.generic_menu()
    textinput = menu.add.text_input("title", maxchar=20)

    # Test maxchar cropping
    textinput.set_value("the size of this textinput is way greater than the limit")
    assert textinput.get_value() == "eater than the limit"

    # Undo/Redo
    textinput._undo()
    assert textinput.get_value() == ""
    textinput._redo()
    assert textinput.get_value() == "eater than the limit"


def test_textinput_unicode_conversions():
    """
    Test Alt+X Unicode conversion support.
    """
    menu = MenuUtils.generic_menu()
    textinput = menu.add.text_input("title")

    # Convert '215' to Unicode (ȕ) via Alt+X simulation
    textinput.set_value("tk 215")
    textinput.update(PygameEventUtils.keydown_mod_alt(pygame.K_x))
    assert textinput.get_value() == "tkȕ"


def test_textinput_readonly_and_active_states():
    """
    Test readonly locks and focus states.
    """
    menu = MenuUtils.generic_menu()
    textinput = menu.add.text_input("title")
    textinput.set_value("tk")

    textinput.readonly = True
    textinput.update(PygameEventUtils.key(pygame.K_t, keydown=True, char="k"))
    assert textinput.get_value() == "tk"  # Should not change

    textinput.readonly = False
    textinput.active = True
    # Moving up/down or Esc should deactivate the widget
    textinput.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
    assert not textinput.active


@pytest.mark.parametrize(
    "invalid_size",
    [
        (1, 0),
        (-1, -1),
        (1, 1, 0),
        [1, 1],  # Must be tuple
        (1.6, 2.5),
    ],
)
def test_textinput_invalid_cursor_sizes(invalid_size):
    """
    Parametrized test for cursor size validation.
    """
    menu = MenuUtils.generic_menu()
    with pytest.raises(AssertionError):
        menu.add.text_input("title", cursor_size=invalid_size)


def test_textinput_transformation_exceptions():
    """
    Verify that certain transformations are explicitly not implemented.
    """
    menu = MenuUtils.generic_menu()
    textinput = menu.add.text_input("title", maxwidth=10)

    with pytest.raises(WidgetTransformationNotImplemented):
        textinput.resize()
    with pytest.raises(WidgetTransformationNotImplemented):
        textinput.scale()


def test_password_constraints():
    """
    Test password-specific behaviors.
    """
    menu = MenuUtils.generic_menu()
    password_input = menu.add.text_input("title", password=True)

    # Password values usually cannot be set programmatically to non-empty strings
    with pytest.raises(ValueError):
        password_input.set_value("new_value")

    password_input.set_value("")  # Should be allowed
    assert password_input.get_value() == ""


def test_colorinput_rgb_basics():
    """Test ColorInput with RGB type and separator constraints."""
    menu = MenuUtils.generic_menu(theme=TEST_THEME.copy())

    # Base RGB setup
    widget = menu.add.color_input("title", color_type="rgb", input_separator=",")
    widget.set_value((123, 234, 55))
    assert_color(widget, 123, 234, 55)

    # Invalid value types/ranges
    with pytest.raises(AssertionError):
        widget.set_value("0,0,0")  # Must be tuple
    with pytest.raises(AssertionError):
        widget.set_value((255, 0))  # Missing channel
    with pytest.raises(AssertionError):
        widget.set_value((255, 255, -255))  # Out of range


@pytest.mark.parametrize("invalid_sep", ["", "  ", "unknown", "1", "5", "9"])
def test_colorinput_invalid_configs(invalid_sep):
    """Test invalid separators and color types."""
    menu = MenuUtils.generic_menu()

    if invalid_sep == "unknown":
        with pytest.raises(AssertionError):
            menu.add.color_input("title", color_type="unknown")
    else:
        with pytest.raises(AssertionError):
            menu.add.color_input("title", color_type="rgb", input_separator=invalid_sep)


def test_colorinput_automatic_formatting():
    """Test that commas and zeros are handled correctly during typing."""
    menu = MenuUtils.generic_menu()
    widget = menu.add.color_input("color", color_type="rgb", input_separator=",")

    # Sequence: Type '2', '5', ',' -> '25,'
    widget.update(PygameEventUtils.key(pygame.K_2, keydown=True, char="2"))
    widget.update(PygameEventUtils.key(pygame.K_5, keydown=True, char="5"))
    widget.update(PygameEventUtils.key(pygame.K_COMMA, keydown=True, char=","))
    assert widget._input_string == "25,"

    # Type '0' -> should trigger auto-separator logic '25,0,'
    widget.update(PygameEventUtils.key(pygame.K_0, keydown=True, char="0"))
    assert widget._input_string == "25,0,"
    assert_invalid_color(widget)

    # Test max value constraint (typing '5' to make '2555' should fail)
    widget._cursor_position = 2  # after '25'
    widget.update(PygameEventUtils.key(pygame.K_5, keydown=True, char="5"))
    assert widget._input_string.startswith("255")

    widget.update(PygameEventUtils.key(pygame.K_5, keydown=True, char="5"))
    assert widget._input_string == "255,0,"  # Still 255 because 2555 is invalid


def test_colorinput_hex_behavior():
    """Test Hex color input specifically."""
    menu = MenuUtils.generic_menu()
    widget = menu.add.color_input("title", color_type="hex")

    assert widget._input_string == "#"
    assert widget._cursor_position == 1

    # Set valid hex
    widget.set_value("FF00FF")
    assert_color(widget, 255, 0, 255)

    # Hex formatting (Upper/Lower)
    widget_upper = menu.add.color_input("title", color_type="hex", hex_format="upper")
    widget_upper.set_value("aabbcc")
    assert widget_upper.get_value(as_string=True) == "#AABBCC"


def test_widget_value_tracking():
    """Test value_changed and reset_value logic for Text and Color inputs."""
    menu = MenuUtils.generic_menu()

    # Track changes via a list (mocking a nonlocal reference)
    callback_data = {"val": None}

    def on_change(m, w):
        callback_data["val"] = w.get_value()

    menu.set_onwidgetchange(on_change)

    # Text Input Logic
    text = menu.add.text_input("title", default="initial")
    assert not text.value_changed()

    text.set_value("changed")
    assert text.get_value() == "changed"
    assert text.value_changed()

    text.reset_value()
    assert text.get_value() == "initial"
    assert not text.value_changed()

    # Color Input Logic
    color = menu.add.color_input("title", color_type="hex", default="#ff0000")
    assert_color(color, 255, 0, 0)
    color.set_value("#000000")
    assert color.value_changed()
    color.change()  # Trigger callback
    assert callback_data["val"] == (0, 0, 0)


def test_keyrepeat_functionality():
    """Test that repeat_keys accurately simulates multiple inputs over time."""
    menu = MenuUtils.generic_menu(keyboard_ignore_nonphysical=False)
    event = PygameEventUtils.key(pygame.K_a, keydown=True, char="a")

    text_on = menu.add.text_input("On", repeat_keys=True)
    text_off = menu.add.text_input("Off", repeat_keys=False)

    text_on.update(event)
    text_off.update(event)

    # Simulate time passing
    for _ in range(3):
        sleep(0.2)
        text_on.update([])
        text_off.update([])

    assert len(text_on.get_value()) > 1
    assert len(text_off.get_value()) == 1


def test_empty_title_sizing():
    """Ensure widgets with no titles still occupy minimum space."""
    menu = MenuUtils.generic_menu()
    text = menu.add.text_input("")
    width, height = text.get_size()
    assert width > 0
    assert height > 0


def test_textinput_mouse_and_touch_interactions():
    """Test mouse click, cursor repositioning, and touch behavior."""
    menu = MenuUtils.generic_menu()
    textinput = menu.add.text_input("title")
    textinput.set_value("testing")
    textinput._selected = True
    textinput._selection_time = 0

    # Middle click should show cursor
    textinput.update(PygameEventUtils.middle_rect_click(textinput))
    assert textinput._cursor_visible

    # Select all, then click → cursor moves but selection remains active
    textinput._select_all()
    assert textinput._selection_box == [0, len("testing")]

    textinput.update(
        PygameEventUtils.middle_rect_click(textinput, evtype=pygame.MOUSEBUTTONDOWN)
    )

    # Correct behavior:
    # - selection remains active
    # - selection box unchanged
    # - cursor moves to click position (end of text)
    assert textinput._selection_active
    assert textinput._selection_box == [0, len("testing")]
    assert textinput._cursor_position == len("testing")

    # Touch input should also reposition cursor
    textinput._cursor_position = 0
    pos = PygameEventUtils.middle_rect_click(textinput)[0].pos
    textinput._check_touch_collide_input(pos)
    assert textinput._cursor_position > 0


def test_textinput_selection_arrows_and_delete():
    """Test arrow movement while selection is active."""
    menu = MenuUtils.generic_menu()
    textinput = menu.add.text_input("title")
    textinput.set_value("hello")

    textinput._select_all()
    assert textinput._selection_surface is not None

    # LEFT arrow collapses selection to start
    textinput.update(PygameEventUtils.key(pygame.K_LEFT, keydown=True))
    assert textinput._selection_surface is None

    # Re-select and test DELETE
    textinput._select_all()
    textinput.update(PygameEventUtils.key(pygame.K_DELETE, keydown=True))
    assert textinput.get_value() == ""


def test_textinput_overflow_renderbox_behavior():
    """Test right-overflow trimming and renderbox updates."""
    menu = MenuUtils.generic_menu()
    menu._copy_theme()
    menu._theme.widget_font_size = 20

    textinput = menu.add.text_input("Some long text:", maxwidth=19, input_underline="_")

    # Overflow should push renderbox window
    textinput.set_value("a" * 26)
    assert textinput._cursor_position == 26
    assert textinput._renderbox == [1, 26, 25]

    # Backspace should shift window left
    textinput.update(PygameEventUtils.key(pygame.K_BACKSPACE, keydown=True))
    assert textinput._renderbox == [0, 25, 25]


def test_textinput_underline_recalculation():
    """Test underline string resizing logic."""
    theme = TEST_THEME.copy()
    theme.widget_selection_effect = None
    theme.title_font_size = 35
    theme.widget_font_size = 25

    menu = pygame_menu.Menu(
        width=400,
        height=300,
        title="Label",
        theme=theme,
        onclose=pygame_menu.events.CLOSE,
    )

    textinput = menu.add.text_input("title", input_underline="_")
    menu.render()

    # Changing title should expand underline
    textinput.set_title("nice")
    menu.render()
    assert len(textinput._current_underline_string) > 0

    # Long value should expand underline further
    textinput.set_value("Q" * 35)
    menu.render()
    assert len(textinput._current_underline_string) > 40


def test_textinput_frame_packing_and_column_constraints():
    """Test column width constraints and frame packing behavior."""
    theme = TEST_THEME.copy()
    menu = pygame_menu.Menu(
        width=400,
        height=300,
        title="Label",
        theme=theme,
        column_max_width=200,
        onclose=pygame_menu.events.CLOSE,
    )

    # Invalid frame sizes
    with pytest.raises(pygame_menu.menu._MenuSizingException):
        menu.add.frame_v(300, 100)
    with pytest.raises(pygame_menu.menu._MenuSizingException):
        menu.add.frame_v(201, 100)

    textinput = menu.add.text_input("title", input_underline="_")
    assert textinput.get_width() <= 200
    assert textinput.get_width() > 0

    v_frame = menu.add.frame_v(150, 100, background_color=(20, 20, 20))
    v_frame.pack(textinput)
    assert textinput.get_width() < 200


def test_colorinput_copy_paste_exceptions():
    """Test clipboard exception handling for ColorInput."""
    import pygame_menu.widgets.widget.textinput as tinput

    menu = MenuUtils.generic_menu()
    widget = menu.add.color_input("title", color_type="rgb")

    def invalid_clipboard(*args):
        raise tinput.PyperclipException("test")

    original_copy = tinput.clipboard_copy
    tinput.clipboard_copy = invalid_clipboard
    assert not widget._copy()
    tinput.clipboard_copy = original_copy

    original_paste = tinput.clipboard_paste
    tinput.clipboard_paste = invalid_clipboard
    assert not widget._paste()
    tinput.clipboard_paste = original_paste


def test_multiple_selected_widgets_exception():
    """Ensure selecting multiple text inputs raises the correct exception."""
    menu = MenuUtils.generic_menu()
    menu.add.text_input("A", password=True).select()
    menu.add.text_input("B").select()

    with pytest.raises(pygame_menu.menu._MenuMultipleSelectedWidgetsException):
        menu.draw(surface)


def test_menu_clear_and_widget_reassignment():
    """Test widget removal stats and reattachment behavior."""
    menu = MenuUtils.generic_menu()
    textinput = menu.add.text_input("title")

    assert textinput.get_menu() is menu
    menu.clear()
    assert textinput.get_menu() is None
    assert menu._stats.removed_widgets > 0

    # Reattach
    menu.add.generic_widget(textinput)
    assert textinput.get_menu() is menu

    menu.clear()
    assert menu._stats.removed_widgets > 1
