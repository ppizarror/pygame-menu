"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EVENTS
Menu events definition and locals.
"""

from __future__ import annotations

__all__ = [
    # Class
    "MenuAction",
    # Utils
    "is_event",
    # Menu events
    "BACK",
    "CLOSE",
    "EXIT",
    "NONE",
    "RESET",
    # Last menu events
    "MENU_LAST_DISABLE_UPDATE",
    "MENU_LAST_FRAMES",
    "MENU_LAST_JOY_REPEAT",
    "MENU_LAST_MENU_BACK",
    "MENU_LAST_MENU_CLOSE",
    "MENU_LAST_MENUBAR",
    "MENU_LAST_MOUSE_ENTER_MENU",
    "MENU_LAST_MOUSE_ENTER_WINDOW",
    "MENU_LAST_MOUSE_LEAVE_MENU",
    "MENU_LAST_MOUSE_LEAVE_WINDOW",
    "MENU_LAST_MOVE_DOWN",
    "MENU_LAST_MOVE_LEFT",
    "MENU_LAST_MOVE_RIGHT",
    "MENU_LAST_MOVE_UP",
    "MENU_LAST_NONE",
    "MENU_LAST_QUIT",
    "MENU_LAST_SCROLL_AREA",
    "MENU_LAST_SELECTED_WIDGET_BUTTON_UP",
    "MENU_LAST_SELECTED_WIDGET_EVENT",
    "MENU_LAST_SELECTED_WIDGET_FINGER_UP",
    "MENU_LAST_WIDGET_DISABLE_ACTIVE_STATE",
    "MENU_LAST_WIDGET_SELECT",
    "MENU_LAST_WIDGET_SELECT_MOTION",
    # Pygame events
    "PYGAME_QUIT",
    "PYGAME_WINDOWCLOSE",
]

from enum import Enum
from typing import Any, Final, Literal

import pygame.locals as __locals


class MenuAction(Enum):
    """
    Pygame-menu events representation. Immutable value type backed by an Enum.
    """

    BACK = 0
    CLOSE = 1
    EXIT = 3
    NONE = 4
    RESET = 5

    def __repr__(self) -> str:
        return f"<MenuAction::{self.name}>"

    def __str__(self) -> str:
        return self.name


def is_event(event: Any) -> bool:
    """
    Check if event is a pygame_menu MenuAction event type.

    :param event: Event object to check
    :return: ``True`` if event is a valid MenuAction instance
    """
    return isinstance(event, MenuAction)


# Events
BACK: Final[MenuAction] = MenuAction.BACK  # Menu back
CLOSE: Final[MenuAction] = MenuAction.CLOSE  # Close Menu
EXIT: Final[MenuAction] = MenuAction.EXIT  # Menu exit program
NONE: Final[MenuAction] = MenuAction.NONE  # None action. It's the same as 'None'
RESET: Final[MenuAction] = MenuAction.RESET  # Menu reset

# Pygame events
PYGAME_QUIT: Final[int] = __locals.QUIT
PYGAME_WINDOWCLOSE: int = -1

if hasattr(__locals, "WINDOWCLOSE"):
    PYGAME_WINDOWCLOSE = __locals.WINDOWCLOSE
elif hasattr(__locals, "WINDOWEVENT_CLOSE"):
    PYGAME_WINDOWCLOSE = __locals.WINDOWEVENT_CLOSE

# Menu last event types. Returned by menu.get_last_update_mode()
MenuLastEventType = Literal[
    "DISABLE_UPDATE",
    "FRAMES",
    "JOY_REPEAT",
    "MENU_BACK",
    "MENU_CLOSE",
    "MENUBAR",
    "MOUSE_ENTER_MENU",
    "MOUSE_ENTER_WINDOW",
    "MOUSE_LEAVE_MENU",
    "MOUSE_LEAVE_WINDOW",
    "MOVE_DOWN",
    "MOVE_LEFT",
    "MOVE_RIGHT",
    "MOVE_UP",
    "NONE",
    "QUIT",
    "SCROLL_AREA",
    "SELECTED_WIDGET_BUTTON_UP",
    "SELECTED_WIDGET_EVENT",
    "SELECTED_WIDGET_FINGER_UP",
    "WIDGET_DISABLE_ACTIVE_STATE",
    "WIDGET_SELECT",
    "WIDGET_SELECT_MOTION",
]

MENU_LAST_DISABLE_UPDATE: Final[MenuLastEventType] = "DISABLE_UPDATE"
MENU_LAST_FRAMES: Final[MenuLastEventType] = "FRAMES"
MENU_LAST_JOY_REPEAT: Final[MenuLastEventType] = "JOY_REPEAT"
MENU_LAST_MENU_BACK: Final[MenuLastEventType] = "MENU_BACK"
MENU_LAST_MENU_CLOSE: Final[MenuLastEventType] = "MENU_CLOSE"
MENU_LAST_MENUBAR: Final[MenuLastEventType] = "MENUBAR"
MENU_LAST_MOUSE_ENTER_MENU: Final[MenuLastEventType] = "MOUSE_ENTER_MENU"
MENU_LAST_MOUSE_ENTER_WINDOW: Final[MenuLastEventType] = "MOUSE_ENTER_WINDOW"
MENU_LAST_MOUSE_LEAVE_MENU: Final[MenuLastEventType] = "MOUSE_LEAVE_MENU"
MENU_LAST_MOUSE_LEAVE_WINDOW: Final[MenuLastEventType] = "MOUSE_LEAVE_WINDOW"
MENU_LAST_MOVE_DOWN: Final[MenuLastEventType] = "MOVE_DOWN"
MENU_LAST_MOVE_LEFT: Final[MenuLastEventType] = "MOVE_LEFT"
MENU_LAST_MOVE_RIGHT: Final[MenuLastEventType] = "MOVE_RIGHT"
MENU_LAST_MOVE_UP: Final[MenuLastEventType] = "MOVE_UP"
MENU_LAST_NONE: Final[MenuLastEventType] = "NONE"
MENU_LAST_QUIT: Final[MenuLastEventType] = "QUIT"
MENU_LAST_SCROLL_AREA: Final[MenuLastEventType] = "SCROLL_AREA"
MENU_LAST_SELECTED_WIDGET_BUTTON_UP: Final[MenuLastEventType] = (
    "SELECTED_WIDGET_BUTTON_UP"
)
MENU_LAST_SELECTED_WIDGET_EVENT: Final[MenuLastEventType] = "SELECTED_WIDGET_EVENT"
MENU_LAST_SELECTED_WIDGET_FINGER_UP: Final[MenuLastEventType] = (
    "SELECTED_WIDGET_FINGER_UP"
)
MENU_LAST_WIDGET_DISABLE_ACTIVE_STATE: Final[MenuLastEventType] = (
    "WIDGET_DISABLE_ACTIVE_STATE"
)
MENU_LAST_WIDGET_SELECT: Final[MenuLastEventType] = "WIDGET_SELECT"
MENU_LAST_WIDGET_SELECT_MOTION: Final[MenuLastEventType] = "WIDGET_SELECT_MOTION"
