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
        """Toggle state."""
        state["value"] = not state["value"]

    btn = menu.add.button("toggle", toggle)
    return btn, state


@pytest.fixture
def controller():
    """Return a default controller."""
    return ctrl.Controller()


def test_controller_default_joystick_timing(controller):
    """Validate default joystick delay and repeat values."""
    assert controller.joy_delay == ctrl.JOY_DELAY
    assert controller.joy_repeat == ctrl.JOY_REPEAT


def test_controller_joystick_timing_can_be_changed(controller):
    """Validate joystick timing values can be customized."""
    controller.joy_delay = 500
    controller.joy_repeat = 150

    assert controller.joy_delay == 500
    assert controller.joy_repeat == 150


@pytest.mark.parametrize(
    "method,event",
    [
        (
            "apply",
            PygameEventUtils.key(
                ctrl.KEY_APPLY,
                keydown=True,
                inlist=False,
            ),
        ),
        (
            "back",
            PygameEventUtils.key(
                ctrl.KEY_BACK,
                keydown=True,
                inlist=False,
            ),
        ),
        (
            "close_menu",
            PygameEventUtils.key(
                ctrl.KEY_CLOSE_MENU,
                keydown=True,
                inlist=False,
            ),
        ),
        (
            "delete",
            PygameEventUtils.key(
                ctrl.KEY_DELETE,
                keydown=True,
                inlist=False,
            ),
        ),
        (
            "end",
            PygameEventUtils.key(
                ctrl.KEY_END,
                keydown=True,
                inlist=False,
            ),
        ),
        (
            "escape",
            PygameEventUtils.key(
                ctrl.KEY_ESCAPE,
                keydown=True,
                inlist=False,
            ),
        ),
        (
            "home",
            PygameEventUtils.key(
                ctrl.KEY_HOME,
                keydown=True,
                inlist=False,
            ),
        ),
        (
            "left",
            PygameEventUtils.key(
                ctrl.KEY_LEFT,
                keydown=True,
                inlist=False,
            ),
        ),
        (
            "move_down",
            PygameEventUtils.key(
                ctrl.KEY_MOVE_DOWN,
                keydown=True,
                inlist=False,
            ),
        ),
        (
            "move_up",
            PygameEventUtils.key(
                ctrl.KEY_MOVE_UP,
                keydown=True,
                inlist=False,
            ),
        ),
        (
            "right",
            PygameEventUtils.key(
                ctrl.KEY_RIGHT,
                keydown=True,
                inlist=False,
            ),
        ),
        (
            "tab",
            PygameEventUtils.key(
                ctrl.KEY_TAB,
                keydown=True,
                inlist=False,
            ),
        ),
        (
            "joy_up",
            PygameEventUtils.joy_hat_motion(
                ctrl.JOY_UP,
                inlist=False,
            ),
        ),
        (
            "joy_down",
            PygameEventUtils.joy_hat_motion(
                ctrl.JOY_DOWN,
                inlist=False,
            ),
        ),
        (
            "joy_left",
            PygameEventUtils.joy_hat_motion(
                ctrl.JOY_LEFT,
                inlist=False,
            ),
        ),
        (
            "joy_right",
            PygameEventUtils.joy_hat_motion(
                ctrl.JOY_RIGHT,
                inlist=False,
            ),
        ),
        (
            "joy_select",
            PygameEventUtils.joy_button(
                ctrl.JOY_BUTTON_SELECT,
                inlist=False,
            ),
        ),
        (
            "joy_back",
            PygameEventUtils.joy_button(
                ctrl.JOY_BUTTON_BACK,
                inlist=False,
            ),
        ),
    ],
)
def test_controller_predicates(controller, method, event):
    """Validate controller predicate methods."""
    assert getattr(controller, method)(event, None) is True


@pytest.mark.parametrize(
    "method,event",
    [
        (
            "apply",
            PygameEventUtils.key(pygame.K_a, keydown=True, inlist=False),
        ),
        (
            "back",
            PygameEventUtils.key(pygame.K_a, keydown=True, inlist=False),
        ),
        (
            "close_menu",
            PygameEventUtils.key(pygame.K_a, keydown=True, inlist=False),
        ),
        (
            "delete",
            PygameEventUtils.key(pygame.K_a, keydown=True, inlist=False),
        ),
        (
            "end",
            PygameEventUtils.key(pygame.K_a, keydown=True, inlist=False),
        ),
        (
            "escape",
            PygameEventUtils.key(pygame.K_a, keydown=True, inlist=False),
        ),
        (
            "home",
            PygameEventUtils.key(pygame.K_a, keydown=True, inlist=False),
        ),
        (
            "left",
            PygameEventUtils.key(pygame.K_a, keydown=True, inlist=False),
        ),
        (
            "move_down",
            PygameEventUtils.key(pygame.K_a, keydown=True, inlist=False),
        ),
        (
            "move_up",
            PygameEventUtils.key(pygame.K_a, keydown=True, inlist=False),
        ),
        (
            "right",
            PygameEventUtils.key(pygame.K_a, keydown=True, inlist=False),
        ),
        (
            "tab",
            PygameEventUtils.key(pygame.K_a, keydown=True, inlist=False),
        ),
        (
            "joy_select",
            PygameEventUtils.joy_button(99, inlist=False),
        ),
        (
            "joy_back",
            PygameEventUtils.joy_button(99, inlist=False),
        ),
        (
            "joy_up",
            PygameEventUtils.joy_hat_motion((0, 0), inlist=False),
        ),
        (
            "joy_down",
            PygameEventUtils.joy_hat_motion((0, 0), inlist=False),
        ),
        (
            "joy_left",
            PygameEventUtils.joy_hat_motion((0, 0), inlist=False),
        ),
        (
            "joy_right",
            PygameEventUtils.joy_hat_motion((0, 0), inlist=False),
        ),
    ],
)
def test_controller_predicates_reject_unmatched_events(
    controller,
    method,
    event,
):
    """Validate predicates reject unrelated events."""
    assert getattr(controller, method)(event, None) is False


@pytest.mark.parametrize(
    "method,key",
    [
        ("apply", ctrl.KEY_APPLY),
        ("back", ctrl.KEY_BACK),
        ("close_menu", ctrl.KEY_CLOSE_MENU),
        ("delete", ctrl.KEY_DELETE),
        ("end", ctrl.KEY_END),
        ("escape", ctrl.KEY_ESCAPE),
        ("home", ctrl.KEY_HOME),
        ("left", ctrl.KEY_LEFT),
        ("move_down", ctrl.KEY_MOVE_DOWN),
        ("move_up", ctrl.KEY_MOVE_UP),
        ("right", ctrl.KEY_RIGHT),
        ("tab", ctrl.KEY_TAB),
    ],
)
def test_keyboard_predicates_reject_keyup_events(controller, method, key):
    """Validate keyboard predicates only accept KEYDOWN events."""
    event = PygameEventUtils.key(
        key,
        keyup=True,
        inlist=False,
    )

    assert getattr(controller, method)(event, None) is False


def test_keyboard_predicate_rejects_joystick_event(controller):
    """Validate keyboard predicates reject joystick events."""
    event = PygameEventUtils.joy_button(
        ctrl.JOY_BUTTON_SELECT,
        inlist=False,
    )

    assert controller.apply(event, None) is False


def test_joystick_button_predicate_rejects_keyboard_event(controller):
    """Validate joystick button predicates reject keyboard events."""
    event = PygameEventUtils.key(
        pygame.K_RETURN,
        keydown=True,
        inlist=False,
    )

    assert controller.joy_select(event, None) is False


@pytest.mark.parametrize(
    "value,expected",
    [
        (-ctrl.JOY_DEADZONE - 0.01, True),
        (-ctrl.JOY_DEADZONE, False),
        (-ctrl.JOY_DEADZONE + 0.01, False),
    ],
)
def test_deadzone_x_left(value, expected):
    """Test X-axis left deadzone boundary."""
    event = PygameEventUtils.joy_motion(x=value, inlist=False)

    assert ctrl.Controller.joy_axis_x_left(event, None) is expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (ctrl.JOY_DEADZONE + 0.01, True),
        (ctrl.JOY_DEADZONE, False),
        (ctrl.JOY_DEADZONE - 0.01, False),
    ],
)
def test_deadzone_x_right(value, expected):
    """Test X-axis right deadzone boundary."""
    event = PygameEventUtils.joy_motion(x=value, inlist=False)

    assert ctrl.Controller.joy_axis_x_right(event, None) is expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (-ctrl.JOY_DEADZONE - 0.01, True),
        (-ctrl.JOY_DEADZONE, False),
        (-ctrl.JOY_DEADZONE + 0.01, False),
    ],
)
def test_deadzone_y_up(value, expected):
    """Test Y-axis up deadzone boundary."""
    event = PygameEventUtils.joy_motion(y=value, inlist=False)

    assert ctrl.Controller.joy_axis_y_up(event, None) is expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (ctrl.JOY_DEADZONE + 0.01, True),
        (ctrl.JOY_DEADZONE, False),
        (ctrl.JOY_DEADZONE - 0.01, False),
    ],
)
def test_deadzone_y_down(value, expected):
    """Test Y-axis down deadzone boundary."""
    event = PygameEventUtils.joy_motion(y=value, inlist=False)

    assert ctrl.Controller.joy_axis_y_down(event, None) is expected


@pytest.mark.parametrize(
    "method",
    [
        "joy_axis_x_left",
        "joy_axis_x_right",
        "joy_axis_y_up",
        "joy_axis_y_down",
    ],
)
def test_axis_predicates_reject_hat_events(method):
    """Validate axis predicates reject hat events."""
    event = PygameEventUtils.joy_hat_motion(
        ctrl.JOY_UP,
        inlist=False,
    )

    assert getattr(ctrl.Controller, method)(event, None) is False


@pytest.mark.parametrize(
    "value",
    [
        (1, 1),
        (-1, -1),
        (1, -1),
        (-1, 1),
    ],
)
def test_joystick_diagonals_do_not_trigger(value):
    """Test diagonal hat directions do not trigger movement."""
    event = PygameEventUtils.joy_hat_motion(
        value,
        inlist=False,
    )

    assert ctrl.Controller.joy_up(event, None) is False
    assert ctrl.Controller.joy_down(event, None) is False
    assert ctrl.Controller.joy_left(event, None) is False
    assert ctrl.Controller.joy_right(event, None) is False


def test_key_apply_global_override(toggle_button, monkeypatch):
    """Test KEY_APPLY override affects existing widgets."""
    btn, state = toggle_button

    monkeypatch.setattr(ctrl, "KEY_APPLY", pygame.K_END)

    btn.update(PygameEventUtils.key(pygame.K_END, keydown=True))

    assert state["value"] is True


def test_key_apply_override_rejects_original_key(toggle_button, monkeypatch):
    """Test overridden KEY_APPLY no longer accepts the original key."""
    btn, state = toggle_button

    monkeypatch.setattr(ctrl, "KEY_APPLY", pygame.K_END)

    btn.update(PygameEventUtils.key(pygame.K_RETURN, keydown=True))

    assert state["value"] is False


def test_key_apply_affects_future_widgets(menu, monkeypatch):
    """Test KEY_APPLY override affects newly created widgets."""
    monkeypatch.setattr(ctrl, "KEY_APPLY", pygame.K_END)

    state = {"value": False}

    def toggle():
        """Toggle state."""
        state["value"] = not state["value"]

    btn = menu.add.button("x", toggle)
    btn.update(PygameEventUtils.key(pygame.K_END, keydown=True))

    assert state["value"] is True


def test_custom_controller_apply(toggle_button):
    """Test custom apply method overrides default behavior."""
    btn, state = toggle_button
    count = {"n": 0}

    def custom_apply(event, _):
        """Custom apply method overrides default behavior."""
        count["n"] += 1
        return event.key == pygame.K_a

    custom_controller = ctrl.Controller()
    custom_controller.apply = custom_apply
    btn.set_controller(custom_controller)

    btn.update(PygameEventUtils.key(pygame.K_a, keydown=True))

    assert state["value"] is True
    assert count["n"] == 1


def test_custom_controller_does_not_trigger_default(toggle_button):
    """Test custom controller blocks default KEY_APPLY."""
    btn, state = toggle_button

    custom_controller = ctrl.Controller()
    custom_controller.apply = lambda event, _: event.key == pygame.K_a
    btn.set_controller(custom_controller)

    btn.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))

    assert state["value"] is False


def test_custom_controller_rejects_nonmatching_key(toggle_button):
    """Test custom controller rejects a nonmatching key."""
    btn, state = toggle_button
    count = {"n": 0}

    def custom_apply(event, _):
        """Accept only the A key."""
        count["n"] += 1
        return event.key == pygame.K_a

    custom_controller = ctrl.Controller()
    custom_controller.apply = custom_apply
    btn.set_controller(custom_controller)

    btn.update(PygameEventUtils.key(pygame.K_b, keydown=True))

    assert state["value"] is False
    assert count["n"] == 1


def test_menu_controller_override(menu, button):
    """Test menu controller does not override widget controllers."""
    original = menu.get_controller()
    new_controller = ctrl.Controller()

    menu.set_controller(new_controller)

    assert menu.get_controller() is new_controller
    assert button.get_controller() is not new_controller

    menu.set_controller(original, apply_to_widgets=True)

    assert button.get_controller() is original


def test_menu_controller_applies_to_existing_widgets(menu):
    """Test apply_to_widgets=True updates existing widgets."""
    first = menu.add.button("first")
    second = menu.add.button("second")
    new_controller = ctrl.Controller()

    menu.set_controller(new_controller, apply_to_widgets=True)

    assert first.get_controller() is new_controller
    assert second.get_controller() is new_controller


def test_widget_controller_precedence(menu):
    """Test widget controller overrides menu controller."""
    widget_controller = ctrl.Controller()
    menu_controller = ctrl.Controller()

    btn = menu.add.button("x")
    btn.set_controller(widget_controller)
    menu.set_controller(menu_controller)

    assert btn.get_controller() is widget_controller


def test_menu_ignores_nonphysical_by_default(menu):
    """Test menu ignores nonphysical events by default."""
    menu.add.button("a")
    menu.add.button("b")

    assert menu.get_index() == 0

    events = PygameEventUtils.key(
        pygame.K_DOWN,
        keydown=True,
        testmode=False,
    )
    menu.update(events)

    assert menu.get_index() == 0


def test_menu_processes_nonphysical_when_enabled(menu):
    """Test menu processes nonphysical events when allowed."""
    menu.add.button("a")
    menu.add.button("b")

    assert menu.get_index() == 0

    events = PygameEventUtils.key(
        pygame.K_DOWN,
        keydown=True,
        testmode=False,
    )
    menu._keyboard_ignore_nonphysical = False
    menu.update(events)

    assert menu.get_index() == 1


def test_widget_always_ignores_nonphysical(menu):
    """Test widgets always ignore nonphysical events."""
    btn = menu.add.button("x")

    events = PygameEventUtils.key(
        pygame.K_RETURN,
        keydown=True,
        testmode=False,
    )
    btn.update(events)

    assert btn._ignores_keyboard_nonphysical() is True
