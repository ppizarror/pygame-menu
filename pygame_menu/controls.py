"""
pygame-menu
https://github.com/ppizarror/pygame-menu

CONTROLS
Default controls of Menu object and key definition.
"""

__all__ = [

    # Joy pad
    'JOY_AXIS_X',
    'JOY_AXIS_Y',
    'JOY_BUTTON_BACK',
    'JOY_BUTTON_SELECT',
    'JOY_DEADZONE',
    'JOY_DELAY',
    'JOY_DOWN',
    'JOY_LEFT',
    'JOY_REPEAT',
    'JOY_RIGHT',
    'JOY_UP',

    # Keyboard events
    'KEY_APPLY',
    'KEY_BACK',
    'KEY_CLOSE_MENU',
    'KEY_LEFT',
    'KEY_MOVE_DOWN',
    'KEY_MOVE_UP',
    'KEY_RIGHT',

    # Controller object
    'Controller'

]

# Imports
import pygame.locals as _locals
from pygame.event import Event as EventType
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from pygame_menu.menu import Menu
    from pygame_menu.widgets import Widget

# Joy pad
JOY_AXIS_X = 0
JOY_AXIS_Y = 1
JOY_BUTTON_BACK = 1
JOY_BUTTON_SELECT = 0
JOY_DEADZONE = 0.5
JOY_DELAY = 300  # ms
JOY_DOWN = (0, -1)
JOY_LEFT = (-1, 0)
JOY_REPEAT = 100  # ms
JOY_RIGHT = (1, 0)
JOY_UP = (0, 1)

# Keyboard events
KEY_APPLY = _locals.K_RETURN
KEY_BACK = _locals.K_BACKSPACE
KEY_CLOSE_MENU = _locals.K_ESCAPE
KEY_LEFT = _locals.K_LEFT
KEY_MOVE_DOWN = _locals.K_UP
KEY_MOVE_UP = _locals.K_DOWN  # Consider keys are "inverted"
KEY_RIGHT = _locals.K_RIGHT
KEY_TAB = _locals.K_TAB


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class Controller(object):
    """
    Controller class. Accepts any object and provides functions to handle each
    event.
    """

    def __init__(self) -> None:
        return

    def apply(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts apply. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.key == KEY_APPLY

    def back(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts back. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.key == KEY_BACK

    def close_menu(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts close menu. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.key == KEY_CLOSE_MENU

    def escape(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts escape. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.key == _locals.K_ESCAPE

    def joy_axis_x(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts joy movement on x-axis. Requires ``pygame.JOYAXISMOTION``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.axis == JOY_AXIS_X

    def joy_axis_y(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts joy movement on y-axis. Requires ``pygame.JOYAXISMOTION``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.axis == JOY_AXIS_Y

    def joy_back(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts joy back button. Requires ``pygame.JOYBUTTONDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.axis == JOY_AXIS_X

    def left(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts left. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.key == KEY_LEFT

    def move_down(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts move down. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.key == KEY_MOVE_DOWN

    def move_up(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts move up. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.key == KEY_MOVE_UP

    def right(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts right. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.key == KEY_RIGHT

    def tab(self, event: EventType, widget: Union['Menu', 'Widget']) -> bool:
        """
        Accepts tab. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.key == KEY_TAB
