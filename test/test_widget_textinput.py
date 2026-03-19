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
    PYGAME_V2,
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
    """Test basic TextInput widget functionality and constraints."""
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
    """Test selection box logic and event handling."""
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
    """Test undo/redo and clipboard operations."""
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
    """Test Alt+X Unicode conversion support."""
    menu = MenuUtils.generic_menu()
    textinput = menu.add.text_input("title")

    # Convert '215' to Unicode (ȕ) via Alt+X simulation
    textinput.set_value("tk 215")
    textinput.update(PygameEventUtils.keydown_mod_alt(pygame.K_x))
    assert textinput.get_value() == "tkȕ"


def test_textinput_readonly_and_active_states():
    """Test readonly locks and focus states."""
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
    """Parametrized test for cursor size validation."""
    menu = MenuUtils.generic_menu()
    with pytest.raises(AssertionError):
        menu.add.text_input("title", cursor_size=invalid_size)  # type: ignore


def test_textinput_transformation_exceptions():
    """Verify that certain transformations are explicitly not implemented."""
    menu = MenuUtils.generic_menu()
    textinput = menu.add.text_input("title", maxwidth=10)

    with pytest.raises(WidgetTransformationNotImplemented):
        textinput.resize()
    with pytest.raises(WidgetTransformationNotImplemented):
        textinput.scale()


def test_password_constraints():
    """Test password-specific behaviors."""
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
        widget.set_value((255, 0))  # type: ignore
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

    def on_change(_, w):
        """Callback when a change is made."""
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

    def invalid_clipboard(*_):
        """Incorrect clipboard handling."""
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


def test_colorinput():
    """Test ColorInput widget."""

    def _assert_invalid_color(widg) -> None:
        """Assert that the widget color is invalid."""
        r, g, b = widg.get_value()
        assert r == -1
        assert g == -1
        assert b == -1

    def _assert_color(widg, cr, cg, cb) -> None:
        """Assert widget RGB channels."""
        r, g, b = widg.get_value()
        assert r == cr
        assert g == cg
        assert b == cb

    menu = MenuUtils.generic_menu(theme=TEST_THEME.copy())

    # Base rgb
    widget = menu.add.color_input("title", color_type="rgb", input_separator=",")
    widget.set_value((123, 234, 55))
    with pytest.raises(AssertionError):
        widget.set_value("0,0,0")
    with pytest.raises(AssertionError):
        widget.set_value((255, 0,))  # type: ignore
    with pytest.raises(AssertionError):
        widget.set_value((255, 255, -255))
    _assert_color(widget, 123, 234, 55)

    # Test separator
    widget = menu.add.color_input("color", color_type="rgb", input_separator="+")
    widget.set_value((34, 12, 12))
    assert widget._input_string == "34+12+12"
    with pytest.raises(AssertionError):
        menu.add.color_input("title", color_type="rgb", input_separator="")
    with pytest.raises(AssertionError):
        menu.add.color_input("title", color_type="rgb", input_separator="  ")
    with pytest.raises(AssertionError):
        menu.add.color_input("title", color_type="unknown")
    for i in range(10):
        with pytest.raises(AssertionError):
            menu.add.color_input("title", color_type="rgb", input_separator=str(i))

    # Empty rgb
    widget = menu.add.color_input("color", color_type="rgb", input_separator=",")

    PygameEventUtils.test_widget_key_press(widget)
    assert widget._cursor_position == 0
    widget.update(PygameEventUtils.key(pygame.K_RIGHT, keydown=True))
    assert widget._cursor_position == 0
    _assert_invalid_color(widget)

    # Write sequence: 2 -> 25 -> 25, -> 25,0,
    # The comma after the zero must be automatically set
    assert not widget.update(PygameEventUtils.key(0, keydown=True, testmode=False))
    widget.update(PygameEventUtils.key(pygame.K_2, keydown=True, char="2"))
    widget.update(PygameEventUtils.key(pygame.K_5, keydown=True, char="5"))
    widget.update(PygameEventUtils.key(pygame.K_COMMA, keydown=True, char=","))
    assert widget._input_string == "25,"
    widget.update(PygameEventUtils.key(pygame.K_0, keydown=True, char="0"))
    assert widget._input_string == "25,0,"
    _assert_invalid_color(widget)

    # Now, sequence: 25,0,c -> 25c,0, with cursor c
    widget.update(PygameEventUtils.key(pygame.K_LEFT, keydown=True))
    widget.update(PygameEventUtils.key(pygame.K_LEFT, keydown=True))
    widget.update(PygameEventUtils.key(pygame.K_LEFT, keydown=True))
    assert widget._cursor_position == 2

    # Sequence. 25,0, -> 255,0, -> 255,0, trying to write another 5 in the same position
    # That should be canceled because 2555 > 255
    widget.update(PygameEventUtils.key(pygame.K_5, keydown=True, char="5"))
    assert widget._input_string == "255,0,"
    widget.update(PygameEventUtils.key(pygame.K_5, keydown=True, char="5"))
    assert widget._input_string == "255,0,"

    # Invalid left zeros, try to write 255,0, -> 255,00, but that should be disabled
    widget.update(PygameEventUtils.key(pygame.K_RIGHT, keydown=True))
    widget.update(PygameEventUtils.key(pygame.K_0, keydown=True, char="0"))
    assert widget._input_string == "255,0,"

    # Second comma cannot be deleted because there's a number between ,0,
    widget.update(PygameEventUtils.key(pygame.K_BACKSPACE, keydown=True))
    assert widget._input_string == "255,0,"
    widget.update(PygameEventUtils.key(pygame.K_LEFT, keydown=True))
    widget.update(PygameEventUtils.key(pygame.K_DELETE, keydown=True))
    assert widget._input_string == "255,0,"

    # Current cursor is at 255c,0,
    # Now right comma and 0 can be deleted
    widget.update(PygameEventUtils.key(pygame.K_END, keydown=True))
    widget.update(PygameEventUtils.key(pygame.K_BACKSPACE, keydown=True))
    widget.update(PygameEventUtils.key(pygame.K_BACKSPACE, keydown=True))
    assert widget._input_string == "255,"

    # Fill with zeros, then number with 2 consecutive 0 types must be 255,0,0
    # Commas should be inserted automatically
    widget.readonly = True
    widget.update(PygameEventUtils.key(pygame.K_0, keydown=True, char="0"))
    assert widget._input_string == "255,"
    widget.readonly = False
    widget.update(PygameEventUtils.key(pygame.K_0, keydown=True, char="0"))
    widget.update(PygameEventUtils.key(pygame.K_0, keydown=True, char="0"))
    assert widget._input_string == "255,0,0"
    _assert_color(widget, 255, 0, 0)

    # At this state, user cannot add more zeros at right
    for _ in range(5):
        widget.update(PygameEventUtils.key(pygame.K_0, keydown=True, char="0"))
    assert widget._input_string == "255,0,0"
    widget.get_rect()

    widget.clear()
    assert widget._input_string == ""

    # Assert invalid defaults rgb
    with pytest.raises(AssertionError):
        menu.add.color_input("title", color_type="rgb", default=(255, 255,))  # type: ignore
    with pytest.raises(AssertionError):
        menu.add.color_input("title", color_type="rgb", default=(255, 255))  # type: ignore
    with pytest.raises(AssertionError):
        menu.add.color_input("title", color_type="rgb", default=(255, 255, 255, 255))  # type: ignore

    # Assert hex widget
    widget = menu.add.color_input("title", color_type="hex")
    assert widget._input_string == "#"
    assert widget._cursor_position == 1
    _assert_invalid_color(widget)
    with pytest.raises(AssertionError):
        widget.set_value("#FF")
    with pytest.raises(AssertionError):
        widget.set_value("#FFFFF<")
    with pytest.raises(AssertionError):
        widget.set_value("#FFFFF")
    with pytest.raises(AssertionError):
        widget.set_value("#F")
    with pytest.raises(AssertionError):
        widget.set_value("FFFFF")
    with pytest.raises(AssertionError):
        widget.set_value("F")
    widget.set_value("FF00FF")
    _assert_color(widget, 255, 0, 255)
    widget.set_value("#12FfAa")
    _assert_color(widget, 18, 255, 170)
    widget.set_value("   59C1e5")
    _assert_color(widget, 89, 193, 229)

    widget.render()
    widget.draw(surface)

    widget.clear()
    assert widget._input_string == "#"  # This cannot be empty
    assert widget._cursor_position == 1

    # In hex widget # cannot be deleted
    widget.update(PygameEventUtils.key(pygame.K_BACKSPACE, keydown=True))
    assert widget._cursor_position == 1
    widget.update(PygameEventUtils.key(pygame.K_LEFT, keydown=True))
    widget.update(PygameEventUtils.key(pygame.K_DELETE, keydown=True))
    assert widget._input_string == "#"
    widget.update(PygameEventUtils.key(pygame.K_END, keydown=True))
    for _ in range(10):
        widget.update(PygameEventUtils.key(pygame.K_f, keydown=True, char="f"))
    assert widget._input_string == "#ffffff"
    _assert_color(widget, 255, 255, 255)

    # Test hex formats
    widget = menu.add.color_input("title", color_type="hex", hex_format="none")
    widget.set_value("#ff00ff")
    assert not widget.update(PygameEventUtils.key(0, keydown=True, testmode=False))
    assert widget.get_value(as_string=True) == "#ff00ff"
    widget.set_value("#FF00ff")
    assert widget.get_value(as_string=True) == "#FF00ff"

    widget = menu.add.color_input("title", color_type="hex", hex_format="lower")
    widget.set_value("#FF00ff")
    assert widget.get_value(as_string=True) == "#ff00ff"
    widget.set_value("AABBcc")
    assert widget.get_value(as_string=True) == "#aabbcc"

    widget = menu.add.color_input("title", color_type="hex", hex_format="upper")
    widget.set_value("#FF00ff")
    assert widget.get_value(as_string=True) == "#FF00FF"
    widget.set_value("AABBcc")
    assert widget.get_value(as_string=True) == "#AABBCC"

    # Test dynamic sizing
    widget = menu.add.color_input("title", color_type="hex", hex_format="upper", dynamic_width=True)
    assert widget.get_width() == 200
    widget.set_value("#ffffff")
    width = 342 if PYGAME_V2 else 345
    assert widget.get_width() == width
    widget.set_value(None)
    assert widget.get_width() == 200
    assert widget.get_value(as_string=True) == "#"
    widget.set_value("#ffffff")
    assert widget.get_width() == width
    widget.update(
        PygameEventUtils.key(pygame.K_BACKSPACE, keydown=True)
    )  # remove the last character, now color is invalid
    assert widget.get_value(as_string=True) == "#FFFFF"  # is upper
    widget.render()
    assert widget.get_width() == 200

    widget = menu.add.color_input("title", color_type="hex", hex_format="upper", dynamic_width=False)
    assert widget.get_width() == width
    widget.set_value("#ffffff")
    assert widget.get_width() == width


def test_textinput_underline():
    """Test underline."""
    theme = TEST_THEME.copy()
    theme.widget_selection_effect = None
    theme.title_font_size = 35
    theme.widget_font_size = 25

    menu = pygame_menu.Menu(
        column_min_width=400,
        height=300,
        theme=theme,
        title="Label",
        onclose=pygame_menu.events.CLOSE,
        width=400,
    )
    textinput = menu.add.text_input("title", input_underline="_")
    assert menu._widget_offset[1] == (107 if PYGAME_V2 else 106)
    assert textinput.get_width() == 398
    assert textinput._current_underline_string == "________________________________"
    menu.render()
    assert (menu.get_width(widget=True), menu.get_width(inner=True)) == (398, 400)
    assert textinput.get_width() == 398
    assert textinput._current_underline_string == "________________________________"
    menu.render()
    assert (menu.get_width(widget=True), menu.get_width(inner=True)) == (398, 400)
    textinput.set_title("nice")
    assert textinput.get_width() == 401
    assert textinput._current_underline_string == "________________________________"
    menu.render()
    assert (menu.get_width(widget=True), menu.get_width(inner=True)) == (401, 400)
    textinput.set_value("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
    assert textinput.get_width() == 731
    assert textinput._current_underline_string == (
        "______________________________________________________________"
    )
    menu.render()
    assert (menu.get_width(widget=True), menu.get_width(inner=True)) == (731, 400)
    textinput.set_padding(100)
    assert textinput.get_width() == 931
    assert textinput._current_underline_string == (
        "______________________________________________________________"
    )
    menu.render()
    assert (menu.get_width(widget=True), menu.get_width(inner=True)) == (931, 380)
    textinput.set_padding(200)
    assert textinput.get_width() == 1131
    assert textinput._current_underline_string == (
        "______________________________________________________________"
    )
    menu.render()
    assert (menu.get_width(widget=True), menu.get_width(inner=True)) == (1131, 380)

    # Test underline
    textinput = menu.add.text_input("title: ")
    textinput.set_value("this is a test value")
    assert textinput.get_width() == 266

    menu.clear()
    textinput = menu.add.text_input("title: ", input_underline=".-")
    textinput.set_value("QQQQQQQQQQQQQQQ")
    assert textinput.get_width() == 403
    assert textinput._current_underline_string == (
        ".-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-"
    )

    textinput = menu.add.text_input("title: ", input_underline="_", input_underline_len=10)
    assert textinput._current_underline_string == "_" * 10

    # Text underline with different column widths
    menu = pygame_menu.Menu(
        column_max_width=200,
        height=300,
        theme=theme,
        title="Label",
        onclose=pygame_menu.events.CLOSE,
        width=400,
    )
    with pytest.raises(pygame_menu.menu._MenuSizingException):
        menu.add.frame_v(300, 100)
    with pytest.raises(pygame_menu.menu._MenuSizingException):
        menu.add.frame_v(201, 100)
    assert len(menu._widgets) == 0
    textinput = menu.add.text_input("title", input_underline="_")
    assert menu._widget_offset[1] == (107 if PYGAME_V2 else 106)
    assert textinput.get_width() == 200
    assert textinput._current_underline_string == "______________"
    v_frame = menu.add.frame_v(150, 100, background_color=(20, 20, 20))
    v_frame.pack(textinput)
    assert menu._widget_offset[1] == (76 if PYGAME_V2 else 75)
    assert textinput.get_width() == 145
    assert textinput._current_underline_string == "_________"

    # Test cursor size
    with pytest.raises(AssertionError):
        menu.add.text_input("title", cursor_size=(1, 0))
    with pytest.raises(AssertionError):
        menu.add.text_input("title", cursor_size=(-1, -1))
    with pytest.raises(AssertionError):
        menu.add.text_input("title", cursor_size=(1, 1, 0))  # type: ignore
    with pytest.raises(AssertionError):
        menu.add.text_input("title", cursor_size=[1, 1])  # type: ignore
    with pytest.raises(AssertionError):
        menu.add.text_input("title", cursor_size=(1.6, 2.5))  # type: ignore

    textinput_cursor = menu.add.text_input("title", cursor_size=(10, 2))
    assert textinput_cursor._cursor_size == (10, 2)


def test_overflow_removal():
    """Test text with max width and right overflow removal."""
    menu = MenuUtils.generic_menu()
    menu._copy_theme()
    menu._theme.widget_font_size = 20
    textinput = menu.add.text_input(
        "Some long text: ",
        maxwidth=19,
        textinput_id="long_text",
        input_underline="_",
    )
    with pytest.raises(WidgetTransformationNotImplemented):
        textinput.resize()
    with pytest.raises(WidgetTransformationNotImplemented):
        textinput.set_max_width()
    with pytest.raises(WidgetTransformationNotImplemented):
        textinput.set_max_height()
    with pytest.raises(WidgetTransformationNotImplemented):
        textinput.scale()
    with pytest.raises(WidgetTransformationNotImplemented):
        textinput.rotate()
    textinput.flip(True, True)
    assert textinput._flip == (False, True)
    textinput.set_value("aaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert textinput._cursor_position == 26
    assert textinput._renderbox == [1, 26, 25]
    textinput.update(PygameEventUtils.key(pygame.K_BACKSPACE, keydown=True))
    assert textinput._cursor_position == 25
    assert textinput._renderbox == [0, 25, 25]
    textinput.update(PygameEventUtils.key(pygame.K_a, keydown=True, char="a"))
    assert textinput._cursor_position == 26
    assert textinput._renderbox == [1, 26, 25]
    textinput.update(PygameEventUtils.key(pygame.K_BACKSPACE, keydown=True))
    assert textinput._cursor_position == 25
    assert textinput._renderbox == [0, 25, 25]


def test_copy_paste():
    """Test copy/paste."""
    menu = MenuUtils.generic_menu()

    # Test copy/paste
    textinput_nocopy = menu.add.text_input(
        "title",
        input_underline="_",
        maxwidth=20,
        copy_paste_enable=False,
    )
    textinput_nocopy.set_value("this cannot be copied")
    assert not textinput_nocopy._copy()
    assert not textinput_nocopy._paste()
    assert not textinput_nocopy._cut()
    assert textinput_nocopy.get_value() == "this cannot be copied"

    # Test copy/paste without block
    textinput_copy = menu.add.text_input(
        "title",
        input_underline="_",
        maxwidth=20,
        maxchar=20,
    )
    textinput_copy.set_value("this value should be cropped as this is longer than the max char")
    assert not textinput_copy._block_copy_paste
    textinput_copy._copy()
    if textinput_copy._block_copy_paste:  # Otherwise, an exception happened
        textinput_copy._block_copy_paste = False
    textinput_copy._select_all()
    textinput_copy._cut()
    assert textinput_copy.get_value() == ""
    textinput_copy._block_copy_paste = False
    textinput_copy._paste()
    textinput_copy._cut()
    textinput_copy._block_copy_paste = False
    textinput_copy._valid_chars = ["e", "r"]
    textinput_copy._paste()

    # Copy password
    textinput_copy._password = True
    assert not textinput_copy._copy()
    textinput_copy._password = False

    # Test copy/paste exception
    import pygame_menu.widgets.widget.textinput as tinput

    def invalid_clipboard(*args) -> None:
        """
        Tests invalid copying/pasting from clipboard.
        """
        raise tinput.PyperclipException(f"test: {args}")

    original_copy = tinput.clipboard_copy
    tinput.clipboard_copy = invalid_clipboard
    assert not textinput_copy._copy()
    tinput.clipboard_copy = original_copy

    original_paste = tinput.clipboard_paste
    tinput.clipboard_paste = invalid_clipboard
    assert not textinput_copy._paste()
    tinput.clipboard_paste = original_paste


def test_unicode():
    """Test unicode support."""
    menu = MenuUtils.generic_menu()
    textinput = menu.add.text_input("title", input_underline="_")
    textinput.set_value("tk")

    # Test alt+x
    textinput.update(PygameEventUtils.key(pygame.K_SPACE, keydown=True))
    textinput.update(PygameEventUtils.key(pygame.K_2, keydown=True, char="2"))
    textinput.update(PygameEventUtils.key(pygame.K_1, keydown=True, char="1"))
    textinput.update(PygameEventUtils.key(pygame.K_1, keydown=True, char="5"))
    assert textinput.get_value() == "tk 215"
    textinput.update(PygameEventUtils.keydown_mod_alt(pygame.K_x))  # convert 215 to unicode
    assert textinput.get_value() == "tkȕ"
    textinput.update(PygameEventUtils.key(pygame.K_SPACE, keydown=True))
    textinput.update(PygameEventUtils.key(pygame.K_SPACE, keydown=True))
    textinput.update(PygameEventUtils.key(pygame.K_b, keydown=True, char="B"))
    textinput.update(PygameEventUtils.key(pygame.K_1, keydown=True, char="1"))
    textinput.update(PygameEventUtils.keydown_mod_alt(pygame.K_x))  # convert 215 to unicode
    assert textinput.get_value() == "tkȕ ±"

    # Remove all
    textinput.clear()
    textinput.update(PygameEventUtils.key(pygame.K_b, keydown=True, char="B"))
    textinput.update(PygameEventUtils.key(pygame.K_1, keydown=True, char="1"))
    textinput.update(PygameEventUtils.keydown_mod_alt(pygame.K_x))  # convert 215 to unicode
    assert textinput.get_value() == "±"
    textinput.update(PygameEventUtils.keydown_mod_alt(pygame.K_x))  # convert same to unicode, do nothing
    assert textinput.get_value() == "±"

    # Test consecutive
    textinput.update(PygameEventUtils.key(pygame.K_2, keydown=True, char="2"))
    textinput.update(PygameEventUtils.key(pygame.K_0, keydown=True, char="0"))
    textinput.update(PygameEventUtils.key(pygame.K_1, keydown=True, char="1"))
    textinput.update(PygameEventUtils.key(pygame.K_3, keydown=True, char="3"))
    textinput.update(PygameEventUtils.keydown_mod_alt(pygame.K_x))  # convert 215 to unicode
    assert textinput.get_value() == "±–"

    # Test 0x
    textinput.clear()
    PygameEventUtils.release_key_mod()
    textinput.update(PygameEventUtils.key(pygame.K_0, keydown=True, char="0"))
    assert textinput.get_value() == "0"
    textinput.update(PygameEventUtils.key(pygame.K_x, keydown=True, char="x"))
    assert textinput.get_value() == "0x"
    textinput.update(PygameEventUtils.keydown_mod_alt(pygame.K_x))
    assert textinput.get_value() == "0x"
    textinput.update(PygameEventUtils.key(pygame.K_b, keydown=True, char="B"))
    textinput.update(PygameEventUtils.key(pygame.K_1, keydown=True, char="1"))
    assert textinput.get_value() == "0xB1"
    textinput.update(PygameEventUtils.keydown_mod_alt(pygame.K_x))
    assert textinput.get_value() == "±"
    PygameEventUtils.release_key_mod()

    textinput.update(PygameEventUtils.key(pygame.K_0, keydown=True, char="0"))
    textinput.update(PygameEventUtils.key(pygame.K_x, keydown=True, char="x"))
    textinput.update(PygameEventUtils.key(pygame.K_b, keydown=True, char="B"))
    textinput.update(PygameEventUtils.key(pygame.K_1, keydown=True, char="1"))
    textinput.update(PygameEventUtils.keydown_mod_alt(pygame.K_x))
    assert textinput.get_value() == "±±"

    # Test keyup
    assert pygame.K_1 in textinput._keyrepeat_counters.keys()
    assert not textinput.update(PygameEventUtils.key(pygame.K_1, keyup=True, char="1"))
    assert pygame.K_1 not in textinput._keyrepeat_counters.keys()

    # Test tab
    assert textinput._tab_size == 4
    textinput.update(PygameEventUtils.key(pygame.K_TAB, keydown=True))
    assert textinput.get_value() == "±±    "

    # Test invalid unicode
    assert not textinput.update(PygameEventUtils.key(pygame.K_1, keydown=True))

    # Test others
    textinput._input_type = "other"
    assert textinput._check_input_type("-")
    assert not textinput._check_input_type("x")
    textinput._maxwidth_update = None  # type: ignore
    assert textinput._update_maxlimit_renderbox() is None


def test_complex_textinput():
    """Test TextInput widget."""
    menu = MenuUtils.generic_menu()

    # Assert bad settings
    with pytest.raises(ValueError):
        menu.add.text_input("title",
                            input_type=pygame_menu.locals.INPUT_FLOAT,
                            default="bad")
    with pytest.raises(ValueError):  # Default and password cannot coexist
        menu.add.text_input("title",
                            password=True,
                            default="bad")

    # Create text input widget
    textinput = menu.add.text_input("title", input_underline="_")
    textinput.set_value("new_value")  # No error
    textinput._selected = False
    textinput.draw(surface)
    textinput.select(update_menu=True)
    textinput.draw(surface)
    assert textinput.get_value() == "new_value"
    textinput.clear()
    assert textinput.get_value() == ""

    # Create selection box
    string = "the text"
    textinput._cursor_render = True
    textinput.set_value(string)
    textinput._select_all()
    assert textinput._get_selected_text() == "the text"
    textinput.draw(surface)
    textinput._unselect_text()
    textinput.draw(surface)

    # Assert events
    textinput.update(PygameEventUtils.key(0, keydown=True, testmode=False))
    PygameEventUtils.test_widget_key_press(textinput)
    textinput.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    textinput.update(PygameEventUtils.key(pygame.K_LSHIFT, keydown=True))
    textinput.clear()

    # Type
    textinput.update(PygameEventUtils.key(pygame.K_t, keydown=True, char="t"))
    textinput.update(PygameEventUtils.key(pygame.K_e, keydown=True, char="e"))
    textinput.update(PygameEventUtils.key(pygame.K_s, keydown=True, char="s"))
    textinput.update(PygameEventUtils.key(pygame.K_t, keydown=True, char="t"))

    # Keyup
    textinput.update(PygameEventUtils.key(pygame.K_a, keyup=True, char="a"))
    assert textinput.get_value() == "test"  # The text we typed

    # Ctrl events
    textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_c))  # copy
    textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_v))  # paste
    textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_z))  # undo
    assert textinput.get_value() == "tes"
    textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_y))  # redo
    assert textinput.get_value() == "test"
    textinput._select_all()
    textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_x))  # cut
    assert textinput.get_value() == ""
    textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_z))  # undo
    assert textinput.get_value() == "test"
    textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_y))  # redo
    assert textinput.get_value() == ""
    textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_z))  # undo
    assert textinput.get_value() == "test"

    # Test ignore ctrl events
    textinput._copy_paste_enabled = False
    assert not textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_c))
    assert not textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_v))
    max_history = textinput._max_history
    textinput._max_history = 0
    assert not textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_z))
    assert not textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_y))
    assert not textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_x))
    textinput._selection_enabled = False
    assert not textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_a))
    assert not textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_r))  # invalid

    # Reset
    textinput._copy_paste_enabled = True
    textinput._max_history = max_history
    textinput._selection_enabled = True

    # Test selection, if user selects all and types anything the selected
    # text must be destroyed
    textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_a))  # select all
    textinput._unselect_text()
    assert textinput._get_selected_text() == ""
    textinput._select_all()
    assert textinput._get_selected_text() == "test"
    textinput._unselect_text()
    assert textinput._get_selected_text() == ""
    textinput.update(PygameEventUtils.keydown_mod_ctrl(pygame.K_a))
    assert textinput._get_selected_text() == "test"
    textinput.update(PygameEventUtils.key(pygame.K_t, keydown=True, char="t"))
    textinput._select_all()
    assert textinput.update(PygameEventUtils.key(pygame.K_ESCAPE, keydown=True))
    textinput._select_all()
    assert textinput.update(PygameEventUtils.key(pygame.K_BACKSPACE, keydown=True))
    assert textinput.get_value() == ""
    textinput.set_value("t")

    # Releasing shift disable selection
    textinput._selection_active = True
    textinput.update(PygameEventUtils.key(pygame.K_LSHIFT, keyup=True))
    assert not textinput._selection_active

    # Arrows while selection
    textinput._select_all()
    assert textinput._selection_surface is not None
    textinput.update(PygameEventUtils.key(pygame.K_LEFT, keydown=True))
    assert textinput._selection_surface is None
    textinput._select_all()
    assert textinput._selection_surface is not None
    textinput.update(PygameEventUtils.key(pygame.K_RIGHT, keydown=True))
    assert textinput._selection_surface is None

    textinput._select_all()
    textinput._selection_active = True
    assert textinput._selection_box == [0, 1]
    textinput.update(PygameEventUtils.key(pygame.K_LEFT, keydown=True))
    assert textinput._selection_box == [0, 0]
    textinput._select_all()
    textinput._selection_active = True
    textinput.update(PygameEventUtils.key(pygame.K_RIGHT, keydown=True))
    assert textinput._selection_box == [0, 1]

    # Remove while selection
    textinput._select_all()
    textinput.update(PygameEventUtils.key(pygame.K_DELETE, keydown=True))
    assert textinput.get_value() == ""
    textinput.set_value("t")

    # Now the value must be t
    assert textinput._get_selected_text() == ""
    assert textinput.get_value() == "t"

    # Test readonly
    textinput.update(PygameEventUtils.key(pygame.K_t, keydown=True, char="k"))
    assert textinput.get_value() == "tk"
    textinput.readonly = True
    textinput.update(PygameEventUtils.key(pygame.K_t, keydown=True, char="k"))
    assert textinput.get_value() == "tk"
    textinput.readonly = False

    # Test keyup
    assert pygame.K_t in textinput._keyrepeat_counters.keys()
    assert not textinput.update(
        PygameEventUtils.key(pygame.K_t, keyup=True, char="1"))
    assert pygame.K_t not in textinput._keyrepeat_counters.keys()

    # Test tab
    assert textinput._tab_size == 4
    textinput.update(PygameEventUtils.key(pygame.K_TAB, keydown=True))
    assert textinput.get_value() == "tk    "

    # Test invalid unicode
    assert not textinput.update(PygameEventUtils.key(pygame.K_1, keydown=True))

    # Up/Down disable active status
    textinput.active = True
    textinput.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
    assert not textinput.active
    textinput.active = True
    textinput.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
    assert not textinput.active
    textinput.active = True
    assert textinput.update(PygameEventUtils.key(pygame.K_ESCAPE, keydown=True))
    assert not textinput.active

    # Test mouse
    textinput._selected = True
    textinput._selection_time = 0
    textinput.update(PygameEventUtils.middle_rect_click(textinput))
    assert textinput._cursor_visible
    textinput._select_all()
    textinput._selection_active = True
    assert textinput._cursor_position == 6
    assert textinput._selection_box == [0, 6]
    textinput.update(PygameEventUtils.middle_rect_click(textinput, evtype=pygame.MOUSEBUTTONDOWN))
    assert textinput._selection_box == [0, 0]

    # Check click pos
    textinput._check_mouse_collide_input(PygameEventUtils.middle_rect_click(textinput)[0].pos)
    assert textinput._cursor_position == 6

    # Test touch
    textinput._cursor_position = 0
    textinput._check_touch_collide_input(PygameEventUtils.middle_rect_click(textinput)[0].pos)
    assert textinput._cursor_position == 6

    # Update mouse
    for i in range(50):
        textinput.update(PygameEventUtils.key(pygame.K_t, keydown=True, char="t"))
    textinput._update_cursor_mouse(50)
    textinput._cursor_render = True
    textinput._render_cursor()

    # Test multiple are selected
    menu.add.text_input("title", password=True, input_underline="_").select()
    with pytest.raises(pygame_menu.menu._MenuMultipleSelectedWidgetsException):
        menu.draw(surface)
    textinput.clear()
    textinput.select(update_menu=True)
    menu.draw(surface)

    # Clear the menu
    assert menu._stats.removed_widgets == 0
    assert textinput.get_menu() == menu
    menu.clear()
    assert textinput.get_menu() is None
    assert menu._stats.removed_widgets == 3
    menu.add.generic_widget(textinput)
    assert textinput.get_menu() == menu
    menu.clear()
    assert menu._stats.removed_widgets == 4


def test_undo_redo():
    """Test undo/redo."""
    menu = MenuUtils.generic_menu()

    # Test maxchar and undo/redo
    textinput = menu.add.text_input("title", input_underline="_", maxchar=20)
    textinput.set_value("the size of this textinput is way greater than the limit")
    assert textinput.get_value() == "eater than the limit"  # Same as maxchar
    assert textinput._cursor_position == 20
    textinput._undo()  # This must set default at ""
    assert textinput.get_value() == ""
    textinput._redo()
    assert textinput.get_value() == "eater than the limit"
    textinput.draw(surface)
    textinput._copy()
    textinput._paste()
    textinput._block_copy_paste = False
    textinput._select_all()
    textinput._cut()
    assert textinput.get_value() == ""
    textinput._undo()
    assert textinput.get_value() == "eater than the limit"

    assert textinput._history_index == 1
    textinput._history_index = 0
    assert not textinput._undo()
    textinput._history_index = len(textinput._history) - 1
    assert not textinput._redo()
