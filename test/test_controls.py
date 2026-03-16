"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST CONTROLS
Test controls configuration.
"""

import pygame
import pytest

import pygame_menu.controls as ctrl
from test._utils import MenuUtils, PygameEventUtils


@pytest.fixture
def menu():
    """Return a generic menu."""
    return MenuUtils.generic_menu()


@pytest.fixture
def button(menu):
    """Return a simple button."""
    return menu.add.button("btn", lambda: None)


@pytest.fixture
def toggle_button(menu):
    """Return a button that toggles state."""
    state = {"value": False}

    def toggle():
        state["value"] = not state["value"]

    btn = menu.add.button("toggle", toggle)
    return btn, state


@pytest.fixture
def controller():
    """Return a default controller."""
    return ctrl.Controller()


@pytest.mark.parametrize(
    "method,event,expected",
    [
        (
                "apply",
                PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True, inlist=False),
                True,
        ),
        ("back", PygameEventUtils.key(ctrl.KEY_BACK, keydown=True, inlist=False), True),
        (
                "close_menu",
                PygameEventUtils.key(ctrl.KEY_CLOSE_MENU, keydown=True, inlist=False),
                True,
        ),
        ("left", PygameEventUtils.key(ctrl.KEY_LEFT, keydown=True, inlist=False), True),
        (
                "right",
                PygameEventUtils.key(ctrl.KEY_RIGHT, keydown=True, inlist=False),
                True,
        ),
        (
                "move_up",
                PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True, inlist=False),
                True,
        ),
        (
                "move_down",
                PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True, inlist=False),
                True,
        ),
        ("tab", PygameEventUtils.key(ctrl.KEY_TAB, keydown=True, inlist=False), True),
        ("joy_up", PygameEventUtils.joy_hat_motion(ctrl.JOY_UP, inlist=False), True),
        (
                "joy_down",
                PygameEventUtils.joy_hat_motion(ctrl.JOY_DOWN, inlist=False),
                True,
        ),
        (
                "joy_left",
                PygameEventUtils.joy_hat_motion(ctrl.JOY_LEFT, inlist=False),
                True,
        ),
        (
                "joy_right",
                PygameEventUtils.joy_hat_motion(ctrl.JOY_RIGHT, inlist=False),
                True,
        ),
        (
                "joy_select",
                PygameEventUtils.joy_button(ctrl.JOY_BUTTON_SELECT, inlist=False),
                True,
        ),
        (
                "joy_back",
                PygameEventUtils.joy_button(ctrl.JOY_BUTTON_BACK, inlist=False),
                True,
        ),
    ],
)
def test_controller_predicates(controller, method, event, expected):
    """Validate controller predicate methods."""
    assert getattr(controller, method)(event, None) is expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (-ctrl.JOY_DEADZONE - 0.01, True),
        (-ctrl.JOY_DEADZONE + 0.01, False),
        (-ctrl.JOY_DEADZONE, False),
    ],
)
def test_deadzone_x_left(value, expected):
    """Test left deadzone boundary."""
    event = PygameEventUtils.joy_motion(x=value, inlist=False)
    assert ctrl.Controller.joy_axis_x_left(event, None) is expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (ctrl.JOY_DEADZONE + 0.01, True),
        (ctrl.JOY_DEADZONE - 0.01, False),
        (ctrl.JOY_DEADZONE, False),
    ],
)
def test_deadzone_x_right(value, expected):
    """Test right deadzone boundary."""
    event = PygameEventUtils.joy_motion(x=value, inlist=False)
    assert ctrl.Controller.joy_axis_x_right(event, None) is expected


def test_key_apply_global_override(toggle_button):
    """Test KEY_APPLY override affects existing widgets."""
    btn, state = toggle_button
    ctrl.KEY_APPLY = pygame.K_END
    btn.update(PygameEventUtils.key(pygame.K_END, keydown=True))
    assert state["value"] is True
    ctrl.KEY_APPLY = pygame.K_RETURN


def test_key_apply_affects_future_widgets(menu):
    """Test KEY_APPLY override affects newly created widgets."""
    ctrl.KEY_APPLY = pygame.K_END
    state = {"value": False}

    def toggle():
        state["value"] = not state["value"]

    btn = menu.add.button("x", toggle)
    btn.update(PygameEventUtils.key(pygame.K_END, keydown=True))
    assert state["value"] is True
    ctrl.KEY_APPLY = pygame.K_RETURN


def test_custom_controller_apply(toggle_button):
    """Test custom apply method overrides default behavior."""
    btn, state = toggle_button
    count = {"n": 0}

    def custom_apply(event, _):
        count["n"] += 1
        return event.key == pygame.K_a

    c = ctrl.Controller()
    c.apply = custom_apply
    btn.set_controller(c)

    btn.update(PygameEventUtils.key(pygame.K_a, keydown=True))
    assert state["value"] is True
    assert count["n"] == 1


def test_custom_controller_does_not_trigger_default(toggle_button):
    """Test custom controller blocks default KEY_APPLY."""
    btn, state = toggle_button
    c = ctrl.Controller()
    c.apply = lambda event, _: event.key == pygame.K_a
    btn.set_controller(c)

    btn.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
    assert state["value"] is False


def test_menu_controller_override(menu, button):
    """Test menu-level controller override does not override widget controllers."""
    original = menu.get_controller()
    new = ctrl.Controller()

    menu.set_controller(new)
    assert menu.get_controller() is new
    assert button.get_controller() is not new

    menu.set_controller(original, apply_to_widgets=True)
    assert button.get_controller() is original


def test_widget_controller_precedence(menu):
    """Test widget controller overrides menu controller."""
    widget_ctrl = ctrl.Controller()
    menu_ctrl = ctrl.Controller()

    btn = menu.add.button("x")
    btn.set_controller(widget_ctrl)
    menu.set_controller(menu_ctrl)

    assert btn.get_controller() is widget_ctrl


def test_menu_ignores_nonphysical_by_default(menu):
    """Test menu ignores nonphysical events."""
    menu.add.button("a")
    menu.add.button("b")
    assert menu.get_index() == 0

    events = PygameEventUtils.key(pygame.K_DOWN, keydown=True, testmode=False)
    menu.update(events)
    assert menu.get_index() == 0


def test_menu_processes_nonphysical_when_enabled(menu):
    """Test menu processes nonphysical events when allowed."""
    menu.add.button("a")
    menu.add.button("b")
    assert menu.get_index() == 0

    events = PygameEventUtils.key(pygame.K_DOWN, keydown=True, testmode=False)
    menu._keyboard_ignore_nonphysical = False
    menu.update(events)
    assert menu.get_index() == 1


def test_widget_always_ignores_nonphysical(menu):
    """Test widgets always ignore nonphysical events."""
    btn = menu.add.button("x")
    events = PygameEventUtils.key(pygame.K_RETURN, keydown=True, testmode=False)
    btn.update(events)
    assert btn._ignores_keyboard_nonphysical() is True


@pytest.mark.parametrize("value", [(1, 1), (-1, -1), (1, -1), (-1, 1)])
def test_joystick_diagonals_do_not_trigger(value):
    """Test diagonal hat directions do not trigger movement."""
    event = PygameEventUtils.joy_hat_motion(value, inlist=False)
    assert ctrl.Controller.joy_up(event, None) is False
    assert ctrl.Controller.joy_down(event, None) is False
    assert ctrl.Controller.joy_left(event, None) is False
    assert ctrl.Controller.joy_right(event, None) is False
