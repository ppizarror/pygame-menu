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
