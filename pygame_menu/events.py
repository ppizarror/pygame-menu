"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EVENTS
Menu events definition and locals.
"""

__all__ = [

    # Class
    'MenuAction',

    # Utils
    'is_event',

    # Menu events
    'BACK',
    'CLOSE',
    'EXIT',
    'NONE',
    'RESET',

    # Last menu events
    'MENU_LAST_DISABLE_UPDATE',
    'MENU_LAST_FRAMES',
    'MENU_LAST_JOY_REPEAT',
    'MENU_LAST_MENU_BACK',
    'MENU_LAST_MENU_CLOSE',
    'MENU_LAST_MENUBAR',
    'MENU_LAST_MOUSE_ENTER_MENU',
    'MENU_LAST_MOUSE_ENTER_WINDOW',
    'MENU_LAST_MOUSE_LEAVE_MENU',
    'MENU_LAST_MOUSE_LEAVE_WINDOW',
    'MENU_LAST_MOVE_DOWN',
    'MENU_LAST_MOVE_LEFT',
    'MENU_LAST_MOVE_RIGHT',
    'MENU_LAST_MOVE_UP',
    'MENU_LAST_NONE',
    'MENU_LAST_QUIT',
    'MENU_LAST_SCROLL_AREA',
    'MENU_LAST_SELECTED_WIDGET_BUTTON_UP',
    'MENU_LAST_SELECTED_WIDGET_EVENT',
    'MENU_LAST_SELECTED_WIDGET_FINGER_UP',
    'MENU_LAST_WIDGET_DISABLE_ACTIVE_STATE',
    'MENU_LAST_WIDGET_SELECT',
    'MENU_LAST_WIDGET_SELECT_MOTION',

    # Pygame events
    'PYGAME_QUIT',
    'PYGAME_WINDOWCLOSE'

]

from typing import Any
import pygame.locals as __locals


class MenuAction(object):
    """
    Pygame-menu events.

    :param action: Action identifier
    """
    _action: int

    def __init__(self, action: int) -> None:
        assert isinstance(action, int)
        self._action = action

    def __eq__(self, other: 'MenuAction') -> bool:
        if isinstance(other, MenuAction):
            return self._action == other._action
        return False


def is_event(event: Any) -> bool:
    """
    Check if event is pygame_menu event type.

    :param event: Event
    :return: ``True`` if it's an event
    """
    return isinstance(event, MenuAction) or \
           str(type(event)) == "<class 'pygame_menu.events.MenuAction'>"


# Events
BACK = MenuAction(0)  # Menu back
CLOSE = MenuAction(1)  # Close Menu
EXIT = MenuAction(3)  # Menu exit program
NONE = MenuAction(4)  # None action. It's the same as 'None'
RESET = MenuAction(5)  # Menu reset

# Pygame events
PYGAME_QUIT = __locals.QUIT
PYGAME_WINDOWCLOSE = -1
if hasattr(__locals, 'WINDOWCLOSE'):
    PYGAME_WINDOWCLOSE = __locals.WINDOWCLOSE
elif hasattr(__locals, 'WINDOWEVENT_CLOSE'):
    PYGAME_WINDOWCLOSE = __locals.WINDOWEVENT_CLOSE

# Menu last event types. Returned by menu.get_last_update_mode()
MENU_LAST_DISABLE_UPDATE = 'DISABLE_UPDATE'
MENU_LAST_FRAMES = 'FRAMES'
MENU_LAST_JOY_REPEAT = 'JOY_REPEAT'
MENU_LAST_MENU_BACK = 'MENU_BACK'
MENU_LAST_MENU_CLOSE = 'MENU_CLOSE'
MENU_LAST_MENUBAR = 'MENUBAR'
MENU_LAST_MOUSE_ENTER_MENU = 'MOUSE_ENTER_MENU'
MENU_LAST_MOUSE_ENTER_WINDOW = 'MOUSE_ENTER_WINDOW'
MENU_LAST_MOUSE_LEAVE_MENU = 'MOUSE_LEAVE_MENU'
MENU_LAST_MOUSE_LEAVE_WINDOW = 'MOUSE_LEAVE_WINDOW'
MENU_LAST_MOVE_DOWN = 'MOVE_DOWN'
MENU_LAST_MOVE_LEFT = 'MOVE_LEFT'
MENU_LAST_MOVE_RIGHT = 'MOVE_RIGHT'
MENU_LAST_MOVE_UP = 'MOVE_UP'
MENU_LAST_NONE = 'NONE'
MENU_LAST_QUIT = 'QUIT'
MENU_LAST_SCROLL_AREA = 'SCROLL_AREA'
MENU_LAST_SELECTED_WIDGET_BUTTON_UP = 'SELECTED_WIDGET_BUTTON_UP'
MENU_LAST_SELECTED_WIDGET_EVENT = 'SELECTED_WIDGET_EVENT'
MENU_LAST_SELECTED_WIDGET_FINGER_UP = 'SELECTED_WIDGET_FINGER_UP'
MENU_LAST_WIDGET_DISABLE_ACTIVE_STATE = 'WIDGET_DISABLE_ACTIVE_STATE'
MENU_LAST_WIDGET_SELECT = 'WIDGET_SELECT'
MENU_LAST_WIDGET_SELECT_MOTION = 'WIDGET_SELECT_MOTION'
