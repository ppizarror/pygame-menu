"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EVENTS
Menu events definition and locals.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2021 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
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
    'PYGAME_WINDOWCLOSE',

    # Compatibility
    'DISABLE_CLOSE'

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
DISABLE_CLOSE = MenuAction(2)  # Compatibility. This will be removed in v4.1. Shorthand for NONE
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
