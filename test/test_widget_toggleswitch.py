"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - TOGGLESWITCH
Test ToggleSwitch widget.
"""

import pytest

import pygame_menu
import pygame_menu.controls as ctrl
from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented
from test._utils import MenuUtils, PygameEventUtils, surface


@pytest.fixture
def menu():
    return MenuUtils.generic_menu()


def test_toggleswitch_basic(menu):
    value = [None]

    def onchange(v):
        value[0] = v

    switch = menu.add.toggle_switch(
        "toggle", False, onchange=onchange, infinite=False, single_click=False
    )

    assert switch.get_value() is False
    assert value[0] is None

    switch.apply()
    assert value[0] is None

    # Not infinite: left does nothing
    switch.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert value[0] is None

    # Right toggles
    switch.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert value[0] is True

    switch.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert value[0] is False

    # No change
    switch.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert value[0] is False

    assert not switch.update(
        PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True, testmode=False)
    )

    # Infinite mode
    switch = menu.add.toggle_switch(
        "toggle", False, onchange=onchange, infinite=True, single_click=False
    )

    switch.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert value[0] is True

    switch.update(PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True))
    assert value[0] is False

    # KEY_APPLY toggles
    switch.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    assert value[0] is True
    switch.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    assert value[0] is False

    # Mouse clicks
    x, y = switch.get_rect(to_real_position=True, apply_padding=False).midleft

    switch.update(PygameEventUtils.mouse_click(x + 150, y))
    assert value[0] is False

    switch.update(PygameEventUtils.mouse_click(x + 250, y))
    assert value[0] is True

    switch.update(PygameEventUtils.mouse_click(x + 150, y))
    assert value[0] is False

    # Touch clicks
    switch._touchscreen_enabled = True

    switch.update(PygameEventUtils.touch_click(x + 250, y, menu=switch.get_menu()))
    assert value[0] is True

    switch.update(PygameEventUtils.touch_click(x + 250, y, menu=switch.get_menu()))
    assert value[0] is True

    switch.update(PygameEventUtils.touch_click(x + 150, y, menu=switch.get_menu()))
    assert value[0] is False

    # Readonly mode
    switch.readonly = True

    switch.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    assert value[0] is False

    switch._left()
    assert value[0] is False

    switch._right()
    assert value[0] is False

    # Back to normal
    switch.readonly = False
    switch.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert value[0] is True
    switch.update(PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True))
    assert value[0] is False

    switch.draw(surface)


@pytest.mark.parametrize(
    "method,args",
    [
        ("rotate", (10,)),
        ("scale", (100, 100)),
        ("resize", (100, 100)),
        ("flip", (True, True)),
        ("set_max_width", (100,)),
        ("set_max_height", (100,)),
    ],
)
def test_toggleswitch_invalid_transforms(menu, method, args):
    switch = menu.add.toggle_switch("toggle", False)
    with pytest.raises(WidgetTransformationNotImplemented):
        getattr(switch, method)(*args)


def test_toggleswitch_position_and_translate(menu):
    switch = menu.add.toggle_switch("toggle", False)

    switch.set_position(1, 1)
    assert switch.get_position() == (1, 1)

    switch.translate(1, 1)
    assert switch.get_translate() == (1, 1)


@pytest.mark.parametrize("bad_value", ["false"])
def test_toggleswitch_invalid_constructor(menu, bad_value):
    with pytest.raises(ValueError):
        menu.add.toggle_switch("toggle", bad_value)  # type: ignore


@pytest.mark.parametrize(
    "param,value",
    [
        ("single_click", "true"),
        ("single_click_dir", "true"),
    ],
)
def test_toggleswitch_invalid_single_click_params(menu, param, value):
    kwargs = {param: value}
    with pytest.raises(AssertionError):
        menu.add.toggle_switch("toggle", False, **kwargs)


def test_toggleswitch_state_font_validation(menu):
    pygame_menu.widgets.ToggleSwitch("Epic", state_text_font=menu._theme.widget_font)
    with pytest.raises(AssertionError):
        pygame_menu.widgets.ToggleSwitch("Epic", state_text_font_size=-1)


def test_toggleswitch_single_click(menu):
    switch = menu.add.toggle_switch("toggle", False)
    assert switch._infinite is True  # single_click=True implies infinite

    assert switch.get_value() is False
    switch._left()
    assert switch.get_value() is True

    x, y = switch.get_rect(to_real_position=True, apply_padding=False).midleft

    switch.update(PygameEventUtils.mouse_click(x + 150, y))
    assert switch.get_value() is False

    switch.update(PygameEventUtils.mouse_click(x + 250, y))
    assert switch.get_value() is True

    switch.update(PygameEventUtils.mouse_click(x + 250, y))
    assert switch.get_value() is False

    switch._single_click_dir = False
    switch.update(PygameEventUtils.mouse_click(x + 250, y))
    assert switch.get_value() is True


def test_toggleswitch_value(menu):
    switch = menu.add.toggle_switch("toggle", False)

    assert switch._default_value == 0
    assert not switch.value_changed()

    switch.set_value(1)
    assert switch.get_value() == 1
    assert switch.value_changed()

    switch.reset_value()
    assert switch.get_value() == 0
    assert not switch.value_changed()


def test_toggleswitch_empty_title(menu):
    switch = menu.add.toggle_switch("")
    assert switch.get_size() == (191, 49)


def test_toggleswitch_update_font(menu):
    switch = menu.add.toggle_switch("abc")

    assert switch.get_size() == (240, 49)
    assert switch._state_font.get_height() == 41

    switch.update_font(dict(size=100))

    assert switch._state_font.get_height() == 137
    assert switch.get_size() == (356, 145)
