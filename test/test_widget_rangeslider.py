"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - RANGE SLIDER
Test RangeSlider widget.
"""

import pygame
import pytest

import pygame_menu
import pygame_menu.controls as ctrl
from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented
from test._utils import MenuUtils, PygameEventUtils, sleep, surface


@pytest.fixture
def menu():
    """Provides a generic menu for testing."""
    return MenuUtils.generic_menu()


@pytest.fixture
def menu_no_ignore():
    """Menu with keyboard_ignore_nonphysical=False."""
    return MenuUtils.generic_menu(keyboard_ignore_nonphysical=False)


@pytest.fixture
def slider_single():
    """Provides a single-value RangeSlider."""
    return pygame_menu.widgets.RangeSlider("Range S", default_value=0.5)


@pytest.fixture
def slider_double():
    """Provides a double-value RangeSlider."""
    return pygame_menu.widgets.RangeSlider(
        "Range D", default_value=(0.2, 0.8), range_values=(0, 1), increment=0.1
    )


def test_single_rangeslider_basic_flow(menu, slider_single):
    test_state = {"change": 0, "return": 0}

    def onchange(x: float):
        test_state["change"] = x  # type: ignore

    def onreturn(x: float):
        test_state["return"] = x  # type: ignore

    slider_single.set_onchange(onchange)
    slider_single.set_onreturn(onreturn)
    menu.add.generic_widget(slider_single, True)

    # Initial value check
    assert slider_single.get_value() == 0.5
    assert slider_single._value == [0.5, 0]

    # LEFT navigation
    slider_single.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert pytest.approx(slider_single.get_value()) == 0.4
    assert test_state["change"] == pytest.approx(0.4)

    slider_single.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert pytest.approx(slider_single.get_value(), rel=1e-3) == 0.3

    # Move to 0
    for _ in range(10):
        slider_single.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert slider_single.get_value() == 0

    # RIGHT navigation
    assert slider_single.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert slider_single.get_value() == 0.1

    # Apply value
    assert test_state["return"] == 0
    slider_single.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    assert test_state["return"] == 0.1

    # Ignore invalid key (testmode=False)
    assert not slider_single.update(
        PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True, testmode=False)
    )


def test_single_rangeslider_readonly_and_internal_update(menu, slider_single):
    menu.add.generic_widget(slider_single, True)
    slider_single.set_value(0.5)
    slider_single.draw(surface)
    slider_single.draw_after_if_selected(surface)

    slider_single.readonly = True
    assert not slider_single.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert slider_single.get_value() == 0.5

    # Internal update should not change public value
    slider_single._update_value(0)
    assert slider_single.get_value() == 0.5

    slider_single.readonly = False


@pytest.mark.parametrize("invalid_val", [-1, [0.4, 0.5], "string"])
def test_invalid_value_exceptions(slider_single, invalid_val):
    with pytest.raises(AssertionError):
        slider_single.set_value(invalid_val)


def test_single_invalid_constructor_cases():
    with pytest.raises(AssertionError):
        pygame_menu.widgets.RangeSlider("Range S", default_value=2)
    with pytest.raises(AssertionError):
        pygame_menu.widgets.RangeSlider("Range S", default_value=1, range_values=[1, 0])
    with pytest.raises(AssertionError):
        pygame_menu.widgets.RangeSlider("Range S", default_value=1, range_values=[1, 1])
    with pytest.raises(AssertionError):
        pygame_menu.widgets.RangeSlider("Range S", default_value="a")  # type: ignore


def test_transformation_not_implemented(slider_single):
    transforms = [
        slider_single.rotate,
        slider_single.flip,
        slider_single.scale,
        slider_single.resize,
        slider_single.set_max_width,
        slider_single.set_max_height,
    ]
    for action in transforms:
        with pytest.raises(WidgetTransformationNotImplemented):
            action()


def test_single_mouse_click_and_extremes(menu, slider_single):
    menu.add.generic_widget(slider_single, True)
    slider_single.set_value(0.5)

    # Initial state
    assert not slider_single._selected_mouse

    # Click at 0.5 (middle rect click)
    pos = slider_single._test_get_pos_value(0.5)
    slider_single.update(
        PygameEventUtils.middle_rect_click(pos, evtype=pygame.MOUSEBUTTONDOWN)
    )
    assert slider_single.get_value() == 0.5
    assert slider_single._selected_mouse
    assert slider_single._scrolling

    # Release click at same pos
    slider_single.update(PygameEventUtils.middle_rect_click(pos))
    assert not slider_single._scrolling
    assert slider_single.get_value() == 0.5
    assert not slider_single._selected_mouse

    # Mouse click out of range (right)
    slider_single._selected_mouse = True
    pos = slider_single._test_get_pos_value(1, dx=100)
    slider_single.update(PygameEventUtils.middle_rect_click(pos))
    assert slider_single.get_value() == 0.5
    assert not slider_single._selected_mouse

    # Mouse click out of range (left)
    slider_single._selected_mouse = True
    pos = slider_single._test_get_pos_value(0, dx=-100)
    slider_single.update(PygameEventUtils.middle_rect_click(pos))
    assert slider_single.get_value() == 0.5
    assert not slider_single._selected_mouse

    # Extremes
    slider_single._selected_mouse = True
    pos = slider_single._test_get_pos_value(0)
    slider_single.update(PygameEventUtils.middle_rect_click(pos))
    assert slider_single.get_value() == 0

    slider_single._selected_mouse = True
    pos = slider_single._test_get_pos_value(1)
    slider_single.update(PygameEventUtils.middle_rect_click(pos))
    assert slider_single.get_value() == 1


def test_single_scroll_drag(menu, slider_single):
    menu.add.generic_widget(slider_single, True)
    slider_single.set_value(1)

    # Scroll to 0.5
    pos2 = slider_single._test_get_pos_value(0.5)
    assert not slider_single._scrolling
    slider_rect = slider_single._get_slider_inflate_rect(0, to_real_position=True)

    # Start scrolling
    slider_single.update(
        PygameEventUtils.middle_rect_click(slider_rect, evtype=pygame.MOUSEBUTTONDOWN)
    )
    assert slider_single._scrolling
    assert slider_single._selected_mouse

    # Move from 1 to 0.5
    pos = slider_single._test_get_pos_value(1)
    dx = pos[0] - pos2[0]
    slider_single.update(
        PygameEventUtils.mouse_motion(slider_rect, rel=(-dx, pos[1]), update_mouse=True)
    )
    assert slider_single.get_value() == pytest.approx(0.5)
    assert slider_single._scrolling

    # Release
    slider_single.update(PygameEventUtils.middle_rect_click(pos))
    assert not slider_single._scrolling


def test_single_ignore_tab_and_keyrepeat(menu, slider_single):
    menu.add.generic_widget(slider_single, True)
    slider_single.set_value(0.5)

    # Ignore TAB
    assert not slider_single.update(PygameEventUtils.key(ctrl.KEY_TAB, keydown=True))

    # Keyrepeat internal behavior
    slider_single.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert ctrl.KEY_RIGHT in slider_single._keyrepeat_counters
    assert slider_single.get_value() == 0.6  # moved by +0.1

    # Make RIGHT repeat
    slider_single._keyrepeat_counters[ctrl.KEY_RIGHT] += 1e4
    assert len(slider_single._events) == 0
    assert not slider_single.update([])
    assert len(slider_single._events) == 1
    assert not slider_single.update([])
    assert len(slider_single._events) == 0

    # Keyup removes counters
    slider_single.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keyup=True))
    assert ctrl.KEY_RIGHT not in slider_single._keyrepeat_counters


def test_single_range_box_single_slider(menu):
    slider_rb = pygame_menu.widgets.RangeSlider("Range", range_box_single_slider=True)
    menu.add.generic_widget(slider_rb, True)
    slider_rb.draw(surface)
    assert hasattr(slider_rb, "_range_box")
    assert slider_rb._range_box.get_width() == 0
    slider_rb.set_value(1)
    assert slider_rb._range_box.get_width() == 150


def test_single_discrete_logic(menu):
    rv = [0, 1, 2, 3, 4, 5]
    slider = pygame_menu.widgets.RangeSlider("Range", range_values=rv)
    menu.add.generic_widget(slider, True)

    # Invalid default values
    with pytest.raises(AssertionError):
        pygame_menu.widgets.RangeSlider("Range", default_value=0.5, range_values=rv)
    with pytest.raises(AssertionError):
        pygame_menu.widgets.RangeSlider("Range", default_value=-1, range_values=rv)

    # Invalid set_value
    with pytest.raises(AssertionError):
        slider.set_value(-1)
    with pytest.raises(AssertionError):
        slider.set_value([0, 1])
    with pytest.raises(AssertionError):
        slider.set_value((0, 1))

    # Key events
    assert not slider.update(PygameEventUtils.key(ctrl.KEY_TAB, keydown=True))
    slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert slider.get_value() == 1
    slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert slider.get_value() == 2
    slider._increment = 0
    slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert slider.get_value() == 3
    slider.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert slider.get_value() == 2
    slider.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert slider.get_value() == 1
    slider.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert slider.get_value() == 0
    slider.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert slider.get_value() == 0

    # Mouse click snapping
    slider._selected_mouse = True
    pos = slider._test_get_pos_value(2)
    slider.update(PygameEventUtils.middle_rect_click(pos))
    assert slider.get_value() == 2
    assert not slider._selected_mouse

    # Invalid click (far away)
    slider._selected_mouse = True
    pos = slider._test_get_pos_value(2, dx=1000)
    slider.update(PygameEventUtils.middle_rect_click(pos))
    assert slider.get_value() == 2
    assert not slider._selected_mouse

    # Scroll to 4
    pos = slider._test_get_pos_value(2)
    pos2 = slider._test_get_pos_value(4)
    assert not slider._scrolling
    slider_rect = slider._get_slider_inflate_rect(0, to_real_position=True)
    slider.update(
        PygameEventUtils.middle_rect_click(slider_rect, evtype=pygame.MOUSEBUTTONDOWN)
    )
    assert slider._scrolling
    assert slider._selected_mouse
    dx = pos[0] - pos2[0]
    slider.update(
        PygameEventUtils.mouse_motion(slider_rect, rel=(-dx, pos[1]), update_mouse=True)
    )
    assert slider.get_value() == 4
    assert slider._scrolling
    slider.update(PygameEventUtils.middle_rect_click(pos))
    assert not slider._scrolling

    # Back to 2
    slider.set_value(2)

    # Invalid scrolling if clicked outside slider
    slider.update(
        PygameEventUtils.middle_rect_click(
            slider._test_get_pos_value(0), evtype=pygame.MOUSEBUTTONDOWN
        )
    )
    assert not slider._scrolling


def test_double_slider_selection_cycling(slider_double):
    # Default: first handle selected
    assert slider_double._slider_selected[0] is True

    # Tab cycles selection
    assert slider_double.update(PygameEventUtils.key(ctrl.KEY_TAB, keydown=True))
    assert slider_double._slider_selected[0] is False
    assert slider_double._slider_selected[1] is True


def test_double_slider_overlap_constraints(slider_double):
    # Invalid values
    with pytest.raises(AssertionError):
        slider_double.set_value(0.2)
    with pytest.raises(AssertionError):
        slider_double.set_value((0.2, 0.2))
    with pytest.raises(AssertionError):
        slider_double.set_value((1.0, 0.2))
    with pytest.raises(AssertionError):
        slider_double.set_value((0.2, 0.5, 1.0))  # type: ignore

    # Overlap constraints
    with pytest.raises(AssertionError):
        slider_double.set_value((0.9, 0.2))
    with pytest.raises(AssertionError):
        slider_double.set_value((0.5, 0.5))


def test_double_slider_mouse_drag_and_limits(menu):
    slider = pygame_menu.widgets.RangeSlider(
        "Range",
        range_text_value_tick_number=3,
        default_value=(0.2, 1.0),
        slider_text_value_font=pygame_menu.font.FONT_BEBAS,
        range_text_value_font=pygame_menu.font.FONT_8BIT,
        slider_text_value_triangle=False,
    )
    slider._slider_text_value_vmargin = -2
    menu.add.generic_widget(slider, True)
    slider.draw(surface)
    slider.draw_after_if_selected(surface)

    assert slider.get_value() == (0.2, 1.0)

    # Slider selection via TAB
    assert slider._slider_selected[0]
    assert slider.update(PygameEventUtils.key(ctrl.KEY_TAB, keydown=True))
    assert not slider._slider_selected[0]
    slider.draw(surface)
    slider.draw_after_if_selected(surface)

    # Click sliders
    slider_rect = slider._get_slider_inflate_rect(0, to_real_position=True)
    assert slider.update(
        PygameEventUtils.middle_rect_click(slider_rect, evtype=pygame.MOUSEBUTTONDOWN)
    )
    assert slider._slider_selected[0]
    assert not slider.update(
        PygameEventUtils.middle_rect_click(slider_rect, evtype=pygame.MOUSEBUTTONDOWN)
    )

    # Click when sliders colliding
    slider.set_value((0.5, 0.50000001))
    slider_rect = slider._get_slider_inflate_rect(1, to_real_position=True)
    assert not slider.update(
        PygameEventUtils.middle_rect_click(slider_rect, evtype=pygame.MOUSEBUTTONDOWN)
    )
    assert slider._slider_selected[0]
    slider.set_value((0.5, 0.7))
    slider_rect = slider._get_slider_inflate_rect(1, to_real_position=True)
    assert slider.update(
        PygameEventUtils.middle_rect_click(slider_rect, evtype=pygame.MOUSEBUTTONDOWN)
    )
    assert slider._slider_selected[1]

    # Left slider drag
    pos = slider._test_get_pos_value(0.5)
    pos2 = slider._test_get_pos_value(0.6)
    slider_rect = slider._get_slider_inflate_rect(0, to_real_position=True)
    assert isinstance(slider_rect, pygame.Rect)
    slider.update(
        PygameEventUtils.middle_rect_click(slider_rect, evtype=pygame.MOUSEBUTTONDOWN)
    )
    assert slider._slider_selected[0]
    assert slider._scrolling
    assert slider._selected_mouse
    dx = pos[0] - pos2[0]
    slider.update(
        PygameEventUtils.mouse_motion(slider_rect, rel=(-dx, pos[1]), update_mouse=True)
    )
    assert slider.get_value() == (0.6, 0.7)

    # Ignore further motion if already moved
    slider.update(
        PygameEventUtils.mouse_motion(slider_rect, rel=(-dx, pos[1]), update_mouse=True)
    )
    assert slider.get_value() == (0.6, 0.7)
    assert slider._scrolling
    assert slider._slider_selected[0]

    # Move to 0
    pos = slider._test_get_pos_value(0)
    pos2 = slider._test_get_pos_value(0.6)
    dx = pos[0] - pos2[0]
    slider.update(
        PygameEventUtils.mouse_motion(slider_rect, rel=(dx, pos[1]), update_mouse=True)
    )
    assert slider.get_value() == (0, 0.7)

    # Move more than 0.7 (clamped)
    pos = slider._test_get_pos_value(0)
    pos2 = slider._test_get_pos_value(0.75)
    slider_rect = slider._get_slider_inflate_rect(0, to_real_position=True)
    dx = pos[0] - pos2[0]
    slider.update(
        PygameEventUtils.mouse_motion(slider_rect, rel=(-dx, pos[1]), update_mouse=True)
    )
    assert slider.get_value() == (0, 0.7)

    # Move to 0.7 - eps
    pos = slider._test_get_pos_value(0)
    pos2 = slider._test_get_pos_value(0.7 - 1e-6)
    slider_rect = slider._get_slider_inflate_rect(0, to_real_position=True)
    dx = pos[0] - pos2[0]
    slider.update(
        PygameEventUtils.mouse_motion(slider_rect, rel=(-dx, pos[1]), update_mouse=True)
    )
    assert pytest.approx(slider.get_value()[0], rel=1e-1) == 0.7 - 1e-7

    # Ignore if move 0.7 + eps
    assert not slider.update(
        PygameEventUtils.mouse_motion(slider_rect, rel=(1, pos[1]), update_mouse=True)
    )

    # Change to right slider
    slider_rect = slider._get_slider_inflate_rect(1, to_real_position=True)
    assert slider.update(PygameEventUtils.key(ctrl.KEY_TAB, keydown=True))
    pos = slider._test_get_pos_value(0.7)
    pos2 = slider._test_get_pos_value(0.8)
    dx = pos[0] - pos2[0]
    assert not slider.update(
        PygameEventUtils.mouse_motion(slider_rect, rel=(-1, pos[1]), update_mouse=True)
    )
    assert slider.update(
        PygameEventUtils.mouse_motion(slider_rect, rel=(-dx, pos[1]), update_mouse=True)
    )
    assert pytest.approx(slider.get_value()[1], rel=1e-2) == 0.8

    # Key left/right logic (mirroring original)
    slider.set_value((0.7, 0.8))
    slider.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    slider.set_value((0.7, 0.8))  # Ignored
    slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    slider.set_value((0.7, 0.9))
    slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    slider.set_value((0.7, 1.0))
    slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    slider.set_value((0.7, 1.0))
    slider.set_value((0.7, 0.8))
    slider.update(PygameEventUtils.key(ctrl.KEY_TAB, keydown=True))
    slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    slider.set_value((0.7, 0.8))
    slider.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    slider.set_value((0.6, 0.8))

    # Reset value
    slider.reset_value()
    assert slider.get_value() == (0.2, 1.0)


def test_double_discrete(menu):
    rv = [0, 1, 2, 3, 4, 5]
    slider = menu.add.range_slider("Range", (1, 4), rv, range_text_value_tick_number=3)
    slider.draw(surface)

    # Set values
    slider.set_value([1, 2])
    assert slider.get_value() == (1, 2)

    # Invalid values
    with pytest.raises(AssertionError):
        slider.set_value((1.1, 2.2))
    with pytest.raises(AssertionError):
        slider.set_value((1, 1))
    with pytest.raises(AssertionError):
        slider.set_value((2, 1))
    with pytest.raises(AssertionError):
        slider.set_value(1)

    # Left/right
    assert slider.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert slider.get_value() == (0, 2)
    assert not slider.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert slider.get_value() == (0, 2)
    assert slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert slider.get_value() == (1, 2)
    assert not slider.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert slider.get_value() == (1, 2)

    slider._update_value(0.99)
    assert slider.get_value() == (1, 2)

    rect = slider._get_slider_inflate_rect(0, to_absolute_position=True)

    # Width/height must match exactly
    assert rect.size == (15, 28)

    # Position must be *close* to expected, but not pixel-perfect
    assert abs(rect.x - 301) <= 4
    assert abs(rect.y - 209) <= 4


def test_kwargs_from_manager(menu):
    slider = menu.add.range_slider("Range", 0.5, (0, 1), 1, range_margin=(100, 0))
    assert len(slider._kwargs) == 0
    assert slider._range_margin == (100, 0)


def test_empty_title(menu):
    r = menu.add.range_slider("", 0.5, (0, 1), 0.1)
    assert r.get_size() == (198, 66)


def test_invalid_range(menu):
    r = menu.add.range_slider(
        "Infection Rate", default=2, increment=0.5, range_values=(2, 10)
    )
    assert r.get_value() == 2
    assert r.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert r.get_value() == 2.5
    assert r.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert r.get_value() == 2
    assert not r.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert r.get_value() == 2
    for _ in range(20):
        r.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert r.get_value() == 10


def test_value_single_and_double(menu):
    # Single
    r = menu.add.range_slider("Range", 0.5, (0, 1), 0.1)
    assert r.get_value() == 0.5
    assert not r.value_changed()
    r.set_value(0.8)
    assert r.value_changed()
    assert r.get_value() == 0.8
    r.reset_value()
    assert r.get_value() == 0.5
    assert not r.value_changed()

    # Double
    r = menu.add.range_slider("Range", [0.2, 0.6], (0, 1), 0.1)
    assert r.get_value() == (0.2, 0.6)
    assert not r.value_changed()
    with pytest.raises(AssertionError):
        r.set_value(0.8)
    r.set_value((0.5, 1))
    assert r.value_changed()
    assert r.get_value() == (0.5, 1)
    r.reset_value()
    assert r.get_value() == (0.2, 0.6)
    assert not r.value_changed()


def test_reset_functionality(slider_double):
    slider_double.set_value((0.4, 0.9))
    assert slider_double.value_changed() is True

    slider_double.reset_value()
    assert slider_double.get_value() == (0.2, 0.8)
    assert slider_double.value_changed() is False


def test_keyrepeat_original_style(menu_no_ignore):
    e = PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True)
    slider_on = menu_no_ignore.add.range_slider("", 0, [0, 1], increment=0.1)
    slider_on.update(e)
    slider_off = menu_no_ignore.add.range_slider(
        "", 0, [0, 1], increment=0.1, repeat_keys=False
    )
    slider_off.update(e)

    for _ in range(5):
        sleep(0.5)
        slider_on.update([])
        slider_off.update([])
    assert slider_on.get_value() > 0.1
    assert slider_off.get_value() == 0.1


def test_key_repeat_functionality(menu):
    # Controlled version (no sleep)
    menu._keyboard_ignore_nonphysical = False
    slider = menu.add.range_slider("", 0, [0, 1], increment=0.1, repeat_keys=True)

    # Initial press
    e = PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True)
    slider.update(e)
    assert slider.get_value() == 0.1

    # Force repeat
    slider._keyrepeat_counters[ctrl.KEY_RIGHT] += 10000

    # First update: generates repeat event
    slider.update([])

    # Second update: applies repeat event
    slider.update([])

    assert slider.get_value() > 0.1


def test_set_default_value_logic():
    # Single slider
    slider_single = pygame_menu.widgets.RangeSlider(
        "Single", default_value=0.5, range_values=(0, 1), increment=0.1
    )
    assert slider_single._default_value == (0.5, 0)
    assert slider_single.get_value() == 0.5

    slider_single.set_value(0.8)
    assert slider_single.get_value() == 0.8
    slider_single.reset_value()
    assert slider_single.get_value() == 0.5

    # Double slider
    slider_double = pygame_menu.widgets.RangeSlider(
        "Double", default_value=(0.2, 0.7), range_values=(0, 1), increment=0.1
    )
    assert slider_double._default_value == (0.2, 0.7)
    assert slider_double.get_value() == (0.2, 0.7)

    slider_double.set_value((0.3, 0.9))
    assert slider_double.get_value() == (0.3, 0.9)
    slider_double.reset_value()
    assert slider_double.get_value() == (0.2, 0.7)

    # Set new defaults
    slider_single.set_default_value(0.3)
    assert slider_single._default_value == (0.3, 0)
    slider_single.reset_value()
    assert slider_single.get_value() == 0.3

    slider_double.set_default_value((0.1, 0.4))
    assert slider_double._default_value == (0.1, 0.4)
    slider_double.reset_value()
    assert slider_double.get_value() == (0.1, 0.4)

    # Invalid default types
    with pytest.raises(AssertionError):
        slider_single.set_default_value([0.1, 0.2])  # type: ignore
    with pytest.raises(AssertionError):
        slider_single.set_default_value("invalid")  # type: ignore

    with pytest.raises(AssertionError):
        slider_double.set_default_value(0.5)  # type: ignore
    with pytest.raises(AssertionError):
        slider_double.set_default_value((0.1, 0.2, 0.3))  # type: ignore


def test_render_invariants(menu):
    r = menu.add.range_slider("R", 0.5, (0, 1), 0.1)
    r.draw(surface)
    assert r._slider_height > 0
    assert r._range_box_height > 0
    assert r._range_line.get_width() == r._range_width
    assert r._slider[0].get_height() == r._slider_height


def test_tick_generation(menu):
    r = menu.add.range_slider("R", 0.5, (0, 1), 0.1, range_text_value_tick_number=5)
    r.draw(surface)
    assert len(r._range_text_value_tick_surfaces) == 5
    xs = [p[0] for p in r._range_text_value_tick_surfaces_pos]
    assert xs == sorted(xs)


def test_tick_disabled(menu):
    r = menu.add.range_slider(
        "R", 0.5, (0, 1), 0.1, range_text_value_tick_enabled=False
    )
    r.draw(surface)
    assert len(r._range_text_value_tick_surfaces) > 0


def test_custom_value_format(menu):
    r = menu.add.range_slider(
        "R", 0.5, (0, 1), 0.1, value_format=lambda x: f"{int(x * 100)}%"
    )
    r.draw(surface)
    assert isinstance(r._slider_text_value_surfaces[0], pygame.Surface)


def test_value_format_double(menu):
    r = menu.add.range_slider(
        "R", (0.2, 0.8), (0, 1), 0.1, value_format=lambda x: f"{x:.2f}"
    )
    r.draw(surface)
    assert len(r._slider_text_value_surfaces) == 2
    assert isinstance(r._slider_text_value_surfaces[0], pygame.Surface)
    assert isinstance(r._slider_text_value_surfaces[1], pygame.Surface)


def test_readonly_render(menu):
    r = menu.add.range_slider("R", 0.5, (0, 1), 0.1)
    r.readonly = True
    r.draw(surface)
    r.draw_after_if_selected(surface)
    assert r._slider_selected_highlight_enabled
    assert r.is_selected()


def test_overlap_selection(menu):
    r = menu.add.range_slider("R", (0.5, 0.50000001), (0, 1), 0.1)
    r.draw(surface)
    rect = r._get_slider_inflate_rect(1, to_real_position=True)
    assert not r.update(
        PygameEventUtils.middle_rect_click(rect, evtype=pygame.MOUSEBUTTONDOWN)
    )


def test_discrete_drag_snapping(menu):
    rv = [0, 1, 2, 3, 4]
    r = menu.add.range_slider("R", 2, rv)
    r.draw(surface)
    rect = r._get_slider_inflate_rect(0, to_real_position=True)
    r.update(PygameEventUtils.middle_rect_click(rect, evtype=pygame.MOUSEBUTTONDOWN))
    pos = r._test_get_pos_value(2.7)
    r.update(
        PygameEventUtils.mouse_motion(rect, rel=(pos[0], pos[1]), update_mouse=True)
    )
    assert r.get_value() in rv


def test_shift_increment(menu):
    r = menu.add.range_slider("R", 0.5, (0, 1), 0.1)
    v = r.get_value()
    r.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert r.get_value() == v + 0.1


@pytest.mark.parametrize("range_box", [True, False])
def test_range_box_visibility(menu, range_box):
    r = menu.add.range_slider("R", (0.2, 0.8), (0, 1), 0.1, range_box_enabled=range_box)
    r.draw(surface)
    if range_box:
        assert hasattr(r, "_range_box")
    else:
        assert not (hasattr(r, "_range_box") and r._range_box_enabled)


def test_range_box_disabled(menu):
    r = menu.add.range_slider("R", (0.2, 0.8), (0, 1), 0.1, range_box_enabled=False)
    r.draw(surface)
    assert not (hasattr(r, "_range_box") and r._range_box_enabled)


def test_padding_effect(menu):
    r = menu.add.range_slider("R", 0.5, (0, 1), 0.1, slider_text_value_padding=(10, 20))
    r.draw(surface)
    s = r._slider_text_value_surfaces[0]
    assert s.get_width() > 0


def test_margin_effect(menu):
    r = menu.add.range_slider("R", 0.5, (0, 1), 0.1, range_margin=(50, 0))
    r.draw(surface)
    assert r._range_margin == (50, 0)


def test_repeated_set_value(menu):
    r = menu.add.range_slider("R", 0.5, (0, 1), 0.1)
    r.set_value(0.5)
    r.set_value(0.5)
    assert r.get_value() == 0.5


def test_repeated_reset(menu):
    r = menu.add.range_slider("R", 0.5, (0, 1), 0.1)
    r.reset_value()
    r.reset_value()
    assert r.get_value() == 0.5


def test_small_increment(menu):
    r = menu.add.range_slider("R", 0.5, (0, 1), 1e-9)
    r.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert r.get_value() == pytest.approx(0.500000001)
