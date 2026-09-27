"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST EVENTS
Test MenuAction class.
"""

import pickle

import pygame.locals as locals
import pytest

import pygame_menu.events as events


def test_menuaction_enum_members():
    """Ensure enum members map to correct integer values."""
    assert events.MenuAction.BACK.value == 0
    assert events.MenuAction.CLOSE.value == 1
    assert events.MenuAction.EXIT.value == 3
    assert events.MenuAction.NONE.value == 4
    assert events.MenuAction.RESET.value == 5


def test_menuaction_repr_and_str():
    """Verify __repr__ and __str__ produce readable names."""
    assert repr(events.MenuAction.BACK) == "<MenuAction::BACK>"
    assert str(events.MenuAction.BACK) == "BACK"


def test_menuaction_equality_with_int():
    """Confirm standard Enum members do not equal raw integers directly, but values match."""
    assert events.MenuAction.BACK != 0
    assert events.MenuAction.BACK.value == 0
    assert events.MenuAction.EXIT.value == 3
    assert events.MenuAction.NONE.value == 4


def test_menuaction_identity():
    """Check identity behavior for enum members vs raw integers."""
    assert events.MenuAction.BACK is events.MenuAction.BACK
    assert 0 is not events.MenuAction.BACK


def test_menuaction_unknown_value_raises():
    """Unknown integer values must raise ValueError."""
    with pytest.raises(ValueError):
        events.MenuAction(999)


def test_is_event_with_enum_member():
    """is_event must accept valid MenuAction instances."""
    assert events.is_event(events.MenuAction.BACK) is True


def test_is_event_with_raw_int():
    """is_event must reject raw integers."""
    assert events.is_event(0) is False


def test_is_event_with_other_type():
    """is_event must reject non-MenuAction objects."""
    assert events.is_event("BACK") is False


def test_is_event_dynamic_reload_fallback():
    """Dynamic reload fallback must not classify foreign MenuAction types."""
    FakeMenuAction = type("MenuAction", (), {})
    assert events.is_event(FakeMenuAction()) is False


def test_constants_are_enum_members():
    """Module-level constants must reference enum members."""
    assert events.BACK is events.MenuAction.BACK
    assert events.CLOSE is events.MenuAction.CLOSE
    assert events.EXIT is events.MenuAction.EXIT
    assert events.NONE is events.MenuAction.NONE
    assert events.RESET is events.MenuAction.RESET


def test_pygame_quit_constant():
    """PYGAME_QUIT must match pygame.locals.QUIT."""
    assert events.PYGAME_QUIT == locals.QUIT


def test_pygame_windowclose_constant():
    """PYGAME_WINDOWCLOSE must match the correct pygame constant."""
    if hasattr(locals, "WINDOWCLOSE"):
        assert events.PYGAME_WINDOWCLOSE == locals.WINDOWCLOSE
    elif hasattr(locals, "WINDOWEVENT_CLOSE"):
        assert events.PYGAME_WINDOWCLOSE == locals.WINDOWEVENT_CLOSE
    else:
        assert events.PYGAME_WINDOWCLOSE == -1


def test_menu_last_event_literals():
    """MENU_LAST_* constants must match expected literal strings."""
    assert events.MENU_LAST_DISABLE_UPDATE == "DISABLE_UPDATE"
    assert events.MENU_LAST_FRAMES == "FRAMES"
    assert events.MENU_LAST_JOY_REPEAT == "JOY_REPEAT"
    assert events.MENU_LAST_MENU_BACK == "MENU_BACK"
    assert events.MENU_LAST_MENU_CLOSE == "MENU_CLOSE"
    assert events.MENU_LAST_MENUBAR == "MENUBAR"
    assert events.MENU_LAST_MOUSE_ENTER_MENU == "MOUSE_ENTER_MENU"
    assert events.MENU_LAST_MOUSE_ENTER_WINDOW == "MOUSE_ENTER_WINDOW"
    assert events.MENU_LAST_MOUSE_LEAVE_MENU == "MOUSE_LEAVE_MENU"
    assert events.MENU_LAST_MOUSE_LEAVE_WINDOW == "MOUSE_LEAVE_WINDOW"
    assert events.MENU_LAST_MOVE_DOWN == "MOVE_DOWN"
    assert events.MENU_LAST_MOVE_LEFT == "MOVE_LEFT"
    assert events.MENU_LAST_MOVE_RIGHT == "MOVE_RIGHT"
    assert events.MENU_LAST_MOVE_UP == "MOVE_UP"
    assert events.MENU_LAST_NONE == "NONE"
    assert events.MENU_LAST_QUIT == "QUIT"
    assert events.MENU_LAST_SCROLL_AREA == "SCROLL_AREA"
    assert events.MENU_LAST_SELECTED_WIDGET_BUTTON_UP == "SELECTED_WIDGET_BUTTON_UP"
    assert events.MENU_LAST_SELECTED_WIDGET_EVENT == "SELECTED_WIDGET_EVENT"
    assert events.MENU_LAST_SELECTED_WIDGET_FINGER_UP == "SELECTED_WIDGET_FINGER_UP"
    assert events.MENU_LAST_WIDGET_DISABLE_ACTIVE_STATE == "WIDGET_DISABLE_ACTIVE_STATE"
    assert events.MENU_LAST_WIDGET_SELECT == "WIDGET_SELECT"
    assert events.MENU_LAST_WIDGET_SELECT_MOTION == "WIDGET_SELECT_MOTION"


def test_backwards_identity_comparison_breakage():
    """Document identity mismatch between raw ints and enum members."""
    assert events.MenuAction(0) is events.MenuAction.BACK
    assert 0 is not events.MenuAction.BACK


def test_backwards_unknown_action_breakage():
    """Document that unknown integer actions now raise ValueError."""
    with pytest.raises(ValueError):
        events.MenuAction(42)


def test_menuaction_iteration_and_length():
    """Verify MenuAction contains exactly all defined actions."""
    expected_members = [
        events.MenuAction.BACK,
        events.MenuAction.CLOSE,
        events.MenuAction.EXIT,
        events.MenuAction.NONE,
        events.MenuAction.RESET,
    ]
    assert list(events.MenuAction) == expected_members
    assert len(events.MenuAction) == 5


def test_menuaction_hashable_and_dict_key():
    """Ensure MenuAction members can be hashed and used as dictionary keys."""
    action_handlers = {
        events.MenuAction.BACK: "go_back",
        events.MenuAction.CLOSE: "close_menu",
    }
    assert action_handlers[events.MenuAction.BACK] == "go_back"
    assert len({events.MenuAction.BACK, events.MenuAction.BACK}) == 1


def test_menuaction_pickle_serialization():
    """Ensure MenuAction enum members retain identity after pickling."""
    pickled = pickle.dumps(events.MenuAction.BACK)
    unpickled = pickle.loads(pickled)
    assert unpickled is events.MenuAction.BACK
