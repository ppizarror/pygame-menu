"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - SELECTOR
Test Selector widget.
"""

import pytest

import pygame_menu
import pygame_menu.controls as ctrl
from test._utils import MenuUtils, PygameEventUtils, surface


@pytest.fixture
def menu():
    return MenuUtils.generic_menu()


def test_selector_basic(menu):
    selector = menu.add.selector(
        "selector",
        [("1 - Easy", "EASY"), ("2 - Medium", "MEDIUM"), ("3 - Hard", "HARD")],
        default=1,
    )

    menu.enable()
    menu.draw(surface)

    selector.draw(surface)
    selector._selected = False
    selector.draw(surface)

    # Keyboard and joystick events
    selector.update(PygameEventUtils.key(0, keydown=True, testmode=False))
    selector.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    selector.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    selector.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    selector.update(PygameEventUtils.joy_hat_motion(ctrl.JOY_LEFT))
    selector.update(PygameEventUtils.joy_hat_motion(ctrl.JOY_RIGHT))
    selector.update(PygameEventUtils.joy_motion(1, 0))
    selector.update(PygameEventUtils.joy_motion(-1, 0))

    # Mouse click on center
    cx, cy = selector.get_rect(to_real_position=True, apply_padding=False).center
    selector.update(PygameEventUtils.mouse_click(cx, cy))

    # Left/right click cycling
    assert selector.get_index() == 0
    left_x, left_y = selector.get_rect(
        to_real_position=True, apply_padding=False
    ).midleft

    selector.update(PygameEventUtils.mouse_click(left_x + 150, left_y))
    assert selector.get_index() == 2
    selector.update(PygameEventUtils.mouse_click(left_x + 150, left_y))
    assert selector.get_index() == 1
    selector.update(PygameEventUtils.mouse_click(left_x + 150, left_y))
    assert selector.get_index() == 0

    selector.update(PygameEventUtils.mouse_click(left_x + 250, left_y))
    assert selector.get_index() == 1
    selector.update(PygameEventUtils.mouse_click(left_x + 250, left_y))
    assert selector.get_index() == 2
    selector.update(PygameEventUtils.mouse_click(left_x + 250, left_y))
    assert selector.get_index() == 0

    # Touchscreen cycling
    selector._touchscreen_enabled = True
    selector.update(
        PygameEventUtils.touch_click(left_x + 150, left_y, menu=selector.get_menu())
    )
    assert selector.get_index() == 2
    selector.update(
        PygameEventUtils.touch_click(left_x + 250, left_y, menu=selector.get_menu())
    )
    assert selector.get_index() == 0
    selector.update(
        PygameEventUtils.touch_click(left_x + 250, left_y, menu=selector.get_menu())
    )
    assert selector.get_index() == 1

    # Update items
    new_items = [
        ("4 - Easy", "EASY"),
        ("5 - Medium", "MEDIUM"),
        ("6 - Hard", "HARD"),
    ]
    selector.update_items(new_items)

    selector.set_value("6 - Hard")
    assert selector.get_value()[1] == 2

    # Invalid set_value inputs
    with pytest.raises(AssertionError):
        selector.set_value(bool)  # type: ignore
    with pytest.raises(AssertionError):
        selector.set_value(200)

    selector.set_value(1)
    assert selector.get_value()[1] == 1
    assert selector.get_value()[0][0] == "5 - Medium"

    # Left navigation
    selector.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert selector.get_value()[0][0] == "4 - Easy"

    # Readonly mode
    selector.readonly = True
    selector.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert selector.get_value()[0][0] == "4 - Easy"

    selector._left()
    assert selector.get_value()[0][0] == "4 - Easy"
    selector._right()
    assert selector.get_value()[0][0] == "4 - Easy"

    # Fancy selector
    sel_fancy = menu.add.selector(
        "Fancy ",
        [("1 - Easy", "EASY"), ("2 - Medium", "MEDIUM"), ("3 - Hard", "HARD")],
        default=1,
        style=pygame_menu.widgets.widget.selector.SELECTOR_STYLE_FANCY,
    )

    assert sel_fancy.get_items() == [
        ("1 - Easy", "EASY"),
        ("2 - Medium", "MEDIUM"),
        ("3 - Hard", "HARD"),
    ]

    # Invalid default index
    with pytest.raises(AssertionError):
        menu.add.selector("title", [("a", "a"), ("b", "b")], default=2)


@pytest.mark.parametrize(
    "initial,change,expected",
    [
        (("b", "b"), "a", ("a", "a")),
    ],
)
def test_selector_value(menu, initial, change, expected):
    sel = menu.add.selector("title", [("a", "a"), ("b", "b")], default=1)

    assert sel.get_value() == (initial, 1)
    assert not sel.value_changed()

    sel.set_value(change)
    assert sel.get_value() == (expected, 0)
    assert sel.value_changed()

    sel.reset_value()
    assert sel.get_value() == (initial, 1)
    assert not sel.value_changed()


def test_selector_empty_title(menu):
    sel = menu.add.selector("", [("a", "a"), ("b", "b")])
    assert sel.get_size() == (83, 49)
